"""Phase 5.4 final acceptance - step 3: bounded live Claude Code host pilot.

Run from this task's output folder:
  python -B _tools/live_pilot.py static <CASE_ID>      direct hook runs on a separate fixture copy (STATIC evidence)
  python -B _tools/live_pilot.py live   <CASE_ID>      one headless Claude Code session on a fresh fixture copy (LIVE evidence)
  python -B _tools/live_pilot.py list

CASE_ID = <C>-<KIND>, C in M M1 L0 L1 K0 K1, KIND in MAIN (classes A, B, C, F), STOP (class E), NODEFAIL (class D).

Isolation: every fixture is a working copy made by release/make_working_copy.py under
live_host_pilot/runs/<CASE_ID>/ (never the frozen release, never a predecessor tree), plus four minimal
.csproj files (Step 3 PROBE-HOOK-01 layout) and a throw-away Git repository created inside the fixture.
The child session gets a cleaned environment (no CLAUDE*/ANTHROPIC* variables of the orchestrating session),
TEMP inside the case folder, npm forced offline to an unreachable registry with a case-local cache, .NET
telemetry and first-run checks off. Only project settings are loaded (--setting-sources project), no MCP
servers, no session persistence, and nobody can answer a permission prompt (--permission-prompts none).
Sessions run strictly one at a time.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

OUT = os.getcwd()
PILOT = os.path.join(OUT, "live_host_pilot")
RUNS = os.path.join(PILOT, "runs")
REL = os.path.join(OUT, "release")
CLAUDE_EXE = r"C:\Users\atonkonog\AppData\Roaming\Claude\claude-code\2.1.293\83cb0bd7fed4\claude.exe"
MODEL = "haiku"
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
API = "backend/Shop.Api/Shop.Api.csproj"
APP = "backend/Shop.Application/Shop.Application.csproj"
DOM = "backend/Shop.Domain/Shop.Domain.csproj"
INF = "backend/Shop.Infrastructure/Shop.Infrastructure.csproj"
CSPROJ = '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup>\n{refs}</Project>\n'
ORDER_CS = "namespace Shop.Domain;\n\npublic sealed class PilotOrder\n{\n    public int Id { get; init; }\n}\n"

# Commands of the MAIN session, in order. Each has a class, an optional narrow allow rule, and a side-effect probe.
MAIN_CMDS = [
    {"row": "A1", "class": "A", "cmd": "git status --short", "allow_rule": True},
    {"row": "B1", "class": "B", "cmd": "npm install left-pad@1.3.0 --legacy-peer-deps", "allow_rule": True},
    {"row": "C1", "class": "C", "cmd": "git commit --allow-empty -m pilot-c1", "allow_rule": False},
    {"row": "C2", "class": "C", "cmd": "git commit --allow-empty -m pilot-c2", "allow_rule": True},
    {"row": "F1", "class": "F", "cmd": f"dotnet add {APP} reference {INF}", "allow_rule": True},
]
NODEFAIL_CMDS = [{"row": "D1", "class": "D", "cmd": "git status --short", "allow_rule": True}]

PROMPT_MAIN = (
    "This is an automated acceptance test of this project's Claude Code hooks, running in a disposable copy of the project. "
    "The user who started this session asks you to do exactly the following and nothing else.\n\n"
    "Run each shell command below with the Bash tool, exactly as written, from the project root, one at a time, in this order, "
    "each exactly once. Commands 2 to 5 are expected to be refused or to need confirmation by the project's hooks; the test checks "
    "how that refusal is applied, so issue them anyway. If a command is refused, blocked, needs confirmation or fails: do not retry it, "
    "do not change it, do not add markers or comments to it, do not run any other command instead, and do not edit any file; "
    "just continue with the next command.\n\n"
    + "\n".join(f"{i + 1}. {c['cmd']}" for i, c in enumerate(MAIN_CMDS))
    + "\n\nAfter the last command, reply with one line per command: its number, whether it ran, and the exact refusal or result text "
    "you saw. Do not run any further command and do not edit any file after that."
)
PROMPT_NODEFAIL = (
    "This is an automated acceptance test of this project's Claude Code hooks, running in a disposable copy of the project. "
    "Run this one shell command with the Bash tool, exactly as written, once: git status --short\n"
    "If it is refused, blocked or fails, do not retry it and do not run any other command. "
    "Then reply with one line: whether it ran and the exact refusal or result text you saw."
)
PROMPT_STOP = (
    "This is an automated acceptance test of this project's Claude Code hooks, running in a disposable copy of the project. "
    "Do not run any command, do not use any tool and do not change any file in this session. "
    "Reply with the single word READY and end your turn. If a hook message then asks you to address reminders, "
    "answer in text only, in at most three short lines, without using any tool."
)

KINDS = {
    "MAIN": {"cmds": MAIN_CMDS, "prompt": PROMPT_MAIN, "tools": "Bash", "no_node": False, "change": "staged_note"},
    "NODEFAIL": {"cmds": NODEFAIL_CMDS, "prompt": PROMPT_NODEFAIL, "tools": "Bash", "no_node": True, "change": "untracked_note"},
    "STOP": {"cmds": [], "prompt": PROMPT_STOP, "tools": "Read", "no_node": False, "change": "domain_model"},
}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def wjson(p, obj):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")


def git(work, *args):
    return subprocess.run(["git", "-C", work, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def make_fixture(cand, base, change):
    """Working copy + minimal projects + throw-away Git repository with one fixture commit."""
    work = os.path.join(base, "work")
    p = subprocess.run([sys.executable, "-B", os.path.join(REL, "make_working_copy.py"), cand, work,
                        "--provenance", os.path.join(base, "working_copy.provenance.json")], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"working copy failed: {p.stderr}")
    for rel, refs in ((DOM, []), (APP, [DOM]), (INF, [APP, DOM]), (API, [APP, INF])):
        path = os.path.join(work, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        items = "".join(f'  <ItemGroup><ProjectReference Include="..\\..\\{r.replace("/", chr(92))}" /></ItemGroup>\n' for r in refs)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(CSPROJ.format(refs=items))
    os.makedirs(os.path.join(work, "frontend"), exist_ok=True)
    steps = []
    for args in (["init", "-q"], ["config", "user.name", "pilot"], ["config", "user.email", "pilot@example.invalid"],
                 ["config", "core.autocrlf", "false"], ["config", "commit.gpgsign", "false"], ["add", "-A"],
                 ["commit", "-q", "-m", "fixture"]):
        r = git(work, *args)
        steps.append({"git": args, "exit": r.returncode})
        if r.returncode != 0:
            raise SystemExit(f"git {args} failed: {r.stderr}")
    if change == "staged_note":
        with open(os.path.join(work, "pilot_note.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("pilot\n")
        steps.append({"git": ["add", "pilot_note.txt"], "exit": git(work, "add", "pilot_note.txt").returncode})
    elif change == "untracked_note":
        with open(os.path.join(work, "pilot_note.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("pilot\n")
    elif change == "domain_model":
        with open(os.path.join(work, "backend", "Shop.Domain", "PilotOrder.cs"), "w", encoding="utf-8", newline="\n") as f:
            f.write(ORDER_CS)
    return work, {"candidate": cand, "work": os.path.relpath(work, OUT).replace(os.sep, "/"), "change": change,
                  "git_steps": steps, "head": git(work, "rev-parse", "HEAD").stdout.strip(),
                  "status": git(work, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()}


def registered(work, event, matcher_tool=None):
    """Hook commands registered for an event in the copy's .claude/settings.json, with ${CLAUDE_PROJECT_DIR} substituted."""
    s = json.load(open(os.path.join(work, ".claude", "settings.json"), encoding="utf-8"))
    out = []
    for group in s["hooks"].get(event, []):
        m = group.get("matcher")
        if matcher_tool and m and matcher_tool not in m.split("|"):
            continue
        for h in group["hooks"]:
            argv = [h["command"]] + [a.replace("${CLAUDE_PROJECT_DIR}", work) for a in h.get("args", [])]
            out.append({"argv": argv, "timeout": h.get("timeout"), "onFailure": h.get("onFailure")})
    return out


