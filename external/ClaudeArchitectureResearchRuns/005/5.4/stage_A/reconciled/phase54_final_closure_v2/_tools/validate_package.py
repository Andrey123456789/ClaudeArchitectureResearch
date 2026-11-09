"""Validates the final closure package and writes VALIDATION_REPORT.json and PACKAGE_MANIFEST.json. Read-only toward everything else.

Usage: python -B validate_package.py
"""
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
REC = os.path.normpath(os.path.join(OUT, ".."))
DOCS = ["FINAL_CLOSURE_REPORT.md", "EVIDENCE_INDEX.md", "CLI_AND_DESKTOP_ENVIRONMENT.md", "CANDIDATE_FREEZE_VERIFICATION.md", "ITERATION_006_HANDOFF.md"]
REQUIRED = DOCS + ["ACCEPTANCE_MATRIX.json", "FINAL_STATE.json"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rj(p):
    return json.load(open(p, encoding="utf-8"))


def collect_hashes(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            collect_hashes(k, out)
            collect_hashes(v, out)
    elif isinstance(o, list):
        for v in o:
            collect_hashes(v, out)
    elif isinstance(o, str):
        out.update(re.findall(r"\b[0-9a-f]{64}\b", o.lower()))


checks = []


def chk(name, ok, detail=None):
    checks.append({"id": name, "pass": bool(ok), "detail": detail})


def resolve(p):
    return os.path.join(os.path.expanduser("~"), p[2:].replace("/", os.sep)) if p.startswith("~/") else os.path.join(REC, p.replace("/", os.sep))


chk("required_files_present", all(os.path.isfile(os.path.join(OUT, n)) for n in REQUIRED))
M = rj(os.path.join(OUT, "ACCEPTANCE_MATRIX.json"))
S = rj(os.path.join(OUT, "FINAL_STATE.json"))
F = rj(os.path.join(OUT, "evidence", "EVIDENCE_FACTS.json"))
rows = M["criteria"]
chk("status_vocabulary", all(r["status"] in ("PASS", "FAIL", "NOT_RUN", "NOT_VERIFIED") for r in rows))
chk("unique_ids", len({r["id"] for r in rows}) == len(rows))
missing = sorted({e for r in rows for e in r["evidence"] if not os.path.exists(resolve(e))})
chk("every_evidence_path_exists", not missing, missing)
chk("every_row_has_evidence_and_basis", all(r["evidence"] and r["basis"] for r in rows))
crit = [r for r in rows if r["critical"]]
all_pass = all(r["status"] == "PASS" for r in crit)
chk("final_status_follows_rule", M["final_status"] == S["final_status"] == ("CLOSED_VERIFIED" if all_pass else "CLOSED_CONDITIONAL"), M["final_status"])
chk("summary_counts_match", M["summary"]["critical_pass"] == sum(1 for r in crit if r["status"] == "PASS") and M["summary"]["critical_total"] == len(crit) and S["counts"] == M["summary"])
chk("no_not_run_promoted", all(r["status"] == "NOT_RUN" for r in rows if r["id"] in ("NC-01", "NC-02", "NC-03", "NC-04", "NC-05", "NC-12")))
chk("no_not_verified_promoted", all(r["status"] == "NOT_VERIFIED" for r in rows if r["id"] in ("NC-06", "NC-07", "NC-08", "NC-09", "NC-10", "NC-11")))
chk("history_preserves_failures", any(h["id"] == "H-02" and len(h["rows"]) == 6 for h in M["historical_results"]) and any(h["id"] == "H-04" and len(h["rows"]) == 7 for h in M["historical_results"]))
chk("non_k0_interactive_not_claimed", all("K0 only" in r["scope"] for r in rows if r["id"].startswith(("V1-", "V2-"))))
chk("confirmations", S["confirmations"]["normative_templates_edited"] is False and S["confirmations"]["iteration_006_started"] is False and S["confirmations"]["candidates_byte_for_byte_frozen"] is True)
# Every 64-hex token in the Markdown must be a value computed in this task, or a file hash in the package evidence.
known = set()
collect_hashes(F, known)
collect_hashes(rj(os.path.join(OUT, "_baseline", "PROTECTED_BASELINE.json")), known)
known |= set(re.findall(r"\b[0-9a-f]{64}\b", open(os.path.join(OUT, "evidence", "ENVIRONMENT_PROBE.txt"), encoding="utf-8").read()))
known.add(sha(os.path.join(OUT, "evidence", "VERIFY_RELEASE_FINAL.json")))
known.add(sha(os.path.join(OUT, "evidence", "v1_transcript_excerpt.jsonl")))
known.add(sha(os.path.join(OUT, "evidence", "ENVIRONMENT_PROBE.txt")))
known.add(sha(os.path.join(OUT, "evidence", "corroborating_pending_card_image_1_from_v1_chat.png")))
known.add(sha(os.path.join(OUT, "_baseline", "PROTECTED_VERIFY.json")))
for n in ("t1_stdout.json", "collect_stdout.json"):
    known.add(sha(os.path.join(OUT, "evidence", "v2_readonly_rerun", n)))
known.add(sha(os.path.join(REC, "phase54_cli317_host_recheck_v1", "RECHECK_TOTALS.json")))
unknown = {}
for d in DOCS:
    tokens = set(re.findall(r"\b[0-9a-f]{64}\b", open(os.path.join(OUT, d), encoding="utf-8").read()))
    bad = sorted(tokens - known)
    if bad:
        unknown[d] = bad
chk("markdown_hashes_are_computed_values", not unknown, unknown)
text = {d: open(os.path.join(OUT, d), encoding="utf-8").read() for d in DOCS}
report = text["FINAL_CLOSURE_REPORT.md"]
chk("report_states_scope_limits", "K0 only" in report and "does not prove" in report and "CLOSED_CONDITIONAL" in report)
chk("report_no_transcript_hook_text_claim", "contains no K0 text" in report)
chk("non_ascii_is_limited", all(not re.search(r"[Ѐ-ӿ]", t) for t in text.values()), "no Cyrillic text in Markdown")
chk("v2_evidence_untouched", rj(os.path.join(OUT, "evidence", "v2_readonly_rerun", "RERUN_RECORD.json"))["v2_evidence_unchanged"] is True)
prot = rj(os.path.join(OUT, "_baseline", "PROTECTED_VERIFY.json"))
chk("protected_tree_unchanged", prot["verdict"] == "UNCHANGED", prot["verdict"])
chk("originals_listed_preserved", all(os.path.isfile(resolve(p)) for p in S["preserved_originals"]))

res = {"tool": "_tools/validate_package.py", "passed": sum(1 for c in checks if c["pass"]), "total": len(checks), "verdict": "PASS" if all(c["pass"] for c in checks) else "FAIL", "checks": checks}
with open(os.path.join(OUT, "VALIDATION_REPORT.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
    f.write("\n")
files = []
for dp, dn, fn in os.walk(OUT):
    for n in sorted(fn):
        p = os.path.join(dp, n)
        r = os.path.relpath(p, OUT).replace(os.sep, "/")
        if r != "PACKAGE_MANIFEST.json":
            files.append({"path": r, "bytes": os.path.getsize(p), "sha256": sha(p)})
with open(os.path.join(OUT, "PACKAGE_MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({"package": "phase54_final_closure_v2", "excludes_itself": True, "n_files": len(files), "files": sorted(files, key=lambda x: x["path"])}, f, indent=1)
    f.write("\n")
print(json.dumps({"passed": res["passed"], "total": res["total"], "verdict": res["verdict"], "failed": [c for c in checks if not c["pass"]], "files": len(files)}, indent=1, ensure_ascii=False))
sys.exit(0 if res["verdict"] == "PASS" else 1)
