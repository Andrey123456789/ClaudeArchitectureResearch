"""Hash every file in the 5.4 project tree except this task's output folder.

Usage (from the 5.4 root):
  python -B <out>/_tools/protect_snapshot.py snapshot <out>/_baseline/PROTECTED_BASELINE_SHA256.json
  python -B <out>/_tools/protect_snapshot.py verify   <out>/_baseline/PROTECTED_BASELINE_SHA256.json <result.json>

Used to prove that candidate templates, Step 2 v3, Step 3, originals, Codex passes and
the kit are unchanged by this task.
"""
import hashlib, json, os, sys

ROOT = os.getcwd()
EXCLUDE = os.path.normpath("stage_A/reconciled/benchmark_readiness_fair02_cp01_v1")


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


def main():
    mode, baseline = sys.argv[1], sys.argv[2]
    if mode == "snapshot":
        files = walk()
        with open(baseline, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"root": "005/5.4", "excluded": EXCLUDE.replace(os.sep, "/"),
                       "file_count": len(files), "files": files}, f, indent=0, sort_keys=True)
        print(f"snapshot: {len(files)} files")
    elif mode == "verify":
        with open(baseline, encoding="utf-8") as f:
            base = json.load(f)["files"]
        now = walk()
        added = sorted(set(now) - set(base))
        removed = sorted(set(base) - set(now))
        changed = sorted(k for k in set(base) & set(now) if base[k] != now[k])
        result = {"baseline_files": len(base), "current_files": len(now),
                  "added": added, "removed": removed, "changed": changed,
                  "verdict": "UNCHANGED" if not (added or removed or changed) else "DRIFT"}
        with open(sys.argv[3], "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in result.items()}))
    else:
        raise SystemExit("mode must be snapshot|verify")


if __name__ == "__main__":
    main()
