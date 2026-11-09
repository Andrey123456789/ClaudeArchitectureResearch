"""PV2-01 regression: equivalent Git PreToolUse gating in all six candidates (kit 74 Part B PV2-01).

Every case runs each candidate's real PreToolUse hook directly on a disposable copy. Expected: read-only Git allowed without a Git prompt;
repository-changing Git asks; a non-Git deny or block wins over the Git ask; the reason names the authority rule. How a live host shows the
ask and what a user answers is NOT_RUN. The ask is not authorization (R02 and C04 model that part and replay in the cumulative run).
"""
import json
import os
import re
import shutil
import subprocess

from rcommon import CANDIDATES, norm_ws, out_path, read_lines, wc_path
from sandbox import PRE_TOOL, env_for, fresh_copy, run_node
from suitelib import has, mutate_text

RULE = 'PV2-01-GIT-GATING'
DENIED = ('deny', 'block')
HOOK_WITH_TABLE = {'M': '.claude/hooks/dependency-guard.mjs', 'M1': '.claude/scripts/lib/dependency-commands.js', 'L0': '.claude/hooks/claude-hook.mjs', 'L1': '.claude/hooks/pre-shell-command.mjs', 'K1': '.claude/scripts/classify-command.cjs'}
BLOCK_START = '// ---------- Git: repository-changing vs read-only (PV2-01) ----------'
BLOCK_END = '// ---------- end of Git table (PV2-01) ----------'

READ_ONLY = ['git status', 'git diff --cached', 'git log --oneline -5', 'git show HEAD', 'git -C sub status', 'git -c core.pager=cat log', 'git --no-pager diff', 'git branch', 'git branch -a',
             'git branch --show-current', 'git tag', 'git tag -l', 'git stash list', 'git remote -v', 'git config --get user.name', 'git rev-parse --abbrev-ref HEAD', 'git ls-files', 'git blame README.md',
             'git --version', 'git log --oneline | head -5', 'git status; git diff', 'bash -c "git status"', 'ls -la', 'echo "git commit -m x"', 'grep -r "git push" .']
MUTATING = ['git commit -m x', 'git add .', 'git push', 'git push --force origin main', 'git reset --hard', 'git checkout main', 'git switch dev', 'git clean -fd', 'git branch -D old', 'git tag v1',
            'git stash', 'git stash push -m wip', 'git rebase main', 'git merge feature', 'git pull', 'git fetch origin', 'git cherry-pick abc123', 'git revert abc123', 'git rm old.txt', 'git mv a b',
            'git restore x.cs', 'git config user.name x', 'git remote add o https://example.invalid/r.git', 'git -C sub commit -m x', 'git -c user.name=x commit -m y', 'git --git-dir=.git --work-tree=. commit -m z',
            'git init', 'git apply fix.patch', 'git worktree add ../w', 'git submodule update', 'bash -c "git reset --hard"', "sh -c 'git commit -m x'", 'cmd /c git push', 'pwsh -Command "git push --force"',
            'powershell -Command "git clean -fdx"', 'env GIT_DIR=.git git commit -m y', 'GIT_AUTHOR_NAME=x git commit -m y', 'git status && git commit -m x', 'git add . && git commit -m "a; b"',
            'git commit -m "fix: one; two"', '/usr/bin/git push']
POWERSHELL_MUTATING = ['& git commit -m x', '& "C:\\Program Files\\Git\\cmd\\git.exe" commit -m x', 'git push; Write-Output done']
DENY_WINS = ['npm i left-pad@1.3.0 --force && git commit -m x', 'git commit -m x && npm i left-pad@1.3.0 --legacy-peer-deps', 'bash -c "npm install left-pad@1.3.0 --force; git push"']
# Known, reported difference: K0 classifies the first recognized tool anywhere in a segment.
K0_ONLY_ASK = ['echo git commit -m x']


def decision(code, out):
    if code == 2:
        return 'block'
    for line in reversed((out or '').strip().splitlines()):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        d = (o.get('hookSpecificOutput') or {}).get('permissionDecision')
        if d:
            return d
        if o.get('decision') == 'block':
            return 'block'
    return 'allow' if code == 0 else 'error:%d' % code


