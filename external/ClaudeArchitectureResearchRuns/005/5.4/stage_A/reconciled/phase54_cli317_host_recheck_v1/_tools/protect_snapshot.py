"""Hash every file in the 5.4 project tree except this task's output folder (read-only toward everything else).

Usage (any working directory):
  python -B protect_snapshot.py snapshot                 write _baseline/PROTECTED_BASELINE.json (refuses to overwrite)
  python -B protect_snapshot.py verify <result-name>     write _baseline/<result-name>.json with added/removed/changed
  python -B protect_snapshot.py manifest-check           verify phase54_final_acceptance_v1 against its own FILE_MANIFEST.json
  python -B protect_snapshot.py strays                   list every directory under the frozen release that is not a known top-level entry
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
PRED = os.path.join(OUT, "..", "phase54_final_acceptance_v1")
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
    if mode == "snapshot":
        p = os.path.join(BASE, "PROTECTED_BASELINE.json")
        if os.path.exists(p):
            raise SystemExit("baseline exists; refusing to overwrite")
        files, dirs = walk()
        wjson(p, {"root": "005/5.4", "excluded": EXCLUDE.replace(os.sep, "/"), "file_count": len(files),
                  "dir_count": len(dirs), "files": files, "dirs": dirs})
        print(f"snapshot: {len(files)} files, {len(dirs)} dirs")
    elif mode == "verify":
        with open(os.path.join(BASE, "PROTECTED_BASELINE.json"), encoding="utf-8") as f:
            b = json.load(f)
        files, dirs = walk()
        added = sorted(set(files) - set(b["files"]))
        removed = sorted(set(b["files"]) - set(files))
        changed = sorted(k for k in set(files) & set(b["files"]) if files[k] != b["files"][k])
        dirs_added = sorted(set(dirs) - set(b["dirs"]))
        dirs_removed = sorted(set(b["dirs"]) - set(dirs))
        r = {"baseline_files": len(b["files"]), "current_files": len(files), "added": added, "removed": removed,
             "changed": changed, "dirs_added": dirs_added, "dirs_removed": dirs_removed,
             "verdict": "UNCHANGED" if not (added or removed or changed or dirs_added or dirs_removed) else "DRIFT"}
        wjson(os.path.join(BASE, sys.argv[2] + ".json"), r)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in r.items()}))
        for k in ("added", "removed", "changed", "dirs_added", "dirs_removed"):
            for x in r[k][:20]:
                print(k, x)
    elif mode == "manifest-check":
        with open(os.path.join(PRED, "FILE_MANIFEST.json"), encoding="utf-8") as f:
            m = json.load(f)
        rows = m["output_files"]
        sections = {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in m.items()}
        bad, missing, n = [], [], 0
        no_hash = [r.get("path") for r in rows if "sha256" not in r]
        for row in rows:
            if "sha256" not in row:
                continue
            rel, want = row["path"], row["sha256"]
            p = os.path.join(PRED, rel)
            n += 1
            if not os.path.exists(p):
                missing.append(rel)
            elif sha256(p) != want:
                bad.append(rel)
        r = {"manifest_sections": sections, "output_file_entries": n, "entries_without_hash": no_hash, "missing": missing, "mismatched": bad,
             "note": "FILE_MANIFEST.json lists its own hash-independent entries; a row for FILE_MANIFEST.json itself or for files rewritten after its generation would appear under mismatched and is reported, not hidden.",
             "verdict": "MATCH" if not (bad or missing) else "MISMATCH"}
        wjson(os.path.join(BASE, "PREDECESSOR_MANIFEST_CHECK.json"), r)
        print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in r.items()}))
    elif mode == "strays":
        rel = os.path.join(PRED, "release")
        known = {"candidates", "CANDIDATE_FREEZE_MANIFEST.json", "CANDIDATE_FREEZE_MANIFEST.json.sha256",
                 "make_working_copy.py", "RELEASE_PROVENANCE.md", "verify_release.py"}
        entries = sorted(os.listdir(rel))
        print(json.dumps({"entries": entries, "unknown": [e for e in entries if e not in known]}))
    else:
        raise SystemExit("mode must be snapshot|verify|manifest-check|strays")


if __name__ == "__main__":
    main()
