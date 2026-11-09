"""Create an independent, writable working copy of one released candidate for a benchmark run.

Usage:
  python -B make_working_copy.py <candidate> <destination> [--provenance FILE]

- <candidate> is one of M, M1, L0, L1, K0, K1.
- <destination> must not exist or must be an empty directory, and must lie outside this release folder.
- The released template is hash-verified against CANDIDATE_FREEZE_MANIFEST.json before copying.
- Files are copied content-only (shutil.copyfile): the copy is writable and the frozen snapshot is never opened for writing.
- The copy is re-hashed; a provenance record is written next to the destination (default: <destination>.provenance.json),
  never inside it, so the candidate tree the agent sees contains exactly the released files.
Exit code 0 = copy created and verified.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", choices=CANDS)
    ap.add_argument("destination")
    ap.add_argument("--provenance")
    a = ap.parse_args()

    dest = os.path.abspath(a.destination)
    if os.path.commonpath([dest, HERE]) == HERE:
        raise SystemExit("destination is inside the frozen release folder; refusing")
    if os.path.exists(dest) and (not os.path.isdir(dest) or os.listdir(dest)):
        raise SystemExit("destination exists and is not an empty directory; refusing")
    mpath = os.path.join(HERE, "CANDIDATE_FREEZE_MANIFEST.json")
    if sha(mpath) != open(mpath + ".sha256", encoding="utf-8").read().split()[0]:
        raise SystemExit("manifest does not match its .sha256 sidecar; run verify_release.py")
    man = json.load(open(mpath, encoding="utf-8"))
    files = man["candidates"][a.candidate]["files"]
    src_root = os.path.join(HERE, "candidates", a.candidate, "template")
    for rel, row in files.items():
        if sha(os.path.join(src_root, rel)) != row["sha256"]:
            raise SystemExit(f"released file {rel} differs from the manifest; run verify_release.py")
    for rel in files:
        d = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(os.path.join(src_root, rel), d)
    bad = [rel for rel, row in files.items() if sha(os.path.join(dest, rel)) != row["sha256"]]
    if bad:
        raise SystemExit(f"copy verification failed for {bad}")
    prov = {"release_id": man["release_id"], "candidate": a.candidate, "destination": dest,
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "files": len(files), "tree_sha256": man["candidates"][a.candidate]["tree_sha256"],
            "manifest_sha256": sha(mpath), "verified": True}
    ppath = a.provenance or dest.rstrip("\\/") + ".provenance.json"
    with open(ppath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(prov, f, indent=1)
    print(json.dumps(prov, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
