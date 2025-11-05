#!/usr/bin/env python3
"""
Banking Catalogue Orchestrator

Locates, classifies, and catalogues banking statements and transaction
spreadsheets across the local FIELD, mirroring data from configured Notion
databases into a single SQLite ledger. The resulting catalogue supports
gap analysis so investigators can see which accounts and periods are
covered and which require follow-up requests.

Usage:
    python banking_catalogue.py run --config ../config/banking_catalogue_config.yml

Key features:
    • Recursive filesystem scan across configured roots with bank-aware
      keyword matching and extension filtering.
    • SQLite store (tables: files, bank_year_coverage, notion_records)
      for downstream analytics and cross references.
    • Optional Notion ingestion (requires `notion-client` package and
      integration token exposed via environment variable).
    • Priority gap detection based on expected years per bank, surfaced in
      `bank_year_coverage` and JSON summary output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover - configuration requires PyYAML
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

try:
    from notion_client import Client  # type: ignore
except ImportError:
    Client = None  # Notion integration remains optional


# ---------------------------------------------------------------------------
# Configuration models
# ---------------------------------------------------------------------------


@dataclass
class NotionDatabaseConfig:
    database_id: str
    name: str
    table_name: str
    title_property: Optional[str] = None
    account_property: Optional[str] = None
    year_property: Optional[str] = None


@dataclass
class NotionConfig:
    enabled: bool
    integration_token_env: str
    databases: List[NotionDatabaseConfig] = field(default_factory=list)


@dataclass
class CatalogueConfig:
    roots: List[Path]
    include_extensions: Set[str]
    bank_keywords: Dict[str, List[str]]
    output_database: Path
    report_path: Path
    expected_years: Dict[str, List[int]]
    notion: Optional[NotionConfig] = None
    hash_prefix_bytes: int = 0
    variance_snapshots: List[Path] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


YEAR_PATTERN = re.compile(r"(19|20)\d{2}")


def load_config(path: Path) -> CatalogueConfig:
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    roots = [Path(entry).expanduser() for entry in raw["roots"]]
    include_extensions = {ext.lower() for ext in raw.get("include_extensions", [])}
    bank_keywords = {}
    for bank, keywords in raw.get("bank_keywords", {}).items():
        normalized = []
        for kw in keywords:
            text = str(kw).lower()
            normalized.append(text)
        bank_keywords[bank] = normalized
    output_database = Path(raw["output_database"]).expanduser()
    report_path = Path(raw.get("report_path", output_database.with_suffix(".json"))).expanduser()
    expected_years = {
        bank: sorted({int(year) for year in years})
        for bank, years in raw.get("expected_years", {}).items()
    }
    hash_prefix_bytes = int(raw.get("hash_prefix_bytes", 0))
    variance_snapshots = [Path(p).expanduser() for p in raw.get("variance_snapshots", [])]

    notion_cfg = None
    notion_raw = raw.get("notion")
    if notion_raw:
        databases = [
            NotionDatabaseConfig(
                database_id=db["id"],
                name=db.get("name", db["id"]),
                table_name=db.get("table_name", f"notion_{idx}"),
                title_property=db.get("title_property"),
                account_property=db.get("account_property"),
                year_property=db.get("year_property"),
            )
            for idx, db in enumerate(notion_raw.get("databases", []), start=1)
        ]
        notion_cfg = NotionConfig(
            enabled=bool(notion_raw.get("enabled", True) and databases),
            integration_token_env=notion_raw.get("integration_token_env", "NOTION_TOKEN"),
            databases=databases,
        )

    return CatalogueConfig(
        roots=roots,
        include_extensions=include_extensions,
        bank_keywords=bank_keywords,
        output_database=output_database,
        report_path=report_path,
        expected_years=expected_years,
        notion=notion_cfg,
        hash_prefix_bytes=hash_prefix_bytes,
        variance_snapshots=variance_snapshots,
    )


def ensure_database(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            bank TEXT,
            filename TEXT,
            extension TEXT,
            size_bytes INTEGER,
            modified_at TEXT,
            detected_years TEXT,
            account_hint TEXT,
            hash_prefix TEXT,
            indexed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bank_year_coverage (
            bank TEXT NOT NULL,
            year INTEGER NOT NULL,
            file_count INTEGER NOT NULL,
            status TEXT NOT NULL,
            PRIMARY KEY (bank, year)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notion_records (
            record_id TEXT PRIMARY KEY,
            database_name TEXT NOT NULL,
            title TEXT,
            account_reference TEXT,
            year_reference TEXT,
            raw_json TEXT NOT NULL,
            synced_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS variance_snapshots (
            snapshot_path TEXT NOT NULL,
            domain TEXT NOT NULL,
            entry_path TEXT NOT NULL,
            classification TEXT NOT NULL,
            raw_json TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(snapshot_path, entry_path)
        )
        """
    )
    connection.commit()


