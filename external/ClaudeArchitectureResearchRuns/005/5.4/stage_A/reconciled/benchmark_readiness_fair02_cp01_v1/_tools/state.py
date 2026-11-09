"""Update STATE.json units. Usage: python -B _tools/state.py <unit> <status> [note]"""
import json, sys, datetime
p = "STATE.json"
s = json.load(open(p, encoding="utf-8"))
unit, status = sys.argv[1], sys.argv[2]
if unit not in s["units"]:
    raise SystemExit(f"unknown unit {unit}")
s["units"][unit] = status
if len(sys.argv) > 3:
    s["notes"].append({"at": datetime.datetime.now().isoformat(timespec="seconds"), "unit": unit, "note": sys.argv[3]})
if all(v == "DONE" for v in s["units"].values()):
    s["status"] = "COMPLETE"
json.dump(s, open(p, "w", encoding="utf-8", newline="\n"), indent=2)
print(unit, status)
