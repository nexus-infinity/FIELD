#!/usr/bin/env python3
import os, json, sys, datetime as dt

BASE = "/Users/jbear/FIELD-DEV"
EVENTS = f"{BASE}/logs/petal_lapaz.events.jsonl"

def emit(kind, data):
    rec = {
        "ts": dt.datetime.utcnow().isoformat()+"Z",
        "petal": "PETAL_LAPAZ_10_16_SHOWERS",
        "kind": kind,
        "data": data
    }
    os.makedirs(os.path.dirname(EVENTS), exist_ok=True)
    with open(EVENTS, "a") as f: f.write(json.dumps(rec)+"\n")
    print(f"➤ event: {kind}")

if __name__ == "__main__":
    # Usage: emit_event.py carrier_lock on|off  OR daily_pulse present|absent
    if len(sys.argv) < 3:
        print("Usage: emit_event.py <carrier_lock|daily_pulse|note> <value>")
        sys.exit(1)
    kind = sys.argv[1]
    value = " ".join(sys.argv[2:])
    emit(kind, {"value": value})
