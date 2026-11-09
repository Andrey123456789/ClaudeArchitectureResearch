"""Independent cross-check of CP-01 logs (second parser, Python) -> cp01/OBSERVED_VS_EXPECTED.json.

Parses raw logs of: the supplied-script run (partial), replica harness run 1 and run 2.
A diagnostic counts only in compiler format: '<file>(l,c): warning|error ID: msg' or 'CSC : warning ID: msg'.
Run from this task's output folder: python -B _tools/cp01_tabulate.py
"""
import json, os, re

DIAG = re.compile(r"^\s*(?:\d+>)?(?P<loc>[A-Za-z]:\\[^(\r\n]*?\(\d+,\d+\)|CSC)\s*:\s*(?P<sev>warning|error)\s+(?P<id>[A-Za-z]+\d*[A-Za-z]*):\s*(?P<msg>.*?)\s*(?:\[[^\]]*\])?\s*$")


def read(p):
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def diags(*texts):
    out = {}
    for t in texts:
        if not t:
            continue
        # PowerShell 5.1 error records wrap long lines; rejoin the wrapped IDE0005 record before matching.
        t = re.sub(r"warning\s*\r?\n\s*IDE0005:", "warning IDE0005:", t)
        t = re.sub(r"unnecessary\.\s*\r?\n\s*\[", "unnecessary. [", t)
        for line in t.splitlines():
            m = DIAG.match(line)
            if m:
                loc = m["loc"] if m["loc"] == "CSC" else os.path.basename(m["loc"].rsplit("(", 1)[0]) + "(" + m["loc"].rsplit("(", 1)[1]
                out[(loc, m["sev"], m["id"])] = m["msg"][:160]
    return [{"location": k[0], "severity": k[1], "id": k[2], "message": v} for k, v in out.items()]


EXPECTED = {
    "A_M_as_is": "IDE0005 absent (kit README)",
    "B_M_docs_override": "IDE0005 present (kit README)",
    "B2_M_docs_only": "IDE0005 present (supplementary)",
    "C_L0_as_is": "IDE0005 present (kit README)",
    "F_M_format_style": "not predeclared; nonzero exit can indicate IDE0005 (kit script)",
    "V_M_verify_format": "not predeclared (supplementary: M verify-skill command)",
}
PREDICATE = {"A_M_as_is": False, "B_M_docs_override": True, "B2_M_docs_only": True, "C_L0_as_is": True}

rows = []
for run in ("replica_harness_run1", "replica_harness_run2"):
    base = f"cp01/{run}"
    summ = json.load(open(f"{base}/EVIDENCE_SUMMARY.json", encoding="utf-8-sig"))
    for r in summ["results"]:
        case = r["case"]
        main = "03_build" if r["kind"] == "build" else ("03_format_style" if r["kind"] == "format_style" else "03_format_verify")
        so, se = read(f"{base}/{case}/{main}.stdout.log"), read(f"{base}/{case}/{main}.stderr.log")
        d = diags(so, se)
        ide = [x for x in d if x["id"] == "IDE0005"]
        p = r["effective_properties"]
        row = {
            "source": run, "case": case, "origin": r["origin"], "candidate": r["candidate"], "kind": r["kind"],
            "command": r["main_command"], "exit_code": r["main_exit"], "restore_exit": r["restore_exit"],
            "sdk_msbuild_NETCoreSdkVersion": p["NETCoreSdkVersion"], "sdk_muxer_in_case_dir": r["muxer_sdk_version_in_case_dir"],
            "EnforceCodeStyleInBuild": p["EnforceCodeStyleInBuild"], "GenerateDocumentationFile": p["GenerateDocumentationFile"],
            "DocumentationFile": p["DocumentationFile"], "NoWarn": p["NoWarn"], "TreatWarningsAsErrors": p["TreatWarningsAsErrors"],
            "csc_doc_switch_present": r["csc_doc_switch_present"],
            "diagnostics_python_parser": d, "ide0005_count_python": len(ide),
            "ide0005_count_powershell": r["ide0005_diagnostic_count"],
            "parsers_agree": len(ide) == r["ide0005_diagnostic_count"],
            "inputs_match_kit": r["inputs_match_kit"], "inputs_unchanged_after": r["inputs_unchanged_after"],
            "expected": EXPECTED[case],
        }
        if case in PREDICATE:
            row["matches_expectation"] = (len(ide) > 0) == PREDICATE[case] and r["main_exit"] == 0
        else:
            row["matches_expectation"] = "NOT_PREDECLARED"
        rows.append(row)

# Supplied script (partial run): parse its own logs and its console streams.
sbase = "cp01/supplied_script_run"
meta = json.load(open(f"{sbase}/RUN_METADATA.json", encoding="utf-8-sig"))
so, se = read(f"{sbase}/console.stdout.log"), read(f"{sbase}/console.stderr.log")
build_a = read(f"{sbase}/probe_root_copy/A_M_as_is/build.log")
supplied = {
    "script_sha256": meta["script_sha256"], "script_exit_code": meta["exit_code"],
    "cases_started": re.findall(r"^=== (\S+) ===", so or "", re.M),
    "A_script_reported": re.findall(r"^Build exit: .*$", so or "", re.M),
    "A_build_diagnostics_python_parser": diags(build_a),
    "format_command_stderr_diagnostics": diags(se),
    "termination": "NativeCommandError" if se and "NativeCommandError" in se else None,
    "files_left_by_script": [a["file"] for a in meta["archived_files"]],
    "summary_json_written": any(a["file"] == "summary.json" for a in meta["archived_files"]),
}

out = {
    "parser": "python strict compiler-format regex (independent of the PowerShell harness parser)",
    "supplied_script_run": supplied,
    "replica_rows": rows,
    "replicates_identical": all(
        [x for x in rows if x["source"] == "replica_harness_run1" and x["case"] == c][0]["ide0005_count_python"]
        == [x for x in rows if x["source"] == "replica_harness_run2" and x["case"] == c][0]["ide0005_count_python"]
        and [x for x in rows if x["source"] == "replica_harness_run1" and x["case"] == c][0]["exit_code"]
        == [x for x in rows if x["source"] == "replica_harness_run2" and x["case"] == c][0]["exit_code"]
        for c in EXPECTED),
    "all_predeclared_expectations_met": all(x["matches_expectation"] is True for x in rows if x["case"] in PREDICATE),
    "all_parsers_agree": all(x["parsers_agree"] for x in rows),
}
json.dump(out, open("cp01/OBSERVED_VS_EXPECTED.json", "w", encoding="utf-8", newline="\n"), indent=2)
print(json.dumps({k: v for k, v in out.items() if k != "replica_rows"}, indent=1)[:3000])
for x in rows:
    print(x["source"][-4:], x["case"], x["exit_code"], x["ide0005_count_python"], x["matches_expectation"], [d["id"] for d in x["diagnostics_python_parser"]])
