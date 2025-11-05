#!/usr/bin/env python3
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta

TARGET_DIRS = [
    "/Volumes/Akron/▼TATA/_vault/BANK_RECORDS/financial_management/",
    "/Volumes/Akron/▼TATA/_vault/corporate_entities/",
]
TARGET_PORTS = [963, 5815, 16354]

SCAN_WINDOW_HOURS = 72  # recent change window
LARGE_FILE_BYTES = 200 * 1024 * 1024  # 200MB threshold
VALID_FILE_EXTENSIONS = {".json", ".csv", ".txt", ".md"}


def file_sha256(path, block_size=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
    return h.hexdigest()


def check_port_in_use(port):
    # Use lsof if available for detailed info; fallback to socket connect check
    try:
        proc = subprocess.run(
            ["lsof", "-nP", f"-i:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3,
        )
        return proc.stdout.strip()
    except Exception:
        # fallback: try connecting
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect(("127.0.0.1", port))
            s.close()
            return f"CONNECTED:127.0.0.1:{port}"
        except Exception:
            return ""


def scan_dir(path):
    findings = {
        "path": path,
        "missing": False,
        "zero_byte_files": [],
        "large_files": [],
        "unexpected_extensions": [],
        "recent_changes": [],
        "permission_anomalies": [],
        "hashes": {},
        "errors": [],
    }
    if not os.path.exists(path):
        findings["missing"] = True
        return findings

    recent_cutoff = time.time() - (SCAN_WINDOW_HOURS * 3600)

    for root, dirs, files in os.walk(path):
        for name in files:
            fp = os.path.join(root, name)
            try:
                st = os.stat(fp)
                # zero-byte
                if st.st_size == 0:
                    findings["zero_byte_files"].append(fp)
                # large files
                if st.st_size >= LARGE_FILE_BYTES:
                    findings["large_files"].append({"path": fp, "bytes": st.st_size})
                # extensions
                _, ext = os.path.splitext(name)
                if ext and ext.lower() not in VALID_FILE_EXTENSIONS:
                    findings["unexpected_extensions"].append(fp)
                # recent modifications
                if st.st_mtime >= recent_cutoff:
                    findings["recent_changes"].append({
                        "path": fp,
                        "modified_at": datetime.fromtimestamp(st.st_mtime).isoformat(),
                        "bytes": st.st_size,
                    })
                # simple permission check (644-ish for files)
                mode = st.st_mode & 0o777
                if mode not in (0o644, 0o640, 0o600):
                    findings["permission_anomalies"].append({"path": fp, "mode": oct(mode)})
                # hash small/medium files only (<= 50MB)
                if st.st_size <= 50 * 1024 * 1024:
                    findings["hashes"][fp] = file_sha256(fp)
            except Exception as e:
                findings["errors"].append({"path": fp, "error": str(e)})
    return findings


def main():
    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "target_dirs": TARGET_DIRS,
        "ports": {},
        "directories": [],
    }

    # Ports
    for p in TARGET_PORTS:
        status = check_port_in_use(p)
        report["ports"][str(p)] = {
            "in_use": bool(status),
            "detail": status[:2000],  # cap
        }

    # Directories
    for d in TARGET_DIRS:
        report["directories"].append(scan_dir(d))

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    sys.exit(main())
