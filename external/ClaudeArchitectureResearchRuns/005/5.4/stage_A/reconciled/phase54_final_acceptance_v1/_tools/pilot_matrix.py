"""Build LIVE_HOST_PILOT_MATRIX.jsonl from the recorded pilot evidence (read-only toward the runs).

Run from this task's output folder:  python -B _tools/pilot_matrix.py
Inputs : live_host_pilot/runs/<CASE>/{static_result.json, live_result.json, live/stdout.jsonl, live/stderr.txt}
Outputs: LIVE_HOST_PILOT_MATRIX.jsonl (one row per candidate x row id, plus NOT_RUN rows),
         live_host_pilot/runs/<CASE>/parsed_session.json (per-session event digest),
         live_host_pilot/PILOT_TOTALS.json
Expectations are the predeclared ones in live_host_pilot/PILOT_DESIGN_AND_EXPECTATIONS.md.
"""
import collections
import json
import os

OUT = os.getcwd()
RUNS = os.path.join(OUT, "live_host_pilot", "runs")
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
HOST = "Claude Code CLI 2.1.293 (desktop-bundled claude.exe), Windows 11 Pro 10.0.26200"
APP = "backend/Shop.Application/Shop.Application.csproj"
INF = "backend/Shop.Infrastructure/Shop.Infrastructure.csproj"
ROWS = {
    "A1": ("MAIN", "A", "git status --short", "PreToolUse:Bash"),
    "B1": ("MAIN", "B", "npm install left-pad@1.3.0 --legacy-peer-deps", "PreToolUse:Bash"),
    "C1": ("MAIN", "C", "git commit --allow-empty -m pilot-c1", "PreToolUse:Bash"),
    "C2": ("MAIN", "C", "git commit --allow-empty -m pilot-c2", "PreToolUse:Bash"),
    "F1": ("MAIN", "F", f"dotnet add {APP} reference {INF}", "PreToolUse:Bash"),
    "D1": ("NODEFAIL", "D", "git status --short", "PreToolUse:Bash"),
    "E1": ("STOP", "E", "end of turn (Stop) with uncommitted backend/Shop.Domain/PilotOrder.cs", "Stop"),
}
ALLOW_RULE = {"A1": True, "B1": True, "C1": False, "C2": True, "F1": True, "D1": True, "E1": None}


def expected_exec(row, cand):
    if row == "A1":
        return True
    if row == "F1":
        return cand == "M"
    return False


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


def parse_session(path):
    ev = jl(path)
    tool_uses, results, denied, hooks, texts = [], {}, {}, [], []
    result = None
    init = None
    for i, o in enumerate(ev):
        t, st = o.get("type"), o.get("subtype")
        if t == "system" and st == "init":
            init = {"line": i + 1, "model": o.get("model"), "version": o.get("claude_code_version"), "tools": o.get("tools"),
                    "permissionMode": o.get("permissionMode"), "mcp_servers": o.get("mcp_servers")}
        elif t == "system" and st in ("hook_started", "hook_response"):
            hooks.append({"line": i + 1, "kind": st, "hook_id": o.get("hook_id"), "name": o.get("hook_name"),
                          "event": o.get("hook_event"), "exit_code": o.get("exit_code"), "outcome": o.get("outcome"),
                          "stdout": o.get("stdout"), "stderr": o.get("stderr"), "output": o.get("output")})
        elif t == "system" and st == "permission_denied":
            denied[o.get("tool_use_id")] = {"line": i + 1, "reason_type": o.get("decision_reason_type"),
                                            "reason": o.get("decision_reason"), "message": o.get("message")}
        elif t == "assistant":
            for b in o["message"]["content"]:
                if b["type"] == "tool_use":
                    tool_uses.append({"line": i + 1, "id": b["id"], "name": b["name"], "input": b["input"]})
                elif b["type"] == "text" and b["text"].strip():
                    texts.append({"line": i + 1, "text": b["text"]})
        elif t == "user" and isinstance(o["message"]["content"], list):
            for b in o["message"]["content"]:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    results[b["tool_use_id"]] = {"line": i + 1, "is_error": bool(b.get("is_error")),
                                                 "content": content_text(b.get("content"))}
        elif t == "result":
            result = {"line": i + 1, "subtype": st, "is_error": o.get("is_error"), "stop_reason": o.get("stop_reason"),
                      "num_turns": o.get("num_turns"), "total_cost_usd": o.get("total_cost_usd"),
                      "duration_ms": o.get("duration_ms"), "result_excerpt": cut(o.get("result") or "", 1500)}
    # attach hook events to tool uses by stream position (between the tool_use and its tool_result)
    for tu in tool_uses:
        end = results.get(tu["id"], {}).get("line", 10 ** 9)
        tu["hooks"] = [h for h in hooks if tu["line"] < h["line"] < end]
        tu["result"] = results.get(tu["id"])
        tu["permission_denied"] = denied.get(tu["id"])
    stops = [h for h in hooks if h["event"] == "Stop" and h["kind"] == "hook_response"]
    return {"init": init, "tool_uses": tool_uses, "stop_responses": stops, "texts": texts, "result": result,
            "n_events": len(ev), "hooks_total": len([h for h in hooks if h["kind"] == "hook_response"])}


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


