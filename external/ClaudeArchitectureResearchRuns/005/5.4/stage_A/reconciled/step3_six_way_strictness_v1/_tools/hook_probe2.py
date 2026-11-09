"""Static PreToolUse probe (Step 3, PROBE-HOOK-02): npm peer-dependency bypass variants (DEP-025).

Same harness as PROBE-HOOK-01 (hook_probe.py): each candidate's registered PreToolUse script is run
directly with a JSON payload on a disposable copy of the v3 template under _work/probe2/. No Git,
no network, no npm execution, no live Claude Code host. Static script decisions only.

Usage: python -B _tools/hook_probe2.py
Writes: HOOK_PROBE2_RESULTS.json and removes the copies.
"""
import datetime
import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import CANDS, S3, write_json_atomic  # noqa: E402
from hook_probe import make_fixture, run  # noqa: E402

PKG = '@angular/material@20.0.0'
CASES = [
    ('Q1 --legacy-peer-deps', f'npm install {PKG} --legacy-peer-deps'),
    ('Q2 --force', f'npm install {PKG} --force'),
    ('Q3 npm i -f (no package)', 'npm i -f'),
    ('Q4 env npm_config_legacy_peer_deps=true', f'npm_config_legacy_peer_deps=true npm install {PKG}'),
    ('Q5 npm ci --legacy-peer-deps', 'npm ci --legacy-peer-deps'),
    ('Q6 --legacy-peer-deps=true', f'npm install {PKG} --legacy-peer-deps=true'),
    ('Q7 npm config set legacy-peer-deps true', 'npm config set legacy-peer-deps true'),
    ('Q8 control: pinned install, no bypass', f'npm install {PKG}'),
    ('Q9 --legacy-peer-deps with both dependency markers', f'npm install {PKG} --legacy-peer-deps # add-dependency: checked # add-dependency: reviewed'),
    ('Q10 --force with both dependency markers', f'npm install {PKG} --force # add-dependency: checked # add-dependency: reviewed'),
]


def main():
    base = S3 / '_work' / 'probe2' / uuid.uuid4().hex[:8]
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
    write_json_atomic(S3 / 'HOOK_PROBE2_RESULTS.json', {
        'probe': 'PROBE-HOOK-02', 'at': datetime.datetime.now().isoformat(timespec='seconds'), 'node': node,
        'method': 'Same harness as PROBE-HOOK-01 (direct run of each registered PreToolUse script with a JSON payload on a disposable copy of the v3 template plus four minimal project files). Commands are never executed. Each command is run twice with the same hook state directory.',
        'semantics': 'Static script decision only. How a live Claude Code host shows or applies allow/ask/deny/exit 2 is NOT_RUN. Persistent bypass through an edited .npmrc is a file edit, not a shell command, and is not covered by this probe (source-read only).',
        'cases': [{'label': l, 'command': c} for l, c in CASES], 'results': results})


if __name__ == '__main__':
    main()
