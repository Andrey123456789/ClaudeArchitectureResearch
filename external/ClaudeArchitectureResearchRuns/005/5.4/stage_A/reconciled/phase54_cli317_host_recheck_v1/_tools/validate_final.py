"""Final validation of the CLI 2.1.317 recheck. Writes VALIDATION_REPORT.json and FILE_MANIFEST.json. Exit code 0 = all checks PASS.

Usage: python -B validate_final.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.normpath(os.path.join(OUT, "..", "phase54_final_acceptance_v1"))
TOOLS = os.path.join(OUT, "_tools")
DELIV = ["CLI317_RECHECK_MATRIX.jsonl", "CLI317_RECHECK_REPORT.md", "CLI_VERSION_AND_HASH.md", "PHASE54_CLOSURE_ADDENDUM.md", "STATE.json", "RESUME.md", "DESIGN_AND_EXPECTATIONS.md", "DESIGN_AMENDMENTS.md", "RECHECK_TOTALS.json", "RAW_EVIDENCE_AUDIT.json"]
DESIGN_SHA = "ed1e0e9c89dee459ffedf0715ab1994863e6974216dc85a21a486ca2e685ed19"
checks = []


def check(cid, ok, detail=None):
    checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    missing = [d for d in DELIV if not os.path.isfile(os.path.join(OUT, d))]
    check("V01_deliverables_present", not missing, {"missing": missing})

    rows = [json.loads(x) for x in open(os.path.join(OUT, "CLI317_RECHECK_MATRIX.jsonl"), encoding="utf-8") if x.strip()]
    totals = json.load(open(os.path.join(OUT, "RECHECK_TOTALS.json"), encoding="utf-8"))
    eff = [r for r in rows if r["effective"]]
    check("V02_every_row_classified", all(r["status"] in ("PASS", "FAIL", "NOT_RUN") for r in rows), {"rows": len(rows)})
    check("V03_totals_match_matrix", len(rows) == totals["rows_total"] and len(eff) == totals["effective_rows"], {"rows": len(rows), "effective": len(eff)})
    keys = [r["row_key"] for r in rows]
    check("V04_row_keys_unique", len(keys) == len(set(keys)))
    bad = [r["row_key"] for r in rows if r.get("evidence_level") == "LIVE_HOST_VERIFIED" and not (r.get("cli_version_from_init") == "2.1.317" and r.get("session_mode", "").startswith("LIVE_HOST") and os.path.isfile(os.path.join(OUT, "runs", r["folder"], "stdout.jsonl")))]
    check("V05_live_verified_only_with_a_recorded_2_1_317_session", not bad, {"bad": bad})
    bad = [r["row_key"] for r in rows if r["status"] == "PASS" and r.get("evidence_level") != "LIVE_HOST_VERIFIED"]
    check("V06_no_pass_without_live_evidence", not bad, {"bad": bad})
    check("V07_no_effective_fail", not [r for r in eff if r["status"] == "FAIL"], {"effective_by_status": totals["effective_by_status"]})
    bad = [r["row_key"] for r in rows if r["status"] == "FAIL" and "TEST_HARNESS" not in r.get("failure_attribution", "")]
    check("V08_every_fail_attributed", not bad, {"fails": [r["row_key"] for r in rows if r["status"] == "FAIL"], "unattributed": bad})
    fields = ("triggering_action", "expected", "actual", "operation_executed", "session_exit_code", "session_started_at", "session_finished_at", "evidence_paths", "host_events", "tool_result_excerpt", "process_stderr_excerpt")
    bad = [r["row_key"] for r in eff if r.get("case") and r["status"] != "NOT_RUN" and not r["row_id"].endswith("-E1") and any(f not in r for f in fields)]
    check("V09_required_fields_present", not bad, {"bad": bad})
    d1 = {r["row_id"]: r for r in eff if r.get("row_id", "").endswith(("-D1", "-D1M"))}
    cands = ["M", "M1", "L0", "L1", "K0", "K1"]
    ok = all(d1.get(f"{c}-{s}", {}).get("status") == "PASS" and d1[f"{c}-{s}"]["attempt"] == 2 and d1[f"{c}-{s}"]["operation_executed"] is False for c in cands for s in ("D1", "D1M"))
    check("V10_six_d1_reproductions_pass_on_attempt_2", ok)

    a = json.load(open(os.path.join(OUT, "RAW_EVIDENCE_AUDIT.json"), encoding="utf-8"))
    check("V11_raw_audit_all_pass", a["fail"] == 0 and a["pass"] == 8, {"pass": a["pass"], "fail": a["fail"]})
    check("V12_design_hash_unchanged", sha(os.path.join(OUT, "DESIGN_AND_EXPECTATIONS.md")) == DESIGN_SHA)
    r = run([sys.executable, "-B", os.path.join(PRED, "release", "verify_release.py")])
    check("V13_frozen_release_verifies", r.returncode == 0 and "PASS (448 files" in r.stdout, {"last_line": r.stdout.strip().splitlines()[-1]})
    r = run([sys.executable, "-B", os.path.join(TOOLS, "protect_snapshot.py"), "verify", "PROTECTED_VERIFY_FINAL"])
    v = json.load(open(os.path.join(OUT, "_baseline", "PROTECTED_VERIFY_FINAL.json"), encoding="utf-8"))
    check("V14_predecessors_unchanged_since_task_baseline", v["verdict"] == "UNCHANGED", {"files": v["current_files"]})
    r = run([sys.executable, "-B", os.path.join(TOOLS, "protect_snapshot.py"), "manifest-check"])
    m = json.load(open(os.path.join(OUT, "_baseline", "PREDECESSOR_MANIFEST_CHECK.json"), encoding="utf-8"))
    check("V15_final_acceptance_matches_its_manifest", m["verdict"] == "MATCH", {"entries": m["output_file_entries"]})
    c = json.load(open(os.path.join(OUT, "_baseline", "COMPARE_WITH_PRIOR_KIT_BASELINE.json"), encoding="utf-8"))
    check("V16_rest_of_project_matches_prior_baseline", not c["changed"] and not c["removed"] and c["added"] == [".claude/settings.local.json"], {"prior_files": c["prior_kit_baseline_files"], "added": c["added"]})
    entries = sorted(os.listdir(os.path.join(PRED, "release")))
    check("V17_no_stray_entries_in_release", entries == sorted(["CANDIDATE_FREEZE_MANIFEST.json", "CANDIDATE_FREEZE_MANIFEST.json.sha256", "RELEASE_PROVENANCE.md", "candidates", "make_working_copy.py", "verify_release.py"]), {"entries": entries})
    closure = open(os.path.join(PRED, "FINAL_PHASE54_CLOSURE_REPORT.md"), encoding="utf-8").read()
    check("V18_original_closure_report_not_rewritten", "**Closure decision: CLOSED_CONDITIONAL.**" in closure and "2.1.317" not in closure)
    text = {d: open(os.path.join(OUT, d), encoding="utf-8").read() for d in DELIV if d.endswith(".md")}
    add = text["PHASE54_CLOSURE_ADDENDUM.md"]
    check("V19_addendum_is_append_only_and_states_recommendation", "Append-only" in add and "CLOSED_VERIFIED" in add and "CLI 2.1.317" in add)
    cyr = {d: len(re.findall("[Ѐ-ӿ]", t)) for d, t in text.items()}
    check("V20_reports_in_english", not any(cyr.values()), cyr)
    pyc = [os.path.join(d, x) for d, ds, _ in os.walk(OUT) for x in ds if x == "__pycache__" and ".git" not in d and "work" not in d]
    check("V21_no_bytecode_written_by_tools", not pyc, {"found": pyc[:5]})

    res = {"checks": checks, "pass": sum(x["status"] == "PASS" for x in checks), "fail": sum(x["status"] == "FAIL" for x in checks)}
    with open(os.path.join(OUT, "VALIDATION_REPORT.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
        f.write("\n")

    files, bulk = [], []
    for d, ds, fs in os.walk(OUT):
        rel = os.path.relpath(d, OUT).replace(os.sep, "/")
        parts = rel.split("/")
        if len(parts) >= 3 and parts[0] in ("runs", "static_precheck") and parts[2] in ("work", "tmp", "npm-cache", "nuget-packages", "shim"):
            if len(parts) == 3:
                h = hashlib.sha256()
                n = 0
                for dd, dds, ffs in os.walk(d):
                    dds.sort()
                    for x in sorted(ffs):
                        p = os.path.join(dd, x)
                        h.update(os.path.relpath(p, d).replace(os.sep, "/").encode("utf-8"))
                        h.update(sha(p).encode("ascii"))
                        n += 1
                bulk.append({"dir": rel, "files": n, "tree_sha256": h.hexdigest()})
            ds[:] = []
            continue
        for x in sorted(fs):
            if rel == "." and x == "FILE_MANIFEST.json":
                continue
            p = os.path.join(d, x)
            files.append({"path": os.path.relpath(p, OUT).replace(os.sep, "/"), "bytes": os.path.getsize(p), "sha256": sha(p)})
    with open(os.path.join(OUT, "FILE_MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"task": "Phase 5.4 CLI 2.1.317 host recheck", "output_file_count": len(files), "output_files": files, "bulk_fixture_dirs": bulk}, f, indent=1)
        f.write("\n")
    for x in checks:
        print(x["id"], x["status"])
    print({"pass": res["pass"], "fail": res["fail"], "manifest_files": len(files), "bulk_dirs": len(bulk)})
    sys.exit(0 if res["fail"] == 0 else 1)


if __name__ == "__main__":
    main()
