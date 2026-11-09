"""Host diagnostic for the D1 finding: does Claude Code 2.1.293 apply `onFailure: "block"` to a failing PreToolUse hook?

Run from this task's output folder:  python -B _tools/onfailure_diagnostic.py <DX_ID>
DX_ID in DX1..DX5. Uses SYNTHETIC projects (not candidates): a .claude/settings.json with one PreToolUse hook,
an untracked file, and a throw-away Git repository, under live_host_pilot/diagnostic/<DX_ID>/.
  DX1 node script exits 1,                 onFailure: block   (script failure)
  DX2 node script exits 1,                 no onFailure       (baseline)
  DX3 executable not on PATH,              onFailure: block   (same failure kind as D1)
  DX4 node script exits 2,                 no onFailure       (control: documented blocking exit code)
  DX5 node script sleeps 20 s, timeout 3,  onFailure: block   (timeout)
The session flags and environment are those of live_pilot.py (headless, project settings only, no prompts can be answered),
with the same narrow allow rule for the one command. One session per DX, strictly sequential.
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import live_pilot as lp  # noqa: E402

DIAG = os.path.join(lp.PILOT, "diagnostic")
SCRIPTS = {
    "exit1.js": "process.stderr.write('diagnostic hook failure (exit 1)\\n');\nprocess.exit(1);\n",
    "exit2.js": "process.stderr.write('diagnostic hook block (exit 2)\\n');\nprocess.exit(2);\n",
    "sleep20.js": "setTimeout(() => process.exit(0), 20000);\n",
}
CASES = {
    "DX1": {"command": "node", "script": "exit1.js", "onFailure": "block", "timeout": 30},
    "DX2": {"command": "node", "script": "exit1.js", "onFailure": None, "timeout": 30},
    "DX3": {"command": "node-missing-p54", "script": "exit1.js", "onFailure": "block", "timeout": 30},
    "DX4": {"command": "node", "script": "exit2.js", "onFailure": None, "timeout": 30},
    "DX5": {"command": "node", "script": "sleep20.js", "onFailure": "block", "timeout": 3},
}
CMD = "git status --short"
PROMPT = ("This is an automated acceptance test of Claude Code hooks in a disposable folder. "
          "Run this one shell command with the Bash tool, exactly as written, once: git status --short\n"
          "If it is refused, blocked or fails, do not retry it and do not run any other command. "
          "Then reply with one line: whether it ran and the exact refusal or result text you saw.")


def main():
    dx = sys.argv[1]
    spec = CASES[dx]
    base = os.path.join(DIAG, dx)
    if os.path.exists(base):
        raise SystemExit(f"{base} exists; never re-run in place")
    work = os.path.join(base, "work")
    os.makedirs(os.path.join(work, ".claude", "hooks"))
    with open(os.path.join(work, ".claude", "hooks", spec["script"]), "w", encoding="utf-8", newline="\n") as f:
        f.write(SCRIPTS[spec["script"]])
    hook = {"type": "command", "command": spec["command"], "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/" + spec["script"]],
            "timeout": spec["timeout"]}
    if spec["onFailure"]:
        hook["onFailure"] = spec["onFailure"]
    settings = {"hooks": {"PreToolUse": [{"matcher": "Bash|PowerShell", "hooks": [hook]}]}}
    with open(os.path.join(work, ".claude", "settings.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(settings, f, indent=2)
    for args in (["init", "-q"], ["config", "user.name", "pilot"], ["config", "user.email", "pilot@example.invalid"],
                 ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
        r = lp.git(work, *args)
        if r.returncode != 0:
            raise SystemExit(r.stderr)
    with open(os.path.join(work, "pilot_note.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("pilot\n")
    env, _ = lp.child_env(base, False)
    argv = [lp.CLAUDE_EXE, "-p", "--output-format", "stream-json", "--verbose", "--include-hook-events",
            "--setting-sources", "project", "--no-session-persistence", "--strict-mcp-config", "--model", lp.MODEL,
            "--permission-prompts", "none", "--max-budget-usd", "1", "--tools", "Bash", "--allowedTools", f"Bash({CMD})"]
    t0 = time.time()
    with open(os.path.join(base, "stdout.jsonl"), "w", encoding="utf-8", newline="\n") as so, \
            open(os.path.join(base, "stderr.txt"), "w", encoding="utf-8", newline="\n") as se:
        p = subprocess.Popen(argv, cwd=work, stdin=subprocess.PIPE, stdout=so, stderr=se, env=env, text=True,
                             encoding="utf-8", errors="replace")
        try:
            p.communicate(PROMPT, timeout=300)
            timed_out = False
        except subprocess.TimeoutExpired:
            p.kill()
            p.communicate()
            timed_out = True
    s = lp_parse(os.path.join(base, "stdout.jsonl"))
    res = {"dx": dx, "at": lp.now(), "settings_hook": hook, "command": CMD, "exit_code": p.returncode,
           "timed_out": timed_out, "duration_s": round(time.time() - t0, 1), **s}
    lp.wjson(os.path.join(base, "result.json"), res)
    print(json.dumps({k: res[k] for k in ("dx", "executed", "pre_hook", "tool_result_excerpt")}, ensure_ascii=False))


def lp_parse(path):
    import pilot_matrix as pm
    s = pm.parse_session(path)
    tus = [t for t in s["tool_uses"] if (t["input"].get("command") or "").strip() == CMD]
    if not tus:
        return {"executed": None, "pre_hook": None, "tool_result_excerpt": None, "issued": False}
    tu = tus[0]
    pre = [h for h in tu["hooks"] if h["event"] == "PreToolUse" and h["kind"] == "hook_response"]
    res = tu["result"] or {}
    executed = (not res.get("is_error", True)) and "pilot_note.txt" in res.get("content", "")
    return {"issued": True, "executed": executed,
            "pre_hook": [{"exit_code": h["exit_code"], "outcome": h["outcome"], "stderr": pm.cut(h["stderr"] or "", 300)} for h in pre],
            "tool_result_excerpt": pm.cut(res.get("content", ""), 400), "tool_result_is_error": res.get("is_error"),
            "tool_use_line": tu["line"]}


if __name__ == "__main__":
    main()
