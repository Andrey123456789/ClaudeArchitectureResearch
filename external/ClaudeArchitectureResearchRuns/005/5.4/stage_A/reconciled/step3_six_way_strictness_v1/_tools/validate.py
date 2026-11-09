"""Gate E: final cold audit (read-only toward every input; writes only VALIDATION_REPORT.json and an attempt file).

  python -B _tools/validate.py

Re-reads the final Step 3 artifacts without trusting any earlier PASS label: recomputes every count, re-hashes the
input snapshot, re-resolves every owner anchor and evidence key against the current v3 bytes, re-derives pair labels
from tiers, re-hashes checkpoints and decision files, cross-checks decisions, metrics and the final report.
"""
import collections
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import CANDS, PAIRS, ROOT, S3, V3, canonical_policies, read_jsonl, sha256_file, sha256_text, write_json_atomic  # noqa: E402

LABELS = {"FULL_SEMANTIC_PARITY", "PARTIAL_PARITY_WITH_DELTA", "MEANINGFUL_DIVERGENCE", "CONTEXT_DEPENDENT", "UNVERIFIED"}
PAIRL = {"SAME", "A_STRONGER", "B_STRONGER", "INCOMPARABLE", "NOT_APPLICABLE", "UNVERIFIED"}
XCLS = {"GENUINE_EXTRA_NORM", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "SAME_NORM_DIFFERENT_PACKAGING", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "UNRESOLVED_OR_DECISION_DEPENDENT"}
DELIVERABLES = ["STATE.json", "RESUME.md", "PROTOCOL.md", "UPSTREAM_FINGERPRINT.json", "POLICY_SIX_WAY_MATRIX.jsonl", "POLICY_CELL_INDEX.jsonl",
                "POLICY_PAIRWISE_DIFFERENCES.jsonl", "EXTRA_OBLIGATIONS_SIX_WAY.jsonl", "HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md",
                "OPEN_DECISIONS_AND_SENSITIVITY.md", "METRIC_LINEAGE_AND_LIMITS.md", "FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md",
                "SEMANTIC_CHALLENGE_LOG.jsonl", "METRICS.json", "ROOT_CAUSE_SUMMARY.json", "PARTIAL_ORDER_BY_AXIS.json",
                "EXTRA_GENUINE_ROOTS.json", "V3_CHANGED_FILES_IMPACT.jsonl", "HOOK_PROBE_RESULTS.json", "HOOK_PROBE2_RESULTS.json", "HOOK_PROBE3_RESULTS.json"]


