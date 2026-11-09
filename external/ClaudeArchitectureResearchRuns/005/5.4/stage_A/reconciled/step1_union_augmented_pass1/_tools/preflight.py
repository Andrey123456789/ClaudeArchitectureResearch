"""Preflight: pin input hashes, verify the frozen inputs, build the 152-claim review queue.

  python -B preflight.py          # first run: writes INPUT_HASHES.json, REVIEW_QUEUE.jsonl, PREFLIGHT_REPORT.json
  python -B preflight.py --verify # later runs: recompute and compare against INPUT_HASHES.json (no rewrite)

Never reads PASSES/pass_0002 or later. Rolling Codex files (NOVEL/UNRESOLVED/ALREADY_COVERED) are
pinned by their discovery_pass == 1 subset; a full-file change there is reported, not imported.
"""
from __future__ import annotations

import collections
import csv
import json
import subprocess
import sys

from aug_lib import (CANDS, CIS, INPUTS, OUT, PASS1, ROOT, UNION, atomic_write_json,
                     atomic_write_jsonl, read_jsonl, rel, sha256_bytes, sha256_file,
                     verify_quote)

ROLLUPS = ["NOVEL_FINDINGS.jsonl", "UNRESOLVED_FINDINGS.jsonl", "ALREADY_COVERED_SAMPLES.jsonl"]
CIS_FIXED = ["BASELINE_RECORD_INDEX.jsonl", "BASELINE_LOCATION_MAP.jsonl", "BASELINE_MANIFEST.json"]


def pass1_subset_digest(p):
    rows = [raw for raw, o in read_jsonl(p) if o.get("discovery_pass") == 1]
    return sha256_bytes(b"\n".join(sorted(rows))), len(rows)


def tree_files(d):
    return sorted(x for x in d.rglob("*") if x.is_file() and "__pycache__" not in x.parts)


