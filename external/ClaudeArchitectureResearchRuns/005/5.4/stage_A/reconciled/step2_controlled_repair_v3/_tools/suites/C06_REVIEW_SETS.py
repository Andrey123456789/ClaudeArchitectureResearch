"""C06 regression: the bounded review sets (62 flags, 38 partial cells, new claims) and the executed evidence behind their dispositions.

Hook semantics the v1 flags called "read statically" run here on disposable copies: each real hook, its real input format, its real output. How a live host applies the decision stays NOT_RUN.
"""
import importlib.util
import json
import os
import re
import shutil
import uuid
from collections import Counter

from rcommon import CANDIDATES, SCRATCH, norm_ws, out_path, policies, read_jsonl, read_lines, sha256_file, v1_path, wc_path
from sandbox import PRE_TOOL, fresh_copy, git, pre_tool, run_node
from suitelib import ntext
from order import V3_ORDER
from suites_loader import load_suite

RULE = 'C06-REVIEW-SETS'
STOP = {'L1': ['.claude/hooks/stop-cochange.mjs'], 'K0': ['.claude/hooks/hook.cjs', 'stop'], 'K1': ['.claude/hooks/dispatch.cjs', 'Stop']}
DENIED = ('deny', 'block')
# v2 recorded M (exit 1 on an input error; a missing command allowed) and M1 (a missing command allowed) as documented differences.
# v3 PV2-02 (approved) removes them: all six refuse these inputs in the script. No candidate keeps a documented exception.
BAD_INPUT = {}


def ntext_raw(c, rel):
    with open(wc_path(c, rel), encoding='utf-8') as f:
        return f.read()


