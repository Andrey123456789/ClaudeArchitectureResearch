"""Phase 5.4 final acceptance - step 4: focused, read-only closure review (CR-01..CR-11).

Run from this task's output folder:  python -B _tools/closure_review.py
Writes closure_review/CLOSURE_REVIEW.json and closure_review/fair02_assembly_check/ (prompt assembly on a placeholder task).
Reads every predecessor read-only. Does not re-run old suites, re-judge cells or redo Codex searches.
"""
import collections
import hashlib
import json
import os
import subprocess
import sys

OUT = os.getcwd()
REC = os.path.normpath(os.path.join(OUT, ".."))
STAGE_A = os.path.normpath(os.path.join(REC, ".."))
V3 = os.path.join(REC, "step2_controlled_repair_v3")
S3 = os.path.join(REC, "step3_six_way_strictness_v1")
K76 = os.path.join(REC, "benchmark_readiness_fair02_cp01_v1")
REL = os.path.join(OUT, "release")
CR = os.path.join(OUT, "closure_review")
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]


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


checks = []


def check(cid, ok, detail):
    checks.append({"id": cid, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + cid)


os.makedirs(CR, exist_ok=True)
man = jload(os.path.join(REL, "CANDIDATE_FREEZE_MANIFEST.json"))
v3man = jload(os.path.join(V3, "V3_FINAL_MANIFEST.json"))

# CR-01 release byte-identical to v3 (independent verifier, v3 comparison on)
p = subprocess.run([sys.executable, "-B", os.path.join(REL, "verify_release.py"), "--json"], capture_output=True, text=True)
vr = json.loads(p.stdout)
with open(os.path.join(CR, "VERIFY_RELEASE_AT_CLOSURE.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(vr, f, indent=1)
check("CR-01 six released candidates byte-identical to the approved v3 templates (verify_release.py, v3 comparison run)",
      p.returncode == 0 and vr["verdict"] == "PASS" and vr["v3_comparison"] == "RUN" and vr["totals"]["files"] == 448,
      {"verdict": vr["verdict"], "files": vr["totals"]["files"], "warnings": vr["warnings"]})

# CR-02 approved decisions preserved
instr = open(os.path.join(K76, "fair02", "RUN_REPORT_INSTRUCTION.txt"), encoding="utf-8").read()
probe = "produce a final report titled `Run Report`"
embedded = []
for c in CANDS:
    root = os.path.join(REL, "candidates", c, "template")
    for rel in man["candidates"][c]["files"]:
        try:
            if probe in open(os.path.join(root, rel), encoding="utf-8").read():
                embedded.append(f"{c}/{rel}")
        except UnicodeDecodeError:
            pass
settings_same = all(man["candidates"][c]["files"][".claude/settings.json"]["sha256"] ==
                    v3man["candidates"][c]["files"][".claude/settings.json"]["sha256"] for c in CANDS)
m_props = open(os.path.join(REL, "candidates", "M", "template", "Directory.Build.props"), encoding="utf-8").read()
m_files_same = all(v["sha256"] == v3man["candidates"]["M"]["files"][k]["sha256"] for k, v in man["candidates"]["M"]["files"].items())
check("CR-02 decisions preserved: FAIR-01 (hook settings and all files unchanged), FAIR-02 (instruction hash; not embedded in any template), CP-01 (M unchanged, no GenerateDocumentationFile)",
      settings_same and not embedded and sha(os.path.join(K76, "fair02", "RUN_REPORT_INSTRUCTION.txt")).startswith("bb17a883")
      and "GenerateDocumentationFile" not in m_props and m_files_same and instr.startswith("At the end of this run"),
      {"settings_json_unchanged_all_six": settings_same, "instruction_embedded_in_templates": embedded,
       "M_all_files_equal_v3": m_files_same})

# CR-03 Step 3 comparison and metric lineage refer to the released version
up = jload(os.path.join(S3, "UPSTREAM_V3_TREE_HASHES.json"))
bad = [f"{c}/{rel}" for c in CANDS for rel, v in man["candidates"][c]["files"].items()
       if up.get(f"candidates/{c}/template/{rel}") != v["sha256"]]
fp = jload(os.path.join(S3, "UPSTREAM_FINGERPRINT.json"))
check("CR-03 Step 3 input hashes equal every released file; release manifest pins Step 3 METRICS/matrix/cell index",
      not bad and man["policy_data_version"]["step3_metrics_sha256"] == sha(os.path.join(S3, "METRICS.json"))
      and man["policy_data_version"]["step3_policy_cell_index_sha256"] == sha(os.path.join(S3, "POLICY_CELL_INDEX.jsonl"))
      and man["policy_data_version"]["step3_upstream_v3_tree_aggregate_sha256"] == fp["v3_tree"]["aggregate_sha256"],
      {"released_files_not_in_step3_input": bad})

# CR-04 Codex passes 0001-0003 accounted for
CODEX = os.path.join(STAGE_A, "codex_iterative_search")
nf, uf = jl(os.path.join(CODEX, "NOVEL_FINDINGS.jsonl")), jl(os.path.join(CODEX, "UNRESOLVED_FINDINGS.jsonl"))
p1 = {r["id"] for r in nf + uf if r["discovery_pass"] == 1}
p23 = {r["id"] for r in nf + uf if r["discovery_pass"] in (2, 3)}
ledger1 = {r["claim_id"] for r in jl(os.path.join(REC, "step1_union_augmented_pass1", "PASS1_REVIEW_LEDGER.jsonl"))}
adj = {r["codex_id"] for r in jl(os.path.join(V3, "PASS2_PASS3_ADJUDICATION.jsonl"))}
passes = sorted(os.listdir(os.path.join(CODEX, "PASSES")))
check("CR-04 Codex Passes 0001-0003: every finding has a review/adjudication row (Pass 1 ledger, v3 Pass 2+3 adjudication)",
      p1 <= ledger1 and p23 == adj and passes == ["pass_0001", "pass_0002", "pass_0003"],
      {"passes": passes, "pass1_findings": len(p1), "pass1_ledger": len(ledger1), "pass23_findings": len(p23), "pass23_adjudicated": len(adj)})

# CR-05 1,176 canonical cell identifiers traceable
ci = {(r["policy_id"], r["candidate"]) for r in jl(os.path.join(S3, "POLICY_CELL_INDEX.jsonl"))}
cov = {(r["policy_id"], r["candidate"]) for r in jl(os.path.join(V3, "REPAIRED_POLICY_COVERAGE.jsonl"))}
prim = {(r["rule_id"], c) for c in CANDS for r in jl(os.path.join(STAGE_A, "primary", c, "policies.jsonl"))}
check("CR-05 1,176 (policy, candidate) cells identical in primary extraction, v3 coverage, Step 3 cell index; all six released",
      ci == cov == prim and len(ci) == 1176 and {c for _, c in ci} == set(man["candidates"]),
      {"cells": len(ci)})

# CR-06 extras and enforcement differences kept out of canonical counts
mx = jl(os.path.join(S3, "POLICY_SIX_WAY_MATRIX.jsonl"))
metrics = jload(os.path.join(S3, "METRICS.json"))
roots = jload(os.path.join(S3, "EXTRA_GENUINE_ROOTS.json"))
canon_ids = {r["policy_id"] for r in mx}
extras = jl(os.path.join(S3, "EXTRA_OBLIGATIONS_SIX_WAY.jsonl"))
extra_ids_in_canon = sorted({e.get("cluster_id") or e.get("id") for e in extras} & canon_ids)
lab = collections.Counter(r["label"] for r in mx)
check("CR-06 canonical universe stays 196 policies / 1,176 cells; 797 extras clusters and 11 material enforcement roots are separate universes",
      len(canon_ids) == 196 and sum(lab.values()) == 196 and len(extras) == 797 and not extra_ids_in_canon
      and metrics["universe_extras"]["clusters"] == 797 and metrics["universe_cells"]["n"] == 1176
      and metrics["universe_differences"]["policy_level_roots_material"] == 11,
      {"labels": dict(lab), "extras_clusters": len(extras), "extras_ids_colliding_with_policy_ids": extra_ids_in_canon,
       "genuine_roots_file_keys": list(roots)[:5]})

# CR-07 reporting contract identical for all six (prompt assembly on a placeholder task)
ac = os.path.join(CR, "fair02_assembly_check")
os.makedirs(ac, exist_ok=True)
task = os.path.join(ac, "PLACEHOLDER_TASK.txt")
with open(task, "w", encoding="utf-8", newline="\n") as f:
    f.write("PLACEHOLDER benchmark task prompt (identical for all six candidates).\n")
p = subprocess.run([sys.executable, "-B", os.path.join(K76, "fair02", "assemble_prompt.py"), "--task", task, "--out-dir",
                    os.path.join(ac, "out")], capture_output=True, text=True)
outs = {c: sha(os.path.join(ac, "out", f"{c}.prompt.txt")) for c in CANDS if os.path.exists(os.path.join(ac, "out", f"{c}.prompt.txt"))}
ends = all(open(os.path.join(ac, "out", f"{c}.prompt.txt"), "rb").read().endswith(open(os.path.join(K76, "fair02", "RUN_REPORT_INSTRUCTION.txt"), "rb").read()) for c in outs)
check("CR-07 FAIR-02 instruction assembles byte-identically for all six and ends each prompt verbatim; absent from templates",
      p.returncode == 0 and len(outs) == 6 and len(set(outs.values())) == 1 and ends and not embedded,
      {"assemble_exit": p.returncode, "prompt_sha256": sorted(set(outs.values())), "stderr": p.stderr[-300:]})

# CR-08 NOT_RUN limitations explicit (predecessor NOT_RUN carried; pilot NOT_RUN rows present)
tally = jload(os.path.join(V3, "FINAL_SUITE_TALLY.json"))
nr = sum(t.get("NOT_RUN", 0) for t in tally["by_suite"].values())
matrix = jl(os.path.join(OUT, "LIVE_HOST_PILOT_MATRIX.jsonl"))
nr_rows = [r["row_id"] for r in matrix if r["status"] == "NOT_RUN"]
lim_files = {"v3 EVIDENCE_LIMITS.md": os.path.exists(os.path.join(V3, "EVIDENCE_LIMITS.md")),
             "Step 3 METRIC_LINEAGE_AND_LIMITS.md": os.path.exists(os.path.join(S3, "METRIC_LINEAGE_AND_LIMITS.md"))}
check("CR-08 NOT_RUN kept explicit: v3 32 NOT_RUN suite checks on record; pilot NOT_RUN rows present (interactive, malformed live, timeouts)",
      nr == 32 and any(r.startswith("ALL-I") for r in nr_rows) and any(r.endswith("-D2") for r in nr_rows) and all(lim_files.values()),
      {"v3_suite_not_run": nr, "pilot_not_run_rows": nr_rows, "limit_files": lim_files})

# CR-09 CP-01 reproduction preserved, M not modified
fm = jload(os.path.join(K76, "FILE_MANIFEST.json"))
cp_bad = [r["path"] for r in fm["output_files"] if r["path"].startswith("cp01/") and r.get("sha256") and sha(os.path.join(K76, r["path"])) != r["sha256"]]
cp_n = len([r for r in fm["output_files"] if r["path"].startswith("cp01/")])
check("CR-09 CP-01 evidence files unchanged (kit 76 manifest); M template byte-identical to v3; no GenerateDocumentationFile in M",
      not cp_bad and cp_n > 0 and m_files_same and "GenerateDocumentationFile" not in m_props,
      {"cp01_files": cp_n, "changed": cp_bad})

# CR-10 pilot findings traceable to execution evidence
missing, untraced = [], []
for r in matrix:
    if r["evidence_level"] != "LIVE_HOST_VERIFIED":
        continue
    for pth in r["evidence_paths"]:
        if not os.path.exists(os.path.join(OUT, pth)):
            missing.append(pth)
    if r["row"] != "E1":
        line = r["transcript_excerpt"]["tool_use_line"]
        ev = open(os.path.join(OUT, r["evidence_paths"][0]), encoding="utf-8").read().splitlines()[line - 1]
        if r["transcript_excerpt"]["command"] not in ev:
            untraced.append(r["row_id"])
live_rows = [r for r in matrix if r["evidence_level"] == "LIVE_HOST_VERIFIED"]
check("CR-10 every LIVE_HOST_VERIFIED row points to existing raw evidence; each command row's tool_use line contains the command",
      live_rows and not missing and not untraced, {"live_rows": len(live_rows), "missing_paths": missing, "untraced": untraced})

# CR-11 release folder holds only the approved snapshot and its utilities
top = sorted(os.listdir(REL))
expected_top = sorted(["CANDIDATE_FREEZE_MANIFEST.json", "CANDIDATE_FREEZE_MANIFEST.json.sha256", "RELEASE_PROVENANCE.md",
                       "candidates", "make_working_copy.py", "verify_release.py"])
check("CR-11 release/ contains only the snapshot, its manifest, provenance and two utilities; no unapproved modification",
      top == expected_top and sorted(os.listdir(os.path.join(REL, "candidates"))) == sorted(CANDS) and vr["verdict"] == "PASS",
      {"release_top": top})

res = {"tool": "_tools/closure_review.py", "mode": "read-only toward predecessors and release",
       "passed": sum(c["pass"] for c in checks), "total": len(checks),
       "verdict": "PASS" if all(c["pass"] for c in checks) else "DISCREPANCY", "checks": checks}
with open(os.path.join(CR, "CLOSURE_REVIEW.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=1)
print(res["verdict"], f"{res['passed']}/{res['total']}")
sys.exit(0 if res["verdict"] == "PASS" else 1)
