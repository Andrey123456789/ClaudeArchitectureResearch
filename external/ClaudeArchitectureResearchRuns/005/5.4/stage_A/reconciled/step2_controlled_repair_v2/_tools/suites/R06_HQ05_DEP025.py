"""R06 regression: HQ-05 / DEP-025. Executes each candidate's real PreToolUse hook. Confirmation, comment markers and exception records cannot open a peer-dependency bypass."""
import json
import os

from rcommon import CANDIDATES
from sandbox import fresh_copy, pre_tool
from suitelib import mutate_text, post

SKILL = '.claude/skills/add-dependency/SKILL.md'
DENIED = ('deny', 'block')
BYPASS = ['npm install x --force', 'npm install x --legacy-peer-deps', 'npm i x -f', 'npm install x --legacy-peer-deps=true', 'npm --prefix frontend i x --force', 'npm ci --legacy-peer-deps', 'npm update --force',
          'bash -c "npm install x --force"', 'pwsh -Command "npm install x --legacy-peer-deps"', 'cmd /c npm install x --force', 'cd frontend && npm install x --legacy-peer-deps', 'npm run build; npm install x --force',
          'npm_config_legacy_peer_deps=true npm install x', 'npm_config_force=true npm install x', 'npm config set legacy-peer-deps true', 'npm.cmd install x --force']
MARKERS = ['npm install x --force # peer-override: approved-by-user', 'npm install x --legacy-peer-deps # peer-override: approved-by-user', 'npm install x --force # add-dependency: checked', 'npm install x --force # add-dependency: reviewed',
           'npm install x --legacy-peer-deps # add-dependency: reviewed', 'npm install x --legacy-peer-deps # approved by user']
NOT_PEER = ['npm cache clean --force', 'npm run build', 'npm ci', 'git status']
SAFE = {'M': ['npm install x@1.2.3'], 'M1': ['npm install x@1.2.3 # add-dependency: checked'], 'L0': ['npm install x@1.2.3'], 'L1': ['npm install x@1.2.3', 'npm install x@1.2.3'], 'K0': ['npm install x@1.2.3 # add-dependency: reviewed'], 'K1': ['npm install x@1.2.3']}
TEXT_MUST = ['--force', '--legacy-peer-deps', 'resolve the actual compatibility problem', 'no confirmation, comment marker, or approval']
TEXT_NOT = {'M1': ['# peer-override: approved-by-user', 'peer-dependency override additionally needs'], 'L0': ['if the user explicitly decides to override, the user runs the command'], 'L1': ['confirm only if the user explicitly wants this']}
HOOK_FILE = {'M': '.claude/hooks/dependency-guard.mjs', 'M1': '.claude/scripts/lib/dependency-commands.js', 'L0': '.claude/hooks/claude-hook.mjs', 'L1': '.claude/hooks/pre-shell-command.mjs', 'K0': '.claude/hooks/hook.cjs', 'K1': '.claude/scripts/classify-command.cjs'}