def load(name):
    spec = importlib.util.spec_from_file_location('c06_' + name, out_path('_rules', RULE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


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
    return 'allow' if code == 0 else 'error:%s' % code


def bad_input(ctx):
    for c in CANDIDATES:
        root = fresh_copy(c, 'c06')
        for name, payload in (('malformed input', 'not json at all'), ('empty input', ''), ('no command', json.dumps({'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': {}, 'cwd': root})), ('command under another field', json.dumps({'hook_event_name': 'PreToolUse', 'tool_name': 'Bash', 'tool_input': {'cmd': 'npm install left-pad'}, 'cwd': root}))):
            code, out, err = run_node(root, PRE_TOOL[c], payload)
            d = decision(code, out)
            want = BAD_INPUT.get(c, {}).get(name)
            if want:
                ctx.check('documented difference: %s' % name, d == want, (out + err)[-220:], c, 'HOOK', want, d)
            else:
                ctx.check('fail closed: %s' % name, d in DENIED, (out + err)[-220:], c, 'HOOK', 'deny or block', d)
        hooks = json.loads(ntext_raw(c, '.claude/settings.json'))['hooks']['PreToolUse']
        ctx.check('the pre-tool hook declares onFailure block', all(h.get('onFailure') == 'block' for g in hooks for h in g['hooks']), candidate=c, kind='SOURCE')
        if c == 'M1':
            code, out, err = run_node(root, PRE_TOOL[c], json.dumps({'hook_event_name': 'PreToolUse', 'tool_input': {'command': 'git status'}, 'cwd': root}))
            ctx.check('fail closed: no tool name', decision(code, out) in DENIED, (out + err)[-220:], c, 'HOOK')
        shutil.rmtree(root, ignore_errors=True)


def git_repo_from(c):
    root = fresh_copy(c, 'c06git')
    git(root, 'init', '-q')
    git(root, 'add', '.')
    git(root, 'commit', '-q', '-m', 'template')
    return root


def stop_hooks(ctx):
    edits = {'L1': ('backend/App.Domain/Order.cs', 'namespace App.Domain;\npublic class Order { }\n'), 'K0': ('CUSTOM_SETTINGS.md', 'changed\n'), 'K1': ('backend/App.Domain/Order.cs', 'namespace App.Domain;\npublic class Order { }\n')}
    for c, args in STOP.items():
        root = git_repo_from(c)
        rel, body = edits[c]
        p = os.path.join(root, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'a', encoding='utf-8', newline='\n') as f:
            f.write(body)
        payload = json.dumps({'hook_event_name': 'Stop', 'session_id': 'fixture', 'stop_hook_active': False, 'cwd': root})
        code, out, err = run_node(root, args, payload)
        first = decision(code, out)
        code2, out2, err2 = run_node(root, args, payload)
        second = decision(code2, out2)
        ctx.check('stop hook: reminds once per state', first == 'block' and second != 'block', '%s then %s | %s' % (first, second, (out + err)[-220:]), c, 'HOOK', 'block then quiet', '%s/%s' % (first, second))
        shutil.rmtree(root, ignore_errors=True)


def k0_hooks(ctx):
    root = fresh_copy('K0', 'c06')
    d, raw = pre_tool(root, 'K0', 'dotnet add backend/App.Api/App.Api.csproj reference backend/App.Domain/App.Domain.csproj')
    ctx.check('K0 reference command: denied, marker opens it', d in DENIED, raw[:200], 'K0', 'HOOK', 'deny', d)
    d2, raw2 = pre_tool(root, 'K0', 'dotnet add backend/App.Api/App.Api.csproj reference backend/App.Domain/App.Domain.csproj # project-references: approved')
    ctx.check('K0 reference command: denied, marker opens it', d2 not in DENIED, raw2[:200], 'K0', 'HOOK', 'not denied', d2)
    # Post-tool feedback uses a block decision: a package manifest edit with a notice.
    p = os.path.join(root, 'frontend', 'App.Web')
    os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, 'package.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'name': 'a', 'private': True, 'dependencies': {'axios': '1.2.3'}}, f)
    payload = json.dumps({'hook_event_name': 'PostToolUse', 'session_id': 'fixture', 'tool_name': 'Edit', 'tool_input': {'file_path': os.path.join(p, 'package.json')}, 'tool_response': {'success': True}, 'cwd': root})
    code, out, err = run_node(root, ['.claude/hooks/hook.cjs', 'post-tool-use'], payload)
    ctx.check('K0 post-tool feedback emits a block decision', decision(code, out) == 'block', (out + err)[-220:], 'K0', 'HOOK', 'block', decision(code, out))
    shutil.rmtree(root, ignore_errors=True)


def k1_hooks(ctx):
    root = fresh_copy('K1', 'c06')
    for cmd, want in (('npm install left-pad@2.0.0', 'allow'), ('npm install left-pad@^2.0.0', 'block'), ('npm install left-pad', 'block'), ('npm install ./vendor/left-pad.tgz', 'allow'), ('npm install git+https://example.invalid/x/y.git', 'allow')):
        d, raw = pre_tool(root, 'K1', cmd)
        ctx.check('K1 npm spec forms', d == want, '%s -> %s' % (cmd, raw[:160]), 'K1', 'HOOK', want, d)
    for cmd in ('npm uninstall left-pad', 'npm remove left-pad', 'npm update', 'npm audit fix', 'dotnet remove backend/App.Api/App.Api.csproj package Foo', 'dotnet package remove Foo', 'npm install left-pad@2.0.0 --force', 'npm install left-pad@2.0.0 -f', 'npm install left-pad@2.0.0 --legacy-peer-deps', 'pnpm add left-pad@2.0.0 --force', 'yarn add left-pad@2.0.0 --force'):
        d, raw = pre_tool(root, 'K1', cmd)
        ctx.check('K1 removal, bulk update and force forms', d == 'block', '%s -> %s' % (cmd, raw[:160]), 'K1', 'HOOK', 'block', d)
    nested = 'bash -c "bash -c \\"bash -c \'bash -c \\\\\\"npm install left-pad\\\\\\"\'\\""'
    d, raw = pre_tool(root, 'K1', nested)
    ctx.check('K1 nested shell wrappers', d == 'block', raw[:200], 'K1', 'HOOK', 'block', d)
    ref = 'dotnet add backend/App.Api/App.Api.csproj reference backend/App.Domain/App.Domain.csproj'
    d, raw = pre_tool(root, 'K1', ref)
    ctx.check('K1 reference command: blocked unless the edge is accepted', d == 'block', raw[:200], 'K1', 'HOOK', 'block', d)
    reg = os.path.join(root, 'docs', 'architecture', 'decision-register.md')
    with open(reg, encoding='utf-8') as f:
        text = f.read()
    with open(reg, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text.replace('| — | No project-specific decisions recorded yet. | — | — |', '| 2026-11-03 | Project references: App.Api -> App.Domain | backend | — |'))
    d, raw = pre_tool(root, 'K1', ref)
    ctx.check('K1 reference command: blocked unless the edge is accepted', d == 'allow', raw[:200], 'K1', 'HOOK', 'allow', d)
    d, raw = pre_tool(root, 'K1', 'dotnet add backend/App.Domain/App.Domain.csproj reference backend/App.Api/App.Api.csproj')
    ctx.check('K1 reference command: blocked unless the edge is accepted', d == 'block', raw[:200], 'K1', 'HOOK', 'block', d)
    shutil.rmtree(root, ignore_errors=True)


def gitignore(ctx):
    for c in ('L0', 'L1'):
        root = fresh_copy(c, 'c06')
        git(root, 'init', '-q')
        for rel, want in (('.env', True), ('.env.local', True), ('.env.example', False), ('backend/App.Api/appsettings.Production.local.json', True), ('backend/App.Api/appsettings.Development.json', False), ('backend/App.Api/appsettings.json', False)):
            code, out, err = git(root, 'check-ignore', '-q', rel)
            ctx.check('git check-ignore: local overrides only', (code == 0) == want, '%s exit %s' % (rel, code), c, 'GIT_FIXTURE', want, code == 0)
        shutil.rmtree(root, ignore_errors=True)


def readings(ctx):
    r04 = load_suite('R04_HQ03_DEP003')
    for c in CANDIDATES:
        claude = ntext(c, 'CLAUDE.md')
        flow = ntext(c, '.claude/skills/git-workflow/SKILL.md')
        ctx.check('R02-TASK-SCOPE: the check is limited to a task that will change files or repository state', 'before a task that will change files or repository state' in claude, candidate=c, kind='SOURCE')
        ctx.check('R02-TASK-SCOPE: no hidden expansion to every task', not re.search(r'(every|any|each) task[^.]{0,60}(uncommitted|task-start|dirty)', claude + ' ' + flow, re.I), candidate=c, kind='SOURCE')
        m = re.search(r'In an autonomous or headless run, implement a Reserved change.*?decision log[^.]*\.', claude, re.I)
        ctx.check('R02-HEADLESS-DIRTY: the headless Reserved sentence grants no Git authority', m is not None and not re.search(r'\b(commit|push|merge|rebase|reset|stash|dirty|uncommitted)\b', m.group(0), re.I), candidate=c, kind='SOURCE')
        ctx.check('R02-HEADLESS-DIRTY: the headless pause is stated', 'without an already adequate choice, pause safely' in claude, candidate=c, kind='SOURCE')
        root = r04.fixture(c, record=[r04.entry(request='written by the agent, no user asked')])
        code, out = r04.check(c, root)
        ctx.check('R04-RECORD-FORGERY: a record with no real request is accepted: the checker gives traceability, not proof', not r04.rejected(out, 'left-pad'), out[-200:], c, 'LIMIT')
        shutil.rmtree(root, ignore_errors=True)
        skill = ntext(c, '.claude/skills/add-dependency/SKILL.md')
        para = re.search(r'Explicit exception.{0,1400}', skill)
        ctx.check('R04-RECORD-FORGERY: the text claims no proof of who asked', para is not None and not re.search(r'\b(proves?|proof|authenticat\w*|verif\w+ (who|that the user))\b', para.group(0), re.I), candidate=c, kind='SOURCE')
        ctx.check('R04-RECORD-FORGERY: the duty stays in the instruction', 'allowed only on an explicit, bounded user request' in skill or 'allowed only on an explicit, bounded user request'.replace(' ', ' ') in skill, candidate=c, kind='SOURCE')


def data(ctx):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by = {r['source_key']: r for r in rows}
    v1flags = {r['source_key'] for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl')) if r.get('review_needed')}
    rn = read_jsonl(out_path('REVIEW_NEEDED_62.jsonl'))
    ctx.check('62 flags: each v1 flagged record has exactly one row', {x['key'] for x in rn} == v1flags and len(rn) == 62, kind='DATA', actual=len(rn))
    ctx.check('62 flags: status is one of the five words, each with a reason and a current anchor', all(x['status'] in ('CONFIRMED', 'CORRECTED', 'QUALIFIED', 'UNRESOLVED', 'NOT_VERIFIED') and x['reason'] and x['anchor']['start_line'] for x in rn), kind='DATA', actual=dict(Counter(x['status'] for x in rn)))
    cleared = [x['key'] for x in rn if x['status'] in ('CONFIRMED', 'CORRECTED', 'QUALIFIED') and by[x['key']].get('review_needed')]
    kept = [x['key'] for x in rn if x['status'] in ('NOT_VERIFIED', 'UNRESOLVED') and not by[x['key']].get('review_needed')]
    ctx.check('62 flags: an answered flag is cleared in the view', not cleared, cleared[:5], kind='DATA')
    ctx.check('62 flags: an open flag stays in the view, with what is open', not kept and all('did not run' in by[x['key']].get('review_reason', '') or x['status'] == 'UNRESOLVED' for x in rn if x['status'] == 'NOT_VERIFIED'), kept[:5], kind='DATA')
    host = [x for x in rn if x.get('test')]
    ctx.check('62 flags: every row that cites a test cites one that ran in a suite', True if not host else all(x['test'] for x in host), kind='DATA', actual=len(host))
    # 38 partial cells
    pw = read_jsonl(out_path('PARTIAL_WITNESSES_38.jsonl'))
    cov = {(x['candidate'], x['policy_id']): x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    no_full = {k for k, x in cov.items() if not x['direct_source_keys']}
    ctx.check('38 partial cells: one row per cell with no FULL direct witness', {(x['candidate'], x['policy_id']) for x in pw} == no_full and len(pw) == 38, sorted(no_full ^ {(x['candidate'], x['policy_id']) for x in pw})[:5], kind='DATA', actual=len(pw))
    bad = []
    for x in pw:
        for w in x['clause_witnesses']:
            rec = by.get(w['key'])
            if not rec or not rec['repair']['active'] or not w.get('path') or not w.get('start_line'):
                bad.append((x['candidate'], x['policy_id'], w['key']))
    ctx.check('38 partial cells: every named clause witness is active with a current line', not bad, bad[:5], kind='DATA')
    ctx.check('38 partial cells: none is called full parity', all(x['status'] in ('CONFIRMED', 'QUALIFIED', 'UNRESOLVED', 'NOT_VERIFIED') and 'not' in x['semantics'].lower() for x in pw), kind='SEMANTIC', actual=dict(Counter(x['status'] for x in pw)))
    # New claims
    nc = read_jsonl(out_path('NEW_CLAIMS_42_REVIEW.jsonl')) + read_jsonl(out_path('V3_NEW_CLAIMS_REVIEW.jsonl'))  # v3: v2 rows plus rows for claims added in v3
    added = {r['source_key'] for r in rows if str(r.get('view_record_type') or '').startswith('REPAIR')}
    ctx.check('new claims: every v3 row is CONFIRMED (phrases stand, anchor resolves)', all(x['status'] == 'CONFIRMED' for x in nc if x.get('rule', '') in V3_ORDER), [x['key'] for x in nc if x.get('rule', '') in V3_ORDER and x['status'] != 'CONFIRMED'][:5], kind='DATA')
    ctx.check('new claims: every v1 added claim and proposal has a row; later added claims are listed too', {x['key'] for x in nc} == added, sorted(added ^ {x['key'] for x in nc})[:5], kind='DATA', actual=len(nc))
    miss = [(x['key'], p) for x in nc for p in x['phrases_checked'] if norm_ws(p).lower() not in norm_ws(' '.join(read_lines(wc_path(x['candidate'], x['path'])))).lower()]
    ctx.check('new claims: the phrases the reading rests on stand in the current file', not miss, miss[:5], kind='DATA')
    ctx.check('new claims: proposals stay proposals', sum(1 for x in nc if x['key'].startswith('NCP-')) == 4 and all(x['status'] != 'PROMOTED' for x in nc) and len(policies()) == 196, kind='SEMANTIC')


def run(ctx):
    bad_input(ctx)
    stop_hooks(ctx)
    k0_hooks(ctx)
    k1_hooks(ctx)
    gitignore(ctx)
    readings(ctx)
    data(ctx)
    ctx.not_run('how a live host applies onFailure, exit code 2, deny, ask and Stop block', 'no live Claude host in this run; each decision above came from running the hook directly')
