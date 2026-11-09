"""Gate B (per-batch structural gate) and per-policy checkpoints.

Usage:
  python -B _tools/judge.py check <BATCH> [<BATCH> ...]
  python -B _tools/judge.py status

check: loads _judgments/<BATCH>.py, validates every judgment against the protocol and the
batch dossier, and on PASS writes CHECKPOINTS/policies/<PID>.json for each policy and
CHECKPOINTS/gates/<BATCH>.json with the cumulative tally. Every attempt (PASS or FAIL) is
kept in VALIDATION_ATTEMPTS/gateB_<BATCH>_attemptN_<STATUS>.json.
"""
import datetime
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jdsl  # noqa: E402
from s3common import (CANDS, PAIRS, S3, V3, canonical_policies, cand_lines, read_json, read_jsonl,  # noqa: E402
                      sha256_file, sha256_text, write_json_atomic)

_REC = {}


def recs():
    if not _REC:
        for r in read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl"):
            _REC[r["source_key"]] = r
    return _REC


def norm(s):
    s = re.sub(r"[`*_>#|]", "", s or "")
    s = re.sub(r"^\s*(?:[-+]|\d+\.)\s+", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def anchor_check(key):
    """Every current evidence ref of the record resolves to existing lines of the v3 file."""
    r = recs().get(key)
    if r is None:
        return "UNKNOWN_KEY"
    refs = r.get("current_evidence_refs") or []
    if not refs:
        return "NO_REFS"
    for e in refs:
        try:
            lines = cand_lines(e["path"])
        except FileNotFoundError:
            return f"MISSING_FILE {e['path']}"
        if not (1 <= e["start_line"] <= e["end_line"] <= len(lines)):
            return f"OUT_OF_RANGE {e['path']}:{e['start_line']}-{e['end_line']}"
    return "OK"


def quote_check(key):
    """For records whose text v3 did not change, the stored quote's first words are found in a current range."""
    r = recs()[key]
    q = r.get("primary_quote")
    if not q or r["repair"]["status"] not in ("UNCHANGED", "MOVED"):
        return "SKIPPED"
    head = norm(q)[:50]
    for e in r.get("current_evidence_refs") or []:
        txt = norm(" ".join(cand_lines(e["path"])[e["start_line"] - 1:e["end_line"]]))
        if head and head in txt:
            return "OK"
    return "NOT_FOUND"


def load_batch(bid):
    path = S3 / "_judgments" / f"{bid}.py"
    jdsl.take()
    spec = importlib.util.spec_from_file_location(f"judg_{bid}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return jdsl.take(), sha256_file(path)


def expand_cells(j, dossier_pol, canon):
    cells = {}
    dcells = {c["candidate"]: c for c in dossier_pol["cells"]}
    for c in CANDS:
        ov = j["cells"].get(c) or {}
        dc = dcells[c]
        direct = [o["key"] for o in dc["owners"] if o["role"] == "D"]
        cells[c] = {
            "level": jdsl.LEVELS[ov.get("level") or "FULL"],
            "force": ov.get("force") or canon["normative_strength"],
            "compliance": ov.get("compliance") or "EQUIVALENT",
            "owners": ov.get("owners") or direct,
            "linked_keys": [o["key"] for o in dc["owners"]],
            "note": ov.get("note"), "unread": ov.get("unread"), "conditions": ov.get("conditions"),
            "best_reach": dc["best_reach"], "direct_reach": dc["direct_reach"], "enforcing_reach": dc["enforcing_reach"],
            "v3_check_level": dc["check_level"], "v3_strength_status": dc["strength_status"],
            "v3_status": dc["status"], "partial_witness_38": dc["partial_witness_38"],
            "step2_divergence_keys": sorted({k for k, _ in dc["step2_divergences"]}),
        }
    return cells


def pair_label(diff, a, b, cells):
    for x in (a, b):
        if x in diff["unverified"] or cells[x]["level"] in ("MECHANICAL_WITNESS_ONLY", "UNVERIFIED"):
            return "UNVERIFIED"
    for x in (a, b):
        if x in diff["na"]:
            return "NOT_APPLICABLE"
    if [a, b] in diff["incomparable"] or [b, a] in diff["incomparable"]:
        return "INCOMPARABLE"
    ta = next(i for i, t in enumerate(diff["tiers"]) if a in t)
    tb = next(i for i, t in enumerate(diff["tiers"]) if b in t)
    if ta == tb:
        return "SAME"
    return "A_STRONGER" if ta < tb else "B_STRONGER"


def validate(j, dossier_pol, canon, errors, warns):
    pid = j["policy_id"]
    e = lambda m: errors.append(f"{pid}: {m}")  # noqa: E731
    if j["label"] not in jdsl.LABELS:
        e(f"bad label {j['label']}")
    if not j["dims"] or not all(re.match(r"^D\d+ ", d) for d in j["dims"]):
        e("dims must be 'D<n> text'")
    dim_ids = {d.split(" ", 1)[0] for d in j["dims"]}
    if not (j["same"] or "").strip():
        e("missing 'same' justification")
    for c, ov in j["cells"].items():
        if c not in CANDS:
            e(f"unknown candidate {c}")
            continue
        if (ov.get("level") or "FULL") not in jdsl.LEVELS:
            e(f"{c} bad level")
        if ov.get("level") == "PARTIAL" and not ov.get("unread"):
            e(f"{c} PARTIAL needs 'unread'")
        if ov.get("force") and ov["force"] not in jdsl.FORCES:
            e(f"{c} bad force {ov['force']}")
        if ov.get("compliance") and ov["compliance"] not in jdsl.COMPLIANCE:
            e(f"{c} bad compliance {ov['compliance']}")
        for k in ov.get("owners") or []:
            if recs().get(k, {}).get("candidate") != c:
                e(f"{c} owner {k} not a {c} record")
    material = False
    for d in j["diffs"]:
        if d["dim"] not in dim_ids:
            e(f"diff dim {d['dim']} not declared")
        if d["axis"] not in jdsl.AXES:
            e(f"bad axis {d['axis']}")
        if d["kind"] not in jdsl.KINDS:
            e(f"bad kind {d['kind']}")
        placed = [x for t in d["tiers"] for x in t] + list(d["na"]) + list(d["unverified"])
        if sorted(placed) != sorted(CANDS):
            e(f"diff {d['dim']} tiers/na/unverified must place each candidate once: {placed}")
        if not (d["what"] or "").strip():
            e(f"diff {d['dim']} missing 'what'")
        if d["material"]:
            material = True
            if not (d["counterexample"] or "").strip():
                e(f"material diff {d['dim']} needs a counterexample")
        for c, keys in d["evidence"].items():
            if c not in CANDS:
                e(f"evidence candidate {c}")
            for k in keys:
                if recs().get(k, {}).get("candidate") != c:
                    e(f"evidence key {k} not a {c} record")
    lab = j["label"]
    if lab == "FULL_SEMANTIC_PARITY":
        if j["diffs"]:
            e("FULL_SEMANTIC_PARITY with recorded diffs")
        if any((ov.get("level") or "FULL") != "FULL" for ov in j["cells"].values()):
            e("FULL_SEMANTIC_PARITY needs all cells FULL")
    if lab == "PARTIAL_PARITY_WITH_DELTA" and (not j["diffs"] or material):
        e("PARTIAL_PARITY_WITH_DELTA needs >=1 diff and no material diff")
    if lab == "MEANINGFUL_DIVERGENCE" and not material:
        e("MEANINGFUL_DIVERGENCE needs a material diff")
    if lab == "CONTEXT_DEPENDENT" and not any(d["incomparable"] or d["scope"] or d["decision"] for d in j["diffs"]):
        e("CONTEXT_DEPENDENT needs incomparable pairs, a scope note or a decision dependency")
    if lab in ("FULL_SEMANTIC_PARITY", "PARTIAL_PARITY_WITH_DELTA") and any(
            (ov.get("level") or "FULL") in ("MECHANICAL", "UNVERIFIED") for ov in j["cells"].values()):
        e(f"{lab} with a MECHANICAL/UNVERIFIED cell")
    if material and lab in ("FULL_SEMANTIC_PARITY", "PARTIAL_PARITY_WITH_DELTA"):
        e("material diff under a parity label")


def check(bid):
    plan = read_json(S3 / "BATCH_PLAN.json")
    b = [x for x in plan["batches"] if x["batch"] == bid][0]
    dossier = read_json(S3 / "_dossiers" / f"{bid}.json")
    dpol = {p["policy_id"]: p for p in dossier["policies"]}
    canon = {p["id"]: p for p in canonical_policies()}
    errors, warns = [], []
    try:
        judgments, jsha = load_batch(bid)
    except Exception as ex:  # a crash is a FAIL attempt, kept
        judgments, jsha = [], None
        errors.append(f"LOAD_ERROR {type(ex).__name__}: {ex}")
    ids = [j["policy_id"] for j in judgments]
    if sorted(ids) != sorted(b["policies"]) or len(ids) != len(set(ids)):
        errors.append(f"batch coverage: judged {sorted(ids)} expected {sorted(b['policies'])}")
    out = []
    anchors = Counter()
    quotes = Counter()
    for j in judgments:
        if j["policy_id"] not in dpol:
            continue
        validate(j, dpol[j["policy_id"]], canon[j["policy_id"]], errors, warns)
        cells = expand_cells(j, dpol[j["policy_id"]], canon[j["policy_id"]])
        keys = set()
        for c in CANDS:
            keys |= set(cells[c]["owners"])
        for d in j["diffs"]:
            for ks in d["evidence"].values():
                keys |= set(ks)
        for k in sorted(keys):
            a = anchor_check(k)
            anchors[a if a == "OK" else "BAD"] += 1
            if a != "OK":
                errors.append(f"{j['policy_id']}: anchor {k} {a}")
            q = quote_check(k)
            quotes[q] += 1
            if q == "NOT_FOUND":
                warns.append(f"{j['policy_id']}: stored quote head of {k} not found in current range (rewording?)")
        pairs = []
        for d in j["diffs"]:
            if d["material"] and not any(e.startswith(j["policy_id"]) for e in errors):
                for a_, b_ in PAIRS:
                    pairs.append({"dim": d["dim"], "a": a_, "b": b_, "label": pair_label(d, a_, b_, cells)})
        out.append({"judgment": j, "cells": cells, "pairs": pairs})
    status = "PASS" if not errors else "FAIL"
    att_dir = S3 / "VALIDATION_ATTEMPTS"
    n = len(list(att_dir.glob(f"gateB_{bid}_attempt*.json"))) + 1
    now = datetime.datetime.now().isoformat(timespec="seconds")
    att = {"gate": "B", "batch": bid, "attempt": n, "at": now, "status": status, "errors": errors, "warnings": warns,
           "anchors": dict(anchors), "quotes": dict(quotes), "judgment_sha256": jsha,
           "dossier_sha256": sha256_file(S3 / "_dossiers" / f"{bid}.json")}
    write_json_atomic(att_dir / f"gateB_{bid}_attempt{n}_{status}.json", att)
    if status == "PASS":
        for o in out:
            pid = o["judgment"]["policy_id"]
            write_json_atomic(S3 / "CHECKPOINTS" / "policies" / f"{pid}.json", {
                "policy_id": pid, "batch": bid, "at": now, "judgment_sha256": jsha,
                "dossier_sha256": att["dossier_sha256"], "record_sha256": sha256_text(json.dumps(o, sort_keys=True)),
                **o})
        done = sorted(p.stem for p in (S3 / "CHECKPOINTS" / "policies").glob("*.json"))
        labels = Counter()
        levels = Counter()
        for p in done:
            cp = read_json(S3 / "CHECKPOINTS" / "policies" / f"{p}.json")
            labels[cp["judgment"]["label"]] += 1
            for c in CANDS:
                levels[cp["cells"][c]["level"]] += 1
        write_json_atomic(S3 / "CHECKPOINTS" / "gates" / f"gateB_{bid}.json", {
            "gate": "B", "batch": bid, "at": now, "status": status, "attempt": n,
            "cumulative": {"policies_done": len(done), "cells_done": len(done) * 6, "labels": dict(labels),
                           "cell_levels": dict(levels)}})
    print(bid, status, f"errors={len(errors)} warnings={len(warns)}", dict(anchors), dict(quotes))
    for x in errors[:40]:
        print("  E", x)
    for x in warns[:15]:
        print("  W", x)
    return status


def status():
    plan = read_json(S3 / "BATCH_PLAN.json")
    done = {p.stem for p in (S3 / "CHECKPOINTS" / "policies").glob("*.json")}
    for b in plan["batches"]:
        n = sum(1 for p in b["policies"] if p in done)
        print(b["batch"], f"{n}/{len(b['policies'])}", "DONE" if n == len(b["policies"]) else "")
    print("policies done:", len(done), "/ 196")


if __name__ == "__main__":
    if sys.argv[1] == "check":
        rc = 0
        for bid in sys.argv[2:]:
            rc |= check(bid) != "PASS"
        sys.exit(rc)
    elif sys.argv[1] == "status":
        status()
