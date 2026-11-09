"""Compile reviewer decisions (_review/<C>.rev) into per-candidate outputs.

  python -B build.py <C>               # build per_candidate/<C>/*
  python -B build.py <C> --checkpoint  # build, verify integrity, write CHECKPOINTS/<C>.checkpoint.json, update PROGRESS.json

Decision grammar (one block per pass-1 claim, keys may continue on lines indented by two spaces):

  @@ <CIS id>
  disp: ALREADY_REPRESENTED | EXISTING_GROUP_NEEDS_EXPLICIT_FACET | DISTINCT_UNREPRESENTED_CLAUSE
        | NOT_AN_INDEPENDENT_CONSTRAINT | UNRESOLVED
  nature: <source-truth category, e.g. OBLIGATION, DEFAULT, CHECKER_ACCEPTANCE_GATE ...>
  appl: actor=..; action=..; trigger=..; modality=..; scope=..; exceptions=..; timing=..; enforcement=..; loading=..
  match: FG-... [FG-...]          # groups that represent it / facet targets / behaviour it merely implements
  compared: FG-... [FG-...]       # other same-candidate groups inspected (closest non-matches)
  rationale: ...
  scenario: ...                   # distinguishing scenario, or "N/A: <reason>"
  conf: HIGH | MEDIUM | LOW
  question: ...                   # required for UNRESOLVED
  next_check: ...                 # required for UNRESOLVED
  facet: <FG-id> | NEW_GRANULARITY|NEW_BEHAVIOR_BOUNDARY | <facet text>     (repeatable)
  proposal: <modality> | <trigger/scope> | <clause text>                    (repeatable)
  open_issue: ...                 # secondary open issue on a non-UNRESOLVED claim (repeatable)
  policy_hint: <ids or free text> # non-binding suspected policy link
"""
from __future__ import annotations

import collections
import datetime
import json
import re
import subprocess
import sys

from aug_lib import (AUG_VERSION, CANDS, DISPOSITIONS, OUT, ROOT, UnionIndex, atomic_write_json,
                     atomic_write_jsonl, load_queue, sha256_file, source_lines)

APPL_KEYS = ["actor", "action", "trigger", "modality", "scope", "exceptions", "timing", "enforcement", "loading"]
REPEATABLE = {"facet", "proposal", "open_issue"}
KNOWN = {"disp", "nature", "appl", "match", "compared", "rationale", "scenario", "conf", "question",
         "next_check", "facet", "proposal", "open_issue", "policy_hint", "basis"}
FACET_KINDS = {"NEW_GRANULARITY", "NEW_BEHAVIOR_BOUNDARY"}
CODE_EXT = (".mjs", ".js", ".cjs", ".ts", ".json", ".ps1", ".sh", ".py", ".cs", ".csproj", ".props", ".yml", ".yaml")


def parse_rev(path):
    blocks, errors = {}, []
    cur = None
    last_key = None
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@@ "):
            cid = line[3:].strip()
            if cid in blocks:
                errors.append(f"{path.name}:{n} duplicate block {cid}")
            cur = {"_line": n, "_id": cid}
            blocks[cid] = cur
            last_key = None
            continue
        if cur is None:
            errors.append(f"{path.name}:{n} text outside block")
            continue
        if line.startswith("  ") and last_key:
            if last_key in REPEATABLE:
                cur[last_key][-1] += " " + line.strip()
            else:
                cur[last_key] += " " + line.strip()
            continue
        m = re.match(r"^([a-z_]+):\s?(.*)$", line)
        if not m or m.group(1) not in KNOWN:
            errors.append(f"{path.name}:{n} bad line: {line[:80]}")
            continue
        k, v = m.group(1), m.group(2).strip()
        if k in REPEATABLE:
            cur.setdefault(k, []).append(v)
        else:
            if k in cur:
                errors.append(f"{path.name}:{n} repeated key {k} in {cur['_id']}")
            cur[k] = v
        last_key = k
    return blocks, errors


def parse_appl(s):
    d = {}
    for part in re.split(r";\s*(?=[a-z_]+=)", s or ""):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip().rstrip(";")
    return d


def suffixes(n):
    return [chr(ord("a") + i) for i in range(n)]


