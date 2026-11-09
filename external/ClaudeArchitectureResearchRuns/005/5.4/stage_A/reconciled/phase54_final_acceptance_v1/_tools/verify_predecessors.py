"""Phase 5.4 final acceptance - step 1: read-only verification of the completed predecessors.

Run from this task's output folder:  python -B _tools/verify_predecessors.py
Writes predecessor/PREDECESSOR_VERIFICATION.json. Opens every predecessor file read-only.
It checks machine-readable records against the numbers the task brief cites; it does not
re-run old suites or re-judge the 1,176 semantic cells.
"""
import collections
import hashlib
import json
import os
import sys

OUT = os.getcwd()
REC = os.path.normpath(os.path.join(OUT, ".."))
STAGE_A = os.path.normpath(os.path.join(REC, ".."))
V3 = os.path.join(REC, "step2_controlled_repair_v3")
S3 = os.path.join(REC, "step3_six_way_strictness_v1")
K76 = os.path.join(REC, "benchmark_readiness_fair02_cp01_v1")
CODEX = os.path.join(STAGE_A, "codex_iterative_search")
P1 = os.path.join(REC, "step1_union_augmented_pass1")
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
FAIR02_REQUIRED = ["RUN_REPORT_INSTRUCTION.txt", "BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md", "INTEGRATION_CONTRACT.md",
                   "REPORT_COMPLETENESS_RUBRIC.md", "RUN_EVIDENCE_SCHEMA.md", "assemble_prompt.py", "score_report.py"]
