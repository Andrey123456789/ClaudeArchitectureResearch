"""Step 3 assembly (P5): build the deliverable data files from the per-policy checkpoints.

  python -B _tools/assemble.py

Reads only CHECKPOINTS/policies/, the Step 3 extras outputs, the probe results and v3 inputs (read-only).
Writes:
  POLICY_SIX_WAY_MATRIX.jsonl        196 policy records (six cells embedded, with owner anchors)
  POLICY_CELL_INDEX.jsonl            1,176 cell rows
  POLICY_PAIRWISE_DIFFERENCES.jsonl  15 pair rows per material difference
  ROOT_CAUSE_SUMMARY.json            policy-level and extras-level roots, each counted once
  PARTIAL_ORDER_BY_AXIS.json         pair tallies per axis and the predeclared ranking-rule evaluation
  V3_CHANGED_FILES_IMPACT.jsonl      the 104 changed-vs-frozen files (26 also vs v2) and the comparisons they bear on
  _assembly/CHALLENGE_TARGETS.json   the 5 STRONGER_AND_WEAKER cells and 38 partial-witness cells with their Step 3 treatment
  METRICS.json                       every count the reports cite (one universe per key)
"""
import collections
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import CANDS, PAIRS, S3, V3, canonical_policies, cand_lines, read_jsonl, sha256_file, write_json_atomic, write_jsonl_atomic  # noqa: E402

LABELS = ["FULL_SEMANTIC_PARITY", "PARTIAL_PARITY_WITH_DELTA", "MEANINGFUL_DIVERGENCE", "CONTEXT_DEPENDENT", "UNVERIFIED"]
LEVELS = ["FULL_SOURCE_COMPARED", "PARTIAL_SOURCE_COMPARED", "MECHANICAL_WITNESS_ONLY", "UNVERIFIED"]


def anchor_of(rec):
    ref = (rec.get("current_evidence_refs") or [{}])[0]
    p = ref.get("path") or ""
    return p, ref.get("start_line"), ref.get("end_line") or ref.get("start_line")


