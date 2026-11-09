"""Runs the unmodified v2 check_state.py `t1` and `collect`, with their output folder pointed at this package.

Why a wrapper: check_state.py is read-only toward work/, but its `t1` appends to and its `collect` adds files to
phase54_desktop_auto_smoke_v2/evidence/. Historical evidence must not change, so the module is imported as is and only its
EVID variable is set at run time. The file on disk is not edited; its SHA-256 is recorded with the output.

Usage: python -B run_readonly_checks.py
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
V2 = os.path.normpath(os.path.join(OUT, "..", "phase54_desktop_auto_smoke_v2"))
TOOL = os.path.join(V2, "_tools", "check_state.py")
DEST = os.path.join(OUT, "evidence", "v2_readonly_rerun")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tree(d):
    return {n: sha(os.path.join(d, n)) for n in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, n))}


def run(fn, *a):
    buf = io.StringIO()
    code = 0
    with contextlib.redirect_stdout(buf):
        try:
            fn(*a)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
    return code, buf.getvalue()


def main():
    os.makedirs(DEST, exist_ok=False)
    before = tree(os.path.join(V2, "evidence"))
    spec = importlib.util.spec_from_file_location("check_state", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.EVID = DEST
    t1_code, t1_out = run(mod.stage_check, "t1")
    coll_code, coll_out = run(mod.collect, [])
    with open(os.path.join(DEST, "t1_stdout.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(t1_out)
    with open(os.path.join(DEST, "collect_stdout.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(coll_out)
    after = tree(os.path.join(V2, "evidence"))
    rec = {"tool": "phase54_desktop_auto_smoke_v2/_tools/check_state.py", "tool_sha256": sha(TOOL), "stages_run": ["t1", "collect"], "t1_exit_code": t1_code, "collect_exit_code": coll_code, "output_folder_override": "evidence/v2_readonly_rerun (EVID set at run time; tool file unchanged)", "v2_evidence_files_before": before, "v2_evidence_unchanged": before == after}
    with open(os.path.join(DEST, "RERUN_RECORD.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "v2_evidence_files_before"}, indent=1))


if __name__ == "__main__":
    main()
