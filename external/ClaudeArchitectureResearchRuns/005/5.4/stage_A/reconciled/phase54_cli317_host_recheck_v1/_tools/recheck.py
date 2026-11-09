"""Phase 5.4 - Claude Code 2.1.317 live hook compatibility recheck (genuine host sessions).

Usage (any working directory; always python -B):
  python -B recheck.py identity             write cli_identity/IDENTITY.json (fails if not exactly 2.1.317 with the pinned SHA-256)
  python -B recheck.py list                 list the case ids in execution order
  python -B recheck.py static <C>           direct hook runs on a separate copy (STATIC precheck only, never a live verdict)
  python -B recheck.py live <CASE>          one headless host session on a fresh fixture (refuses an existing case folder)
  python -B recheck.py all [CASE-PREFIX]    every case not yet recorded, strictly sequential, stops on an identity failure

Case families
  <C>-D1      exact reproduction of the 2.1.293 D1 failure: unmodified frozen settings, every PATH entry with node.exe removed
  <C>-D1X     the PreToolUse script of a disposable working copy replaced by one that exits 1 (settings untouched)
  L1-D3       the PreToolUse script of a disposable working copy sleeps past L1's declared 15 s timeout (settings untouched)
  SYN-DX1..5  the five 2.1.293 synthetic one-hook diagnostics, same hook definitions
  SYN-ASKNONE synthetic hook returning ask under --permission-prompts none
  <C>-SMOKE   allow, deny, ask (real approval surface, harness always answers deny) and Stop in one session

Identity: before and after every session the executable is re-hashed and asked for its version; a mismatch aborts.
There is no fallback path and no other version in this file. The version in each session's own init event is checked by build_matrix.py.
Isolation: child environment without CLAUDE*/ANTHROPIC* variables, TEMP inside the case folder, npm offline to an unreachable
registry, project settings only, no MCP servers, no session persistence.
Approval: the harness NEVER answers a permission request with allow; DENY_REPLY is the only response it can send.
"""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import state as st  # noqa: E402

OUT = os.path.dirname(HERE)
RUNS = os.path.join(OUT, "runs")
STATIC = os.path.join(OUT, "static_precheck")
REL = os.path.normpath(os.path.join(OUT, "..", "phase54_final_acceptance_v1", "release"))
CLAUDE_EXE = r"C:\Users\atonkonog\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\2.1.317\a33aa5518497\claude.exe"
EXPECT_VERSION = "2.1.317"
EXPECT_SHA = "26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038"
MODEL = "haiku"
CANDS = ["M", "M1", "L0", "L1", "K0", "K1"]
API = "backend/Shop.Api/Shop.Api.csproj"
APP = "backend/Shop.Application/Shop.Application.csproj"
DOM = "backend/Shop.Domain/Shop.Domain.csproj"
INF = "backend/Shop.Infrastructure/Shop.Infrastructure.csproj"
CSPROJ = '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup>\n{refs}</Project>\n'
ORDER_CS = "namespace Shop.Domain;\n\npublic sealed class PilotOrder\n{\n    public int Id { get; init; }\n}\n"

OP_STATUS = "git status --short"
MARKER = "recheck_marker.txt"
OP_MARKER = f"echo recheck-marker > {MARKER}"
NPM_MARKER = "npm_shim_marker.txt"
OP_MARKER_A2 = f"touch {MARKER}"
OP_NPM_VERSION = "npm --version"
OP_NPM = "npm install left-pad@1.3.0 --legacy-peer-deps"
OP_C1 = "git commit --allow-empty -m pilot-c1"
OP_C2 = "git commit --allow-empty -m pilot-c2"

