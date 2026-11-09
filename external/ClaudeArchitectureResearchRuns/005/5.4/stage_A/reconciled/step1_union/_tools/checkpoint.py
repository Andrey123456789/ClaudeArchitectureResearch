"""Freeze one completed candidate: final build -> validate -> write immutable checkpoint -> assemble.

Usage: python checkpoint.py M
Refuses to overwrite an existing checkpoint whose frozen output hashes differ from the rebuild.
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys

from union_lib import OUT, ROOT, input_files, support_files, file_sha256, sha256_text, read_jsonl
from build_candidate import build, BuildError

LEDGERS = ["SOURCE_RECORD_INDEX", "SOURCE_OCCURRENCES", "SOURCE_CLAUSES", "MERGED_FINDINGS",
           "RECORD_ACCOUNTING", "MERGE_REVIEW_QUEUE", "SOURCE_VERIFICATION_ISSUES", "MERGE_DECISIONS",
           "CO_LOCATION_INDEX"]
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]


def validate(args):
    r = subprocess.run([sys.executable, str(OUT / "VALIDATE_STAGE1_UNION.py")] + args,
                       capture_output=True, text=True, encoding="utf-8")
    last = [l for l in r.stdout.splitlines() if l.startswith("RESULT:")]
    return (last[-1].split(":", 1)[1].strip() if last else "NO_RESULT"), r.stdout


def assemble():
    done = [c for c in CANDS if (OUT / "CHECKPOINTS" / f"{c}.checkpoint.json").exists()]
    for n in LEDGERS:
        data = b"".join((OUT / "per_candidate" / c / f"{n}.jsonl").read_bytes() for c in done)
        tmp = OUT / f"{n}.jsonl.tmp"
        tmp.write_bytes(data)
        tmp.replace(OUT / f"{n}.jsonl")
    return done


def main():
    c = sys.argv[1]
    cp = OUT / "CHECKPOINTS" / f"{c}.checkpoint.json"
    old = json.loads(cp.read_text(encoding="utf-8")) if cp.exists() else None
    try:
        summ = build(c, final=True)
    except BuildError as ex:
        print("BUILD ERROR:\n" + str(ex))
        return 2
    res, out = validate(["--candidate", c, "--pre-checkpoint"])
    if res not in ("PASS", "PASS_WITH_OPEN_ISSUES"):
        print(out[-4000:])
        print(f"checkpoint NOT written: validator {res}")
        return 1
    outs = {f"per_candidate/{c}/{n}.jsonl": file_sha256(f"stage_A/reconciled/step1_union/per_candidate/{c}/{n}.jsonl") for n in LEDGERS}
    outs[f"per_candidate/{c}/BUILD_SUMMARY.json"] = file_sha256(f"stage_A/reconciled/step1_union/per_candidate/{c}/BUILD_SUMMARY.json")
    gids = sorted(g["group_id"] for g in read_jsonl(OUT / "per_candidate" / c / "MERGED_FINDINGS.jsonl"))
    if old is not None:
        if old["output_sha256"] != outs:
            print("checkpoint exists and rebuild differs; refusing to overwrite an immutable checkpoint")
            return 3
        print("checkpoint already present and identical; nothing rewritten")
    else:
        ins = {rel: file_sha256(rel) for (_, _, rel, _, _) in input_files(c)}
        ins.update({rel: file_sha256(rel) for rel in support_files(c)})
        ck = {
            "candidate": c, "status": "CANDIDATE_STEP1_COMPLETE",
            "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "protocol_sha256": file_sha256("stage_A/reconciled/step1_union/MERGE_PROTOCOL.md"),
            "input_manifest_sha256": file_sha256("inputs/INPUT_MANIFEST_SHA256.csv"),
            "input_sha256": ins, "output_sha256": outs,
            "decision_file_sha256": summ["decision_file_sha256"],
            "group_ids_sha256": sha256_text("\n".join(gids)),
            "counts": {k: v for k, v in summ.items() if k != "decision_file_sha256"},
            "pre_checkpoint_validator_result": res,
        }
        cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(ck, indent=1, sort_keys=True), encoding="utf-8")
    done = assemble()
    res2, out2 = validate(["--candidate", c])
    print(f"{c}: checkpoint {'written' if old is None else 'verified'}; validator(after checkpoint) = {res2}; assembled candidates = {done}")
    return 0 if res2 in ("PASS", "PASS_WITH_OPEN_ISSUES") else 1


if __name__ == "__main__":
    sys.exit(main())