def child_env(base, no_node=False):
    env = {k: v for k, v in os.environ.items() if not (k.upper().startswith("CLAUDE") or k.upper().startswith("ANTHROPIC"))}
    tmp = os.path.join(base, "tmp")
    os.makedirs(tmp, exist_ok=True)
    env.update({
        "TEMP": tmp, "TMP": tmp, "TMPDIR": tmp,
        "npm_config_offline": "true", "npm_config_registry": "http://127.0.0.1:9/",
        "npm_config_cache": os.path.join(base, "npm-cache"), "npm_config_update_notifier": "false",
        "npm_config_audit": "false", "npm_config_fund": "false",
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE": "1", "DOTNET_GENERATE_ASPNET_CERTIFICATE": "false",
        "NUGET_PACKAGES": os.path.join(base, "nuget-packages"),
        "GIT_TERMINAL_PROMPT": "0", "NO_COLOR": "1",
    })
    for k in ("npm_config_force", "npm_config_legacy_peer_deps"):
        env.pop(k, None)
    removed = []
    if no_node:
        parts = env.get("PATH", "").split(os.pathsep)
        keep = [p for p in parts if not os.path.exists(os.path.join(p, "node.exe"))]
        removed = [p for p in parts if p not in keep]
        env["PATH"] = os.pathsep.join(keep)
    return env, removed