def build(cand):
    U = UnionIndex()
    queue = [q for q in load_queue() if q["candidate"] == cand]
    revp = OUT / "_review" / f"{cand}.rev"
    blocks, errors = parse_rev(revp)
    qids = {q["claim_id"] for q in queue}
    for cid in blocks:
        if cid not in qids:
            errors.append(f"block for claim not in {cand} queue: {cid}")
    for cid in sorted(qids - set(blocks)):
        errors.append(f"missing decision for {cid}")
    ledger, proposals, facets, unresolved = [], [], [], []
    cand_groups = set(U.groups_by_cand[cand])
    for q in queue:
        cid = q["claim_id"]
        b = blocks.get(cid)
        if b is None:
            continue
        disp = b.get("disp")
        if disp not in DISPOSITIONS:
            errors.append(f"{cid}: bad disp {disp}")
        for k in ("nature", "appl", "rationale", "scenario", "conf"):
            if not b.get(k):
                errors.append(f"{cid}: missing {k}")
        appl = parse_appl(b.get("appl", ""))
        miss = [k for k in APPL_KEYS if k not in appl]
        if miss:
            errors.append(f"{cid}: appl missing {miss}")
        if b.get("conf") not in ("HIGH", "MEDIUM", "LOW"):
            errors.append(f"{cid}: bad conf {b.get('conf')}")
        match = b.get("match", "").split()
        compared = b.get("compared", "").split()
        for gid in match + compared:
            if gid not in U.groups:
                errors.append(f"{cid}: unknown group {gid}")
            elif gid not in cand_groups:
                errors.append(f"{cid}: cross-candidate group {gid}")
        if set(match) & set(compared):
            errors.append(f"{cid}: group both match and compared")
        if disp == "ALREADY_REPRESENTED" and not match:
            errors.append(f"{cid}: ALREADY_REPRESENTED needs match")
        if disp == "EXISTING_GROUP_NEEDS_EXPLICIT_FACET" and not b.get("facet"):
            errors.append(f"{cid}: FACET disposition needs facet lines")
        if disp != "EXISTING_GROUP_NEEDS_EXPLICIT_FACET" and b.get("facet"):
            errors.append(f"{cid}: facet lines only allowed for EXISTING_GROUP_NEEDS_EXPLICIT_FACET")
        if disp == "DISTINCT_UNREPRESENTED_CLAUSE" and not b.get("proposal"):
            errors.append(f"{cid}: DISTINCT disposition needs proposal lines")
        if disp != "DISTINCT_UNREPRESENTED_CLAUSE" and b.get("proposal"):
            errors.append(f"{cid}: proposal lines only allowed for DISTINCT_UNREPRESENTED_CLAUSE")
        if disp == "UNRESOLVED" and (not b.get("question") or not b.get("next_check")):
            errors.append(f"{cid}: UNRESOLVED needs question and next_check")
        evidence = {
            "candidate": cand, "path": q["path"], "source_file": q["source_file"],
            "start_line": q["start_line"], "end_line": q["end_line"], "quote": q["quote"],
            "quote_verification": q["quote_verification"], "source_file_sha256": q["source_file_sha256"],
            "codex_evidence_verification_status": q["codex_evidence_verification_status"],
        }
        basis = b.get("basis") or ("STATIC_CODE_OR_CONFIG_READ_NOT_EXECUTED"
                                   if q["path"].endswith(CODE_EXT) or q["path"].endswith(".editorconfig")
                                   else "INSTRUCTION_TEXT_READ_IN_CONTEXT")
        lrow = {
            "ledger_id": f"AUG1-LR-{cid}",
            "claim_id": cid,
            "candidate": cand,
            "augmentation_version": AUG_VERSION,
            "original_status": q["original_status"],
            "effective_status": q["effective_status"],
            "revision_id": q["revision_id"],
            "revision_path": q["revision_path"],
            "revision_field_updates": q["revision_field_updates"],
            "codex_claim": q["claim"],
            "codex_confidence": q["codex_confidence"],
            "codex_baseline_keys": sorted({k for bc in q["baseline_comparisons"] for k in bc["baseline_keys"]}),
            "codex_assessments": [bc["assessment"] for bc in q["baseline_comparisons"]],
            "codex_effective_closest_policy_ids": q["effective_closest_policy_ids"],
            "codex_open_question": q.get("open_question"),
            "evidence": evidence,
            "evidence_basis": basis,
            "source_nature": b.get("nature"),
            "applicability": appl,
            "disposition": disp,
            "matching_group_ids": match,
            "compared_group_ids": compared,
            "matched_group_texts": {g: U.groups[g]["neutral_claim_text"] for g in match if g in U.groups},
            "rationale": b.get("rationale"),
            "distinguishing_scenario": b.get("scenario"),
            "reviewer_confidence": b.get("conf"),
            "unresolved_question": b.get("question"),
            "next_check": b.get("next_check"),
            "suspected_policy_links_non_binding": b.get("policy_hint"),
            "proposal_ids": [],
            "facet_ids": [],
            "unresolved_queue_ids": [],
            "review_source": f"_review/{cand}.rev:{b['_line']}",
            "status_note": "Reviewer adjudication of a Codex pass-1 hypothesis; not an EXTRA/ORACLE or strictness verdict.",
        }
        lines = source_lines(cand, q["path"])
        excerpt = "\n".join(lines[q["start_line"] - 1:q["end_line"]])
        for sfx, ptxt in zip(suffixes(len(b.get("proposal", []))), b.get("proposal", [])):
            parts = [x.strip() for x in ptxt.split("|", 2)]
            if len(parts) != 3 or not all(parts):
                errors.append(f"{cid}: bad proposal line")
                continue
            pid = f"AUG1-NC-{cid}-{sfx}"
            proposals.append({
                "proposal_id": pid, "candidate": cand, "source_claim_id": cid, "ledger_id": lrow["ledger_id"],
                "augmentation_version": AUG_VERSION,
                "proposed_clause_text": parts[2], "modality": parts[0], "trigger_scope": parts[1],
                "applicability": appl,
                "evidence": dict(evidence, exact_excerpt=excerpt),
                "same_candidate_groups_compared": match + compared,
                "distinguishing_scenario": b.get("scenario"),
                "rationale": b.get("rationale"),
                "reviewer_confidence": b.get("conf"),
                "suspected_policy_links_non_binding": b.get("policy_hint"),
                "status": "PROVISIONAL_PROPOSAL",
                "status_note": "Proposal only: not a confirmed EXTRA, not an oracle mapping, not a cross-candidate comparison.",
            })
            lrow["proposal_ids"].append(pid)
        for sfx, ftxt in zip(suffixes(len(b.get("facet", []))), b.get("facet", [])):
            parts = [x.strip() for x in ftxt.split("|", 2)]
            if len(parts) != 3 or parts[1] not in FACET_KINDS:
                errors.append(f"{cid}: bad facet line")
                continue
            gid = parts[0]
            if gid not in U.groups or gid not in cand_groups:
                errors.append(f"{cid}: facet target {gid} invalid")
                continue
            if gid not in match:
                errors.append(f"{cid}: facet target {gid} must be listed in match")
            g = U.groups[gid]
            fid = f"AUG1-FX-{cid}-{sfx}"
            facets.append({
                "facet_id": fid, "candidate": cand, "target_group_id": gid,
                "target_group_raw_sha256": U.groups_raw_sha[gid],
                "target_group_original": {k: g[k] for k in ("neutral_claim_text", "neutral_claim_text_source",
                                                            "claim_unit_ids", "merge_type", "supporting_runs",
                                                            "source_record_keys")},
                "facet_kind": parts[1], "facet_text": parts[2],
                "source_claim_id": cid, "ledger_id": lrow["ledger_id"], "augmentation_version": AUG_VERSION,
                "evidence": dict(evidence, exact_excerpt=excerpt),
                "distinguishing_scenario": b.get("scenario"),
                "rationale": b.get("rationale"),
                "reviewer_confidence": b.get("conf"),
                "operation": "NON_DESTRUCTIVE_OVERLAY",
                "status": "PROVISIONAL_OVERLAY",
                "status_note": "Adds an explicit facet next to the original group; the original group, its ID, text and provenance are unchanged.",
            })
            lrow["facet_ids"].append(fid)
        if disp == "UNRESOLVED":
            uid = f"AUG1-UR-{cid}"
            unresolved.append({
                "queue_id": uid, "candidate": cand, "claim_id": cid, "ledger_id": lrow["ledger_id"],
                "issue_type": "UNRESOLVED_DISPOSITION", "original_status": q["original_status"],
                "effective_status": q["effective_status"], "question": b.get("question"),
                "next_check": b.get("next_check"), "compared_group_ids": match + compared,
                "evidence": evidence, "why_not_forced": b.get("rationale"),
                "augmentation_version": AUG_VERSION, "status": "OPEN",
            })
            lrow["unresolved_queue_ids"].append(uid)
        for i, oi in enumerate(b.get("open_issue", []), 1):
            uid = f"AUG1-UR-{cid}-{i}"
            unresolved.append({
                "queue_id": uid, "candidate": cand, "claim_id": cid, "ledger_id": lrow["ledger_id"],
                "issue_type": "SECONDARY_OPEN_ISSUE", "original_status": q["original_status"],
                "effective_status": q["effective_status"], "question": oi, "next_check": None,
                "compared_group_ids": match + compared, "evidence": evidence, "why_not_forced": None,
                "augmentation_version": AUG_VERSION, "status": "OPEN",
            })
            lrow["unresolved_queue_ids"].append(uid)
        ledger.append(lrow)
    return ledger, proposals, facets, unresolved, errors