def hash_prefix(path: Path, prefix_bytes: int) -> str:
    if prefix_bytes <= 0:
        return ""
    import hashlib

    hsh = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            chunk = handle.read(prefix_bytes)
            hsh.update(chunk)
    except (OSError, PermissionError):
        return ""
    return hsh.hexdigest()


def detect_bank(name: str, keywords_map: Dict[str, List[str]]) -> Optional[str]:
    lowered = name.lower()
    for bank, keywords in keywords_map.items():
        if any(keyword in lowered for keyword in keywords):
            return bank
    return None


def detect_years(text: str) -> List[int]:
    years = {int(match.group()) for match in YEAR_PATTERN.finditer(text)}
    return sorted(years)


def derive_account_hint(text: str) -> Optional[str]:
    account_pattern = re.compile(r"(?:CH|AU)?[0-9]{4,}")
    match = account_pattern.search(text.replace(" ", ""))
    return match.group(0) if match else None


def scan_files(config: CatalogueConfig) -> List[Dict[str, object]]:
    collected: List[Dict[str, object]] = []
    for root in config.roots:
        if not root.exists():
            continue
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            extension = file_path.suffix.lower()
            if config.include_extensions and extension not in config.include_extensions:
                continue
            bank = detect_bank(file_path.name, config.bank_keywords) or detect_bank(
                str(file_path.parent), config.bank_keywords
            )
            stat = file_path.stat()
            years = detect_years(file_path.stem)
            account_hint = derive_account_hint(file_path.stem)
            collected.append(
                {
                    "path": str(file_path.resolve()),
                    "bank": bank or "Unclassified",
                    "filename": file_path.name,
                    "extension": extension,
                    "size_bytes": stat.st_size,
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "detected_years": years,
                    "account_hint": account_hint,
                    "hash_prefix": hash_prefix(file_path, config.hash_prefix_bytes),
                }
            )
    return collected


