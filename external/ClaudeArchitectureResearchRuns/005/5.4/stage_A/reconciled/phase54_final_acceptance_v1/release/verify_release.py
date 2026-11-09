"""Read-only verification of the Phase 5.4 candidate release (phase54-final-v1).

Usage (any working directory):
  python -B verify_release.py [--release-dir DIR] [--v3-dir DIR] [--json]

Independent of the tool that built the release: it re-reads CANDIDATE_FREEZE_MANIFEST.json and
confirms, for each of the six candidates,
  R1 the manifest's own SHA-256 equals the .sha256 sidecar;
  R2 every listed file exists and its SHA-256 and byte size equal the manifest;
  R3 no file exists in the template tree that the manifest does not list (no unexpected files);
  R4 the per-candidate file count and tree hash recompute to the manifest values;
  R5 (when the v3 source is reachable) every released file equals the approved v3 template byte for byte,
     and both trees list the same files; the v3 file hashes equal V3_FINAL_MANIFEST.json;
  R6 every released file still carries the read-only attribute (warning only).
It opens files for reading only and writes nothing. Exit code 0 = PASS, 1 = FAIL.
"""
import argparse
import filecmp
import hashlib
import json
import os
import stat
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def walk(root):
    out = []
    for dp, dn, fn in os.walk(root):
        for n in fn:
            out.append(os.path.relpath(os.path.join(dp, n), root).replace(os.sep, "/"))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release-dir", default=HERE)
    ap.add_argument("--v3-dir", default=os.path.normpath(os.path.join(HERE, "..", "..", "step2_controlled_repair_v3")))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    mpath = os.path.join(a.release_dir, "CANDIDATE_FREEZE_MANIFEST.json")
    res = {"release_dir": os.path.abspath(a.release_dir), "checks": {}, "warnings": [], "per_candidate": {}}
    side = open(mpath + ".sha256", encoding="utf-8").read().split()[0]
    res["checks"]["R1_manifest_sidecar"] = sha(mpath) == side
    man = json.load(open(mpath, encoding="utf-8"))

    v3_ok = os.path.isdir(a.v3_dir)
    v3man = json.load(open(os.path.join(a.v3_dir, "V3_FINAL_MANIFEST.json"), encoding="utf-8")) if v3_ok else None
    all_ok = res["checks"]["R1_manifest_sidecar"] and sorted(man["candidates"]) == sorted(CANDS)
    for c in CANDS:
        row = man["candidates"][c]
        root = os.path.join(a.release_dir, "candidates", c, "template")
        listed = row["files"]
        disk = walk(root)
        missing = sorted(set(listed) - set(disk))
        unexpected = sorted(set(disk) - set(listed))
        bad_hash, bad_size, writable = [], [], []
        hashes = {}
        for rel in disk:
            p = os.path.join(root, rel)
            h = sha(p)
            hashes[rel] = h
            if rel in listed:
                if h != listed[rel]["sha256"]:
                    bad_hash.append(rel)
                if os.path.getsize(p) != listed[rel]["bytes"]:
                    bad_size.append(rel)
            if os.stat(p).st_mode & stat.S_IWRITE:
                writable.append(rel)
        th = hashlib.sha256()
        for rel in sorted(listed):
            th.update(f"{rel}\t{hashes.get(rel, 'MISSING')}\n".encode("utf-8"))
        r4 = len(disk) == row["n_files"] and th.hexdigest() == row["tree_sha256"]
        c_res = {"n_files": len(disk), "missing": missing, "unexpected": unexpected, "hash_mismatch": bad_hash,
                 "size_mismatch": bad_size, "R4_count_and_tree_hash": r4}
        if v3_ok:
            src = os.path.join(a.v3_dir, "candidates", c, "template")
            src_files = walk(src)
            not_identical = [rel for rel in src_files if rel in hashes and
                             not filecmp.cmp(os.path.join(src, rel), os.path.join(root, rel), shallow=False)]
            v3_hash_bad = [rel for rel in src_files if sha(os.path.join(src, rel)) != v3man["candidates"][c]["files"].get(rel, {}).get("sha256")]
            c_res["R5_v3"] = {"same_file_set": src_files == disk and sorted(v3man["candidates"][c]["files"]) == disk,
                              "not_byte_identical": not_identical, "v3_differs_from_V3_FINAL_MANIFEST": v3_hash_bad}
            r5 = c_res["R5_v3"]["same_file_set"] and not not_identical and not v3_hash_bad
        else:
            c_res["R5_v3"] = "NOT_RUN (v3 source not reachable)"
            r5 = True
        if writable:
            res["warnings"].append(f"{c}: {len(writable)} file(s) lost the read-only attribute")
        c_ok = not (missing or unexpected or bad_hash or bad_size) and r4 and r5
        c_res["pass"] = c_ok
        res["per_candidate"][c] = c_res
        all_ok = all_ok and c_ok
    res["checks"]["R2_R3_R4_R5_all_candidates"] = all(v["pass"] for v in res["per_candidate"].values())
    res["totals"] = {"files": sum(v["n_files"] for v in res["per_candidate"].values()), "expected": man["totals"]["files"]}
    res["verdict"] = "PASS" if all_ok and res["totals"]["files"] == man["totals"]["files"] else "FAIL"
    res["v3_comparison"] = "RUN" if v3_ok else "NOT_RUN"
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        for c, v in res["per_candidate"].items():
            print(f"{c:3} files={v['n_files']:3} {'PASS' if v['pass'] else 'FAIL'}")
        for w in res["warnings"]:
            print("WARNING", w)
        print(f"{res['verdict']} ({res['totals']['files']} files; v3 byte comparison {res['v3_comparison']})")
    return 0 if res["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
