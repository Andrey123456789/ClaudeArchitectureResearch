"""Assemble the top-level outputs from the six checkpointed candidates.

  python -B finalize.py

Writes PASS1_REVIEW_LEDGER.jsonl, NEW_CLAUSE_PROPOSALS.jsonl, EXISTING_GROUP_FACETS.jsonl,
UNRESOLVED_REVIEW_QUEUE.jsonl, AUGMENTED_UNION_VIEW.jsonl, UNION_AUGMENTATION_MANIFEST.json and STATS.json.
Refuses to run unless every candidate checkpoint still matches its per-candidate files and the pinned
inputs are unchanged.
"""
from __future__ import annotations

import collections
import json
import subprocess
import sys

from aug_lib import (AUG_VERSION, CANDS, DISPOSITIONS, OUT, UNION, atomic_write_json, atomic_write_jsonl,
                     atomic_write_text, dumps, load_jsonl, read_jsonl, sha256_file)

NAMES = ["PASS1_REVIEW_LEDGER.jsonl", "NEW_CLAUSE_PROPOSALS.jsonl", "EXISTING_GROUP_FACETS.jsonl",
         "UNRESOLVED_REVIEW_QUEUE.jsonl"]


def main():
    ver = subprocess.run([sys.executable, "-B", str(OUT / "_tools" / "preflight.py"), "--verify"],
                         cwd=str(OUT / "_tools"), capture_output=True, text=True)
    integ = json.loads(ver.stdout)
    if integ["integrity"] != "PASS":
        print("INTEGRITY ERROR: STOP", json.dumps(integ, indent=1))
        sys.exit(2)
    merged = {n: [] for n in NAMES}
    for c in CANDS:
        ck = json.loads((OUT / "CHECKPOINTS" / f"{c}.checkpoint.json").read_text(encoding="utf-8"))
        for n in NAMES:
            p = OUT / "per_candidate" / c / n
            if sha256_file(p) != ck["outputs_sha256"][f"per_candidate/{c}/{n}"]:
                print(f"CHECKPOINT MISMATCH {c}/{n}: rebuild and re-checkpoint first")
                sys.exit(3)
            merged[n].extend(load_jsonl(p))
        if sha256_file(OUT / "_review" / f"{c}.rev") != ck["review_file_sha256"]:
            print(f"REVIEW FILE CHANGED AFTER CHECKPOINT {c}")
            sys.exit(3)
    for n in NAMES:
        atomic_write_jsonl(OUT / n, merged[n])
    ledger = merged["PASS1_REVIEW_LEDGER.jsonl"]
    proposals = merged["NEW_CLAUSE_PROPOSALS.jsonl"]
    facets = merged["EXISTING_GROUP_FACETS.jsonl"]
    unresolved = merged["UNRESOLVED_REVIEW_QUEUE.jsonl"]

    # ---------------------------------------------------------------- augmented view
    facets_by_group = collections.defaultdict(list)
    for f in facets:
        facets_by_group[f["target_group_id"]].append(f["facet_id"])
    view = []
    base = read_jsonl(UNION / "MERGED_FINDINGS.jsonl")
    import hashlib
    for raw, g in base:
        view.append({
            "view_record_type": "ORIGINAL_GROUP",
            "augmentation_version": AUG_VERSION,
            "candidate": g["candidate"],
            "group_id": g["group_id"],
            "original_raw_sha256": hashlib.sha256(raw).hexdigest(),
            "original_group": g,
            "facet_overlay_ids": facets_by_group.get(g["group_id"], []),
            "provisional": False,
        })
    for p in proposals:
        view.append({
            "view_record_type": "PROVISIONAL_NEW_CLAUSE",
            "augmentation_version": AUG_VERSION,
            "candidate": p["candidate"],
            "proposal_id": p["proposal_id"],
            "source_claim_id": p["source_claim_id"],
            "proposed_clause_text": p["proposed_clause_text"],
            "modality": p["modality"],
            "trigger_scope": p["trigger_scope"],
            "evidence": {k: p["evidence"][k] for k in ("path", "start_line", "end_line", "quote")},
            "same_candidate_groups_compared": p["same_candidate_groups_compared"],
            "provisional": True,
            "status_note": "Provisional addition from the pass-1 review; not a confirmed EXTRA or oracle mapping.",
        })
    for f in facets:
        view.append({
            "view_record_type": "PROVISIONAL_FACET_OVERLAY",
            "augmentation_version": AUG_VERSION,
            "candidate": f["candidate"],
            "facet_id": f["facet_id"],
            "target_group_id": f["target_group_id"],
            "facet_kind": f["facet_kind"],
            "facet_text": f["facet_text"],
            "source_claim_id": f["source_claim_id"],
            "provisional": True,
            "status_note": "Overlay on an unchanged original group; provisional.",
        })
    atomic_write_jsonl(OUT / "AUGMENTED_UNION_VIEW.jsonl", view)

    # ---------------------------------------------------------------- stats
    def ctr(rows, key):
        return dict(sorted(collections.Counter(r[key] for r in rows).items()))
    stats = {
        "claims": len(ledger),
        "by_candidate": {c: sum(1 for r in ledger if r["candidate"] == c) for c in CANDS},
        "by_original_status": ctr(ledger, "original_status"),
        "by_effective_status": ctr(ledger, "effective_status"),
        "by_disposition": {d: sum(1 for r in ledger if r["disposition"] == d) for d in DISPOSITIONS},
        "candidate_x_disposition": {c: {d: sum(1 for r in ledger if r["candidate"] == c and r["disposition"] == d)
                                        for d in DISPOSITIONS} for c in CANDS},
        "original_status_x_disposition": {s: {d: sum(1 for r in ledger if r["original_status"] == s and r["disposition"] == d)
                                              for d in DISPOSITIONS} for s in sorted({r["original_status"] for r in ledger})},
        "effective_status_x_disposition": {s: {d: sum(1 for r in ledger if r["effective_status"] == s and r["disposition"] == d)
                                               for d in DISPOSITIONS} for s in sorted({r["effective_status"] for r in ledger})},
        "candidate_x_effective_status": {c: ctr([r for r in ledger if r["candidate"] == c], "effective_status") for c in CANDS},
        "reviewer_confidence": ctr(ledger, "reviewer_confidence"),
        "confidence_x_disposition": {k: {d: sum(1 for r in ledger if r["reviewer_confidence"] == k and r["disposition"] == d)
                                         for d in DISPOSITIONS} for k in ("HIGH", "MEDIUM", "LOW")},
        "proposals": len(proposals),
        "proposals_by_candidate": ctr(proposals, "candidate"),
        "proposals_by_modality": ctr(proposals, "modality"),
        "facets": len(facets),
        "facets_by_candidate": ctr(facets, "candidate"),
        "facets_by_kind": ctr(facets, "facet_kind"),
        "unresolved_queue_items": len(unresolved),
        "unresolved_by_type": ctr(unresolved, "issue_type"),
        "view_rows": {"ORIGINAL_GROUP": sum(1 for v in view if v["view_record_type"] == "ORIGINAL_GROUP"),
                      "PROVISIONAL_NEW_CLAUSE": len(proposals), "PROVISIONAL_FACET_OVERLAY": len(facets)},
    }
    atomic_write_json(OUT / "STATS.json", stats)

    # ---------------------------------------------------------------- manifest
    groups_by_cand = collections.Counter(g["candidate"] for _, g in base)
    manifest = {
        "augmentation_version": AUG_VERSION,
        "task": "_STAGE_A_KIT/31_CLAUDE_CODEX_PASS1_REVIEW_TASK_EN.md",
        "scope": "Adjudication of Codex iterative search pass_0001 only (152 claims incl. 4 pinned revisions); "
                 "no pass_0002+, no new extraction, no strictness comparison, no Stage 2.",
        "immutable_base_union": {
            "path": "stage_A/reconciled/step1_union/MERGED_FINDINGS.jsonl",
            "sha256": sha256_file(UNION / "MERGED_FINDINGS.jsonl"),
            "groups": sum(groups_by_cand.values()),
            "groups_by_candidate": {c: groups_by_cand[c] for c in CANDS},
            "rule": "Original groups, IDs, texts and provenance are unchanged; additions live only in this directory.",
        },
        "input_hashes": {"file": "INPUT_HASHES.json", "sha256": sha256_file(OUT / "INPUT_HASHES.json"),
                         "integrity_at_finalize": integ},
        "review_ledger": {"file": "PASS1_REVIEW_LEDGER.jsonl", "rows": len(ledger),
                          "claim_ids_cover_pass1": True, "by_disposition": stats["by_disposition"]},
        "proposed_new_clauses": {"file": "NEW_CLAUSE_PROPOSALS.jsonl", "count": len(proposals),
                                 "ids": [p["proposal_id"] for p in proposals]},
        "proposed_facet_overlays": {"file": "EXISTING_GROUP_FACETS.jsonl", "count": len(facets),
                                    "ids": [f["facet_id"] for f in facets],
                                    "target_groups": sorted({f["target_group_id"] for f in facets})},
        "unresolved_review_queue": {"file": "UNRESOLVED_REVIEW_QUEUE.jsonl", "count": len(unresolved),
                                    "by_type": stats["unresolved_by_type"]},
        "augmented_view": {"file": "AUGMENTED_UNION_VIEW.jsonl", "rows": len(view), "row_types": stats["view_rows"],
                           "derived": True, "additions_provisional": True},
        "deterministic_identifiers": {
            "ledger": "AUG1-LR-<CIS claim id>",
            "proposal": "AUG1-NC-<CIS claim id>-<a|b|...> (order of proposal lines in _review/<C>.rev)",
            "facet": "AUG1-FX-<CIS claim id>-<a|b|...> (order of facet lines in _review/<C>.rev)",
            "unresolved": "AUG1-UR-<CIS claim id> (disposition) / AUG1-UR-<CIS claim id>-<n> (secondary issue)",
        },
        "stage2_assembly": [
            "Start from every ORIGINAL_GROUP row (or the immutable base file); never rewrite group IDs or texts.",
            "Attach PROVISIONAL_FACET_OVERLAY rows to their target_group_id as explicit facets.",
            "Treat PROVISIONAL_NEW_CLAUSE rows as candidate-scoped proposals to be adjudicated (EXTRA vs ORACLE) in Stage 2.",
            "Consult UNRESOLVED_REVIEW_QUEUE.jsonl before relying on any affected claim.",
        ],
        "outputs_sha256": {n: sha256_file(OUT / n) for n in NAMES + ["AUGMENTED_UNION_VIEW.jsonl", "STATS.json"]},
        "checkpoints": {c: sha256_file(OUT / "CHECKPOINTS" / f"{c}.checkpoint.json") for c in CANDS},
        "review_files": {c: sha256_file(OUT / "_review" / f"{c}.rev") for c in CANDS},
    }
    atomic_write_json(OUT / "UNION_AUGMENTATION_MANIFEST.json", manifest)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
