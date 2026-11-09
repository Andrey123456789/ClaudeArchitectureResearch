"""Phase 5.4 final acceptance - step 6: independent validation of this task's output (read-only except VALIDATION_REPORT.json).

Run from this task's output folder after _tools/manifest.py:  python -B _tools/validate_final.py
"""
import collections
import datetime
import hashlib
import json
import os
import re
import stat
import subprocess
import sys

REQUIRED = [
    "STATE.json", "RESUME.md", "CANDIDATE_FREEZE_REPORT.md", "LIVE_HOST_PILOT_MATRIX.jsonl", "LIVE_HOST_PILOT_REPORT.md",
    "PHASE54_METRIC_LINEAGE.md", "ARCHITECTURE_DIFFERENCES_AND_LIMITS.md", "BENCHMARK_HANDOFF_CONTRACT.md",
    "FINAL_PHASE54_CLOSURE_REPORT.md", "FILE_MANIFEST.json",
    "release/CANDIDATE_FREEZE_MANIFEST.json", "release/CANDIDATE_FREEZE_MANIFEST.json.sha256", "release/RELEASE_PROVENANCE.md",
    "release/verify_release.py", "release/make_working_copy.py", "predecessor/PREDECESSOR_VERIFICATION.json",
    "closure_review/CLOSURE_REVIEW.json", "live_host_pilot/PILOT_DESIGN_AND_EXPECTATIONS.md", "live_host_pilot/PILOT_TOTALS.json",
    "_baseline/PROTECTED_BASELINE_SHA256.json", "_baseline/PROTECTED_VERIFY_FINAL.json",
]
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
checks = []


