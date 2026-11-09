"""Hermetic execution helpers. Everything runs on disposable copies under _scratch, with temp variables pointed inside the fence."""
import json
import os
import shutil
import subprocess
import uuid

from rcommon import SCRATCH, template_root, wc_path

PRE_TOOL = {'M': ['.claude/hooks/dependency-guard.mjs'], 'M1': ['.claude/hooks/pre-tool-use.js'], 'L0': ['.claude/hooks/claude-hook.mjs', 'pre-bash'], 'L1': ['.claude/hooks/pre-shell-command.mjs'],
            'K0': ['.claude/hooks/hook.cjs', 'pre-tool-use'], 'K1': ['.claude/hooks/dispatch.cjs', 'PreToolUse']}
CHECKERS = {'M': [['.claude/scripts/check-instructions.mjs'], ['.claude/scripts/check-manifests.mjs']],
            'M1': [['.claude/scripts/check-instructions.js'], ['.claude/scripts/check-manifests.js'], ['.claude/scripts/check-architecture.js']],
            'L0': [['.claude/tools/check-instructions.mjs']],
            'L1': [['.claude/scripts/check-instructions.mjs'], ['.claude/scripts/check-architecture.mjs']],
            'K0': [['.claude/scripts/check-instructions.cjs'], ['.claude/scripts/check-dependencies.cjs']],
            'K1': [['.claude/scripts/check-instructions.cjs'], ['.claude/scripts/check-manifests.cjs'], ['.claude/scripts/check-cochange.cjs']]}


def scratch_dir(*parts):
    d = os.path.join(SCRATCH, *parts)
    os.makedirs(d, exist_ok=True)
    return d


def fresh_copy(c, tag=None):
    d = os.path.join(SCRATCH, 'runs', '%s-%s-%s' % (c, tag or 't', uuid.uuid4().hex[:8]))
    shutil.copytree(template_root(c), d)
    return d


def env_for(root):
    tmp = scratch_dir('tmp')
    e = dict(os.environ)
    e.update({'TEMP': tmp, 'TMP': tmp, 'TMPDIR': tmp, 'CLAUDE_PROJECT_DIR': root, 'CLAUDE_HOOK_STATE_DIR': scratch_dir('hookstate', uuid.uuid4().hex[:8]), 'GIT_CONFIG_NOSYSTEM': '1',
              'GIT_TERMINAL_PROMPT': '0', 'NO_COLOR': '1'})
    e.pop('npm_config_force', None)
    e.pop('npm_config_legacy_peer_deps', None)
    return e


def run_node(root, args, stdin=None, timeout=120):
    r = subprocess.run(['node'] + args, cwd=root, input=stdin, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env_for(root), timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def pre_tool(root, c, command, tool='Bash'):
    """Runs the candidate's PreToolUse hook once. Returns decision in allow, deny, ask, block, plus the raw output."""
    payload = json.dumps({'hook_event_name': 'PreToolUse', 'session_id': 'fixture', 'tool_name': tool, 'tool_input': {'command': command}, 'cwd': root})
    code, out, err = run_node(root, PRE_TOOL[c], payload)
    decision = 'allow'
    if code == 2:
        decision = 'block'
    elif code != 0:
        decision = 'error:%d' % code
    elif out.strip():
        try:
            o = json.loads(out.strip().splitlines()[-1])
            d = (o.get('hookSpecificOutput') or {}).get('permissionDecision')
            if d:
                decision = d
            elif o.get('decision') == 'block':
                decision = 'block'
        except ValueError:
            pass
    return decision, out + err


def run_checkers(c, root=None):
    root = root or fresh_copy(c, 'chk')
    rows = []
    for args in CHECKERS[c]:
        code, out, err = run_node(root, args)
        rows.append({'candidate': c, 'checker': args[0], 'exit': code, 'tail': (out + err).strip().splitlines()[-1:] if (out + err).strip() else [], 'output_chars': len(out + err), 'full': (out + err)[-3000:]})
    return rows


def git(cwd, *args):
    e = env_for(cwd)
    e.update({'GIT_AUTHOR_NAME': 'fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid', 'GIT_COMMITTER_NAME': 'fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid'})
    r = subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'init.defaultBranch=main', '-c', 'commit.gpgsign=false'] + list(args), cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=e, timeout=60)
    return r.returncode, r.stdout, r.stderr


def cleanup_runs():
    shutil.rmtree(os.path.join(SCRATCH, 'runs'), ignore_errors=True)
