"""Refresh STATE.json progress from the per-policy checkpoints (P1 bookkeeping).

Usage: python -B _tools/state_sync.py [--probe "TEXT"]
Recomputes policies_done, batches_done, next_batch, the resume point and root_causes_so_far
from CHECKPOINTS/policies/ and BATCH_PLAN.json. Never touches the checkpoints themselves.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s3common import S3, write_json_atomic  # noqa: E402


def main():
    state = json.loads((S3 / 'STATE.json').read_text(encoding='utf-8'))
    plan = json.loads((S3 / 'BATCH_PLAN.json').read_text(encoding='utf-8'))
    done = {p.stem for p in (S3 / 'CHECKPOINTS' / 'policies').glob('*.json')}
    roots = set(state.get('root_causes_so_far', []))
    for p in (S3 / 'CHECKPOINTS' / 'policies').glob('*.json'):
        cp = json.loads(p.read_text(encoding='utf-8'))
        for d in (cp.get('judgment') or cp).get('diffs') or []:
            if d.get('root'):
                roots.add(d['root'])
    batches = plan['batches'] if isinstance(plan, dict) else plan
    finished, nxt = [], None
    for b in batches:
        ids = b['policies']
        if all(i in done for i in ids):
            finished.append(b['batch'])
        elif nxt is None:
            nxt = b['batch']
    state['progress'] = {'policies_done': len(done), 'batches_done': finished, 'next_batch': nxt}
    state['root_causes_so_far'] = sorted(roots)
    if nxt:
        state['resume_point'] = (f'P1: next batch {nxt} (python -B _tools/judge.py status). Read _dossiers/{nxt}.md, '
                                 f'write _judgments/{nxt}.py, then python -B _tools/judge.py check {nxt}.')
    if '--probe' in sys.argv:
        text = sys.argv[sys.argv.index('--probe') + 1]
        if text not in state.setdefault('probes', []):
            state['probes'].append(text)
    write_json_atomic(S3 / 'STATE.json', state)
    print(state['progress'], len(state['root_causes_so_far']), 'roots')


if __name__ == '__main__':
    main()
