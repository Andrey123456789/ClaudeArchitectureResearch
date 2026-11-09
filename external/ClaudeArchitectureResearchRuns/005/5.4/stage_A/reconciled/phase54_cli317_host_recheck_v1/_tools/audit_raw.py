"""Independent audit of the raw session evidence. Does not import build_matrix or recheck; reads stdout.jsonl, result.json and the disk.

Usage: python -B audit_raw.py     writes RAW_EVIDENCE_AUDIT.json (exit code 0 = every check PASS)
"""
import glob
import hashlib
import json
import os
import sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(OUT, "runs")
PRED = os.path.normpath(os.path.join(OUT, "..", "phase54_final_acceptance_v1"))
REL = os.path.join(PRED, "release")
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
SHA = "26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038"
BLOCK = 'blocking because onFailure is "block"'
checks = []


def check(cid, ok, detail):
    checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(folder):
    base = os.path.join(RUNS, folder)
    res = json.load(open(os.path.join(base, "result.json"), encoding="utf-8"))
    ev = [json.loads(x) for x in open(os.path.join(base, "stdout.jsonl"), encoding="utf-8") if x.strip()]
    uses, results = [], []
    for o in ev:
        if o.get("type") == "assistant":
            uses += [b for b in o["message"]["content"] if b["type"] == "tool_use"]
        elif o.get("type") == "user" and isinstance(o["message"]["content"], list):
            results += [b for b in o["message"]["content"] if isinstance(b, dict) and b.get("type") == "tool_result"]
    return base, res, ev, uses, results


def text(b):
    c = b.get("content")
    return c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c) if isinstance(c, list) else str(c)


def effective_folders():
    out = {}
    for d in sorted(os.listdir(RUNS)):
        if not os.path.exists(os.path.join(RUNS, d, "result.json")):
            continue
        case = d.split("__a")[0]
        out[case] = max(out.get(case, d), d, key=lambda x: (x.endswith("__a2"), x))
    return out