def prompt_two(op_a, op_b): return (
    "This is an automated acceptance test of this project's Claude Code hooks, running in a disposable copy of the project. "
    "The user who started this session asks you to do exactly the following and nothing else.\n\n"
    "Run these two shell commands with the Bash tool, exactly as written, from the project root, one at a time, in this order, each exactly once. "
    "Attempt both commands even if the first one is refused. If a command is refused, blocked or fails: do not retry it, do not change it, "
    "do not run any other command instead, and do not edit any file; just continue with the next command.\n\n"
    f"1. {op_a}\n2. {op_b}\n\n"
    "After the second command, reply with one line per command: its number, whether it ran, and the exact refusal or result text you saw. "
    "Do not run any further command and do not edit any file after that."
)
def prompt_smoke(marker): return (
    "This is an automated acceptance test of this project's Claude Code hooks, running in a disposable copy of the project. "
    "The user who started this session asks you to do exactly the following and nothing else.\n\n"
    "Run each shell command below with the Bash tool, exactly as written, from the project root, one at a time, in this order, each exactly once. "
    "Commands 3 to 5 are expected to be refused or to need a permission decision; the test checks how that is applied, so issue them anyway. "
    "A permission decision, if one is requested, is answered by the test harness, not by you. "
    "If a command is refused, blocked, needs confirmation or fails: do not retry it, do not change it, do not add markers or comments to it, "
    "do not run any other command instead, and do not edit any file; just continue with the next command.\n\n"
    f"1. {OP_STATUS}\n2. {marker}\n3. {OP_NPM}\n4. {OP_C1}\n5. {OP_C2}\n\n"
    "After the last command, reply with one line per command: its number, whether it ran, and the exact refusal or result text you saw. "
    "Do not run any further command and do not edit any file after that. "
    "If a hook message then asks you to address reminders, answer in text only, in at most three short lines, without using any tool."
)

DENY_REPLY_MESSAGE = "Denied by the recheck harness: no person is available to approve this in the automated acceptance test."

SYN_SCRIPTS = {
    "exit1.js": "process.stderr.write('diagnostic hook failure (exit 1)\\n');\nprocess.exit(1);\n",
    "exit2.js": "process.stderr.write('diagnostic hook block (exit 2)\\n');\nprocess.exit(2);\n",
    "sleep20.js": "setTimeout(() => process.exit(0), 20000);\n",
    "noop.js": "process.exit(0);\n",
    "ask.js": "process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:'PreToolUse',permissionDecision:'ask',permissionDecisionReason:'recheck synthetic ask'}}));\nprocess.exit(0);\n",
}
SYN = {
    "DX1": {"command": "node", "script": "exit1.js", "onFailure": "block", "timeout": 30},
    "DX2": {"command": "node", "script": "exit1.js", "onFailure": None, "timeout": 30},
    "DX3": {"command": "node-missing-p54", "script": "exit1.js", "onFailure": "block", "timeout": 30},
    "DX4": {"command": "node", "script": "exit2.js", "onFailure": None, "timeout": 30},
    "DX5": {"command": "node", "script": "sleep20.js", "onFailure": "block", "timeout": 3},
    "ASKNONE": {"command": "node", "script": "ask.js", "onFailure": None, "timeout": 30},
    "ASKHOST": {"command": "node", "script": "ask.js", "onFailure": None, "timeout": 30},
    "SHIM": {"command": "node", "script": "noop.js", "onFailure": None, "timeout": 30},
}
FAULT_CRASH = "process.stderr.write('recheck injected crash (exit 1)\\n');\nprocess.exit(1);\n"
FAULT_SLOW = "setTimeout(() => process.exit(0), 40000);\n"


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="milliseconds")


def wjson(p, obj):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def base_env(tmp_base):
    env = {k: v for k, v in os.environ.items() if not (k.upper().startswith("CLAUDE") or k.upper().startswith("ANTHROPIC"))}
    tmp = os.path.join(tmp_base, "tmp")
    os.makedirs(tmp, exist_ok=True)
    env.update({
        "TEMP": tmp, "TMP": tmp, "TMPDIR": tmp, "DISABLE_AUTOUPDATER": "1",
        "npm_config_offline": "true", "npm_config_registry": "http://127.0.0.1:9/",
        "npm_config_cache": os.path.join(tmp_base, "npm-cache"), "npm_config_update_notifier": "false",
        "npm_config_audit": "false", "npm_config_fund": "false",
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE": "1", "DOTNET_GENERATE_ASPNET_CERTIFICATE": "false",
        "NUGET_PACKAGES": os.path.join(tmp_base, "nuget-packages"),
        "GIT_TERMINAL_PROMPT": "0", "NO_COLOR": "1",
    })
    for k in ("npm_config_force", "npm_config_legacy_peer_deps"):
        env.pop(k, None)
    return env