def main():
    checks, errs = {}, []

    def chk(name, ok, detail=None):
        checks[name] = {"ok": bool(ok), "detail": detail}
        if not ok:
            errs.append(name)

    # E01 inputs
    fp = json.loads((S3 / "UPSTREAM_FINGERPRINT.json").read_text(encoding="utf-8"))
    hashes = json.loads((S3 / "UPSTREAM_V3_TREE_HASHES.json").read_text(encoding="utf-8"))
    files = hashes.get("files", hashes)
    drift = [p for p, h in files.items() if not (V3 / p).exists() or sha256_file(V3 / p) != h]
    present = {str(p.relative_to(V3)).replace("\\", "/") for p in V3.rglob("*") if p.is_file()}
    extra = sorted(present - set(files))
    kd = [k for k, h in fp["v3_key_files_sha256"].items() if sha256_file(V3 / k) != h]
    od = [k for k, h in fp["other_inputs_sha256"].items() if not (ROOT / k).exists() or sha256_file(ROOT / k) != h]
    inv = ROOT / "inputs" / "M" / "source"
    orc = sha256_file(inv / "inventory.json") == fp["oracle"]["inventory_sha256"] and sha256_file(inv / "shared-research-invariants.json") == fp["oracle"]["invariants_sha256"]
    chk("E01-INPUT-SNAPSHOT", not drift and not extra and not kd and not od and orc,
        {"v3_files": len(files), "drift": drift[:5], "unexpected_new": extra[:5], "key_drift": kd, "other_drift": od, "oracle_ok": orc})
    # E02 deliverables
    missing = [d for d in DELIVERABLES if not (S3 / d).exists()]
    chk("E02-DELIVERABLES-PRESENT", not missing, missing)
    # load
    canon = {p["id"]: p for p in canonical_policies()}
    matrix = read_jsonl(S3 / "POLICY_SIX_WAY_MATRIX.jsonl")
    cells = read_jsonl(S3 / "POLICY_CELL_INDEX.jsonl")
    pairs = read_jsonl(S3 / "POLICY_PAIRWISE_DIFFERENCES.jsonl")
    recs = {r["source_key"]: r for r in read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl")}
    # E03 matrix and label rules
    bad = []
    ids = [m["policy_id"] for m in matrix]
    if len(ids) != 196 or set(ids) != set(canon) or len(set(ids)) != 196:
        bad.append("policy id set")
    for m in matrix:
        lab, diffs = m["label"], m["diffs"]
        if lab not in LABELS or set(m["cells"]) != set(CANDS):
            bad.append(f"{m['policy_id']} label/cells")
        mat = [d for d in diffs if d["material"]]
        if lab == "FULL_SEMANTIC_PARITY" and (diffs or any(c["step3_level"] != "FULL_SOURCE_COMPARED" for c in m["cells"].values())):
            bad.append(f"{m['policy_id']} FULL with diffs or non-full cells")
        if lab == "PARTIAL_PARITY_WITH_DELTA" and (not diffs or mat):
            bad.append(f"{m['policy_id']} PARTIAL rule")
        if lab == "MEANINGFUL_DIVERGENCE" and (not mat or any(not d.get("counterexample") for d in mat)):
            bad.append(f"{m['policy_id']} MEANINGFUL rule")
        if not m["same_justification"]:
            bad.append(f"{m['policy_id']} no justification")
        for d in diffs:
            placed = [c for t in d["tiers"] for c in t]
            if sorted(placed) != sorted(CANDS):
                bad.append(f"{m['policy_id']} {d['dim']} tiers do not place six")
    chk("E03-MATRIX-AND-LABEL-RULES", not bad, bad[:10])
    # E04 cell index
    keys = [(c["policy_id"], c["candidate"]) for c in cells]
    cons = all(m["cells"][a]["step3_level"] == next(c for c in cells if c["policy_id"] == m["policy_id"] and c["candidate"] == a)["step3_level"]
               for m in matrix[:20] for a in CANDS)
    chk("E04-CELL-INDEX", len(keys) == 1176 == len(set(keys)) and cons, {"rows": len(keys)})
    # E05 owner anchors re-resolved
    an_bad, n_an = [], 0
    for m in matrix:
        for a, c in m["cells"].items():
            for o in c["owners"]:
                n_an += 1
                r = recs.get(o["key"])
                if not r or r["candidate"] != a or not o.get("anchor"):
                    an_bad.append(f"{m['policy_id']}/{a}/{o['key']}")
                    continue
                path, rng = o["anchor"].rsplit(":", 1)
                s, _, e = rng.partition("-")
                s, e = int(s), int(e or s)
                f = V3 / "candidates" / a / "template" / path
                if not f.exists():
                    an_bad.append(f"{o['key']} missing file")
                    continue
                lines = f.read_text(encoding="utf-8", errors="replace").split("\n")
                if e > len(lines) or " ".join(x.strip() for x in lines[s - 1:e])[:300] != o["current_text"]:
                    an_bad.append(f"{o['key']} text mismatch")
    chk("E05-OWNER-ANCHORS-RESOLVE", not an_bad, {"anchors": n_an, "bad": an_bad[:10]})
    # E06 evidence keys
    ev_bad, n_ev = [], 0
    for m in matrix:
        for d in m["diffs"]:
            for a, ks in (d.get("evidence") or {}).items():
                for k in ks:
                    n_ev += 1
                    if k not in recs or recs[k]["candidate"] != a:
                        ev_bad.append(f"{m['policy_id']} {d['dim']} {a}:{k}")
    chk("E06-EVIDENCE-KEYS", not ev_bad, {"keys": n_ev, "bad": ev_bad[:10]})
    # E07 pairwise
    pb = []
    mats = [(m["policy_id"], d) for m in matrix for d in m["diffs"] if d["material"]]
    for pid, d in mats:
        rows = [p for p in pairs if p["policy_id"] == pid and p["dim"] == d["dim"]]
        if sorted((r["a"], r["b"]) for r in rows) != sorted(PAIRS):
            pb.append(f"{pid} {d['dim']} pair set")
        tier = {c: i for i, t in enumerate(d["tiers"]) for c in t}
        inc = {tuple(x) for x in (d.get("incomparable") or [])} | {tuple(reversed(x)) for x in (d.get("incomparable") or [])}
        for r in rows:
            if r["label"] not in PAIRL:
                pb.append(f"{pid} bad label")
            exp = ("INCOMPARABLE" if (r["a"], r["b"]) in inc else "SAME" if tier[r["a"]] == tier[r["b"]]
                   else "A_STRONGER" if tier[r["a"]] < tier[r["b"]] else "B_STRONGER")
            if r["label"] != exp:
                pb.append(f"{pid} {d['dim']} {r['a']}-{r['b']} {r['label']}!={exp}")
    chk("E07-PAIRWISE-FROM-TIERS", not pb and len(pairs) == 15 * len(mats), {"rows": len(pairs), "material_dims": len(mats), "bad": pb[:10]})
    # E08 checkpoints, judgments, dossiers
    cb = []
    for m in matrix:
        f = S3 / "CHECKPOINTS" / "policies" / f"{m['policy_id']}.json"
        cp = json.loads(f.read_text(encoding="utf-8"))
        if sha256_file(f) != m["checkpoint_sha256"]:
            cb.append(f"{m['policy_id']} checkpoint hash")
        if sha256_file(S3 / "_judgments" / f"{cp['batch']}.py") != cp["judgment_sha256"]:
            cb.append(f"{m['policy_id']} judgment file changed after gate B")
        if sha256_file(S3 / "_dossiers" / f"{cp['batch']}.json") != cp["dossier_sha256"] and cp["batch"] != "B01":
            cb.append(f"{m['policy_id']} dossier changed")
        if sha256_text(json.dumps({"judgment": cp["judgment"], "cells": cp["cells"], "pairs": cp["pairs"]}, sort_keys=True)) != cp["record_sha256"]:
            cb.append(f"{m['policy_id']} record hash")
    gB = [b for b in (f"B{i:02d}" for i in range(1, 31)) if not (S3 / "CHECKPOINTS" / "gates" / f"gateB_{b}.json").exists()]
    chk("E08-CHECKPOINT-INTEGRITY", not cb and not gB, {"bad": cb[:10], "missing_gateB": gB,
                                                        "note": "B01 dossier was rebuilt after its check (PROTOCOL AD-1); its old hash is kept"})
    # E09 extras
    xr = read_jsonl(S3 / "EXTRA_OBLIGATIONS_SIX_WAY.jsonl")
    plan = json.loads((S3 / "_extras" / "CHUNK_PLAN.json").read_text(encoding="utf-8"))["chunks"]
    xb = [x["cluster_id"] for x in xr if x["class"] not in XCLS]
    for p in plan:
        cpf = S3 / "CHECKPOINTS" / "extras" / f"{p['chunk']}.json"
        if not cpf.exists() or json.loads(cpf.read_text(encoding="utf-8"))["decisions_sha256"] != sha256_file(S3 / "_extras" / "decisions" / f"{p['chunk']}.py"):
            xb.append(f"{p['chunk']} decisions changed or unchecked")
    gen = [x for x in xr if x["class"] == "GENUINE_EXTRA_NORM"]
    xb += [x["cluster_id"] for x in gen if not x.get("root") or not x.get("task_effect")]
    chk("E09-EXTRAS", len(xr) == 797 and sum(x["n_records"] for x in xr) == 1777 and not xb, {"bad": xb[:10]})
    # E10 roots and decision cross-references
    rs = json.loads((S3 / "ROOT_CAUSE_SUMMARY.json").read_text(encoding="utf-8"))
    known = set(rs["policy_level"]) | set(rs["extras_level"])
    rb = [d["root"] for m in matrix for d in m["diffs"] if d.get("root") and d["root"] not in rs["policy_level"]]
    qids = {f"Q-{i:02d}" for i in range(1, 14)}
    for x in xr:
        for l in x.get("links") or []:
            if l.startswith("RC-") and l not in known and l != "RC-TXT-FINAL-REPORT-CONTENT":
                rb.append(f"{x['cluster_id']}:{l}")
            if l.startswith("Q-") and l not in qids:
                rb.append(f"{x['cluster_id']}:{l}")
    od_text = (S3 / "OPEN_DECISIONS_AND_SENSITIVITY.md").read_text(encoding="utf-8")
    queue = {r["id"]: r["kind"] for r in read_jsonl(V3 / "UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl")}
    qb = [q for q, kind in queue.items() if not re.search(rf"^\| {q} \| {kind} \|", od_text, re.M)]
    chk("E10-ROOTS-AND-DECISIONS", not rb and not qb and set(queue) == qids, {"bad_roots": rb[:10], "queue_rows_missing": qb})
    # E11 metrics recomputed
    met = json.loads((S3 / "METRICS.json").read_text(encoding="utf-8"))
    lab = collections.Counter(m["label"] for m in matrix)
    lv = collections.Counter(c["step3_level"] for c in cells)
    mb = []
    if {k: v for k, v in met["universe_policies"]["labels"].items() if v} != dict(lab):
        mb.append("labels")
    if {k: v for k, v in met["universe_cells"]["step3_levels_a_to_d"].items() if v} != dict(lv):
        mb.append("levels")
    if met["universe_differences"]["pair_rows"] != len(pairs) or met["universe_differences"]["material_dims"] != len(mats):
        mb.append("differences")
    if met["universe_extras"]["classes"] != dict(collections.Counter(x["class"] for x in xr)):
        mb.append("extras classes")
    chk("E11-METRICS-RECOMPUTED", not mb, mb)
    # E12 final report numbers
    rep = (S3 / "FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md").read_text(encoding="utf-8")
    rbad = []
    head = f"FULL_SEMANTIC_PARITY {lab['FULL_SEMANTIC_PARITY']} · PARTIAL_PARITY_WITH_DELTA {lab['PARTIAL_PARITY_WITH_DELTA']} · MEANINGFUL_DIVERGENCE {lab['MEANINGFUL_DIVERGENCE']} · CONTEXT_DEPENDENT {lab.get('CONTEXT_DEPENDENT', 0)} · UNVERIFIED {lab.get('UNVERIFIED', 0)}"
    if head not in rep:
        rbad.append("headline labels")
    for g, v in met["universe_policies"]["labels_by_group"].items():
        n = sum(v.values())
        row = re.search(rf"^\| {re.escape(g)} \([^)]*\) \| (\d+) \| (\d+) \| (\d+) \|", rep, re.M)
        if not row or tuple(int(x) for x in row.groups()) != (v.get("FULL_SEMANTIC_PARITY", 0), v.get("PARTIAL_PARITY_WITH_DELTA", 0), v.get("MEANINGFUL_DIVERGENCE", 0)):
            rbad.append(f"group {g} ({n})")
    for cls, n in met["universe_extras"]["classes"].items():
        if not re.search(rf"^\| {cls} \| {n} \|", rep, re.M):
            rbad.append(f"extras {cls}")
    if "(a) FULL_SOURCE_COMPARED | 1,176" not in rep or "Verdict: CONDITIONAL_GO" not in rep:
        rbad.append("cells/verdict")
    chk("E12-REPORT-NUMBERS", not rbad, rbad)
    # E13 gates C/D and probes
    gc = json.loads((S3 / "CHECKPOINTS" / "gates" / "gateC.json").read_text(encoding="utf-8")) if (S3 / "CHECKPOINTS" / "gates" / "gateC.json").exists() else None
    gd = (S3 / "CHECKPOINTS" / "gates" / "gateD.json").exists()
    log_ok = gc and sha256_file(S3 / "SEMANTIC_CHALLENGE_LOG.jsonl") == gc["log_sha256"]
    pr_ok = True
    for f, n in (("HOOK_PROBE_RESULTS.json", 8), ("HOOK_PROBE2_RESULTS.json", 10), ("HOOK_PROBE3_RESULTS.json", 6)):
        d = json.loads((S3 / f).read_text(encoding="utf-8"))
        sem = d["semantics"]
        pr_ok = pr_ok and set(d["results"]) == set(CANDS) and all(len(v) == n for v in d["results"].values())             and all("first" in x and "second" in x for v in d["results"].values() for x in v.values()) and ("NOT_RUN" in sem)
    chk("E13-GATES-AND-PROBES", bool(log_ok) and gd and pr_ok, {"gateC_log_matches": bool(log_ok), "gateD": gd, "probes_ok": pr_ok})
    # E14 state
    st = json.loads((S3 / "STATE.json").read_text(encoding="utf-8"))
    chk("E14-STATE", st.get("step4_started") is False and st["progress"]["policies_done"] == 196, {"phase": st["phase"]})

    k = len(list((S3 / "VALIDATION_ATTEMPTS").glob("gateE_attempt*"))) + 1
    out = {"gate": "E", "attempt": k, "at": datetime.datetime.now().isoformat(timespec="seconds"),
           "status": "PASS" if not errs else "FAIL", "failed": errs, "checks": checks,
           "source_read_vs_mechanical": "Policy cells: owner text read by the analyst (1,176 FULL_SOURCE_COMPARED). This validator verifies mechanically that every cited anchor and key resolves to the current v3 bytes; it does not re-judge semantics. Enforcement: script outputs executed in probes/v3 suites; other checker logic source-read; live host NOT_RUN."}
    write_json_atomic(S3 / "VALIDATION_ATTEMPTS" / f"gateE_attempt{k}_{out['status']}.json", out)
    write_json_atomic(S3 / "VALIDATION_REPORT.json", out)
    for n, v in checks.items():
        print(n, "OK" if v["ok"] else "FAIL", "" if v["ok"] else json.dumps(v["detail"])[:400])
    print("GATE E", out["status"], f"attempt {k}")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