def main():
    canon = {p["id"]: p for p in canonical_policies()}
    recs = {r["source_key"]: r for r in read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl")}
    v3m = {(r["policy_id"], r["candidate"]): r for r in read_jsonl(V3 / "POLICY_PARITY_MATRIX.jsonl")}
    pw38 = {(r["policy_id"], r["candidate"]): r for r in read_jsonl(V3 / "PARTIAL_WITNESSES_38.jsonl")}
    cps = {}
    for f in sorted((S3 / "CHECKPOINTS" / "policies").glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        cps[c["policy_id"]] = (c, sha256_file(f))
    if set(cps) != set(canon):
        raise SystemExit(f"checkpoint set mismatch: missing {sorted(set(canon) - set(cps))} extra {sorted(set(cps) - set(canon))}")
    order = [p["id"] for p in canonical_policies()]

    def owner_entry(k):
        r = recs.get(k)
        if not r:
            return {"key": k, "anchor": None}
        p, s, e = anchor_of(r)
        rel = p.split("/template/", 1)[-1]
        text = ""
        try:
            lines = cand_lines(p)
            text = " ".join(x.strip() for x in lines[s - 1:e])[:300]
        except Exception:  # noqa: BLE001
            text = None
        return {"key": k, "anchor": f"{rel}:{s}" + (f"-{e}" if e and e != s else ""), "modality": r["modality"],
                "classification": r["classification"], "current_text": text}

    matrix, cells_rows, pair_rows = [], [], []
    roots = collections.defaultdict(lambda: {"policies": [], "material": False, "axes": set(), "kinds": set(), "extras_clusters": []})
    for pid in order:
        c, h = cps[pid]
        j = c["judgment"]
        p = canon[pid]
        cell_out = {}
        for a in CANDS:
            cell = c["cells"][a]
            v = v3m[(pid, a)]
            row = {"policy_id": pid, "candidate": a, "step3_level": cell["level"], "force_read": cell["force"],
                   "canonical_compliance": cell["compliance"], "best_reach": cell["best_reach"],
                   "direct_reach": cell["direct_reach"], "enforcing_reach": cell["enforcing_reach"],
                   "owners": [owner_entry(k) for k in cell["owners"]], "linked_keys": cell["linked_keys"],
                   "note": cell["note"], "unread": cell["unread"], "conditions": cell["conditions"],
                   "v3_check_level": v["check_level"], "v3_status": v["status"], "v3_strength_status": v["strength_status"],
                   "partial_witness_38": (pid, a) in pw38, "step2_divergence_keys": cell["step2_divergence_keys"],
                   "policy_label": j["label"]}
            cells_rows.append(row)
            cell_out[a] = {k: row[k] for k in row if k not in ("policy_id", "candidate", "policy_label")}
        diffs = j.get("diffs") or []
        for d in diffs:
            if d.get("root"):
                rt = roots[d["root"]]
                rt["policies"].append({"policy_id": pid, "dim": d["dim"], "material": d["material"], "tiers": d["tiers"], "label": j["label"]})
                rt["material"] = rt["material"] or d["material"]
                rt["axes"].add(d["axis"])
                rt["kinds"].add(d["kind"])
                rt.setdefault("what", d["what"])
            if d["material"]:
                pl = {(x["a"], x["b"]): x["label"] for x in c["pairs"] if x["dim"] == d["dim"]}
                for a, b in PAIRS:
                    lab = pl.get((a, b))
                    if lab is None:
                        raise SystemExit(f"{pid} {d['dim']}: pair {a}-{b} missing in checkpoint")
                    ev = d.get("evidence") or {}
                    pair_rows.append({"policy_id": pid, "dim": d["dim"], "axis": d["axis"], "kind": d["kind"], "root": d.get("root"),
                                      "a": a, "b": b, "label": lab, "evidence_a": ev.get(a, []), "evidence_b": ev.get(b, []),
                                      "counterexample": d.get("counterexample"), "tiers": d["tiers"],
                                      "verification": j.get("enforcement") or "source-read"})
        matrix.append({"policy_id": pid, "name": p.get("name"), "group": p["group"], "canonical_strength": p["normative_strength"],
                       "trigger_class": p.get("trigger_class"), "scope": p.get("scope"), "canonical_text": p.get("normalized_policy"),
                       "label": j["label"], "dims": j["dims"], "same_justification": j["same"], "diffs": diffs,
                       "cells": cell_out, "reach": j.get("reach"), "enforcement_evidence": j.get("enforcement"),
                       "notes": j.get("notes"), "challenge": j.get("challenge"), "batch": c["batch"],
                       "checkpoint_sha256": h, "judgment_sha256": c["judgment_sha256"], "dossier_sha256": c["dossier_sha256"]})

    # extras roots
    extras = read_jsonl(S3 / "EXTRA_OBLIGATIONS_SIX_WAY.jsonl")
    for x in extras:
        for l in x.get("links") or []:
            if l.startswith("RC-") and l in roots:
                roots[l]["extras_clusters"].append(x["cluster_id"])
    gen = json.loads((S3 / "EXTRA_GENUINE_ROOTS.json").read_text(encoding="utf-8"))["roots"]
    root_out = {"policy_level": {}, "extras_level": {}}
    for k, v in sorted(roots.items()):
        root_out["policy_level"][k] = {"material": v["material"], "axes": sorted(v["axes"]), "kinds": sorted(v["kinds"]),
                                       "policies": v["policies"], "what_first": v.get("what"),
                                       "extras_clusters_linked": sorted(set(v["extras_clusters"]))}
    for g in gen:
        root_out["extras_level"][g["id"]] = {k: g[k] for k in ("family", "title", "present", "absent", "task_effect", "clusters", "evidence")}
    write_json_atomic(S3 / "ROOT_CAUSE_SUMMARY.json", root_out)

    # partial order per axis: per pair, count policy-dims and distinct roots
    po = {}
    for axis in ("NORMATIVE", "DELIVERY", "ENFORCEMENT"):
        mat = {}
        for a, b in PAIRS:
            t = collections.Counter()
            tr = collections.defaultdict(set)
            for r in pair_rows:
                if r["axis"] == axis and r["a"] == a and r["b"] == b:
                    t[r["label"]] += 1
                    tr[r["label"]].add(r["root"] or f"{r['policy_id']}:{r['dim']}")
            mat[f"{a}-{b}"] = {"policy_dims": dict(t), "distinct_roots": {k: sorted(v) for k, v in tr.items()}}
        po[axis] = mat
    n_full = sum(1 for r in cells_rows if r["step3_level"] == "FULL_SOURCE_COMPARED")
    norm_material = sum(1 for m in matrix for d in m["diffs"] if d["axis"] == "NORMATIVE" and d["material"])
    ranking = {
        "rule": "PROTOCOL.md section 10 (predeclared)",
        "cond1_full_cells_share": round(n_full / len(cells_rows), 4), "cond1_pass": n_full / len(cells_rows) >= 0.95,
        "cond2_normative_material_dims": norm_material,
        "cond2_pass": False,
        "cond2_reason": ("No material NORMATIVE difference exists, so no pair has a normative dominance count above zero; the "
                         "normative relation is parity (empty strict order), which yields no ranking.") if norm_material == 0 else "see tallies",
        "cond3_pass": None, "global_ranking_reported": False,
        "consequence": "Partial order per axis only; normative and enforcement axes are never combined."}
    po["ranking_rule_evaluation"] = ranking
    write_json_atomic(S3 / "PARTIAL_ORDER_BY_AXIS.json", po)

    # changed files impact
    fx = read_jsonl(V3 / "V2_TO_V3_FILE_CROSSWALK.jsonl")
    uses = collections.defaultdict(set)
    for m in matrix:
        for a, cell in m["cells"].items():
            for k in set(cell["linked_keys"]) | {o["key"] for o in cell["owners"]}:
                r = recs.get(k)
                if r:
                    uses[(a, anchor_of(r)[0].split("/template/", 1)[-1])].add(m["policy_id"])
        for d in m["diffs"]:
            for a, ks in (d.get("evidence") or {}).items():
                for k in ks:
                    r = recs.get(k)
                    if r:
                        uses[(a, anchor_of(r)[0].split("/template/", 1)[-1])].add(m["policy_id"])
    labels = {m["policy_id"]: m["label"] for m in matrix}
    ch_rows = []
    for x in fx:
        if not x["changed_vs_frozen"]:
            continue
        pols = sorted(uses.get((x["candidate"], x["path"]), set()))
        ch_rows.append({"candidate": x["candidate"], "path": x["path"], "changed_vs_frozen": True, "changed_vs_v2": x["changed_vs_v2"],
                        "repair_rules": x["rules"], "v3_sha256": x["v3_sha256"], "policies_compared_from_this_file": pols,
                        "labels": dict(collections.Counter(labels[p] for p in pols)),
                        "bearing": ("Compared from current v3 bytes in P1 (dossier lines and targeted reads)." if pols else
                                    "No P1 cell owner or difference evidence anchors in this file; it bears on extras, enforcement wiring or meta files only.")})
    write_jsonl_atomic(S3 / "V3_CHANGED_FILES_IMPACT.jsonl", ch_rows)

    # challenge targets
    saw = [(pid, a) for (pid, a), v in v3m.items() if v["strength_status"] == "STRONGER_AND_WEAKER_EVIDENCE"]
    tgt = {"stronger_and_weaker_cells": [], "partial_witness_cells": []}
    for pid, a in sorted(saw):
        m = next(x for x in matrix if x["policy_id"] == pid)
        tgt["stronger_and_weaker_cells"].append({"policy_id": pid, "candidate": a, "label": m["label"], "challenge": m["challenge"],
                                                  "cell_note": m["cells"][a]["note"], "cell_level": m["cells"][a]["step3_level"]})
    for (pid, a), w in sorted(pw38.items()):
        m = next(x for x in matrix if x["policy_id"] == pid)
        tgt["partial_witness_cells"].append({"policy_id": pid, "candidate": a, "label": m["label"], "v3_status": w["status"],
                                             "cell_note": m["cells"][a]["note"], "cell_owners": [o["key"] for o in m["cells"][a]["owners"]],
                                             "cell_level": m["cells"][a]["step3_level"]})
    write_json_atomic(S3 / "_assembly" / "CHALLENGE_TARGETS.json", tgt)

    write_jsonl_atomic(S3 / "POLICY_SIX_WAY_MATRIX.jsonl", matrix)
    write_jsonl_atomic(S3 / "POLICY_CELL_INDEX.jsonl", cells_rows)
    write_jsonl_atomic(S3 / "POLICY_PAIRWISE_DIFFERENCES.jsonl", pair_rows)

    # metrics
    lab = collections.Counter(m["label"] for m in matrix)
    met = {
        "built_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "universe_policies": {"n": len(matrix), "labels": {k: lab.get(k, 0) for k in LABELS},
                              "labels_by_group": {g: dict(collections.Counter(m["label"] for m in matrix if m["group"] == g))
                                                  for g in sorted({m["group"] for m in matrix})},
                              "labels_by_canonical_strength": {s: dict(collections.Counter(m["label"] for m in matrix if m["canonical_strength"] == s))
                                                               for s in sorted({m["canonical_strength"] for m in matrix})}},
        "universe_cells": {"n": len(cells_rows),
                           "step3_levels_a_to_d": {k: sum(1 for r in cells_rows if r["step3_level"] == k) for k in LEVELS},
                           "canonical_compliance": dict(collections.Counter(r["canonical_compliance"] for r in cells_rows)),
                           "v3_check_levels": dict(collections.Counter(r["v3_check_level"] for r in cells_rows)),
                           "v3_strength_status": dict(collections.Counter(r["v3_strength_status"] for r in cells_rows)),
                           "partial_witness_38_cells": sum(1 for r in cells_rows if r["partial_witness_38"]),
                           "cells_with_analyst_note": sum(1 for r in cells_rows if r["note"])},
        "universe_differences": {"total": sum(len(m["diffs"]) for m in matrix),
                                 "by_axis_material": {f"{ax}/{'material' if mt else 'non_material'}": n for (ax, mt), n in collections.Counter(
                                     (d["axis"], d["material"]) for m in matrix for d in m["diffs"]).items()},
                                 "by_kind": dict(collections.Counter(d["kind"] for m in matrix for d in m["diffs"])),
                                 "material_dims": sum(1 for m in matrix for d in m["diffs"] if d["material"]),
                                 "pair_rows": len(pair_rows), "pair_labels": dict(collections.Counter(r["label"] for r in pair_rows)),
                                 "policy_level_roots": len(root_out["policy_level"]),
                                 "policy_level_roots_material": sum(1 for v in root_out["policy_level"].values() if v["material"])},
        "universe_extras": {"records": sum(x["n_records"] for x in extras), "clusters": len(extras),
                            "classes": dict(collections.Counter(x["class"] for x in extras)),
                            "decided_by": dict(collections.Counter(x["decided_by"] for x in extras)),
                            "extras_level_roots": len(gen)},
        "universe_files": {"changed_vs_frozen": len(ch_rows), "changed_vs_v2": sum(1 for r in ch_rows if r["changed_vs_v2"]),
                           "changed_files_bearing_on_p1": sum(1 for r in ch_rows if r["policies_compared_from_this_file"])},
        "challenge_targets": {"stronger_and_weaker_cells": len(tgt["stronger_and_weaker_cells"]),
                              "partial_witness_cells": len(tgt["partial_witness_cells"])},
        "ranking_rule": ranking,
    }
    write_json_atomic(S3 / "METRICS.json", met)
    print(json.dumps({k: met[k] for k in ("universe_policies", "universe_cells")}, indent=1)[:2500])
    print(json.dumps(met["universe_differences"], indent=1))
    print(json.dumps(met["universe_files"]), json.dumps(met["challenge_targets"]))


if __name__ == "__main__":
    main()