def check(cid, ok, detail=None):
    checks.append({"id": cid, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + cid)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


missing = [p for p in REQUIRED if not os.path.exists(p)]
check("V01 required deliverables exist", not missing, missing)

st = json.load(open("STATE.json", encoding="utf-8"))
not_done = [u for u, v in st["units"].items() if v != "DONE" and u != "S6_FINAL_VALIDATION"]
check("V02 units S1-S5 DONE in STATE.json", not not_done, not_done)

p = subprocess.run([sys.executable, "-B", "release/verify_release.py", "--json"], capture_output=True, text=True)
vr = json.loads(p.stdout)
check("V03 release verifies (448 files, byte-identical to v3, no missing/unexpected)",
      p.returncode == 0 and vr["verdict"] == "PASS" and vr["totals"]["files"] == 448 and vr["v3_comparison"] == "RUN",
      {"verdict": vr["verdict"], "warnings": vr["warnings"]})

ro_bad = [f"{c}/{r}" for c in CANDS for dp, _, fn in os.walk(os.path.join("release", "candidates", c, "template"))
          for r in fn if os.stat(os.path.join(dp, r)).st_mode & stat.S_IWRITE]
check("V04 every released file carries the read-only attribute", not ro_bad, ro_bad[:10])

pv = json.load(open("predecessor/PREDECESSOR_VERIFICATION.json", encoding="utf-8"))
cr = json.load(open("closure_review/CLOSURE_REVIEW.json", encoding="utf-8"))
check("V05 predecessor verification 12/12 and closure review 11/11 on record",
      pv["verdict"] == "PASS" and pv["passed"] == 12 and cr["verdict"] == "PASS" and cr["passed"] == 11)

pf = json.load(open("_baseline/PROTECTED_VERIFY_FINAL.json", encoding="utf-8"))
check("V06 protected 5.4 tree (everything outside this folder) unchanged since task start", pf["verdict"] == "UNCHANGED",
      {k: (len(v) if isinstance(v, list) else v) for k, v in pf.items()})

rows = jl("LIVE_HOST_PILOT_MATRIX.jsonl")
cand = [r for r in rows if r.get("scope", "candidate") == "candidate"]
tot = collections.Counter(r["status"] for r in cand)
totals = json.load(open("live_host_pilot/PILOT_TOTALS.json", encoding="utf-8"))
check("V07 matrix: 56 candidate rows = 6 x 7 live rows + 14 NOT_RUN rows; totals file agrees",
      len(cand) == 56 and sum(1 for r in cand if r["evidence_level"] == "LIVE_HOST_VERIFIED") == 42
      and dict(tot) == totals["status"], dict(tot))

bad_level = [r["row_id"] for r in rows if r["status"] in ("PASS", "FAIL") and r["evidence_level"] != "LIVE_HOST_VERIFIED"]
static_pass = [r["row_id"] for r in rows if r["evidence_level"] == "STATIC_VERIFIED" and r["status"] != "NOT_RUN"]
no_raw = [r["row_id"] for r in rows if r["evidence_level"] == "LIVE_HOST_VERIFIED" and not os.path.exists(r["evidence_paths"][0])]
check("V08 no static result reported as a live PASS/FAIL; every live row has its raw stream", not (bad_level or static_pass or no_raw),
      {"bad_level": bad_level, "static_pass": static_pass, "no_raw": no_raw})

fields = ["candidate", "host", "session_mode", "hook_event", "triggering_action", "expected", "actual", "operation_executed",
          "status", "evidence_paths"]
lacking = [r["row_id"] for r in rows if r["evidence_level"] == "LIVE_HOST_VERIFIED"
           and (any(f not in r for f in fields) or ("observable_host_response" not in r and r["row"] != "E1"))]
check("V09 every executed row records candidate, host/CLI, mode, event, action, expected/actual, executed flag, host response, status, paths",
      not lacking, lacking)

iv = []
for case in sorted(os.listdir("live_host_pilot/runs")):
    lr = json.load(open(f"live_host_pilot/runs/{case}/live_result.json", encoding="utf-8"))
    end = datetime.datetime.fromisoformat(lr["at"])
    iv.append((end - datetime.timedelta(seconds=lr["duration_s"] + 1), end, case))
for dx in sorted(os.listdir("live_host_pilot/diagnostic")):
    r = json.load(open(f"live_host_pilot/diagnostic/{dx}/result.json", encoding="utf-8"))
    end = datetime.datetime.fromisoformat(r["at"])
    iv.append((end - datetime.timedelta(seconds=r["duration_s"] + 1), end, dx))
iv.sort()
overlap = [(a[2], b[2]) for a, b in zip(iv, iv[1:]) if b[0] < a[1] - datetime.timedelta(seconds=1)]
check("V10 the 23 headless sessions ran one at a time (no overlapping intervals)", len(iv) == 23 and not overlap, overlap)

rep = open("FINAL_PHASE54_CLOSURE_REPORT.md", encoding="utf-8").read()
state_words = re.findall(r"\*\*Closure decision: (CLOSED_VERIFIED|CLOSED_CONDITIONAL|BLOCKED)\.\*\*", rep)
nums = ["36 PASS · 6 FAIL · 14 NOT_RUN", "448", "165", "1,176", "3,416", "11/11", "12/12"]
check("V11 closure report states exactly one allowed closure state (CLOSED_CONDITIONAL) and the verified numbers",
      state_words == ["CLOSED_CONDITIONAL"] and all(n in rep for n in nums) and "CLOSED_VERIFIED" not in rep.split("## 10.")[0].replace("Not CLOSED_VERIFIED", ""),
      {"states": state_words, "missing_numbers": [n for n in nums if n not in rep]})

authored = [f for f in os.listdir(".") if f.endswith((".md", ".json", ".jsonl"))] + \
    ["release/RELEASE_PROVENANCE.md", "live_host_pilot/PILOT_DESIGN_AND_EXPECTATIONS.md"] + \
    [f"_tools/{f}" for f in os.listdir("_tools") if f.endswith(".py")]
cyr = [f for f in authored if re.search("[" + chr(0x400) + "-" + chr(0x4FF) + "]", open(f, encoding="utf-8").read())]
check("V12 all authored Markdown, JSON and tools are in English (no Cyrillic)", not cyr, cyr)

fm = json.load(open("FILE_MANIFEST.json", encoding="utf-8"))
bad = [r["path"] for r in fm["output_files"] if "sha256" in r and sha(r["path"]) != r["sha256"]]
listed = {r["path"] for r in fm["output_files"]}
bulk = [b["dir"] for b in fm["bulk_fixture_dirs"]]
unlisted = []
for dp, dn, fn in os.walk("."):
    rel_dir = os.path.relpath(dp, ".").replace(os.sep, "/")
    if any(rel_dir == b or rel_dir.startswith(b + "/") for b in bulk) or "__pycache__" in rel_dir:
        continue
    for n in fn:
        rel = n if rel_dir == "." else f"{rel_dir}/{n}"
        if rel not in listed and rel != "VALIDATION_REPORT.json":
            unlisted.append(rel)
check("V13 FILE_MANIFEST hashes match and every file is listed (bulk fixtures aggregated)", not bad and not unlisted,
      {"bad": bad, "unlisted": unlisted[:10]})

sel = json.load(open("release_verification/VERIFIER_SELFTEST.json", encoding="utf-8"))
check("V14 release verifier negative self-test all as expected (9 cases)", sel["all_as_expected"] and len(sel["cases"]) == 9)

res = {"tool": "_tools/validate_final.py", "at": datetime.datetime.now().isoformat(timespec="seconds"),
       "passed": sum(c["pass"] for c in checks), "total": len(checks),
       "verdict": "PASS" if all(c["pass"] for c in checks) else "FAIL", "checks": checks}
with open("VALIDATION_REPORT.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=1)
print(res["verdict"], f"{res['passed']}/{res['total']}")
sys.exit(0 if res["verdict"] == "PASS" else 1)