def run(ctx):
    for c in CANDIDATES:
        root = fresh_copy(c, 'peer')
        for cmd in BYPASS:
            d, raw = pre_tool(root, c, cmd)
            ctx.check('peer bypass denied: %s' % cmd, d in DENIED, raw[:160], c, 'HOOK', 'deny or block', d)
        for cmd in MARKERS:
            d, raw = pre_tool(root, c, cmd)
            ctx.check('marker does not open it: %s' % cmd, d in DENIED, raw[:160], c, 'HOOK', 'deny or block', d)
        # Forms that routing alone could mask: pinned, with the candidate's workflow marker, second attempt counted.
        tail = {'M1': ' # add-dependency: checked', 'K0': ' # add-dependency: reviewed'}.get(c, '')
        for cmd in ('npm_config_legacy_peer_deps=true npm install x@1.2.3', 'npm_config_force=true npm install x@1.2.3', "$env:npm_config_force='true'; npm install x@1.2.3", 'env npm_config_legacy_peer_deps=true npm install x@1.2.3', 'npm install x@1.2.3 --force'):
            first = pre_tool(root, c, cmd + tail)[0]
            d, raw = pre_tool(root, c, cmd + tail)
            ctx.check('bypass not opened by the workflow marker or a retry: %s' % cmd, first in DENIED and d in DENIED, raw[:160], c, 'HOOK', 'deny or block', d)
        if c == 'M1':
            d, raw = pre_tool(root, c, 'npm install x@1.2.3 --force # add-dependency: checked # peer-override: approved-by-user')
            ctx.check('old override marker no longer opens it', d in DENIED, raw[:160], c, 'HOOK', 'deny or block', d)
        d, raw = pre_tool(root, c, 'npm install x --legacy-peer-deps', tool='PowerShell')
        ctx.check('PowerShell tool: denied', d in DENIED, raw[:160], c, 'HOOK', 'deny or block', d)
        for cmd in NOT_PEER:
            d, raw = pre_tool(root, c, cmd)
            ctx.check('unrelated command is not stopped as a peer bypass: %s' % cmd, d not in DENIED or 'peer' not in raw.lower(), raw[:200], c, 'HOOK')
        last = None
        for cmd in SAFE[c]:
            last = pre_tool(root, c, cmd)
        ctx.check('legitimate pinned install still goes through', last[0] == 'allow', last[1][:200], c, 'HOOK', 'allow', last[0])
        # The DEP-003 record never opens a peer bypass.
        with open(os.path.join(root, 'dependency-version-exceptions.json'), 'w', encoding='utf-8') as f:
            json.dump({'exceptions': [{'ecosystem': 'npm', 'package': 'x', 'version': '^1.0.0', 'manifest': 'frontend/App.Web/package.json', 'requested_by': 'user', 'request': 'user asked for x at ^1.0.0', 'date': '2026-11-03'}]}, f)
        d, raw = pre_tool(root, c, 'npm install x@^1.0.0 --force')
        ctx.check('DEP-003 exception record does not excuse --force', d in DENIED, raw[:160], c, 'HOOK', 'deny or block', d)
        post(ctx, c, 'add-dependency states no confirmation route', SKILL, TEXT_MUST, TEXT_NOT.get(c, ()))
        m = mutate_text(c, SKILL, 'No confirmation, comment marker, or', 'A confirmation or')
        ctx.check('mutation: approval route reinserted in text is caught', m is not None and not post(None, c, '', SKILL, TEXT_MUST, (), m), candidate=c, kind='MUTATION')
    # Disabled enforcement in a copy: the executed test must notice.
    MUT = {'M': ("(NPM_INSTALL_LIKE.has(npm.sub) && bypassFlag) || bypassConfig", "false"), 'M1': ("if (flag) {", "if (false) {"), 'L0': ("for (const item of found.filter(entry => entry.bypass)) {", "for (const item of []) {"),
           'L1': ("decide('deny', 'Peer-dependency bypass", "void ('Peer-dependency bypass"), 'K0': ("deny.push('The command uses --force, --legacy-peer-deps", "void ('The command uses --force, --legacy-peer-deps"), 'K1': ("if (options.some(o => PEER_BYPASS.test(o))) findings.push({ kind: 'peer-bypass', segment });", "")}
    for c, (old, new) in MUT.items():
        m = mutate_text(c, HOOK_FILE[c], old, new)
        cmd = 'npm install x@1.2.3 --force' + {'M1': ' # add-dependency: checked', 'K0': ' # add-dependency: reviewed'}.get(c, '')
        d = 'n/a'
        if m:
            pre_tool(m, c, cmd)  # L1 routes a dependency change once
            d = pre_tool(m, c, cmd)[0]
        ctx.check('mutation: disabled peer enforcement lets the bypass through, so the hook test would catch it', d == 'allow', d, c, 'MUTATION', 'allow', d)
    ctx.not_run('host enforcement of deny and exit code 2 in a live Claude session', 'hook decisions were executed directly; the host loop is not available in this run')