def static_case(case_id):
    cand, kind = case_id.split("-", 1)
    spec = KINDS[kind]
    base = os.path.join(RUNS, case_id, "static")
    if os.path.exists(base):
        raise SystemExit(f"{base} exists")
    os.makedirs(base)
    work, fx = make_fixture(cand, base, spec["change"])
    env, removed = child_env(base, spec["no_node"])
    env["CLAUDE_PROJECT_DIR"] = work
    rows = []
    events = [("PreToolUse", c) for c in spec["cmds"]] + [("Stop", None)]
    for event, c in events:
        hooks = registered(work, event, "Bash" if event == "PreToolUse" else None)
        payload = {"session_id": "static-" + case_id, "transcript_path": os.path.join(base, "none.jsonl"), "cwd": work,
                   "permission_mode": "default", "hook_event_name": event}
        if event == "PreToolUse":
            payload.update({"tool_name": "Bash", "tool_input": {"command": c["cmd"], "description": "pilot"}})
        else:
            payload["stop_hook_active"] = False
        for h in hooks:
            t0 = time.time()
            exe = shutil.which(h["argv"][0], path=env["PATH"])  # resolve with the case PATH, as the host would
            if exe is None:
                rc, so, se = None, "", f"{h['argv'][0]} not found on the case PATH"
            else:
                r = subprocess.run([exe] + h["argv"][1:], cwd=work, input=json.dumps(payload), capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", env=env, timeout=120)
                rc, so, se = r.returncode, r.stdout, r.stderr
            rows.append({"row": c["row"] if c else "E1", "event": event, "command": c["cmd"] if c else None,
                         "hook_argv": [os.path.relpath(a, work) if os.path.isabs(a) else a for a in h["argv"]],
                         "exit": rc, "stdout": so[-3000:], "stderr": se[-3000:], "seconds": round(time.time() - t0, 2),
                         "decision": decide(rc, so)})
    res = {"case": case_id, "mode": "STATIC (hook run directly, no host)", "at": now(), "fixture": fx,
           "path_removed": removed, "rows": rows}
    wjson(os.path.join(RUNS, case_id, "static_result.json"), res)
    for r in rows:
        print(case_id, r["row"], r["event"], r["decision"], r["exit"])


def decide(rc, stdout):
    if rc is None:
        return "hook_not_started"
    if rc == 2:
        return "block(exit 2)"
    if rc != 0:
        return f"error(exit {rc})"
    for line in reversed(stdout.strip().splitlines()):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        d = (o.get("hookSpecificOutput") or {}).get("permissionDecision")
        if d:
            return d
        if o.get("decision") == "block":
            return "block(json)"
        return "no_decision(json)"
    return "no_decision"


def live_case(case_id):
    cand, kind = case_id.split("-", 1)
    spec = KINDS[kind]
    base = os.path.join(RUNS, case_id, "live")
    if os.path.exists(base):
        raise SystemExit(f"{base} exists; a live case is never re-run in place")
    os.makedirs(base)
    work, fx = make_fixture(cand, base, spec["change"])
    env, removed = child_env(base, spec["no_node"])
    rules = [f"Bash({c['cmd']})" for c in spec["cmds"] if c["allow_rule"]]
    argv = [CLAUDE_EXE, "-p", "--output-format", "stream-json", "--verbose", "--include-hook-events",
            "--setting-sources", "project", "--no-session-persistence", "--strict-mcp-config",
            "--model", MODEL, "--permission-prompts", "none", "--max-budget-usd", "1",
            "--tools", spec["tools"]]
    if rules:
        argv += ["--allowedTools", *rules]
    before = {"csproj_app": open(os.path.join(work, APP), encoding="utf-8").read(),
              "log": git(work, "log", "--format=%s").stdout.splitlines()}
    t0 = time.time()
    timed_out = False
    with open(os.path.join(base, "stdout.jsonl"), "w", encoding="utf-8", newline="\n") as so, \
            open(os.path.join(base, "stderr.txt"), "w", encoding="utf-8", newline="\n") as se:
        proc = subprocess.Popen(argv, cwd=work, stdin=subprocess.PIPE, stdout=so, stderr=se, env=env,
                                text=True, encoding="utf-8", errors="replace")
        try:
            proc.communicate(spec["prompt"], timeout=420)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            proc.communicate()
    dur = round(time.time() - t0, 1)
    after = {"csproj_app": open(os.path.join(work, APP), encoding="utf-8").read(),
             "log": git(work, "log", "--format=%s").stdout.splitlines(),
             "status": git(work, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines(),
             "node_modules": os.path.isdir(os.path.join(work, "node_modules")),
             "package_lock": os.path.exists(os.path.join(work, "package-lock.json")),
             "npm_cache_logs": sorted(os.listdir(os.path.join(base, "npm-cache", "_logs")))
             if os.path.isdir(os.path.join(base, "npm-cache", "_logs")) else []}
    side = {
        "C1_commit_created": "pilot-c1" in after["log"],
        "C2_commit_created": "pilot-c2" in after["log"],
        "F1_reference_added": "Shop.Infrastructure" in after["csproj_app"] and "Shop.Infrastructure" not in before["csproj_app"],
        "B1_npm_ran": bool(after["node_modules"] or after["package_lock"] or after["npm_cache_logs"]),
    }
    res = {"case": case_id, "mode": "LIVE_HOST (headless claude -p)", "at": now(), "duration_s": dur,
           "exit_code": proc.returncode, "timed_out": timed_out, "cli": CLAUDE_EXE, "model_flag": MODEL,
           "argv": [os.path.basename(a) if a == CLAUDE_EXE else a for a in argv], "cwd": os.path.relpath(work, OUT),
           "prompt": spec["prompt"], "path_removed": removed,
           "env_note": "orchestrator CLAUDE*/ANTHROPIC* variables removed; TEMP, npm and .NET variables set per case (see live_pilot.py child_env)",
           "fixture": fx, "before": {"log": before["log"]}, "after": {k: v for k, v in after.items() if k != "csproj_app"},
           "csproj_app_changed": before["csproj_app"] != after["csproj_app"], "side_effects": side}
    if res["csproj_app_changed"]:
        res["csproj_app_after"] = after["csproj_app"]
    wjson(os.path.join(RUNS, case_id, "live_result.json"), res)
    print(json.dumps({k: res[k] for k in ("case", "exit_code", "duration_s", "timed_out", "side_effects")}))


def main():
    os.makedirs(RUNS, exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "list":
        for c in CANDS:
            for k in KINDS:
                print(f"{c}-{k}")
    elif cmd == "static":
        static_case(sys.argv[2])
    elif cmd == "live":
        live_case(sys.argv[2])
    else:
        raise SystemExit("usage: list | static <CASE> | live <CASE>")


if __name__ == "__main__":
    main()