def main():
    eff = effective_folders()
    bad_host = []
    for case, f in eff.items():
        _, r, ev, _, _ = load(f)
        init = [o for o in ev if o.get("type") == "system" and o.get("subtype") == "init"]
        if not init or init[0].get("claude_code_version") != "2.1.317" or r["exit_code"] != 0 or r["timed_out"] or r["identity_before"]["sha256"] != SHA or r["identity_after"]["sha256"] != SHA or r["identity_before"]["gate"] != "PASS" or r["identity_after"]["gate"] != "PASS":
            bad_host.append(f)
    check("R1_host_identity_every_effective_session", not bad_host, {"sessions": len(eff), "bad": bad_host})

    fault = [f"{c}-D1" for c in CANDS] + [f"{c}-D1X" for c in CANDS] + ["L1-D3", "SYN-DX1", "SYN-DX3", "SYN-DX5"]
    bad, per = [], {}
    for case in fault:
        f = eff[case]
        base, r, ev, uses, results = load(f)
        reasons = []
        if not f.endswith("__a2"):
            reasons.append("not attempt 2")
        if len(uses) != 2 or len(results) != 2:
            reasons.append(f"tool uses {len(uses)} results {len(results)}")
        for b in results:
            if not b.get("is_error") or BLOCK not in text(b):
                reasons.append("tool result is not the onFailure block: " + text(b)[:120])
        if any(o.get("subtype") == "permission_denied" for o in ev):
            reasons.append("permission_denied present")
        if os.path.exists(os.path.join(base, "work", "recheck_marker.txt")):
            reasons.append("marker on disk")
        if r["after"]["log"] != ["fixture"]:
            reasons.append("git log changed")
        if case.endswith("-D1") and not r["path_removed"]:
            reasons.append("no PATH removal recorded")
        per[case] = {"folder": f, "tool_result_first_line": text(results[0]).splitlines()[0] if results else None, "commands": [u["input"].get("command") for u in uses]}
        if reasons:
            bad.append({case: reasons})
    check("R2_fault_cases_blocked_with_marker_absent", not bad, {"cases": len(fault), "bad": bad, "per_case": per})

    def marker(case):
        base = os.path.join(RUNS, eff[case], "work")
        return os.path.exists(os.path.join(base, "recheck_marker.txt")), os.path.exists(os.path.join(base, "npm_shim_marker.txt"))

    check("R3a_control_nonblocking_hook_runs_marker", marker("SYN-DX2") == (True, False), {"SYN-DX2 marker,shim": marker("SYN-DX2")})
    check("R3b_control_shim_and_marker_can_execute", marker("SYN-SHIM") == (True, True), {"SYN-SHIM marker,shim": marker("SYN-SHIM")})
    check("R3c_control_exit2_blocks", marker("SYN-DX4") == (False, False), {"SYN-DX4 marker,shim": marker("SYN-DX4")})

    bad, per = [], {}
    for c in CANDS:
        f = eff[f"{c}-SMOKE"]
        base, r, ev, uses, results = load(f)
        reasons = []
        cu = [o["request"] for o in ev if o.get("type") == "control_request" and o["request"].get("subtype") == "can_use_tool"]
        cmds = [x["input"]["command"] for x in cu]
        if cmds != ["git commit --allow-empty -m pilot-c1", "git commit --allow-empty -m pilot-c2"]:
            reasons.append(f"can_use_tool commands {cmds}")
        if any(x.get("decision_reason_type") != "hook" for x in cu):
            reasons.append("can_use_tool not attributed to a hook")
        if [p["harness_reply"] for p in map(json.loads, open(os.path.join(base, "permission_requests.jsonl"), encoding="utf-8"))] != ["deny", "deny"]:
            reasons.append("harness replies are not exactly deny, deny")
        a = r["after"]
        if a["log"] != ["fixture"]:
            reasons.append("commit created")
        if not a["marker_present"]:
            reasons.append("allow marker absent")
        if a["npm_shim_marker_present"] or a["node_modules_present"] or a["package_lock_present"] or a["npm_cache_logs"]:
            reasons.append("npm trace present")
        stops = [o for o in ev if o.get("type") == "system" and o.get("subtype") == "hook_response" and o.get("hook_event") == "Stop"]
        blocks = [o for o in stops if o.get("exit_code") == 2 or '"decision":"block"' in (o.get("stdout") or "").replace(" ", "")]
        if len(blocks) != 1 or len(stops) != 2:
            reasons.append(f"Stop invocations {len(stops)} blocks {len(blocks)}")
        final = [o for o in ev if o.get("type") == "result"]
        if not final or final[-1].get("subtype") != "success":
            reasons.append("no successful final result")
        if len(uses) != 5:
            reasons.append(f"{len(uses)} tool uses, expected 5")
        per[c] = {"folder": f, "can_use_tool": cmds, "stop_invocations": len(stops), "stop_blocks": len(blocks), "tool_uses": len(uses)}
        if reasons:
            bad.append({c: reasons})
    check("R4_smoke_allow_deny_ask_stop", not bad, {"bad": bad, "per_candidate": per})

    replies = set()
    n = 0
    for p in glob.glob(os.path.join(RUNS, "*", "permission_requests.jsonl")):
        for line in open(p, encoding="utf-8"):
            if line.strip():
                replies.add(json.loads(line)["harness_reply"])
                n += 1
    src = open(os.path.join(OUT, "_tools", "recheck.py"), encoding="utf-8").read()
    check("R5_harness_never_approved", replies == {"deny"} and '"behavior": "allow"' not in src, {"permission_requests_seen": n, "replies": sorted(replies), "allow_reply_in_source": '"behavior": "allow"' in src})

    man = json.load(open(os.path.join(REL, "CANDIDATE_FREEZE_MANIFEST.json"), encoding="utf-8"))
    bad = []
    for d in sorted(os.listdir(RUNS)):
        cand = d.split("-")[0]
        if cand not in CANDS or not os.path.exists(os.path.join(RUNS, d, "result.json")):
            continue
        r = json.load(open(os.path.join(RUNS, d, "result.json"), encoding="utf-8"))
        s = sha(os.path.join(RUNS, d, "work", ".claude", "settings.json"))
        if s != man["candidates"][cand]["files"][".claude/settings.json"]["sha256"]:
            bad.append({d: "settings.json differs from frozen"})
        diffs = r["frozen_files_differing_after_session"]
        inj = (r["fixture"].get("fault_injection") or {}).get("file")
        if diffs != ([inj] if inj else []):
            bad.append({d: diffs})
    check("R6_candidate_config_preserved", not bad, {"bad": bad, "note": "settings.json byte-identical to frozen in every candidate fixture; only the declared injected script differs in D1X and D3"})

    res = {"checks": checks, "pass": sum(c["status"] == "PASS" for c in checks), "fail": sum(c["status"] == "FAIL" for c in checks)}
    with open(os.path.join(OUT, "RAW_EVIDENCE_AUDIT.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for c in checks:
        print(c["id"], c["status"])
    sys.exit(0 if res["fail"] == 0 else 1)


if __name__ == "__main__":
    main()
