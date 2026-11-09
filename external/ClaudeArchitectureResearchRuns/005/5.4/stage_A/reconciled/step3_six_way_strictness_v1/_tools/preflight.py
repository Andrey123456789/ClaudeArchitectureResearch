"""Step 3 preflight (contract section 1). Read-only toward every predecessor.

First run: verifies v3 completeness and writes UPSTREAM_FINGERPRINT.json,
UPSTREAM_V3_TREE_HASHES.json, PREFLIGHT_RESULT.json and PREFLIGHT_REPORT.md.
Later runs (resume): re-verify the same facts and compare every hash with the
stored fingerprint; never overwrite the stored fingerprint.

Usage: python -B _tools/preflight.py
"""
import datetime
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import (CANDS, INPUTS, RECON, ROOT, S3, V2, V3, canonical_policies, read_json,  # noqa: E402
                      read_jsonl, sha256_file, write_json_atomic, write_text_atomic)

EXPECT_CHECKPOINTS = [
    "PV2-01-GIT-GATING", "PV2-02-FAILCLOSED-INPUT", "PV2-03-K0-CPM-ROOT", "PV2-03B-CPM-IMPORT-PROVEN",
    "PV2-04-M-FRONTEND-TESTS", "V3-0-BASELINE-REPLAY", "V3-D01-PASS23-OVERLAY", "V3-D02-MODALITY86",
    "V3-Q10-PACKAGEVERSION-VERSION",
]
EXPECT_CHANGED_VS_FROZEN = {"M": 18, "M1": 16, "L0": 16, "L1": 16, "K0": 17, "K1": 21}
EXPECT_CHANGED_VS_V2 = {"M": 7, "M1": 6, "L0": 3, "L1": 3, "K0": 3, "K1": 4}
KEY_FILES = [
    "FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md", "STATE.json", "RESUME.md", "EVIDENCE_LIMITS.md",
    "UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl", "V3_METRIC_IMPACT.md", "V3_METRIC_CROSSWALK.json",
    "DATASET_MANIFEST.json", "V3_FINAL_MANIFEST.json", "FINAL_AUDIT_RESULTS.jsonl", "FINAL_SUITE_TALLY.json",
    "REGRESSION_MATRIX.md", "GATE_LOG.jsonl", "REPAIRED_CLASSIFICATIONS.jsonl", "REPAIRED_POLICY_COVERAGE.jsonl",
    "POLICY_PARITY_MATRIX.jsonl", "ORIGINAL_TO_REPAIRED_CLAIMS.jsonl", "V2_TO_V3_CROSSWALK.jsonl",
    "V2_TO_V3_FILE_CROSSWALK.jsonl", "PARTIAL_WITNESSES_38.jsonl", "PASS2_PASS3_ADJUDICATION.jsonl",
    "UNIQUE_ISSUE_CLUSTERS.jsonl", "ADJUDICATION_COUNTS.json", "MARKED_NEVER_86_REVIEW.jsonl",
    "MARKED_NEVER_SOFT_MODALITY.jsonl", "V3_NEW_CLAIMS_REVIEW.jsonl", "SAME_TASK_MATRIX_V3.json",
    "INTERACTION_MATRIX_V3.json", "APPROVED_DECISION_IMPLEMENTATION_MATRIX.md", "EXTERNAL_EVENTS.json",
    "CHANGE_LOG.jsonl", "PI012_230_REVIEW.jsonl", "PI012_79_REVIEW.jsonl", "PI012_SENSITIVITY.md",
    "PI012_SENSITIVITY_V2.md", "CLAIM_DISPOSITIONS.jsonl", "UNRESOLVED_DECISIONS.jsonl",
]
OTHER_INPUTS = [
    "_STAGE_A_KIT/75_CLAUDE_STAGE_A_STEP3_SIX_WAY_STRICTNESS_TASK_EN.md",
    "_STAGE_A_KIT/75_CLAUDE_STAGE_A_STEP3_START_EN.txt",
    "_STAGE_A_KIT/74_CLAUDE_STAGE_A_STEP2_PASS23_INTEGRATION_TASK_EN.md",
    "_STAGE_A_KIT/62_APPROVED_DECISIONS_AND_GATES_EN.md",
    "Stage_A_Step2_Post_V2_Approved_Decisions_EN.md",
    "ClaudeArchitectureResearch_5_4_decision_register_2026-11-03.md",
    "Stage_A_Step2_V3_Independent_Interim_Review_EN.md",
    "inputs/INPUT_MANIFEST_SHA256.csv",
] + [f"inputs/{c}/source/inventory.json" for c in CANDS] + [
    f"inputs/{c}/source/shared-research-invariants.json" for c in CANDS]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def main():
    checks = []

    def check(cid, ok, detail, kind="CHECK"):
        checks.append({"id": cid, "status": ("PASS" if ok else "FAIL") if kind == "CHECK" else kind,
                       "detail": detail})

    # P01 state
    st = read_json(V3 / "STATE.json")
    check("P01-V3-STATE", st.get("phase") == "COMPLETE" and st["result"]["status"] == "PASS_WITH_DOCUMENTED_NOT_RUN"
          and st.get("step3_started") is False,
          f"phase={st.get('phase')} result={st['result']['status']} step3_started={st.get('step3_started')} "
          f"recommendation={st['result']['step3_recommendation']}")

    # P02 checkpoints
    cps = sorted(p.name.replace(".checkpoint.json", "") for p in (V3 / "CHECKPOINTS").glob("*.checkpoint.json"))
    cp_ok = cps == sorted(EXPECT_CHECKPOINTS) and sorted(st["checkpoints"]) == sorted(EXPECT_CHECKPOINTS)
    gates = {}
    for c in cps:
        d = read_json(V3 / "CHECKPOINTS" / f"{c}.checkpoint.json")
        gates[c] = (d["gate"], d["n_policy_rows"], d["test_tally"])
        cp_ok = cp_ok and d["gate"] == "PASS_WITH_DOCUMENTED_NOT_RUN" and d["n_policy_rows"] == 1176
    check("P02-NINE-CHECKPOINTS", cp_ok, {"found": cps, "gates": {k: v[0] for k, v in gates.items()}})

    # P03 final checkpoint vs dataset bytes
    fin = read_json(V3 / "CHECKPOINTS" / "V3-Q10-PACKAGEVERSION-VERSION.checkpoint.json")
    dm = read_json(V3 / "DATASET_MANIFEST.json")
    actual = {k: sha256_file(V3 / k) for k in fin["view_sha256"]}
    ok3 = (fin["test_tally"] == {"NOT_RUN": 32, "PASS": 3416} and fin["dataset"]["rows"] == 6498
           and fin["dataset"]["active"] == 6495 and fin["dataset"]["coverage_cells"] == 1176
           and all(actual[k] == fin["view_sha256"][k] == dm["sha256"][k] for k in actual))
    v2v3 = sha256_file(V3 / "V2_TO_V3_CROSSWALK.jsonl")
    ok3 = ok3 and v2v3 == dm["v2_to_v3"]["sha256"]
    check("P03-FINAL-CHECKPOINT-DATASET-HASHES", ok3,
          {"test_tally": fin["test_tally"], "dataset": fin["dataset"], "view_sha256_match": actual == fin["view_sha256"],
           "v2_to_v3_crosswalk_sha256_match": v2v3 == dm["v2_to_v3"]["sha256"]})

    # P04/P05/P06 candidate bytes vs manifest
    man = read_json(V3 / "V3_FINAL_MANIFEST.json")
    cand_hashes = {}
    bad, missing, extra = [], [], []
    n_total = 0
    ch_frozen, ch_v2 = Counter(), Counter()
    frozen_bad, v2_bad = [], []
    for c in CANDS:
        mc = man["candidates"][c]
        tdir = V3 / "candidates" / c / "template"
        on_disk = sorted(str(p.relative_to(tdir)).replace("\\", "/") for p in tdir.rglob("*") if p.is_file())
        n_total += len(on_disk)
        mf = mc["files"]
        missing += [f"{c}/{p}" for p in mf if p not in on_disk]
        extra += [f"{c}/{p}" for p in on_disk if p not in mf]
        cand_hashes[c] = {}
        for p in on_disk:
            h = sha256_file(tdir / p)
            cand_hashes[c][p] = h
            if p in mf and mf[p]["sha256"] != h:
                bad.append(f"{c}/{p}")
            if p in mf:
                fz = INPUTS / c / "output" / "template" / p
                fh = sha256_file(fz) if fz.exists() else None
                if fh != mf[p]["frozen_sha256"]:
                    frozen_bad.append(f"{c}/{p}")
                if (h != fh) != mf[p]["changed_vs_frozen"]:
                    frozen_bad.append(f"{c}/{p} flag")
                if h != fh:
                    ch_frozen[c] += 1
                v2p = V2 / "candidates" / c / "template" / p
                v2h = sha256_file(v2p) if v2p.exists() else None
                if v2h != mf[p]["v2_sha256"]:
                    v2_bad.append(f"{c}/{p}")
                if h != v2h:
                    ch_v2[c] += 1
        if len(on_disk) != mc["n_files"]:
            bad.append(f"{c}: n_files {len(on_disk)} != {mc['n_files']}")
    check("P04-448-FILES-MATCH-V3-FINAL-MANIFEST", n_total == 448 and not bad and not missing and not extra,
          {"n_files": n_total, "per_candidate": {c: len(cand_hashes[c]) for c in CANDS}, "hash_mismatch": bad,
           "missing": missing, "extra": extra})
    check("P05-CHANGED-VS-FROZEN-104", dict(ch_frozen) == EXPECT_CHANGED_VS_FROZEN and not frozen_bad,
          {"changed_vs_frozen": dict(ch_frozen), "total": sum(ch_frozen.values()), "frozen_hash_mismatch": frozen_bad})
    check("P06-CHANGED-VS-V2-26", dict(ch_v2) == EXPECT_CHANGED_VS_V2 and not v2_bad,
          {"changed_vs_v2": dict(ch_v2), "total": sum(ch_v2.values()), "v2_hash_mismatch": v2_bad})

    # P07 oracle
    pols = canonical_policies()
    ids = [p["id"] for p in pols]
    inv_h = {c: sha256_file(INPUTS / c / "source" / "inventory.json") for c in CANDS}
    shr_h = {c: sha256_file(INPUTS / c / "source" / "shared-research-invariants.json") for c in CANDS}
    check("P07-ORACLE-196", len(ids) == 196 and len(set(ids)) == 196 and len(set(inv_h.values())) == 1
          and len(set(shr_h.values())) == 1,
          {"n": len(ids), "unique": len(set(ids)), "inventory_sha256": sorted(set(inv_h.values())),
           "invariants_sha256": sorted(set(shr_h.values())), "by_group": dict(Counter(p["group"] for p in pols))})

    # P08 coverage and parity matrix
    cov = read_jsonl(V3 / "REPAIRED_POLICY_COVERAGE.jsonl")
    pm = read_jsonl(V3 / "POLICY_PARITY_MATRIX.jsonl")
    def cells_ok(rows):
        keys = [(r["candidate"], r["policy_id"]) for r in rows]
        return (len(rows) == 1176 and len(set(keys)) == 1176
                and all(sorted(r["policy_id"] for r in rows if r["candidate"] == c) == sorted(ids) for c in CANDS))
    check("P08-1176-CELLS", cells_ok(cov) and cells_ok(pm),
          {"coverage_rows": len(cov), "parity_rows": len(pm),
           "coverage_status": dict(Counter(r["status"] for r in cov)),
           "strength_status": dict(Counter(r["strength_status"] for r in cov)),
           "check_level": dict(Counter(r["check_level"] for r in pm))})

    # P09 classification universe (keep inactive rows)
    recs = read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl")
    keys = [r["source_key"] for r in recs]
    act = sum(1 for r in recs if r["repair"]["active"])
    mc = read_json(V3 / "V3_METRIC_CROSSWALK.json")
    byc = Counter(r["candidate"] for r in recs)
    ok9 = (len(recs) == 6498 and len(set(keys)) == 6498 and act == 6495
           and all(byc[c] == mc["data_labels"]["rows_by_candidate"][c]["v3"] for c in CANDS))
    check("P09-CLASSIFICATION-UNIVERSE", ok9,
          {"rows": len(recs), "unique_keys": len(set(keys)), "active": act, "inactive": len(recs) - act,
           "by_candidate": dict(byc), "view_record_type": dict(Counter(r["view_record_type"] for r in recs))})

    # P10 crosswalk
    xw = read_jsonl(V3 / "V2_TO_V3_CROSSWALK.jsonl")
    xs = Counter(r.get("status") for r in xw)
    check("P10-V2-TO-V3-CROSSWALK", len(xw) == 6498 and dict(xs) == dm["v2_to_v3"]["by_status"],
          {"rows": len(xw), "status": dict(xs)})

    # P11 suite tally
    ft = read_json(V3 / "FINAL_SUITE_TALLY.json")
    sp = sum(v.get("PASS", 0) for v in ft["by_suite"].values())
    sn = sum(v.get("NOT_RUN", 0) for v in ft["by_suite"].values())
    sf = sum(v.get("FAIL", 0) for v in ft["by_suite"].values())
    check("P11-SUITE-TALLY-3416-0-32", len(ft["by_suite"]) == 44 and (sp, sf, sn) == (3416, 0, 32)
          and ft["tally"] == {"NOT_RUN": 32, "PASS": 3416},
          {"suites": len(ft["by_suite"]), "PASS": sp, "FAIL": sf, "NOT_RUN": sn})

    # P12 cold audit
    au = read_jsonl(V3 / "FINAL_AUDIT_RESULTS.jsonl")
    at = Counter(r["status"] for r in au)
    check("P12-COLD-AUDIT-263-0-35-9", dict(at) == {"PASS": 263, "NOT_RUN": 35, "FINDING": 9} and at.get("FAIL", 0) == 0,
          {"rows": len(au), "tally": dict(at)})

    # P13 Codex provenance (not re-adjudicated)
    ac = read_json(V3 / "ADJUDICATION_COUNTS.json")
    adj = read_jsonl(V3 / "PASS2_PASS3_ADJUDICATION.jsonl")
    nadjcp = len(list((V3 / "ADJUDICATION_CHECKPOINTS").glob("*")))
    p1 = RECON / "step1_union_augmented_pass1" / "REVIEW_REPORT.md"
    check("P13-CODEX-PROVENANCE", ac["codex_records"] == {"pass2": 63, "pass3": 148, "total": 211} and len(adj) == 211
          and nadjcp == 30 and p1.exists(),
          {"codex_records": ac["codex_records"], "adjudication_rows": len(adj), "adjudication_checkpoints": nadjcp,
           "by_verdict": ac["by_verdict"], "pass1_review_report": str(p1.relative_to(ROOT)).replace("\\", "/"),
           "pass1_review_report_sha256": sha256_file(p1)})

    # P14 queue
    q = read_jsonl(V3 / "UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl")
    qids = sorted(r["id"] for r in q)
    check("P14-QUEUE-Q01-Q13", qids == [f"Q-{i:02d}" for i in range(1, 14)],
          {"ids": qids, "kinds": {r["id"]: r["kind"] for r in q}})

    # P15 gate attempts
    gl = read_jsonl(V3 / "GATE_LOG.jsonl")
    gt = Counter("PASS" if str(r.get("gate", "")).startswith("PASS") else "FAIL" for r in gl)
    check("P15-GATE-ATTEMPTS-16", len(gl) == 16 and gt == Counter({"PASS": 9, "FAIL": 7}),
          {"attempts": len(gl), "by_outcome": dict(gt)})

    # P16 environment (informational; never blocks when trees verify)
    env = {}
    for name in ["step2_controlled_repair_v1.zip", "step2_controlled_repair_v2.zip", "step2_controlled_repair_v3.zip"]:
        p = RECON / name
        env[name] = {"present": p.exists()}
        if p.exists():
            env[name]["sha256"] = sha256_file(p)
            env[name]["bytes"] = p.stat().st_size
            env[name]["mtime"] = datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")
    ee = read_json(V3 / "EXTERNAL_EVENTS.json")
    env2 = [a for a in ee["added"] if a["id"] == "ENV-02"][0]
    z = RECON / "step2_controlled_repair_v3.zip"
    zip_cmp = None
    if z.exists():
        zip_cmp = {"same_as_ENV02": env["step2_controlled_repair_v3.zip"]["sha256"] == env2["sha256"]}
        with zipfile.ZipFile(z) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            prefix = "step2_controlled_repair_v3/"
            same = diff = absent = 0
            diffs = []
            import hashlib
            for n in names:
                rel = n[len(prefix):] if n.startswith(prefix) else n
                p = V3 / rel
                if not p.exists():
                    absent += 1
                    diffs.append(("absent_in_tree", rel))
                    continue
                h = hashlib.sha256(zf.read(n)).hexdigest()
                if h == sha256_file(p):
                    same += 1
                else:
                    diff += 1
                    diffs.append(("bytes_differ", rel))
            zip_cmp.update({"entries": len(names), "same_bytes_as_tree": same, "differ": diff,
                            "absent_in_tree": absent, "examples": diffs[:20]})
    check("P16-ENVIRONMENT-ARCHIVES", True, {"archives": env, "v3_zip_vs_tree": zip_cmp,
                                            "note": "Convenience archives are not source trees; trees are verified above."},
          kind="INFO")

    # Tree fingerprint of all of v3 (read-only)
    tree = {}
    for p in sorted(V3.rglob("*")):
        if p.is_file():
            tree[str(p.relative_to(V3)).replace("\\", "/")] = sha256_file(p)
    import hashlib
    agg = hashlib.sha256("\n".join(f"{k} {v}" for k, v in tree.items()).encode()).hexdigest()
    other = {k: (sha256_file(ROOT / k) if (ROOT / k).exists() else None) for k in OTHER_INPUTS}
    key = {k: tree[k] for k in KEY_FILES}

    fp_path = S3 / "UPSTREAM_FINGERPRINT.json"
    tree_path = S3 / "UPSTREAM_V3_TREE_HASHES.json"
    fp = {
        "at": now(), "v3_root": "stage_A/reconciled/step2_controlled_repair_v3",
        "v3_tree": {"n_files": len(tree), "aggregate_sha256": agg, "per_file": "UPSTREAM_V3_TREE_HASHES.json"},
        "v3_key_files_sha256": key,
        "v3_candidate_template_sha256": cand_hashes,
        "other_inputs_sha256": other,
        "oracle": {"n_policies": 196, "inventory_sha256": sorted(set(inv_h.values()))[0],
                   "invariants_sha256": sorted(set(shr_h.values()))[0]},
        "environment": env,
    }
    resume = fp_path.exists()
    if resume:
        old = read_json(fp_path)
        oldtree = read_json(tree_path)
        drift = [k for k in set(oldtree) | set(tree) if oldtree.get(k) != tree.get(k)]
        odrift = [k for k in other if old["other_inputs_sha256"].get(k) != other[k]]
        check("P17-RESUME-INPUT-INTEGRITY", not drift and old["v3_tree"]["aggregate_sha256"] == agg and not odrift,
              {"v3_files_changed_since_fingerprint": sorted(drift)[:50], "other_inputs_changed": odrift})
    else:
        write_json_atomic(tree_path, tree)
        write_json_atomic(fp_path, fp)

    status = "PASS" if all(c["status"] in ("PASS", "INFO") for c in checks) else "BLOCKED"
    res = {"at": now(), "status": status, "mode": "RESUME_VERIFY" if resume else "INITIAL", "checks": checks}
    hist = S3 / "PREFLIGHT_HISTORY"
    n = len(list(hist.glob("attempt*.json"))) + 1
    write_json_atomic(hist / f"attempt{n}_{status}.json", res)
    write_json_atomic(S3 / "PREFLIGHT_RESULT.json", res)
    for c in checks:
        print(c["status"], c["id"])
    print("PREFLIGHT", status)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
