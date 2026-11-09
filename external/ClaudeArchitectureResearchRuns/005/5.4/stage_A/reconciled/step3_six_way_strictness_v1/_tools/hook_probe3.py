"""Static PreToolUse probe (Step 3, PROBE-HOOK-03): dependency removal and bare update commands.

Same harness as PROBE-HOOK-01 (hook_probe.py) on disposable copies under _work/probe3/. Commands are
never executed; no Git, no network, no live Claude Code host. Static script decisions only.

Usage: python -B _tools/hook_probe3.py
Writes: HOOK_PROBE3_RESULTS.json and removes the copies.
"""
import datetime
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import CANDS, S3, write_json_atomic  # noqa: E402
from hook_probe import API, make_fixture, run  # noqa: E402

CASES = [
    ('R1 dotnet remove package', f'dotnet remove {API} package Serilog.AspNetCore'),
    ('R2 npm uninstall', 'npm uninstall left-pad'),
    ('R3 npm update (bare)', 'npm update'),
    ('R4 npm audit fix', 'npm audit fix'),
    ('R5 dotnet package update (bare)', f'dotnet package update --project {API}'),
    ('R6 control: dotnet restore', 'dotnet restore'),
]


def main():
    base = S3 / '_work' / 'probe3' / uuid.uuid4().hex[:8]
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
    write_json_atomic(S3 / 'HOOK_PROBE3_RESULTS.json', {
        'probe': 'PROBE-HOOK-03', 'at': datetime.datetime.now().isoformat(timespec='seconds'), 'node': node,
        'method': 'Same harness as PROBE-HOOK-01. Commands are never executed. Each command is run twice with the same hook state directory.',
        'semantics': 'Static script decision only; live host NOT_RUN.',
        'cases': [{'label': l, 'command': c} for l, c in CASES], 'results': results})


if __name__ == '__main__':
    main()