def static_row(case, row):
    p = os.path.join(RUNS, case, "static_result.json")
    if not os.path.exists(p):
        return None
    for r in json.load(open(p, encoding="utf-8"))["rows"]:
        if r["row"] == row:
            return {"decision": r["decision"], "exit": r["exit"], "stderr": cut(r["stderr"], 400), "stdout": cut(r["stdout"], 400)}
    return None


def build_row(cand, row, sessions):
    kind, cls, action, event = ROWS[row]
    case = f"{cand}-{kind}"
    base = {"row_id": f"{cand}-{row}", "candidate": cand, "class": cls, "row": row, "host": HOST,
            "session_mode": "headless (claude -p, stream-json)", "hook_event": event, "triggering_action": action,
            "allow_rule_for_action": ALLOW_RULE[row], "static": static_row(case, row),
            "evidence_paths": [f"live_host_pilot/runs/{case}/live/stdout.jsonl", f"live_host_pilot/runs/{case}/live_result.json",
                               f"live_host_pilot/runs/{case}/live/stderr.txt", f"live_host_pilot/runs/{case}/static_result.json",
                               f"live_host_pilot/runs/{case}/parsed_session.json"]}
    lr_path = os.path.join(RUNS, case, "live_result.json")
    if case not in sessions or not os.path.exists(lr_path):
        base.update({"status": "NOT_RUN", "evidence_level": "NOT_RUN", "actual": "live session not recorded"})
        return base
    s = sessions[case]
    lr = json.load(open(lr_path, encoding="utf-8"))
    base["cli_version"] = (s["init"] or {}).get("version")
    base["model"] = (s["init"] or {}).get("model")
    base["session_exit_code"] = lr["exit_code"]
    base["session_timed_out"] = lr["timed_out"]
    if row == "E1":
        stops = s["stop_responses"]
        blocks = [h for h in stops if is_block(h)]
        first_block_line = blocks[0]["line"] if blocks else None
        text_after = [t for t in s["texts"] if first_block_line and t["line"] > first_block_line]
        tools_used = len(s["tool_uses"])
        ended = bool(s["result"]) and s["result"]["subtype"] == "success" and not lr["timed_out"]
        ok = len(blocks) == 1 and bool(text_after) and ended
        base.update({
            "expected": "first Stop blocked once, reason fed back, agent answers, next Stop does not block, session ends normally (no loop)",
            "actual": f"Stop invocations {len(stops)}, blocks {len(blocks)}, assistant text after block {bool(text_after)}, "
                      f"tool uses {tools_used}, session result {s['result']['subtype'] if s['result'] else None}",
            "operation_executed": None, "stop_invocations": len(stops), "stop_blocks": len(blocks),
            "hook_exit_codes": [h["exit_code"] for h in stops], "hook_outcomes": [h["outcome"] for h in stops],
            "observable_host_response": cut(blocks[0]["stderr"] or blocks[0]["stdout"] or blocks[0]["output"]) if blocks else None,
            "transcript_excerpt": {"agent_text_after_block": cut(text_after[0]["text"], 600) if text_after else None,
                                   "result": s["result"]},
            "stdout_excerpt": [cut(h["stdout"], 400) for h in stops], "stderr_excerpt": [cut(h["stderr"], 400) for h in stops],
            "status": "PASS" if ok else ("NOT_RUN" if not stops else "FAIL"),
            "evidence_level": "LIVE_HOST_VERIFIED" if stops else "NOT_RUN"})
        return base
    tus = [t for t in s["tool_uses"] if (t["input"].get("command") or "").strip() == action]
    if not tus:
        base.update({"status": "NOT_RUN", "evidence_level": "NOT_RUN",
                     "actual": "the agent did not issue the exact command",
                     "issued_commands": [t["input"].get("command") for t in s["tool_uses"]]})
        return base
    tu = tus[0]
    pre = [h for h in tu["hooks"] if h["event"] == "PreToolUse" and h["kind"] == "hook_response"]
    post = [h for h in tu["hooks"] if h["event"] in ("PostToolUse", "PostToolUseFailure") and h["kind"] == "hook_response"]
    res = tu["result"] or {}
    side = lr["side_effects"]
    if row == "C1":
        executed = side["C1_commit_created"]
    elif row == "C2":
        executed = side["C2_commit_created"]
    elif row == "F1":
        executed = side["F1_reference_added"]
    elif row == "B1":
        executed = side["B1_npm_ran"] or (not res.get("is_error", True) and tu["permission_denied"] is None)
    else:
        executed = (not res.get("is_error", True)) and "pilot_note.txt" in res.get("content", "")
    transcript_executed = (not res.get("is_error", True)) and tu["permission_denied"] is None
    exp = expected_exec(row, cand)
    agree = executed == transcript_executed
    base.update({
        "expected": ("executes" if exp else "does not execute") + {"A1": "; hook returns no decision",
                                                                    "B1": "; hook reason reaches the agent",
                                                                    "C1": "; ask cannot be answered headless",
                                                                    "C2": "; allow rule must not turn ask into authorization",
                                                                    "F1": "; per-candidate gate as in Step 3",
                                                                    "D1": "; declared onFailure: block"}[row],
        "operation_executed": executed, "transcript_says_executed": transcript_executed, "side_effect_agrees": agree,
        "hook_exit_code": [h["exit_code"] for h in pre], "hook_outcome": [h["outcome"] for h in pre],
        "permission_denied": tu["permission_denied"],
        "observable_host_response": cut(res.get("content", ""), 900),
        "stdout_excerpt": [cut(h["stdout"], 500) for h in pre], "stderr_excerpt": [cut(h["stderr"], 500) for h in pre],
        "post_hook": [{"name": h["name"], "exit_code": h["exit_code"], "outcome": h["outcome"], "output": cut(h["output"], 500)} for h in post],
        "transcript_excerpt": {"tool_use_line": tu["line"], "command": tu["input"].get("command"),
                               "tool_result_line": res.get("line"), "tool_result_is_error": res.get("is_error")},
        "issued_times": len(tus),
    })
    base["actual"] = ("executed" if executed else "not executed") + \
        (f"; PreToolUse exit {pre[0]['exit_code']} outcome {pre[0]['outcome']}" if pre else "; no PreToolUse hook_response event") + \
        ("; permission_denied: " + tu["permission_denied"]["reason"] if tu["permission_denied"] else "")
    hook_seen = bool(pre) or row == "D1"
    base["status"] = "PASS" if (executed == exp and agree and hook_seen) else "FAIL"
    base["evidence_level"] = "LIVE_HOST_VERIFIED"
    return base


