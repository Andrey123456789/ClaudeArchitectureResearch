#!/usr/bin/env python3
"""E0 Claude Code mechanics-validation harness.

Usage (see research/e0/probes/README.md for the full procedure):

  python e0.py env                         record environment metadata (no model calls)
  python e0.py selftest                    materialize every run without launching Claude
  python e0.py run R1-pos [R2-read-match ...] | all
                                           fresh workspace -> fresh headless Claude Code
                                           process -> collect raw evidence -> evaluate
  python e0.py startup R1-pos ... | all    startup-only runs (fresh process, model endpoint pointed at an
                                           unroutable local port): loading/discovery evidence, no model call
  python e0.py preflight                   can a fresh headless process authenticate and answer?
  python e0.py t1-static --transcript P    structure-only telemetry inventory + cost-derivation evidence
  python e0.py prepare RUN                 only materialize a workspace (for a manual session)
  python e0.py collect RUN_DIR --session-id ID
                                           collect evidence for a manually started session
  python e0.py evaluate [RESULT_DIR ...]   re-run deterministic checks on stored raw evidence
  python e0.py summarize                   write results/<env-id>/summary.json

Raw evidence is never derived from Claude's own claims alone: every check names
the artifact (hook log, stream event, transcript entry, workspace file) it reads.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import glob
import hashlib
import json
import os
import platform
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HARNESS_VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
PROBES_DIR = HERE.parent
E0_DIR = PROBES_DIR.parent
FIXTURES = PROBES_DIR / "fixtures"
PROBES_JSON = PROBES_DIR / "probes.json"
RESULTS = E0_DIR / "results"
HOOK_LOGGER = HERE / "hook_logger.py"

RENAMES = {"dot-claude": ".claude", "CLAUDE.fixture.md": "CLAUDE.md"}

HOOK_EVENTS_WITH_MATCHER = ["PreToolUse", "PostToolUse", "PostToolUseFailure", "PermissionRequest", "PermissionDenied"]
HOOK_EVENTS_PLAIN = ["SessionStart", "InstructionsLoaded", "UserPromptSubmit", "SubagentStart", "SubagentStop", "Stop", "SessionEnd"]

# Variables injected by a parent Claude Code / desktop-app session. A fresh benchmark
# process must not inherit them (they identify the parent session or change host wiring).
PARENT_SESSION_ENV = re.compile(r"^(CLAUDECODE|CLAUDE_PID|CLAUDE_AGENT_SDK_.*|CLAUDE_PREVIEW_.*|MCP_CONNECTION_NONBLOCKING|MCP_SERVER_CONNECTION_BATCH_SIZE|CLAUDE_CODE_.*)$")
KEEP_ENV = {"CLAUDE_CODE_GIT_BASH_PATH", "CLAUDE_CODE_OAUTH_TOKEN", "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX"}

REDACTIONS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<redacted-email>"),
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}"), "<redacted-key>"),
    (re.compile(r'("(?:organizationUuid|accountUuid|organization_uuid|account_uuid|orgId|organizationId)"\s*:\s*")[0-9a-fA-F-]{36}(")'), r"\1<redacted-uuid>\2"),
]
TEXT_SUFFIXES = {".json", ".jsonl", ".txt", ".md", ".patch", ".cs", ".ts", ".log", ".qledger", ".pellucid", ""}

READ_LIKE_TOOLS = {"Read", "Glob", "Grep", "LS", "Bash", "PowerShell", "NotebookRead"}
AGENT_TOOLS = {"Agent", "Task"}


# --------------------------------------------------------------------------- utils

def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_probes() -> dict:
    return json.loads(PROBES_JSON.read_text(encoding="utf-8"))


def run_defs(probes: dict) -> dict:
    return {r["run"]: r for r in probes["runs"]}


def setting(rd: dict, probes: dict, key: str):
    return rd.get(key, probes["defaults"].get(key))


def norm(p: str) -> str:
    return str(p).replace("\\", "/").rstrip("/").lower()


def path_aliases(path: Path) -> list[str]:
    """Long and 8.3 short spellings of a Windows path (hooks may report either)."""
    out = {norm(str(path))}
    if os.name == "nt":
        import ctypes
        for fn in ("GetShortPathNameW", "GetLongPathNameW"):
            buf = ctypes.create_unicode_buffer(1024)
            if getattr(ctypes.windll.kernel32, fn)(str(path), buf, 1024):
                out.add(norm(buf.value))
    return sorted(out)


def rel_to_ws(p: str | None, aliases: list[str]) -> str | None:
    if not p:
        return None
    n = norm(p)
    for a in aliases:
        if n == a:
            return "."
        if n.startswith(a + "/"):
            return n[len(a) + 1:]
    return "OUTSIDE:" + n


def text_of(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                parts.append(c.get("text") or c.get("content") and text_of(c.get("content")) or "")
            else:
                parts.append(str(c))
        return "\n".join(p for p in parts if p)
    if isinstance(content, dict):
        return content.get("text") or json.dumps(content, ensure_ascii=False)
    return str(content)


def markers_in(text: str, markers) -> list[str]:
    return [m for m in markers if m and m in (text or "")]


# --------------------------------------------------------------------------- environment

def resolve_claude(explicit: str | None) -> Path:
    cand = explicit or os.environ.get("E0_CLAUDE") or shutil.which("claude")
    if cand:
        return Path(cand)
    appdata = os.environ.get("APPDATA")
    if appdata:
        found = sorted(glob.glob(os.path.join(appdata, "Claude", "claude-code", "*", "*", "claude.exe")), key=os.path.getmtime)
        if found:
            return Path(found[-1])
    sys.exit("Claude Code binary not found. Pass --claude PATH or set E0_CLAUDE.")


def clean_env(extra: dict | None = None) -> tuple[dict, list[str]]:
    env, stripped = {}, []
    for k, v in os.environ.items():
        if PARENT_SESSION_ENV.match(k) and k not in KEEP_ENV:
            stripped.append(k)
            continue
        env[k] = v
    env.update(extra or {})
    return env, sorted(stripped)


def claude_version(claude: Path) -> str:
    env, _ = clean_env()
    out = subprocess.run([str(claude), "--version"], capture_output=True, text=True, env=env, timeout=60)
    return out.stdout.strip()


def auth_status(claude: Path) -> dict:
    env, _ = clean_env()
    try:
        out = subprocess.run([str(claude), "auth", "status"], capture_output=True, text=True, env=env, timeout=60)
        data = json.loads(out.stdout)
    except Exception as exc:  # noqa: BLE001
        return {"error": repr(exc)}
    keep = ("loggedIn", "authMethod", "apiProvider", "subscriptionType", "analyticsDisabled")
    return {k: data[k] for k in keep if k in data}


def env_id(version: str, model: str) -> str:
    ver = (version.split() or ["unknown"])[0]
    return f"{sys.platform}-cc{ver}-{model}"


def config_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def user_level_config() -> dict:
    cd = config_dir()
    return {
        "config_dir": str(cd),
        "user_CLAUDE_md": (cd / "CLAUDE.md").exists(),
        "user_rules_dir": (cd / "rules").exists(),
        "user_skills_dir": (cd / "skills").exists(),
        "user_agents_dir": (cd / "agents").exists(),
        "user_settings_json": (cd / "settings.json").exists(),
        "user_plugins_dir": (cd / "plugins").exists(),
    }


def repo_state() -> dict:
    def git(*a):
        r = subprocess.run(["git", *a], cwd=E0_DIR, capture_output=True, text=True)
        return r.stdout.strip()
    return {"head": git("rev-parse", "HEAD"), "dirty_paths": git("status", "--porcelain").splitlines()}


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        h.update(p.relative_to(root).as_posix().encode())
        h.update(sha256_file(p).encode())
    return h.hexdigest()


def environment(claude: Path, probes: dict, workroot: Path) -> dict:
    version = claude_version(claude)
    d = probes["defaults"]
    return {
        "captured_at": utcnow(),
        "env_id": env_id(version, d["model"]),
        "os": {"platform": platform.platform(), "system": platform.system(), "release": platform.release(), "version": platform.version()},
        "shell": {"COMSPEC": os.environ.get("COMSPEC"), "SHELL": os.environ.get("SHELL")},
        "python": sys.version.split()[0],
        "claude_binary": str(claude),
        "claude_code_version": version,
        "auth": auth_status(claude),
        "desktop_app_version": os.environ.get("CLAUDE_CODE_DESKTOP_APP_VERSION"),
        "launched_from_parent_claude_session": bool(os.environ.get("CLAUDECODE")),
        "defaults": d,
        "user_level_config": user_level_config(),
        "workroot": str(workroot),
        "harness": {
            "version": HARNESS_VERSION,
            "e0_py_sha256": sha256_file(Path(__file__)),
            "hook_logger_sha256": sha256_file(HOOK_LOGGER),
            "probes_json_sha256": sha256_file(PROBES_JSON),
            "fixtures_tree_sha256": tree_hash(FIXTURES),
        },
        "research_repo": repo_state(),
    }


# --------------------------------------------------------------------------- workspace

def rename_rel(rel: str) -> str:
    return "/".join(RENAMES.get(part, part) for part in Path(rel).parts)


def copy_tree_renamed(src: Path, dst: Path) -> None:
    for p in sorted(src.rglob("*")):
        if p.is_file():
            target = dst / rename_rel(p.relative_to(src).as_posix())
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)


def file_manifest(root: Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.relative_to(root).parts:
            out[p.relative_to(root).as_posix()] = sha256_file(p)
    return out


def ancestors_gate(ws: Path) -> dict:
    home = Path.home().resolve()
    findings = []
    for d in ws.resolve().parents:
        for name in ("CLAUDE.md", "CLAUDE.local.md", ".claude"):
            p = d / name
            if p.exists():
                if name == ".claude" and d == home:
                    continue  # user config dir, recorded separately
                findings.append(str(p))
    return {"checked_from": str(ws), "project_instruction_files_in_ancestors": findings, "passed": not findings}


def hook_settings(log_path: Path) -> dict:
    py = Path(sys.executable).as_posix()
    cmd = f'"{py}" "{HOOK_LOGGER.as_posix()}" "{log_path.as_posix()}"'
    entry = {"type": "command", "command": cmd, "timeout": 30}
    hooks = {ev: [{"matcher": "*", "hooks": [entry]}] for ev in HOOK_EVENTS_WITH_MATCHER}
    hooks.update({ev: [{"hooks": [entry]}] for ev in HOOK_EVENTS_PLAIN})
    return {"hooks": hooks}


def rmtree_force(path: Path) -> None:
    def onexc(func, p, _exc):  # git object files are read-only on Windows
        os.chmod(p, 0o700)
        func(p)
    shutil.rmtree(path, onexc=onexc)


def materialize(rd: dict, run_dir: Path) -> dict:
    if run_dir.exists():
        rmtree_force(run_dir)
    ws, live = run_dir / "ws", run_dir / "live"
    ws.mkdir(parents=True)
    live.mkdir()
    copy_tree_renamed(FIXTURES / rd["fixture"], ws)
    if rd.get("overlay"):
        copy_tree_renamed(FIXTURES / rd["overlay"], ws)
    for rel in rd.get("remove", []):
        target = ws / rename_rel(rel)
        if target.is_dir():
            rmtree_force(target)
        elif target.exists():
            target.unlink()
    fixture_manifest = file_manifest(ws)
    fixture_hash = sha256_bytes(json.dumps(fixture_manifest, sort_keys=True).encode())

    hooks_log = live / "hooks.jsonl"
    hooks_log.touch()
    settings = ws / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    write_json(settings, hook_settings(hooks_log))

    canaries = {}
    if rd.get("canaries"):
        parent = run_dir / "outside-parent-canary.txt"
        sibling = run_dir / "sibling" / "sibling-canary.txt"
        sibling.parent.mkdir()
        canaries = {
            "parent_path": str(parent), "parent_marker": f"E0W1-PARENT-{secrets.token_hex(3).upper()}",
            "sibling_path": str(sibling), "sibling_marker": f"E0W1-SIBLING-{secrets.token_hex(3).upper()}",
        }
        parent.write_text(canaries["parent_marker"] + "\n", encoding="utf-8")
        sibling.write_text(canaries["sibling_marker"] + "\n", encoding="utf-8")
        write_json(live / "canaries.json", canaries)

    # fresh local repository with no research history or remotes (isolation protocol)
    git = ["git", "-c", "user.name=e0-harness", "-c", "user.email=e0-harness@example.invalid", "-c", "core.autocrlf=false"]
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=ws, check=True)
    subprocess.run([*git, "add", "-A"], cwd=ws, check=True, capture_output=True)
    subprocess.run([*git, "commit", "-q", "-m", "e0 fixture"], cwd=ws, check=True, capture_output=True)

    gate = ancestors_gate(ws)
    write_json(live / "isolation-gate.json", gate)
    write_json(live / "fixture-manifest.json", {"fixture": rd["fixture"], "overlay": rd.get("overlay"), "remove": rd.get("remove", []), "sha256": fixture_hash, "files": fixture_manifest})
    return {"ws": ws, "live": live, "fixture_sha256": fixture_hash, "canaries": canaries, "gate": gate}


def render_prompt(rd: dict, canaries: dict) -> str:
    prompt = rd["prompt"]
    if canaries:
        prompt = (prompt.replace("{PARENT_CANARY_POSIX}", Path(canaries["parent_path"]).as_posix())
                        .replace("{PARENT_CANARY}", canaries["parent_path"])
                        .replace("{SIBLING_CANARY}", canaries["sibling_path"]))
    return prompt


# --------------------------------------------------------------------------- execution

def build_argv(claude: Path, rd: dict, probes: dict, session_id: str, debug_file: Path | None) -> list[str]:
    argv = [str(claude), "-p", "--output-format", "stream-json", "--verbose", "--include-hook-events",
            "--model", setting(rd, probes, "model"),
            "--effort", setting(rd, probes, "effort"),
            "--permission-mode", setting(rd, probes, "permission_mode"),
            "--permission-prompts", setting(rd, probes, "permission_prompts"),
            "--setting-sources", setting(rd, probes, "setting_sources"),
            "--max-budget-usd", str(setting(rd, probes, "max_budget_usd")),
            "--session-id", session_id]
    if debug_file:
        argv += ["--debug-file", str(debug_file)]
    return argv + list(rd.get("extra_args", []))


def preflight(claude: Path, probes: dict, workroot: Path) -> dict:
    ws = workroot / f"preflight-{stamp()}"
    ws.mkdir(parents=True)
    env, stripped = clean_env()
    argv = [str(claude), "-p", "--output-format", "json", "--model", probes["defaults"]["model"],
            "--permission-mode", "manual", "--permission-prompts", "none", "--tools", "", "--max-budget-usd", "0.5"]
    t0 = time.monotonic()
    proc = subprocess.run(argv, cwd=ws, input="Reply with exactly: E0-PREFLIGHT-OK".encode(), capture_output=True, env=env, timeout=300)
    try:
        res = json.loads(proc.stdout.decode("utf-8", errors="replace"))
    except ValueError:
        res = {"_raw_stdout": proc.stdout.decode("utf-8", errors="replace")[:2000]}
    ok = bool(res.get("result") and "E0-PREFLIGHT-OK" in res.get("result", "") and not res.get("is_error"))
    return {
        "checked_at": utcnow(), "claude_binary": str(claude), "claude_code_version": claude_version(claude),
        "auth_status": auth_status(claude), "argv": argv, "env_stripped_names": stripped, "cwd": str(ws),
        "exit_code": proc.returncode, "elapsed_s": round(time.monotonic() - t0, 2),
        "result": {k: res.get(k) for k in ("type", "subtype", "is_error", "result", "terminal_reason", "num_turns", "duration_ms", "total_cost_usd", "api_error_status", "session_id")},
        "stderr_tail": proc.stderr.decode("utf-8", errors="replace")[-1000:],
        "fresh_headless_session_usable": ok,
    }


def kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
    else:
        proc.kill()


def find_transcripts(session_id: str) -> tuple[Path | None, Path | None]:
    projects = config_dir() / "projects"
    main = next(iter(projects.glob(f"*/{session_id}.jsonl")), None)
    side = next((p for p in projects.glob(f"*/{session_id}") if p.is_dir()), None)
    return main, side


def snapshot_after(ws: Path, live: Path) -> None:
    before = read_json(live / "fixture-manifest.json")["files"]
    after = file_manifest(ws)
    after.pop(".claude/settings.json", None)
    changed = {p: ("added" if p not in before else "modified") for p, h in after.items() if before.get(p) != h}
    changed.update({p: "deleted" for p in before if p not in after})
    write_json(live / "post-manifest.json", {"files": after, "changes": changed})
    patch = []
    for rel, kind in sorted(changed.items()):
        new = (ws / rel).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True) if kind != "deleted" else []
        old = []
        if kind != "added":
            old = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ws, capture_output=True, text=True).stdout.splitlines(keepends=True)
        patch.extend(difflib.unified_diff(old, new, f"a/{rel}", f"b/{rel}"))
        if kind != "deleted":
            target = live / "changed-files" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ws / rel, target)
    (live / "workspace-diff.patch").write_text("".join(patch), encoding="utf-8")


def collect_transcripts(session_id: str, live: Path) -> dict:
    main, side = find_transcripts(session_id)
    tdir = live / "transcript"
    tdir.mkdir(exist_ok=True)
    info = {"main": None, "side_dir": None}
    if main:
        shutil.copy2(main, tdir / "main.jsonl")
        info["main"] = str(main)
    if side:
        shutil.copytree(side, tdir / "session-dir", dirs_exist_ok=True)
        info["side_dir"] = str(side)
    return info


def redact(text: str) -> tuple[str, int]:
    total = 0
    for rx, repl in REDACTIONS:
        text, n = rx.subn(repl, text)
        total += n
    return text, total


def export(live: Path, dest: Path) -> dict:
    report = {}
    for p in sorted(live.rglob("*")):
        if not p.is_file() or p.name == "debug.log":
            continue
        rel = p.relative_to(live).as_posix()
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = p.read_bytes()
        if p.suffix.lower() in TEXT_SUFFIXES:
            text, n = redact(raw.decode("utf-8", errors="replace"))
            target.write_text(text, encoding="utf-8", newline="")
            report[rel] = {"raw_sha256": sha256_bytes(raw), "redactions": n}
        else:
            shutil.copy2(p, target)
            report[rel] = {"raw_sha256": sha256_bytes(raw), "redactions": 0}
    return report


def run_one(name: str, rd: dict, probes: dict, claude: Path, workroot: Path, envid: str, debug: bool, startup: bool = False) -> Path:
    tag = stamp()
    run_dir = workroot / (f"startup-{name}-{tag}" if startup else f"{name}-{tag}")
    m = materialize(rd, run_dir)
    if not m["gate"]["passed"]:
        sys.exit(f"isolation gate failed for {name}: {m['gate']}")
    prompt = render_prompt(rd, m["canaries"])
    session_id = str(uuid.uuid4())
    debug_file = m["live"] / "debug.log" if debug else None
    argv = build_argv(claude, rd, probes, session_id, debug_file)
    env_over = dict(rd.get("env", {}))
    if startup:
        env_over.update(probes["startup_mode"]["env"])
    env, stripped = clean_env(env_over)
    (m["live"] / "prompt.txt").write_text(prompt, encoding="utf-8")

    print(f"[{name}] launching fresh Claude Code process ({'startup-only' if startup else 'full'}) in {m['ws']}", flush=True)
    started, t0 = utcnow(), time.monotonic()
    timed_out = False
    with open(m["live"] / "stream.jsonl", "wb") as out, open(m["live"] / "stderr.txt", "wb") as err:
        proc = subprocess.Popen(argv, cwd=m["ws"], stdin=subprocess.PIPE, stdout=out, stderr=err, env=env)
        try:
            proc.communicate(input=prompt.encode("utf-8"), timeout=setting(rd, probes, "timeout_s"))
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc)
            proc.wait()
    finished, elapsed = utcnow(), time.monotonic() - t0

    transcripts = collect_transcripts(session_id, m["live"])
    snapshot_after(m["ws"], m["live"])

    probe_dir = RESULTS / envid / rd["probe"].replace("E0-", "")
    dest = (probe_dir / "startup" / f"{name}-{tag}") if startup else (probe_dir / f"{name}-{tag}")
    meta = {
        "schema": "e0-run/1",
        "run": name, "probe": rd["probe"], "role": rd.get("role"),
        "mode": "startup-only" if startup else "headless-cli",
        "fixture": rd["fixture"], "overlay": rd.get("overlay"), "remove": rd.get("remove", []),
        "fixture_sha256": m["fixture_sha256"],
        "workspace": str(m["ws"]), "workspace_aliases": path_aliases(m["ws"]),
        "argv": argv,
        "prompt_via": "stdin",
        "env_overrides": env_over, "env_stripped_names": stripped,
        "session_id": session_id,
        "started_at": started, "finished_at": finished, "harness_elapsed_s": round(elapsed, 3),
        "exit_code": proc.returncode, "timed_out": timed_out,
        "transcripts_source": transcripts,
        "harness_version": HARNESS_VERSION,
        "env_id": envid,
    }
    write_json(m["live"] / "run.json", meta)
    exported = export(m["live"], dest)
    meta["exported_files"] = exported
    write_json(dest / "run.json", meta)
    evaluate_dir(dest, probes)
    print(f"[{name}] exit={proc.returncode} elapsed={elapsed:.1f}s evidence={dest}", flush=True)
    return dest


# --------------------------------------------------------------------------- parsing

def parse_stream(path: Path) -> dict:
    res = {"init": None, "result": None, "assistant_messages": [], "tool_uses": [], "tool_results": {},
           "hook_events": [], "non_json_lines": 0, "other_types": {}}
    if not path.exists():
        return res
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            res["non_json_lines"] += 1
            continue
        if not isinstance(ev, dict):
            continue
        t, st = ev.get("type"), ev.get("subtype")
        parent = ev.get("parent_tool_use_id")
        if t == "system" and st == "init":
            res["init"] = ev
        elif t == "system" and st and st.startswith("hook"):
            res["hook_events"].append(ev)
        elif t == "assistant":
            msg = ev.get("message") or {}
            res["assistant_messages"].append({"id": msg.get("id"), "model": msg.get("model"), "usage": msg.get("usage"), "parent": parent})
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    res["tool_uses"].append({"id": b.get("id"), "name": b.get("name"), "input": b.get("input") or {}, "parent": parent})
        elif t == "user":
            msg = ev.get("message") or {}
            content = msg.get("content")
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        res["tool_results"][b.get("tool_use_id")] = {"is_error": bool(b.get("is_error")), "text": text_of(b.get("content")), "parent": parent}
        elif t == "result":
            res["result"] = ev
        else:
            key = f"{t}/{st}" if st else str(t)
            res["other_types"][key] = res["other_types"].get(key, 0) + 1
    return res


def parse_hooks(path: Path, aliases: list[str]) -> list[dict]:
    out = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        p = rec.get("payload") or {}
        item = {"event": rec.get("event"), "logged_at": rec.get("logged_at")}
        if item["event"] == "InstructionsLoaded":
            item.update({
                "file": rel_to_ws(p.get("file_path"), aliases),
                "memory_type": p.get("memory_type"), "load_reason": p.get("load_reason"),
                "globs": p.get("globs"),
                "trigger": rel_to_ws(p.get("trigger_file_path"), aliases),
                "parent": rel_to_ws(p.get("parent_file_path"), aliases),
                "agent_id": p.get("agent_id"),
            })
        elif item["event"] in ("PreToolUse", "PostToolUse", "PostToolUseFailure", "PermissionRequest", "PermissionDenied"):
            ti = p.get("tool_input") or {}
            item.update({"tool_name": p.get("tool_name"), "tool_use_id": p.get("tool_use_id"),
                         "file": rel_to_ws(ti.get("file_path") or ti.get("path"), aliases),
                         "command": ti.get("command"), "agent_id": p.get("agent_id"),
                         "permission_mode": p.get("permission_mode")})
        elif item["event"] in ("SubagentStart", "SubagentStop"):
            item.update({"agent_id": p.get("agent_id"), "agent_type": p.get("agent_type")})
        elif item["event"] == "SessionStart":
            item.update({"source": p.get("source"), "model": p.get("model")})
        out.append(item)
    return out


def parse_transcripts(tdir: Path, markers: list[str]) -> dict:
    res = {"files": [], "entries": 0, "first_ts": None, "last_ts": None, "attachments": [], "marker_hits": [],
           "assistant_usage": {}, "tool_uses": [],
           # context records Claude Code assembled for the model (main transcript only)
           "instructions": [], "skill_listing": [], "agent_listing": [], "prompt_snapshot": [], "cost_state": []}
    if not tdir.exists():
        return res
    main = tdir / "main.jsonl"
    if main.exists():
        for line in main.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            att = e.get("attachment") if isinstance(e.get("attachment"), dict) else {}
            kind = att.get("type")
            if kind == "instructions":
                res["instructions"].append([{"path": x.get("path"), "type": x.get("type"), "content": x.get("content", "")} for x in att.get("files") or []])
            elif kind == "skill_listing":
                res["skill_listing"].append({"names": att.get("names"), "content": att.get("content", ""), "skillCount": att.get("skillCount")})
            elif kind == "agent_listing_delta":
                res["agent_listing"].append({"addedTypes": att.get("addedTypes"), "addedLines": att.get("addedLines")})
            elif kind == "prompt_snapshot":
                res["prompt_snapshot"].append(text_of(att.get("systemPrompt")))
            if e.get("type") == "cost-state":
                res["cost_state"].append({k: e.get(k) for k in ("totalCostUSD", "totalAPIDuration", "totalDuration", "modelUsage", "hasUnknownModelCost")})
    for f in sorted(tdir.rglob("*.jsonl")):
        rel = f.relative_to(tdir).as_posix()
        res["files"].append(rel)
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines()):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            res["entries"] += 1
            ts = e.get("timestamp")
            if ts:
                res["first_ts"] = min(res["first_ts"] or ts, ts)
                res["last_ts"] = max(res["last_ts"] or ts, ts)
            att = e.get("attachment")
            if isinstance(att, dict):
                res["attachments"].append({"file": rel, "line": i, "type": att.get("type"), "path": att.get("path")})
            msg = e.get("message") or {}
            if e.get("type") == "assistant" and isinstance(msg, dict):
                if msg.get("id") and msg.get("usage"):
                    res["assistant_usage"][f"{rel}:{msg['id']}"] = msg["usage"]
                for b in msg.get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        res["tool_uses"].append({"file": rel, "name": b.get("name"), "id": b.get("id")})
            for m in markers_in(line, markers):
                res["marker_hits"].append({"marker": m, "file": rel, "line": i, "type": e.get("type"),
                                           "attachment_type": att.get("type") if isinstance(att, dict) else None})
    return res


# --------------------------------------------------------------------------- facts + checks

def facts_for(rdir: Path, probes: dict) -> dict:
    run = read_json(rdir / "run.json", {})
    aliases = run.get("workspace_aliases") or [norm(run.get("workspace", ""))]
    canaries = read_json(rdir / "canaries.json", {}) or {}
    markers = list(probes["markers"].values()) + [v for k, v in canaries.items() if k.endswith("marker")]
    stream = parse_stream(rdir / "stream.jsonl")
    for tu in stream["tool_uses"]:
        inp = tu["input"]
        tu["file"] = rel_to_ws(inp.get("file_path") or inp.get("path") or inp.get("notebook_path"), aliases)
    result = stream["result"] or {}
    post = read_json(rdir / "post-manifest.json", {}) or {}
    changed_text = {}
    for rel in (post.get("changes") or {}):
        p = rdir / "changed-files" / rel
        if p.exists():
            changed_text[rel] = p.read_text(encoding="utf-8", errors="replace")
    return {
        "run": run, "aliases": aliases, "canaries": canaries,
        "stream": stream, "result": result, "final_text": result.get("result") or "",
        "hooks": parse_hooks(rdir / "hooks.jsonl", aliases),
        "transcript": parse_transcripts(rdir / "transcript", markers),
        "changes": post.get("changes") or {}, "changed_text": changed_text,
        "fixture_files": (read_json(rdir / "fixture-manifest.json", {}) or {}).get("files", {}),
    }


class Checks:
    def __init__(self):
        self.items, self.invalid, self.notes = [], [], []

    def add(self, cid, desc, expected, observed, ok, evidence):
        self.items.append({"id": cid, "description": desc, "expected": expected, "observed": observed, "pass": bool(ok), "evidence": evidence})
        return bool(ok)

    def ok(self, cid):
        return next((c["pass"] for c in self.items if c["id"] == cid), None)


def il(f, rel):
    return [h for h in f["hooks"] if h["event"] == "InstructionsLoaded" and h.get("file") == rel]


def il_any(f):
    return [h for h in f["hooks"] if h["event"] == "InstructionsLoaded"]


def main_tools(f):
    return [t for t in f["stream"]["tool_uses"] if not t["parent"]]


def nested_memory_paths(f):
    return [a for a in f["transcript"]["attachments"] if a["type"] == "nested_memory"]


def common_checks(c: Checks, f: dict) -> None:
    r = f["result"]
    if not r:
        c.invalid.append("no result event in stream.jsonl (process failed before completing)")
    elif r.get("is_error"):
        c.invalid.append(f"result is_error: {str(r.get('result'))[:200]}")
    if f["run"].get("timed_out"):
        c.invalid.append("timed out")
    if not f["hooks"]:
        c.notes.append("hook channel produced no events")


def eval_context_listing(c, f, expect_present, expect_absent, rule_files_loaded, rule_files_absent, label):
    tools = main_tools(f)
    if tools:
        c.invalid.append(f"tools were used although the prompt forbade it: {[t['name'] for t in tools]}")
    for rel in rule_files_loaded:
        ev = il(f, rel)
        c.add(f"loaded:{rel}", f"InstructionsLoaded hook fired for {rel}", "≥1 event", [{k: e.get(k) for k in ('load_reason', 'parent', 'memory_type')} for e in ev], ev, "hooks.jsonl")
    for rel in rule_files_absent:
        ev = il(f, rel)
        c.add(f"not-loaded:{rel}", f"no InstructionsLoaded event for {rel}", "0 events", len(ev), not ev, "hooks.jsonl")
    final = f["final_text"]
    for m in expect_present:
        c.add(f"final-has:{m}", f"{label}: final reply contains {m}", True, m in final, m in final, "stream.jsonl result.result")
    for m in expect_absent:
        c.add(f"final-lacks:{m}", f"{label}: final reply does not contain {m}", False, m in final, m not in final, "stream.jsonl result.result")


def eval_R1(c, f, rd, mk):
    if rd["run"] == "R1-pos":
        eval_context_listing(c, f, [mk["R1_FLAT"], mk["R1_NESTED"], mk["R1_DEEP"]], [mk["R1_DECOY"]],
                             [".claude/rules/r1-flat.md", ".claude/rules/e0-group/r1-nested.md", ".claude/rules/e0-group/deeper/r1-deep.md"],
                             [".claude/rule-decoy/r1-decoy.md"], "positive")
    else:
        eval_context_listing(c, f, [mk["R1_FLAT"]], [mk["R1_NESTED"], mk["R1_DEEP"], mk["R1_DECOY"]],
                             [".claude/rules/r1-flat.md"], [".claude/rules/e0-group/r1-nested.md", ".claude/rule-decoy/r1-decoy.md"], "negative")


R2_RULES = {"backend": ".claude/rules/r2-scope/backend-cs.md", "domain": ".claude/rules/r2-flat-domain.md", "frontend": ".claude/rules/r2-scope/frontend-ts.md"}


def r2_rule_events(f):
    return {k: [{x: e.get(x) for x in ("load_reason", "trigger", "globs", "logged_at")} for e in il(f, rel)] for k, rel in R2_RULES.items()}


def eval_R2(c, f, rd, mk):
    name = rd["run"]
    ev = r2_rule_events(f)
    tools = main_tools(f)
    final = f["final_text"]
    if name in ("R2-read-match", "R2-read-nonmatch"):
        target = "backend/orders.domain/order.cs" if name == "R2-read-match" else "notes/readme.txt"
        reads = [t for t in tools if t["name"] == "Read"]
        others = [t for t in tools if not (t["name"] == "Read" and t["file"] == target)]
        if not any(t["file"] == target for t in reads):
            c.invalid.append("target file was not read with the Read tool")
        if others:
            c.invalid.append(f"other tool calls were made: {[(t['name'], t['file']) for t in others]}")
        if name == "R2-read-match":
            c.add("backend-loaded-on-read", "backend rule (nested group) loaded by path_glob_match on Read", "≥1 path_glob_match with trigger Order.cs", ev["backend"],
                  any(e["load_reason"] == "path_glob_match" for e in ev["backend"]), "hooks.jsonl")
            c.add("domain-loaded-on-read", "domain rule (flat, layer glob backend/*.Domain/**) loaded on Read", "≥1 path_glob_match", ev["domain"],
                  any(e["load_reason"] == "path_glob_match" for e in ev["domain"]), "hooks.jsonl")
            c.add("frontend-not-loaded", "frontend rule not loaded for a backend read", "0 events", ev["frontend"], not ev["frontend"], "hooks.jsonl")
            for key in ("R2_BACKEND", "R2_DOMAIN"):
                c.add(f"final-has:{mk[key]}", "model reports the path-scoped marker after the read", True, mk[key] in final, mk[key] in final, "result.result")
            c.add(f"final-lacks:{mk['R2_FRONTEND']}", "model does not report the non-matching marker", False, mk["R2_FRONTEND"] in final, mk["R2_FRONTEND"] not in final, "result.result")
        else:
            c.add("no-r2-rule-loaded", "no path-scoped rule loaded for a non-matching read", "all empty", ev, not any(ev.values()), "hooks.jsonl")
            hits = markers_in(final, [mk["R2_BACKEND"], mk["R2_DOMAIN"], mk["R2_FRONTEND"]])
            c.add("final-no-markers", "model reports no path-scoped marker", [], hits, not hits, "result.result")
    elif name == "R2-edit-match":
        target = "backend/orders.domain/order.cs"
        edits = [t for t in tools if t["name"] in ("Edit", "MultiEdit", "Write") and t["file"] == target]
        if not edits:
            c.invalid.append("Order.cs was not edited")
        content = next((v for k, v in f["changed_text"].items() if k.lower() == target), "")
        c.add("backend-loaded", "backend rule loaded during the edit task", "≥1 event", ev["backend"], ev["backend"], "hooks.jsonl")
        c.add("domain-loaded", "domain rule loaded during the edit task", "≥1 event", ev["domain"], ev["domain"], "hooks.jsonl")
        first_line = content.splitlines()[0] if content else ""
        c.add("edited-file-backend-header", "edited Order.cs starts with the backend probe comment", f"// probe: {mk['R2_BACKEND']}", first_line, first_line.strip() == f"// probe: {mk['R2_BACKEND']}", "changed-files/backend/Orders.Domain/Order.cs")
        c.add("edited-file-domain-line", "edited Order.cs contains the domain probe comment", True, mk["R2_DOMAIN"] in content, mk["R2_DOMAIN"] in content, "changed-files/backend/Orders.Domain/Order.cs")
        c.add("frontend-not-loaded", "frontend rule not loaded", "0 events", ev["frontend"], not ev["frontend"], "hooks.jsonl")
    elif name == "R2-write-new-match":
        target = "backend/billing.domain/invoice.cs"
        writes = [i for i, t in enumerate(tools) if t["name"] in ("Write", "Edit", "MultiEdit") and t["file"] == target]
        if not writes:
            c.invalid.append("Invoice.cs was never written")
            return
        before = [t for t in tools[:writes[0]] if t["name"] in READ_LIKE_TOOLS]
        if before:
            c.invalid.append(f"read/search tools ran before the first write: {[(t['name'], t['file']) for t in before]}")
        first = tools[writes[0]]
        first_content = first["input"].get("content", "") or first["input"].get("new_string", "")
        final_content = next((v for k, v in f["changed_text"].items() if k.lower() == target), "")
        post_writes = [h for h in f["hooks"] if h["event"] == "PostToolUse" and h.get("file") == target]
        first_post = post_writes[0]["logged_at"] if post_writes else None
        load_after = [e for e in ev["backend"] if first_post and e["logged_at"] and e["logged_at"] >= first_post]
        load_before = [e for e in ev["backend"] if first_post and e["logged_at"] and e["logged_at"] < first_post]
        c.notes.append(f"tool sequence: {[(t['name'], t['file']) for t in tools]}")
        c.add("rule-loaded-at-all", "backend rule loaded at some point in the new-file task", "≥1 event", ev["backend"], ev["backend"], "hooks.jsonl")
        c.add("rule-loaded-before-first-write", "backend rule loaded before the first Write completed", "≥1 event", load_before, load_before, "hooks.jsonl vs PostToolUse logged_at")
        c.add("first-write-compliant", "content of the FIRST Write already carries the backend probe header", True, mk["R2_BACKEND"] in first_content, mk["R2_BACKEND"] in first_content, "stream.jsonl tool_use input")
        c.add("final-file-compliant", "final Invoice.cs carries the backend probe header", True, mk["R2_BACKEND"] in final_content, mk["R2_BACKEND"] in final_content, "changed-files/backend/Billing.Domain/Invoice.cs")
        c.add("final-file-domain-line", "final Invoice.cs carries the domain probe comment", True, mk["R2_DOMAIN"] in final_content, mk["R2_DOMAIN"] in final_content, "changed-files/backend/Billing.Domain/Invoice.cs")
        c.add("trigger-is-new-file", "load event triggered by the new file path", target, [e["trigger"] for e in ev["backend"]], any(e["trigger"] == target for e in ev["backend"]), "hooks.jsonl")
        c.add("writes-count", "number of write/edit calls on Invoice.cs (1 = no post-hoc correction)", 1, len(writes), True, "stream.jsonl")
        c.add("loaded-after-first-write", "backend rule loaded only after the first Write", "informational", load_after, True, "hooks.jsonl")
    elif name == "R2-write-nonmatch":
        target = "notes/todo.txt"
        if not any(t["name"] == "Write" and t["file"] == target for t in tools):
            c.invalid.append("notes/todo.txt was not written")
        c.add("no-r2-rule-loaded", "no path-scoped rule loaded for a non-matching new file", "all empty", ev, not any(ev.values()), "hooks.jsonl")
        content = next((v for k, v in f["changed_text"].items() if k.lower() == target), "")
        hits = markers_in(content + final, [mk["R2_BACKEND"], mk["R2_DOMAIN"], mk["R2_FRONTEND"]])
        c.add("no-markers", "neither the file nor the reply contains a path-scoped marker", [], hits, not hits, "changed-files + result.result")


def skill_calls(f, skill, parent=None):
    out = []
    for t in f["stream"]["tool_uses"]:
        if t["name"] != "Skill" or (parent is not None and t["parent"] != parent):
            continue
        vals = json.dumps(t["input"])
        if skill in vals:
            out.append(t)
    return out


def skill_discovered(f, skill):
    init = f["stream"]["init"] or {}
    fields = {k: (skill in json.dumps(init.get(k))) for k in ("skills", "slash_commands", "agents") if k in init}
    return fields


def eval_S1(c, f, rd, mk):
    if rd["role"] in ("collision", "config"):
        final = f["final_text"]
        for nm, body in (("verify", mk["S1C_VERIFYBODY"]), ("code-review", mk["S1C_REVIEWBODY"])):
            calls = [t for t in f["stream"]["tool_uses"] if t["name"] == "Skill" and nm in json.dumps(t["input"])]
            c.add(f"invoked:{nm}", f"Skill tool invoked for '{nm}'", "characterize", [t["input"] for t in calls], True, "stream.jsonl tool_use")
            c.add(f"project-body-used:{nm}", f"reply carries the PROJECT '{nm}' skill body marker (project skill won the name)", "characterize", body in final, True, "result.result")
        return
    skill = "e0-ledger-summary"
    calls = skill_calls(f, skill)
    direct_reads = [t for t in f["stream"]["tool_uses"] if t["name"] == "Read" and (t["file"] or "").endswith("skill.md")]
    final = f["final_text"]
    c.add("skill-in-init", "skill is listed in the session init event", "true in skills/slash_commands", skill_discovered(f, skill), any(skill_discovered(f, skill).values()), "stream.jsonl system/init")
    if rd["role"] == "positive":
        c.add("skill-tool-invoked", "Skill tool invoked for e0-ledger-summary without naming it in the prompt", "≥1 Skill call", [t["input"] for t in calls], calls, "stream.jsonl tool_use")
        c.add("final-has-skill-marker", "reply carries the marker that exists only in the skill body", True, mk["S1_SKILL"] in final, mk["S1_SKILL"] in final, "result.result")
        c.add("not-via-file-read", "SKILL.md was not read with the Read tool (mechanism = skill, not file access)", 0, len(direct_reads), not direct_reads, "stream.jsonl tool_use")
        c.add("arithmetic", "reply has the reconciled totals", "Debits 160.00 / Credits 160.00", ("160.00" in final), "160.00" in final, "result.result")
    else:
        c.add("skill-not-invoked", "no Skill call for an unrelated prompt", 0, len(calls), not calls, "stream.jsonl tool_use")
        c.add("final-lacks-skill-marker", "reply lacks the skill marker", False, mk["S1_SKILL"] in final, mk["S1_SKILL"] not in final, "result.result")


def eval_S2(c, f, rd, mk):
    skill, ref = "e0-freight-tariff", ".claude/skills/e0-freight-tariff/references/rates.md"
    calls = skill_calls(f, skill)
    ref_reads = [t for t in f["stream"]["tool_uses"] if t["file"] == ref]
    final = f["final_text"]
    name = rd["run"]
    if name == "S2-pos":
        c.add("skill-tool-invoked", "Skill tool invoked for e0-freight-tariff", "≥1", [t["input"] for t in calls], calls, "stream.jsonl tool_use")
        c.add("reference-read", "the private reference was read via a tool call", "≥1 Read of references/rates.md", [(t["name"], t["file"]) for t in ref_reads], ref_reads, "stream.jsonl tool_use")
        c.add("final-has-ref-marker", "reply has the verification code that exists only in the reference", True, mk["S2_REF"] in final, mk["S2_REF"] in final, "result.result")
        c.add("final-has-correct-tariff", "reply has 63.49 (needs the reference's rate table)", True, "63.49" in final, "63.49" in final, "result.result")
        c.add("final-has-skill-marker", "reply has the skill-body marker", True, mk["S2_SKILL"] in final, mk["S2_SKILL"] in final, "result.result")
        c.add("ref-not-instruction", "reference never reported by InstructionsLoaded (not a memory file)", 0, len(il(f, ref)), not il(f, ref), "hooks.jsonl")
    elif name == "S2-neg-context":
        tools = main_tools(f)
        if tools:
            c.invalid.append(f"tools were used although the prompt forbade it: {[t['name'] for t in tools]}")
        hits = markers_in(final, [mk["S2_REF"], mk["S2_SKILL"]])
        c.add("final-no-skill-or-ref-marker", "neither the skill body nor the reference is in session-start context", [], hits, not hits, "result.result")
        c.add("ref-not-instruction", "reference never reported by InstructionsLoaded", 0, len(il(f, ref)), not il(f, ref), "hooks.jsonl")
        c.add("skill-in-init", "skill (name/description only) is discoverable", True, skill_discovered(f, skill), any(skill_discovered(f, skill).values()), "stream.jsonl system/init")
    else:
        c.add("skill-not-invoked", "unrelated task does not invoke the owning skill", 0, len(calls), not calls, "stream.jsonl tool_use")
        c.add("reference-not-read", "unrelated task does not read the private reference", 0, len(ref_reads), not ref_reads, "stream.jsonl tool_use")
        hits = markers_in(final, [mk["S2_REF"], mk["S2_SKILL"]])
        c.add("final-no-markers", "reply carries no skill/reference marker", [], hits, not hits, "result.result")


def eval_A1(c, f, rd, mk):
    codes = ["PX-731", "PX-482", "PX-905"]
    agent_calls = [t for t in f["stream"]["tool_uses"] if t["name"] in AGENT_TOOLS and not t["parent"]]
    rev = [t for t in agent_calls if t["input"].get("subagent_type") == "e0-reviewer"]
    if not rev:
        c.invalid.append(f"main session did not delegate to e0-reviewer: {[t['input'].get('subagent_type') for t in agent_calls]}")
        return
    call = rev[0]
    out = f["stream"]["tool_results"].get(call["id"], {}).get("text", "")
    sub_tools = [t for t in f["stream"]["tool_uses"] if t["parent"] == call["id"]]
    leak_prompt = markers_in(json.dumps(call["input"]), [mk["A1_PROC"], *codes])
    main_skill = [t for t in main_tools(f) if t["name"] == "Skill"] + [t for t in main_tools(f) if (t["file"] or "").startswith(".claude/skills")]
    sub_skill_access = [t for t in sub_tools if t["name"] == "Skill" or (t["file"] or "").startswith(".claude/skills")]
    agent_def = ".claude/agents/e0-reviewer.md"
    c.add("delegated", "main session invoked the e0-reviewer subagent", "≥1 Agent call", len(rev), True, "stream.jsonl tool_use")
    c.add("prompt-carries-no-criteria", "the delegation prompt does not contain the procedure marker or finding codes", [], leak_prompt, not leak_prompt, "stream.jsonl Agent input")
    c.add("main-did-not-load-skill", "main session neither invoked nor read the review skill", [], [(t["name"], t["file"]) for t in main_skill], not main_skill, "stream.jsonl tool_use")
    c.add("subagent-did-not-fetch-skill", "subagent did not invoke/read the skill via tools", [], [(t["name"], t["file"]) for t in sub_tools if t in sub_skill_access], not sub_skill_access, "stream.jsonl tool_use (parent_tool_use_id)")
    subagent_marker_hits = [h for h in f["transcript"]["marker_hits"] if h["marker"] == mk["A1_PROC"] and "subagents" in h["file"]]
    if rd["role"] == "positive":
        c.add("output-has-proc-marker", "subagent output carries the marker that exists only in the skill body", True, mk["A1_PROC"] in out, mk["A1_PROC"] in out, "stream.jsonl Agent tool_result")
        found = [x for x in codes if x in out]
        c.add("output-has-all-findings", "subagent applied all three skill-only criteria", codes, found, found == codes, "stream.jsonl Agent tool_result")
        c.add("preload-visible-in-subagent-transcript", "skill body (marker) present in the subagent transcript", "≥1 hit", subagent_marker_hits[:3], subagent_marker_hits, "transcript/session-dir/subagents/*.jsonl")
    else:
        c.add("output-lacks-proc-marker", "without `skills:` the subagent output lacks the procedure marker", False, mk["A1_PROC"] in out, mk["A1_PROC"] not in out, "stream.jsonl Agent tool_result")
        found = [x for x in codes if x in out]
        c.add("output-lacks-findings", "without `skills:` the skill-only finding codes are absent", [], found, not found, "stream.jsonl Agent tool_result")
    c.notes.append(f"agent definition file present in fixture: {agent_def in f['fixture_files']}")
    c.notes.append(f"subagent output (first 400 chars): {out[:400]!r}")


def eval_I1(c, f, rd, mk):
    tools = main_tools(f)
    if tools:
        c.invalid.append(f"tools were used although the prompt forbade it: {[t['name'] for t in tools]}")
    final = f["final_text"]
    d = il(f, "docs/decisions.md")
    n = il(f, "docs/nested/details.md")
    c.add("direct-import-event", "docs/decisions.md loaded with load_reason=include from CLAUDE.md", "include / parent CLAUDE.md",
          [(e["load_reason"], e["parent"]) for e in d], any(e["load_reason"] == "include" and (e["parent"] or "").endswith("claude.md") for e in d), "hooks.jsonl")
    c.add("nested-import-event", "docs/nested/details.md loaded with load_reason=include from docs/decisions.md", "include / parent docs/decisions.md",
          [(e["load_reason"], e["parent"]) for e in n], any(e["load_reason"] == "include" and e["parent"] == "docs/decisions.md" for e in n), "hooks.jsonl")
    for key in ("I1_ROOT", "I1_DIRECT", "I1_NESTED"):
        c.add(f"final-has:{mk[key]}", f"reply contains {key}", True, mk[key] in final, mk[key] in final, "result.result")
    c.add("not-imported-absent", "plainly mentioned (non-@) file is not loaded", "0 events / marker absent",
          (len(il(f, "docs/background.md")), mk["I1_NOTIMPORTED"] in final), not il(f, "docs/background.md") and mk["I1_NOTIMPORTED"] not in final, "hooks.jsonl + result.result")
    ov = il(f, ".claude/rules/l0-arch/overview.md")
    al = il(f, ".claude/rules/l0-arch/always.md")
    c.add("l0-paths-rule-imported", "L0 shape: rule file WITH paths, imported from CLAUDE.md — loaded at session start?", "characterize",
          {"events": [(e["load_reason"], e["parent"]) for e in ov], "marker_in_reply": mk["I1_RULEIMPORT"] in final}, True, "hooks.jsonl + result.result")
    c.add("l0-always-rule-imported", "L0 shape: rule file WITHOUT paths, imported from CLAUDE.md — loaded once or twice?", "characterize",
          {"events": [(e["load_reason"], e["parent"]) for e in al], "marker_in_reply": mk["I1_RULEALWAYS"] in final}, True, "hooks.jsonl + result.result")


def eval_T1(c, f, rd, mk):
    r = f["result"]
    c.add("result-present", "result event present", True, bool(r), bool(r), "stream.jsonl")
    out = f["changed_text"].get("out/sum.txt", "")
    c.add("task-done", "out/sum.txt contains 100", "100", out.strip(), out.strip() == "100", "changed-files/out/sum.txt")
    c.add("ack-rule", "reply carries the rule ACK marker", True, mk["T1_ACK"] in f["final_text"], mk["T1_ACK"] in f["final_text"], "result.result")


def classify_w1_step(f, tool_filter, marker):
    denials = {d.get("tool_use_id") for d in (f["result"].get("permission_denials") or [])}
    tus = [t for t in main_tools(f) if tool_filter(t)]
    if not tus:
        return {"outcome": "NOT_ATTEMPTED"}
    outcomes = []
    for t in tus:
        res = f["stream"]["tool_results"].get(t["id"], {})
        txt = res.get("text", "")
        if marker in txt and not res.get("is_error"):
            o = "CONTENT"
        elif t["id"] in denials or re.search(r"permission|not allowed|denied|requires approval|was blocked by", txt, re.I):
            o = "PERMISSION_DENIED"
        elif res:
            o = "ERROR"
        else:
            o = "NO_RESULT"
        outcomes.append({"tool": t["name"], "tool_use_id": t["id"], "outcome": o, "result_excerpt": txt[:300]})
    order = ["CONTENT", "PERMISSION_DENIED", "ERROR", "NO_RESULT"]
    best = min(outcomes, key=lambda x: order.index(x["outcome"]))
    return {"outcome": best["outcome"], "attempts": outcomes}


def eval_W1(c, f, rd, mk):
    can = f["canaries"]
    if not can:
        c.invalid.append("canaries.json missing")
        return
    pname = Path(can["parent_path"]).name.lower()
    sname = Path(can["sibling_path"]).name.lower()
    step1 = classify_w1_step(f, lambda t: t["name"] == "Read" and pname in (t["file"] or ""), can["parent_marker"])
    step2 = classify_w1_step(f, lambda t: t["name"] == "Read" and sname in (t["file"] or ""), can["sibling_marker"])
    step3 = classify_w1_step(f, lambda t: t["name"] in ("Bash", "PowerShell") and pname in (t["input"].get("command") or "").lower(), can["parent_marker"])
    steps = {"read_parent": step1, "read_sibling": step2, "shell_parent": step3}
    outs = [s["outcome"] for s in steps.values()]
    if "CONTENT" in outs:
        cls = "REACHABLE"
    elif "PERMISSION_DENIED" in outs:
        cls = "PERMISSION_GATED"
    elif "ERROR" in outs:
        cls = "BLOCKED"
    else:
        cls = "INCONCLUSIVE"
    final = f["final_text"]
    c.add("classification", f"outside-root access under permission mode {rd.get('permission_mode')}", "characterize", cls, True, "stream.jsonl tool_use/tool_result + result.permission_denials")
    c.add("steps", "per-vector outcome", "characterize", {k: v["outcome"] for k, v in steps.items()}, True, "stream.jsonl")
    c.add("no-hallucinated-content", "canary markers appear in the reply only if a tool actually returned them", True,
          markers_in(final, [can["parent_marker"], can["sibling_marker"]]),
          all(m not in final or any(m in r["text"] for r in f["stream"]["tool_results"].values()) for m in (can["parent_marker"], can["sibling_marker"])), "stream.jsonl")
    c.notes.append(json.dumps(steps)[:3000])
    c.notes.append(f"permission_denials: {json.dumps(f['result'].get('permission_denials'))[:1000]}")
    c.w1_class = cls


# --------------------------------------------------------------------------- startup-only evaluators
# Startup-only runs exercise Claude Code up to the first model request. Evidence is what the
# harness itself assembled for the model: InstructionsLoaded hooks, system/init, and the
# transcript's context records. They never test model behavior (triggering, adherence, tools).

def startup_files(f) -> list[dict]:
    out = []
    for batch in f["transcript"]["instructions"]:
        for x in batch:
            out.append({"file": rel_to_ws(x["path"], f["aliases"]), "type": x["type"], "content": x["content"]})
    return out


def startup_text(f) -> str:
    t = f["transcript"]
    parts = [x["content"] for x in startup_files(f)]
    parts += [s["content"] for s in t["skill_listing"]]
    parts += ["\n".join(a.get("addedLines") or []) for a in t["agent_listing"]]
    parts += t["prompt_snapshot"]
    return "\n".join(parts)


def listing_entry(f, name: str) -> list[str]:
    lines = []
    for s in f["transcript"]["skill_listing"]:
        lines += [ln for ln in s["content"].splitlines() if ln.startswith(f"- {name}:")]
    return lines


def startup_common(c: Checks, f: dict) -> None:
    if not f["stream"]["init"]:
        c.invalid.append("no system/init event")
    if not f["transcript"]["files"]:
        c.invalid.append("no transcript captured")
    if not f["transcript"]["instructions"] and not f["transcript"]["skill_listing"]:
        c.notes.append("no instructions/skill_listing context records in transcript")
    r = f["result"] or {}
    if r and r.get("num_turns", 0) > 1:
        c.invalid.append("model request appears to have succeeded (startup-only mode must not reach the model)")
    c.notes.append(f"terminal result: {str(r.get('result'))[:160]!r}")
    sl = f["transcript"]["skill_listing"]
    c.notes.append(f"skill_listing: {sum(len(s['content']) for s in sl)} chars, {sum(len(s.get('names') or []) for s in sl)} skills; "
                   f"instructions: {sum(len(x['content']) for x in startup_files(f))} chars in {len(startup_files(f))} files; "
                   f"system prompt snapshot: {sum(len(s) for s in f['transcript']['prompt_snapshot'])} chars; "
                   f"auto-memory path announced: {bool(((f['stream']['init'] or {}).get('memory_paths') or {}).get('auto'))}")


def su_loaded(c, f, rel, marker, expect=True):
    files = [x for x in startup_files(f) if x["file"] == rel]
    ev = il(f, rel)
    has_marker = marker in startup_text(f) if marker else None
    if expect:
        c.add(f"startup-loaded:{rel}", f"{rel} is in the startup context record, has an InstructionsLoaded event and its marker is in the assembled context",
              "in instructions + hook + marker", {"in_instructions": len(files), "hook_events": [(e["load_reason"], e["parent"]) for e in ev], "marker": has_marker},
              files and ev and (has_marker is not False), "transcript/main.jsonl attachment.instructions + hooks.jsonl")
    else:
        c.add(f"startup-absent:{rel}", f"{rel} is NOT in the startup context and has no InstructionsLoaded event",
              "absent", {"in_instructions": len(files), "hook_events": len(ev), "marker": has_marker},
              not files and not ev and not has_marker, "transcript/main.jsonl attachment.instructions + hooks.jsonl")


def su_R1(c, f, rd, mk):
    if rd["run"] == "R1-pos":
        su_loaded(c, f, ".claude/rules/r1-flat.md", mk["R1_FLAT"])
        su_loaded(c, f, ".claude/rules/e0-group/r1-nested.md", mk["R1_NESTED"])
        su_loaded(c, f, ".claude/rules/e0-group/deeper/r1-deep.md", mk["R1_DEEP"])
        su_loaded(c, f, ".claude/rule-decoy/r1-decoy.md", mk["R1_DECOY"], expect=False)
    else:
        su_loaded(c, f, ".claude/rules/r1-flat.md", mk["R1_FLAT"])
        su_loaded(c, f, ".claude/rules/e0-group/r1-nested.md", mk["R1_NESTED"], expect=False)
        su_loaded(c, f, ".claude/rules/e0-group/deeper/r1-deep.md", mk["R1_DEEP"], expect=False)
        su_loaded(c, f, ".claude/rule-decoy/r1-decoy.md", mk["R1_DECOY"], expect=False)


def su_R2(c, f, rd, mk):
    for key, rel in R2_RULES.items():
        su_loaded(c, f, rel, mk[f"R2_{key.upper()}"], expect=False)


def su_skill_listed(c, f, skill):
    init_skills = (f["stream"]["init"] or {}).get("skills") or []
    entry = listing_entry(f, skill)
    c.add(f"listed:{skill}", f"'{skill}' discovered: in system/init skills and in the skill_listing sent to the model", "init + listing entry",
          {"init": skill in init_skills, "listing_entry": entry}, skill in init_skills and entry, "stream.jsonl system/init + transcript skill_listing")


def su_S1(c, f, rd, mk):
    if rd["role"] == "config":
        init = f["stream"]["init"] or {}
        names = sorted({n for s in f["transcript"]["skill_listing"] for n in (s.get("names") or [])})
        # characterization of benchmark-configuration levers, not a pass/fail condition of E0-S1
        c.add("bundled-skills-disabled", "with CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1: which skills are still listed to the model?", "characterize",
              {"listing_names": names, "init_skills": init.get("skills"), "only_project_skills_listed": names == ["code-review", "verify"]}, True, "transcript skill_listing + system/init")
        c.add("auto-memory-disabled", "with CLAUDE_CODE_DISABLE_AUTO_MEMORY=1: is an auto-memory path still announced?", "characterize",
              {"memory_paths": init.get("memory_paths"), "auto_memory_off": not (init.get("memory_paths") or {}).get("auto")}, True, "stream.jsonl system/init")
        return
    if rd["role"] == "collision":
        init_skills = (f["stream"]["init"] or {}).get("skills") or []
        for nm, desc_marker, body_marker in (("verify", mk["S1C_VERIFY"], mk["S1C_VERIFYBODY"]), ("code-review", mk["S1C_REVIEW"], mk["S1C_REVIEWBODY"])):
            entry = listing_entry(f, nm)
            project = any(desc_marker in e for e in entry)
            c.add(f"collision:{nm}", f"which '{nm}' skill is listed when a project skill reuses a bundled skill name", "characterize",
                  {"init_occurrences": init_skills.count(nm), "listing_entries": entry, "project_description_listed": project,
                   "bundled_description_listed": any(desc_marker not in e for e in entry)}, True, "stream.jsonl system/init + transcript skill_listing")
            c.add(f"body-not-preloaded:{nm}", "skill body is not in startup context", "absent", body_marker in startup_text(f), body_marker not in startup_text(f), "transcript context records")
        return
    su_skill_listed(c, f, "e0-ledger-summary")
    c.add("body-not-preloaded", "skill body marker is not in the startup context (only name + description are)", "absent",
          mk["S1_SKILL"] in startup_text(f), mk["S1_SKILL"] not in startup_text(f), "transcript context records")


def su_S2(c, f, rd, mk):
    su_skill_listed(c, f, "e0-freight-tariff")
    txt = startup_text(f)
    hits = markers_in(txt, [mk["S2_REF"], mk["S2_SKILL"]])
    c.add("reference-not-global", "neither the private reference nor the skill body is in the startup context", [], hits, not hits, "transcript context records")
    su_loaded(c, f, ".claude/skills/e0-freight-tariff/references/rates.md", mk["S2_REF"], expect=False)


def su_A1(c, f, rd, mk):
    added = [t for a in f["transcript"]["agent_listing"] for t in (a.get("addedTypes") or [])]
    init_agents = (f["stream"]["init"] or {}).get("agents") or []
    c.add("agent-listed", "e0-reviewer agent discovered (system/init agents + agent listing sent to the model)", "listed",
          {"init": "e0-reviewer" in init_agents, "listing": "e0-reviewer" in added}, "e0-reviewer" in init_agents and "e0-reviewer" in added, "stream.jsonl system/init + transcript agent_listing_delta")
    su_skill_listed(c, f, "e0-pellucid-review")
    c.add("procedure-not-in-main-context", "procedure body (marker) is not in the MAIN session's startup context", "absent",
          mk["A1_PROC"] in startup_text(f), mk["A1_PROC"] not in startup_text(f), "transcript context records")
    agent_lines = [ln for a in f["transcript"]["agent_listing"] for ln in (a.get("addedLines") or []) if ln.startswith("- e0-reviewer")]
    c.notes.append(f"agent listing line: {agent_lines}")


def su_I1(c, f, rd, mk):
    su_loaded(c, f, "claude.md", mk["I1_ROOT"])
    su_loaded(c, f, "docs/decisions.md", mk["I1_DIRECT"])
    su_loaded(c, f, "docs/nested/details.md", mk["I1_NESTED"])
    su_loaded(c, f, "docs/background.md", mk["I1_NOTIMPORTED"], expect=False)
    d, n = il(f, "docs/decisions.md"), il(f, "docs/nested/details.md")
    c.add("direct-import-reason", "docs/decisions.md: load_reason=include, parent=CLAUDE.md", "include/claude.md",
          [(e["load_reason"], e["parent"]) for e in d], any(e["load_reason"] == "include" and e["parent"] == "claude.md" for e in d), "hooks.jsonl")
    c.add("nested-import-reason", "docs/nested/details.md: load_reason=include, parent=docs/decisions.md", "include/docs/decisions.md",
          [(e["load_reason"], e["parent"]) for e in n], any(e["load_reason"] == "include" and e["parent"] == "docs/decisions.md" for e in n), "hooks.jsonl")
    files = startup_files(f)
    for rel, key in ((".claude/rules/l0-arch/overview.md", "I1_RULEIMPORT"), (".claude/rules/l0-arch/always.md", "I1_RULEALWAYS")):
        copies = [x for x in files if x["file"] == rel]
        c.add(f"l0-shape:{rel}", "L0 shape (rule-directory file imported from CLAUDE.md): copies in startup context, hook events, frontmatter retained?", "characterize",
              {"copies_in_instructions": len(copies), "hook_events": [(e["load_reason"], e["parent"]) for e in il(f, rel)],
               "marker_in_context": mk[key] in startup_text(f), "frontmatter_in_content": any("paths:" in x["content"] for x in copies),
               "marker_occurrences_in_context": startup_text(f).count(mk[key])}, True, "transcript instructions + hooks.jsonl")
    c.notes.append(f"startup instruction files in order: {[x['file'] for x in files]}")


def su_W1(c, f, rd, mk):
    # configuration preflight only: the boundary itself needs model-driven tool calls
    init = f["stream"]["init"] or {}
    want = rd.get("permission_mode")
    internal = {"manual": "default"}.get(want, want)  # the CLI choice 'manual' is reported as 'default' in system/init
    c.add("permission-mode-applied", f"CLI accepted and applied --permission-mode {want}", internal, init.get("permissionMode"), init.get("permissionMode") == internal, "stream.jsonl system/init")
    can = f["canaries"]
    c.add("canaries-outside-root", "canary files were generated outside the launch root", "OUTSIDE:...",
          [rel_to_ws(can.get("parent_path"), f["aliases"]), rel_to_ws(can.get("sibling_path"), f["aliases"])],
          all((rel_to_ws(can.get(k), f["aliases"]) or "").startswith("OUTSIDE:") for k in ("parent_path", "sibling_path")), "canaries.json")
    c.add("no-tool-calls", "no tool call happened in a startup-only run", 0, len(f["stream"]["tool_uses"]), not f["stream"]["tool_uses"], "stream.jsonl")


STARTUP_EVALUATORS = {"E0-W1": su_W1, "E0-R1": su_R1, "E0-R2": su_R2, "E0-S1": su_S1, "E0-S2": su_S2, "E0-A1": su_A1, "E0-I1": su_I1}

EVALUATORS = {"E0-R1": eval_R1, "E0-R2": eval_R2, "E0-S1": eval_S1, "E0-S2": eval_S2, "E0-A1": eval_A1, "E0-I1": eval_I1, "E0-T1": eval_T1, "E0-W1": eval_W1}


def evaluate_dir(rdir: Path, probes: dict) -> dict:
    run = read_json(rdir / "run.json", {})
    rd = run_defs(probes)[run["run"]]
    f = facts_for(rdir, probes)
    c = Checks()
    startup = run.get("mode") == "startup-only"
    try:
        if startup:
            startup_common(c, f)
            STARTUP_EVALUATORS[rd["probe"]](c, f, rd, probes["markers"])
        else:
            common_checks(c, f)
            EVALUATORS[rd["probe"]](c, f, rd, probes["markers"])
    except Exception as exc:  # noqa: BLE001 - record evaluator failures as evidence, never hide them
        c.invalid.append(f"evaluator error: {exc!r}")
    out = {
        "schema": "e0-checks/1", "run": run["run"], "probe": rd["probe"], "role": rd.get("role"),
        "mode": run.get("mode"),
        "evaluated_at": utcnow(), "harness_version": HARNESS_VERSION,
        "valid": not c.invalid, "invalid_reasons": c.invalid,
        "all_checks_pass": all(x["pass"] for x in c.items) if c.items else None,
        "checks": c.items, "notes": c.notes,
        "w1_classification": getattr(c, "w1_class", None),
        "observed": {
            "session_id": run.get("session_id"),
            "init_model": (f["stream"]["init"] or {}).get("model"),
            "init_permission_mode": (f["stream"]["init"] or {}).get("permissionMode"),
            "init_claude_code_version": (f["stream"]["init"] or {}).get("claude_code_version"),
            "tool_calls": [(t["name"], t["file"], bool(t["parent"])) for t in f["stream"]["tool_uses"]],
            "instructions_loaded": [{k: h.get(k) for k in ("file", "load_reason", "trigger", "parent", "memory_type")} for h in il_any(f)],
            "hook_event_counts": count_by(f["hooks"], "event"),
            "nested_memory_attachments": nested_memory_paths(f),
            "final_text": f["final_text"][:2000],
        },
    }
    write_json(rdir / "checks.json", out)
    return out


def count_by(items, key):
    out = {}
    for i in items:
        out[i.get(key)] = out.get(i.get(key), 0) + 1
    return out


# --------------------------------------------------------------------------- T1 telemetry inventory

T1_FIELDS = ["elapsed_timestamps", "input_tokens", "output_tokens", "cache_read_input_tokens",
             "cache_creation_input_tokens", "provider_reported_cost", "assistant_turns", "structured_tool_calls"]


def dedup_usage(usages: dict) -> dict:
    tot = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    for u in usages.values():
        for k in tot:
            tot[k] += int(u.get(k) or 0)
    return tot


def t1_run_crosscheck(rdir: Path, probes: dict) -> dict | None:
    f = facts_for(rdir, probes)
    r = f["result"]
    if not r or f["run"].get("mode") != "headless-cli":
        return None
    usage = r.get("usage") or {}
    main_usage = {k: v for k, v in f["transcript"]["assistant_usage"].items() if k.startswith("main.jsonl:")}
    side_usage = {k: v for k, v in f["transcript"]["assistant_usage"].items() if not k.startswith("main.jsonl:")}
    stream_usage = {m["id"]: m["usage"] for m in f["stream"]["assistant_messages"] if m["id"] and m["usage"]}
    model_usage = r.get("modelUsage") or {}
    mu = {k: sum(int(v.get(k2) or 0) for v in model_usage.values()) for k, k2 in
          (("input_tokens", "inputTokens"), ("output_tokens", "outputTokens"), ("cache_read_input_tokens", "cacheReadInputTokens"), ("cache_creation_input_tokens", "cacheCreationInputTokens"))}
    pre = [h for h in f["hooks"] if h["event"] == "PreToolUse"]
    post = [h for h in f["hooks"] if h["event"] in ("PostToolUse", "PostToolUseFailure")]
    otel_lines = 0
    raw = (rdir / "stream.jsonl").read_text(encoding="utf-8", errors="replace") if (rdir / "stream.jsonl").exists() else ""
    for line in raw.splitlines():
        if "claude_code." in line and not line.lstrip().startswith("{"):
            otel_lines += 1
    return {
        "run_dir": rdir.relative_to(E0_DIR).as_posix(),
        "harness_elapsed_s": f["run"].get("harness_elapsed_s"),
        "result_duration_ms": r.get("duration_ms"), "result_duration_api_ms": r.get("duration_api_ms"),
        "transcript_first_ts": f["transcript"]["first_ts"], "transcript_last_ts": f["transcript"]["last_ts"],
        "result_usage": {k: usage.get(k) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")},
        "result_usage_cache_creation_split": usage.get("cache_creation"),
        "modelUsage_sum": mu, "modelUsage_models": sorted(model_usage),
        "stream_main_dedup_sum": dedup_usage({k: v for k, v in stream_usage.items()}),
        "transcript_main_dedup_sum": dedup_usage(main_usage),
        "transcript_subagent_dedup_sum": dedup_usage(side_usage),
        "total_cost_usd": r.get("total_cost_usd"),
        "modelUsage_costUSD": {k: v.get("costUSD") for k, v in model_usage.items()},
        "num_turns": r.get("num_turns"),
        "unique_assistant_messages_main_transcript": len(main_usage),
        "unique_assistant_messages_stream_main": len({m["id"] for m in f["stream"]["assistant_messages"] if m["id"] and not m["parent"]}),
        "tool_use_blocks_stream": len(f["stream"]["tool_uses"]),
        "tool_use_blocks_stream_main": len(main_tools(f)),
        "tool_use_blocks_transcripts": len(f["transcript"]["tool_uses"]),
        "hook_pre_tool_use": len(pre), "hook_post_tool_use": len(post),
        "otel_console_lines": otel_lines,
    }


def t1_inventory(env_dir: Path, probes: dict) -> dict:
    rows = [x for x in (t1_run_crosscheck(d.parent, probes) for d in sorted(env_dir.glob("*/*/run.json"))) if x]
    static_dir = env_dir / "T1" / "static"
    static = {p.name: True for p in static_dir.glob("*")} if static_dir.exists() else {}

    def agree(key_a, key_b, field):
        pairs = [(r[key_a][field], r[key_b][field]) for r in rows if r.get(key_a) and r.get(key_b)]
        return {"runs": len(pairs), "equal": sum(1 for a, b in pairs if a == b)}

    executed = bool(rows)
    cost_state_runs = []
    for tm in sorted(env_dir.rglob("transcript/main.jsonl")):
        if '"type": "cost-state"' in tm.read_text(encoding="utf-8", errors="replace") or '"type":"cost-state"' in tm.read_text(encoding="utf-8", errors="replace"):
            cost_state_runs.append(tm.parent.parent.relative_to(E0_DIR).as_posix())
    tokens = {}
    for fld in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
        tokens[fld] = {
            "availability": "AVAILABLE" if executed and all(r["result_usage"].get(fld) is not None for r in rows) else ("OBSERVED_IN_DESKTOP_TRANSCRIPT_ONLY" if static else "UNVERIFIED"),
            "raw_sources": ["stream.jsonl result.usage." + fld, "stream.jsonl result.modelUsage.*", "transcript main.jsonl message.usage (dedupe by message.id)", "transcript subagents/*.jsonl message.usage"],
            "kind": "direct (API usage fields recorded by Claude Code; result.usage is Claude Code's aggregate of them)",
            "recheck": "sum per-message usage deduplicated by message.id across main + subagent transcripts and compare with result.usage / modelUsage",
            "crosscheck": {"result_vs_modelUsage": agree("result_usage", "modelUsage_sum", fld),
                           "result_vs_transcript_main": agree("result_usage", "transcript_main_dedup_sum", fld)},
        }
    inv = {
        "schema": "e0-t1-inventory/1", "generated_at": utcnow(), "executed_runs": len(rows),
        "fields": {
            "elapsed_timestamps": {
                "availability": "AVAILABLE" if executed else ("OBSERVED_IN_DESKTOP_TRANSCRIPT_ONLY" if static else "UNVERIFIED"),
                "raw_sources": ["run.json started_at/finished_at/harness_elapsed_s (harness clock)", "stream.jsonl result.duration_ms / duration_api_ms", "transcript entry timestamp (ISO-8601 per entry)", "hooks.jsonl logged_at (harness clock per hook)"],
                "kind": "direct (harness clock and Claude Code clock); elapsed = derived difference",
                "recheck": "compare result.duration_ms with harness_elapsed_s and with transcript last_ts - first_ts",
                "caveat": "harness elapsed includes process start-up/shutdown; duration_api_ms excludes tool time",
            },
            **tokens,
            "provider_reported_cost": {
                "availability": "TECHNICAL_UNAVAILABLE",
                "raw_sources": ["none locally: no provider-reported cost field exists in stream.jsonl, transcripts or hooks"],
                "related_derived_value": "stream.jsonl result.total_cost_usd and result.modelUsage.*.costUSD; transcript 'cost-state' entry (totalCostUSD, modelUsage) written at session end",
                "transcript_cost_state_seen_in": cost_state_runs,
                "kind": "derived — Claude Code computes costUSD client-side from token counts and a built-in per-model price table (canonicalModel 'used for the pricing lookup'); see T1/static/cost-computation-evidence.txt",
                "recheck": "recompute from tokens x published per-MTok prices; compare with total_cost_usd",
                "caveat": "under subscription (claude.ai OAuth) auth there is no per-request provider bill; under API-key auth the authoritative figure is the provider's usage/cost reporting outside Claude Code",
                "observed": [{"run": r["run_dir"], "total_cost_usd": r["total_cost_usd"]} for r in rows],
            },
            "assistant_turns": {
                "availability": "AVAILABLE" if executed else ("OBSERVED_IN_DESKTOP_TRANSCRIPT_ONLY" if static else "UNVERIFIED"),
                "raw_sources": ["stream.jsonl result.num_turns", "unique assistant message ids in transcript main.jsonl / stream"],
                "kind": "num_turns direct (Claude Code counter); API-call count derived from unique message ids",
                "recheck": "compare num_turns with unique main-session assistant message ids",
                "caveat": "num_turns semantics are Claude Code's (agentic turns), not necessarily equal to API calls; subagent calls are separate",
                "observed": [{"run": r["run_dir"], "num_turns": r["num_turns"], "unique_msgs_transcript": r["unique_assistant_messages_main_transcript"], "unique_msgs_stream": r["unique_assistant_messages_stream_main"]} for r in rows],
            },
            "structured_tool_calls": {
                "availability": "AVAILABLE" if executed else ("OBSERVED_IN_DESKTOP_TRANSCRIPT_ONLY" if static else "UNVERIFIED"),
                "raw_sources": ["stream.jsonl assistant tool_use blocks (+ parent_tool_use_id for subagents)", "transcript tool_use blocks", "hooks.jsonl PreToolUse/PostToolUse"],
                "kind": "direct",
                "recheck": "count tool_use blocks in stream vs transcript vs PreToolUse hook events",
                "observed": [{"run": r["run_dir"], "stream": r["tool_use_blocks_stream"], "transcripts": r["tool_use_blocks_transcripts"], "hook_pre": r["hook_pre_tool_use"], "hook_post": r["hook_post_tool_use"]} for r in rows],
            },
        },
        "otel_console_exporter": {"runs_with_otel_lines": sum(1 for r in rows if r["otel_console_lines"])},
        "static_evidence": sorted(static),
        "per_run": rows,
    }
    write_json(env_dir / "T1" / "telemetry-inventory.json", inv)
    return inv


def t1_static(env_dir: Path, transcript: Path, claude: Path) -> None:
    """Structure-only inventory of an existing session transcript (no content copied) + cost-computation evidence."""
    out = env_dir / "T1" / "static"
    out.mkdir(parents=True, exist_ok=True)
    types, keys, usage_keys, content_types, att = {}, {}, {}, {}, {}
    msgs = {}
    first = last = None
    for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type")
        types[t] = types.get(t, 0) + 1
        keys.setdefault(t, set()).update(e.keys())
        ts = e.get("timestamp")
        if ts:
            first, last = min(first or ts, ts), max(last or ts, ts)
        m = e.get("message")
        if isinstance(m, dict):
            u = m.get("usage")
            if isinstance(u, dict):
                for k, v in u.items():
                    usage_keys[k] = type(v).__name__
                if m.get("id"):
                    msgs.setdefault(m["id"], set()).add(json.dumps({k: u.get(k) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")}))
            for b in m.get("content") or [] if isinstance(m.get("content"), list) else []:
                if isinstance(b, dict):
                    content_types[f"{t}/{b.get('type')}"] = content_types.get(f"{t}/{b.get('type')}", 0) + 1
        a = e.get("attachment")
        if isinstance(a, dict):
            att[a.get("type")] = att.get(a.get("type"), 0) + 1
    write_json(out / "desktop-session-transcript-structure.json", {
        "note": "Structure-only inventory of the orchestrating desktop Code-tab session transcript (no message content copied).",
        "transcript_sha256_at_capture": sha256_file(transcript), "captured_at": utcnow(),
        "entry_types": types, "keys_by_entry_type": {k: sorted(v) for k, v in keys.items()},
        "usage_keys": usage_keys, "content_block_types": content_types, "attachment_types": att,
        "has_timestamps": bool(first), "first_ts": first, "last_ts": last,
        "assistant_entries_unique_message_ids": len(msgs),
        "message_ids_with_inconsistent_usage_across_entries": sum(1 for v in msgs.values() if len(v) > 1),
        "cost_fields_present": any("cost" in k.lower() for ks in keys.values() for k in ks) or any("cost" in k.lower() for k in usage_keys),
    })
    data = claude.read_bytes()
    snippets = []
    for pat, limit in ((rb".{0,160}Canonical model id used for the pricing lookup.{0,120}", 1),
                       (rb"\{inputTokens:[\d.]+,outputTokens:[\d.]+,promptCacheWriteTokens:[\d.]+,promptCacheWrite1hTokens:[\d.]+,promptCacheReadTokens:[\d.]+,webSearchRequests:[\d.]+\}", 20),
                       (rb".{0,160}totalCostUSD:.{0,160}", 1)):
        found = []
        for m in re.finditer(pat, data):
            s = re.sub(r"[^\x20-\x7e]", "?", m.group(0).decode("utf-8", errors="replace"))
            if s not in found:
                found.append(s)
            if len(found) >= limit:
                break
        snippets.extend(found)
    (out / "cost-computation-evidence.txt").write_text(
        f"Claude Code binary: {claude}\nsha256: {sha256_bytes(data)}\n"
        "Extracted strings showing that costUSD / total_cost_usd are computed client-side from token counts and built-in per-model price tables (USD per million tokens):\n\n"
        + "\n---\n".join(snippets) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- summary

PROBE_QUESTIONS = {
    "E0-R1": "Are rules in nested .claude/rules/<group>/ discovered?",
    "E0-R2": "Do path-scoped rules apply on read/edit/new-file work as intended?",
    "E0-S1": "Is .claude/skills/<name>/SKILL.md discovered and triggered from its description?",
    "E0-S2": "Can private skill references be reached through the owning skill without becoming ordinary global policy?",
    "E0-A1": "Does the subagent + skills: preload mechanism work in this Claude Code version?",
    "E0-I1": "Do CLAUDE.md imports work in the intended shape, including nested imports?",
    "E0-T1": "Which telemetry fields are reliably obtainable from local Claude Code artifacts?",
    "E0-W1": "Is the launch root an access boundary under the permission modes considered for the benchmark?",
}


STARTUP_SCOPE = {
    "E0-R1": ("full", "rule discovery happens at session start; the transcript's instructions record is what Claude Code sends to the model"),
    "E0-I1": ("full", "imports are resolved at session start; the instructions record and include hooks show the assembled context"),
    "E0-R2": ("partial", "shows only that path-scoped rules are not loaded unconditionally; loading on Read/Edit/Write needs model-driven tool calls"),
    "E0-S1": ("partial", "shows discovery/listing (and name collisions) only; description-based triggering needs the model"),
    "E0-S2": ("partial", "shows only that the reference and skill body are not global context; reachability via the owning skill needs the model"),
    "E0-A1": ("partial", "shows agent and skill discovery only; preloading into a spawned subagent needs the model"),
}


def latest_runs(env_dir: Path) -> dict:
    """All evaluated runs grouped by run name (repeats kept); startup-only runs keyed 'startup:<run>'."""
    out = {}
    for chk in sorted(env_dir.rglob("checks.json")):
        data = read_json(chk)
        if data:
            data["_dir"] = chk.parent.relative_to(E0_DIR).as_posix()
            key = ("startup:" if data.get("mode") == "startup-only" else "") + data["run"]
            out.setdefault(key, []).append(data)
    return out


def run_brief(lst):
    return [{"dir": r["_dir"], "valid": r["valid"], "invalid_reasons": r["invalid_reasons"], "all_checks_pass": r["all_checks_pass"],
             "w1_classification": r.get("w1_classification"),
             "failed_checks": [c["id"] for c in r["checks"] if not c["pass"]]} for r in lst]


def startup_status(pid: str, su: dict) -> tuple[str, str]:
    if pid not in STARTUP_SCOPE or not su:
        return "NOT_EXECUTED", "no startup-only evidence"
    valid = {n: [r for r in lst if r["valid"]] for n, lst in su.items()}
    if any(not v for v in valid.values()):
        return "INCONCLUSIVE", f"startup runs without valid evidence: {[n for n, v in valid.items() if not v]}"
    bad = {n: sorted({c["id"] for r in v for c in r["checks"] if not c["pass"]}) for n, v in valid.items()}
    bad = {n: v for n, v in bad.items() if v}
    return ("FAIL", f"startup checks failed: {bad}") if bad else ("PASS", "all startup-context checks hold")


def summarize(env_dir: Path, probes: dict) -> dict:
    runs = latest_runs(env_dir)
    env = read_json(env_dir / "environment.json", {})
    probes_out = {}
    for pid, q in PROBE_QUESTIONS.items():
        mine = {n: lst for n, lst in runs.items() if not n.startswith("startup:") and lst[0]["probe"] == pid}
        su = {n[len("startup:"):]: lst for n, lst in runs.items() if n.startswith("startup:") and lst[0]["probe"] == pid}
        expected = [r["run"] for r in probes["runs"] if r["probe"] == pid and r.get("behavioral", True)]
        required = [r["run"] for r in probes["runs"] if r["probe"] == pid and r.get("behavioral", True) and not r.get("optional")]
        missing = [n for n in required if n not in mine]
        b_status, b_rat = probe_status(pid, mine, missing)
        s_status, s_rat = startup_status(pid, su)
        scope, scope_note = STARTUP_SCOPE.get(pid, (None, None))
        if b_status != "NOT_EXECUTED":
            status, rationale, level = b_status, b_rat, "behavioral (fresh headless sessions)"
        elif s_status == "NOT_EXECUTED":
            status, rationale, level = "NOT_EXECUTED", b_rat, None
        elif s_status in ("FAIL", "INCONCLUSIVE") or scope == "full":
            status, rationale, level = s_status, f"{s_rat} ({scope_note})", "startup-context record (no model call)"
        else:
            status, rationale, level = "INCONCLUSIVE", f"startup part {s_status}: {scope_note}; behavioral runs NOT_EXECUTED", "startup-context record (partial)"
        probes_out[pid] = {
            "question": q, "status": status, "evidence_level": level, "rationale": rationale,
            "behavioral_status": b_status, "behavioral_rationale": b_rat,
            "startup_status": s_status if pid in STARTUP_SCOPE else "N/A", "startup_scope": scope,
            "runs_expected": expected, "runs_missing": missing,
            "runs": {n: run_brief(lst) for n, lst in mine.items()},
            "startup_runs": {n: run_brief(lst) for n, lst in su.items()},
        }
        coll = su.get("S1-collision") or mine.get("S1-collision")
        if coll:
            probes_out[pid]["skill_name_collision"] = {c["id"]: c["observed"] for c in coll[-1]["checks"]}
    inv = t1_inventory(env_dir, probes)
    t1 = probes_out["E0-T1"]
    t1["inventory"] = "T1/telemetry-inventory.json"
    unavailable = [k for k, v in inv["fields"].items() if v["availability"] != "AVAILABLE"]
    if inv["executed_runs"] and t1["behavioral_status"] != "INCONCLUSIVE":
        t1["status"] = "PASS" if not unavailable else "LIMITED"
        t1["evidence_level"] = "behavioral (fresh headless sessions)"
        t1["rationale"] = f"{inv['executed_runs']} headless runs inventoried; not directly available: {unavailable}"
    elif not inv["executed_runs"] and inv["static_evidence"]:
        t1["status"] = "INCONCLUSIVE"
        t1["evidence_level"] = "static (artifact structure + binary cost computation)"
        t1["rationale"] = "field structure and cost derivation established statically; values and cross-checks need authenticated headless runs"
    summary = {"schema": "e0-summary/1", "generated_at": utcnow(), "harness_version": HARNESS_VERSION,
               "environment": env, "preflight": read_json(env_dir / "preflight.json"), "probes": probes_out}
    write_json(env_dir / "summary.json", summary)
    return summary


def probe_status(pid: str, mine: dict, missing: list) -> tuple[str, str]:
    if not mine:
        return "NOT_EXECUTED", "no evaluated run evidence"
    valid = {n: [r for r in lst if r["valid"]] for n, lst in mine.items()}
    if any(not v for v in valid.values()) or missing:
        return "INCONCLUSIVE", f"missing runs {missing} or runs without a valid execution: {[n for n, v in valid.items() if not v]}"

    def passed(n):
        return all(r["all_checks_pass"] for r in valid.get(n, []))

    def failed_ids(n):
        return sorted({c for r in mine.get(n, []) for c in [x["id"] for x in r["checks"] if not x["pass"]]})

    if pid in ("E0-R1", "E0-I1", "E0-S2", "E0-A1"):
        bad = {n: failed_ids(n) for n in valid if not passed(n)}
        return ("PASS", "all positive/negative checks hold") if not bad else ("FAIL", f"failed checks: {bad}")
    if pid == "E0-S1":
        pos = valid.get("S1-pos", [])
        k = sum(1 for r in pos if r["all_checks_pass"])
        if not passed("S1-neg"):
            return "FAIL", f"negative control failed: {failed_ids('S1-neg')}"
        if k == len(pos):
            return "PASS", f"skill triggered in {k}/{len(pos)} positive runs; negative control clean"
        return ("LIMITED" if k else "FAIL"), f"skill triggered in {k}/{len(pos)} positive runs; failed checks {failed_ids('S1-pos')}"
    if pid == "E0-R2":
        core = ["R2-read-match", "R2-read-nonmatch", "R2-edit-match", "R2-write-nonmatch"]
        bad = {n: failed_ids(n) for n in core if not passed(n)}
        if bad:
            return "FAIL", f"core path-scoping checks failed: {bad}"
        if passed("R2-write-new-match"):
            return "PASS", "read, edit, new-file and non-matching controls all behave as intended"
        return "LIMITED", f"read/edit/non-match as intended; new-file creation differs: failed {failed_ids('R2-write-new-match')}"
    if pid == "E0-T1":
        return "PENDING_INVENTORY", "status is set from T1/telemetry-inventory.json"
    if pid == "E0-W1":
        cls = {n: [r.get("w1_classification") for r in lst] for n, lst in valid.items()}
        flat = [c for v in cls.values() for c in v]
        if all(c == "REACHABLE" for c in flat):
            return "FAIL", f"outside-root canary reachable in every tested mode: {cls}"
        if any(c == "REACHABLE" for c in flat):
            return "LIMITED", f"boundary depends on permission mode: {cls}"
        if any(c == "INCONCLUSIVE" for c in flat):
            return "INCONCLUSIVE", f"{cls}"
        return "PASS", f"outside-root canary not reachable without a gate in any tested mode: {cls}"
    return "INCONCLUSIVE", "no status rule"


# --------------------------------------------------------------------------- CLI

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claude", help="path to the Claude Code binary (default: $E0_CLAUDE, PATH, or the desktop-bundled CLI)")
    ap.add_argument("--workroot", help="where fresh workspaces are created (default: $E0_WORKROOT or <tmp>/e0-runs)")
    ap.add_argument("--env-id", help="override the results/<env-id> directory name")
    ap.add_argument("--expect-version", default=os.environ.get("E0_EXPECT_VERSION"),
                    help="abort unless `claude --version` starts with this (the desktop app auto-updates its bundled CLI)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("env")
    sub.add_parser("selftest")
    p_run = sub.add_parser("run")
    p_run.add_argument("runs", nargs="+")
    p_run.add_argument("--debug", action="store_true", help="also write a Claude Code debug log (kept outside the repo)")
    p_su = sub.add_parser("startup", help="startup-only runs: no model request leaves the machine")
    p_su.add_argument("runs", nargs="+")
    p_su.add_argument("--debug", action="store_true")
    p_prep = sub.add_parser("prepare")
    p_prep.add_argument("run")
    p_col = sub.add_parser("collect")
    p_col.add_argument("run_dir")
    p_col.add_argument("--session-id", required=True)
    p_ev = sub.add_parser("evaluate")
    p_ev.add_argument("dirs", nargs="*")
    sub.add_parser("summarize")
    sub.add_parser("reexport", help="re-export (and re-redact) evidence from the raw run directories, then re-evaluate")
    sub.add_parser("preflight", help="record auth status and whether a fresh headless process can complete one minimal request")
    p_t1 = sub.add_parser("t1-static", help="structure-only telemetry inventory of an existing transcript + cost-computation evidence")
    p_t1.add_argument("--transcript", required=True)
    args = ap.parse_args()

    probes = load_probes()
    defs = run_defs(probes)
    workroot = Path(args.workroot or os.environ.get("E0_WORKROOT") or Path(tempfile.gettempdir()) / "e0-runs")
    workroot.mkdir(parents=True, exist_ok=True)

    if args.cmd == "selftest":
        report = {}
        for name, rd in defs.items():
            m = materialize(rd, workroot / f"selftest-{name}")
            prompt = render_prompt(rd, m["canaries"])
            unresolved = re.findall(r"\{[A-Z_]+\}", prompt)
            report[name] = {"fixture_sha256": m["fixture_sha256"], "gate_passed": m["gate"]["passed"], "gate": m["gate"]["project_instruction_files_in_ancestors"],
                            "unresolved_placeholders": unresolved, "files": sorted(read_json(m["live"] / "fixture-manifest.json")["files"])}
        print(json.dumps(report, indent=2))
        return

    claude = resolve_claude(args.claude)
    version = claude_version(claude)
    if args.expect_version and not version.startswith(args.expect_version):
        sys.exit(f"Claude Code version mismatch: expected {args.expect_version}, binary {claude} reports {version!r}")
    envid = args.env_id or env_id(version, probes["defaults"]["model"])
    env_dir = RESULTS / envid

    if args.cmd == "env":
        write_json(env_dir / "environment.json", environment(claude, probes, workroot))
        print(env_dir / "environment.json")
    elif args.cmd == "prepare":
        rd = defs[args.run]
        m = materialize(rd, workroot / f"{args.run}-{stamp()}")
        print(json.dumps({"workspace": str(m["ws"]), "prompt": render_prompt(rd, m["canaries"]), "gate": m["gate"]}, indent=2))
    elif args.cmd == "run":
        if not (env_dir / "environment.json").exists():
            write_json(env_dir / "environment.json", environment(claude, probes, workroot))
        names = [n for n, rd in defs.items() if rd.get("behavioral", True)] if args.runs == ["all"] else args.runs
        for name in names:
            rd = defs[name]
            for _ in range(int(rd.get("repeat", 1))):
                run_one(name, rd, probes, claude, workroot, envid, args.debug)
        summarize(env_dir, probes)
    elif args.cmd == "startup":
        if not (env_dir / "environment.json").exists():
            write_json(env_dir / "environment.json", environment(claude, probes, workroot))
        names = [n for n, rd in defs.items() if rd.get("startup")] if args.runs == ["all"] else args.runs
        for name in names:
            run_one(name, defs[name], probes, claude, workroot, envid, args.debug, startup=True)
        summarize(env_dir, probes)
    elif args.cmd == "collect":
        run_dir = Path(args.run_dir)
        live, ws = run_dir / "live", run_dir / "ws"
        name = re.sub(r"-\d{8}T\d{6}Z$", "", run_dir.name)
        rd = defs[name]
        collect_transcripts(args.session_id, live)
        snapshot_after(ws, live)
        dest = RESULTS / envid / rd["probe"].replace("E0-", "") / run_dir.name
        meta = {"schema": "e0-run/1", "run": name, "probe": rd["probe"], "role": rd.get("role"), "mode": "manual-session",
                "fixture": rd["fixture"], "workspace": str(ws), "workspace_aliases": path_aliases(ws),
                "session_id": args.session_id, "collected_at": utcnow(), "harness_version": HARNESS_VERSION, "env_id": envid,
                "note": "No stream.jsonl exists for manual sessions; checks rely on hooks.jsonl, transcript and workspace files."}
        write_json(live / "run.json", meta)
        meta["exported_files"] = export(live, dest)
        write_json(dest / "run.json", meta)
        evaluate_dir(dest, probes)
        summarize(env_dir, probes)
        print(dest)
    elif args.cmd == "reexport":
        # re-apply export/redaction from the raw live directories (kept outside the repo) and re-evaluate
        for rj in sorted(env_dir.rglob("run.json")):
            meta = read_json(rj)
            if not meta or "workspace" not in meta:
                continue
            live = Path(meta["workspace"]).parent / "live"
            if not live.exists():
                print(f"raw evidence missing for {rj.parent}")
                continue
            meta["exported_files"] = export(live, rj.parent)
            write_json(rj, meta)
            evaluate_dir(rj.parent, probes)
        summarize(env_dir, probes)
    elif args.cmd == "evaluate":
        dirs = [Path(d) for d in args.dirs] or sorted({p.parent for p in env_dir.rglob("run.json") if (p.parent / "stream.jsonl").exists() or (p.parent / "hooks.jsonl").exists()})
        for d in dirs:
            evaluate_dir(d, probes)
        summarize(env_dir, probes)
    elif args.cmd == "summarize":
        print(json.dumps({k: {"status": v["status"], "rationale": v["rationale"]} for k, v in summarize(env_dir, probes)["probes"].items()}, indent=2))
    elif args.cmd == "t1-static":
        t1_static(env_dir, Path(args.transcript), claude)
        print(env_dir / "T1" / "static")
    elif args.cmd == "preflight":
        write_json(env_dir / "preflight.json", preflight(claude, probes, workroot))
        print(json.dumps(read_json(env_dir / "preflight.json"), indent=2))


if __name__ == "__main__":
    main()
