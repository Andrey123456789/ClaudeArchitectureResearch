"""Phase 5.4 Desktop Auto hook smoke test - preparation only. Never starts a Claude session and never answers a permission request.

Usage (any working directory):  python -B setup_k0.py

Creates, with the frozen release tooling:
  work/                 disposable K0 working copy with an isolated local Git repository, a baseline commit and one staged probe file
  setup_verification/   a SEPARATE K0 copy on which the frozen hook script is run directly (so work/ stays untouched by any hook run)
  SETUP_MANIFEST.json   everything the later run needs to compare against

Direct hook runs are static configuration checks. They are not host sessions and do not count as interaction of any kind.
"""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
WORK = os.path.join(OUT, "work")
VERIFY = os.path.join(OUT, "setup_verification")
REL = os.path.normpath(os.path.join(OUT, "..", "phase54_final_acceptance_v1", "release"))
CLI = r"C:\Users\atonkonog\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\claude-code\2.1.317\a33aa5518497\claude.exe"
CLI_SHA = "26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038"
PROBE = "desktop_auto_probe.txt"
PROBE_TEXT = "Disposable probe file for the Phase 5.4 Desktop Auto hook smoke test.\n"
GIT_NAME = "k0-desktop-smoke"
GIT_EMAIL = "k0-desktop-smoke@example.invalid"
BASELINE_MESSAGE = "baseline: frozen K0 working copy"
TEST_COMMIT = 'git commit -m "chore: add desktop auto probe"'
EXPECTED_PRE = {"type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "pre-tool-use"], "timeout": 30, "onFailure": "block"}
GITCONFIG = os.path.join(os.path.expanduser("~"), ".gitconfig")


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def wjson(p, obj):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")


def run(*a, **k):
    return subprocess.run(list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", **k)


def git(work, *a):
    r = run("git", "--no-optional-locks", "-C", work, *a)
    return r


def must(r, what):
    if r.returncode != 0:
        raise SystemExit(f"{what} failed: {r.stderr}")
    return r.stdout


def working_copy(dest, prov):
    must(run(sys.executable, "-B", os.path.join(REL, "make_working_copy.py"), "K0", dest, "--provenance", prov), "make_working_copy")


def init_repo(work):
    steps = []
    for args in (["init", "-q", "-b", "main"], ["config", "--local", "user.name", GIT_NAME], ["config", "--local", "user.email", GIT_EMAIL], ["config", "--local", "core.autocrlf", "false"],
                 ["config", "--local", "commit.gpgsign", "false"], ["add", "-A"], ["commit", "-q", "-m", BASELINE_MESSAGE]):
        must(git(work, *args), "git " + " ".join(args))
        steps.append(args)
    with open(os.path.join(work, PROBE), "w", encoding="utf-8", newline="\n") as f:
        f.write(PROBE_TEXT)
    must(git(work, "add", "--", PROBE), "git add probe")
    steps.append(["add", "--", PROBE])
    return steps


def direct(copy, event, payload_extra, label):
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = copy
    payload = {"session_id": "setup-direct-run", "transcript_path": os.path.join(VERIFY, "none.jsonl"), "cwd": copy, "permission_mode": "auto"}
    payload.update(payload_extra)
    r = run("node", os.path.join(copy, ".claude", "hooks", "hook.cjs"), event, input=json.dumps(payload), cwd=copy, env=env, timeout=120)
    decision = reason = None
    try:
        spec = json.loads(r.stdout).get("hookSpecificOutput") or {}
        decision, reason = spec.get("permissionDecision"), spec.get("permissionDecisionReason")
    except ValueError:
        pass
    return {"label": label, "event": event, "tool": payload_extra.get("tool_name"), "command": (payload_extra.get("tool_input") or {}).get("command"), "permission_mode_sent": "auto", "exit": r.returncode, "permissionDecision": decision, "permissionDecisionReason": reason, "stdout": r.stdout[-1200:], "stderr": r.stderr[-800:]}


def main():
    if os.path.exists(WORK):
        raise SystemExit("work/ already exists; a fixture is never rebuilt in place")
    global_before = sha(GITCONFIG) if os.path.exists(GITCONFIG) else None
    started = now()

    # 1. Disposable working copy, isolated repository, baseline commit, staged probe.
    prov = os.path.join(OUT, "work.provenance.json")
    working_copy(WORK, prov)
    git_steps = init_repo(WORK)

    # 2. Compare the copy with the frozen manifest and read the hook registration.
    man = json.load(open(os.path.join(REL, "CANDIDATE_FREEZE_MANIFEST.json"), encoding="utf-8"))["candidates"]["K0"]
    differing = sorted(rel for rel, row in man["files"].items() if sha(os.path.join(WORK, rel)) != row["sha256"])
    s = json.load(open(os.path.join(WORK, ".claude", "settings.json"), encoding="utf-8"))
    pre = s["hooks"]["PreToolUse"]
    registration_ok = len(pre) == 1 and pre[0]["matcher"] == "Bash|PowerShell" and pre[0]["hooks"] == [EXPECTED_PRE]

    # 3. Direct runs of the frozen hook on a SEPARATE copy, so hook state cannot appear in work/.
    copy = os.path.join(VERIFY, "k0_copy")
    working_copy(copy, os.path.join(VERIFY, "k0_copy.provenance.json"))
    init_repo(copy)
    cmd = lambda c, tool="Bash": {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"command": c, "description": "setup check"}}
    rows = [direct(copy, "pre-tool-use", cmd(TEST_COMMIT), "commit via Bash"),
            direct(copy, "pre-tool-use", cmd(TEST_COMMIT, "PowerShell"), "commit via PowerShell"),
            direct(copy, "pre-tool-use", cmd("git status --short"), "read-only status"),
            direct(copy, "pre-tool-use", cmd("git diff --cached"), "read-only staged diff")]
    state_dir = os.path.join(copy, ".claude", ".hook-state")
    state_before = os.path.isdir(state_dir)
    post = direct(copy, "post-tool-use", {"hook_event_name": "PostToolUse", "tool_name": "Bash", "tool_input": {"command": "git status --short", "description": "setup check"}, "tool_response": {"stdout": "A  " + PROBE + "\n", "stderr": "", "interrupted": False}}, "post hook after read-only status")
    state_after = os.path.isdir(state_dir)
    stop = direct(copy, "stop", {"hook_event_name": "Stop", "stop_hook_active": False}, "stop with staged probe only")
    rows += [post, stop]
    wjson(os.path.join(VERIFY, "HOOK_VERIFICATION.json"), {"mode": "STATIC_DIRECT_HOOK_RUN (no Claude host, no session, no interaction; a separate copy, not work/)", "at": now(), "rows": rows, "post_hook_creates_hook_state": {"before": state_before, "after": state_after}, "copy_is_not_the_test_fixture": True})
    ask_ok = rows[0]["permissionDecision"] == "ask" and rows[1]["permissionDecision"] == "ask" and "Repository-changing Git command (commit)" in (rows[0]["permissionDecisionReason"] or "")
    readonly_ok = all(r["exit"] == 0 and r["permissionDecision"] is None for r in rows[2:4])

    # 4. Record the final state of work/.
    head = git(WORK, "rev-parse", "HEAD").stdout.strip()
    state = {"head": head, "tree": git(WORK, "rev-parse", "HEAD^{tree}").stdout.strip(), "branch": git(WORK, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), "commit_count": int(git(WORK, "rev-list", "--count", "HEAD").stdout.strip()), "log": git(WORK, "log", "--format=%H %an <%ae> %s").stdout.splitlines(), "status": git(WORK, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines(), "staged": git(WORK, "diff", "--cached", "--name-status").stdout.splitlines(), "probe_blob": git(WORK, "rev-parse", ":" + PROBE).stdout.strip(), "remotes": git(WORK, "remote").stdout.split(), "local_config": git(WORK, "config", "--local", "--list").stdout.splitlines(), "active_git_hooks": sorted(x for x in os.listdir(os.path.join(WORK, ".git", "hooks")) if not x.endswith(".sample")) if os.path.isdir(os.path.join(WORK, ".git", "hooks")) else []}
    global_after = sha(GITCONFIG) if os.path.exists(GITCONFIG) else None
    cli = {"path": CLI, "exists": os.path.isfile(CLI), "sha256": sha(CLI) if os.path.isfile(CLI) else None, "expected_sha256": CLI_SHA, "version": run(CLI, "--version").stdout.strip() if os.path.isfile(CLI) else None, "note": "identity of the executable present at setup; the executable used by the later Desktop session is read from that session's transcript"}
    checks = {"work_matches_frozen_k0": not differing, "hook_registration_as_frozen": registration_ok, "hook_returns_ask_for_commit": ask_ok, "hook_passes_read_only_git": readonly_ok, "stop_hook_does_not_block_staged_probe": stop["exit"] == 0 and '"block"' not in stop["stdout"], "no_hook_state_in_work": not os.path.exists(os.path.join(WORK, ".claude", ".hook-state")), "no_local_settings_in_work": not os.path.exists(os.path.join(WORK, ".claude", "settings.local.json")), "baseline_single_commit": state["commit_count"] == 1, "probe_staged_only": state["status"] == ["A  " + PROBE] and state["staged"] == ["A\t" + PROBE], "no_remotes": state["remotes"] == [], "no_active_git_hooks": state["active_git_hooks"] == [], "global_git_config_unchanged": global_before == global_after, "cli_is_2_1_317": cli["sha256"] == CLI_SHA and (cli["version"] or "").split(" ")[0] == "2.1.317"}
    wjson(os.path.join(OUT, "SETUP_MANIFEST.json"), {"task": "Phase 5.4 Desktop Auto hook smoke test - preparation", "started": started, "finished": now(), "work_dir": WORK, "candidate": "K0", "frozen_tree_sha256": man.get("tree_sha256"), "frozen_files_compared": len(man["files"]), "files_differing_from_frozen": differing, "settings_sha256": sha(os.path.join(WORK, ".claude", "settings.json")), "hook_sha256": sha(os.path.join(WORK, ".claude", "hooks", "hook.cjs")), "pre_tool_use_registration": pre, "test_commit_command": TEST_COMMIT, "probe": {"file": PROBE, "text": PROBE_TEXT}, "git_setup_steps": git_steps, "state": state, "global_gitconfig_sha256": {"before": global_before, "after": global_after}, "tool_versions": {"git": run("git", "--version").stdout.strip(), "node": run("node", "--version").stdout.strip()}, "cli_at_setup": cli, "checks": checks, "interactive_tests_executed": False})
    print(json.dumps({"checks": checks, "head": head, "status": state["status"], "ask_reason": rows[0]["permissionDecisionReason"], "post_hook": {"exit": post["exit"], "state_before": state_before, "state_after": state_after}, "stop": {"exit": stop["exit"], "stdout": stop["stdout"][:200]}}, indent=1, ensure_ascii=False))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
