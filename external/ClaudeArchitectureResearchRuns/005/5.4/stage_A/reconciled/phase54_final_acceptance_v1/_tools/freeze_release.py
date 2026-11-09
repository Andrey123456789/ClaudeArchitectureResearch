"""Phase 5.4 final acceptance - step 2: build the immutable candidate release snapshot.

Run once from this task's output folder:  python -B _tools/freeze_release.py
- verifies each v3 template against step2_controlled_repair_v3/V3_FINAL_MANIFEST.json (hash and file set);
- copies every file byte for byte (shutil.copyfile: content only, no text-mode conversion) to
  release/candidates/<C>/template/<same relative path>;
- re-reads every copy and compares it with its source (filecmp, shallow=False) and with the manifest hash;
- writes release/CANDIDATE_FREEZE_MANIFEST.json (+ .sha256 sidecar) and sets the read-only attribute on
  every released file. Refuses to run if release/candidates already exists (no silent re-freeze).
Reads predecessors read-only. Writes only under release/.
"""
import datetime
import filecmp
import hashlib
import json
import os
import platform
import shutil
import stat
import sys

OUT = os.getcwd()
REC = os.path.normpath(os.path.join(OUT, ".."))
V3 = os.path.join(REC, "step2_controlled_repair_v3")
S3 = os.path.join(REC, "step3_six_way_strictness_v1")
K76 = os.path.join(REC, "benchmark_readiness_fair02_cp01_v1")
REL = os.path.join(OUT, "release")
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def text_profile(p):
    data = open(p, "rb").read()
    if b"\x00" in data:
        return {"kind": "binary"}
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    cr = data.count(b"\r") - crlf
    eol = "none" if not (crlf or lf or cr) else ("CRLF" if crlf and not lf and not cr else
                                                 "LF" if lf and not crlf and not cr else "MIXED")
    return {"kind": "text", "eol": eol, "crlf": crlf, "lf": lf, "cr": cr, "utf8_bom": data.startswith(b"\xef\xbb\xbf"),
            "final_newline": data.endswith(b"\n")}


def walk(root):
    out = []
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for n in sorted(fn):
            out.append(os.path.relpath(os.path.join(dp, n), root).replace(os.sep, "/"))
    return out


def tree_sha(files):
    h = hashlib.sha256()
    for rel in sorted(files):
        h.update(f"{rel}\t{files[rel]['sha256']}\n".encode("utf-8"))
    return h.hexdigest()


