"""PV2-02 regression: M and M1 shell PreToolUse guards block invalid hook input in the script (kit 74 Part B PV2-02).

Every case runs the real hook script directly on a disposable copy with its real input format. M blocks with exit 2; M1 returns a deny
decision. Valid read-only commands stay allowed. How a live host applies exit 2, deny or onFailure is NOT_RUN.
"""
import json
import os
import shutil

from rcommon import CANDIDATES, wc_path
from sandbox import PRE_TOOL, fresh_copy, run_node
from suitelib import has, mutate_text

RULE = 'PV2-02-FAILCLOSED-INPUT'
BLOCKED = ('block', 'deny')


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


def pre(tool='Bash', **kw):
    return dict({'hook_event_name': 'PreToolUse', 'session_id': 'fixture', 'tool_name': tool}, **kw)


# (name, payload) - payload is raw text or a dict (cwd is added).
INVALID = [
    ('malformed JSON', 'not json at all'), ('empty input', ''), ('whitespace only', '  \n '), ('byte-order mark only', '﻿'),
    ('JSON array', '[]'), ('JSON string', '"git status"'), ('JSON number', '42'), ('JSON null', 'null'),
    ('no hook_event_name', {'tool_name': 'Bash', 'tool_input': {'command': 'git status'}}),
    ('no tool_name', {'hook_event_name': 'PreToolUse', 'tool_input': {'command': 'git status'}}),
    ('tool_name not a string', pre(tool=7, tool_input={'command': 'git status'})),
    ('no tool_input', pre()), ('tool_input not an object', pre(tool_input='git status')), ('tool_input array', pre(tool_input=['git status'])),
    ('no command', pre(tool_input={})), ('blank command', pre(tool_input={'command': '   '})), ('empty command', pre(tool_input={'command': ''})),
    ('number command', pre(tool_input={'command': 42})), ('array command', pre(tool_input={'command': ['npm', 'i', 'x']})),
    ('command under another field', pre(tool_input={'cmd': 'npm install left-pad --force'})),
    ('PowerShell with no command', pre(tool='PowerShell', tool_input={})),
]
M1_ONLY_INVALID = [('PostToolUse event sent to the PreToolUse hook', {'hook_event_name': 'PostToolUse', 'tool_name': 'Bash', 'tool_input': {'command': 'git status'}})]
M_ONLY_INVALID = [('unknown event', {'hook_event_name': 'Notification', 'tool_name': 'Bash', 'tool_input': {'command': 'git status'}})]
VALID_ALLOWED = [
    ('git status', pre(tool_input={'command': 'git status'})), ('git diff', pre(tool_input={'command': 'git diff --stat'})), ('git log', pre(tool_input={'command': 'git log --oneline -5'})),
    ('ls', pre(tool_input={'command': 'ls -la'})), ('PowerShell Get-ChildItem', pre(tool='PowerShell', tool_input={'command': 'Get-ChildItem'})),
    ('npm ci without bypass', pre(tool_input={'command': 'npm ci'})), ('byte-order mark before valid JSON', '﻿' + json.dumps(pre(tool_input={'command': 'git status'}))),
    ('non-shell tool (nothing to gate)', pre(tool='Edit', tool_input={'file_path': 'x.cs'})),
]
STILL_BLOCKED = [('npm force install', pre(tool_input={'command': 'npm install left-pad@1.3.0 --force'})), ('npm legacy-peer-deps', pre(tool='PowerShell', tool_input={'command': 'npm i left-pad --legacy-peer-deps'}))]
# The categories the approved decision names, checked on all six for the parity row.
APPROVED_CATEGORIES = ['malformed JSON', 'empty input', 'JSON array', 'JSON null', 'no tool_input', 'no command', 'number command', 'command under another field']


def run_case(root, c, payload):
    text = payload if isinstance(payload, str) else json.dumps(dict(payload, cwd=root))
    code, out, err = run_node(root, PRE_TOOL[c], text)
    return decision(code, out), code, (out + err)[-240:]


def matrix(ctx, c, root, label=''):
    cases = INVALID + (M1_ONLY_INVALID if c == 'M1' else M_ONLY_INVALID)
    for name, p in cases:
        d, code, tail = run_case(root, c, p)
        want_code = 2 if c == 'M' else 0
        ok = d in BLOCKED and code == want_code
        ctx.check('%sinvalid input blocked in the script: %s' % (label, name), ok, tail, c, 'HOOK', 'block' if c == 'M' else 'deny', '%s/exit %s' % (d, code))
    for name, p in VALID_ALLOWED:
        d, code, tail = run_case(root, c, p)
        ctx.check('%svalid input still allowed: %s' % (label, name), d == 'allow' and code == 0, tail, c, 'HOOK', 'allow', d)
    for name, p in STILL_BLOCKED:
        d, code, tail = run_case(root, c, p)
        ctx.check('%sdependency guard unchanged: %s' % (label, name), d in BLOCKED, tail, c, 'HOOK', 'block or deny', d)


