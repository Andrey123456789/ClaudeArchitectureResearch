"""Static PreToolUse probe (Step 3, PROBE-HOOK-01).

Runs each candidate's registered PreToolUse hook script directly with a JSON payload, on a
disposable copy of the v3 template under _work/probe/, exactly as v3's sandbox did. No Git
command, no network, no package restore, no live Claude Code host: this is static evidence of
what the script returns, not of how a host applies it.

Usage: python -B _tools/hook_probe.py
Writes: HOOK_PROBE_RESULTS.json (raw decisions and output excerpts) and removes the copies.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import CANDS, S3, V3, write_json_atomic  # noqa: E402

PRE_TOOL = {'M': ['.claude/hooks/dependency-guard.mjs'], 'M1': ['.claude/hooks/pre-tool-use.js'],
            'L0': ['.claude/hooks/claude-hook.mjs', 'pre-bash'], 'L1': ['.claude/hooks/pre-shell-command.mjs'],
            'K0': ['.claude/hooks/hook.cjs', 'pre-tool-use'], 'K1': ['.claude/hooks/dispatch.cjs', 'PreToolUse']}
API = 'backend/Shop.Api/Shop.Api.csproj'
APP = 'backend/Shop.Application/Shop.Application.csproj'
DOM = 'backend/Shop.Domain/Shop.Domain.csproj'
INF = 'backend/Shop.Infrastructure/Shop.Infrastructure.csproj'
CASES = [
    ('P1 npm pinned install', 'npm install left-pad@1.3.0'),
    ('P2 dotnet add package, no version', f'dotnet add {API} package Serilog.AspNetCore'),
    ('P3 dotnet add package, pinned', f'dotnet add {API} package Serilog.AspNetCore --version 8.0.3'),
    ('P4 pinned with both review markers', f'dotnet add {API} package Serilog.AspNetCore --version 8.0.3 # add-dependency: checked # add-dependency: reviewed'),
    ('P5 inward project reference', f'dotnet add {APP} reference {DOM}'),
    ('P6 outward project reference', f'dotnet add {APP} reference {INF}'),
    ('P7 MediatR pinned', f'dotnet add {APP} package MediatR --version 12.4.1'),
    ('P8 AutoMapper pinned', f'dotnet add {API} package AutoMapper --version 13.0.1'),
]
CSPROJ = '<Project Sdk="Microsoft.NET.Sdk">\n  <PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup>\n{refs}</Project>\n'


def make_fixture(c, root):
    shutil.copytree(V3 / 'candidates' / c / 'template', root)
    for rel, refs in ((DOM, []), (APP, [DOM]), (INF, [APP, DOM]), (API, [APP, INF])):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        items = ''.join(f'  <ItemGroup><ProjectReference Include="..\\..\\{r.replace("/", chr(92))}" /></ItemGroup>\n' for r in refs)
        p.write_text(CSPROJ.format(refs=items), encoding='utf-8')
    (root / 'frontend').mkdir(exist_ok=True)


def run(c, root, state, command):
    env = dict(os.environ)
    tmp = root.parent / 'tmp'
    tmp.mkdir(exist_ok=True)
    env.update({'TEMP': str(tmp), 'TMP': str(tmp), 'TMPDIR': str(tmp), 'CLAUDE_PROJECT_DIR': str(root),
                'CLAUDE_HOOK_STATE_DIR': str(state), 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_TERMINAL_PROMPT': '0', 'NO_COLOR': '1'})
    env.pop('npm_config_force', None)
    env.pop('npm_config_legacy_peer_deps', None)
    payload = json.dumps({'hook_event_name': 'PreToolUse', 'session_id': 'probe', 'tool_name': 'Bash',
                          'tool_input': {'command': command}, 'cwd': str(root)})
    r = subprocess.run(['node'] + PRE_TOOL[c], cwd=root, input=payload, capture_output=True, text=True,
                       encoding='utf-8', errors='replace', env=env, timeout=120)
    decision = 'allow'
    if r.returncode == 2:
        decision = 'block'
    elif r.returncode != 0:
        decision = f'error:{r.returncode}'
    elif r.stdout.strip():
        try:
            o = json.loads(r.stdout.strip().splitlines()[-1])
            d = (o.get('hookSpecificOutput') or {}).get('permissionDecision')
            if d:
                decision = d
            elif o.get('decision') == 'block':
                decision = 'block'
        except ValueError:
            pass
    return {'decision': decision, 'exit': r.returncode, 'output': (r.stdout + r.stderr).strip()[:600]}


def main():
    base = S3 / '_work' / 'probe' / uuid.uuid4().hex[:8]
    results = {}
    try:
        for c in CANDS:
            root = base / c / 'repo'
            make_fixture(c, root)
            state = base / c / 'state'
            state.mkdir(parents=True, exist_ok=True)
            results[c] = {}
            for label, cmd in CASES:
                first = run(c, root, state, cmd)
                second = run(c, root, state, cmd)
                results[c][label] = {'command': cmd, 'first': first, 'second': second}
                print(c, label, first['decision'], second['decision'])
    finally:
        shutil.rmtree(base, ignore_errors=True)
    node = subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip()
    write_json_atomic(S3 / 'HOOK_PROBE_RESULTS.json', {
        'probe': 'PROBE-HOOK-01', 'at': datetime.datetime.now().isoformat(timespec='seconds'), 'node': node,
        'method': 'Direct run of each registered PreToolUse script with a JSON payload on a disposable copy of the v3 template plus four minimal project files (Shop.Domain/Application/Infrastructure/Api). No Git repository, no network, no live host. Each command is run twice with the same hook state directory.',
        'semantics': 'Static script decision only. How a live Claude Code host shows or applies allow/ask/deny/exit 2 is NOT_RUN.',
        'cases': [{'label': l, 'command': c} for l, c in CASES], 'results': results})


if __name__ == '__main__':
    main()