def identity(env=None):
    """Exact-version gate. Raises SystemExit on any mismatch; there is no fallback."""
    if not os.path.isfile(CLAUDE_EXE):
        raise SystemExit("BLOCKED: pinned executable not found: " + CLAUDE_EXE)
    h = sha(CLAUDE_EXE)
    t0 = time.time()
    r = subprocess.run([CLAUDE_EXE, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120)
    ver_out = (r.stdout or "").strip()
    ok = h == EXPECT_SHA and r.returncode == 0 and ver_out.split(" ")[0] == EXPECT_VERSION
    res = {"at": now(), "path": CLAUDE_EXE, "size": os.path.getsize(CLAUDE_EXE), "sha256": h, "version_stdout": ver_out, "version_exit": r.returncode,
           "version_stderr": (r.stderr or "").strip(), "version_seconds": round(time.time() - t0, 2), "gate": "PASS" if ok else "FAIL"}
    if not ok:
        raise SystemExit("BLOCKED: identity gate failed: " + json.dumps(res))
    return res


def git(work, *args):
    return subprocess.run(["git", "-C", work, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def hook_script(work):
    """Relative path of the PreToolUse script declared by the frozen settings (args[0])."""
    s = json.load(open(os.path.join(work, ".claude", "settings.json"), encoding="utf-8"))
    h = s["hooks"]["PreToolUse"][0]["hooks"][0]
    a0 = h["args"][0]
    if not a0.startswith("${CLAUDE_PROJECT_DIR}/"):
        raise SystemExit("unexpected PreToolUse arg: " + a0)
    return a0[len("${CLAUDE_PROJECT_DIR}/"):]


def make_candidate_fixture(cand, base, change, fault=None):
    work = os.path.join(base, "work")
    prov = os.path.join(base, "working_copy.provenance.json")
    p = subprocess.run([sys.executable, "-B", os.path.join(REL, "make_working_copy.py"), cand, work, "--provenance", prov], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("working copy failed: " + p.stderr)
    for rel, refs in ((DOM, []), (APP, [DOM]), (INF, [APP, DOM]), (API, [APP, INF])):
        path = os.path.join(work, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        items = "".join(f'  <ItemGroup><ProjectReference Include="..\\..\\{r.replace("/", chr(92))}" /></ItemGroup>\n' for r in refs)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(CSPROJ.format(refs=items))
    os.makedirs(os.path.join(work, "frontend"), exist_ok=True)
    injection = None
    if fault:
        rel = hook_script(work)
        target = os.path.join(work, rel)
        before = sha(target)
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(fault["content"])
        injection = {"file": rel, "kind": fault["kind"], "sha256_before": before, "sha256_after": sha(target), "scope": "disposable working copy only"}
    steps = []
    for args in (["init", "-q"], ["config", "user.name", "pilot"], ["config", "user.email", "pilot@example.invalid"],
                 ["config", "core.autocrlf", "false"], ["config", "commit.gpgsign", "false"], ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
        r = git(work, *args)
        steps.append({"git": args, "exit": r.returncode})
        if r.returncode != 0:
            raise SystemExit(f"git {args} failed: {r.stderr}")
    note = os.path.join(work, "pilot_note.txt")
    with open(note, "w", encoding="utf-8", newline="\n") as f:
        f.write("pilot\n")
    if change == "smoke":
        steps.append({"git": ["add", "pilot_note.txt"], "exit": git(work, "add", "pilot_note.txt").returncode})
        with open(os.path.join(work, "backend", "Shop.Domain", "PilotOrder.cs"), "w", encoding="utf-8", newline="\n") as f:
            f.write(ORDER_CS)
    return work, {"candidate": cand, "change": change, "fault_injection": injection, "git_steps": steps, "head": git(work, "rev-parse", "HEAD").stdout.strip(),
                  "status": git(work, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()}


def make_synthetic_fixture(dx, base):
    spec = SYN[dx]
    work = os.path.join(base, "work")
    os.makedirs(os.path.join(work, ".claude", "hooks"))
    with open(os.path.join(work, ".claude", "hooks", spec["script"]), "w", encoding="utf-8", newline="\n") as f:
        f.write(SYN_SCRIPTS[spec["script"]])
    hook = {"type": "command", "command": spec["command"], "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/" + spec["script"]], "timeout": spec["timeout"]}
    if spec["onFailure"]:
        hook["onFailure"] = spec["onFailure"]
    settings = {"hooks": {"PreToolUse": [{"matcher": "Bash|PowerShell", "hooks": [hook]}]}}
    with open(os.path.join(work, ".claude", "settings.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(settings, f, indent=2)
    for args in (["init", "-q"], ["config", "user.name", "pilot"], ["config", "user.email", "pilot@example.invalid"], ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
        r = git(work, *args)
        if r.returncode != 0:
            raise SystemExit(r.stderr)
    with open(os.path.join(work, "pilot_note.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("pilot\n")
    return work, {"synthetic": dx, "settings_hook": hook, "change": "untracked_note", "head": git(work, "rev-parse", "HEAD").stdout.strip()}


def strip_node(env):
    parts = env.get("PATH", "").split(os.pathsep)
    keep = [p for p in parts if not os.path.exists(os.path.join(p, "node.exe"))]
    removed = [p for p in parts if p not in keep]
    env["PATH"] = os.pathsep.join(keep)
    return removed


def add_npm_shim(env, base):
    """A shim named npm placed first on PATH: if the deny case ever reached the shell, it writes a marker and installs nothing."""
    d = os.path.join(base, "shim")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "npm"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f'#!/bin/sh\necho "npm shim invoked: $*" >> {NPM_MARKER}\nexit 0\n')
    env["PATH"] = d + os.pathsep + env.get("PATH", "")
    return d


def plan():
    out = [f"{c}-D1" for c in CANDS] + [f"{c}-D1X" for c in CANDS] + ["L1-D3"]
    out += [f"SYN-DX{i}" for i in range(1, 6)] + ["SYN-ASKNONE", "SYN-ASKHOST"]
    out += [f"{c}-SMOKE" for c in CANDS]
    return out


def plan_a2():
    out = ["SYN-SHIM"] + [f"{c}-D1" for c in CANDS] + [f"{c}-D1X" for c in CANDS] + ["L1-D3"]
    out += [f"SYN-DX{i}" for i in range(1, 6)] + [f"{c}-SMOKE" for c in CANDS]
    return out


def spec_for(case):
    fam, kind = case.split("-", 1)
    if fam == "SYN":
        return {"kind": "SYN", "dx": kind}
    if kind == "D1":
        return {"kind": "NODEFAIL", "cand": fam}
    if kind == "D1X":
        return {"kind": "CRASH", "cand": fam}
    if kind == "D3":
        return {"kind": "SLOW", "cand": fam}
    if kind == "SMOKE":
        return {"kind": "SMOKE", "cand": fam}
    raise SystemExit("unknown case " + case)


def run_session(base, work, env, argv, prompt, stream):
    """Runs the host and records raw stdout, per-line receive timestamps, stderr and any permission requests."""
    t_start = now()
    t0 = time.time()
    so_path = os.path.join(base, "stdout.jsonl")
    ts_path = os.path.join(base, "events_timestamped.jsonl")
    pr_path = os.path.join(base, "permission_requests.jsonl")
    perm_requests = []
    other_control = []
    state = {"timed_out": False}
    with open(os.path.join(base, "stderr.txt"), "w", encoding="utf-8", newline="\n") as se:
        proc = subprocess.Popen(argv, cwd=work, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=se, env=env, text=True, encoding="utf-8", errors="replace", bufsize=1)

        def expire():
            state["timed_out"] = True
            proc.kill()

        timer = threading.Timer(420, expire)
        timer.start()
        if stream:
            proc.stdin.write(json.dumps({"type": "user", "message": {"role": "user", "content": prompt}, "parent_tool_use_id": None, "session_id": ""}) + "\n")
            proc.stdin.flush()
        else:
            proc.stdin.write(prompt)
            proc.stdin.close()
        with open(so_path, "w", encoding="utf-8", newline="\n") as so, open(ts_path, "w", encoding="utf-8", newline="\n") as ts, open(pr_path, "w", encoding="utf-8", newline="\n") as pr:
            n = 0
            for line in proc.stdout:
                n += 1
                so.write(line)
                so.flush()
                try:
                    o = json.loads(line)
                except ValueError:
                    o = {"type": "unparsable"}
                ts.write(json.dumps({"line": n, "t": now(), "type": o.get("type"), "subtype": o.get("subtype")}) + "\n")
                ts.flush()
                if not stream:
                    continue
                if o.get("type") == "control_request":
                    req = o.get("request") or {}
                    if req.get("subtype") == "can_use_tool":
                        reply = {"type": "control_response", "response": {"subtype": "success", "request_id": o.get("request_id"),
                                                                           "response": {"behavior": "deny", "message": DENY_REPLY_MESSAGE, "interrupt": False}}}
                        rec = {"received_at": now(), "stream_line": n, "request_id": o.get("request_id"), "request": req, "harness_reply": "deny"}
                        perm_requests.append(rec)
                        pr.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        pr.flush()
                        proc.stdin.write(json.dumps(reply) + "\n")
                        proc.stdin.flush()
                    else:
                        other_control.append({"stream_line": n, "request": req})
                        reply = {"type": "control_response", "response": {"subtype": "error", "request_id": o.get("request_id"), "error": "not supported by recheck harness"}}
                        proc.stdin.write(json.dumps(reply) + "\n")
                        proc.stdin.flush()
                elif o.get("type") == "result":
                    try:
                        proc.stdin.close()
                    except OSError:
                        pass
        proc.wait()
        timer.cancel()
    return {"started_at": t_start, "finished_at": now(), "duration_s": round(time.time() - t0, 1), "exit_code": proc.returncode, "timed_out": state["timed_out"],
            "permission_requests": perm_requests, "other_control_requests": other_control}


def frozen_diff(cand, work):
    man = json.load(open(os.path.join(REL, "CANDIDATE_FREEZE_MANIFEST.json"), encoding="utf-8"))
    files = man["candidates"][cand]["files"]
    return sorted(rel for rel, row in files.items() if not os.path.exists(os.path.join(work, rel)) or sha(os.path.join(work, rel)) != row["sha256"]), len(files)


def live_case(case, attempt=1):
    spec = spec_for(case)
    folder = case if attempt == 1 else f"{case}__a{attempt}"
    base = os.path.join(RUNS, folder)
    if os.path.exists(base):
        raise SystemExit(f"{folder}: folder exists; a live case is never re-run in place")
    os.makedirs(base)
    env = base_env(base)
    removed, shim = [], None
    stream = False
    marker_op = OP_MARKER if attempt == 1 else OP_MARKER_A2
    op_first = OP_NPM_VERSION if spec.get("dx") == "SHIM" else OP_STATUS
    rules = [f"Bash({op_first})", f"Bash({marker_op})"]
    prompt = prompt_two(op_first, marker_op)
    if spec["kind"] == "SYN":
        work, fx = make_synthetic_fixture(spec["dx"], base)
        stream = spec["dx"] == "ASKHOST"
        if spec["dx"] == "SHIM":
            shim = add_npm_shim(env, base)
    elif spec["kind"] == "NODEFAIL":
        work, fx = make_candidate_fixture(spec["cand"], base, "untracked_note")
        removed = strip_node(env)
        if shutil.which("node", path=env["PATH"]):
            raise SystemExit("node is still resolvable after PATH removal")
    elif spec["kind"] == "CRASH":
        work, fx = make_candidate_fixture(spec["cand"], base, "untracked_note", {"kind": "exit_1", "content": FAULT_CRASH})
    elif spec["kind"] == "SLOW":
        work, fx = make_candidate_fixture(spec["cand"], base, "untracked_note", {"kind": "sleep_40s_exceeds_declared_timeout", "content": FAULT_SLOW})
    else:
        work, fx = make_candidate_fixture(spec["cand"], base, "smoke")
        stream = True
        prompt = prompt_smoke(marker_op)
        rules = [f"Bash({OP_STATUS})", f"Bash({marker_op})", f"Bash({OP_NPM})", f"Bash({OP_C2})"]
        shim = add_npm_shim(env, base)
    argv = [CLAUDE_EXE, "-p", "--output-format", "stream-json", "--verbose", "--include-hook-events", "--setting-sources", "project",
            "--no-session-persistence", "--strict-mcp-config", "--model", MODEL, "--max-budget-usd", "1", "--tools", "Bash", "--allowedTools", *rules]
    if stream:
        argv += ["--input-format", "stream-json", "--permission-prompts", "host", "--permission-prompt-tool", "stdio"]
    else:
        argv += ["--permission-prompts", "none"]
    id_before = identity(base_env(base))
    before_log = git(work, "log", "--format=%s").stdout.splitlines()
    s = run_session(base, work, env, argv, prompt, stream)
    id_after = identity(base_env(base))
    after = {"log": git(work, "log", "--format=%s").stdout.splitlines(),
             "status": git(work, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines(),
             "marker_present": os.path.exists(os.path.join(work, MARKER)),
             "npm_shim_marker_present": os.path.exists(os.path.join(work, NPM_MARKER)),
             "node_modules_present": os.path.isdir(os.path.join(work, "node_modules")),
             "package_lock_present": os.path.exists(os.path.join(work, "package-lock.json")),
             "npm_cache_logs": sorted(os.listdir(os.path.join(base, "npm-cache", "_logs"))) if os.path.isdir(os.path.join(base, "npm-cache", "_logs")) else []}
    if after["marker_present"]:
        with open(os.path.join(work, MARKER), encoding="utf-8", errors="replace") as f:
            after["marker_content"] = f.read()
    res = {"case": case, "attempt": attempt, "folder": folder, "marker_op": marker_op, "first_op": op_first, "kind": spec["kind"], "mode": "LIVE_HOST (claude -p, stream-json)", "stream_input": stream,
           "permission_surface": "SDK stdio (--permission-prompts host, can_use_tool, harness always denies)" if stream else "none (--permission-prompts none)",
           "identity_before": id_before, "identity_after": id_after, "cli": CLAUDE_EXE, "model_flag": MODEL,
           "argv": ["claude.exe" if a == CLAUDE_EXE else a for a in argv], "cwd": os.path.relpath(work, OUT).replace(os.sep, "/"), "prompt": prompt,
           "path_removed": removed, "npm_shim_dir": os.path.relpath(shim, OUT).replace(os.sep, "/") if shim else None,
           "env_note": "orchestrator CLAUDE*/ANTHROPIC* variables removed; TEMP, npm and .NET variables set per case; DISABLE_AUTOUPDATER=1 (see base_env)",
           "fixture": fx, "before": {"log": before_log}, "after": after, **s}
    if "cand" in spec:
        diffs, nfiles = frozen_diff(spec["cand"], work)
        res["frozen_files_compared"] = nfiles
        res["frozen_files_differing_after_session"] = diffs
    wjson(os.path.join(base, "result.json"), res)
    print(json.dumps({k: res[k] for k in ("case", "exit_code", "duration_s", "timed_out")} | {"marker": after["marker_present"], "log": after["log"], "permission_requests": len(s["permission_requests"]), "frozen_diff": res.get("frozen_files_differing_after_session")}, ensure_ascii=False))


def registered(work, event):
    s = json.load(open(os.path.join(work, ".claude", "settings.json"), encoding="utf-8"))
    out = []
    for group in s["hooks"].get(event, []):
        m = group.get("matcher")
        if m and "Bash" not in m.split("|"):
            continue
        for h in group["hooks"]:
            out.append([h["command"]] + [a.replace("${CLAUDE_PROJECT_DIR}", work) for a in h.get("args", [])])
    return out


def static_case(cand, attempt=1):
    """Direct hook runs on a separate copy; used only to write the predeclared expectations. Never a live verdict."""
    marker_op = OP_MARKER if attempt == 1 else OP_MARKER_A2
    base = os.path.join(STATIC, cand if attempt == 1 else f"{cand}__a{attempt}")
    if os.path.exists(base):
        raise SystemExit(f"{base} exists")
    os.makedirs(base)
    work, fx = make_candidate_fixture(cand, base, "smoke")
    env = base_env(base)
    env["CLAUDE_PROJECT_DIR"] = work
    rows = []
    for row, cmd, event in (("A1", OP_STATUS, "PreToolUse"), ("A2", marker_op, "PreToolUse"), ("B1", OP_NPM, "PreToolUse"), ("C1", OP_C1, "PreToolUse"), ("C2", OP_C2, "PreToolUse"), ("E1", None, "Stop")):
        payload = {"session_id": "static-" + cand, "transcript_path": os.path.join(base, "none.jsonl"), "cwd": work, "permission_mode": "default", "hook_event_name": event}
        if event == "PreToolUse":
            payload.update({"tool_name": "Bash", "tool_input": {"command": cmd, "description": "precheck"}})
        else:
            payload["stop_hook_active"] = False
        for h in registered(work, event):
            r = subprocess.run([shutil.which(h[0], path=env["PATH"])] + h[1:], cwd=work, input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120)
            rows.append({"row": row, "command": cmd, "event": event, "exit": r.returncode, "stdout": r.stdout[-1500:], "stderr": r.stderr[-1500:]})
    wjson(os.path.join(base, "static_precheck.json"), {"mode": "STATIC_PRECHECK (hook run directly, no host; never a live verdict)", "candidate": cand, "at": now(), "fixture": fx, "rows": rows})
    for r in rows:
        d = "exit2" if r["exit"] == 2 else ("ask" if '"ask"' in r["stdout"] else ("deny" if '"deny"' in r["stdout"] else ("block" if '"block"' in r["stdout"] else "none")))
        print(cand, r["row"], r["event"], "exit", r["exit"], d)


def main():
    cmd = sys.argv[1]
    if cmd == "identity":
        res = identity()
        res["policy"] = "exact version and SHA-256 required; no fallback"
        os.makedirs(os.path.join(OUT, "cli_identity"), exist_ok=True)
        wjson(os.path.join(OUT, "cli_identity", "IDENTITY.json"), res)
        print(json.dumps(res, indent=1))
    elif cmd == "list":
        print("\n".join(plan()))
    elif cmd == "static":
        static_case(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif cmd == "live":
        live_case(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif cmd == "a2":
        for case in plan_a2():
            if os.path.exists(os.path.join(RUNS, f"{case}__a2", "result.json")):
                print(case, "attempt 2 already recorded")
                continue
            if os.path.exists(os.path.join(RUNS, f"{case}__a2")):
                print(case, "attempt-2 folder exists without result.json; left for manual review")
                continue
            print("==", now(), case, "attempt 2", flush=True)
            live_case(case, 2)
            st.note("S5_INVESTIGATION", f"{case} attempt 2 recorded")
    elif cmd == "all":
        prefix = sys.argv[2] if len(sys.argv) > 2 else ""
        for case in plan():
            if not case.startswith(prefix):
                continue
            if os.path.exists(os.path.join(RUNS, case, "result.json")):
                print(case, "already recorded")
                continue
            if os.path.exists(os.path.join(RUNS, case)):
                print(case, "folder exists without result.json; left for manual review")
                st.note("S3_LIVE_FAILURE_CASES", f"{case}: folder exists without result.json; not re-run")
                continue
            print("==", now(), case, flush=True)
            live_case(case)
            st.note("S3_LIVE_FAILURE_CASES" if not case.endswith("SMOKE") else "S4_LIVE_SMOKE", f"{case} session recorded")
    else:
        raise SystemExit("usage: identity | list | static <C> | live <CASE> | all [prefix]")


if __name__ == "__main__":
    main()
