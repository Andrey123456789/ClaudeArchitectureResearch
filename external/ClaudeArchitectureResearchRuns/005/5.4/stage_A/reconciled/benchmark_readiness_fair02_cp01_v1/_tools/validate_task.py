"""Validates this task's outputs and writes VALIDATION_REPORT.json.

Run from this task's output folder, after _tools/manifest.py: python -B _tools/validate_task.py
"""
import hashlib
import json
import os
import re

KIT = "../../../_STAGE_A_KIT"
REQUIRED = [
    "FAIR01_APPROVED_DISPOSITION.md", "FAIR02_IMPLEMENTATION_REPORT.md", "CP01_IDE0005_REPRODUCTION_REPORT.md",
    "CP01_CORRECTION_PROPOSAL.md", "FINAL_BENCHMARK_READINESS_DECISIONS.md", "STATE.json", "RESUME.md", "FILE_MANIFEST.json",
    "PROTECTED_INPUTS_VERIFICATION.json", "fair02/RUN_REPORT_INSTRUCTION.txt", "fair02/RUN_REPORT_INSTRUCTION.provenance.json",
    "fair02/REPORT_COMPLETENESS_RUBRIC.md", "fair02/score_report.py", "fair02/RUN_EVIDENCE_SCHEMA.md", "fair02/INTEGRATION_CONTRACT.md",
    "fair02/BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md", "fair02/assemble_prompt.py", "fair02/validation/SYNTHETIC_CHECK_RESULTS.md",
    "fair02/validation/results/LATEST.json", "cp01/CONFIG_PROVENANCE_CHECK.json", "cp01/SCRIPT_REVIEW.md",
    "cp01/OBSERVED_VS_EXPECTED.json", "cp01/supplied_script_run/RUN_METADATA.json",
    "cp01/replica_harness_run1/EVIDENCE_SUMMARY.json", "cp01/replica_harness_run2/EVIDENCE_SUMMARY.json",
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    checks = []

    def add(cid, ok, detail=None):
        checks.append({"id": cid, "pass": bool(ok), "detail": detail})

    missing = [f for f in REQUIRED if not os.path.exists(f)]
    add("V01 required deliverables exist", not missing, missing)

    # V02 instruction is verbatim from the contract (independent re-derivation).
    contract = open(f"{KIT}/Benchmark_Run_Report_Contract_EN.md", encoding="utf-8").read().replace("\r", "")
    block = re.search(r"## Report instruction to append[^\n]*\n\n((?:>.*\n)+)", contract).group(1)
    derived = "\n".join(re.sub(r"^> ?", "", l) for l in block.rstrip("\n").split("\n")).rstrip() + "\n"
    instr = open("fair02/RUN_REPORT_INSTRUCTION.txt", encoding="utf-8", newline="").read()
    add("V02 instruction equals contract text (re-derived)", instr == derived)
    prov = json.load(open("fair02/RUN_REPORT_INSTRUCTION.provenance.json", encoding="utf-8"))
    add("V03 instruction hash matches provenance", sha("fair02/RUN_REPORT_INSTRUCTION.txt") == prov["instruction_sha256"])
    add("V04 instruction contains no scoring/rubric wording", not re.search(r"score|rubric|points|assessor|benchmark", instr, re.I))
    heads = ["Outcome", "Changes", "Verification", "Decisions and deviations", "Risks and follow-ups"]
    pos = [instr.find(f"**{h}:**") for h in heads]
    add("V05 five headings present in order", all(p >= 0 for p in pos) and pos == sorted(pos), pos)

    latest = json.load(open("fair02/validation/results/LATEST.json", encoding="utf-8"))
    add("V06 synthetic checks: latest attempt ALL_PASS", latest["verdict"] == "ALL_PASS", f"{latest['checks_passed']}/{latest['checks_total']}")
    add("V07 synthetic checks ran against the current scorer", latest["scorer_sha256"] == sha("fair02/score_report.py"))
    classes = {json.load(open(f"fair02/validation/fixtures/{n}/expected.json", encoding="utf-8"))["class"] for n in latest["scores"]}
    need = ["genuinely completed", "partially completed", "failed run", "misleading"]
    add("V08 fixtures cover completed, partial, failed, misleading", all(any(k in c for c in classes) for k in need))
    fab = [n for n, s in latest["scores"].items() if any(f.startswith(("FABRICATED_PASS", "UNSUPPORTED_PASS_CLAIM")) for f in s["flags"])]
    add("V09 every fabricated-PASS fixture loses >= 20 verification points", all(latest["scores"][n]["dimensions"]["verification"] <= 10 for n in fab), fab)
    attempts = sorted(d for d in os.listdir("fair02/validation/results") if d.startswith("attempt_"))
    add("V10 all synthetic attempts kept", len(attempts) >= 3, attempts)
    pa = json.load(open("fair02/validation/prompt_assembly_check/out/PROMPT_ASSEMBLY_MANIFEST.json", encoding="utf-8"))
    add("V11 prompt assembly byte-identical for six candidates", pa["byte_identical_across_candidates"] and len(pa["prompts"]) == 6)

    prov_cfg = json.load(open("cp01/CONFIG_PROVENANCE_CHECK.json", encoding="utf-8"))
    add("V12 CP-01 config provenance MATCH_ALL_4", prov_cfg["verdict"] == "MATCH_ALL_4")
    ove = json.load(open("cp01/OBSERVED_VS_EXPECTED.json", encoding="utf-8"))
    add("V13 CP-01 predeclared expectations met, replicates identical, parsers agree",
        ove["all_predeclared_expectations_met"] and ove["replicates_identical"] and ove["all_parsers_agree"])
    rows = ove["replica_rows"]
    add("V14 CP-01 SDK 10.x in every case", all(r["sdk_msbuild_NETCoreSdkVersion"].startswith("10.") and r["sdk_muxer_in_case_dir"].startswith("10.") for r in rows))
    add("V15 CP-01 inputs matched kit and were unchanged", all(r["inputs_match_kit"] and r["inputs_unchanged_after"] for r in rows))
    rep = open("CP01_IDE0005_REPRODUCTION_REPORT.md", encoding="utf-8").read()
    add("V16 CP-01 report states the supplied script's partial run and false positive", "NativeCommandError" in rep and "false positive" in rep)
    run2 = {r["case"]: r for r in rows if r["source"] == "replica_harness_run2"}
    facts = {"A_M_as_is": (0, 0), "B_M_docs_override": (0, 1), "B2_M_docs_only": (0, 1), "C_L0_as_is": (0, 1), "F_M_format_style": (2, 1), "V_M_verify_format": (2, 1)}
    add("V17 CP-01 report table agrees with run 2 data (exit, IDE0005 count)",
        all((run2[c]["exit_code"], run2[c]["ide0005_count_python"]) == v for c, v in facts.items()))

    pv = json.load(open("PROTECTED_INPUTS_VERIFICATION.json", encoding="utf-8"))
    add("V18 protected inputs unchanged", pv["verdict"] == "UNCHANGED", {k: pv[k] for k in ("baseline_files", "current_files")})

    man = json.load(open("FILE_MANIFEST.json", encoding="utf-8"))
    bad = [f["path"] for f in man["output_files"] if "sha256" in f and (not os.path.exists(f["path"]) or sha(f["path"]) != f["sha256"])]
    listed = {f["path"] for f in man["output_files"]}
    unlisted = []
    for d, dirs, fs in os.walk("."):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), ".").replace(os.sep, "/")
            if rel not in listed and rel != "VALIDATION_REPORT.json":
                unlisted.append(rel)
    add("V19 manifest hashes match and every file is listed", not bad and not unlisted, {"bad": bad, "unlisted": unlisted})
    add("V20 manifest inputs all found", all(i["sha256"] != "MISSING" for i in man["inputs_read"]))

    english = []
    for d, _, fs in os.walk("."):
        for f in fs:
            if f.endswith((".md", ".py", ".ps1", ".txt")):
                p = os.path.join(d, f)
                if re.search("[" + chr(0x0400) + "-" + chr(0x04FF) + "]", open(p, encoding="utf-8", errors="replace").read()):
                    english.append(p)
    add("V21 artifacts in English (no Cyrillic)", not english, english)

    state = json.load(open("STATE.json", encoding="utf-8"))
    pending = [u for u, s in state["units"].items() if s != "DONE" and u != "U9_final_decisions_manifest_validation"]
    add("V22 all units except the final one are DONE", not pending, pending)

    out = {"checks": checks, "passed": sum(c["pass"] for c in checks), "total": len(checks),
           "verdict": "PASS" if all(c["pass"] for c in checks) else "FAIL"}
    json.dump(out, open("VALIDATION_REPORT.json", "w", encoding="utf-8", newline="\n"), indent=2)
    print(f"{out['passed']}/{out['total']} {out['verdict']}")
    for c in checks:
        if not c["pass"]:
            print("FAIL", c)


if __name__ == "__main__":
    main()
