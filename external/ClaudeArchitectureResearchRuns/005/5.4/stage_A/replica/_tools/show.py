#!/usr/bin/env python3
"""Print immutable snapshot files with line numbers (read-only viewer for Run 2).

Usage: py show.py <root> <candidate> <batch_id | relative_path> [more...]
"""
import json
import sys
from pathlib import Path


def main():
    root = Path(sys.argv[1]).resolve()
    cand = sys.argv[2]
    queue = json.loads((root / 'stage_A' / '_control' / f'{cand}_WORK_QUEUE.json').read_text(encoding='utf-8'))
    batches = {b['id']: b['files'] for b in queue['batches']}
    targets = []
    for t in sys.argv[3:]:
        if t in batches:
            targets.extend(batches[t])
        else:
            targets.append(t if t.startswith('output/') else 'output/template/' + t)
    for rel in targets:
        p = root / 'inputs' / cand / rel
        data = p.read_bytes()
        try:
            lines = data.decode('utf-8-sig').splitlines()
        except UnicodeDecodeError:
            print(f'=== {rel} (BINARY/NON-UTF8, {len(data)} bytes)')
            continue
        print(f'=== {rel} ({len(lines)} lines)')
        for i, line in enumerate(lines, 1):
            print(f'{i}|{line}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
