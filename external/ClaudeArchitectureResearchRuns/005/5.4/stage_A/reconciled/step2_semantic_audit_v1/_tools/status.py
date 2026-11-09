"""Write a restartable checkpoint and STATUS.json after each phase.

  python -B _tools/status.py PHASE "note"
  python -B _tools/status.py show
"""
import glob
import json
import os
import sys
import time
from collections import Counter

from acommon import DEC, OUT, S2, out_path, read_jsonl, sha256_file, utf8_stdout, write_json
from dsl import load_blind, load_decisions


def snapshot():
    blind, dec = load_blind(), load_decisions()
    targets = read_jsonl(out_path('AUDIT_TARGETS.jsonl')) if os.path.exists(out_path('AUDIT_TARGETS.jsonl')) else []
    cases = {t['case_id']: t for t in targets}
    decided = set()
    for k in dec:
        decided.add(k)
    open_by_list = Counter()
    done_by_list = Counter()
    for t in targets:
        key = t['key']
        ok = key in decided or t['case_id'] in decided
        for m in t['memberships']:
            (done_by_list if ok else open_by_list)[m] += 1
    return {'n_blind': len(blind), 'n_decisions': len(dec), 'decisions': dict(Counter(x['decision'] for x in dec.values())),
            'done_by_list': dict(done_by_list), 'open_by_list': dict(open_by_list),
            'decision_file_hashes': {os.path.basename(p): sha256_file(p) for p in sorted(glob.glob(os.path.join(DEC, '*.dec')) + glob.glob(os.path.join(DEC, '*.blind')))},
            'step2_VALIDATION_RESULT_sha256': sha256_file(os.path.join(S2, 'VALIDATION_RESULT.json'))}


def main():
    utf8_stdout()
    if sys.argv[1] == 'show':
        s = snapshot()
        print(json.dumps({k: s[k] for k in ('n_blind', 'n_decisions', 'decisions', 'done_by_list', 'open_by_list')}, indent=0))
        return
    phase, note = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ''
    s = snapshot()
    s.update({'phase': phase, 'note': note, 'at': time.strftime('%Y-%m-%dT%H:%M:%S')})
    write_json(os.path.join('CHECKPOINTS', phase + '.checkpoint.json'), s)
    write_json('STATUS.json', {'phase': phase, 'note': note, 'at': s['at'], 'n_blind': s['n_blind'], 'n_decisions': s['n_decisions'], 'decisions': s['decisions'],
                               'done_by_list': s['done_by_list'], 'open_by_list': s['open_by_list'],
                               'resume': 'Trust _decisions/*.blind and *.dec plus CHECKPOINTS/, not chat. Run _tools/status.py show for what is open; each batch: view.py batch, blind, write .blind, reveal, write .dec.',
                               'stop_rule': 'Stop before Step 3.'})
    print('checkpoint', phase, s['n_decisions'], s['decisions'])


if __name__ == '__main__':
    main()
