"""Durable checkpoint for the CLI 2.1.317 recheck. Writes STATE.json atomically (temp file + replace).

Usage: python -B state.py show | start <UNIT> | done <UNIT> [note] | note <UNIT> <text>
"""
import datetime
import json
import os
import sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(OUT, "STATE.json")
UNITS = ["S0_BASELINE_AND_INCIDENT", "S1_CLI_IDENTITY", "S2_DESIGN_AND_FIXTURES", "S3_LIVE_FAILURE_CASES", "S4_LIVE_SMOKE",
         "S5_INVESTIGATION", "S6_MATRIX_AND_REPORTS", "S7_FINAL_VALIDATION"]


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def load():
    if os.path.exists(P):
        with open(P, encoding="utf-8") as f:
            return json.load(f)
    return {"task": "Experiment 005 / Phase 5.4 - Claude Code 2.1.317 live hook compatibility recheck",
            "output_dir": "stage_A/reconciled/phase54_cli317_host_recheck_v1", "started": now(), "status": "IN_PROGRESS",
            "target_cli_version": "2.1.317", "units": {u: "PENDING" for u in UNITS}, "notes": [], "next_unit": UNITS[0]}


def save(s):
    pending = [u for u in UNITS if s["units"].get(u) != "DONE"]
    s["next_unit"] = pending[0] if pending else None
    s["status"] = "COMPLETE" if not pending else "IN_PROGRESS"
    s["updated"] = now()
    tmp = P + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(s, f, indent=2)
        f.write("\n")
    os.replace(tmp, P)


def mark(unit, value, note=None):
    s = load()
    if unit not in s["units"]:
        raise SystemExit("unknown unit " + unit)
    s["units"][unit] = value
    if note:
        s["notes"].append({"at": now(), "unit": unit, "note": note})
    save(s)


def note(unit, text):
    s = load()
    s["notes"].append({"at": now(), "unit": unit, "note": text})
    save(s)


def main():
    cmd = sys.argv[1]
    if cmd == "show":
        s = load()
        print(json.dumps({k: s[k] for k in ("status", "units", "next_unit")}, indent=1))
    elif cmd == "start":
        mark(sys.argv[2], "IN_PROGRESS", sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "done":
        mark(sys.argv[2], "DONE", sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "note":
        note(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit("usage: show | start U | done U [note] | note U text")


if __name__ == "__main__":
    main()
