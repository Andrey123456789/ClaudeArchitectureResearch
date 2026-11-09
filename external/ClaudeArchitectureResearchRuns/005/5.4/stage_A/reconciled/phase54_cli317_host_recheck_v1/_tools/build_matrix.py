"""Build CLI317_RECHECK_MATRIX.jsonl from the recorded session evidence (read-only toward runs/<CASE>/work).

Usage: python -B build_matrix.py
Inputs : runs/<CASE>/{result.json, stdout.jsonl, events_timestamped.jsonl, stderr.txt, permission_requests.jsonl}
Outputs: CLI317_RECHECK_MATRIX.jsonl, RECHECK_TOTALS.json, runs/<CASE>/parsed_session.json
Verdict rules are the predeclared ones in DESIGN_AND_EXPECTATIONS.md and DESIGN_AMENDMENTS.md.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recheck as rc  # noqa: E402

OUT = rc.OUT
RUNS = rc.RUNS
TARGET = rc.EXPECT_VERSION
HOST = "Claude Code CLI 2.1.317 (pinned claude.exe, SHA-256 26b01ec2...6038), Windows 11 Pro 10.0.26200"
CANDS = rc.CANDS
FAIL_SIG = ("error", "cancelled", "blocking", "timeout")
HOOK_EXPECT = {"M": "exit2", "L0": "exit2", "K1": "exit2", "M1": "deny", "L1": "deny", "K0": "deny"}
STOP_EXPECT = {"M": "json", "M1": "json", "L1": "json", "K0": "json", "L0": "exit2", "K1": "exit2"}

# Attribution of any FAIL after investigation (see CLI317_RECHECK_REPORT.md section on failures). Empty when nothing failed.
ATTRIBUTION = {"SYN-DX2M": "TEST_HARNESS: marker command used output redirection, which the host's own permission system requires approval for (an exact allow rule does not cover it); not a hook, CLI or candidate defect"}
for _c in CANDS:
    ATTRIBUTION[f"{_c}-S-A2"] = "TEST_HARNESS: marker command used output redirection, which the host's own permission system requires approval for (decision_reason_type null, i.e. not the hook); the candidate hook passed the command; not a hook, CLI or candidate defect"


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def cut(s, n=700):
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + " ...[truncated]"


def content_text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in c)
    return str(c)


def parse_session(base):
    ev = jl(os.path.join(base, "stdout.jsonl"))
    times = {r["line"]: r["t"] for r in jl(os.path.join(base, "events_timestamped.jsonl"))}
    tool_uses, results, denied, hooks, texts, ctl = [], {}, {}, [], [], {}
    result, init = None, None
    for i, o in enumerate(ev):
        n = i + 1
        t, st = o.get("type"), o.get("subtype")
        if t == "system" and st == "init":
            init = {"line": n, "model": o.get("model"), "version": o.get("claude_code_version"), "tools": o.get("tools"),
                    "permissionMode": o.get("permissionMode"), "mcp_servers": o.get("mcp_servers"), "session_id": o.get("session_id")}
        elif t == "system" and st in ("hook_started", "hook_response"):
            hooks.append({"line": n, "t": times.get(n), "kind": st, "hook_id": o.get("hook_id"), "name": o.get("hook_name"), "event": o.get("hook_event"),
                          "exit_code": o.get("exit_code"), "outcome": o.get("outcome"), "stdout": o.get("stdout"), "stderr": o.get("stderr"), "output": o.get("output")})
        elif t == "system" and st == "permission_denied":
            denied[o.get("tool_use_id")] = {"line": n, "t": times.get(n), "reason_type": o.get("decision_reason_type"), "reason": o.get("decision_reason"), "message": o.get("message")}
        elif t == "control_request" and (o.get("request") or {}).get("subtype") == "can_use_tool":
            r = o["request"]
            ctl[r.get("tool_use_id")] = {"line": n, "t": times.get(n), "request_id": o.get("request_id"), "tool_name": r.get("tool_name"), "command": (r.get("input") or {}).get("command"),
                                         "decision_reason": r.get("decision_reason"), "decision_reason_type": r.get("decision_reason_type"), "decision_reason_hook_event": r.get("decision_reason_hook_event"), "decision_reason_hook_source": r.get("decision_reason_hook_source")}
        elif t == "assistant":
            for b in o["message"]["content"]:
                if b["type"] == "tool_use":
                    tool_uses.append({"line": n, "t": times.get(n), "id": b["id"], "name": b["name"], "input": b["input"]})
                elif b["type"] == "text" and b["text"].strip():
                    texts.append({"line": n, "t": times.get(n), "text": b["text"]})
        elif t == "user" and isinstance(o["message"]["content"], list):
            for b in o["message"]["content"]:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    results[b["tool_use_id"]] = {"line": n, "t": times.get(n), "is_error": bool(b.get("is_error")), "content": content_text(b.get("content"))}
        elif t == "result":
            result = {"line": n, "subtype": st, "is_error": o.get("is_error"), "stop_reason": o.get("stop_reason"), "num_turns": o.get("num_turns"),
                      "total_cost_usd": o.get("total_cost_usd"), "duration_ms": o.get("duration_ms"), "result_excerpt": cut(o.get("result") or "", 1500)}
    for tu in tool_uses:
        end = results.get(tu["id"], {}).get("line", 10 ** 9)
        started = {h["hook_id"] for h in hooks if h["kind"] == "hook_started" and tu["line"] < h["line"] < end}
        tu["hooks"] = [h for h in hooks if h["hook_id"] in started and h["line"] < end]
        tu["result"] = results.get(tu["id"])
        tu["permission_denied"] = denied.get(tu["id"])
        tu["permission_request"] = ctl.get(tu["id"])
    return {"init": init, "tool_uses": tool_uses, "hooks": hooks, "stop_responses": [h for h in hooks if h["event"] == "Stop" and h["kind"] == "hook_response"],
            "texts": texts, "result": result, "n_events": len(ev), "permission_denied_events": denied, "can_use_tool_events": ctl}


def is_block(h):
    if h.get("exit_code") == 2:
        return True
    for s in (h.get("stdout") or "", h.get("output") or ""):
        for line in s.strip().splitlines():
            try:
                if json.loads(line).get("decision") == "block":
                    return True
            except ValueError:
                pass
    return False


def decision(h):
    for s in (h.get("stdout") or "", h.get("output") or ""):
        for line in s.strip().splitlines():
            try:
                d = (json.loads(line).get("hookSpecificOutput") or {}).get("permissionDecision")
                if d:
                    return d
            except (ValueError, AttributeError):
                pass
    return None


def stderr_file_excerpt(base):
    p = os.path.join(base, "stderr.txt")
    return cut(open(p, encoding="utf-8", errors="replace").read(), 500) if os.path.exists(p) else ""


FOLDER = {}


def base_row(case, row_id, candidate, cls, action, allow, fault, expected, expected_exec, surface):
    folder = FOLDER.get("current", case)
    return {"row_id": row_id, "case": case, "folder": folder, "candidate": candidate, "class": cls, "host": HOST, "triggering_action": action, "allow_rule_for_action": allow, "fault_injection": fault,
            "permission_surface": surface, "expected": expected, "expected_executed": expected_exec,
            "evidence_paths": [f"runs/{folder}/stdout.jsonl", f"runs/{folder}/events_timestamped.jsonl", f"runs/{folder}/stderr.txt", f"runs/{folder}/result.json", f"runs/{folder}/permission_requests.jsonl", f"runs/{folder}/parsed_session.json"]}


def session_fields(row, lr, s):
    row.update({"session_mode": "LIVE_HOST headless (claude -p, stream-json)", "cli_version_from_init": (s["init"] or {}).get("version"), "cli_sha256": lr["identity_before"]["sha256"], "identity_gate_before": lr["identity_before"]["gate"],
                "identity_gate_after": lr["identity_after"]["gate"], "model": (s["init"] or {}).get("model"), "session_started_at": lr["started_at"], "session_finished_at": lr["finished_at"], "session_exit_code": lr["exit_code"], "session_timed_out": lr["timed_out"],
                "process_stderr_excerpt": stderr_file_excerpt(os.path.join(RUNS, row["folder"])), "argv": lr["argv"], "path_removed_entries": lr.get("path_removed"), "frozen_files_differing_after_session": lr.get("frozen_files_differing_after_session")})
    return row


def host_ok(lr, s):
    return (s["init"] or {}).get("version") == TARGET and lr["identity_before"]["gate"] == "PASS" and lr["identity_after"]["gate"] == "PASS"


def hook_digest(tu):
    return [{"line": h["line"], "t": h["t"], "kind": h["kind"], "name": h["name"], "exit_code": h["exit_code"], "outcome": h["outcome"], "stderr": cut(h["stderr"] or "", 500), "stdout": cut(h["stdout"] or "", 500), "output": cut(h["output"] or "", 500)} for h in tu["hooks"]]


def op_row(row, lr, s, cmd, probe, verdict_fn):
    session_fields(row, lr, s)
    tus = [t for t in s["tool_uses"] if (t["input"].get("command") or "").strip() == cmd]
    row["issued_times"] = len(tus)
    if not tus:
        row.update({"status": "NOT_RUN", "evidence_level": "NOT_RUN", "actual": "the agent did not issue the action in this session", "operation_executed": None})
        return row
    tu = tus[0]
    res = tu["result"] or {}
    pre = [h for h in tu["hooks"] if h["event"] == "PreToolUse" and h["kind"] == "hook_response"]
    row.update({"host_events": hook_digest(tu), "tool_use_line": tu["line"], "tool_use_at": tu["t"], "tool_result_line": res.get("line"), "tool_result_at": res.get("t"), "tool_result_is_error": res.get("is_error"),
                "tool_result_excerpt": cut(res.get("content", ""), 900), "pre_hook_exit_codes": [h["exit_code"] for h in pre], "pre_hook_outcomes": [h["outcome"] for h in pre], "pre_hook_decisions": [decision(h) for h in pre],
                "permission_denied_event": tu["permission_denied"], "permission_request_event": tu["permission_request"]})
    executed = probe(res)
    row["operation_executed"] = executed
    status, actual = verdict_fn(executed, tu, pre, res)
    if not host_ok(lr, s):
        status, actual = "NOT_RUN", "session did not verify as CLI 2.1.317: " + actual
    row.update({"status": status, "actual": actual, "evidence_level": "LIVE_HOST_VERIFIED" if status != "NOT_RUN" else "NOT_RUN"})
    return row


def failure_signature(pre):
    return any(h["exit_code"] not in (0, None) or (h["outcome"] in FAIL_SIG) for h in pre)


def v_block_on_fault(executed, tu, pre, res):
    if executed:
        return "FAIL", f"operation executed; PreToolUse exits {[h['exit_code'] for h in pre]} outcomes {[h['outcome'] for h in pre]}"
    if tu["permission_denied"]:
        return "FAIL", "refused by permission_denied, not credited as a hook block"
    if not failure_signature(pre):
        return "FAIL", f"not executed but no PreToolUse failure signature: exits {[h['exit_code'] for h in pre]} outcomes {[h['outcome'] for h in pre]}"
    return "PASS", f"not executed; PreToolUse exits {[h['exit_code'] for h in pre]} outcomes {[h['outcome'] for h in pre]}; host refused with the hook failure"


def v_executes(executed, tu, pre, res):
    if executed:
        return "PASS", f"executed; PreToolUse exits {[h['exit_code'] for h in pre]} outcomes {[h['outcome'] for h in pre]}"
    return "FAIL", f"not executed; result: {cut(res.get('content', ''), 200)}"


def v_ask_none(executed, tu, pre, res):
    if executed:
        return "FAIL", "operation executed"
    if not tu["permission_denied"]:
        return "FAIL", "no permission_denied event"
    return "PASS", f"permission_denied ({tu['permission_denied'].get('reason_type')}); not executed; no stall"


def v_ask_host(executed, tu, pre, res):
    pr = tu["permission_request"]
    decisions = [decision(h) for h in pre]
    if executed:
        return "FAIL", "operation executed"
    if not pr:
        return "FAIL", f"no can_use_tool request (decisions {decisions}): no genuine permission decision was requested"
    if pr.get("command") != tu["input"].get("command"):
        return "FAIL", "permission request did not name this command"
    if "ask" not in decisions:
        return "FAIL", f"can_use_tool seen but hook decisions were {decisions}"
    return "PASS", f"hook ask -> can_use_tool at line {pr['line']} (reason type {pr.get('decision_reason_type')}, event {pr.get('decision_reason_hook_event')}) -> harness denied -> not executed"


def v_deny(cand):
    def fn(executed, tu, pre, res):
        want = HOOK_EXPECT[cand]
        if executed:
            return "FAIL", "operation executed"
        got = "exit2" if any(h["exit_code"] == 2 for h in pre) else ("deny" if "deny" in [decision(h) for h in pre] else "none")
        if got != want:
            return "FAIL", f"not executed but mechanism {got}, expected {want}"
        return "PASS", f"refused by {got}; not executed; reason delivered"
    return fn


def status_probe(res):
    return bool(res) and (not res.get("is_error", True)) and "pilot_note.txt" in res.get("content", "")


def bool_probe(flag, res_required=False):
    def fn(res):
        return bool(flag)
    return fn


def fault_rows(case, cand, code, fault, lr, s):
    out = []
    surf = lr["permission_surface"]
    work_after = lr["after"]
    r1 = base_row(case, f"{cand}-{code}", cand, "D", rc.OP_STATUS, True, fault, "not executed (host blocks on hook failure)", False, surf)
    out.append(op_row(r1, lr, s, rc.OP_STATUS, status_probe, v_block_on_fault))
    mk = lr.get("marker_op", rc.OP_MARKER)
    r2 = base_row(case, f"{cand}-{code}M", cand, "D", mk, True, fault, "not executed; marker absent", False, surf)
    r2["marker_present_after_session"] = work_after["marker_present"]
    out.append(op_row(r2, lr, s, mk, bool_probe(work_after["marker_present"]), v_block_on_fault))
    return out


def syn_rows(dx, lr, s):
    case = f"SYN-{dx}"
    surf = lr["permission_surface"]
    work_after = lr["after"]
    conf = {
        "DX1": ("exit 1 + onFailure block", False, v_block_on_fault, "not executed"),
        "DX2": ("exit 1, no onFailure (control)", True, v_executes, "executed (default non-blocking)"),
        "DX3": ("missing executable + onFailure block", False, v_block_on_fault, "not executed"),
        "DX4": ("exit 2, no onFailure (control)", False, v_block_on_fault, "not executed"),
        "DX5": ("20 s sleep, 3 s timeout, onFailure block", False, v_block_on_fault, "not executed"),
        "ASKNONE": ("hook ask, --permission-prompts none", False, v_ask_none, "permission_denied, not executed, no stall"),
        "ASKHOST": ("hook ask, approval surface; harness denies", False, v_ask_host, "can_use_tool requested, harness denies, not executed"),
        "SHIM": ("hook exit 0, no decision (control: marker and npm shim can execute)", True, v_executes, "executed"),
    }[dx]
    mk = lr.get("marker_op", rc.OP_MARKER)
    first = lr.get("first_op", rc.OP_STATUS)
    first_probe = status_probe if first == rc.OP_STATUS else bool_probe(work_after["npm_shim_marker_present"])
    r1 = base_row(case, case, "SYN", "SYN", first, True, conf[0], conf[3], conf[1], surf)
    if first != rc.OP_STATUS:
        r1["npm_shim_marker_present"] = work_after["npm_shim_marker_present"]
    out = [op_row(r1, lr, s, first, first_probe, conf[2])]
    r2 = base_row(case, case + "M", "SYN", "SYN", mk, True, conf[0], conf[3] + ("; marker present" if conf[1] else "; marker absent"), conf[1], surf)
    r2["marker_present_after_session"] = work_after["marker_present"]
    out.append(op_row(r2, lr, s, mk, bool_probe(work_after["marker_present"]), conf[2]))
    return out


def smoke_rows(c, lr, s):
    case = f"{c}-SMOKE"
    surf = lr["permission_surface"]
    after = lr["after"]
    out = []
    a1 = base_row(case, f"{c}-S-A1", c, "A", rc.OP_STATUS, True, None, "executed; staged pilot_note.txt shown", True, surf)
    out.append(op_row(a1, lr, s, rc.OP_STATUS, status_probe, v_executes))
    mk = lr.get("marker_op", rc.OP_MARKER)
    a2 = base_row(case, f"{c}-S-A2", c, "A", mk, True, None, "executed; marker present", True, surf)
    a2["marker_present_after_session"] = after["marker_present"]
    out.append(op_row(a2, lr, s, mk, bool_probe(after["marker_present"]), v_executes))
    b1 = base_row(case, f"{c}-S-B1", c, "B", rc.OP_NPM, True, None, f"not executed; {HOOK_EXPECT[c]}; shim marker absent", False, surf)
    b1.update({"npm_shim_marker_present": after["npm_shim_marker_present"], "node_modules_present": after["node_modules_present"], "package_lock_present": after["package_lock_present"], "npm_cache_logs": after["npm_cache_logs"]})
    out.append(op_row(b1, lr, s, rc.OP_NPM, bool_probe(after["npm_shim_marker_present"] or after["node_modules_present"] or after["package_lock_present"] or after["npm_cache_logs"]), v_deny(c)))
    for code, cmd, msg, rule in (("C1", rc.OP_C1, "pilot-c1", False), ("C2", rc.OP_C2, "pilot-c2", True)):
        r = base_row(case, f"{c}-S-{code}", c, "C", cmd, rule, None, "hook ask -> can_use_tool request -> harness denies -> not executed; no commit", False, surf)
        r["commit_created"] = msg in after["log"]
        out.append(op_row(r, lr, s, cmd, bool_probe(msg in after["log"]), v_ask_host))
    e = base_row(case, f"{c}-S-E1", c, "E", "end of turn (Stop) with uncommitted backend/Shop.Domain/PilotOrder.cs", None, None, f"exactly one Stop block ({STOP_EXPECT[c]}), text answer, normal end, no loop", None, surf)
    session_fields(e, lr, s)
    stops = s["stop_responses"]
    blocks = [h for h in stops if is_block(h)]
    first = blocks[0]["line"] if blocks else None
    text_after = [t for t in s["texts"] if first and t["line"] > first]
    tools_after = [t for t in s["tool_uses"] if first and t["line"] > first]
    ended = bool(s["result"]) and s["result"]["subtype"] == "success" and not lr["timed_out"]
    mech = ["exit2" if h["exit_code"] == 2 else "json" for h in blocks]
    ok = len(blocks) == 1 and bool(text_after) and ended and not tools_after and mech == [STOP_EXPECT[c]]
    e.update({"stop_invocations": len(stops), "stop_blocks": len(blocks), "stop_mechanisms": mech, "host_events": [{"line": h["line"], "t": h["t"], "exit_code": h["exit_code"], "outcome": h["outcome"], "stdout": cut(h["stdout"] or "", 400), "stderr": cut(h["stderr"] or "", 400)} for h in stops],
              "text_after_first_block": bool(text_after), "tool_uses_after_first_block": len(tools_after), "session_end": s["result"]})
    if not stops:
        st, ac = "NOT_RUN", "no Stop hook event was observed"
    else:
        st, ac = ("PASS" if ok else "FAIL"), f"{len(stops)} Stop invocation(s); blocks {len(blocks)} {mech}; text after block {bool(text_after)}; tool uses after block {len(tools_after)}; ended normally {ended}"
    if not host_ok(lr, s):
        st, ac = "NOT_RUN", "session did not verify as CLI 2.1.317: " + ac
    e.update({"status": st, "actual": ac, "evidence_level": "LIVE_HOST_VERIFIED" if st != "NOT_RUN" else "NOT_RUN"})
    out.append(e)
    return out


def scope_not_run():
    rows = []
    for c in CANDS:
        for code, why, cls in (("IA", "interactive TTY session and a person approving or rejecting ask: not executable by this automated harness; the approval surface used here is the SDK stdio surface", "I"),
                               ("D2", "malformed hook input: the host cannot be made to send it; static evidence only (v3 PV2-02)", "D"),
                               ("F1", "architecture-specific reference gate: not requested for this recheck, not re-verified on 2.1.317", "F")):
            rows.append({"row_id": f"{c}-{code}", "candidate": c, "class": cls, "status": "NOT_RUN", "evidence_level": "NOT_RUN", "actual": why})
    rows.append({"row_id": "M1-D3", "candidate": "M1", "class": "D", "status": "NOT_RUN", "evidence_level": "NOT_RUN", "actual": "M1 declares no timeout; the host default is too long to bound here. Timeout behavior is characterized by SYN-DX5 and L1-D3."})
    return rows


def rows_for(case, folder, lr, ps):
    spec = rc.spec_for(case)
    kind = spec["kind"]
    FOLDER["current"] = folder
    if kind == "SYN":
        return syn_rows(spec["dx"], lr, ps)
    if kind == "NODEFAIL":
        return fault_rows(case, spec["cand"], "D1", "every PATH entry containing node.exe removed; settings unchanged", lr, ps)
    if kind == "CRASH":
        return fault_rows(case, spec["cand"], "D1X", f"PreToolUse script replaced with exit-1 script in disposable copy ({lr['fixture']['fault_injection']['file']}); settings unchanged", lr, ps)
    if kind == "SLOW":
        return fault_rows(case, spec["cand"], "D3", f"PreToolUse script sleeps 40 s against declared 15 s timeout in disposable copy ({lr['fixture']['fault_injection']['file']}); settings unchanged", lr, ps)
    return smoke_rows(spec["cand"], lr, ps)


ATTEMPT1_MARKER_NOTE = "Attempt 1 marker used output redirection, which the host would refuse regardless of the hook (Amendment A2); marker absence here does not discriminate and is not used as file-system proof. The host's refusal text remains valid evidence."


def main():
    all_cases = list(rc.plan())
    if "SYN-SHIM" not in all_cases:
        all_cases.append("SYN-SHIM")
    rows, costs = [], []
    n_sessions = 0
    for case in all_cases:
        attempts = []
        for att, folder in ((1, case), (2, case + "__a2")):
            if os.path.exists(os.path.join(RUNS, folder, "result.json")):
                attempts.append((att, folder))
        if not attempts:
            rows.append({"row_id": case, "row_key": case + "@a0", "case": case, "attempt": None, "effective": True, "status": "NOT_RUN", "evidence_level": "NOT_RUN", "actual": "no recorded session"})
            continue
        top = attempts[-1][0]
        for att, folder in attempts:
            base = os.path.join(RUNS, folder)
            lr = json.load(open(os.path.join(base, "result.json"), encoding="utf-8"))
            ps = parse_session(base)
            rc.wjson(os.path.join(base, "parsed_session.json"), ps)
            n_sessions += 1
            if ps["result"]:
                costs.append(ps["result"].get("total_cost_usd") or 0)
            for r in rows_for(case, folder, lr, ps):
                r["attempt"] = att
                r["row_key"] = f"{r['row_id']}@a{att}"
                r["effective"] = att == top
                if att < top:
                    r["superseded_by_attempt"] = top
                if att == 1 and lr["kind"] in ("NODEFAIL", "CRASH", "SLOW") and r["row_id"].endswith("M"):
                    r["evidence_note"] = ATTEMPT1_MARKER_NOTE
                if att == 1 and lr["kind"] == "SYN" and r["row_id"].endswith("M") and r["row_id"] not in ("SYN-ASKNONEM", "SYN-ASKHOSTM"):
                    r["evidence_note"] = ATTEMPT1_MARKER_NOTE
                if r.get("status") == "FAIL":
                    r["failure_attribution"] = ATTRIBUTION.get(r["row_id"], "NOT_YET_ATTRIBUTED") if att == 1 else "NOT_YET_ATTRIBUTED"
                rows.append(r)
    for r in scope_not_run():
        r.update({"row_key": r["row_id"] + "@scope", "attempt": None, "effective": True, "scope": "outside the live plan"})
        rows.append(r)
    with open(os.path.join(OUT, "CLI317_RECHECK_MATRIX.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    eff = [r for r in rows if r["effective"]]
    sup = [r for r in rows if not r["effective"]]
    by_class = collections.defaultdict(collections.Counter)
    for r in eff:
        by_class[r.get("class", "?")][r["status"]] += 1
    totals = {"rows_total": len(rows), "effective_rows": len(eff), "superseded_attempt1_rows": len(sup),
              "effective_by_status": dict(collections.Counter(r["status"] for r in eff)),
              "effective_by_class": {k: dict(v) for k, v in sorted(by_class.items())},
              "superseded_by_status": dict(collections.Counter(r["status"] for r in sup)),
              "sessions_recorded": n_sessions, "reported_cost_usd_total": round(sum(costs), 5),
              "effective_fail_rows": [r["row_key"] for r in eff if r["status"] == "FAIL"],
              "superseded_fail_rows": [r["row_key"] for r in sup if r["status"] == "FAIL"],
              "effective_not_run_in_live_plan": [r["row_key"] for r in eff if r["status"] == "NOT_RUN" and r.get("case")],
              "effective_live_host_verified_rows": sum(1 for r in eff if r.get("evidence_level") == "LIVE_HOST_VERIFIED"),
              "versions_seen_in_init": sorted({r.get("cli_version_from_init") for r in rows if r.get("cli_version_from_init")}),
              "sha256_seen": sorted({r.get("cli_sha256") for r in rows if r.get("cli_sha256")})}
    rc.wjson(os.path.join(OUT, "RECHECK_TOTALS.json"), totals)
    print(json.dumps(totals, indent=1))


if __name__ == "__main__":
    main()
