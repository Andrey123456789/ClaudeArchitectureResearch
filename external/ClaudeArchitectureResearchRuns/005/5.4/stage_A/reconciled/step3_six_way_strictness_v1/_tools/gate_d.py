"""Gate D: metric and provenance reconciliation (read-only).

  python -B _tools/gate_d.py

Checks that Step 3 counts reconcile with the final v3 outputs, that direct changes (v3 file changes), indirect
changes (record crosswalk statuses) and limits stay distinct, that Codex Pass 1/2/3 provenance is intact in the
extras inventory, and that no candidate or predecessor file changed (no Codex edit re-applied).
"""
import collections
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import RECON, S3, V3, read_jsonl, sha256_file, write_json_atomic  # noqa: E402


def main():
    res, errs = {}, []

    def chk(name, ok, detail):
        res[name] = {"ok": bool(ok), "detail": detail}
        if not ok:
            errs.append(name)

    met = json.loads((S3 / "METRICS.json").read_text(encoding="utf-8"))
    recs = read_jsonl(V3 / "REPAIRED_CLASSIFICATIONS.jsonl")
    act = [r for r in recs if r["repair"]["active"]]
    chk("D01-RECORD-UNIVERSE", len(recs) == 6498 and len(act) == 6495, {"rows": len(recs), "active": len(act)})
    v3m = read_jsonl(V3 / "POLICY_PARITY_MATRIX.jsonl")
    cells = read_jsonl(S3 / "POLICY_CELL_INDEX.jsonl")
    chk("D02-CELL-UNIVERSE", len(v3m) == len(cells) == 1176 and {(r["policy_id"], r["candidate"]) for r in v3m} == {(r["policy_id"], r["candidate"]) for r in cells},
        {"v3": len(v3m), "step3": len(cells)})
    cl = collections.Counter(r["check_level"] for r in v3m)
    chk("D03-V3-CHECK-LEVELS-CARRIED", dict(cl) == met["universe_cells"]["v3_check_levels"], dict(cl))
    ss = collections.Counter(r["strength_status"] for r in v3m)
    chk("D04-STRENGTH-STATUS", dict(ss) == met["universe_cells"]["v3_strength_status"] and ss["STRONGER_AND_WEAKER_EVIDENCE"] == 5, dict(ss))
    pw = read_jsonl(V3 / "PARTIAL_WITNESSES_38.jsonl")
    chk("D05-PARTIAL-WITNESSES", len(pw) == 38 == met["universe_cells"]["partial_witness_38_cells"], len(pw))
    xw = json.loads((V3 / "V3_METRIC_CROSSWALK.json").read_text(encoding="utf-8"))
    st = xw["data_labels"]["crosswalk_status"]
    chk("D06-INDIRECT-CHANGES-DISTINCT", sum(st.values()) == 6498 and st["ADDED_V3"] == 26,
        {"crosswalk_status": st, "note": "record-level (indirect) changes; reported separately from file-level changes"})
    fx = read_jsonl(V3 / "V2_TO_V3_FILE_CROSSWALK.jsonl")
    imp = read_jsonl(S3 / "V3_CHANGED_FILES_IMPACT.jsonl")
    chk("D07-DIRECT-CHANGES-104-26", len(imp) == sum(1 for x in fx if x["changed_vs_frozen"]) == 104
        and sum(1 for x in imp if x["changed_vs_v2"]) == sum(1 for x in fx if x["changed_vs_v2"]) == 26, {"changed_vs_frozen": len(imp)})
    tally = json.loads((V3 / "FINAL_SUITE_TALLY.json").read_text(encoding="utf-8"))
    chk("D08-SUITE-TALLY-44", len(tally["by_suite"]) == 44 and tally["tally"] == {"NOT_RUN": 32, "PASS": 3416},
        {"suites": len(tally["by_suite"]), "tally": tally["tally"]})
    # extras universe and provenance
    E = ("EXTRA_PRODUCT", "EXTRA_WORKFLOW", "CANONICAL_PLUS_DELTA", "MIXED")
    ex_keys = {r["source_key"] for r in act if r["classification"] in E}
    clusters = json.loads((S3 / "_extras" / "CLUSTERS.json").read_text(encoding="utf-8"))["clusters"]
    members = [m["key"] for c in clusters for m in c["members"]]
    chk("D09-EXTRAS-EVERY-RECORD-ONCE", len(members) == len(set(members)) == len(ex_keys) == 1777 and set(members) == ex_keys,
        {"records": len(members), "unique": len(set(members))})
    pref = collections.Counter(re.match(r"[A-Z0-9]+(?:-NC|-FX)?", k).group(0) for k in members)
    chk("D10-EXTRAS-PROVENANCE-PREFIXES", pref.get("AUG1-NC", 0) + pref.get("AUG1-FX", 0) == 25 and pref.get("V3A", 0) == 20 and pref.get("REP", 0) == 66
        and pref.get("NCP", 0) == 4, dict(pref))
    adj = read_jsonl(V3 / "PASS2_PASS3_ADJUDICATION.jsonl")
    ov = collections.Counter(a["overlay_action"] for a in adj)
    chk("D11-CODEX-PASS23-AS-RECORDED", len(adj) == 211 and ov == collections.Counter({"NONE": 164, "ADD": 29, "APPEND": 18}), dict(ov))
    p1 = RECON / "step1_union_augmented_pass1"
    n_nc = len(read_jsonl(p1 / "NEW_CLAUSE_PROPOSALS.jsonl"))
    n_fx = len(read_jsonl(p1 / "EXISTING_GROUP_FACETS.jsonl"))
    chk("D12-CODEX-PASS1-AS-RECORDED", (n_nc, n_fx) == (26, 29), {"new_clauses": n_nc, "facets": n_fx})
    xrows = read_jsonl(S3 / "EXTRA_OBLIGATIONS_SIX_WAY.jsonl")
    chk("D13-EXTRAS-TOTALS", len(xrows) == 797 and sum(x["n_records"] for x in xrows) == 1777
        and sum(met["universe_extras"]["classes"].values()) == 797, met["universe_extras"]["classes"])
    # no candidate or predecessor change (no Codex edit re-applied, no write outside Step 3)
    hashes = json.loads((S3 / "UPSTREAM_V3_TREE_HASHES.json").read_text(encoding="utf-8"))
    files = hashes.get("files", hashes)
    drift = [p for p, h in files.items() if not (V3 / p).exists() or sha256_file(V3 / p) != h]
    agg = hashlib.sha256("".join(f"{p}\0{files[p]}\n" for p in sorted(files)).encode()).hexdigest()
    fp = json.loads((S3 / "UPSTREAM_FINGERPRINT.json").read_text(encoding="utf-8"))
    chk("D14-V3-TREE-UNCHANGED", not drift, {"files": len(files), "drift": drift[:10], "aggregate_recomputed": agg,
                                             "aggregate_at_preflight": fp["v3_tree"]["aggregate_sha256"]})
    odrift = [p for p, h in fp["other_inputs_sha256"].items() if not (S3.parents[2] / p).exists() or sha256_file(S3.parents[2] / p) != h]
    chk("D15-OTHER-INPUTS-UNCHANGED", not odrift, odrift)
    # internal sums
    pu = met["universe_policies"]["labels"]
    chk("D16-METRIC-SUMS", sum(pu.values()) == 196 and sum(met["universe_cells"]["step3_levels_a_to_d"].values()) == 1176
        and met["universe_differences"]["pair_rows"] == 15 * met["universe_differences"]["material_dims"], {"labels": pu})
    k = len(list((S3 / "VALIDATION_ATTEMPTS").glob("gateD_attempt*"))) + 1
    out = {"gate": "D", "at": datetime.datetime.now().isoformat(timespec="seconds"), "checks": res, "errors": errs}
    write_json_atomic(S3 / "VALIDATION_ATTEMPTS" / f"gateD_attempt{k}_{'PASS' if not errs else 'FAIL'}.json", out)
    if not errs:
        write_json_atomic(S3 / "CHECKPOINTS" / "gates" / "gateD.json", out)
    for n, v in res.items():
        print(n, "OK" if v["ok"] else "FAIL", "" if v["ok"] else json.dumps(v["detail"])[:300])
    print("GATE D", "PASS" if not errs else "FAIL")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
