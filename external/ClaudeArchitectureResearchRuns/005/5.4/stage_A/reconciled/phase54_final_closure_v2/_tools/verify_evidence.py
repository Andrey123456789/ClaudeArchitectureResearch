"""Read-only fact collection for the Phase 5.4 final closure. Writes only inside this package's evidence/ folder.

It re-reads the primary records (manifests, raw run results, Git repositories, transcripts) and stores what it finds in
evidence/EVIDENCE_FACTS.json. It launches no Claude session and runs no test. Git calls use --no-optional-locks.

Usage: python -B verify_evidence.py
"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
EV = os.path.join(OUT, "evidence")
REC = os.path.normpath(os.path.join(OUT, ".."))
FINAL = os.path.join(REC, "phase54_final_acceptance_v1")
RELDIR = os.path.join(FINAL, "release")
RCK = os.path.join(REC, "phase54_cli317_host_recheck_v1")
V1 = os.path.join(REC, "phase54_desktop_auto_smoke_v1")
V2 = os.path.join(REC, "phase54_desktop_auto_smoke_v2")
FAIR = os.path.join(REC, "benchmark_readiness_fair02_cp01_v1")
S3 = os.path.join(REC, "step3_six_way_strictness_v1")
V3 = os.path.join(REC, "step2_controlled_repair_v3")
PROJECTS = os.path.join(os.path.expanduser("~"), ".claude", "projects")
PFX = "C--Projects-AI-Learning-ClaudeArchitectureResearchRuns-005-5-4-stage-A-reconciled-phase54-desktop-auto-smoke-"
T1 = os.path.join(PROJECTS, PFX + "v1-work", "41e9d77f-7c86-43f6-9462-5848bdaa0cfb.jsonl")
T2 = os.path.join(PROJECTS, PFX + "v2-work", "9fe6ddea-d2e5-442a-b5b3-d50708fcc695.jsonl")
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
CLI_SHA = "26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038"
K0_TEXT = "Repository-changing Git command"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rj(p):
    return json.load(open(p, encoding="utf-8"))


def rel(p):
    return os.path.relpath(p, REC).replace(os.sep, "/")


def git(d, *a):
    return subprocess.run(["git", "--no-optional-locks", "-C", d, *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


def walk(root):
    out = []
    for dp, dn, fn in os.walk(root):
        for n in fn:
            out.append(os.path.relpath(os.path.join(dp, n), root).replace(os.sep, "/"))
    return sorted(out)


def release():
    mp = os.path.join(RELDIR, "CANDIDATE_FREEZE_MANIFEST.json")
    side = open(mp + ".sha256", encoding="utf-8").read().split()[0]
    m = rj(mp)
    run = subprocess.run([sys.executable, "-B", os.path.join(RELDIR, "verify_release.py"), "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    with open(os.path.join(EV, "VERIFY_RELEASE_FINAL.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(run.stdout)
    vr = json.loads(run.stdout)
    per, total, ok = {}, 0, 0
    for c in CANDS:
        row = m["candidates"][c]
        root = os.path.join(RELDIR, "candidates", c, "template")
        listed = row["files"]
        actual = walk(root)
        mism = [r for r, x in listed.items() if not os.path.isfile(os.path.join(root, r)) or sha(os.path.join(root, r)) != x["sha256"]]
        total += len(listed)
        ok += len(listed) - len(mism)
        sett = os.path.join(root, ".claude", "settings.json")
        v3s = os.path.join(V3, "candidates", c, "template", ".claude", "settings.json")
        per[c] = {"n_files_manifest": row["n_files"], "n_files_on_disk": len(actual), "bytes": row["bytes"], "tree_sha256": row["tree_sha256"], "independent_sha_mismatches": mism, "unexpected_files": sorted(set(actual) - set(listed)), "settings_sha256": sha(sett), "settings_equals_v3": sha(sett) == sha(v3s), "verifier_pass": vr["per_candidate"][c]["pass"], "verifier_v3_identical": vr["per_candidate"][c]["R5_v3"]["same_file_set"] and not vr["per_candidate"][c]["R5_v3"]["not_byte_identical"]}
    return {"release_id": m["release_id"], "status": m["status"], "created_at": m["created_at"], "manifest_path": rel(mp), "manifest_sha256_computed": sha(mp), "manifest_sha256_sidecar": side, "verify_release_exit": run.returncode, "verify_release_verdict": vr["verdict"], "verify_release_warnings": vr["warnings"], "verify_release_totals": vr["totals"], "v3_comparison": vr["v3_comparison"], "per_candidate": per, "total_files": total, "files_matching_sha": ok, "release_dir_entries": sorted(os.listdir(RELDIR)), "distinct_settings_hashes": len({v["settings_sha256"] for v in per.values()})}


def fair():
    ip = os.path.join(FAIR, "fair02", "RUN_REPORT_INSTRUCTION.txt")
    data = open(ip, "rb").read()
    prov = rj(os.path.join(FAIR, "fair02", "RUN_REPORT_INSTRUCTION.provenance.json"))
    text = data.replace(b"\r\n", b"\n")
    lines = [ln.strip() for ln in text.split(b"\n") if len(ln.strip()) >= 40]
    full_hits, line_hits, scanned = [], {}, 0
    for c in CANDS:
        root = os.path.join(RELDIR, "candidates", c, "template")
        for r in walk(root):
            d = open(os.path.join(root, r), "rb").read().replace(b"\r\n", b"\n")
            scanned += 1
            if text.strip() in d:
                full_hits.append(c + "/" + r)
            for ln in lines:
                if ln in d:
                    line_hits.setdefault(ln.decode("utf-8", "replace")[:80], []).append(c + "/" + r)
    return {"instruction_path": rel(ip), "instruction_sha256_computed": sha(ip), "instruction_sha256_recorded": prov["instruction_sha256"], "fair01_disposition": rel(os.path.join(FAIR, "FAIR01_APPROVED_DISPOSITION.md")), "fair01_disposition_sha256": sha(os.path.join(FAIR, "FAIR01_APPROVED_DISPOSITION.md")), "decisions_path": rel(os.path.join(FAIR, "FINAL_BENCHMARK_READINESS_DECISIONS.md")), "decisions_sha256": sha(os.path.join(FAIR, "FINAL_BENCHMARK_READINESS_DECISIONS.md")), "fair02_implementation_report_sha256": sha(os.path.join(FAIR, "FAIR02_IMPLEMENTATION_REPORT.md")), "fair02_addendum_sha256": sha(os.path.join(FAIR, "fair02", "BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md")), "template_files_scanned": scanned, "instruction_full_text_hits": full_hits, "instruction_distinctive_line_count": len(lines), "instruction_line_hits": line_hits}


def step3():
    st = rj(os.path.join(S3, "STATE.json"))
    me = rj(os.path.join(S3, "METRICS.json"))
    rp = os.path.join(S3, "FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md")
    return {"status": st["status"], "verdict": st["verdict"], "step4_started": st["step4_started"], "policies": me["universe_policies"]["n"], "labels": me["universe_policies"]["labels"], "report_path": rel(rp), "report_sha256": sha(rp), "metrics_sha256": sha(os.path.join(S3, "METRICS.json")), "matrix_sha256": sha(os.path.join(S3, "POLICY_SIX_WAY_MATRIX.jsonl"))}


def manifest_check(folder):
    m = rj(os.path.join(folder, "FILE_MANIFEST.json"))
    hashed = [x for x in m["output_files"] if x.get("sha256")]
    bad = [x["path"] for x in hashed if not os.path.isfile(os.path.join(folder, x["path"])) or sha(os.path.join(folder, x["path"])) != x["sha256"]]
    return {"folder": rel(folder), "entries": len(m["output_files"]), "hashed_entries": len(hashed), "mismatched": bad}


def recheck():
    rows = [json.loads(ln) for ln in open(os.path.join(RCK, "CLI317_RECHECK_MATRIX.jsonl"), encoding="utf-8")]
    eff = {r["row_id"]: r for r in rows if r.get("effective")}
    pilot = [json.loads(ln) for ln in open(os.path.join(FINAL, "LIVE_HOST_PILOT_MATRIX.jsonl"), encoding="utf-8")]
    groups = {}
    for g in ["D1", "D1M", "D1X", "D1XM", "S-A1", "S-A2", "S-B1", "S-C1", "S-C2", "S-E1", "IA", "D2", "F1"]:
        groups[g] = {c: eff[f"{c}-{g}"]["status"] for c in CANDS}
    d3 = {k: eff[k]["status"] for k in eff if k.endswith("-D3") or k.endswith("-D3M")}
    syn = {k: eff[k]["status"] for k in eff if k.startswith("SYN-")}
    raw = {}
    for c in CANDS:
        folder = eff[f"{c}-D1"]["folder"]
        d = os.path.join(RCK, "runs", folder)
        r = rj(os.path.join(d, "result.json"))
        txt = open(os.path.join(d, "stdout.jsonl"), encoding="utf-8", errors="replace").read()
        raw[c] = {"folder": folder, "identity_before_gate": r["identity_before"]["gate"], "identity_after_gate": r["identity_after"]["gate"], "sha256_before": r["identity_before"]["sha256"], "sha256_after": r["identity_after"]["sha256"], "version": r["identity_before"]["version_stdout"], "tool_result_blocking_text": 'blocking because onFailure is \\"block\\"' in txt, "init_reports_2_1_317": '"claude_code_version":"2.1.317"' in txt, "marker_present": os.path.exists(os.path.join(d, "work", "recheck_marker.txt")), "operation_executed_D1": eff[f"{c}-D1"]["operation_executed"], "operation_executed_D1M": eff[f"{c}-D1M"]["operation_executed"]}
    pos = {}
    for rid in [f"{c}-S-A2" for c in CANDS] + ["SYN-DX2M", "SYN-SHIMM"]:
        d = os.path.join(RCK, "runs", eff[rid]["folder"])
        pos[rid] = {"folder": eff[rid]["folder"], "marker_present": os.path.exists(os.path.join(d, "work", "recheck_marker.txt")), "operation_executed": eff[rid]["operation_executed"], "status": eff[rid]["status"]}
    sessions, gates_ok, shas, vers = 0, 0, set(), set()
    for rp in glob.glob(os.path.join(RCK, "runs", "*", "result.json")):
        r = rj(rp)
        if "identity_before" not in r:
            continue
        sessions += 1
        gates_ok += r["identity_before"]["gate"] == "PASS" and r["identity_after"]["gate"] == "PASS"
        shas |= {r["identity_before"]["sha256"], r["identity_after"]["sha256"]}
        vers |= {r["identity_before"]["version_stdout"], r["identity_after"]["version_stdout"]}
    totals = rj(os.path.join(RCK, "RECHECK_TOTALS.json"))
    audit = rj(os.path.join(RCK, "RAW_EVIDENCE_AUDIT.json"))
    val = rj(os.path.join(RCK, "VALIDATION_REPORT.json"))
    identity = rj(os.path.join(RCK, "cli_identity", "IDENTITY.json"))
    ask = {c: {"folder": eff[f"{c}-S-C1"]["folder"], "request_reason_type_hook": "hook" in open(os.path.join(RCK, "runs", eff[f"{c}-S-C1"]["folder"], "permission_requests.jsonl"), encoding="utf-8", errors="replace").read(), "operation_executed": eff[f"{c}-S-C1"]["operation_executed"]} for c in CANDS}
    return {"matrix_path": rel(os.path.join(RCK, "CLI317_RECHECK_MATRIX.jsonl")), "matrix_sha256": sha(os.path.join(RCK, "CLI317_RECHECK_MATRIX.jsonl")), "rows_total": len(rows), "effective_rows": len(eff), "effective_by_status": {s: sum(1 for r in eff.values() if r["status"] == s) for s in ("PASS", "FAIL", "NOT_RUN")}, "superseded_rows": sum(1 for r in rows if not r.get("effective")), "superseded_fail_rows": sorted(f"{r['row_id']}@a{r['attempt']}" for r in rows if not r.get("effective") and r["status"] == "FAIL"), "totals_file": totals, "groups": groups, "d3": d3, "synthetic": syn, "d1_raw": raw, "positive_controls": pos, "ask_requests": ask, "sessions_with_identity": sessions, "sessions_gate_pass": gates_ok, "sha256_seen": sorted(shas), "versions_seen": sorted(vers), "identity_file": identity, "raw_audit": {x["id"]: x["status"] for x in audit["checks"]}, "validation": {k: v for k, v in val.items() if not isinstance(v, (list, dict))}, "original_pilot_fail_rows": sorted(r["row_id"] for r in pilot if r.get("status") == "FAIL"), "original_pilot_candidate_by_status": {s: sum(1 for r in pilot if r.get("status") == s and not str(r.get("row_id")).startswith(("SYN-", "DX"))) for s in ("PASS", "FAIL", "NOT_RUN")}, "original_pilot_synthetic_by_status": {s: sum(1 for r in pilot if r.get("status") == s and str(r.get("row_id")).startswith(("SYN-", "DX"))) for s in ("PASS", "FAIL", "NOT_RUN")}, "report_sha256": sha(os.path.join(RCK, "CLI317_RECHECK_REPORT.md")), "addendum_sha256": sha(os.path.join(RCK, "PHASE54_CLOSURE_ADDENDUM.md")), "amendments_sha256": sha(os.path.join(RCK, "DESIGN_AMENDMENTS.md")), "cli_doc_sha256": sha(os.path.join(RCK, "CLI_VERSION_AND_HASH.md")), "host_probe_sha256": sha(os.path.join(RCK, "cli_identity", "HOST_PROBE.txt"))}


def load_lines(p):
    return open(p, encoding="utf-8", errors="replace").read().split("\n")


def parse_transcript(L):
    versions, entries, modes = set(), set(), {}
    uses, results, hooks = [], {}, []
    for n, line in enumerate(L, 1):
        if not line.strip():
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") not in ("user", "assistant", "attachment"):
            continue
        if o.get("version"):
            versions.add(o["version"])
        if o.get("entrypoint"):
            entries.add(o["entrypoint"])
        if "permissionMode" in o:
            modes[o["permissionMode"]] = modes.get(o["permissionMode"], 0) + 1
        if o.get("type") == "attachment":
            a = o.get("attachment") or {}
            if str(a.get("type", "")).startswith("hook"):
                hooks.append({"line": n, "at": o.get("timestamp"), "type": a.get("type"), "hookName": a.get("hookName"), "toolUseID": a.get("toolUseID"), "exitCode": a.get("exitCode"), "stdout": a.get("stdout"), "command": a.get("command"), "durationMs": a.get("durationMs")})
        c = (o.get("message") or {}).get("content")
        if isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use" and "command" in (b.get("input") or {}):
                    uses.append({"line": n, "at": o.get("timestamp"), "id": b.get("id"), "tool": b.get("name"), "command": b["input"]["command"], "description": b["input"].get("description")})
                elif isinstance(b, dict) and b.get("type") == "tool_result":
                    x = b.get("content")
                    t = x if isinstance(x, str) else "\n".join(y.get("text", "") for y in x if isinstance(y, dict)) if isinstance(x, list) else str(x)
                    results.setdefault(b.get("tool_use_id"), {"line": n, "at": o.get("timestamp"), "is_error": bool(b.get("is_error")), "text": t[:260]})
    for u in uses:
        u["result"] = results.get(u["id"])
    commits = [u for u in uses if u["command"].startswith("git commit")]
    return {"cli_versions": sorted(versions), "entrypoints": sorted(entries), "permission_modes": modes, "commit_attempts": commits, "hook_records": hooks}


def desktop_v1():
    W = os.path.join(V1, "work")
    m = rj(os.path.join(RELDIR, "CANDIDATE_FREEZE_MANIFEST.json"))["candidates"]["K0"]["files"]
    diffs = sorted(r for r, x in m.items() if not os.path.isfile(os.path.join(W, r)) or sha(os.path.join(W, r)) != x["sha256"])
    prov = rj(os.path.join(V1, "work.provenance.json"))
    state = rj(os.path.join(V1, "STATE.json"))
    res = rj(os.path.join(W, "desktop_auto_smoke", "results.json"))
    L = load_lines(T1)
    p = parse_transcript(L)
    hook = next((h for h in p["hook_records"] if h["hookName"] == "PreToolUse:PowerShell" and "permissionDecision" in (h["stdout"] or "")), None)
    keep = [124, 125, 126, 129, 165, 166, 167, 232, 239, 285, 292]
    with open(os.path.join(EV, "v1_transcript_excerpt.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for n in keep:
            f.write(json.dumps({"source_line": n, "raw": L[n - 1]}, ensure_ascii=False) + "\n")
    fix = [k for k in ("Was the second card shown",) if k in L[284]]
    img = glob.glob(os.path.join(os.environ["LOCALAPPDATA"], "Temp", "claude", "*", "41e9d77f-7c86-43f6-9462-5848bdaa0cfb", "images", "1.png"))
    return {"state_json_status": state["status"], "state_json_interactive_tests_executed": state["interactive_tests_executed"], "evidence_dir_entries": sorted(os.listdir(os.path.join(V1, "evidence"))), "work_provenance_tree_sha256": prov["tree_sha256"], "work_provenance_manifest_sha256": prov["manifest_sha256"], "baseline_expected": "f4b37516203bc41c208ae326613b7076ab4ecc2a", "head": git(W, "rev-parse", "HEAD"), "parent": git(W, "rev-parse", "HEAD^"), "commit_count": int(git(W, "rev-list", "--count", "--all")), "log": git(W, "log", "--format=%H %s").splitlines(), "head_changes": git(W, "show", "--name-status", "--format=", "HEAD").splitlines(), "staged": git(W, "diff", "--cached", "--name-status").splitlines(), "status": git(W, "status", "--porcelain=v1").splitlines(), "probe_blob_head": git(W, "rev-parse", "HEAD:desktop_auto_probe.txt"), "k0_files_differing_from_frozen": diffs, "k0_files_checked": len(m), "local_settings_present": os.path.exists(os.path.join(W, ".claude", "settings.local.json")), "hook_state_present": os.path.isdir(os.path.join(W, ".claude", ".hook-state")), "transcript_path": T1, "transcript_sha256": sha(T1), "transcript": p, "hook_record_for_allow": hook, "operator_lines": {"129": "contains 'I explicitly clicked DENY' and 'I will explicitly ALLOW the second hook permission request.'" if "I explicitly clicked DENY" in L[128] and "I will explicitly ALLOW" in L[128] else "NOT_FOUND", "239": "First card unconfirmed" if "First card unconfirmed" in L[238] else "NOT_FOUND", "292": "Yes, confirmed" if "Yes, confirmed" in L[291] else "NOT_FOUND"}, "question_before_292_found_at_line_285": bool(fix), "results_json_sha256": sha(os.path.join(W, "desktop_auto_smoke", "results.json")), "report_md_sha256": sha(os.path.join(W, "desktop_auto_smoke", "REPORT.md")), "scenarios": {s["id"]: s["status"] for s in res["scenarios"]}, "overall": res["overall"]["status"], "corroborating_operator_image_found": img}


def desktop_v2():
    W = os.path.join(V2, "work")
    D = os.path.join(EV, "v2_readonly_rerun")
    state = rj(os.path.join(V2, "STATE.json"))
    rows = [json.loads(ln) for ln in open(os.path.join(D, "state_checks.jsonl"), encoding="utf-8")]
    hist = [json.loads(ln) for ln in open(os.path.join(V2, "evidence", "state_checks.jsonl"), encoding="utf-8")]
    summary = rj(sorted(glob.glob(os.path.join(D, "transcript_summary_*.json")))[-1])
    L = load_lines(T2)
    p = parse_transcript(L)
    png = os.path.join(V2, "evidence", "k0_deny_permission_card.png")
    trans_copy = sorted(glob.glob(os.path.join(D, "transcript_*.jsonl")))[-1]
    hv = rj(os.path.join(V2, "setup_verification", "HOOK_VERIFICATION.json"))
    commit_row = next(r for r in hv["rows"] if r["label"] == "commit via PowerShell")
    titles = sorted({json.loads(ln).get("customTitle") for ln in L if '"custom-title"' in ln and ln.strip()} - {None})
    binding = {"session_title_in_transcript": titles, "tool_description_line_78": "Commit the already-staged probe file" in L[77], "assistant_text_line_77": "so I'm running your exact commit command" in L[76], "plan_items_line_57": all(x in L[56] for x in ("Load project Git workflow", "Inspect staged state read-only", "Run the requested commit once"))}
    a = p["commit_attempts"][0] if p["commit_attempts"] else None
    import datetime as dt
    seconds = None
    if a and a.get("result"):
        f = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        seconds = round((f(a["result"]["at"]) - f(a["at"])).total_seconds(), 3)
    s = rows[-1]["state"]
    img = glob.glob(os.path.join(os.environ["LOCALAPPDATA"], "Temp", "claude", "*", "41e9d77f-7c86-43f6-9462-5848bdaa0cfb", "images", "1.png"))
    corr = None
    if img:
        target = os.path.join(EV, "corroborating_pending_card_image_1_from_v1_chat.png")
        if not os.path.exists(target):
            shutil.copy2(img[0], target)
        corr = {"source_path": img[0], "archived_as": "evidence/corroborating_pending_card_image_1_from_v1_chat.png", "sha256": sha(target), "bytes": os.path.getsize(target), "referenced_in_v1_transcript_line": 459, "sent_at_utc": json.loads(load_lines(T1)[458]).get("timestamp")}
    return {"state_json_status": state["status"], "state_json_interactive_tests_executed": state["interactive_tests_executed"], "baseline_head_expected": state["baseline_head"], "rerun_record": rj(os.path.join(D, "RERUN_RECORD.json")), "rerun_t1": {"at": rows[-1]["at"], "git_state": rows[-1]["git_state"], "checks": rows[-1]["checks"], "head": s["head"], "commit_count": s["commit_count"], "staged": s["staged"], "status": s["status"], "hook_state_present": s["hook_state_present"], "local_settings_present": s["local_settings_present"], "k0_files_differing_from_frozen": s["k0_files_differing_from_frozen"]}, "historical_state_check_rows": [{"stage": r["stage"], "at": r["at"], "git_state": r["git_state"], "hook_state_present": r["state"]["hook_state_present"]} for r in hist], "rerun_collect": {k: summary[k] for k in ("sessions_found_for_this_folder", "lines", "cli_versions_in_transcript", "entrypoints", "permissionMode_values", "lines_containing_k0_hook_text", "hook_text_found_in_transcript", "hook_related_attachment_types", "ui_interaction")}, "transcript_path": T2, "transcript_sha256": sha(T2), "rerun_transcript_copy_sha256": sha(trans_copy), "historical_transcript_copies_sha256": {os.path.basename(x): sha(x) for x in glob.glob(os.path.join(V2, "evidence", "transcript_*.jsonl"))}, "transcript": p, "seconds_tool_use_to_rejection": seconds, "screenshot": {"path": rel(png), "sha256": sha(png), "bytes": os.path.getsize(png)}, "screenshot_binding": binding, "corroborating_image": corr, "hook_verification_reason": commit_row["permissionDecisionReason"], "hook_verification_decision": commit_row["permissionDecision"], "k0_text_in_hook_verification": K0_TEXT in commit_row["permissionDecisionReason"], "work_status": git(W, "status", "--porcelain=v1").splitlines(), "work_provenance_tree_sha256": rj(os.path.join(V2, "work.provenance.json"))["tree_sha256"], "builder_same_as_v1": sha(os.path.join(V1, "_tools", "setup_k0.py")) == sha(os.path.join(V2, "_tools", "setup_k0.py")), "checker_same_as_v1": sha(os.path.join(V1, "_tools", "check_state.py")) == sha(os.path.join(V2, "_tools", "check_state.py"))}


def continuity():
    base = rj(os.path.join(V2, "_baseline", "PROTECTED_BASELINE.json"))
    now = rj(os.path.join(OUT, "_baseline", "PROTECTED_BASELINE.json"))
    bf = base.get("files", base)
    nf = now.get("files", now)
    changed = sorted(k for k in bf if k in nf and bf[k] != nf[k])
    removed = sorted(k for k in bf if k not in nf)
    return {"v2_baseline_files": len(bf), "closure_baseline_files": len(nf), "changed_since_v2_baseline": changed, "removed_since_v2_baseline": removed}


def immutable_inputs():
    names = [
        "phase54_final_acceptance_v1/release/CANDIDATE_FREEZE_MANIFEST.json", "phase54_final_acceptance_v1/release/CANDIDATE_FREEZE_MANIFEST.json.sha256", "phase54_final_acceptance_v1/release/RELEASE_PROVENANCE.md", "phase54_final_acceptance_v1/release/verify_release.py", "phase54_final_acceptance_v1/release/make_working_copy.py",
        "phase54_final_acceptance_v1/FINAL_PHASE54_CLOSURE_REPORT.md", "phase54_final_acceptance_v1/BENCHMARK_HANDOFF_CONTRACT.md", "phase54_final_acceptance_v1/ARCHITECTURE_DIFFERENCES_AND_LIMITS.md", "phase54_final_acceptance_v1/PHASE54_METRIC_LINEAGE.md", "phase54_final_acceptance_v1/LIVE_HOST_PILOT_MATRIX.jsonl", "phase54_final_acceptance_v1/LIVE_HOST_PILOT_REPORT.md",
        "phase54_cli317_host_recheck_v1/CLI317_RECHECK_REPORT.md", "phase54_cli317_host_recheck_v1/PHASE54_CLOSURE_ADDENDUM.md", "phase54_cli317_host_recheck_v1/CLI_VERSION_AND_HASH.md", "phase54_cli317_host_recheck_v1/CLI317_RECHECK_MATRIX.jsonl",
        "benchmark_readiness_fair02_cp01_v1/FAIR01_APPROVED_DISPOSITION.md", "benchmark_readiness_fair02_cp01_v1/FINAL_BENCHMARK_READINESS_DECISIONS.md", "benchmark_readiness_fair02_cp01_v1/CP01_IDE0005_REPRODUCTION_REPORT.md", "benchmark_readiness_fair02_cp01_v1/fair02/RUN_REPORT_INSTRUCTION.txt", "benchmark_readiness_fair02_cp01_v1/fair02/BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md", "benchmark_readiness_fair02_cp01_v1/fair02/INTEGRATION_CONTRACT.md", "benchmark_readiness_fair02_cp01_v1/fair02/REPORT_COMPLETENESS_RUBRIC.md", "benchmark_readiness_fair02_cp01_v1/fair02/RUN_EVIDENCE_SCHEMA.md", "benchmark_readiness_fair02_cp01_v1/fair02/assemble_prompt.py", "benchmark_readiness_fair02_cp01_v1/fair02/score_report.py",
        "step3_six_way_strictness_v1/FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md", "step3_six_way_strictness_v1/METRICS.json", "step3_six_way_strictness_v1/POLICY_SIX_WAY_MATRIX.jsonl", "step3_six_way_strictness_v1/OPEN_DECISIONS_AND_SENSITIVITY.md",
    ]
    return {n: sha(os.path.join(REC, n)) for n in names}


def main():
    facts = {"immutable_inputs": immutable_inputs(), "release": release(), "fair": fair(), "step3": step3(), "manifests": [manifest_check(FINAL), manifest_check(RCK)], "recheck": recheck(), "desktop_v1": desktop_v1(), "desktop_v2": desktop_v2(), "continuity": continuity(), "original_closure": {"report_sha256": sha(os.path.join(FINAL, "FINAL_PHASE54_CLOSURE_REPORT.md")), "state_sha256": sha(os.path.join(FINAL, "STATE.json")), "closure_review": {k: v for k, v in rj(os.path.join(FINAL, "closure_review", "CLOSURE_REVIEW.json")).items() if k in ("passed", "total", "verdict")}, "predecessor_verification": {k: v for k, v in rj(os.path.join(FINAL, "predecessor", "PREDECESSOR_VERIFICATION.json")).items() if k in ("passed", "total", "verdict")}, "predecessor_verification_sha256": sha(os.path.join(FINAL, "predecessor", "PREDECESSOR_VERIFICATION.json")), "handoff_sha256": sha(os.path.join(FINAL, "BENCHMARK_HANDOFF_CONTRACT.md"))}}
    with open(os.path.join(EV, "EVIDENCE_FACTS.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(facts, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("facts written")


if __name__ == "__main__":
    main()