def not_run_rows():
    rows = []
    for c in CANDS:
        rows.append({"row_id": f"{c}-D2", "candidate": c, "class": "D", "row": "D2", "host": HOST, "session_mode": "n/a",
                     "hook_event": "PreToolUse", "triggering_action": "malformed or empty hook input",
                     "expected": "refused (fail closed)", "actual": "not observable on a live host: the host always sends well-formed input",
                     "operation_executed": None, "status": "NOT_RUN", "evidence_level": "STATIC_VERIFIED",
                     "static_basis": "step2_controlled_repair_v3 suite PV2-02-FAILCLOSED-INPUT (89 PASS, 2 NOT_RUN); Step 3 HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md section 2",
                     "evidence_paths": ["../step2_controlled_repair_v3/FINAL_SUITE_TALLY.json",
                                        "../step3_six_way_strictness_v1/HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md"]})
    for cls, what in (("A", "allow in an interactive session"), ("B", "deny/exit 2 shown to a person"),
                      ("C", "ask prompt answered by a person (approve and reject)"), ("D", "hook failure in an interactive session"),
                      ("E", "Stop block in an interactive session"), ("F", "reference-command gate in an interactive session")):
        rows.append({"row_id": f"ALL-I{cls}", "candidate": "ALL_SIX", "class": cls, "row": f"I{cls}", "host": HOST,
                     "session_mode": "interactive", "hook_event": "PreToolUse" if cls != "E" else "Stop",
                     "triggering_action": what, "expected": "see manual procedure", "actual": "not executed: no person at a TTY in this environment",
                     "operation_executed": None, "status": "NOT_RUN", "evidence_level": "NOT_RUN",
                     "manual_procedure": "LIVE_HOST_PILOT_REPORT.md section 7", "evidence_paths": []})
    for c, what in (("M1", "PreToolUse hook without a timeout under a hung script"), ("L1", "15 s PreToolUse/Stop budget exceeded")):
        rows.append({"row_id": f"{c}-D3", "candidate": c, "class": "D", "row": "D3", "host": HOST, "session_mode": "n/a",
                     "hook_event": "PreToolUse", "triggering_action": what, "expected": "host-defined timeout handling",
                     "actual": "not executed on the candidate (would need a modified hook script); the host's timeout handling was characterized on a synthetic hook (SYN-DX5: hook cancelled at its timeout, command executed)", "operation_executed": None,
                     "status": "NOT_RUN", "evidence_level": "NOT_RUN", "evidence_paths": []})
    return rows


