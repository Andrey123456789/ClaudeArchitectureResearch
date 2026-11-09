"""Writes FILE_MANIFEST.json: every output file (hash, size, role) plus the inputs this task read (hash) and external side effects.

Run from this task's output folder: python -B _tools/manifest.py
Mutable bookkeeping files (STATE.json, RESUME.md, FILE_MANIFEST.json, VALIDATION_REPORT.json) are listed without hashes.
"""
import hashlib
import json
import os
import platform
import subprocess

ROOT = "../../.."  # the 5.4 folder, relative to this output folder
MUTABLE = {"STATE.json", "RESUME.md", "FILE_MANIFEST.json", "VALIDATION_REPORT.json"}
ROLES = [
    ("cp01/", "CP-01 evidence"), ("fair02/validation/", "FAIR-02 synthetic validation"), ("fair02/", "FAIR-02 contract, tools, rubric"),
    ("_tools/", "task tools"), ("_baseline/", "protected-input baseline"),
]
INPUTS_READ = [
    "_STAGE_A_KIT/76_CLAUDE_FAIR02_CP01_TASK_EN.md", "_STAGE_A_KIT/76_README_FAIR02_CP01_EN.md",
    "_STAGE_A_KIT/Benchmark_Run_Report_Contract_EN.md", "_STAGE_A_KIT/ide0005_probe_en/README_EN.md",
    "_STAGE_A_KIT/ide0005_probe_en/Test-IDE0005.ps1", "_STAGE_A_KIT/ide0005_probe_en/CONFIG_PROVENANCE_SHA256.json",
    "_STAGE_A_KIT/ide0005_probe_en/Probe.csproj", "_STAGE_A_KIT/ide0005_probe_en/Source.cs",
    "_STAGE_A_KIT/ide0005_probe_en/configs/M/.editorconfig", "_STAGE_A_KIT/ide0005_probe_en/configs/M/Directory.Build.props",
    "_STAGE_A_KIT/ide0005_probe_en/configs/L0/.editorconfig", "_STAGE_A_KIT/ide0005_probe_en/configs/L0/Directory.Build.props",
    "stage_A/reconciled/step3_six_way_strictness_v1/FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md",
    "stage_A/reconciled/step3_six_way_strictness_v1/OPEN_DECISIONS_AND_SENSITIVITY.md",
    "stage_A/reconciled/step3_six_way_strictness_v1/METRIC_LINEAGE_AND_LIMITS.md",
    "stage_A/reconciled/step3_six_way_strictness_v1/ROOT_CAUSE_SUMMARY.json",
    "stage_A/reconciled/step3_six_way_strictness_v1/EXTRA_GENUINE_ROOTS.json",
    "stage_A/reconciled/step3_six_way_strictness_v1/POLICY_SIX_WAY_MATRIX.jsonl",
    "stage_A/reconciled/step3_six_way_strictness_v1/SEMANTIC_CHALLENGE_LOG.jsonl",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/.editorconfig",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/Directory.Build.props",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/.claude/MAP.md",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/.claude/rules/coding-style.md",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/.claude/scripts/check-instructions.mjs",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/.claude/scripts/check-manifests.mjs",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/M/template/docs/technology-stack.md",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/L0/template/.editorconfig",
    "stage_A/reconciled/step2_controlled_repair_v3/candidates/L0/template/Directory.Build.props",
] + [f"stage_A/reconciled/step2_controlled_repair_v3/candidates/{c}/template/.claude/skills/verify/SKILL.md" for c in ("M", "M1", "L0", "L1", "K0", "K1")] \
  + [f"stage_A/reconciled/step2_controlled_repair_v3/candidates/{c}/template/CLAUDE.md" for c in ("M", "M1", "L0", "L1", "K0", "K1")] \
  + ["../5.2/README.md", "../5.2/GOAL_PROMPT.txt", "../5.2/protocol-amendments/5.2.2-bounded-convergence.md", "../5.1/README.md",
     "inputs/M/baseline/TASK.md", "inputs/M/REFINEMENT_TASK.md", "inputs/M/CANDIDATE.md", "SETUP_5_4.py"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def role(rel):
    if "/" not in rel:
        return "top-level deliverable"
    return next((r for pre, r in ROLES if rel.startswith(pre)), "other")


def main():
    files = []
    for d, dirs, fs in os.walk("."):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for f in sorted(fs):
            rel = os.path.relpath(os.path.join(d, f), ".").replace(os.sep, "/")
            entry = {"path": rel, "role": role(rel), "bytes": os.path.getsize(rel)}
            if rel not in MUTABLE:
                entry["sha256"] = sha(rel)
            files.append(entry)
    inputs = []
    for rel in INPUTS_READ:
        p = os.path.join(ROOT, rel)
        inputs.append({"path": "5.4/" + rel if not rel.startswith("../") else rel.replace("../", "005/"),
                       "sha256": sha(p) if os.path.exists(p) else "MISSING"})
    try:
        sdk = subprocess.run(["dotnet", "--version"], capture_output=True, text=True, cwd=os.environ.get("TEMP", "."), timeout=60).stdout.strip()
    except Exception as e:  # noqa: BLE001 - provenance only
        sdk = f"UNAVAILABLE ({e})"
    manifest = {
        "task": "Experiment 005 / Phase 5.4 - kit 76 FAIR-02 + CP-01",
        "output_folder": "stage_A/reconciled/benchmark_readiness_fair02_cp01_v1",
        "environment": {"python": platform.python_version(), "os": platform.platform(), "dotnet_active_sdk_in_TEMP": sdk},
        "output_files": files,
        "output_file_count": len(files),
        "inputs_read": inputs,
        "external_side_effects": {
            "windows_temp_directories_created": [
                "%TEMP%/IDE0005-Probe-7eaa635019bb471c98d5c185d5af14fa (created by the supplied script)",
                "%TEMP%/CP01-KitCopy-48cffc95b82745c3a15c59cc8aa63fa7 (hash-verified kit copy)",
                "%TEMP%/CP01-Evidence-b2ca7eefc8f24adc97b206aba9d2a8ee (replica harness run 1)",
                "%TEMP%/CP01-Evidence-9f1c6aecf5ea46518641553e6ecb7393 (replica harness run 2)",
            ],
            "installed_or_configured": "nothing; process-scoped environment variables only",
            "network": "no package feed contacted by design (empty local feed); telemetry and workload-update checks disabled per process",
        },
    }
    with open("FILE_MANIFEST.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2)
    print(f"{len(files)} output files, {len(inputs)} inputs, missing inputs: {[i['path'] for i in inputs if i['sha256'] == 'MISSING']}")


if __name__ == "__main__":
    main()
