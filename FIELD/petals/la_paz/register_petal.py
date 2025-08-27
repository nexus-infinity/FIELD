#!/usr/bin/env python3
import os, json, yaml, time, datetime as dt, pathlib, sys

BASE = "/Users/jbear/FIELD-DEV"
PETAL_DIR = f"{BASE}/field/petals/la_paz"
REGISTRY_DIR = f"{BASE}/field/registry"
AUDIT = f"{BASE}/logs/petal_lapaz.audit.jsonl"

def jwrite(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: json.dump(obj, f, indent=2)

def jappend(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    obj["ts"] = dt.datetime.utcnow().isoformat()+"Z"
    with open(path, "a") as f: f.write(json.dumps(obj)+"\n")

def load_yaml(p):
    with open(p, "r") as f:
        return yaml.safe_load(f)

def main():
    y = load_yaml(f"{PETAL_DIR}/petal.yml")
    c = json.load(open(f"{PETAL_DIR}/constants.json"))
    reg_key = y["outputs"]["registry_key"]

    registry_path = f"{REGISTRY_DIR}/{reg_key}.json"
    payload = {
        "id": y["id"],
        "name": y["name"],
        "version": y["version"],
        "symbol": y["symbol"],
        "summary": y["summary"],
        "coords": y["coords"],
        "archetype": y["archetype"],
        "band": c["band_celsius"],
        "altitude_m": c["altitude_m"],
        "pattern": c["pattern"],
        "signals": c["signals"],
        "paths": {
            "audit": y["logs"]["audit"],
            "events": y["logs"]["events"],
            "registry_file": registry_path
        }
    }
    jwrite(registry_path, payload)
    jappend(AUDIT, {"kind":"register", "registry": registry_path, "id": y["id"]})
    print(f"✅ Registered {y['name']} → {registry_path}")

if __name__ == "__main__":
    # lazy import yaml if needed
    try:
        import yaml  # noqa
    except Exception:
        print("Installing pyyaml locally...")
        os.system(f"{sys.executable} -m pip install --user pyyaml >/dev/null 2>&1")
    main()