def main():
    if os.path.exists(os.path.join(REL, "candidates")):
        raise SystemExit("release/candidates already exists: the release is frozen; use release/verify_release.py")
    man_path = os.path.join(V3, "V3_FINAL_MANIFEST.json")
    man = json.load(open(man_path, encoding="utf-8"))
    assert man["version"] == "step2-controlled-repair-v3", man["version"]

    # 1. verify every source before copying anything
    for c in CANDS:
        src = os.path.join(V3, "candidates", c, "template")
        listed = man["candidates"][c]["files"]
        on_disk = walk(src)
        if sorted(on_disk) != sorted(listed):
            raise SystemExit(f"{c}: source file set differs from V3_FINAL_MANIFEST")
        for rel in on_disk:
            if sha(os.path.join(src, rel)) != listed[rel]["sha256"]:
                raise SystemExit(f"{c}: {rel} differs from V3_FINAL_MANIFEST")

    # 2. copy and 3. verify each copy
    cand_rows = {}
    for c in CANDS:
        src = os.path.join(V3, "candidates", c, "template")
        dst = os.path.join(REL, "candidates", c, "template")
        files = {}
        for rel in walk(src):
            s, d = os.path.join(src, rel), os.path.join(dst, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)
            if not filecmp.cmp(s, d, shallow=False):
                raise SystemExit(f"{c}: copy of {rel} is not byte-identical")
            h = sha(d)
            if h != man["candidates"][c]["files"][rel]["sha256"]:
                raise SystemExit(f"{c}: copy of {rel} hash differs from V3_FINAL_MANIFEST")
            files[rel] = {"sha256": h, "bytes": os.path.getsize(d), "v3_sha256": man["candidates"][c]["files"][rel]["sha256"],
                          "byte_identical_to_v3": True, "profile": text_profile(d)}
        if sorted(walk(dst)) != sorted(files):
            raise SystemExit(f"{c}: released tree has unexpected or missing files")
        cand_rows[c] = {"source": f"stage_A/reconciled/step2_controlled_repair_v3/candidates/{c}/template",
                        "release_path": f"release/candidates/{c}/template",
                        "n_files": len(files), "n_files_v3_manifest": man["candidates"][c]["n_files"],
                        "bytes": sum(v["bytes"] for v in files.values()), "tree_sha256": tree_sha(files),
                        "files": files}

    metrics = os.path.join(S3, "METRICS.json")
    fp = json.load(open(os.path.join(S3, "UPSTREAM_FINGERPRINT.json"), encoding="utf-8"))
    ds = json.load(open(os.path.join(V3, "DATASET_MANIFEST.json"), encoding="utf-8"))
    manifest = {
        "release_id": "phase54-final-v1",
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "created_by": "_tools/freeze_release.py (Phase 5.4 final acceptance)",
        "status": "FROZEN",
        "what_this_proves": "Byte identity of the released templates with the approved Step 2 v3 templates. It does not prove runtime behavior.",
        "source_version": {
            "version": man["version"], "manifest": "stage_A/reconciled/step2_controlled_repair_v3/V3_FINAL_MANIFEST.json",
            "manifest_sha256": sha(man_path), "manifest_at": man["at"],
            "last_gated_change": "V3-Q10-PACKAGEVERSION-VERSION (v3 STATE.json last_gate)",
            "v3_state_sha256": sha(os.path.join(V3, "STATE.json")),
        },
        "policy_data_version": {
            "dataset": ds["version"], "dataset_manifest_sha256": sha(os.path.join(V3, "DATASET_MANIFEST.json")),
            "oracle": fp["oracle"],
            "step3_comparison": "step3-six-way-strictness-v1",
            "step3_metrics_sha256": sha(metrics),
            "step3_policy_six_way_matrix_sha256": sha(os.path.join(S3, "POLICY_SIX_WAY_MATRIX.jsonl")),
            "step3_policy_cell_index_sha256": sha(os.path.join(S3, "POLICY_CELL_INDEX.jsonl")),
            "step3_upstream_v3_tree_aggregate_sha256": fp["v3_tree"]["aggregate_sha256"],
            "canonical_policies": 196, "policy_cells": 1176,
        },
        "research_decisions": {
            "FAIR-01": "APPROVED: preserve every enforcement, hook, checker, loading, routing and capability difference; no harmonization (benchmark_readiness_fair02_cp01_v1/FAIR01_APPROVED_DISPOSITION.md)",
            "FAIR-02": {"state": "ADOPTED: one external reporting instruction, identical for all six, appended to the task prompt, never embedded in a template; Report Completeness Score is secondary",
                        "instruction": "benchmark_readiness_fair02_cp01_v1/fair02/RUN_REPORT_INSTRUCTION.txt",
                        "instruction_sha256": sha(os.path.join(K76, "fair02", "RUN_REPORT_INSTRUCTION.txt"))},
            "CP-01": "Option 0: M keeps IDE0005 detection through dotnet format; no GenerateDocumentationFile added; M comments not patched (CP01_CORRECTION_PROPOSAL.md)",
            "other": ["CI/CD outside the practical benchmark scope", "common engineering contract preserved",
                      "approved Git user-authorization requirements preserved (PV2-01)", "no new normative policies",
                      "raw MUST_NOT counts are not a strictness score"],
        },
        "runtime_dependencies": {
            "claude_code_host": "Hooks use the exec form {command: node, args: [...]} with ${CLAUDE_PROJECT_DIR} in args and onFailure: block on PreToolUse. Whether a given host version honors these keys is a host fact (see LIVE_HOST_PILOT_REPORT.md).",
            "node": "All hooks and checkers are Node.js scripts (.mjs/.js/.cjs) started as `node` from PATH. No candidate declares a minimum version; Step 3 probes and this pilot used Node v26.13.0.",
            "dotnet_sdk": ".NET SDK 10 (all six target net10.0 with ManagePackageVersionsCentrally=true); checkers call `dotnet` for MSBuild evaluation; CP-01 used SDK 10.0.403.",
            "git": "Hooks and checkers call `git` (status/diff/ls-files) for change detection; Git commit/push gating needs a work tree.",
            "shell": "PreToolUse hooks are registered for both Bash and PowerShell tool names.",
            "network": "None needed by the hooks themselves; package restore by an agent needs a feed (benchmark-level decision).",
        },
        "immutability": {
            "read_only_attribute": "set on every released file after verification (a guard, not a security boundary)",
            "integrity_check": "python -B release/verify_release.py",
            "working_copies": "python -B release/make_working_copy.py <candidate> <empty destination outside release/>",
            "git": "no commit, tag, branch, push or reset was made (the 5.4 folder is not a Git repository)",
        },
        "environment": {"python": platform.python_version(), "os": platform.platform()},
        "totals": {"candidates": len(cand_rows), "files": sum(v["n_files"] for v in cand_rows.values()),
                   "bytes": sum(v["bytes"] for v in cand_rows.values())},
        "candidates": cand_rows,
    }
    mpath = os.path.join(REL, "CANDIDATE_FREEZE_MANIFEST.json")
    with open(mpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=1, sort_keys=False)
        f.write("\n")
    with open(mpath + ".sha256", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{sha(mpath)}  CANDIDATE_FREEZE_MANIFEST.json\n")

    # 4. read-only attribute on every released file
    for c in CANDS:
        root = os.path.join(REL, "candidates", c, "template")
        for rel in walk(root):
            os.chmod(os.path.join(root, rel), stat.S_IREAD)
    for p in (mpath, mpath + ".sha256"):
        os.chmod(p, stat.S_IREAD)
    print(json.dumps({"frozen": manifest["totals"], "manifest_sha256": sha(mpath),
                      "per_candidate": {c: (v["n_files"], v["tree_sha256"][:16]) for c, v in cand_rows.items()}}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