def upsert_files(connection: sqlite3.Connection, records: Iterable[Dict[str, object]]) -> None:
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO files (
            path, bank, filename, extension, size_bytes,
            modified_at, detected_years, account_hint, hash_prefix, indexed_at
        ) VALUES (
            :path, :bank, :filename, :extension, :size_bytes,
            :modified_at, :detected_years_json, :account_hint, :hash_prefix, CURRENT_TIMESTAMP
        )
        ON CONFLICT(path) DO UPDATE SET
            bank=excluded.bank,
            filename=excluded.filename,
            extension=excluded.extension,
            size_bytes=excluded.size_bytes,
            modified_at=excluded.modified_at,
            detected_years=excluded.detected_years,
            account_hint=excluded.account_hint,
            hash_prefix=CASE
                WHEN excluded.hash_prefix != '' THEN excluded.hash_prefix
                ELSE files.hash_prefix
            END,
            indexed_at=CURRENT_TIMESTAMP
        """,
        [
            {
                **record,
                "detected_years_json": json.dumps(record["detected_years"]),
            }
            for record in records
        ],
    )
    connection.commit()


def update_coverage(connection: sqlite3.Connection, expected_years: Dict[str, List[int]]) -> Dict[str, Dict[str, object]]:
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bank_year_coverage")

    coverage_summary: Dict[str, Dict[str, object]] = {}

    for bank, years in expected_years.items():
        coverage_summary[bank] = {"expected_years": years, "missing_years": [], "coverage": {}}

    cursor.execute("SELECT bank, detected_years FROM files")
    rows = cursor.fetchall()

    coverage: Dict[Tuple[str, int], int] = {}
    for bank, years_json in rows:
        years = json.loads(years_json) if years_json else []
        for year in years:
            key = (bank, int(year))
            coverage[key] = coverage.get(key, 0) + 1

    for (bank, year), count in coverage.items():
        cursor.execute(
            """
            INSERT INTO bank_year_coverage (bank, year, file_count, status)
            VALUES (?, ?, ?, ?)
            """,
            (bank, year, count, "covered"),
        )
        if bank not in coverage_summary:
            coverage_summary[bank] = {"expected_years": [], "missing_years": [], "coverage": {}}
        coverage_summary[bank]["coverage"][year] = count

    for bank, expected in expected_years.items():
        missing = [
            year for year in expected if (bank, year) not in coverage or coverage[(bank, year)] == 0
        ]
        coverage_summary[bank]["missing_years"] = missing
        for year in missing:
            cursor.execute(
                """
                INSERT INTO bank_year_coverage (bank, year, file_count, status)
                VALUES (?, ?, 0, 'missing')
                ON CONFLICT(bank, year) DO UPDATE SET
                    status='missing'
                """,
                (bank, year),
            )

    connection.commit()
    return coverage_summary


def flatten_notion_property(prop: dict) -> Optional[str]:
    prop_type = prop.get("type")
    if prop_type == "title":
        return " ".join(part.get("plain_text", "") for part in prop.get("title", [])) or None
    if prop_type == "rich_text":
        return " ".join(part.get("plain_text", "") for part in prop.get("rich_text", [])) or None
    if prop_type == "number":
        value = prop.get("number")
        return str(value) if value is not None else None
    if prop_type == "select":
        selected = prop.get("select")
        return selected.get("name") if selected else None
    if prop_type == "multi_select":
        return ", ".join(option.get("name") for option in prop.get("multi_select", []))
    if prop_type == "date":
        date_obj = prop.get("date")
        return date_obj.get("start") if date_obj else None
    if prop_type == "relation":
        return ", ".join(rel.get("id") for rel in prop.get("relation", []))
    if prop_type == "checkbox":
        return "true" if prop.get("checkbox") else "false"
    if prop_type in {"url", "email", "phone_number"}:
        return prop.get(prop_type)
    return None


def sync_notion(connection: sqlite3.Connection, config: CatalogueConfig) -> List[Dict[str, str]]:
    if not config.notion or not config.notion.enabled or not config.notion.databases:
        return []
    if Client is None:
        print("Notion client not installed; skipping Notion sync", file=sys.stderr)
        return []

    token = os.getenv(config.notion.integration_token_env)
    if not token:
        print("Notion token not found; skipping Notion sync", file=sys.stderr)
        return []

    client = Client(auth=token)
    cursor = connection.cursor()
    synced_records: List[Dict[str, str]] = []

    for database in config.notion.databases:
        has_more = True
        next_cursor = None
        while has_more:
            response = client.databases.query(
                database_id=database.database_id,
                start_cursor=next_cursor,
                page_size=100,
            )
            for result in response.get("results", []):
                record_id = result["id"]
                properties = result.get("properties", {})
                title = None
                account_reference = None
                year_reference = None

                if database.title_property and database.title_property in properties:
                    title = flatten_notion_property(properties[database.title_property])
                if database.account_property and database.account_property in properties:
                    account_reference = flatten_notion_property(properties[database.account_property])
                if database.year_property and database.year_property in properties:
                    year_reference = flatten_notion_property(properties[database.year_property])

                cursor.execute(
                    """
                    INSERT INTO notion_records (
                        record_id, database_name, title, account_reference,
                        year_reference, raw_json, synced_at
                    ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(record_id) DO UPDATE SET
                        database_name=excluded.database_name,
                        title=excluded.title,
                        account_reference=excluded.account_reference,
                        year_reference=excluded.year_reference,
                        raw_json=excluded.raw_json,
                        synced_at=CURRENT_TIMESTAMP
                    """,
                    (
                        record_id,
                        database.name,
                        title,
                        account_reference,
                        year_reference,
                        json.dumps(result),
                    ),
                )

                synced_records.append(
                    {
                        "record_id": record_id,
                        "database": database.name,
                        "title": title or "",
                        "account_reference": account_reference or "",
                        "year_reference": year_reference or "",
                    }
                )

            has_more = response.get("has_more", False)
            next_cursor = response.get("next_cursor")

    connection.commit()
    return synced_records


def write_report(
    report_path: Path,
    files: List[Dict[str, object]],
    coverage: Dict[str, Dict[str, object]],
    notion_records: List[Dict[str, str]],
    variance_snapshots: List[Dict[str, str]],
) -> None:
    summary = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_files": len(files),
        "banks": {},
        "notion_records": notion_records,
        "variance_snapshots": variance_snapshots,
    }
    for record in files:
        bank = record["bank"]
        summary["banks"].setdefault(bank, {"count": 0, "years": set()})
        summary["banks"][bank]["count"] += 1
        for year in record["detected_years"]:
            summary["banks"][bank]["years"].add(year)

    for bank, data in summary["banks"].items():
        data["years"] = sorted(data["years"])

    for bank, info in coverage.items():
        summary["banks"].setdefault(bank, {"count": 0, "years": []})
        summary["banks"][bank]["expected_years"] = info.get("expected_years", [])
        summary["banks"][bank]["missing_years"] = info.get("missing_years", [])

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)


# ---------------------------------------------------------------------------
# CLI entry points
# ---------------------------------------------------------------------------


def command_run(args: argparse.Namespace) -> None:
    config_path = Path(args.config).expanduser()
    config = load_config(config_path)

    config.output_database.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(config.output_database))
    ensure_database(connection)

    files = scan_files(config)
    upsert_files(connection, files)

    coverage = update_coverage(connection, config.expected_years)

    notion_records = sync_notion(connection, config)

    variance_details = import_variance_snapshots(connection, config)

    write_report(config.report_path, files, coverage, notion_records, variance_details)

    print(f"Indexed {len(files)} files into {config.output_database}")
    print(f"Coverage summary written to {config.report_path}")
    if notion_records:
        print(f"Synchronized {len(notion_records)} Notion records")
    else:
        print("No Notion records synchronized (see logs for details)")
    if variance_details:
        for item in variance_details:
            print(f"Imported variance snapshot {item['snapshot']} ({item['entries']} entries)")
    else:
        print("No variance snapshots processed")


def import_variance_snapshots(connection: sqlite3.Connection, config: CatalogueConfig) -> List[Dict[str, str]]:
    if not config.variance_snapshots:
        return []

    cursor = connection.cursor()
    imported: List[Dict[str, str]] = []

    for snapshot_path in config.variance_snapshots:
        if not snapshot_path.exists():
            print(f"Variance snapshot missing: {snapshot_path}", file=sys.stderr)
            continue
        try:
            with snapshot_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Failed to load snapshot {snapshot_path}: {exc}", file=sys.stderr)
            continue

        domain = snapshot_path.stem.split("_")[0]
        raw_json = json.dumps(data)

        for entry_path, classification in data.items():
            entry_payload = json.dumps({entry_path: classification})
            cursor.execute(
                """
                INSERT INTO variance_snapshots (
                    snapshot_path, domain, entry_path, classification, raw_json, imported_at
                ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(snapshot_path, entry_path) DO UPDATE SET
                    classification=excluded.classification,
                    raw_json=excluded.raw_json,
                    imported_at=CURRENT_TIMESTAMP
                """,
                (
                    str(snapshot_path),
                    domain,
                    entry_path,
                    classification,
                    entry_payload,
                ),
            )
        imported.append({"snapshot": str(snapshot_path), "domain": domain, "entries": len(data)})

    connection.commit()
    return imported


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Banking catalogue automation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Execute a full scan + sync")
    run_parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML configuration file",
    )
    run_parser.set_defaults(func=command_run)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