def main():
    cand = sys.argv[1]
    assert cand in CANDS
    ledger, proposals, facets, unresolved, errors = build(cand)
    if errors:
        print("BUILD ERRORS:")
        for e in errors:
            print("  " + e)
        sys.exit(1)
    d = OUT / "per_candidate" / cand
    atomic_write_jsonl(d / "PASS1_REVIEW_LEDGER.jsonl", ledger)
    atomic_write_jsonl(d / "NEW_CLAUSE_PROPOSALS.jsonl", proposals)
    atomic_write_jsonl(d / "EXISTING_GROUP_FACETS.jsonl", facets)
    atomic_write_jsonl(d / "UNRESOLVED_REVIEW_QUEUE.jsonl", unresolved)
    counts = {
        "claims": len(ledger),
        "by_disposition": dict(collections.Counter(r["disposition"] for r in ledger)),
        "by_effective_status_and_disposition": {f"{k[0]} -> {k[1]}": v for k, v in sorted(collections.Counter(
            (r["effective_status"], r["disposition"]) for r in ledger).items())},
        "proposals": len(proposals), "facets": len(facets), "unresolved_queue_items": len(unresolved),
    }
    print(json.dumps(counts, indent=1))
    if "--checkpoint" in sys.argv:
        ver = subprocess.run([sys.executable, "-B", str(OUT / "_tools" / "preflight.py"), "--verify"],
                             cwd=str(OUT / "_tools"), capture_output=True, text=True)
        integ = json.loads(ver.stdout)
        if integ["integrity"] != "PASS":
            print("INTEGRITY ERROR: STOP", json.dumps(integ, indent=1))
            sys.exit(2)
        ck = {
            "candidate": cand, "augmentation_version": AUG_VERSION,
            "status": "CANDIDATE_REVIEW_COMPLETE",
            "written_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "counts": counts,
            "claim_ids": [r["claim_id"] for r in ledger],
            "review_file": f"_review/{cand}.rev",
            "review_file_sha256": sha256_file(OUT / "_review" / f"{cand}.rev"),
            "outputs_sha256": {f"per_candidate/{cand}/{n}": sha256_file(d / n) for n in (
                "PASS1_REVIEW_LEDGER.jsonl", "NEW_CLAUSE_PROPOSALS.jsonl", "EXISTING_GROUP_FACETS.jsonl",
                "UNRESOLVED_REVIEW_QUEUE.jsonl")},
            "input_hashes_sha256": sha256_file(OUT / "INPUT_HASHES.json"),
            "integrity_check": integ,
        }
        atomic_write_json(OUT / "CHECKPOINTS" / f"{cand}.checkpoint.json", ck)
        prog_p = OUT / "PROGRESS.json"
        prog = json.loads(prog_p.read_text(encoding="utf-8")) if prog_p.exists() else {}
        done = [c for c in CANDS if (OUT / "CHECKPOINTS" / f"{c}.checkpoint.json").exists()]
        prog.update({
            "task": "_STAGE_A_KIT/31_CLAUDE_CODEX_PASS1_REVIEW_TASK_EN.md",
            "augmentation_version": AUG_VERSION,
            "candidate_order": CANDS,
            "completed_candidates": done,
            "next_candidate": next((c for c in CANDS if c not in done), None),
            "claims_reviewed": sum(json.loads((OUT / "CHECKPOINTS" / f"{c}.checkpoint.json").read_text(
                encoding="utf-8"))["counts"]["claims"] for c in done),
            "claims_total": 152,
            "last_update": ck["written_at"],
            "resume_rule": "Re-read the task; run preflight.py --verify; resume at next_candidate; never rebuild a "
                           "checkpointed candidate unless its checkpoint hashes still match.",
        })
        prog.setdefault("finalized", False)
        atomic_write_json(prog_p, prog)
        print(f"CHECKPOINT written for {cand}; integrity PASS; warnings={integ['warnings']}")


if __name__ == "__main__":
    main()
