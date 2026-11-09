"""Build per-batch reading dossiers for the six-way policy comparison.

A dossier is a reading aid: it shows, for one policy, the canonical text and, for each
candidate, the v3 source lines (read from candidates/<C>/template at the current anchors)
of every record Step 2 v3 links to the cell. It writes only under _dossiers/.

Usage:
  python -B _tools/dossier.py plan            # write BATCH_PLAN.json
  python -B _tools/dossier.py build <BATCH>   # write _dossiers/<BATCH>.md and .json
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reach import RANK, ENFORCING, reach_class  # noqa: E402
from s3common import (CANDS, RECON, S3, V3, canonical_policies, cand_lines, read_json, read_jsonl,  # noqa: E402
                      write_json_atomic, write_text_atomic)

BATCH_SIZE = 8
STRENGTH_ORDER = {"WEAKER": 0, "STRONGER": 0, "INCOMPARABLE": 0, "SAME": 1, "N/A": 2}


def plan():
    pols = canonical_policies()
    groups = []
    for p in pols:
        if not groups or groups[-1][0] != p["group"]:
            groups.append((p["group"], []))
        groups[-1][1].append(p["id"])
    batches = []
    for g, ids in groups:
        n = (len(ids) + BATCH_SIZE - 1) // BATCH_SIZE
        size = (len(ids) + n - 1) // n
        for i in range(n):
            chunk = ids[i * size:(i + 1) * size]
            if chunk:
                batches.append({"batch": f"B{len(batches) + 1:02d}", "group": g, "policies": chunk})
    out = {"batch_size_max": BATCH_SIZE, "n_batches": len(batches), "n_policies": sum(len(b["policies"]) for b in batches),
           "batches": batches}
    assert out["n_policies"] == 196
    write_json_atomic(S3 / "BATCH_PLAN.json", out)
    print(out["n_batches"], "batches")


_cache = {}


def load():
    if _cache:
        return _cache
    _cache["pol"] = {p["id"]: p for p in canonical_policies()}
    _cache["rec"] = {r["source_key"]: r for r in read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl")}
    _cache["cov"] = {(r["candidate"], r["policy_id"]): r for r in read_jsonl(V3 / "REPAIRED_POLICY_COVERAGE.jsonl")}
    _cache["pm"] = {(r["candidate"], r["policy_id"]): r for r in read_jsonl(V3 / "POLICY_PARITY_MATRIX.jsonl")}
    man = read_json(V3 / "V3_FINAL_MANIFEST.json")
    _cache["man"] = {(c, p): v for c in CANDS for p, v in man["candidates"][c]["files"].items()}
    div = defaultdict(list)
    for c in CANDS:
        for r in read_jsonl(RECON / "step2_classification" / "per_candidate" / c / "STRENGTH_DIVERGENCES.jsonl"):
            for ln in r.get("links", []):
                div[(c, ln["policy_id"])].append((r["source_key"], r.get("normative_strength_equivalence")))
    _cache["div"] = div
    pw = {}
    for r in read_jsonl(V3 / "PARTIAL_WITNESSES_38.jsonl"):
        pw[(r["candidate"], r["policy_id"])] = r
    _cache["pw"] = pw
    _cache["xw"] = {r["source_key"]: r["status"] for r in read_jsonl(V3 / "V2_TO_V3_CROSSWALK.jsonl")}
    return _cache


def norm_ws(s):
    return re.sub(r"\s+", " ", s or "").strip()


def anchor_of(rec, cov_row):
    """Current v3 anchor for a record: the coverage witness line when present, else the first current ref."""
    w = None
    for x in cov_row.get("witnesses", []):
        if x["source_key"] == rec["source_key"]:
            w = x
            break
    refs = rec.get("current_evidence_refs") or []
    if w:
        for e in refs:
            if e["path"] == w["path"] and e["start_line"] == w["start_line"]:
                return e["path"], e["start_line"], e["end_line"]
        return w["path"], w["start_line"], w["start_line"]
    if refs:
        e = refs[0]
        return e["path"], e["start_line"], e["end_line"]
    return None, None, None


def text_at(path, s, e):
    try:
        lines = cand_lines(path)
    except FileNotFoundError:
        return None
    if s is None or s < 1 or e > len(lines):
        return None
    return norm_ws(" ".join(lines[s - 1:e]))


def trim(s, n):
    s = s or ""
    return s if len(s) <= n else s[:n] + " …"


def cell_data(c, pid):
    d = load()
    cov = d["cov"][(c, pid)]
    pm = d["pm"][(c, pid)]
    direct = list(cov["direct_source_keys"])
    partial = [k for k in cov["partial_source_keys"] if k not in direct]
    extra = [k for k in (cov.get("stronger_source_keys", []) + cov.get("weaker_source_keys", [])
                         + cov.get("uncertain_source_keys", [])) if k not in direct and k not in partial]
    owners = []
    for role, keys in (("D", direct), ("P", partial), ("X", extra)):
        for k in keys:
            r = d["rec"][k]
            path, s, e = anchor_of(r, cov)
            txt = text_at(path, s, e) if path else None
            rc = reach_class(r["delivery_context"])
            fm = d["man"].get((c, path.split("/template/", 1)[1])) if path else None
            owners.append({
                "key": k, "role": role, "modality": r["modality"], "svc": r.get("strength_vs_canonical"),
                "classification": r["classification"], "reach": rc, "delivery": r["delivery_context"],
                "path": path, "start": s, "end": e, "text": txt, "active": r["repair"]["active"],
                "repair_status": r["repair"]["status"], "rules": r["repair"].get("rules", []),
                "changed_vs_frozen": bool(fm and fm["changed_vs_frozen"]), "changed_vs_v2": bool(fm and fm["changed_vs_v2"]),
                "exceptions": r.get("exceptions"), "exc_status": r.get("exceptions_status"),
                "trigger": r.get("trigger"), "trig_status": r.get("trigger_status"),
                "app_override": r.get("applicability_override"), "comparison_qualifier": r.get("comparison_qualifier"),
                "extra_fragment": r.get("extra_fragment"), "v2v3": d["xw"].get(k),
            })
    owners.sort(key=lambda o: (o["role"] != "D", STRENGTH_ORDER.get(o["svc"], 3) if o["role"] == "D" else 0,
                               RANK.get(o["reach"], 9)))
    # put the best-reach SAME direct owner first
    best = [o for o in owners if o["role"] == "D" and o["svc"] == "SAME"]
    if best:
        b = min(best, key=lambda o: RANK.get(o["reach"], 9))
        owners.remove(b)
        owners.insert(0, b)
    reaches = sorted({o["reach"] for o in owners if o["role"] == "D"}, key=lambda x: RANK.get(x, 9))
    enforcing = sorted({o["reach"] for o in owners if o["reach"] in ENFORCING})
    return {
        "candidate": c, "policy_id": pid, "status": cov["status"], "strength_status": cov["strength_status"],
        "check_level": pm["check_level"], "reviews": pm.get("reviews", []), "counterexample": pm.get("counterexample", []),
        "n_direct": len(direct), "n_partial": len(partial), "owners": owners, "direct_reach": reaches,
        "best_reach": reaches[0] if reaches else None, "enforcing_reach": enforcing,
        "step2_divergences": d["div"].get((c, pid), []), "partial_witness_38": (c, pid) in d["pw"],
        "reviewer_override_note": cov.get("reviewer_override_note"),
    }


def render(batch):
    d = load()
    out_md = []
    out_js = []
    for pid in batch["policies"]:
        p = d["pol"][pid]
        out_md.append(f"## {pid} — {p['name']}  [{p['normative_strength']}, trigger={p['trigger_class']}, scope={p['scope']}]")
        out_md.append(f"CANON: {p['normalized_policy']}")
        cells = [cell_data(c, pid) for c in CANDS]
        out_md.append("REACH: " + "  ".join(f"{cd['candidate']}={cd['best_reach']}" for cd in cells)
                      + " || ENF: " + "  ".join(f"{cd['candidate']}={'/'.join(cd['enforcing_reach']) or '-'}" for cd in cells))
        for cd in cells:
            c = cd["candidate"]
            flags = []
            if cd["strength_status"] != "EQUIVALENT_EVIDENCE_PRESENT":
                flags.append(cd["strength_status"])
            if cd["partial_witness_38"]:
                flags.append("PW38")
            if cd["check_level"] != "MECHANICAL_WITNESS_ONLY":
                flags.append(cd["check_level"])
            if cd["step2_divergences"]:
                flags.append("S2DIV:" + ",".join(sorted({x[1] or "?" for x in cd["step2_divergences"]})))
            if cd["reviewer_override_note"]:
                flags.append("OVERRIDE")
            if any(o["v2v3"] not in ("UNCHANGED", "ANCHOR_SHIFT_ONLY") for o in cd["owners"]):
                flags.append("V3_RECORD_DELTA")
            out_md.append(f"### {c}  D{cd['n_direct']}/P{cd['n_partial']} reach={'/'.join(cd['direct_reach'])}"
                          f" enf={'/'.join(cd['enforcing_reach']) or '-'} {' '.join(flags)}")
            shown = 0
            rest = []
            seen = {}
            uniq = []
            for o in cd["owners"]:
                sig = (o["path"], o["start"], o["end"])
                if sig in seen and o["path"]:
                    seen[sig]["dup_keys"].append(f"{o['key']}({o['role']},{o['modality']},{o['svc']})")
                    continue
                o = dict(o)
                o["dup_keys"] = []
                seen[sig] = o
                uniq.append(o)
            shown_p = 0
            for o in uniq:
                loc0 = f"{o['path'].split('/template/', 1)[1]}:{o['start']}" if o["path"] else "?"
                compact = (o["role"] == "D" and shown >= 4) or (
                    o["role"] != "D" and (o["svc"] == "SAME" or o["svc"] == "N/A" or shown_p >= 2))
                if compact:
                    rest.append(f"{o['key']}({o['role']},{o['modality']},{o['svc']},{o['reach']},{loc0})")
                    continue
                if o["role"] == "D":
                    shown += 1
                else:
                    shown_p += 1
                lim = (300 if o["role"] == "D" else 150) if o["svc"] == "SAME" else 380
                loc = f"{o['path'].split('/template/', 1)[1]}:{o['start']}" if o["path"] else "?"
                if o["end"] and o["start"] and o["end"] != o["start"]:
                    loc += f"-{o['end']}"
                head = f"- [{o['role']}] {o['key']} {o['modality']}/{o['svc']} {o['reach']} @{loc}"
                if not o["active"]:
                    head += " INACTIVE"
                if o["repair_status"] not in ("UNCHANGED", "MOVED"):
                    head += f" ({o['repair_status']})"
                if o["v2v3"] not in ("UNCHANGED", "ANCHOR_SHIFT_ONLY"):
                    head += f" [v3:{o['v2v3']}]"
                if o["dup_keys"]:
                    head += " +same-lines: " + ", ".join(o["dup_keys"])
                out_md.append(head)
                out_md.append(f"    > {trim(o['text'], lim) if o['text'] else 'UNRESOLVED ANCHOR'}")
                notes = []
                if o["exc_status"] in ("REVIEWER", "REPAIR") and o["exceptions"] not in (None, "NONE"):
                    notes.append("exc: " + trim(o["exceptions"], 160))
                if o["app_override"]:
                    notes.append("app: " + trim(json.dumps(o["app_override"], ensure_ascii=False), 160))
                if o["comparison_qualifier"]:
                    notes.append("qual: " + trim(str(o["comparison_qualifier"]), 160))
                if notes:
                    out_md.append("    " + " | ".join(notes))
            if rest:
                out_md.append("  +" + str(len(rest)) + " more: " + "; ".join(rest))
            if cd["reviews"]:
                out_md.append("  reviews: " + "; ".join(f"{x.get('rule')}={x.get('verdict')}" for x in cd["reviews"]))
        out_md.append("")
        out_js.append({"policy_id": pid, "cells": [
            {k: v for k, v in cd.items() if k not in ("owners",)} | {"owners": [
                {k: o[k] for k in ("key", "role", "modality", "svc", "classification", "reach", "path", "start", "end",
                                   "active", "repair_status", "changed_vs_frozen", "changed_vs_v2")} | {
                    "text_sha_ok": o["text"] is not None} for o in cd["owners"]]}
            for cd in cells]})
    return "\n".join(out_md), out_js


def build(bid):
    bp = read_json(S3 / "BATCH_PLAN.json")
    b = [x for x in bp["batches"] if x["batch"] == bid][0]
    md, js = render(b)
    write_text_atomic(S3 / "_dossiers" / f"{bid}.md", f"# Dossier {bid} ({b['group']})\n\n" + md)
    write_json_atomic(S3 / "_dossiers" / f"{bid}.json", {"batch": bid, "group": b["group"], "policies": js})
    print(bid, len(md), "chars")


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan()
    elif sys.argv[1] == "build":
        for bid in sys.argv[2:]:
            build(bid)
