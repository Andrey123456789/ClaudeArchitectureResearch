"""Read-only state checks for the Desktop Auto hook smoke test. Run by the operator from a terminal OUTSIDE the Claude Desktop session.

Usage:  python -B check_state.py preflight | t0 | t1 | t2
        python -B check_state.py collect [--transcript FILE] [--dry-run]

  preflight  same checks as t0; records nothing
  t0         before the session starts:      baseline HEAD, probe staged, no hook state
  t1         after the Deny decision:        still no new commit, probe still staged
  t2         after the Allow decision:       exactly one new commit, containing only the probe
  collect    after the session: copies the newest session transcript to evidence/ and summarizes what it contains

This tool reports Git state and transcript contents only. It cannot see the Desktop UI and it never decides whether a person
saw or answered a permission request; those rows are recorded by the operator in RUN_INSTRUCTIONS.md. It never writes inside work/.
"""
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(OUT, "evidence")
REL = os.path.normpath(os.path.join(OUT, "..", "phase54_final_acceptance_v1", "release"))
M = json.load(open(os.path.join(OUT, "SETUP_MANIFEST.json"), encoding="utf-8"))
WORK = M["work_dir"]
BASE = M["state"]["head"]
PROBE = M["probe"]["file"]
HOOK_TEXT = "Repository-changing Git command"


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git(*a):
    return subprocess.run(["git", "--no-optional-locks", "-C", WORK, *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


def frozen_diffs():
    files = json.load(open(os.path.join(REL, "CANDIDATE_FREEZE_MANIFEST.json"), encoding="utf-8"))["candidates"]["K0"]["files"]
    return sorted(r for r, row in files.items() if not os.path.exists(os.path.join(WORK, r)) or sha(os.path.join(WORK, r)) != row["sha256"])


def snapshot():
    head = git("rev-parse", "HEAD")
    return {"head": head, "commit_count": int(git("rev-list", "--count", "HEAD")), "log": git("log", "--format=%h %s").splitlines(), "staged": git("diff", "--cached", "--name-status").splitlines(), "status": git("status", "--porcelain=v1", "--untracked-files=all").splitlines(),
            "parent_of_head": git("rev-parse", "--verify", "-q", "HEAD^"), "head_changes": git("show", "--name-status", "--format=", "HEAD").splitlines(), "hook_state_present": os.path.isdir(os.path.join(WORK, ".claude", ".hook-state")), "local_settings_present": os.path.exists(os.path.join(WORK, ".claude", "settings.local.json")), "k0_files_differing_from_frozen": frozen_diffs()}


def evaluate(stage, s):
    staged = ["A\t" + PROBE]
    if stage in ("preflight", "t0"):
        c = {"head_is_baseline": s["head"] == BASE, "one_commit": s["commit_count"] == 1, "probe_is_the_only_staged_file": s["staged"] == staged, "no_hook_state_yet": not s["hook_state_present"]}
    elif stage == "t1":
        c = {"head_is_baseline": s["head"] == BASE, "one_commit": s["commit_count"] == 1, "probe_is_the_only_staged_file": s["staged"] == staged}
    else:
        c = {"exactly_one_new_commit": s["commit_count"] == 2, "new_commit_parent_is_baseline": s["parent_of_head"] == BASE and s["head"] != BASE, "new_commit_contains_only_probe": s["head_changes"] == staged, "nothing_left_staged": s["staged"] == []}
    c["no_k0_file_changed"] = s["k0_files_differing_from_frozen"] == []
    c["no_local_permission_rule_file"] = not s["local_settings_present"]
    return c


def stage_check(stage):
    s = snapshot()
    c = evaluate(stage, s)
    rec = {"stage": stage, "at": now(), "git_state": "PASS" if all(c.values()) else "FAIL", "checks": c, "state": s, "scope_note": "Git state only; says nothing about any permission request or who answered it"}
    if stage != "preflight":
        with open(os.path.join(EVID, "state_checks.jsonl"), "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, indent=1, ensure_ascii=False))
    sys.exit(0 if rec["git_state"] == "PASS" else 1)


def blocks(o):
    c = (o.get("message") or {}).get("content")
    return c if isinstance(c, list) else []


def collect(argv):
    slug = re.sub(r"[^A-Za-z0-9]", "-", WORK)
    d = os.path.join(os.path.expanduser("~"), ".claude", "projects", slug)
    if "--transcript" in argv:
        path = argv[argv.index("--transcript") + 1]
        sessions = [path]
    else:
        sessions = sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime)
        if not sessions:
            raise SystemExit("no session transcript found in " + d)
        path = sessions[-1]
    versions, modes, entry, attach = set(), {}, set(), {}
    uses, results, hook_lines = [], {}, []
    n = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            if HOOK_TEXT in line:
                hook_lines.append(n)
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("version"):
                versions.add(o["version"])
            if o.get("entrypoint"):
                entry.add(o["entrypoint"])
            if "permissionMode" in o:
                modes[o["permissionMode"]] = modes.get(o["permissionMode"], 0) + 1
            if o.get("type") == "attachment":
                k = (o.get("attachment") or {}).get("type")
                attach[k] = attach.get(k, 0) + 1
            for b in blocks(o):
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and "command" in (b.get("input") or {}):
                    uses.append({"line": n, "at": o.get("timestamp"), "id": b.get("id"), "tool": b.get("name"), "command": b["input"]["command"]})
                elif b.get("type") == "tool_result":
                    c = b.get("content")
                    t = c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c if isinstance(x, dict)) if isinstance(c, list) else str(c)
                    results[b.get("tool_use_id")] = {"line": n, "at": o.get("timestamp"), "is_error": bool(b.get("is_error")), "text": t[:800]}
    for u in uses:
        u["result"] = results.get(u["id"])
    commits = [u for u in uses if re.search(r"\bgit\b.*\bcommit\b", u["command"])]
    summary = {"at": now(), "transcript": path, "sessions_found_for_this_folder": len(sessions), "lines": n, "cli_versions_in_transcript": sorted(versions), "entrypoints": sorted(entry), "permissionMode_values": modes, "commands_run": [{k: u[k] for k in ("line", "tool", "command")} for u in uses], "git_commit_attempts": commits, "lines_containing_k0_hook_text": hook_lines, "hook_related_attachment_types": {k: v for k, v in attach.items() if k and "hook" in k}, "hook_text_found_in_transcript": bool(hook_lines),
               "ui_interaction": "NOT DERIVABLE FROM THIS FILE. Whether a permission card was shown and what a person chose is recorded only by the operator."}
    if "--dry-run" in argv:
        print(json.dumps({k: v for k, v in summary.items() if k not in ("commands_run", "git_commit_attempts")}, indent=1, ensure_ascii=False)[:1800])
        print("dry run: nothing written; commands parsed:", len(uses), "commit attempts parsed:", len(commits))
        return
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    shutil.copy2(path, os.path.join(EVID, f"transcript_{stamp}_{os.path.basename(path)}"))
    with open(os.path.join(EVID, f"transcript_summary_{stamp}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(summary, indent=1, ensure_ascii=False))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd in ("preflight", "t0", "t1", "t2"):
        stage_check(cmd)
    elif cmd == "collect":
        collect(sys.argv[2:])
    else:
        raise SystemExit("usage: preflight | t0 | t1 | t2 | collect [--transcript FILE] [--dry-run]")


if __name__ == "__main__":
    main()