MATERIAL_ROOTS_EXPECTED = 11


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jload(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def walk(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for n in sorted(fn):
            p = os.path.join(dp, n)
            out[os.path.relpath(p, root).replace(os.sep, "/")] = sha(p)
    return out


checks = []


def check(cid, ok, detail):
    checks.append({"id": cid, "pass": bool(ok), "detail": detail})


# PV-01 Step 2 v3 completion state and suite tally
st = jload(os.path.join(V3, "STATE.json"))
tally = jload(os.path.join(V3, "FINAL_SUITE_TALLY.json"))
tot = collections.Counter()
for suite, t in tally["by_suite"].items():
    tot.update(t)
check("PV-01 v3 COMPLETE, PASS_WITH_DOCUMENTED_NOT_RUN, 3,416 PASS / 0 FAIL / 32 NOT_RUN over 44 suites",
      st["phase"] == "COMPLETE" and st["result"]["status"] == "PASS_WITH_DOCUMENTED_NOT_RUN"
      and tot.get("PASS") == 3416 and tot.get("FAIL", 0) == 0 and tot.get("NOT_RUN") == 32 and len(tally["by_suite"]) == 44
      and st["last_gate"]["tally"] == {"NOT_RUN": 32, "PASS": 3416},
      {"phase": st["phase"], "result": st["result"]["status"], "suites": len(tally["by_suite"]), "tally": dict(tot),
       "checkpoints": st["checkpoints"], "cold_audit": st["cold_audit"]["tally"]})

# PV-02 V3_FINAL_MANIFEST equals the candidate trees on disk
man = jload(os.path.join(V3, "V3_FINAL_MANIFEST.json"))
per = {}
ok = man["version"] == "step2-controlled-repair-v3" and sorted(man["candidates"]) == sorted(CANDS)
for c in CANDS:
    m = {k: v["sha256"] for k, v in man["candidates"][c]["files"].items()}
    d = walk(os.path.join(V3, "candidates", c, "template"))
    bad = sorted(k for k in m if k in d and d[k] != m[k])
    miss, extra = sorted(set(m) - set(d)), sorted(set(d) - set(m))
    per[c] = {"n_files": len(m), "declared": man["candidates"][c]["n_files"], "missing": miss, "extra": extra, "mismatch": bad}
    ok = ok and not (bad or miss or extra) and len(m) == man["candidates"][c]["n_files"]
check("PV-02 V3_FINAL_MANIFEST matches all six template trees byte for byte (448 files)",
      ok and sum(v["n_files"] for v in per.values()) == 448,
      {"manifest_sha256": sha(os.path.join(V3, "V3_FINAL_MANIFEST.json")), "manifest_at": man["at"], "per_candidate": per})

# PV-03 Step 3 completion state and validation
s3 = jload(os.path.join(S3, "STATE.json"))
s3v = jload(os.path.join(S3, "VALIDATION_REPORT.json"))
check("PV-03 Step 3 COMPLETE, verdict CONDITIONAL_GO, gate E PASS",
      s3["status"] == "COMPLETE" and s3["verdict"] == "CONDITIONAL_GO" and s3v["status"] == "PASS" and not s3v["failed"],
      {"status": s3["status"], "verdict": s3["verdict"], "gate_e": s3v["status"], "gate_e_attempt": s3v["attempt"]})

# PV-04 Step 3 label counts recomputed from the matrix and the cell index
mx = jl(os.path.join(S3, "POLICY_SIX_WAY_MATRIX.jsonl"))
ci = jl(os.path.join(S3, "POLICY_CELL_INDEX.jsonl"))
metrics = jload(os.path.join(S3, "METRICS.json"))
labels = collections.Counter(r["label"] for r in mx)
pids = [r["policy_id"] for r in mx]
cells = collections.Counter((r["policy_id"], r["candidate"]) for r in ci)
levels = collections.Counter(r["step3_level"] for r in ci)
check("PV-04 Step 3 196 policies -> 165 FULL / 16 PARTIAL / 15 MEANINGFUL; 1,176 unique cells all FULL_SOURCE_COMPARED",
      len(mx) == 196 and len(set(pids)) == 196 and labels == collections.Counter(
          {"FULL_SEMANTIC_PARITY": 165, "PARTIAL_PARITY_WITH_DELTA": 16, "MEANINGFUL_DIVERGENCE": 15})
      and len(ci) == 1176 and len(cells) == 1176 and max(cells.values()) == 1
      and set(c for _, c in cells) == set(CANDS) and set(p for p, _ in cells) == set(pids)
      and levels == collections.Counter({"FULL_SOURCE_COMPARED": 1176})
      and metrics["universe_policies"]["labels"]["FULL_SEMANTIC_PARITY"] == 165,
      {"labels": dict(labels), "cells": len(ci), "unique_cells": len(cells), "levels": dict(levels)})

# PV-05 eleven material enforcement roots
rcs = jload(os.path.join(S3, "ROOT_CAUSE_SUMMARY.json"))["policy_level"]
mat = sorted(k for k, v in rcs.items() if v["material"])
mat_axes = {k: rcs[k]["axes"] for k in mat}
check("PV-05 Step 3 material roots = 11, all on the ENFORCEMENT axis",
      len(mat) == MATERIAL_ROOTS_EXPECTED and all(a == ["ENFORCEMENT"] for a in mat_axes.values())
      and metrics["universe_differences"]["policy_level_roots_material"] == 11
      and metrics["universe_differences"]["by_axis_material"].get("ENFORCEMENT/material") == 15,
      {"material_roots": mat, "policy_level_roots": len(rcs)})

# PV-06 Step 3 compared exactly the v3 version: its recorded tree hashes equal the final manifest and the current v3 tree
up = jload(os.path.join(S3, "UPSTREAM_V3_TREE_HASHES.json"))
tmpl_mismatch = []
for c in CANDS:
    for rel, v in man["candidates"][c]["files"].items():
        key = f"candidates/{c}/template/{rel}"
        if up.get(key) != v["sha256"]:
            tmpl_mismatch.append(key)
up_tmpl = [k for k in up if k.startswith("candidates/") and "/template/" in k]
now_v3 = walk(V3)
drift = sorted(k for k in up if now_v3.get(k) != up[k])
new = sorted(set(now_v3) - set(up))
check("PV-06 Step 3 input fingerprint = V3_FINAL_MANIFEST template hashes = current v3 tree (8,698 files, no drift)",
      not tmpl_mismatch and len(up_tmpl) == 448 and not drift and not new and len(up) == 8698,
      {"upstream_files": len(up), "upstream_template_files": len(up_tmpl), "template_mismatch": tmpl_mismatch,
       "v3_now": len(now_v3), "drift": drift, "new_since_step3": new})

# PV-07 1,176 cell identifiers traceable across v3 and Step 3 (and the original extraction universe)
rc = jl(os.path.join(V3, "REPAIRED_POLICY_COVERAGE.jsonl"))
pm = jl(os.path.join(V3, "POLICY_PARITY_MATRIX.jsonl"))
prim = []
for c in CANDS:
    p = os.path.join(STAGE_A, "primary", c, "policies.jsonl")
    for r in jl(p):
        prim.append((r["rule_id"], c))
set_ci, set_rc, set_pm, set_pr = set(cells), {(r["policy_id"], r["candidate"]) for r in rc}, \
    {(r["policy_id"], r["candidate"]) for r in pm}, set(prim)
check("PV-07 the same 1,176 (policy, candidate) identifiers in primary extraction, v3 coverage, v3 parity matrix, Step 3 cell index",
      set_ci == set_rc == set_pm == set_pr and len(set_ci) == 1176 and len(prim) == 1176,
      {"step3_cell_index": len(set_ci), "v3_repaired_coverage": len(set_rc), "v3_parity_matrix": len(set_pm),
       "primary_extraction_rows": len(prim), "primary_unique": len(set_pr),
       "step3_only": sorted(set_ci - set_pr), "primary_only": sorted(set_pr - set_ci)})

# PV-08 Codex passes 0001-0003 accounted for
cst = jload(os.path.join(CODEX, "STATE.json"))
nf, uf = jl(os.path.join(CODEX, "NOVEL_FINDINGS.jsonl")), jl(os.path.join(CODEX, "UNRESOLVED_FINDINGS.jsonl"))
samples = jl(os.path.join(CODEX, "ALREADY_COVERED_SAMPLES.jsonl"))
p1_ids = {r["id"] for r in nf + uf if r["discovery_pass"] == 1}
p23_ids = {r["id"] for r in nf + uf if r["discovery_pass"] in (2, 3)}
ledger1 = {r["claim_id"] for r in jl(os.path.join(P1, "PASS1_REVIEW_LEDGER.jsonl"))}
adj23 = {r["codex_id"] for r in jl(os.path.join(V3, "PASS2_PASS3_ADJUDICATION.jsonl"))}
sample_ids = {r["id"] for r in samples}
by_pass = collections.Counter(r["discovery_pass"] for r in nf + uf)
check("PV-08 Codex Pass 1 (132 findings + 20 samples = 152 ledger rows) and Pass 2+3 (211 = 211 adjudicated) fully accounted",
      cst["last_completed_pass"] == 3 and not cst["pass_0004_started"] and p1_ids <= ledger1
      and ledger1 - p1_ids <= sample_ids and len(ledger1) == 152 and p23_ids == adj23 and len(adj23) == 211,
      {"codex_final_status": cst["final_status"], "by_pass": dict(by_pass), "pass1_ledger": len(ledger1),
       "pass1_findings": len(p1_ids), "pass1_samples_in_ledger": len(ledger1 - p1_ids),
       "pass23_findings": len(p23_ids), "pass23_adjudicated": len(adj23),
       "pass1_validation": jload(os.path.join(P1, "VALIDATION_RESULT.json"))["result"]})

# PV-09 kit 76 completion, validation and manifest integrity
k = jload(os.path.join(K76, "STATE.json"))
kv = jload(os.path.join(K76, "VALIDATION_REPORT.json"))
fm = jload(os.path.join(K76, "FILE_MANIFEST.json"))
bad = []
for row in fm["output_files"]:
    p = os.path.join(K76, row["path"])
    if row.get("sha256") and (not os.path.exists(p) or sha(p) != row["sha256"]):
        bad.append(row["path"])
check("PV-09 kit 76 COMPLETE, validator 22/22, FILE_MANIFEST hashes match",
      k["status"] == "COMPLETE" and all(v == "DONE" for v in k["units"].values()) and kv["verdict"] == "PASS"
      and kv["passed"] == kv["total"] == 22 and not bad,
      {"status": k["status"], "validator": f'{kv["passed"]}/{kv["total"]}', "manifest_rows": len(fm["output_files"]), "bad": bad})

# PV-10 FAIR-02 contract files present and instruction pinned
prov = jload(os.path.join(K76, "fair02", "RUN_REPORT_INSTRUCTION.provenance.json"))
f02 = {n: sha(os.path.join(K76, "fair02", n)) for n in FAIR02_REQUIRED if os.path.exists(os.path.join(K76, "fair02", n))}
check("PV-10 FAIR-02: seven contract files present; RUN_REPORT_INSTRUCTION.txt sha256 = provenance bb17a883...",
      len(f02) == 7 and f02["RUN_REPORT_INSTRUCTION.txt"] == prov["instruction_sha256"]
      and prov["instruction_sha256"].startswith("bb17a883"),
      {"files": f02, "provenance_sha256": prov["instruction_sha256"]})

# PV-11 CP-01 result preserved
ov = jload(os.path.join(K76, "cp01", "OBSERVED_VS_EXPECTED.json"))
rows = ov["replica_rows"]
def ide(row):
    return row.get("ide0005_count_python")
sdks = sorted({r.get("sdk_msbuild_NETCoreSdkVersion") for r in rows if r.get("sdk_msbuild_NETCoreSdkVersion")})
summary = [{"source": r["source"], "case": r["case"], "candidate": r.get("candidate"), "kind": r.get("kind"),
            "exit": r.get("exit_code"), "ide0005": ide(r)} for r in rows]
key = {(r["source"], r["case"]): r for r in summary}
cp_ok = all(key[(run, "A_M_as_is")]["ide0005"] == 0 and key[(run, "C_L0_as_is")]["ide0005"] > 0
            and key[(run, "F_M_format_style")]["exit"] == 2 and key[(run, "V_M_verify_format")]["exit"] == 2
            for run in ("replica_harness_run1", "replica_harness_run2"))
check("PV-11 CP-01 on SDK 10.0.403: M build no IDE0005, L0 build IDE0005, M dotnet format exit 2; replicates identical",
      sdks == ["10.0.403"] and cp_ok and ov["replicates_identical"] and ov["all_predeclared_expectations_met"]
      and ov["all_parsers_agree"], {"sdk": sdks, "rows": summary})

# PV-12 M template still lacks GenerateDocumentationFile (CP-01 option 0, no unauthorized change)
mprops = open(os.path.join(V3, "candidates", "M", "template", "Directory.Build.props"), encoding="utf-8").read()
l0props = open(os.path.join(V3, "candidates", "L0", "template", "Directory.Build.props"), encoding="utf-8").read()
check("PV-12 M Directory.Build.props has no GenerateDocumentationFile; L0 has it (CP-01 state preserved)",
      "GenerateDocumentationFile" not in mprops and "GenerateDocumentationFile" in l0props,
      {"M_props_sha256": sha(os.path.join(V3, "candidates", "M", "template", "Directory.Build.props")),
       "M_editorconfig_sha256": sha(os.path.join(V3, "candidates", "M", "template", ".editorconfig"))})

result = {"tool": "_tools/verify_predecessors.py", "mode": "read-only",
          "passed": sum(c["pass"] for c in checks), "total": len(checks),
          "verdict": "PASS" if all(c["pass"] for c in checks) else "DISCREPANCY", "checks": checks}
os.makedirs(os.path.join(OUT, "predecessor"), exist_ok=True)
with open(os.path.join(OUT, "predecessor", "PREDECESSOR_VERIFICATION.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, indent=1)
for c in checks:
    print(("PASS " if c["pass"] else "FAIL ") + c["id"])
print(result["verdict"], f'{result["passed"]}/{result["total"]}')
sys.exit(0 if result["verdict"] == "PASS" else 1)