def run(ctx):
    for c in ('M', 'M1'):
        root = fresh_copy(c, 'pv202')
        matrix(ctx, c, root)
        if c == 'M':
            # The PostToolUse branches of the same script need no command, and still parse their input.
            d, code, tail = run_case(root, 'M', {'hook_event_name': 'PostToolUse', 'tool_name': 'Bash', 'tool_input': {}})
            ctx.check('M PostToolUse with no command is not required to have one', d == 'allow' and code == 0, tail, 'M', 'HOOK', 'allow', d)
            d, code, tail = run_case(root, 'M', 'not json')
            ctx.check('M malformed input exits 2 for any event (documented: the event is unknown before parsing)', code == 2, tail, 'M', 'HOOK', 'exit 2', code)
            for hook in ('.claude/hooks/file-change.mjs', '.claude/hooks/stop-co-change.mjs'):
                code, out, err = run_node(root, [hook], 'not json')
                ctx.check('M advisory hook keeps exit 1 on bad input: %s' % hook.split('/')[-1], code == 1, (out + err)[-160:], 'M', 'HOOK', 1, code)
        shutil.rmtree(root, ignore_errors=True)
    # Six-candidate parity on the categories the decision names.
    parity = {}
    for c in CANDIDATES:
        root = fresh_copy(c, 'pv202p')
        row = {}
        for name, p in INVALID:
            if name in APPROVED_CATEGORIES:
                row[name] = run_case(root, c, p)[0]
        parity[c] = row
        ctx.check('parity: the approved invalid-input categories are refused in the script', all(v in BLOCKED for v in row.values()), json.dumps(row), c, 'HOOK', 'block or deny for all', row)
        d = run_case(root, c, pre(tool_input={'command': 'git status'}))[0]
        ctx.check('parity: a valid read-only command is allowed', d == 'allow', d, c, 'HOOK', 'allow', d)
        shutil.rmtree(root, ignore_errors=True)
    # Source anchors for the documented contract.
    ctx.check('M template-maintenance states that the guard itself blocks unreadable input', has('M', '.claude/skills/template-maintenance/SKILL.md', 'the guard itself blocks (exit 2) shell hook input it cannot read or classify'), candidate='M', kind='SOURCE')
    ctx.check('M MAP names script-level blocking', has('M', '.claude/MAP.md', 'the guard itself blocks hook input it cannot read or classify'), candidate='M', kind='SOURCE')
    ctx.check('M settings keep onFailure block on the PreToolUse guard (backstop)', all(h.get('onFailure') == 'block' for g in json.load(open(wc_path('M', '.claude/settings.json'), encoding='utf-8'))['hooks']['PreToolUse'] for h in g['hooks']), candidate='M', kind='SOURCE')
    ctx.check('M1 settings keep onFailure block on the PreToolUse hook (backstop)', all(h.get('onFailure') == 'block' for g in json.load(open(wc_path('M1', '.claude/settings.json'), encoding='utf-8'))['hooks']['PreToolUse'] for h in g['hooks']), candidate='M1', kind='SOURCE')
    # Mutations: each removed check must be caught by the executed matrix.
    muts = [
        ('M', '.claude/hooks/dependency-guard.mjs', "if (typeof toolInput.command !== 'string' || toolInput.command.trim() === '') invalidInput(", "if (false) invalidInput(", 'no command'),
        ('M', '.claude/hooks/dependency-guard.mjs', 'const input = readInput(invalidInput);', 'const input = readInput();', 'malformed JSON'),
        ('M', '.claude/hooks/dependency-guard.mjs', "if (input === null || typeof input !== 'object' || Array.isArray(input)) invalidInput(", "if (false) invalidInput(", 'JSON null'),
        ('M1', '.claude/hooks/pre-tool-use.js', "if (typeof toolInput.command !== 'string' || toolInput.command.trim() === '') throw new Error(", "if (false) throw new Error(", 'no command'),
        ('M1', '.claude/hooks/pre-tool-use.js', "if (input.hook_event_name !== 'PreToolUse') throw new Error(", "if (false) throw new Error(", 'PostToolUse event sent to the PreToolUse hook'),
    ]
    for c, rel, old, new, case in muts:
        root = mutate_text(c, rel, old, new)
        if root is None:
            ctx.check('mutation target present: %s' % old[:50], False, rel, c, 'MUTATION')
            continue
        p = dict(INVALID + M1_ONLY_INVALID + M_ONLY_INVALID)[case]
        d = run_case(root, c, p)[0]
        ctx.check('mutation: removing the check lets "%s" through, and the matrix catches it' % case, d not in BLOCKED, d, c, 'MUTATION', 'allow or error', d)
        shutil.rmtree(root, ignore_errors=True)
    ctx.not_run('a live Claude Code host applying exit 2 and deny to an invalid shell PreToolUse payload', 'no live host; the scripts ran directly', 'M')
    ctx.not_run('a live Claude Code host applying onFailure: block when the guard crashes or times out', 'no live host; onFailure stays the backstop and is declared in settings.json', 'M1')
