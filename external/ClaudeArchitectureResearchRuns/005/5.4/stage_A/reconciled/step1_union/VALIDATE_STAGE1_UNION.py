#!/usr/bin/env python3
"""VALIDATE_STAGE1_UNION.py: deterministic structural/provenance validator for Stage A Step 1.

What it checks (independently re-implemented; it does not import the builder):
  * required ledgers exist and parse (UTF-8 JSON objects, one per line), unique IDs;
  * six-candidate coverage and per-candidate checkpoints;
  * lossless input accounting: every line of every original input JSONL (constraints,
    policies, orphans, Codex findings) is indexed once with identical raw SHA-256 and content;
  * RECORD_ACCOUNTING: one row per input record, valid disposition, every claim record
    (constraint / Codex finding) mapped to >= 1 finding group or explicitly UNRESOLVED;
    policy/orphan destinations recomputed from their own constraint ids in the same run;
  * referential integrity across index, occurrences, clauses, groups, decisions, queue,
    co-location index and accounting; no orphaned keys; each clause in exactly one group;
  * every declared evidence location (each Claude evidence segment, resolved in the same
    run's coverage_ranges.jsonl, and each Codex quote range) is represented by a clause;
  * exact excerpts and their hashes recomputed from the immutable files under inputs/;
    reported quotes re-checked against the cited lines; clause/occurrence/group IDs recomputed;
  * merged groups are connected by recorded duplicate decisions; SD rationales carry the
    scope/modality/exception/timing checks; no relation sits inside one group;
  * original labels/policy ids in groups equal the indexed originals (no rewritten provenance);
    no adjudication fields (origin/correctness/verdict ...) in group records;
  * inputs unchanged: INPUT_MANIFEST_SHA256.csv re-hashed; run files and outputs compared with
    the SHA-256 values frozen in CHECKPOINTS/<C>.checkpoint.json;
  * combined top-level ledgers equal the concatenation of checkpointed per-candidate ledgers.

What it does NOT check: whether a semantic-duplicate decision is *correct*. Semantic
equivalence is a reviewer judgment; the validator only proves it is recorded, attributed and
structurally consistent. A PASS is therefore not evidence that any claim is right, EXTRA,
ORACLE-linked or mandatory.

Exit codes: 0 PASS or PASS_WITH_OPEN_ISSUES, 1 FAIL.
Usage: python VALIDATE_STAGE1_UNION.py [--candidate C ...] [--allow-incomplete] [--json OUT]
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
LEDGERS = ["SOURCE_RECORD_INDEX", "SOURCE_OCCURRENCES", "SOURCE_CLAUSES", "MERGED_FINDINGS",
           "RECORD_ACCOUNTING", "MERGE_REVIEW_QUEUE", "SOURCE_VERIFICATION_ISSUES", "MERGE_DECISIONS",
           "CO_LOCATION_INDEX"]
TOP_LEDGERS = list(LEDGERS)
FORBIDDEN_GROUP_KEYS = {"origin", "correctness", "verdict", "is_extra", "true_extra", "validated_label",
                        "adjudicated_origin", "parity", "strictness", "final_category"}
DISP = {"CONSTRAINT": {"LINKED_TO_FINDING", "UNRESOLVED"}, "BLIND_FINDING": {"LINKED_TO_FINDING", "UNRESOLVED"},
        "POLICY": {"POLICY_CROSS_REFERENCE", "UNRESOLVED"},
        "ORPHAN": {"ORPHAN_CONTEXT_LINKED", "ORPHAN_PENDING_REVIEW", "UNRESOLVED"}}
RUN_ORDER = {"PRIMARY": 0, "REPLICA": 1, "CODEX": 2}
PRE_CHECKPOINT = False


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def shat(s: str) -> str:
    return sha(s.encode("utf-8"))


class V:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = collections.OrderedDict()

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)


def read_jsonl(p: Path, v: V, label: str):
    rows = []
    if not p.exists():
        v.err(f"missing file {label}")
        return rows
    raw = p.read_bytes()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        v.err(f"{label}: not UTF-8")
        return rows
    for i, line in enumerate(txt.split("\n"), 1):
        if not line.strip():
            continue
        try:
            o = json.loads(line)
        except Exception as ex:
            v.err(f"{label}:{i}: invalid JSON ({ex})")
            continue
        if not isinstance(o, dict):
            v.err(f"{label}:{i}: not a JSON object")
            continue
        rows.append(o)
    return rows


def input_lines(rel: str):
    data = (ROOT / rel).read_bytes()
    parts = data.split(b"\n")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    for i, raw in enumerate(parts, 1):
        if raw.endswith(b"\r"):
            raw = raw[:-1]
        if raw.strip():
            yield i, raw


def inputs_for(c):
    out = []
    for run, d in (("PRIMARY", "primary"), ("REPLICA", "replica")):
        out += [(run, "CONSTRAINT", f"stage_A/{d}/{c}/constraints.jsonl", "id"),
                (run, "POLICY", f"stage_A/{d}/{c}/policies.jsonl", "rule_id"),
                (run, "ORPHAN", f"stage_A/{d}/{c}/ORPHAN_CANDIDATES.jsonl", "id")]
    out.append(("CODEX", "BLIND_FINDING", f"stage_A/independent/{c}/blind/BLIND_FINDINGS.jsonl", "id"))
    return out


def support_for(c):
    out = []
    for d in ("primary", "replica"):
        out += [f"stage_A/{d}/{c}/coverage_ranges.jsonl", f"stage_A/{d}/{c}/files.jsonl"]
    out += [f"stage_A/independent/{c}/blind/FILE_REVIEW_LEDGER.jsonl", f"stage_A/independent/{c}/blind/BLIND_COMPLETE.json"]
    return out


_TXT = {}


def excerpt(c, path, s, e):
    k = (c, path)
    if k not in _TXT:
        p = ROOT / "inputs" / c / path
        try:
            t = p.read_bytes().decode("utf-8")
        except Exception:
            _TXT[k] = None
        else:
            spans, pos = [], 0
            while True:
                j = t.find("\n", pos)
                if j == -1:
                    spans.append((pos, len(t)))
                    break
                spans.append((pos, j - 1 if j > pos and t[j - 1] == "\r" else j))
                pos = j + 1
            _TXT[k] = (t, spans)
    d = _TXT[k]
    if d is None:
        return None
    t, spans = d
    if not (isinstance(s, int) and isinstance(e, int)) or s < 1 or e < s or e > len(spans):
        return None
    return t[spans[s - 1][0]: spans[e - 1][1]]


def wsn(s):
    return re.sub(r"\s+", " ", s.replace("\r", "")).strip()


def qmatch(q, ex):
    if q is None or q == "":
        return "NO_REPORTED_QUOTE"
    a, b = ex.replace("\r\n", "\n"), q.replace("\r\n", "\n")
    if a == b:
        return "EXACT_FULL_RANGE"
    if b in a:
        return "EXACT_SUBSTRING"
    if wsn(b) and wsn(b) in wsn(a):
        return "WHITESPACE_NORMALIZED_SUBSTRING"
    return "MISMATCH"


def validate_manifest(v: V):
    p = ROOT / "inputs" / "INPUT_MANIFEST_SHA256.csv"
    if not p.exists():
        v.err("inputs/INPUT_MANIFEST_SHA256.csv missing")
        return None
    bad = 0
    n = 0
    with open(p, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            fp = ROOT / "inputs" / row["relative_path"]
            if not fp.exists() or sha(fp.read_bytes()) != row["sha256"]:
                bad += 1
                v.err(f"input snapshot changed or missing: inputs/{row['relative_path']}")
    v.info["input_manifest_files_verified"] = n - bad
    return sha(p.read_bytes())


def validate_candidate(c, v: V, require_complete: bool):
    od = HERE / "per_candidate" / c
    if not od.exists():
        (v.err if require_complete else v.warn)(f"{c}: no per_candidate outputs")
        return None
    L = {n: read_jsonl(od / f"{n}.jsonl", v, f"{c}/{n}.jsonl") for n in LEDGERS}
    summ_p = od / "BUILD_SUMMARY.json"
    summ = json.loads(summ_p.read_text(encoding="utf-8")) if summ_p.exists() else None
    if summ is None:
        v.err(f"{c}: BUILD_SUMMARY.json missing")
    stats = collections.Counter()

    # ---------------- lossless input index
    idx = {}
    for r in L["SOURCE_RECORD_INDEX"]:
        if r.get("record_key") in idx:
            v.err(f"{c}: duplicate index key {r.get('record_key')}")
        idx[r.get("record_key")] = r
    expected = {}
    for run, rtype, rel, idf in inputs_for(c):
        if not (ROOT / rel).exists():
            v.err(f"{c}: input file missing {rel}")
            continue
        seen = set()
        for ordinal, raw in input_lines(rel):
            try:
                o = json.loads(raw.decode("utf-8"))
            except Exception:
                v.err(f"{c}: unparseable input line {rel}:{ordinal}")
                continue
            key = f"{run}:{c}:{rtype}:{o.get(idf)}"
            if key in seen or key in expected:
                key = f"{key}#L{ordinal}"
            seen.add(key)
            expected[key] = (rel, ordinal, sha(raw), o, run, rtype)
            stats[f"{run}/{rtype}"] += 1
    for k, (rel, ordinal, h, o, run, rtype) in expected.items():
        r = idx.get(k)
        if r is None:
            v.err(f"{c}: input record not indexed: {k} ({rel}:{ordinal})")
            continue
        if r.get("raw_sha256") != h or r.get("input_file") != rel or r.get("ordinal") != ordinal:
            v.err(f"{c}: index pointer/hash mismatch for {k}")
        if r.get("raw_record") != o:
            v.err(f"{c}: index raw_record differs from input for {k}")
        if r.get("run") != run or r.get("record_type") != rtype or r.get("candidate") != c:
            v.err(f"{c}: index run/type/candidate wrong for {k}")
    for k in idx:
        if k not in expected:
            v.err(f"{c}: index contains unknown record {k}")
    claim_keys = {k for k, x in expected.items() if x[5] in ("CONSTRAINT", "BLIND_FINDING")}

    # ---------------- coverage segments (same run)
    cov = {}
    for run, d in (("PRIMARY", "primary"), ("REPLICA", "replica")):
        cov[run] = {}
        for _, raw in input_lines(f"stage_A/{d}/{c}/coverage_ranges.jsonl"):
            s = json.loads(raw.decode("utf-8"))
            cov[run][s["segment_id"]] = s

    # ---------------- occurrences
    occ = {}
    for o in L["SOURCE_OCCURRENCES"]:
        oid = o.get("occurrence_id")
        if oid in occ:
            v.err(f"{c}: duplicate occurrence {oid}")
        occ[oid] = o
        loc = f"{c}|{o.get('path')}|{o.get('start_line')}|{o.get('end_line')}"
        exp_id = f"OC-{c}-{shat(loc)[:12]}"
        if oid != exp_id:
            v.err(f"{c}: occurrence id not reproducible {oid}")
        ex = excerpt(c, o.get("path"), o.get("start_line"), o.get("end_line"))
        if o.get("location_status") == "VERIFIED_RANGE":
            if ex is None or ex != o.get("exact_excerpt") or shat(ex) != o.get("excerpt_sha256"):
                v.err(f"{c}: occurrence {oid} excerpt does not match immutable file (false VERIFIED)")
        elif ex is not None:
            v.warn(f"{c}: occurrence {oid} marked unverified although the range resolves")

    # ---------------- groups
    groups = {}
    for g in L["MERGED_FINDINGS"]:
        gid = g.get("group_id")
        if gid in groups:
            v.err(f"{c}: duplicate group id {gid}")
        groups[gid] = g
        if g.get("candidate") != c:
            v.err(f"{c}: group {gid} has candidate {g.get('candidate')}")
        bad = FORBIDDEN_GROUP_KEYS & set(g)
        if bad:
            v.err(f"{c}: group {gid} carries adjudication fields {sorted(bad)}")
        if gid != f"FG-{c}-{shat(g.get('seed_claim_unit_id', ''))[:10]}":
            v.err(f"{c}: group id not reproducible from seed for {gid}")
        units = g.get("claim_unit_ids") or []
        if not units or g.get("seed_claim_unit_id") != units[0]:
            v.err(f"{c}: group {gid} seed/claim units inconsistent")
        for f in ("neutral_claim_text", "neutral_claim_text_source", "clause_ids", "source_record_keys",
                  "supporting_runs", "original_labels", "merge_type"):
            if f not in g or g[f] in (None, "", []):
                v.err(f"{c}: group {gid} missing {f}")

    # ---------------- clauses
    clauses = {}
    unit_group = {}
    rec_clause_locs = collections.defaultdict(set)
    for cl in L["SOURCE_CLAUSES"]:
        cid = cl.get("clause_id")
        if cid in clauses:
            v.err(f"{c}: duplicate clause id {cid}")
        clauses[cid] = cl
        if cl.get("group_id") not in groups:
            v.err(f"{c}: clause {cid} -> unknown group {cl.get('group_id')}")
        rk = cl.get("record_key")
        if rk not in claim_keys:
            v.err(f"{c}: clause {cid} -> unknown or non-claim record {rk}")
            continue
        u = cl.get("claim_unit_id")
        if not (u == rk or (u or "").startswith(rk + "#")):
            v.err(f"{c}: clause {cid} unit {u} not of record {rk}")
        if u in unit_group and unit_group[u] != cl.get("group_id"):
            v.err(f"{c}: claim unit {u} in two groups")
        unit_group[u] = cl.get("group_id")
        if cl.get("location_status") == "VERIFIED_RANGE":
            ex = excerpt(c, cl.get("path"), cl.get("start_line"), cl.get("end_line"))
            if ex is None or ex != cl.get("exact_excerpt") or shat(ex) != cl.get("excerpt_sha256"):
                v.err(f"{c}: clause {cid} exact_excerpt not supported by immutable file (false VERIFIED)")
            span = f"{c}|{cl.get('path')}|{cl.get('start_line')}|{cl.get('end_line')}|{cl.get('excerpt_sha256')}"
            exp = f"CL-{c}-{shat(span)[:10]}-{shat(u)[:6]}"
            if cid != exp:
                v.err(f"{c}: clause id not reproducible {cid}")
            if cl.get("occurrence_id") not in occ:
                v.err(f"{c}: clause {cid} -> unknown occurrence")
            if cl.get("reported_quote") and cl.get("anchor_basis") != "NARROWED_BY_REVIEWER_WITHIN_CODEX_QUOTE":
                qm = qmatch(cl["reported_quote"], ex or "")
                if qm != cl.get("reported_quote_match"):
                    v.err(f"{c}: clause {cid} quote_match {cl.get('reported_quote_match')} != recomputed {qm}")
                if qm == "MISMATCH":
                    v.err(f"{c}: clause {cid} marked VERIFIED but reported quote mismatches")
        else:
            stats["clauses_source_unverified"] += 1
        src = idx[rk]["raw_record"]
        if idx[rk]["record_type"] == "CONSTRAINT":
            sid = cl.get("evidence_segment_id")
            seg = cov[idx[rk]["run"]].get(sid)
            if seg is None:
                if cl.get("location_status") == "VERIFIED_RANGE":
                    v.err(f"{c}: clause {cid} verified but segment {sid} unresolvable in same run")
            else:
                if (seg["path"], seg["start_line"], seg["end_line"]) != (cl.get("path"), cl.get("start_line"), cl.get("end_line")):
                    v.err(f"{c}: clause {cid} location differs from same-run segment {sid}")
                if sid not in (src.get("evidence_segment_ids") or []):
                    v.err(f"{c}: clause {cid} cites segment {sid} not declared by {rk}")
                rec_clause_locs[rk].add(sid)
                for extra in cl.get("additional_evidence_segment_ids") or []:
                    rec_clause_locs[rk].add(extra)
        else:
            if cl.get("path") != src.get("path"):
                v.err(f"{c}: Codex clause {cid} path differs from finding")
            s, e = cl.get("start_line"), cl.get("end_line")
            if cl.get("anchor_basis") == "FULL_CODEX_QUOTE_RANGE":
                if (s, e) != (src.get("start_line"), src.get("end_line")):
                    v.err(f"{c}: Codex clause {cid} full-range anchor differs from finding range")
            elif cl.get("anchor_basis") == "NARROWED_BY_REVIEWER_WITHIN_CODEX_QUOTE":
                if not (isinstance(s, int) and src["start_line"] <= s <= e <= src["end_line"]):
                    v.err(f"{c}: Codex clause {cid} narrowed anchor outside the finding's quote")
            else:
                v.err(f"{c}: Codex clause {cid} unknown anchor basis")
            rec_clause_locs[rk].add("CODEX")
        # provenance of labels
        lab_field = "origin" if idx[rk]["record_type"] == "CONSTRAINT" else "classification"
        if cl.get("reported_label") != src.get(lab_field):
            v.err(f"{c}: clause {cid} reported_label rewritten")
    # every declared evidence location represented
    for rk in claim_keys:
        src = idx.get(rk, {}).get("raw_record", {})
        if idx.get(rk, {}).get("record_type") == "CONSTRAINT":
            missing = set(src.get("evidence_segment_ids") or []) - rec_clause_locs[rk]
            if missing:
                v.err(f"{c}: evidence segments of {rk} not represented by clauses: {sorted(missing)[:5]}")
            if not (src.get("evidence_segment_ids") or []) and rk not in {cl.get("record_key") for cl in clauses.values()}:
                v.err(f"{c}: {rk} has no evidence and no clause")
        elif "CODEX" not in rec_clause_locs[rk]:
            v.err(f"{c}: Codex finding {rk} has no clause")

    # ---------------- group <-> clause consistency
    seen_clause = set()
    for gid, g in groups.items():
        cids = g.get("clause_ids") or []
        for cid in cids:
            if cid not in clauses:
                v.err(f"{c}: group {gid} -> unknown clause {cid}")
                continue
            if cid in seen_clause:
                v.err(f"{c}: clause {cid} listed by two groups")
            seen_clause.add(cid)
            if clauses[cid].get("group_id") != gid:
                v.err(f"{c}: clause {cid} back-link mismatch")
        recs = {clauses[x]["record_key"] for x in cids if x in clauses}
        if set(g.get("source_record_keys") or []) != recs:
            v.err(f"{c}: group {gid} source_record_keys != records of its clauses")
        runs = sorted({idx[k]["run"] for k in recs if k in idx}, key=RUN_ORDER.get)
        if (g.get("supporting_runs") or []) != runs:
            v.err(f"{c}: group {gid} supporting_runs wrong")
        units = set(g.get("claim_unit_ids") or [])
        if units != {clauses[x]["claim_unit_id"] for x in cids if x in clauses}:
            v.err(f"{c}: group {gid} claim_unit_ids != units of its clauses")
        for lab in g.get("original_labels") or []:
            k = lab.get("record_key")
            if k not in idx:
                v.err(f"{c}: group {gid} label for unknown record {k}")
                continue
            o = idx[k]["raw_record"]
            if idx[k]["record_type"] == "CONSTRAINT":
                ok = lab.get("reported_label") == o.get("origin") and lab.get("reported_policy_ids") == o.get("policy_ids")
            else:
                ok = lab.get("reported_label") == o.get("classification") and lab.get("reported_policy_ids") == o.get("closest_policy_ids")
            if not ok:
                v.err(f"{c}: group {gid} original label/policy ids of {k} rewritten")
        if {lab.get("record_key") for lab in g.get("original_labels") or []} != recs:
            v.err(f"{c}: group {gid} original_labels do not cover exactly its records")
        # connectivity by recorded merge decisions
        if len(units) == 1:
            if g.get("merge_type") != "SINGLETON":
                v.err(f"{c}: group {gid} has one unit but merge_type {g.get('merge_type')}")
        else:
            par = {u: u for u in units}

            def fd(x):
                while par[x] != x:
                    par[x] = par[par[x]]
                    x = par[x]
                return x
            for m in g.get("merge_decisions") or []:
                us = [u for u in m.get("claim_unit_ids", []) if u in par]
                if m.get("type") == "SEMANTIC_DUPLICATE":
                    rat = m.get("rationale") or ""
                    if not all(t in rat for t in ("S:", "M:", "E:", "T:")):
                        v.err(f"{c}: SD decision {m.get('decision_id')} omits scope/modality/exception/timing checks")
                if m.get("type") not in ("SEMANTIC_DUPLICATE", "EXACT_DUPLICATE"):
                    v.err(f"{c}: unknown merge type in {gid}")
                for u in us[1:]:
                    par[fd(u)] = fd(us[0])
            if len({fd(u) for u in units}) != 1:
                v.err(f"{c}: group {gid} is not connected by recorded duplicate decisions (unsupported merge)")
            stats["merged_groups"] += 1
    for cid in clauses:
        if cid not in seen_clause:
            v.err(f"{c}: clause {cid} not listed by any group")

    # ---------------- accounting
    acct = {}
    for a in L["RECORD_ACCOUNTING"]:
        k = a.get("record_key")
        if k in acct:
            v.err(f"{c}: accounting row duplicated for {k}")
        acct[k] = a
    rec_groups = collections.defaultdict(set)
    for cl in clauses.values():
        rec_groups[cl["record_key"]].add(cl["group_id"])
    by_run_id = {}
    for k, x in expected.items():
        by_run_id[(x[4], x[5], x[3].get("id") or x[3].get("rule_id"))] = k
    for k, x in expected.items():
        a = acct.get(k)
        if a is None:
            v.err(f"{c}: record missing from accounting: {k}")
            continue
        rtype = x[5]
        d = a.get("disposition")
        if d not in DISP[rtype]:
            v.err(f"{c}: {k} has invalid disposition {d}")
        gs = a.get("group_ids") or []
        for gid in gs:
            if gid not in groups:
                v.err(f"{c}: accounting {k} -> unknown group {gid}")
        for gid in a.get("co_located_group_ids") or []:
            if gid not in groups:
                v.err(f"{c}: accounting {k} -> unknown co-located group {gid}")
        if rtype in ("CONSTRAINT", "BLIND_FINDING"):
            if d == "LINKED_TO_FINDING" and set(gs) != rec_groups[k]:
                v.err(f"{c}: accounting groups of {k} differ from its clauses' groups")
            if d == "LINKED_TO_FINDING" and not gs:
                v.err(f"{c}: {k} LINKED_TO_FINDING without group")
            if d == "UNRESOLVED" and not a.get("note"):
                v.err(f"{c}: {k} UNRESOLVED without explanation")
            stats[f"claim_{d}"] += 1
        else:
            o = x[3]
            ids = o.get("atomic_constraint_ids") if rtype == "POLICY" else o.get("constraint_ids")
            exp_g = set()
            for cid in ids or []:
                ck = by_run_id.get((x[4], "CONSTRAINT", cid))
                if ck:
                    exp_g |= rec_groups[ck]
            if set(gs) != exp_g:
                v.err(f"{c}: {k} destinations differ from groups of its own constraint ids")
            if rtype == "ORPHAN":
                if d == "ORPHAN_CONTEXT_LINKED" and not gs:
                    v.err(f"{c}: {k} ORPHAN_CONTEXT_LINKED without group")
                if d == "ORPHAN_PENDING_REVIEW" and gs:
                    v.err(f"{c}: {k} ORPHAN_PENDING_REVIEW but has linked groups")
                stats[f"orphan_{d}"] += 1
    for k in acct:
        if k not in expected:
            v.err(f"{c}: accounting row for unknown record {k}")
    # policies/orphans never support groups
    for gid, g in groups.items():
        for k in g.get("source_record_keys") or []:
            if k in idx and idx[k]["record_type"] in ("POLICY", "ORPHAN"):
                v.err(f"{c}: group {gid} counts a {idx[k]['record_type']} row as a supporting claim")

    # ---------------- decisions, queue, co-location
    units_all = set(unit_group)
    for dct in L["MERGE_DECISIONS"]:
        for f in ("claim_unit_ids", "claim_unit_ids_a", "claim_unit_ids_b"):
            for u in dct.get(f) or []:
                if u not in units_all:
                    v.err(f"{c}: decision {dct.get('decision_id')} -> unknown claim unit {u}")
    qids = set()
    open_items = collections.Counter()
    for q in L["MERGE_REVIEW_QUEUE"]:
        qid = q.get("queue_id")
        if qid in qids:
            v.err(f"{c}: duplicate queue id {qid}")
        qids.add(qid)
        for gid in (q.get("group_ids_a") or []) + (q.get("group_ids_b") or []):
            if gid not in groups:
                v.err(f"{c}: queue {qid} -> unknown group {gid}")
        for k in q.get("record_keys") or []:
            if k not in idx:
                v.err(f"{c}: queue {qid} -> unknown record {k}")
        if q.get("item_type") in ("RELATED_BUT_DISTINCT", "APPARENT_CONFLICT", "UNRESOLVED"):
            if set(q.get("group_ids_a") or []) & set(q.get("group_ids_b") or []):
                v.err(f"{c}: queue {qid}: {q.get('item_type')} between members of one group")
        if not q.get("open_question"):
            v.err(f"{c}: queue {qid} has no open question")
        open_items[q.get("item_type")] += 1
    unreviewed = 0
    for r in L["CO_LOCATION_INDEX"]:
        for gid in r.get("group_ids") or []:
            if gid not in groups:
                v.err(f"{c}: co-location {r.get('region_id')} -> unknown group")
        if not r.get("reviewed"):
            unreviewed += 1
    if unreviewed:
        (v.err if require_complete else v.warn)(f"{c}: {unreviewed} co-location regions not reviewed")
    codex = [k for k in claim_keys if idx.get(k, {}).get("record_type") == "BLIND_FINDING"]
    normed = {u.split("#")[0] for dct in L["MERGE_DECISIONS"] if dct.get("type") in ("CODEX_NORMALIZATION", "SPLIT_PART")
              for u in dct.get("claim_unit_ids") or []}
    miss = [k for k in codex if k not in normed]
    if miss:
        (v.err if require_complete else v.warn)(f"{c}: {len(miss)} Codex findings lack a recorded normalization (CX/SPLIT)")
    sv = collections.Counter()
    for i in L["SOURCE_VERIFICATION_ISSUES"]:
        sv[f"{i.get('severity')}:{i.get('type')}"] += 1
        if i.get("record_key") and i["record_key"] not in idx:
            v.err(f"{c}: verification issue -> unknown record")

    # ---------------- checkpoint immutability
    cp = HERE / "CHECKPOINTS" / f"{c}.checkpoint.json"
    if cp.exists():
        ck = json.loads(cp.read_text(encoding="utf-8"))
        for rel, h in (ck.get("input_sha256") or {}).items():
            p = ROOT / rel
            if not p.exists() or sha(p.read_bytes()) != h:
                v.err(f"{c}: input changed since checkpoint: {rel}")
        for rel, h in (ck.get("output_sha256") or {}).items():
            p = HERE / rel
            if not p.exists() or sha(p.read_bytes()) != h:
                v.err(f"{c}: checkpointed output modified or missing: {rel}")
        if ck.get("group_ids_sha256") != shat("\n".join(sorted(groups))):
            v.err(f"{c}: group IDs changed since checkpoint")
        for rel in [x[2] for x in inputs_for(c)] + support_for(c):
            if rel not in (ck.get("input_sha256") or {}):
                v.err(f"{c}: checkpoint lacks hash for {rel}")
    elif require_complete and not PRE_CHECKPOINT:
        v.err(f"{c}: checkpoint missing")

    v.info[c] = {"input_records": dict(stats_filter(stats, "/")), "groups": len(groups), "merged_groups": stats["merged_groups"],
                 "clauses": len(clauses), "occurrences": len(occ), "review_queue": dict(open_items),
                 "source_verification_issues": dict(sv), "unreviewed_regions": unreviewed,
                 "orphans_pending": stats["orphan_ORPHAN_PENDING_REVIEW"], "claims_unresolved": stats["claim_UNRESOLVED"],
                 "checkpoint": cp.exists()}
    return {"open": sum(open_items.values()) + stats["orphan_ORPHAN_PENDING_REVIEW"] + stats["claim_UNRESOLVED"]
            + sum(n for k, n in sv.items() if not k.startswith("INFO"))}


def stats_filter(st, sub):
    return {k: v for k, v in st.items() if sub in k}


def validate_top(v: V, cands):
    for n in TOP_LEDGERS:
        p = HERE / f"{n}.jsonl"
        if not p.exists():
            v.err(f"top-level {n}.jsonl missing")
            continue
        want = b""
        for c in cands:
            q = HERE / "per_candidate" / c / f"{n}.jsonl"
            if q.exists():
                want += q.read_bytes()
        if p.read_bytes() != want:
            v.err(f"top-level {n}.jsonl is not the concatenation of checkpointed per-candidate ledgers {cands}")
    for f in ("MERGE_PROTOCOL.md", "STEP1_UNION_REPORT.md", "VALIDATE_STAGE1_UNION.py"):
        if not (HERE / f).exists():
            v.err(f"missing deliverable {f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", nargs="*")
    ap.add_argument("--allow-incomplete", action="store_true",
                    help="report missing candidates/regions as warnings (progress check only; never a final PASS)")
    ap.add_argument("--pre-checkpoint", action="store_true",
                    help="used by checkpoint.py before the checkpoint file is written (only with --candidate)")
    ap.add_argument("--json")
    a = ap.parse_args()
    global PRE_CHECKPOINT
    PRE_CHECKPOINT = bool(a.pre_checkpoint and a.candidate)
    v = V()
    cands = a.candidate or CANDS
    for c in cands:
        if c not in CANDS:
            v.err(f"unknown candidate {c}")
    if "L1-Restart" in {p.name for p in (HERE / "per_candidate").glob("*")} if (HERE / "per_candidate").exists() else False:
        v.err("L1-Restart must not be reintroduced")
    v.info["input_manifest_sha256"] = validate_manifest(v)
    opens = 0
    for c in cands:
        r = validate_candidate(c, v, require_complete=not a.allow_incomplete)
        if r:
            opens += r["open"]
    if not a.candidate:
        done = [c for c in CANDS if (HERE / "CHECKPOINTS" / f"{c}.checkpoint.json").exists()]
        if len(done) != 6:
            (v.warn if a.allow_incomplete else v.err)(f"checkpoints present for {done}; six required")
        validate_top(v, done) if (not a.allow_incomplete or done) else None
    if v.errors:
        result = "FAIL"
    elif a.allow_incomplete and (v.warnings or len(cands) < 6):
        result = "INCOMPLETE_PROGRESS_CHECK"
    elif opens or v.warnings:
        result = "PASS_WITH_OPEN_ISSUES"
    else:
        result = "PASS"
    out = {"result": result, "errors": v.errors[:500], "error_count": len(v.errors), "warnings": v.warnings[:200],
           "warning_count": len(v.warnings), "info": v.info,
           "scope_note": "Structural/provenance validation only; semantic-equivalence decisions are reviewer judgments and are not proven correct by this validator."}
    s = json.dumps(out, indent=1, ensure_ascii=False)
    if a.json:
        Path(a.json).write_text(s, encoding="utf-8")
    print(s if len(s) < 20000 else s[:20000] + "\n...")
    print(f"RESULT: {result}")
    return 1 if result == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
