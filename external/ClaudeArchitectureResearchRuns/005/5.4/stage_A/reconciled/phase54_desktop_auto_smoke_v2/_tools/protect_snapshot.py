"""Hash every file in the 5.4 project tree except this task's output folder (read-only toward everything else).

Usage (any working directory; always python -B):
  python -B protect_snapshot.py snapshot        write _baseline/PROTECTED_BASELINE.json (refuses to overwrite)
  python -B protect_snapshot.py verify          write _baseline/PROTECTED_VERIFY.json with added/removed/changed
  python -B protect_snapshot.py prior           compare the baseline with the earlier recheck baseline and that folder's own manifest
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
RECHECK = os.path.normpath(os.path.join(OUT, "..", "phase54_cli317_host_recheck_v1"))
BASE = os.path.join(OUT, "_baseline")
EXCLUDE = os.path.normpath(os.path.relpath(OUT, ROOT))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk():
    out, dirs = {}, []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.normpath(os.path.relpath(dirpath, ROOT))
        if rel_dir == EXCLUDE or rel_dir.startswith(EXCLUDE + os.sep):
            dirnames[:] = []
            continue
        dirnames.sort()
        dirs.append(rel_dir.replace(os.sep, "/"))
        for name in sorted(filenames):
            rel = os.path.normpath(os.path.join(rel_dir, name)).replace(os.sep, "/")
            out[rel] = sha256(os.path.join(dirpath, name))
    return out, dirs


def wjson(p, obj):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write("\n")


def main():
    mode = sys.argv[1]
    bp = os.path.join(BASE, "PROTECTED_BASELINE.json")
    if mode == "snapshot":
        if os.path.exists(bp):
            raise SystemExit("baseline exists; refusing to overwrite")
        files, dirs = walk()
        wjson(bp, {"root": "005/5.4", "excluded": EXCLUDE.replace(os.sep, "/"), "file_count": len(files), "dir_count": len(dirs), "files": files, "dirs": dirs})
        print(f"snapshot: {len(files)} files, {len(dirs)} dirs")
    elif mode == "verify":
        b = json.load(open(bp, encoding="utf-8"))
        files, dirs = walk()
        added = sorted(set(files) - set(b["files"]))
        removed = sorted(set(b["files"]) - set(files))
        changed = sorted(k for k in set(files) & set(b["files"]) if files[k] != b["files"][k])
        dirs_added = sorted(set(dirs) - set(b["dirs"]))
        dirs_removed = sorted(set(b["dirs"]) - set(dirs))
        r = {"baseline_files": len(b["files"]), "current_files": len(files), "added": added, "removed": removed, "changed": changed, "dirs_added": dirs_added, "dirs_removed": dirs_removed,
             "verdict": "UNCHANGED" if not (added or removed or changed or dirs_added or dirs_removed) else "DRIFT"}
        wjson(os.path.join(BASE, "PROTECTED_VERIFY.json"), r)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in r.items()}))
        for k in ("added", "removed", "changed", "dirs_added", "dirs_removed"):
            for x in r[k][:20]:
                print(k, x)
    elif mode == "prior":
        b = json.load(open(bp, encoding="utf-8"))["files"]
        old = json.load(open(os.path.join(RECHECK, "_baseline", "PROTECTED_BASELINE.json"), encoding="utf-8"))["files"]
        diff = sorted(k for k, v in old.items() if b.get(k) != v)
        m = json.load(open(os.path.join(RECHECK, "FILE_MANIFEST.json"), encoding="utf-8"))
        bad = [r["path"] for r in m["output_files"] if not os.path.exists(os.path.join(RECHECK, r["path"])) or sha256(os.path.join(RECHECK, r["path"])) != r["sha256"]]
        r = {"recheck_baseline_files": len(old), "recheck_baseline_files_differing_now": diff, "recheck_manifest_entries": len(m["output_files"]), "recheck_manifest_mismatches": bad,
             "verdict": "UNCHANGED" if not (diff or bad) else "DIFFERENCES"}
        wjson(os.path.join(BASE, "COMPARE_WITH_RECHECK.json"), r)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in r.items()}))
        for x in (diff + bad)[:20]:
            print("diff", x)
    else:
        raise SystemExit("mode must be snapshot|verify|prior")


if __name__ == "__main__":
    main()
