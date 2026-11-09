"""Compile one candidate's Step 1 union ledgers from immutable inputs + reviewer decisions.

Usage:
  python build_candidate.py M            # draft build (tolerates unreviewed regions)
  python build_candidate.py M --final    # requires every multi-run region reviewed and
                                         # every Codex finding normalized (CX or SPLIT)

Writes only to stage_A/reconciled/step1_union/per_candidate/<C>/.
Hard errors (inconsistent decisions, bad refs, anchors outside quotes, ED that is not
mechanically exact, relation inside one group, ...) abort the build with exit code 2.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys

from model import Candidate
from review_view import regions as compute_regions
from union_lib import (OUT, write_jsonl, harmless_norm, clause_id, group_id, sha256_text,
                       occurrence_id, exact_excerpt, quote_match)

RUN_ORDER = {"PRIMARY": 0, "REPLICA": 1, "CODEX": 2}
RD_SUBTYPES = {"BROADER_NARROWER", "COMPOUND_PART", "EXAMPLE_GENERAL", "OVERLAP", "DIFFERENT_SCOPE",
               "DIFFERENT_STRENGTH", "DIFFERENT_LAYER", "DETAIL_DIFFERENCE"}
REF_RE = re.compile(r"^([PRX]):([A-Za-z0-9][A-Za-z0-9\-]*)(?:#([a-z]{1,3}))?(?:@(\d+)(?:-(\d+))?)?$")
REG_RE = re.compile(r"^r(\d+)(?:-r?(\d+))?$")


class BuildError(Exception):
    pass


def parse_ref(tok):
    m = REF_RE.match(tok)
    if not m:
        raise BuildError(f"bad ref {tok!r}")
    letter, oid, part, s, e = m.groups()
    anchor = None
    if s:
        anchor = (int(s), int(e) if e else int(s))
    return letter, oid, part, anchor


def load_decisions(cand):
    d = OUT / "_review" / cand
    out = []
    if not d.exists():
        return out, {}
    hashes = {}
    for f in sorted(d.glob("*.dec")):
        txt = f.read_text(encoding="utf-8")
        hashes[f.name] = sha256_text(txt)
        for i, line in enumerate(txt.split("\n"), 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.append((f"{f.name}:{i}", s))
    return out, hashes


def build(cand, final=False):
    cm = Candidate(cand)
    errors = []
    decisions, dec_hashes = load_decisions(cand)

    def rec_of(letter, oid, src):
        k = cm.resolve_ref(f"{letter}:{oid}")
        if k is None:
            raise BuildError(f"{src}: unknown record {letter}:{oid}")
        return k

    # ---------------------------------------------------------- pass 1: units
    units = {}              # unit_id -> dict
    split_of = collections.defaultdict(list)
    cx = {}
    for k in cm.claim_keys():
        units[k] = {"unit_id": k, "record_key": k, "part": None, "reviewer_text": None,
                    "anchor": None, "quote_note": None, "decl_src": None}
    parsed = []
    for src, line in decisions:
        op, _, rest = line.partition(" ")
        op = op.strip()
        rest = rest.strip()
        parsed.append((src, op, rest))
        try:
            if op == "SPLIT":
                fields = [x.strip() for x in rest.split("|")]
                letter, oid, part, anchor = parse_ref(fields[0])
                if part or anchor:
                    raise BuildError(f"{src}: SPLIT target must be a bare record")
                k = rec_of(letter, oid, src)
                if k in split_of:
                    raise BuildError(f"{src}: record split twice")
                if len(fields) < 3:
                    raise BuildError(f"{src}: SPLIT needs >= 2 parts")
                for fpart in fields[1:]:
                    m = re.match(r"^([a-z]{1,3})(?:@(\d+)(?:-(\d+))?)?\s*:\s*(.+)$", fpart)
                    if not m:
                        raise BuildError(f"{src}: bad SPLIT part {fpart!r}")
                    p, s, e, text = m.groups()
                    anc = (int(s), int(e) if e else int(s)) if s else None
                    if anc and cm.records[k]["record_type"] != "BLIND_FINDING":
                        raise BuildError(f"{src}: @anchor only allowed for Codex parts")
                    uid = f"{k}#{p}"
                    if uid in units:
                        raise BuildError(f"{src}: duplicate part {uid}")
                    units[uid] = {"unit_id": uid, "record_key": k, "part": p, "reviewer_text": text.strip(),
                                  "anchor": anc, "quote_note": None, "decl_src": src}
                    split_of[k].append(uid)
                units.pop(k, None)
            elif op == "CX":
                fields = [x.strip() for x in rest.split("|")]
                letter, oid, part, anchor = parse_ref(fields[0])
                if letter != "X" or part:
                    raise BuildError(f"{src}: CX applies to an unsplit Codex finding")
                k = rec_of(letter, oid, src)
                if k in cx:
                    raise BuildError(f"{src}: CX given twice for {k} (first {cx[k]})")
                if len(fields) < 2 or not fields[1]:
                    raise BuildError(f"{src}: CX needs claim text")
                cx[k] = src
                units[k]["reviewer_text"] = fields[1]
                units[k]["anchor"] = anchor
                units[k]["quote_note"] = fields[2] if len(fields) > 2 and fields[2] else None
                units[k]["decl_src"] = src
        except BuildError as ex:
            errors.append(str(ex))
    for k in cx:
        if k in split_of:
            errors.append(f"{k}: both CX ({cx[k]}) and SPLIT given")
    # validate codex anchors
    for u in units.values():
        r = cm.records[u["record_key"]]
        if u["anchor"]:
            o = r["raw_record"]
            s, e = u["anchor"]
            if not (o["start_line"] <= s <= e <= o["end_line"]):
                errors.append(f"{u['decl_src']}: anchor {s}-{e} outside quote range {o['start_line']}-{o['end_line']} of {u['unit_id']}")

    def resolve_units(tok, src, allow_whole):
        letter, oid, part, anchor = parse_ref(tok)
        if anchor:
            raise BuildError(f"{src}: anchors only allowed in CX/SPLIT ({tok})")
        k = rec_of(letter, oid, src)
        if part:
            uid = f"{k}#{part}"
            if uid not in units:
                raise BuildError(f"{src}: undeclared part {tok}")
            return [uid]
        if k in split_of:
            if not allow_whole:
                raise BuildError(f"{src}: {tok} is split; name a part")
            return list(split_of[k])
        return [k]

    # ---------------------------------------------------------- pass 2: edges
    parent = {u: u for u in units}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    merges = []           # decision dicts
    relations = []
    reviewed = set()
    for src, op, rest in parsed:
        try:
            if op in ("SPLIT", "CX"):
                continue
            if op == "REVIEWED":
                for tok in rest.split():
                    m = REG_RE.match(tok)
                    if not m:
                        raise BuildError(f"{src}: bad region token {tok}")
                    a = int(m.group(1))
                    b = int(m.group(2)) if m.group(2) else a
                    reviewed.update(range(a, b + 1))
                continue
            if op in ("SD", "ED"):
                fields = [x.strip() for x in rest.split("|")]
                toks = fields[0].split()
                if len(toks) < 2:
                    raise BuildError(f"{src}: {op} needs >= 2 refs")
                us = []
                for t in toks:
                    us += resolve_units(t, src, allow_whole=False)
                if len(set(us)) != len(us):
                    raise BuildError(f"{src}: repeated unit in {op}")
                rationale = " | ".join(fields[1:]).strip()
                if op == "SD":
                    for tag in ("S:", "M:", "E:", "T:"):
                        if tag not in rationale:
                            raise BuildError(f"{src}: SD rationale lacks {tag} check")
                if op == "ED":
                    sig = set()
                    for u in us:
                        r = cm.records[units[u]["record_key"]]
                        if r["record_type"] != "CONSTRAINT" or units[u]["part"]:
                            raise BuildError(f"{src}: ED only for whole Claude constraints")
                        o = r["raw_record"]
                        sig.add(tuple(harmless_norm(str(o.get(f))) for f in
                                      ("normative_action", "modality", "trigger_scope", "exceptions")))
                    if len(sig) != 1:
                        raise BuildError(f"{src}: ED members are not identical after harmless normalization")
                did = f"MD-{cand}-{sha256_text(src + op + rest)[:8]}"
                merges.append({"decision_id": did, "type": "EXACT_DUPLICATE" if op == "ED" else "SEMANTIC_DUPLICATE",
                               "claim_unit_ids": us, "rationale": rationale, "decision_src": f"_review/{cand}/{src}"})
                for u in us[1:]:
                    parent[find(u)] = find(us[0])
                continue
            if op in ("RD", "AC", "UR", "NE"):
                fields = [x.strip() for x in rest.split("|")]
                toks = fields[0].split()
                sub = None
                if op == "RD":
                    sub = toks[0]
                    if sub not in RD_SUBTYPES:
                        raise BuildError(f"{src}: unknown RD subtype {sub}")
                    toks = toks[1:]
                need = 1 if op == "NE" else 2
                if len(toks) != need:
                    raise BuildError(f"{src}: {op} needs exactly {need} ref(s)")
                note = " | ".join(fields[1:]).strip()
                if not note:
                    raise BuildError(f"{src}: {op} needs a note / open question")
                sides = [resolve_units(t, src, allow_whole=True) for t in toks]
                rel = {"APPARENT_CONFLICT" if op == "AC" else "UNRESOLVED" if op == "UR" else
                       "NEEDS_EVIDENCE" if op == "NE" else "RELATED_BUT_DISTINCT": None}
                relations.append({"op": op, "relation": list(rel)[0], "subtype": sub, "sides": sides,
                                  "refs": toks, "note": note, "decision_src": f"_review/{cand}/{src}"})
                continue
            raise BuildError(f"{src}: unknown directive {op}")
        except BuildError as ex:
            errors.append(str(ex))

    # ---------------------------------------------------------- groups
    def unit_sort(u):
        r = cm.records[units[u]["record_key"]]
        return (RUN_ORDER[r["run"]], r["original_id"], units[u]["part"] or "")

    comps = collections.defaultdict(list)
    for u in units:
        comps[find(u)].append(u)
    unit_group = {}
    groups = {}
    for root, mem in comps.items():
        mem.sort(key=unit_sort)
        gid = group_id(cand, mem[0])
        if gid in groups:
            errors.append(f"group id collision {gid}")
        groups[gid] = {"members": mem}
        for u in mem:
            unit_group[u] = gid
    # split parts of one record must not land in one group
    for k, parts in split_of.items():
        gs = [unit_group[p] for p in parts]
        if len(set(gs)) != len(gs):
            errors.append(f"{k}: two split parts merged into one group")
    # relations inside one group are contradictions
    for rel in relations:
        if rel["op"] == "NE":
            continue
        for a in rel["sides"][0]:
            for b in rel["sides"][1]:
                if unit_group[a] == unit_group[b]:
                    errors.append(f"{rel['decision_src']}: {rel['relation']} between units of one group ({a}, {b})")

    # ---------------------------------------------------------- regions
    regs = [g for g in compute_regions(cm) if g["multi_run"]]
    unit_regions = collections.defaultdict(set)
    rec_units = collections.defaultdict(list)
    for u in units:
        rec_units[units[u]["record_key"]].append(u)
    for i, g in enumerate(regs, 1):
        for _, _, k in g["items"]:
            for u in rec_units[k]:
                unit_regions[u].add(i)
    unreviewed = [i for i in range(1, len(regs) + 1) if i not in reviewed]
    extra_rev = sorted(i for i in reviewed if i > len(regs))
    if extra_rev:
        errors.append(f"REVIEWED names regions beyond {len(regs)}: {extra_rev[:5]}")
    if final:
        if unreviewed:
            errors.append(f"final build: {len(unreviewed)} multi-run regions not reviewed, e.g. {unreviewed[:10]}")
        missing_cx = [k for k in cm.claim_keys() if cm.records[k]["record_type"] == "BLIND_FINDING"
                      and k not in cx and k not in split_of]
        if missing_cx:
            errors.append(f"final build: {len(missing_cx)} Codex findings without CX/SPLIT, e.g. {missing_cx[:5]}")

    if errors:
        raise BuildError("\n".join(errors))

    # ---------------------------------------------------------- clauses
    issues = [dict(i) for i in cm.issues]
    clauses = []
    unit_clauses = collections.defaultdict(list)
    narrowed_occ = {}
    for u in sorted(units, key=unit_sort):
        info = units[u]
        r = cm.records[info["record_key"]]
        o = r["raw_record"]
        if r["record_type"] == "CONSTRAINT":
            reported = {"modality": o.get("modality"), "trigger_scope": o.get("trigger_scope"),
                        "exceptions": o.get("exceptions")}
            if info["part"]:
                action, asrc = info["reviewer_text"], "REVIEWER_SPLIT_PART_PARAPHRASE (attributed to the source record; not a verdict)"
            else:
                action, asrc = o.get("normative_action"), "REPORTED normative_action (verbatim)"
            entries = cm.rec_occ[info["record_key"]]
            anchors = [(e, e.get("occurrence_id"), "EVIDENCE_SEGMENT") for e in entries]
        else:
            reported = {"modality": "UNKNOWN_NOT_REPORTED", "trigger_scope": "UNKNOWN_NOT_REPORTED",
                        "exceptions": "UNKNOWN_NOT_REPORTED"}
            action = info["reviewer_text"] or o.get("explanation")
            asrc = ("REVIEWER_PARAPHRASE of Codex explanation/scenario (attributed; not a verdict)"
                    if info["reviewer_text"] else "REPORTED explanation (verbatim)")
            e0 = cm.rec_occ[info["record_key"]][0]
            if info["anchor"] and info["anchor"] != (o["start_line"], o["end_line"]):
                s, e = info["anchor"]
                oid = cm._add_occ(o["path"], s, e)
                occ = cm.occ[oid]
                cit = {"record_key": info["record_key"], "via": f"reviewer-narrowed anchor inside Codex quote ({info['decl_src']})",
                       "quote_match": "N/A_NARROWED"}
                if cit not in occ["citations"]:
                    occ["citations"].append(cit)
                anchors = [({"segment_id": None, "reported_quote": o.get("quote"),
                             "quote_match": e0["quote_match"], "original_occurrence_id": e0["occurrence_id"]},
                            oid, "NARROWED_BY_REVIEWER_WITHIN_CODEX_QUOTE")]
            else:
                anchors = [(e0, e0["occurrence_id"], "FULL_CODEX_QUOTE_RANGE")]
        for ent, oid, basis in anchors:
            occ = cm.occ.get(oid) if oid else None
            if occ is None:
                cl = {"clause_id": f"CL-{cand}-UNRESOLVED-{sha256_text(u + str(ent.get('segment_id')))[:6]}",
                      "location_status": "SOURCE_UNVERIFIED", "path": None, "start_line": None, "end_line": None,
                      "exact_excerpt": None, "excerpt_sha256": None, "occurrence_id": None}
            else:
                cl = {"clause_id": clause_id(cand, occ["path"], occ["start_line"], occ["end_line"], occ["excerpt_sha256"], u),
                      "occurrence_id": oid, "path": occ["path"], "start_line": occ["start_line"], "end_line": occ["end_line"],
                      "exact_excerpt": occ["exact_excerpt"], "excerpt_sha256": occ["excerpt_sha256"],
                      "location_status": "VERIFIED_RANGE" if occ["location_status"] == "VERIFIED_RANGE" else "SOURCE_UNVERIFIED"}
            qm = ent.get("quote_match")
            if cl["location_status"] == "VERIFIED_RANGE" and qm in ("MISMATCH", "SOURCE_UNVERIFIED"):
                cl["location_status"] = "SOURCE_UNVERIFIED"
            cl.update({
                "candidate": cand, "claim_unit_id": u, "record_key": info["record_key"], "run": r["run"],
                "part": info["part"], "group_id": unit_group[u], "anchor_basis": basis,
                "evidence_segment_id": ent.get("segment_id"), "evidence_segment_ordinal": ent.get("segment_ordinal"),
                "evidence_segment_disposition": ent.get("segment_disposition"),
                "original_occurrence_id": ent.get("original_occurrence_id"),
                "reported_quote": ent.get("reported_quote"), "reported_quote_match": qm,
                "normalized_claimed_action": action, "normalized_claimed_action_source": asrc,
                "reported_modality": reported["modality"], "reported_trigger_scope": reported["trigger_scope"],
                "reported_exceptions": reported["exceptions"],
                "reported_label": r["original_label"], "reported_label_field": r["original_label_field"],
                "reported_policy_ids": o.get("policy_ids") if r["record_type"] == "CONSTRAINT" else o.get("closest_policy_ids"),
                "quote_note": info["quote_note"],
                "part_location_note": ("split part inherits every evidence occurrence of its record; no part-to-location mapping asserted"
                                       if info["part"] and r["record_type"] == "CONSTRAINT" else None),
            })
            clauses.append(cl)
            unit_clauses[u].append(cl["clause_id"])
    ids = [c["clause_id"] for c in clauses]
    dup = [x for x, n in collections.Counter(ids).items() if n > 1]
    if dup:
        # identical (unit, occurrence) twice = a record citing two segments with identical line ranges
        seen = set()
        uniq = []
        for c in clauses:
            if c["clause_id"] in seen:
                for x in uniq:
                    if x["clause_id"] == c["clause_id"]:
                        x.setdefault("additional_evidence_segment_ids", []).append(c["evidence_segment_id"])
                continue
            seen.add(c["clause_id"])
            uniq.append(c)
        clauses = uniq
        for u in unit_clauses:
            unit_clauses[u] = list(dict.fromkeys(unit_clauses[u]))

    # ---------------------------------------------------------- groups out
    rel_by_group = collections.defaultdict(list)
    queue = []
    for rel in relations:
        ga = sorted({unit_group[u] for u in rel["sides"][0]})
        gb = sorted({unit_group[u] for u in rel["sides"][1]}) if len(rel["sides"]) > 1 else []
        qid = f"RQ-{cand}-{sha256_text(rel['decision_src'] + rel['note'])[:10]}"
        all_units = rel["sides"][0] + (rel["sides"][1] if len(rel["sides"]) > 1 else [])
        recs = list(dict.fromkeys(units[u]["record_key"] for u in all_units))
        queue.append({
            "queue_id": qid, "candidate": cand, "item_type": rel["relation"], "subtype": rel["subtype"],
            "claim_unit_ids_a": rel["sides"][0], "claim_unit_ids_b": rel["sides"][1] if len(rel["sides"]) > 1 else [],
            "group_ids_a": ga, "group_ids_b": gb, "record_keys": recs,
            "sources": [{"record_key": k, "locations": [{"path": p, "start_line": s, "end_line": e} for (p, s, e) in cm.locs(k)]} for k in recs],
            "open_question": rel["note"], "decision_src": rel["decision_src"],
            "status": "OPEN_FOR_STEP2",
        })
        for g in ga:
            for h in gb:
                rel_by_group[g].append({"relation": rel["relation"], "subtype": rel["subtype"], "role": "a", "other_group_id": h, "queue_id": qid})
                rel_by_group[h].append({"relation": rel["relation"], "subtype": rel["subtype"], "role": "b", "other_group_id": g, "queue_id": qid})
        if rel["op"] == "NE":
            for g in ga:
                rel_by_group[g].append({"relation": "NEEDS_EVIDENCE", "subtype": None, "role": "self", "other_group_id": None, "queue_id": qid})

    merges_by_group = collections.defaultdict(list)
    for m in merges:
        merges_by_group[unit_group[m["claim_unit_ids"][0]]].append(m)

    clause_by_id = {c["clause_id"]: c for c in clauses}
    findings = []
    for gid in sorted(groups, key=lambda g: unit_sort(groups[g]["members"][0])):
        mem = groups[gid]["members"]
        seed = mem[0]
        sinfo = units[seed]
        srec = cm.records[sinfo["record_key"]]
        if srec["record_type"] == "CONSTRAINT" and not sinfo["part"]:
            ntext = srec["raw_record"]["normative_action"]
            nsrc = f"{srec['record_key']} normative_action (verbatim, attributed)"
        elif sinfo["reviewer_text"]:
            ntext = sinfo["reviewer_text"]
            nsrc = f"{seed} reviewer paraphrase ({sinfo['decl_src']}; attributed, not a verdict)"
        else:
            ntext = srec["raw_record"].get("explanation")
            nsrc = f"{srec['record_key']} explanation (verbatim, attributed)"
        recs = list(dict.fromkeys(units[u]["record_key"] for u in mem))
        labels = []
        pol = {}
        for k in recs:
            r = cm.records[k]
            o = r["raw_record"]
            if r["record_type"] == "CONSTRAINT":
                labels.append({"record_key": k, "run": r["run"], "label_field": "origin", "reported_label": o["origin"],
                               "reported_policy_ids": o["policy_ids"], "reported_modality": o["modality"]})
                pol[k] = o["policy_ids"]
            else:
                labels.append({"record_key": k, "run": r["run"], "label_field": "classification",
                               "reported_label": o["classification"], "reported_policy_ids": o["closest_policy_ids"],
                               "reported_confidence": o["confidence"], "reported_assessment_status": o["assessment_status"]})
                pol[k] = o["closest_policy_ids"]
        runs = sorted({cm.records[k]["run"] for k in recs}, key=RUN_ORDER.get)
        cids = [c for u in mem for c in unit_clauses[u]]
        mtypes = sorted({m["type"] for m in merges_by_group[gid]})
        mtype = "SINGLETON" if len(mem) == 1 else ("+".join(mtypes) if mtypes else "UNKNOWN")
        regs_seen = sorted({i for u in mem for i in unit_regions[u]})
        lab_set = {(l["reported_label"]) for l in labels}
        pol_set = {tuple(sorted(v)) for v in pol.values()}
        vstat = "ALL_LOCATIONS_VERIFIED"
        if any(clause_by_id[c]["location_status"] != "VERIFIED_RANGE" for c in cids):
            vstat = "HAS_SOURCE_UNVERIFIED_LOCATION"
        f = {
            "group_id": gid, "candidate": cand, "seed_claim_unit_id": seed,
            "neutral_claim_text": ntext, "neutral_claim_text_source": nsrc,
            "claim_unit_ids": mem, "clause_ids": cids, "source_record_keys": recs,
            "supporting_runs": runs, "n_records_by_run": dict(collections.Counter(cm.records[k]["run"] for k in recs)),
            "original_labels": labels, "original_claimed_policy_ids": pol,
            "occurrence_ids": sorted({clause_by_id[c]["occurrence_id"] for c in cids if clause_by_id[c]["occurrence_id"]}),
            "merge_type": mtype, "merge_decisions": merges_by_group[gid],
            "singleton_basis": ((("REVIEWED_NO_DUPLICATE_FOUND" if all(i in reviewed for i in regs_seen) else "PENDING_REGION_REVIEW")
                                 if regs_seen else "NO_CO_LOCATED_RECORD_FROM_OTHER_RUN")
                                if len(mem) == 1 else None),
            "review_region_ids": [f"CR-{cand}-r{i:03d}" for i in regs_seen],
            "merge_review_relations": rel_by_group.get(gid, []),
            "attribution_disagreement": len(mem) > 1 and (len(lab_set) > 1 or len(pol_set) > 1),
            "source_verification_status": vstat,
            "status_note": "Step 1 grouping only; labels are attributed claims, not validated categories.",
        }
        findings.append(f)
        if f["attribution_disagreement"]:
            queue.append({
                "queue_id": f"RQ-{cand}-{sha256_text('ATTR' + gid)[:10]}", "candidate": cand,
                "item_type": "ATTRIBUTION_DISAGREEMENT", "subtype": ("LABEL" if len(lab_set) > 1 else "") + ("+POLICY_IDS" if len(pol_set) > 1 else ""),
                "claim_unit_ids_a": mem, "claim_unit_ids_b": [], "group_ids_a": [gid], "group_ids_b": [],
                "record_keys": recs,
                "sources": [{"record_key": k, "locations": [{"path": p, "start_line": s, "end_line": e} for (p, s, e) in cm.locs(k)]} for k in recs],
                "open_question": "Members of this merged group carry different original labels and/or claimed policy IDs: "
                                 + "; ".join(f"{l['record_key']}={l['reported_label']} {l['reported_policy_ids']}" for l in labels)
                                 + ". Step 2 must adjudicate; Step 1 preserves all attributions.",
                "decision_src": "MECHANICAL", "status": "OPEN_FOR_STEP2",
            })

    # ---------------------------------------------------------- accounting
    rec_groups = collections.defaultdict(list)
    rec_clauses = collections.defaultdict(list)
    for u in units:
        k = units[u]["record_key"]
        rec_groups[k].append(unit_group[u])
        rec_clauses[k] += unit_clauses[u]
    occ_groups = collections.defaultdict(set)
    for c in clauses:
        if c["path"]:
            occ_groups[c["path"]].add((c["start_line"], c["end_line"], c["group_id"]))
    acct = []
    for k in cm.order:
        r = cm.records[k]
        o = r["raw_record"]
        row = {"record_key": k, "run": r["run"], "candidate": cand, "record_type": r["record_type"],
               "original_id": r["original_id"], "original_label": r["original_label"],
               "input_file": r["input_file"], "ordinal": r["ordinal"], "raw_sha256": r["raw_sha256"]}
        if r["record_type"] in ("CONSTRAINT", "BLIND_FINDING"):
            gs = list(dict.fromkeys(rec_groups[k]))
            row.update({"disposition": "LINKED_TO_FINDING" if gs else "UNRESOLVED", "group_ids": gs,
                        "clause_ids": rec_clauses[k], "claim_unit_ids": rec_units[k],
                        "note": "split into parts" if k in split_of else ""})
        elif r["record_type"] == "POLICY":
            gs, unres = [], []
            for cid in o.get("atomic_constraint_ids") or []:
                ck = cm.by_run_id.get((r["run"], "CONSTRAINT", cid))
                if ck is None:
                    unres.append(cid)
                else:
                    gs += rec_groups[ck]
            row.update({"disposition": "POLICY_CROSS_REFERENCE", "group_ids": list(dict.fromkeys(gs)), "clause_ids": [],
                        "unresolved_constraint_ids": unres,
                        "note": "cross-reference only; adds no rule and no support count"})
            if unres:
                issues.append({"type": "POLICY_CONSTRAINT_ID_UNRESOLVED", "record_key": k, "detail": f"{unres}"})
        else:  # ORPHAN
            gs, unres = [], []
            for cid in o.get("constraint_ids") or []:
                ck = cm.by_run_id.get((r["run"], "CONSTRAINT", cid))
                if ck is None:
                    unres.append(cid)
                else:
                    gs += rec_groups[ck]
            co = []
            if o.get("path") in occ_groups and isinstance(o.get("start_line"), int):
                co = sorted({g for (s, e, g) in occ_groups[o["path"]] if s <= o["end_line"] and o["start_line"] <= e})
            if gs:
                disp = "ORPHAN_CONTEXT_LINKED"
            else:
                disp = "ORPHAN_PENDING_REVIEW"
            row.update({"disposition": disp, "group_ids": list(dict.fromkeys(gs)), "clause_ids": [],
                        "unresolved_constraint_ids": unres, "co_located_group_ids": co,
                        "original_resolution": o.get("resolution"),
                        "note": ("orphan passage linked to its registered constraint(s); not an additional rule"
                                 if gs else "no linked constraint; retained for Step 2 re-examination; not a rule")})
            if unres:
                issues.append({"type": "ORPHAN_CONSTRAINT_ID_UNRESOLVED", "record_key": k, "detail": f"{unres}"})
        acct.append(row)

    # ---------------------------------------------------------- index, occurrences, co-location
    index = []
    for k in cm.order:
        r = cm.records[k]
        index.append({"record_key": k, "run": r["run"], "candidate": cand, "record_type": r["record_type"],
                      "original_id": r["original_id"], "original_label_field": r["original_label_field"],
                      "original_label": r["original_label"], "input_file": r["input_file"], "ordinal": r["ordinal"],
                      "raw_sha256": r["raw_sha256"], "raw_record": r["raw_record"],
                      "resolved_evidence": cm.rec_occ.get(k, [])})
    occs = sorted(cm.occ.values(), key=lambda o: (o["path"], o["start_line"], o["end_line"]))
    coloc = []
    for i, g in enumerate(regs, 1):
        us = sorted({u for _, _, k in g["items"] for u in rec_units[k]}, key=unit_sort)
        coloc.append({"region_id": f"CR-{cand}-r{i:03d}", "candidate": cand, "path": g["path"],
                      "start_line": g["lo"], "end_line": g["hi"], "claim_unit_ids": us,
                      "group_ids": sorted({unit_group[u] for u in us}),
                      "runs": sorted({cm.records[units[u]["record_key"]]["run"] for u in us}, key=RUN_ORDER.get),
                      "reviewed": i in reviewed,
                      "meaning": "co-location proposes merge candidates only; pairs without a recorded relation were reviewed and not merged" if i in reviewed else "NOT YET REVIEWED"})
    for n, it in enumerate(issues):
        it.setdefault("severity", "ERROR" if it["type"] in ("QUOTE_MISMATCH", "SOURCE_UNVERIFIED", "SEGMENT_UNRESOLVED", "NO_EVIDENCE_SEGMENTS") else "WARNING")
        it["candidate"] = cand
        it["issue_id"] = f"SV-{cand}-{sha256_text(json.dumps(it, sort_keys=True))[:10]}"

    decs = [{"decision_id": m["decision_id"], "candidate": cand, **{k: v for k, v in m.items() if k != "decision_id"}} for m in merges]
    for rel in relations:
        decs.append({"decision_id": f"RL-{cand}-{sha256_text(rel['decision_src'])[:8]}", "candidate": cand, "type": rel["relation"],
                     "subtype": rel["subtype"], "claim_unit_ids_a": rel["sides"][0],
                     "claim_unit_ids_b": rel["sides"][1] if len(rel["sides"]) > 1 else [], "note": rel["note"],
                     "decision_src": rel["decision_src"]})
    for u, info in units.items():
        if info["decl_src"]:
            decs.append({"decision_id": f"NM-{cand}-{sha256_text(u)[:8]}", "candidate": cand,
                         "type": "SPLIT_PART" if info["part"] else "CODEX_NORMALIZATION", "claim_unit_ids": [u],
                         "reviewer_text": info["reviewer_text"], "anchor": list(info["anchor"]) if info["anchor"] else None,
                         "quote_note": info["quote_note"], "decision_src": f"_review/{cand}/{info['decl_src']}"})

    od = OUT / "per_candidate" / cand
    write_jsonl(od / "SOURCE_RECORD_INDEX.jsonl", index)
    write_jsonl(od / "SOURCE_OCCURRENCES.jsonl", occs)
    write_jsonl(od / "SOURCE_CLAUSES.jsonl", clauses)
    write_jsonl(od / "MERGED_FINDINGS.jsonl", findings)
    write_jsonl(od / "RECORD_ACCOUNTING.jsonl", acct)
    write_jsonl(od / "MERGE_REVIEW_QUEUE.jsonl", sorted(queue, key=lambda q: q["queue_id"]))
    write_jsonl(od / "SOURCE_VERIFICATION_ISSUES.jsonl", issues)
    write_jsonl(od / "MERGE_DECISIONS.jsonl", decs)
    write_jsonl(od / "CO_LOCATION_INDEX.jsonl", coloc)

    cnt = collections.Counter()
    for r in index:
        cnt[f"{r['run']}/{r['record_type']}"] += 1
    summ = {
        "candidate": cand, "final": final, "input_records": dict(cnt), "input_records_total": len(index),
        "claim_units": len(units), "split_records": len(split_of), "clauses": len(clauses), "occurrences": len(occs),
        "groups": len(findings),
        "groups_by_merge_type": dict(collections.Counter(f["merge_type"] for f in findings)),
        "groups_by_supporting_runs": dict(collections.Counter("+".join(f["supporting_runs"]) for f in findings)),
        "singleton_basis": dict(collections.Counter(f["singleton_basis"] for f in findings if f["singleton_basis"])),
        "merge_decisions": dict(collections.Counter(m["type"] for m in merges)),
        "relations": dict(collections.Counter(r["relation"] + (":" + r["subtype"] if r["subtype"] else "") for r in relations)),
        "review_queue_items": dict(collections.Counter(q["item_type"] for q in queue)),
        "source_verification_issues": dict(collections.Counter(f"{i['severity']}:{i['type']}" for i in issues)),
        "accounting_dispositions": dict(collections.Counter(f"{a['record_type']}:{a['disposition']}" for a in acct)),
        "regions_multi_run": len(regs), "regions_reviewed": len([i for i in range(1, len(regs) + 1) if i in reviewed]),
        "codex_normalized": len([k for k in cm.claim_keys() if cm.records[k]["record_type"] == "BLIND_FINDING" and (k in cx or k in split_of)]),
        "codex_total": len([k for k in cm.claim_keys() if cm.records[k]["record_type"] == "BLIND_FINDING"]),
        "decision_file_sha256": dec_hashes,
    }
    (od / "BUILD_SUMMARY.json").write_text(json.dumps(summ, indent=2, sort_keys=True), encoding="utf-8")
    return summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cand")
    ap.add_argument("--final", action="store_true")
    a = ap.parse_args()
    try:
        s = build(a.cand, a.final)
    except BuildError as ex:
        print("BUILD ERROR:\n" + str(ex))
        return 2
    print(json.dumps({k: v for k, v in s.items() if k != "decision_file_sha256"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
