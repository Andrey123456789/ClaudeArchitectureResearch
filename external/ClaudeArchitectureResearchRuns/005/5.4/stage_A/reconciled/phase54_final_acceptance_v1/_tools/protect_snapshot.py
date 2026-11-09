"""Hash every file in the 5.4 project tree except this task's output folder (read-only toward everything else).

Usage (from the 5.4 root):
  python -B <out>/_tools/protect_snapshot.py snapshot <baseline.json>
  python -B <out>/_tools/protect_snapshot.py verify   <baseline.json> <result.json>
  python -B <out>/_tools/protect_snapshot.py compare-kit76 <baseline.json> <result.json>

snapshot/verify prove that inputs, Codex passes, Step 2 v1-v3, Step 3, kit 76 and candidate
sources are unchanged by this task. compare-kit76 compares this task's baseline with the
kit 76 baseline (which excluded the kit 76 folder) to show nothing changed between kit 76's
end and this task's start.
"""
import hashlib
import json
import os
import sys

ROOT = os.getcwd()
EXCLUDE = os.path.normpath("stage_A/reconciled/phase54_final_acceptance_v1")
KIT76 = "stage_A/reconciled/benchmark_readiness_fair02_cp01_v1"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk():
    out = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.normpath(os.path.relpath(dirpath, ROOT))
        if rel_dir == EXCLUDE or rel_dir.startswith(EXCLUDE + os.sep):
            dirnames[:] = []
            continue
        dirnames.sort()
        for name in sorted(filenames):
            rel = os.path.normpath(os.path.join(rel_dir, name)).replace(os.sep, "/")
            out[rel] = sha256(os.path.join(dirpath, name))
    return out


def diff(base, now):
    added = sorted(set(now) - set(base))
    removed = sorted(set(base) - set(now))
    changed = sorted(k for k in set(base) & set(now) if base[k] != now[k])
    return added, removed, changed


def main():
    mode, baseline = sys.argv[1], sys.argv[2]
    if mode == "snapshot":
        if os.path.exists(baseline):
            raise SystemExit("baseline exists; refusing to overwrite")
        files = walk()
        with open(baseline, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"root": "005/5.4", "excluded": EXCLUDE.replace(os.sep, "/"),
                       "file_count": len(files), "files": files}, f, indent=0, sort_keys=True)
        print(f"snapshot: {len(files)} files")
    elif mode == "verify":
        with open(baseline, encoding="utf-8") as f:
            base = json.load(f)["files"]
        now = walk()
        added, removed, changed = diff(base, now)
        result = {"baseline_files": len(base), "current_files": len(now),
                  "added": added, "removed": removed, "changed": changed,
                  "verdict": "UNCHANGED" if not (added or removed or changed) else "DRIFT"}
        with open(sys.argv[3], "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in result.items()}))
    elif mode == "compare-kit76":
        with open(baseline, encoding="utf-8") as f:
            mine = json.load(f)["files"]
        with open(os.path.join(KIT76, "_baseline/PROTECTED_BASELINE_SHA256.json"), encoding="utf-8") as f:
            k76 = json.load(f)["files"]
        outside = {k: v for k, v in mine.items() if not k.startswith(KIT76 + "/")}
        added, removed, changed = diff(k76, outside)
        result = {"kit76_baseline_files": len(k76), "this_baseline_files_outside_kit76": len(outside),
                  "added_since_kit76_start": added, "removed_since_kit76_start": removed,
                  "changed_since_kit76_start": changed,
                  "verdict": "UNCHANGED_SINCE_KIT76" if not (added or removed or changed) else "DRIFT_SINCE_KIT76"}
        with open(sys.argv[3], "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in result.items()}))
    else:
        raise SystemExit("mode must be snapshot|verify|compare-kit76")


if __name__ == "__main__":
    main()