def run_hook(root, c, command, tool='Bash'):
    payload = json.dumps({'hook_event_name': 'PreToolUse', 'session_id': 'fixture', 'tool_name': tool, 'tool_input': {'command': command}, 'cwd': root})
    code, out, err = run_node(root, PRE_TOOL[c], payload)
    return decision(code, out), out + err


def block_text(c):
    s = '\n'.join(read_lines(wc_path(c, HOOK_WITH_TABLE[c])))
    a, b = s.find(BLOCK_START), s.find(BLOCK_END)
    return s[a:b + len(BLOCK_END)] if a >= 0 and b > a else None


def k0_table():
    s = '\n'.join(read_lines(wc_path('K0', '.claude/hooks/hook.cjs')))
    a = s.index('const GIT_GLOBAL_VALUE_OPTIONS')
    b = s.index('function classifyGit(args) {', a)
    e = s.index('\n}\n', b) + 2
    return s[a:e]


def normalized_table(text):
    """K0 and the five copies differ only in the helper names and comments; everything else must be identical."""
    t = text[text.index('const GIT_GLOBAL_VALUE_OPTIONS'):]
    start = t.index('function classifyGit(args) {')
    t = t[:t.index('\n}', start) + 2]
    t = re.sub(r'(?m)^\s*// .*$', '', t)
    for name in ('gitHasAny', 'hasAny', 'gitPositionals'):
        t = re.sub(r'function %s\([^)]*\) \{.*?\n\}\n' % name, '', t, flags=re.S)
    t = t.replace('gitHasAny(', 'hasAny(').replace('gitPositionals(', 'positionalsOf(')
    return norm_ws(t)