DX_EXPECT = {  # declared semantics: onFailure "block" must refuse; without it a non-2 exit is a non-blocking error
    "DX1": (False, "script exit 1 with onFailure: block"), "DX2": (True, "script exit 1 without onFailure (baseline)"),
    "DX3": (False, "executable not on PATH with onFailure: block"), "DX4": (False, "script exit 2 without onFailure (control)"),
    "DX5": (False, "script exceeds 3 s timeout with onFailure: block"),
}


def diagnostic_rows():
    rows = []
    base = os.path.join(OUT, "live_host_pilot", "diagnostic")
    for dx, (exp, what) in DX_EXPECT.items():
        p = os.path.join(base, dx, "result.json")
        if not os.path.exists(p):
            continue
        r = json.load(open(p, encoding="utf-8"))
        ok = r["issued"] and r["executed"] == exp
        rows.append({"row_id": f"SYN-{dx}", "scope": "synthetic_host_diagnostic", "candidate": "SYNTHETIC (not a candidate)",
                     "class": "D", "row": dx, "host": HOST, "session_mode": "headless (claude -p, stream-json)",
                     "hook_event": "PreToolUse", "triggering_action": f"git status --short; hook: {what}",
                     "settings_hook": r["settings_hook"], "allow_rule_for_action": True,
                     "expected": "executes" if exp else "does not execute",
                     "actual": ("executed" if r["executed"] else "not executed") + f"; PreToolUse {r['pre_hook']}",
                     "operation_executed": r["executed"], "hook_exit_code": [h["exit_code"] for h in r["pre_hook"] or []],
                     "hook_outcome": [h["outcome"] for h in r["pre_hook"] or []],
                     "observable_host_response": r["tool_result_excerpt"],
                     "status": "PASS" if ok else ("NOT_RUN" if not r["issued"] else "FAIL"),
                     "evidence_level": "LIVE_HOST_VERIFIED" if r["issued"] else "NOT_RUN",
                     "transcript_excerpt": {"tool_use_line": r.get("tool_use_line"), "command": "git status --short"},
                     "evidence_paths": [f"live_host_pilot/diagnostic/{dx}/stdout.jsonl", f"live_host_pilot/diagnostic/{dx}/result.json",
                                        f"live_host_pilot/diagnostic/{dx}/work/.claude/settings.json"]})
    return rows


def main():
    sessions = {}
    for case in sorted(os.listdir(RUNS)):
        p = os.path.join(RUNS, case, "live", "stdout.jsonl")
        if os.path.exists(p):
            sessions[case] = parse_session(p)
            with open(os.path.join(RUNS, case, "parsed_session.json"), "w", encoding="utf-8", newline="\n") as f:
                json.dump(sessions[case], f, indent=1, ensure_ascii=False)
    rows = [build_row(c, r, sessions) for c in CANDS for r in ROWS] + not_run_rows()
    for r in rows:
        r.setdefault("scope", "candidate")
    rows += diagnostic_rows()
    with open(os.path.join(OUT, "LIVE_HOST_PILOT_MATRIX.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    cand_rows = [r for r in rows if r["scope"] == "candidate"]
    tot = collections.Counter(r["status"] for r in cand_rows)
    live = collections.Counter(r["status"] for r in cand_rows if r["evidence_level"] == "LIVE_HOST_VERIFIED")
    diag = collections.Counter(r["status"] for r in rows if r["scope"] != "candidate")
    by_cls = collections.defaultdict(collections.Counter)
    for r in cand_rows:
        by_cls[r["class"]][r["status"]] += 1
    cost = sum((s["result"] or {}).get("total_cost_usd") or 0 for s in sessions.values())
    totals = {"candidate_rows": len(cand_rows), "status": dict(tot), "live_rows_status": dict(live),
              "synthetic_diagnostic_rows": len(rows) - len(cand_rows), "synthetic_diagnostic_status": dict(diag),
              "by_class": {k: dict(v) for k, v in sorted(by_cls.items())}, "sessions": len(sessions),
              "sessions_cost_usd_reported": round(cost, 4)}
    with open(os.path.join(OUT, "live_host_pilot", "PILOT_TOTALS.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(totals, f, indent=1)
    print(json.dumps(totals, indent=1))
    for r in rows:
        if r["evidence_level"] == "LIVE_HOST_VERIFIED" or r["status"] != "NOT_RUN":
            print(r["row_id"], r["status"], "|", r.get("actual"))


if __name__ == "__main__":
    main()
