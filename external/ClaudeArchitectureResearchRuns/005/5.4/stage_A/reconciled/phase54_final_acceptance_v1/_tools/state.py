"""Durable checkpoints for the Phase 5.4 final acceptance task.

Run from this task's output folder:
  python -B _tools/state.py done <UNIT> "<note>"     mark a unit DONE with a timestamped note
  python -B _tools/state.py note <UNIT> "<note>"     add a note without changing status
  python -B _tools/state.py show
"""
import datetime
import json
import os
import sys

UNITS = [
    "S1_PREDECESSOR_VERIFICATION",
    "S2_CANDIDATE_FREEZE",
    "S3_LIVE_HOST_PILOT",
    "S4_CLOSURE_REVIEW",
    "S5_REPORTS_AND_HANDOFF",
    "S6_FINAL_VALIDATION",
]
P = "STATE.json"


def load():
    if os.path.exists(P):
        with open(P, encoding="utf-8") as f:
            return json.load(f)
    return {"task": "Experiment 005 / Phase 5.4 - final candidate freeze, live host acceptance, formal closure",
            "output_dir": "stage_A/reconciled/phase54_final_acceptance_v1", "started": "2026-11-07",
            "status": "IN_PROGRESS", "units": {u: "PENDING" for u in UNITS}, "notes": []}


def save(s):
    with open(P, "w", encoding="utf-8", newline="\n") as f:
        json.dump(s, f, indent=2)
        f.write("\n")


def main():
    s = load()
    cmd = sys.argv[1]
    if cmd in ("done", "note"):
        unit, note = sys.argv[2], sys.argv[3]
        if unit not in s["units"]:
            raise SystemExit(f"unknown unit {unit}")
        if cmd == "done":
            s["units"][unit] = "DONE"
        s["notes"].append({"at": datetime.datetime.now().isoformat(timespec="seconds"), "unit": unit, "note": note})
        nxt = next((u for u in UNITS if s["units"][u] != "DONE"), None)
        s["next_unit"] = nxt
        s["status"] = "COMPLETE" if nxt is None else "IN_PROGRESS"
        save(s)
    print(json.dumps({"status": s["status"], "units": s["units"], "next_unit": s.get("next_unit")}, indent=1))


if __name__ == "__main__":
    main()
