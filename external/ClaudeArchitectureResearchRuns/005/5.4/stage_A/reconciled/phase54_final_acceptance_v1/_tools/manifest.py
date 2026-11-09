"""Write FILE_MANIFEST.json for this task's output folder.

Run from this task's output folder:  python -B _tools/manifest.py
Every authored file is listed with SHA-256 and size. Bulk pilot fixtures (each case's work/, static/work/, tmp/,
npm-cache/ and nuget-packages/ directories: candidate working copies, throw-away Git repositories and host
scratch files) are listed as one aggregate entry per directory (file count, bytes, tree SHA-256).
Mutable bookkeeping files are listed without hashes.
"""
import hashlib
import json
import os
import platform

MUTABLE = {"STATE.json", "RESUME.md", "FILE_MANIFEST.json", "VALIDATION_REPORT.json"}
BULK = {"work", "tmp", "npm-cache", "nuget-packages"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def role(rel):
    for pre, r in (("release/candidates/", "frozen candidate file"), ("release/", "release manifest, provenance, utility"),
                   ("release_verification/", "freeze verification evidence"), ("live_host_pilot/", "live host pilot evidence"),
                   ("closure_review/", "closure review evidence"), ("predecessor/", "predecessor verification"),
                   ("_tools/", "task tool"), ("_baseline/", "protected-input baseline")):
        if rel.startswith(pre):
            return r
    return "top-level deliverable"


def main():
    files, bulk = [], []
    for dp, dn, fn in os.walk("."):
        dn.sort()
        rel_dir = os.path.relpath(dp, ".").replace(os.sep, "/")
        if rel_dir.startswith("live_host_pilot/") and os.path.basename(dp) in BULK:
            n, size, h = 0, 0, hashlib.sha256()
            for dp2, dn2, fn2 in os.walk(dp):
                dn2.sort()
                for name in sorted(fn2):
                    p = os.path.join(dp2, name)
                    r = os.path.relpath(p, dp).replace(os.sep, "/")
                    h.update(f"{r}\t{sha(p)}\n".encode("utf-8"))
                    n += 1
                    size += os.path.getsize(p)
            bulk.append({"dir": rel_dir, "files": n, "bytes": size, "tree_sha256": h.hexdigest()})
            dn[:] = []
            continue
        if "__pycache__" in rel_dir:
            continue
        for name in sorted(fn):
            rel = (name if rel_dir == "." else f"{rel_dir}/{name}")
            p = os.path.join(dp, name)
            row = {"path": rel, "role": role(rel), "bytes": os.path.getsize(p)}
            if rel not in MUTABLE:
                row["sha256"] = sha(p)
            files.append(row)
    out = {"task": "Experiment 005 / Phase 5.4 final acceptance (phase54_final_acceptance_v1)",
           "environment": {"python": platform.python_version(), "os": platform.platform()},
           "output_files": files, "output_file_count": len(files), "bulk_fixture_dirs": bulk,
           "external_side_effects": {
               "user_profile": "23 empty folders under %USERPROFILE%/.claude/projects/ created by the headless pilot sessions (no files; --no-session-persistence)",
               "plan_usage": "18 candidate + 5 synthetic headless Claude Code sessions on the user's claude.ai login (reported cost about USD 0.06)",
               "network": "only the Claude Code host's own API connection; npm forced offline to 127.0.0.1:9; no package feed contacted",
               "git": "git init/commit only inside throw-away fixture repositories under live_host_pilot/",
               "installed": "nothing"}}
    with open("FILE_MANIFEST.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
    print(f"files {len(files)}, bulk dirs {len(bulk)}")


if __name__ == "__main__":
    main()
