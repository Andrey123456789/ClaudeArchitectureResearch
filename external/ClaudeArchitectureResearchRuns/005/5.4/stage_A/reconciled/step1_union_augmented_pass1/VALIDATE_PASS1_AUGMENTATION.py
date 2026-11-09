#!/usr/bin/env python3
"""Validator for the Codex pass-1 adjudication and non-destructive union augmentation (Experiment 005 / 5.4).

Independent re-implementation: imports nothing from _tools/. Reads only the frozen inputs, the immutable
Step 1 union, Codex pass_0001 (+ the revisions named by its PASS_VALIDATION.json) and this directory.

  python -B VALIDATE_PASS1_AUGMENTATION.py            # prints the result and writes VALIDATION_RESULT.json
  python -B VALIDATE_PASS1_AUGMENTATION.py --no-write # prints only

Checks:
  C01 required outputs exist and every JSONL line parses
  C02 pinned input hashes unchanged (immutable files; pass-1 subset of rolling Codex files); no new files
      in the immutable union / pass_0001; inputs manifest still verifies
  C03 ledger has exactly one row per pass-1 claim id (152 expected), ids equal CANDIDATE_CLAIMS ids
  C04 original / effective statuses and revisions match pass_0001 + PASS_VALIDATION applied_revisions;
      recomputed totals
  C05 dispositions valid; required reviewer fields present
  C06 evidence: file exists under inputs/<C>/, listed in the inputs manifest, line range valid, quote equals
      the pass-1 quote and the source text (newline-normalised), file hash matches
  C07 every FG-* reference exists in the base union and belongs to the same candidate
  C08 disposition <-> addition consistency (proposals only for DISTINCT, facets only for FACET, queue item
      for UNRESOLVED, nothing extra for ALREADY_REPRESENTED / NOT_AN_INDEPENDENT_CONSTRAINT)
  C09 proposals: unique deterministic ids, provisional status, exact excerpt, traced to a reviewed claim,
      no collision with original ids, no duplicate incorporation
  C10 facets: unique deterministic ids, target group unchanged (raw-line hash and preserved fields),
      non-destructive overlay status, traced to a reviewed claim, no duplicate facet
  C11 unresolved queue integrity
  C12 per-candidate checkpoints match per-candidate files; top-level files equal their concatenation
  C13 augmented view retains all 6,347 original groups byte-equivalently and labels additions provisional
  C14 manifest consistency (counts and hashes)
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
UNION = ROOT / "stage_A" / "reconciled" / "step1_union"
CIS = ROOT / "stage_A" / "codex_iterative_search"
PASS1 = CIS / "PASSES" / "pass_0001"
INPUTS = ROOT / "inputs"
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
DISPOSITIONS = {"ALREADY_REPRESENTED", "EXISTING_GROUP_NEEDS_EXPLICIT_FACET", "DISTINCT_UNREPRESENTED_CLAUSE",
                "NOT_AN_INDEPENDENT_CONSTRAINT", "UNRESOLVED"}
APPL_KEYS = ["actor", "action", "trigger", "modality", "scope", "exceptions", "timing", "enforcement", "loading"]
OUTPUT_JSONL = ["REVIEW_QUEUE.jsonl", "PASS1_REVIEW_LEDGER.jsonl", "NEW_CLAUSE_PROPOSALS.jsonl",
                "EXISTING_GROUP_FACETS.jsonl", "UNRESOLVED_REVIEW_QUEUE.jsonl", "AUGMENTED_UNION_VIEW.jsonl"]
OUTPUT_JSON = ["INPUT_HASHES.json", "UNION_AUGMENTATION_MANIFEST.json", "PROGRESS.json", "PREFLIGHT_REPORT.json",
               "STATS.json"]
PER_CAND = ["PASS1_REVIEW_LEDGER.jsonl", "NEW_CLAUSE_PROPOSALS.jsonl", "EXISTING_GROUP_FACETS.jsonl",
            "UNRESOLVED_REVIEW_QUEUE.jsonl"]

errors, warnings, info = [], [], {}


def err(code, msg):
    errors.append(f"{code}: {msg}")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def jsonl(p):
    rows = []
    with open(p, "rb") as f:
        for n, raw in enumerate(f, 1):
            s = raw.rstrip(b"\r\n")
            if not s.strip():
                continue
            try:
                rows.append((s, json.loads(s.decode("utf-8"))))
            except Exception as e:  # noqa: BLE001
                err("C01", f"{p.name}:{n} invalid JSON ({e})")
    return rows


def src_lines(cand, path):
    t = (INPUTS / cand / path).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    ls = t.split("\n")
    return ls[:-1] if ls and ls[-1] == "" else ls


def tree(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts)


def rel(p):
    return p.resolve().relative_to(ROOT).as_posix()


def main():
    write = "--no-write" not in sys.argv
    # ---------------------------------------------------------------- C01
    for n in OUTPUT_JSONL + OUTPUT_JSON + ["REVIEW_REPORT.md"]:
        if not (HERE / n).is_file():
            err("C01", f"missing output {n}")
    if errors:
        return finish(write)
    out = {n: jsonl(HERE / n) for n in OUTPUT_JSONL}
    js = {n: json.loads((HERE / n).read_text(encoding="utf-8")) for n in OUTPUT_JSON}
    ledger = [o for _, o in out["PASS1_REVIEW_LEDGER.jsonl"]]
    proposals = [o for _, o in out["NEW_CLAUSE_PROPOSALS.jsonl"]]
    facets = [o for _, o in out["EXISTING_GROUP_FACETS.jsonl"]]
    unresolved = [o for _, o in out["UNRESOLVED_REVIEW_QUEUE.jsonl"]]
    view = [o for _, o in out["AUGMENTED_UNION_VIEW.jsonl"]]

    # ---------------------------------------------------------------- C02
    pin = js["INPUT_HASHES.json"]
    changed = [rp for rp, hv in pin["immutable_files"].items() if not (ROOT / rp).is_file() or sha_file(ROOT / rp) != hv]
    for rp in changed:
        err("C02", f"pinned file changed or missing: {rp}")
    for rp, d in pin["rolling_files_pass1_subset"].items():
        rows = [raw for raw, o in jsonl(ROOT / rp) if o.get("discovery_pass") == 1]
        if sha_bytes(b"\n".join(sorted(rows))) != d["pass1_subset_sha256"]:
            err("C02", f"pass-1 subset changed: {rp}")
        elif sha_file(ROOT / rp) != d["full_file_sha256_at_pin"]:
            warnings.append(f"C02: rolling file has later-pass changes (pass-1 subset unchanged, not imported): {rp}")
    for d, prefix in ((UNION, "stage_A/reconciled/step1_union/"), (PASS1, "stage_A/codex_iterative_search/PASSES/pass_0001/")):
        pinned = {rp for rp in pin["immutable_files"] if rp.startswith(prefix)}
        for p in tree(d):
            if rel(p) not in pinned:
                err("C02", f"new file in immutable directory: {rel(p)}")
    man_rows = list(csv.DictReader(open(INPUTS / "INPUT_MANIFEST_SHA256.csv", encoding="utf-8-sig", newline="")))
    man_paths = {r["relative_path"] for r in man_rows}
    bad = [r["relative_path"] for r in man_rows if sha_file(INPUTS / r["relative_path"]) != r["sha256"]]
    for b in bad:
        err("C02", f"inputs manifest mismatch: {b}")
    info["immutable_files_verified"] = len(pin["immutable_files"]) - len(changed)
    info["inputs_manifest_files_verified"] = len(man_rows) - len(bad)

    # ---------------------------------------------------------------- C03 / C04
    pv = json.loads((PASS1 / "PASS_VALIDATION.json").read_text(encoding="utf-8"))
    if pv.get("status") != "COMPLETE" or pv.get("source_files") != 448:
        err("C04", "PASS_VALIDATION is not COMPLETE/448")
    claims = {o["id"]: o for _, o in jsonl(PASS1 / "CANDIDATE_CLAIMS.jsonl")}
    ids = [r["claim_id"] for r in ledger]
    if len(ids) != len(set(ids)):
        err("C03", "duplicate claim ids in ledger")
    if set(ids) != set(claims):
        err("C03", f"ledger ids != pass-1 ids (missing {sorted(set(claims) - set(ids))[:5]}, extra {sorted(set(ids) - set(claims))[:5]})")
    if len(ledger) != 152:
        err("C03", f"ledger has {len(ledger)} rows, expected 152")
    revs = {}
    for fid, rv in pv["applied_revisions"].items():
        revs[fid] = json.loads((CIS / rv["revision"]).read_text(encoding="utf-8"))
    for r in ledger:
        c = claims.get(r["claim_id"])
        if not c:
            continue
        if r["candidate"] != c["candidate"]:
            err("C04", f"{r['claim_id']} candidate mismatch")
        if r["original_status"] != c["comparison_status"]:
            err("C04", f"{r['claim_id']} original status mismatch")
        rv = revs.get(r["claim_id"])
        exp_eff = rv["effective_status"] if rv else c["comparison_status"]
        if r["effective_status"] != exp_eff:
            err("C04", f"{r['claim_id']} effective status {r['effective_status']} != {exp_eff}")
        if (rv["revision_id"] if rv else None) != r["revision_id"]:
            err("C04", f"{r['claim_id']} revision id mismatch")
        exp_pol = (rv or {}).get("field_updates", {}).get("closest_policy_ids", c.get("closest_policy_ids") or [])
        if r["codex_effective_closest_policy_ids"] != exp_pol:
            err("C04", f"{r['claim_id']} revision field update not applied")
        if r["ledger_id"] != f"AUG1-LR-{r['claim_id']}":
            err("C03", f"{r['claim_id']} ledger id not deterministic")
    orig = collections.Counter(r["original_status"] for r in ledger)
    eff = collections.Counter(r["effective_status"] for r in ledger)
    info["original_status_totals"] = dict(sorted(orig.items()))
    info["effective_status_totals"] = dict(sorted(eff.items()))
    for k, v in pv["effective_counts_by_candidate"].items():
        got = dict(collections.Counter(r["effective_status"] for r in ledger if r["candidate"] == k))
        if got != v:
            err("C04", f"{k} effective counts {got} != PASS_VALIDATION {v}")
    info["revisions_applied"] = sorted(revs)

    # ---------------------------------------------------------------- base union index
    base_raw = jsonl(UNION / "MERGED_FINDINGS.jsonl")
    groups = {o["group_id"]: o for _, o in base_raw}
    group_sha = {o["group_id"]: sha_bytes(raw) for raw, o in base_raw}

    def check_fg(code, cand, gid, where):
        if not re.fullmatch(r"FG-[A-Z0-9]+-[0-9a-f]{10}", gid or ""):
            err(code, f"{where}: malformed group id {gid!r}")
        elif gid not in groups:
            err(code, f"{where}: unknown group {gid}")
        elif groups[gid]["candidate"] != cand or not gid.startswith(f"FG-{cand}-"):
            err(code, f"{where}: cross-candidate group {gid}")

    # ---------------------------------------------------------------- C05 / C06 / C07
    for r in ledger:
        cid, cand = r["claim_id"], r["candidate"]
        if r["disposition"] not in DISPOSITIONS:
            err("C05", f"{cid} invalid disposition {r['disposition']}")
        for k in ("rationale", "distinguishing_scenario", "reviewer_confidence", "source_nature", "review_source"):
            if not r.get(k):
                err("C05", f"{cid} missing {k}")
        if r.get("reviewer_confidence") not in ("HIGH", "MEDIUM", "LOW"):
            err("C05", f"{cid} invalid confidence")
        for k in APPL_KEYS:
            if not (r.get("applicability") or {}).get(k):
                err("C05", f"{cid} applicability.{k} missing")
        ev = r["evidence"]
        c = claims.get(cid, {})
        if ev["path"] != c.get("path") or ev["start_line"] != c.get("start_line") or ev["end_line"] != c.get("end_line"):
            err("C06", f"{cid} evidence location differs from pass-1 claim")
        if f"{cand}/{ev['path']}" not in man_paths:
            err("C06", f"{cid} path not in inputs manifest (invented path?): {ev['path']}")
        if ev["source_file"] != f"inputs/{cand}/{ev['path']}":
            err("C06", f"{cid} source_file mismatch")
        p = INPUTS / cand / ev["path"]
        if not p.is_file():
            err("C06", f"{cid} missing source file")
            continue
        if sha_file(p) != ev["source_file_sha256"]:
            err("C06", f"{cid} source hash mismatch")
        ls = src_lines(cand, ev["path"])
        if not (1 <= ev["start_line"] <= ev["end_line"] <= len(ls)):
            err("C06", f"{cid} invalid line range")
            continue
        seg = "\n".join(ls[ev["start_line"] - 1:ev["end_line"]])
        q = (ev["quote"] or "").replace("\r\n", "\n")
        if q != c.get("quote", "").replace("\r\n", "\n"):
            err("C06", f"{cid} quote differs from pass-1 quote")
        if not q or q not in seg:
            err("C06", f"{cid} quote not found in source range")
        for gid in r["matching_group_ids"] + r["compared_group_ids"]:
            check_fg("C07", cand, gid, cid)
        if set(r["matching_group_ids"]) & set(r["compared_group_ids"]):
            err("C07", f"{cid} group listed as both match and compared")
        if r["disposition"] in ("ALREADY_REPRESENTED", "EXISTING_GROUP_NEEDS_EXPLICIT_FACET") and not r["matching_group_ids"]:
            err("C07", f"{cid} {r['disposition']} without matching group")

    # ---------------------------------------------------------------- C08 / C09 / C10 / C11
    led = {r["claim_id"]: r for r in ledger}
    prop_by_claim = collections.defaultdict(list)
    for p in proposals:
        prop_by_claim[p["source_claim_id"]].append(p)
    fac_by_claim = collections.defaultdict(list)
    for f in facets:
        fac_by_claim[f["source_claim_id"]].append(f)
    ur_by_claim = collections.defaultdict(list)
    for u in unresolved:
        ur_by_claim[u["claim_id"]].append(u)
    for cid, r in led.items():
        d = r["disposition"]
        np_, nf = len(prop_by_claim[cid]), len(fac_by_claim[cid])
        if d == "DISTINCT_UNREPRESENTED_CLAUSE" and np_ == 0:
            err("C08", f"{cid} DISTINCT without proposal")
        if d != "DISTINCT_UNREPRESENTED_CLAUSE" and np_:
            err("C08", f"{cid} proposal from non-DISTINCT row")
        if d == "EXISTING_GROUP_NEEDS_EXPLICIT_FACET" and nf == 0:
            err("C08", f"{cid} FACET without facet record")
        if d != "EXISTING_GROUP_NEEDS_EXPLICIT_FACET" and nf:
            err("C08", f"{cid} facet from non-FACET row")
        disp_items = [u for u in ur_by_claim[cid] if u["issue_type"] == "UNRESOLVED_DISPOSITION"]
        if (d == "UNRESOLVED") != (len(disp_items) == 1):
            err("C08", f"{cid} UNRESOLVED disposition/queue mismatch")
        if sorted(r["proposal_ids"]) != sorted(p["proposal_id"] for p in prop_by_claim[cid]):
            err("C08", f"{cid} proposal_ids not traced")
        if sorted(r["facet_ids"]) != sorted(f["facet_id"] for f in fac_by_claim[cid]):
            err("C08", f"{cid} facet_ids not traced")
        if sorted(r["unresolved_queue_ids"]) != sorted(u["queue_id"] for u in ur_by_claim[cid]):
            err("C08", f"{cid} unresolved ids not traced")
    for x in set(prop_by_claim) | set(fac_by_claim) | set(ur_by_claim):
        if x not in led:
            err("C08", f"addition traced to unknown claim {x}")
    pids = [p["proposal_id"] for p in proposals]
    if len(pids) != len(set(pids)):
        err("C09", "duplicate proposal ids")
    seen_txt = set()
    for p in proposals:
        cid = p["source_claim_id"]
        if not re.fullmatch(rf"AUG1-NC-{re.escape(cid)}-[a-z]", p["proposal_id"]):
            err("C09", f"{p['proposal_id']} not deterministic")
        if p["proposal_id"] in groups:
            err("C09", f"{p['proposal_id']} collides with an original group id")
        if p["status"] != "PROVISIONAL_PROPOSAL":
            err("C09", f"{p['proposal_id']} not provisional")
        r = led.get(cid)
        if not r or r["candidate"] != p["candidate"] or p["ledger_id"] != r["ledger_id"]:
            err("C09", f"{p['proposal_id']} trace/candidate mismatch")
        ev = p["evidence"]
        ls = src_lines(p["candidate"], ev["path"])
        if ev.get("exact_excerpt") != "\n".join(ls[ev["start_line"] - 1:ev["end_line"]]):
            err("C09", f"{p['proposal_id']} exact excerpt mismatch")
        for k in ("proposed_clause_text", "modality", "trigger_scope", "distinguishing_scenario", "rationale"):
            if not p.get(k):
                err("C09", f"{p['proposal_id']} missing {k}")
        for gid in p["same_candidate_groups_compared"]:
            check_fg("C09", p["candidate"], gid, p["proposal_id"])
        if not p["same_candidate_groups_compared"]:
            err("C09", f"{p['proposal_id']} has no same-candidate comparison")
        key = (p["candidate"], ev["path"], ev["start_line"], ev["end_line"], " ".join(p["proposed_clause_text"].lower().split()))
        if key in seen_txt:
            err("C09", f"{p['proposal_id']} duplicate incorporation")
        seen_txt.add(key)
    fids = [f["facet_id"] for f in facets]
    if len(fids) != len(set(fids)):
        err("C10", "duplicate facet ids")
    seen_fac = set()
    for f in facets:
        cid = f["source_claim_id"]
        if not re.fullmatch(rf"AUG1-FX-{re.escape(cid)}-[a-z]", f["facet_id"]):
            err("C10", f"{f['facet_id']} not deterministic")
        check_fg("C10", f["candidate"], f["target_group_id"], f["facet_id"])
        g = groups.get(f["target_group_id"])
        if g:
            if f["target_group_raw_sha256"] != group_sha[f["target_group_id"]]:
                err("C10", f"{f['facet_id']} target group raw hash differs (group changed?)")
            for k, v in f["target_group_original"].items():
                if g.get(k) != v:
                    err("C10", f"{f['facet_id']} preserved field {k} differs from base group")
        if f["operation"] != "NON_DESTRUCTIVE_OVERLAY" or f["status"] != "PROVISIONAL_OVERLAY":
            err("C10", f"{f['facet_id']} not a provisional non-destructive overlay")
        if f["facet_kind"] not in ("NEW_GRANULARITY", "NEW_BEHAVIOR_BOUNDARY"):
            err("C10", f"{f['facet_id']} bad facet kind")
        r = led.get(cid)
        if not r or f["target_group_id"] not in r["matching_group_ids"] or r["candidate"] != f["candidate"]:
            err("C10", f"{f['facet_id']} trace mismatch")
        key = (f["target_group_id"], " ".join(f["facet_text"].lower().split()))
        if key in seen_fac:
            err("C10", f"{f['facet_id']} duplicate facet")
        seen_fac.add(key)
    uids = [u["queue_id"] for u in unresolved]
    if len(uids) != len(set(uids)):
        err("C11", "duplicate unresolved queue ids")
    for u in unresolved:
        if not u.get("question"):
            err("C11", f"{u['queue_id']} without question")
        if u["issue_type"] == "UNRESOLVED_DISPOSITION" and not u.get("next_check"):
            err("C11", f"{u['queue_id']} without next_check")
        for gid in u.get("compared_group_ids") or []:
            check_fg("C11", u["candidate"], gid, u["queue_id"])

    # ---------------------------------------------------------------- C12
    concat = {n: [] for n in PER_CAND}
    for c in CANDS:
        ckp = HERE / "CHECKPOINTS" / f"{c}.checkpoint.json"
        if not ckp.is_file():
            err("C12", f"missing checkpoint {c}")
            continue
        ck = json.loads(ckp.read_text(encoding="utf-8"))
        for n in PER_CAND:
            p = HERE / "per_candidate" / c / n
            if sha_file(p) != ck["outputs_sha256"][f"per_candidate/{c}/{n}"]:
                err("C12", f"{c}/{n} differs from its checkpoint")
            concat[n].extend(raw for raw, _ in jsonl(p))
        if sha_file(HERE / "_review" / f"{c}.rev") != ck["review_file_sha256"]:
            err("C12", f"review file {c}.rev changed after checkpoint")
        if ck["integrity_check"]["integrity"] != "PASS":
            err("C12", f"{c} checkpoint integrity not PASS")
    for n in PER_CAND:
        if [raw for raw, _ in out[n]] != concat[n]:
            err("C12", f"{n} is not the ordered concatenation of the per-candidate files")

    # ---------------------------------------------------------------- C13
    orig_rows = [v for v in view if v["view_record_type"] == "ORIGINAL_GROUP"]
    if len(orig_rows) != 6347 or {v["group_id"] for v in orig_rows} != set(groups):
        err("C13", f"augmented view original groups {len(orig_rows)} / ids differ from base")
    for v in orig_rows:
        gid = v["group_id"]
        if gid in groups and (v["original_group"] != groups[gid] or v["original_raw_sha256"] != group_sha[gid]):
            err("C13", f"view row for {gid} differs from the base group")
        if v["provisional"] is not False:
            err("C13", f"original row {gid} marked provisional")
    exp_overlays = collections.defaultdict(list)
    for f in facets:
        exp_overlays[f["target_group_id"]].append(f["facet_id"])
    for v in orig_rows:
        if sorted(v["facet_overlay_ids"]) != sorted(exp_overlays.get(v["group_id"], [])):
            err("C13", f"overlay ids for {v['group_id']} inconsistent")
    adds = [v for v in view if v["view_record_type"] != "ORIGINAL_GROUP"]
    if any(v.get("provisional") is not True for v in adds):
        err("C13", "an addition in the view is not labelled provisional")
    if sorted(v["proposal_id"] for v in adds if v["view_record_type"] == "PROVISIONAL_NEW_CLAUSE") != sorted(pids):
        err("C13", "view proposals differ from NEW_CLAUSE_PROPOSALS")
    if sorted(v["facet_id"] for v in adds if v["view_record_type"] == "PROVISIONAL_FACET_OVERLAY") != sorted(fids):
        err("C13", "view facets differ from EXISTING_GROUP_FACETS")

    # ---------------------------------------------------------------- C14
    man = js["UNION_AUGMENTATION_MANIFEST.json"]
    if man["immutable_base_union"]["sha256"] != sha_file(UNION / "MERGED_FINDINGS.jsonl"):
        err("C14", "manifest base union hash mismatch")
    if man["review_ledger"]["rows"] != len(ledger) or man["proposed_new_clauses"]["count"] != len(proposals) \
            or man["proposed_facet_overlays"]["count"] != len(facets) or man["unresolved_review_queue"]["count"] != len(unresolved):
        err("C14", "manifest counts mismatch")
    for n, hv in man["outputs_sha256"].items():
        if sha_file(HERE / n) != hv:
            err("C14", f"manifest hash mismatch for {n}")
    if js["PROGRESS.json"].get("claims_reviewed") != 152:
        err("C14", "PROGRESS.json does not record 152 reviewed claims")

    disp = collections.Counter(r["disposition"] for r in ledger)
    info["dispositions"] = {d: disp.get(d, 0) for d in sorted(DISPOSITIONS)}
    info["uncertain_resolved"] = sum(1 for r in ledger if r["effective_status"] == "UNCERTAIN_NOVELTY" and r["disposition"] != "UNRESOLVED")
    info["uncertain_retained_unresolved"] = sum(1 for r in ledger if r["effective_status"] == "UNCERTAIN_NOVELTY" and r["disposition"] == "UNRESOLVED")
    info["proposals"] = len(proposals)
    info["facets"] = len(facets)
    info["unresolved_queue_items"] = len(unresolved)
    info["view_rows"] = len(view)
    return finish(write)


def finish(write):
    result = {
        "validator": "VALIDATE_PASS1_AUGMENTATION.py",
        "result": "PASS" if not errors else "FAIL",
        "error_count": len(errors), "errors": errors,
        "warning_count": len(warnings), "warnings": warnings,
        "info": info,
        "scope_note": "Structural, provenance and integrity validation; reviewer judgements are evidence-backed but not proven by this script.",
    }
    text = json.dumps(result, indent=1, ensure_ascii=False)
    print(text)
    print(f"RESULT: {result['result']}")
    if write:
        (HERE / "VALIDATION_RESULT.json").write_text(text + "\n", encoding="utf-8", newline="\n")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