def run(ctx):
    matrix = {}
    for c in CANDIDATES:
        root = fresh_copy(c, 'pv201')
        row = {}
        for cmd in READ_ONLY:
            d, raw = run_hook(root, c, cmd)
            row[cmd] = d
            ctx.check('read-only or non-Git runs without a Git prompt: %s' % cmd, d == 'allow', raw[-200:], c, 'HOOK', 'allow', d)
        for cmd in MUTATING:
            d, raw = run_hook(root, c, cmd)
            row[cmd] = d
            ctx.check('repository-changing Git asks: %s' % cmd, d == 'ask', raw[-200:], c, 'HOOK', 'ask', d)
            if cmd == 'git reset --hard':
                ctx.check('the ask reason names the authority rule, not an authorization', 'pre-approved this operation and scope' in raw, raw[-300:], c, 'HOOK')
        for cmd in POWERSHELL_MUTATING:
            d, raw = run_hook(root, c, cmd, 'PowerShell')
            row['[PowerShell] ' + cmd] = d
            ctx.check('repository-changing Git asks (PowerShell): %s' % cmd, d == 'ask', raw[-200:], c, 'HOOK', 'ask', d)
        for cmd in DENY_WINS:
            d, raw = run_hook(root, c, cmd)
            row[cmd] = d
            ctx.check('a non-Git deny or block wins over the Git ask: %s' % cmd, d in DENIED, raw[-200:], c, 'HOOK', 'deny or block', d)
        for cmd in K0_ONLY_ASK:
            d, raw = run_hook(root, c, cmd)
            row[cmd] = d
            ctx.check('documented difference: %s asks in K0 only' % cmd, d == ('ask' if c == 'K0' else 'allow'), raw[-160:], c, 'HOOK', 'ask in K0, allow elsewhere', d)
        matrix[c] = row
        shutil.rmtree(root, ignore_errors=True)
    # Same task, six candidates: every fixture except the documented one has one decision class.
    cls = lambda d: 'denied' if d in DENIED else d
    diverging = [cmd for cmd in matrix['K0'] if cmd not in K0_ONLY_ASK and len({cls(matrix[c][cmd]) for c in CANDIDATES}) != 1]
    ctx.check('same task: all six give the same decision class for every common fixture', not diverging, diverging[:6], kind='HOOK', actual=len(matrix['K0']))
    os.makedirs(out_path('_rules', RULE), exist_ok=True)
    with open(out_path('_rules', RULE, 'SAME_TASK_GIT_MATRIX.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(matrix, f, ensure_ascii=False, indent=1, sort_keys=True)
    # One table, byte-identical in the five, equal to K0's apart from helper names.
    with open(out_path('_rules', RULE, 'git_block.js'), encoding='utf-8') as f:
        ref = f.read().replace('\r\n', '\n').rstrip('\n')
    texts = {c: block_text(c) for c in HOOK_WITH_TABLE}
    for c, t in texts.items():
        ctx.check('the Git table block is the reference block, byte for byte', t is not None and t.replace('\r\n', '\n') == ref, None if t else 'missing', c, 'SOURCE')
    ctx.check('the block equals K0 table apart from helper names', normalized_table(ref) == normalized_table(k0_table()), kind='SOURCE')
    # The M1 post-command manifest check does not change meaning: Git is not a manifest change.
    root = fresh_copy('M1', 'pv201m1')
    lib = os.path.join(root, '.claude', 'scripts', 'lib', 'dependency-commands.js').replace('\\', '/')
    r = subprocess.run(['node', '-e', "const d=require(process.argv[1]); console.log(JSON.stringify([d.changesManifests('git commit -m x','Bash'), d.changesManifests('npm i left-pad@1.3.0','Bash')]))", lib], capture_output=True, text=True, env=env_for(root), timeout=60)
    ctx.check('M1 changesManifests: a Git command is not a manifest change, an npm install still is', r.stdout.strip() == '[false,true]', r.stdout + r.stderr, 'M1', 'LOGIC')
    shutil.rmtree(root, ignore_errors=True)
    # Instruction text: the enforcement sentence and the not-authorization clause in each git-workflow.
    for c in CANDIDATES:
        rel = '.claude/skills/git-workflow/SKILL.md'
        ctx.check('git-workflow names the hook that asks for repository-changing Git', has(c, rel, 'asks the user to confirm Git commands it classifies as repository-changing'), candidate=c, kind='SOURCE')
        if c != 'K0':
            ctx.check('git-workflow says the prompt is not authorization', has(c, rel, 'The prompt is not authorization'), candidate=c, kind='SOURCE')
        ctx.check('CLAUDE.md keeps the authority rule: generic workflow approval is not authority', has(c, 'CLAUDE.md', 'is not that authority'), candidate=c, kind='SOURCE')
    # Mutations: a disabled classifier or a Git ask placed before the deny must be caught by the executed matrix.
    for c, rel in HOOK_WITH_TABLE.items():
        m = mutate_text(c, rel, 'if (!sub || GIT_READ_ONLY.has(sub)) return null;', 'return null;')
        d = run_hook(m, c, 'git commit -m x')[0] if m else 'n/a'
        ctx.check('mutation: a disabled Git classifier is caught (commit no longer asks)', d == 'allow', d, c, 'MUTATION', 'allow', d)
        if m:
            shutil.rmtree(m, ignore_errors=True)
        m = mutate_text(c, rel, "'status', 'diff', 'log',", "'diff', 'log',")
        d = run_hook(m, c, 'git status')[0] if m else 'n/a'
        ctx.check('mutation: status dropped from the read-only table is caught (status now asks)', d == 'ask', d, c, 'MUTATION', 'ask', d)
        if m:
            shutil.rmtree(m, ignore_errors=True)
    m = mutate_text('L1', '.claude/hooks/pre-shell-command.mjs', "const verdict = classify(command, frontendCli(config));", "const verdict = classify(command, frontendCli(config));\n  if (verdict.git.length) decide('ask', gitAskReason(verdict.git));")
    d = run_hook(m, 'L1', 'npm i left-pad@1.3.0 --force && git commit -m x')[0] if m else 'n/a'
    ctx.check('mutation: an L1 Git ask moved before the deny is caught (deny would become ask)', d == 'ask', d, 'L1', 'MUTATION', 'ask', d)
    if m:
        shutil.rmtree(m, ignore_errors=True)
    ctx.not_run('a live Claude Code host showing the ask prompt and applying the user answer', 'no live host; the hook output was read directly', None)
    ctx.not_run('a headless run meeting an ask (no user to answer)', 'host behavior; the headless pause rule is text (R02) and was not executed live', None)
    ctx.not_run('Git run indirectly by a script or program', 'not classified by any candidate; outside the hook design', None)