def compute_hashes(pass_validation):
    h = {"immutable_files": {}, "rolling_files_pass1_subset": {}, "notes": []}
    # inputs: manifest + every manifest-listed file
    man = INPUTS / "INPUT_MANIFEST_SHA256.csv"
    h["immutable_files"][rel(man)] = sha256_file(man)
    bad = []
    n = 0
    with open(man, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            p = INPUTS / row["relative_path"]
            if not p.is_file() or sha256_file(p) != row["sha256"]:
                bad.append(row["relative_path"])
    h["inputs_manifest_check"] = {"files_listed": n, "mismatches": bad}
    for p in tree_files(UNION):
        h["immutable_files"][rel(p)] = sha256_file(p)
    for p in tree_files(PASS1):
        h["immutable_files"][rel(p)] = sha256_file(p)
    for name in CIS_FIXED:
        h["immutable_files"][rel(CIS / name)] = sha256_file(CIS / name)
    for fid, rv in sorted(pass_validation["applied_revisions"].items()):
        p = CIS / rv["revision"]
        h["immutable_files"][rel(p)] = sha256_file(p)
    for name in ROLLUPS:
        p = CIS / name
        d, k = pass1_subset_digest(p)
        h["rolling_files_pass1_subset"][rel(p)] = {
            "pass1_subset_sha256": d, "pass1_rows": k, "full_file_sha256_at_pin": sha256_file(p)}
    return h


def verify_against_pin():
    pin = json.loads((OUT / "INPUT_HASHES.json").read_text(encoding="utf-8"))
    errors, warnings = [], []
    for rp, hv in pin["immutable_files"].items():
        p = ROOT / rp
        if not p.is_file():
            errors.append(f"MISSING {rp}")
        elif sha256_file(p) != hv:
            errors.append(f"CHANGED {rp}")
    for rp, info in pin["rolling_files_pass1_subset"].items():
        p = ROOT / rp
        d, k = pass1_subset_digest(p)
        if d != info["pass1_subset_sha256"]:
            errors.append(f"PASS1_SUBSET_CHANGED {rp}")
        elif sha256_file(p) != info["full_file_sha256_at_pin"]:
            warnings.append(f"ROLLUP_FULL_FILE_CHANGED_PASS1_SUBSET_UNCHANGED {rp} (later-pass rows not imported)")
    pinned_union = {rp for rp in pin["immutable_files"] if rp.startswith("stage_A/reconciled/step1_union/")}
    now_union = {rel(p) for p in tree_files(UNION)}
    for extra in sorted(now_union - pinned_union):
        errors.append(f"NEW_FILE_IN_IMMUTABLE_UNION {extra}")
    pinned_pass1 = {rp for rp in pin["immutable_files"] if rp.startswith("stage_A/codex_iterative_search/PASSES/pass_0001/")}
    now_pass1 = {rel(p) for p in tree_files(PASS1)}
    for extra in sorted(now_pass1 - pinned_pass1):
        errors.append(f"NEW_FILE_IN_PASS1 {extra}")
    pinned_rev = {rp for rp in pin["immutable_files"] if "/REVISIONS/" in rp}
    now_rev = {rel(p) for p in (CIS / "REVISIONS").iterdir() if p.is_file()}
    for extra in sorted(now_rev - pinned_rev):
        warnings.append(f"NEW_REVISION_FILE_NOT_IN_PASS1_VALIDATION {extra} (not read, not applied)")
    return errors, warnings


def build_queue(pv):
    claims = read_jsonl(PASS1 / "CANDIDATE_CLAIMS.jsonl")
    comps = {o["claim_id"]: o for _, o in read_jsonl(PASS1 / "NOVELTY_COMPARISONS.jsonl")}
    roll = {}
    for name in ROLLUPS:
        for raw, o in read_jsonl(CIS / name):
            if o.get("discovery_pass") == 1:
                roll.setdefault(o["id"], []).append((name, raw, o))
    ckpt_ids = {}
    for c in CANDS:
        ck = json.loads((PASS1 / f"{c}_CANDIDATE_CHECKPOINT.json").read_text(encoding="utf-8"))
        for cid in ck["claim_ids"]:
            ckpt_ids.setdefault(cid, []).append(c)
    revs = {}
    for fid, rv in pv["applied_revisions"].items():
        r = json.loads((CIS / rv["revision"]).read_text(encoding="utf-8"))
        revs[fid] = (rv, r)
    problems = []
    queue = []
    seen = set()
    per_cand_ord = collections.Counter()
    for ordinal, (raw, o) in enumerate(claims, 1):
        cid = o["id"]
        if cid in seen:
            problems.append(f"DUPLICATE_CLAIM_ID {cid}")
        seen.add(cid)
        if o.get("discovery_pass") != 1:
            problems.append(f"NOT_PASS1 {cid}")
        c = o["candidate"]
        per_cand_ord[c] += 1
        orig = o["comparison_status"]
        eff = orig
        rev_id = rev_path = None
        field_updates = {}
        closest = list(o.get("closest_policy_ids") or [])
        if cid in revs:
            rv, r = revs[cid]
            if r["finding_id"] != cid or r["discovery_pass"] != 1 or r["previous_status"] != orig \
                    or r["effective_status"] != rv["effective_status"]:
                problems.append(f"REVISION_INCONSISTENT {cid}")
            eff = r["effective_status"]
            rev_id = r["revision_id"]
            rev_path = rel(CIS / rv["revision"])
            field_updates = r.get("field_updates") or {}
            if "closest_policy_ids" in field_updates:
                closest = list(field_updates["closest_policy_ids"])
        idx = ["PASSES/pass_0001/CANDIDATE_CLAIMS.jsonl"]
        if cid in comps:
            idx.append("PASSES/pass_0001/NOVELTY_COMPARISONS.jsonl")
            if comps[cid]["comparison_status"] != orig:
                problems.append(f"COMPARISON_STATUS_MISMATCH {cid}")
        else:
            problems.append(f"NO_NOVELTY_COMPARISON {cid}")
        for name, rraw, ro in roll.get(cid, []):
            idx.append(name)
            if ro != o:
                problems.append(f"ROLLUP_ROW_DIFFERS {cid} in {name}")
        if len(roll.get(cid, [])) != 1:
            problems.append(f"ROLLUP_PRESENCE {cid} {len(roll.get(cid, []))}")
        if ckpt_ids.get(cid) != [c]:
            problems.append(f"CHECKPOINT_MEMBERSHIP {cid} {ckpt_ids.get(cid)}")
        qstat, _ = verify_quote(c, o["path"], o["start_line"], o["end_line"], o["quote"])
        queue.append({
            "claim_id": cid,
            "candidate": c,
            "pass1_ordinal": ordinal,
            "candidate_ordinal": per_cand_ord[c],
            "discovery_pass": 1,
            "raw_line_sha256": sha256_bytes(raw),
            "original_status": orig,
            "effective_status": eff,
            "revision_id": rev_id,
            "revision_path": rev_path,
            "revision_field_updates": field_updates,
            "indexes_present_in": idx,
            "path": o["path"],
            "start_line": o["start_line"],
            "end_line": o["end_line"],
            "source_file": f"inputs/{c}/{o['path']}",
            "source_file_sha256": sha256_file(INPUTS / c / o["path"]),
            "quote": o["quote"],
            "quote_verification": qstat,
            "codex_evidence_verification_status": o["evidence_verification_status"],
            "claim": o["claim"],
            "actor": o["actor"],
            "trigger": o["trigger"],
            "modality": o["modality"],
            "domain": o["domain"],
            "exceptions": o["exceptions"],
            "enforcement_effect": o["enforcement_effect"],
            "original_closest_policy_ids": o.get("closest_policy_ids") or [],
            "effective_closest_policy_ids": closest,
            "baseline_comparisons": o["baseline_comparisons"],
            "comparison_reason": o["comparison_reason"],
            "distinguishing_behavioral_scenario": o["distinguishing_behavioral_scenario"],
            "codex_confidence": o["confidence"],
            "open_question": o.get("open_question"),
            "next_evidence_strategy": o.get("next_evidence_strategy"),
            "adjudication_question": o.get("adjudication_question"),
        })
    for cid in revs:
        if cid not in seen:
            problems.append(f"REVISION_FOR_UNKNOWN_CLAIM {cid}")
    for cid in set(roll) - seen:
        problems.append(f"ROLLUP_ID_NOT_IN_CANDIDATE_CLAIMS {cid}")
    for cid in set(ckpt_ids) - seen:
        problems.append(f"CHECKPOINT_ID_NOT_IN_CANDIDATE_CLAIMS {cid}")
    # counts vs PASS_VALIDATION
    eff_counts = collections.defaultdict(collections.Counter)
    orig_counts = collections.defaultdict(collections.Counter)
    for q in queue:
        eff_counts[q["candidate"]][q["effective_status"]] += 1
        orig_counts[q["candidate"]][q["original_status"]] += 1
    for c in CANDS:
        if dict(eff_counts[c]) != pv["effective_counts_by_candidate"][c]:
            problems.append(f"EFFECTIVE_COUNTS_MISMATCH {c}")
        if dict(orig_counts[c]) != pv["original_counts_by_candidate"][c]:
            problems.append(f"ORIGINAL_COUNTS_MISMATCH {c}")
    for q in queue:
        if q["quote_verification"] in ("MISMATCH", "MISSING_FILE", "INVALID_RANGE"):
            problems.append(f"QUOTE_{q['quote_verification']} {q['claim_id']}")
    return queue, problems, eff_counts, orig_counts


def union_invariants():
    out = {}
    groups = read_jsonl(UNION / "MERGED_FINDINGS.jsonl")
    ids = [o["group_id"] for _, o in groups]
    out["groups_total"] = len(ids)
    out["group_ids_unique"] = len(set(ids)) == len(ids)
    out["group_prefix_matches_candidate"] = all(o["group_id"].startswith(f"FG-{o['candidate']}-") for _, o in groups)
    per = collections.Counter(o["candidate"] for _, o in groups)
    out["groups_by_candidate"] = dict(per)
    pc_ok = {}
    for c in CANDS:
        sub = [raw for raw, o in groups if o["candidate"] == c]
        pc = [raw for raw, _ in read_jsonl(UNION / "per_candidate" / c / "MERGED_FINDINGS.jsonl")]
        pc_ok[c] = sorted(sub) == sorted(pc)
    out["per_candidate_merged_findings_equal_global_subset"] = pc_ok
    out["checkpoints_present"] = {c: (UNION / "CHECKPOINTS" / f"{c}.checkpoint.json").is_file() for c in CANDS}
    return out


def main():
    verify_only = "--verify" in sys.argv
    pv = json.loads((PASS1 / "PASS_VALIDATION.json").read_text(encoding="utf-8"))
    blockers = []
    if pv.get("status") != "COMPLETE" or pv.get("source_files") != 448 or pv.get("pass_id") != 1:
        blockers.append("PASS_VALIDATION not COMPLETE/448/pass 1")
    ch = json.loads((PASS1 / "CHECKPOINT_HASHES.json").read_text(encoding="utf-8"))
    for name, hv in ch.items():
        p = PASS1 / name
        if not p.is_file() or sha256_file(p) != hv:
            blockers.append(f"PASS1_CHECKPOINT_HASH_MISMATCH {name}")
    if verify_only:
        errors, warnings = verify_against_pin()
        res = {"integrity": "PASS" if not errors and not blockers else "FAIL",
               "errors": blockers + errors, "warnings": warnings}
        print(json.dumps(res, indent=1))
        sys.exit(0 if res["integrity"] == "PASS" else 2)
    if (OUT / "INPUT_HASHES.json").exists():
        print("INPUT_HASHES.json exists: use --verify (resume) instead of re-pinning.")
        sys.exit(3)
    hashes = compute_hashes(pv)
    if hashes["inputs_manifest_check"]["mismatches"]:
        blockers.append("INPUT_MANIFEST_MISMATCH")
    inv = union_invariants()
    if inv["groups_total"] != 6347 or not inv["group_ids_unique"] or not inv["group_prefix_matches_candidate"] \
            or not all(inv["per_candidate_merged_findings_equal_global_subset"].values()) \
            or not all(inv["checkpoints_present"].values()):
        blockers.append("UNION_INVARIANT_FAILURE")
    queue, problems, eff, orig = build_queue(pv)
    blockers += problems
    if len(queue) != 152:
        blockers.append(f"QUEUE_SIZE {len(queue)}")
    base_val = subprocess.run([sys.executable, "-B", str(UNION / "VALIDATE_STAGE1_UNION.py")],
                              cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
    base_tail = base_val.stdout.strip().splitlines()[-1] if base_val.stdout.strip() else ""
    base_json = json.loads(base_val.stdout[:base_val.stdout.rfind("}") + 1])
    report = {
        "status": "BLOCKED" if blockers else "PASS",
        "blockers": blockers,
        "pass_validation": {k: pv[k] for k in ("status", "pass_id", "strategy", "source_files",
                                                "baseline_fingerprint", "semantic_completeness_proven")},
        "queue_size": len(queue),
        "original_counts": {c: dict(orig[c]) for c in CANDS},
        "effective_counts": {c: dict(eff[c]) for c in CANDS},
        "original_totals": dict(sum((orig[c] for c in CANDS), collections.Counter())),
        "effective_totals": dict(sum((eff[c] for c in CANDS), collections.Counter())),
        "quote_verification": dict(collections.Counter(q["quote_verification"] for q in queue)),
        "index_presence": {" + ".join(k): v for k, v in
                           collections.Counter(tuple(q["indexes_present_in"]) for q in queue).items()},
        "union_invariants": inv,
        "base_union_validator": {"command": "python -B stage_A/reconciled/step1_union/VALIDATE_STAGE1_UNION.py",
                                 "result_line": base_tail, "error_count": base_json.get("error_count"),
                                 "warning_count": base_json.get("warning_count"),
                                 "input_manifest_files_verified": base_json["info"].get("input_manifest_files_verified")},
        "excluded": ["stage_A/codex_iterative_search/PASSES/pass_0002/** and later (not read)",
                     "STATE.json, FINAL_REPORT.md, HANDOFF_TO_CLAUDE.md not used as count evidence"],
    }
    hashes["applied_revisions"] = pv["applied_revisions"]
    hashes["immutable_directories"] = ["inputs/", "stage_A/reconciled/step1_union/",
                                       "stage_A/codex_iterative_search/PASSES/pass_0001/",
                                       "stage_A/primary/", "stage_A/replica/", "stage_A/independent/"]
    hashes["pinned_at"] = "preflight (before any review decision)"
    hashes["aggregate_sha256"] = sha256_bytes(json.dumps(hashes["immutable_files"], sort_keys=True).encode())
    if blockers:
        atomic_write_json(OUT / "PREFLIGHT_REPORT.json", report)
        print(json.dumps(report, indent=1))
        sys.exit(1)
    atomic_write_json(OUT / "INPUT_HASHES.json", hashes)
    atomic_write_jsonl(OUT / "REVIEW_QUEUE.jsonl", queue)
    atomic_write_json(OUT / "PREFLIGHT_REPORT.json", report)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
