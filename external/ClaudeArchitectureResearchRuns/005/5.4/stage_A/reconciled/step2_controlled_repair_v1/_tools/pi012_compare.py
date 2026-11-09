"""Blind comparison for R01. Logs the blind file hashes first, then compares each blind reading with the stored baseline and the audit suggestion."""
import glob
import json
import os
import sys
from collections import Counter

from pi012 import R, cand_of, obj_of, split_key
from rcommon import AUD, CANDIDATES, baseline, now, out_path, read_json, read_jsonl, sha256_file, utf8_stdout, write_json


def load_blind(pattern='blind/*.dec'):
    rows = {}
    for p in sorted(glob.glob(out_path(R, pattern))):
        for i, line in enumerate(open(p, encoding='utf-8'), 1):
            if not line.strip():
                continue
            parts = [x.strip() for x in line.rstrip('\n').split('|')]
            parts += [''] * (5 - len(parts))
            rows[parts[0]] = {'key': parts[0], 'modality': parts[1], 'confidence': parts[2], 'reading': parts[3], 'counterexample': parts[4], 'file': os.path.basename(p), 'line': i}
    return rows


def main():
    utf8_stdout()
    cases = read_json(out_path(R, 'CASES.json'))['cases']
    blind = load_blind()
    keys = {c['key'] for c in cases}
    print('blind', len(blind), 'cases', len(cases), 'missing', sorted(keys - set(blind))[:10], 'extra', sorted(set(blind) - keys)[:10])
    write_json(os.path.join(R, 'BLIND_HASHES.json'), {'at': now(), 'files': {os.path.basename(p): sha256_file(p) for p in glob.glob(out_path(R, 'blind/*.dec'))}})
    audit = {r['key']: r for r in read_jsonl(os.path.join(AUD, 'PI012_NEGATIVE_MODALITY_REVIEW.jsonl'))}
    agree_stored, agree_audit = Counter(), Counter()
    out = []
    for c in cases:
        k = c['key']
        rec, obj = obj_of(k)
        st = obj.get('modality')
        b = blind[k]['modality']
        a = audit.get(k, {}).get('modality_suggested')
        agree_stored[b == st] += 1
        if a:
            agree_audit[b == a] += 1
        if b != st or (a and a != b):
            out.append('#%d %s stored=%s(%s) blind=%s audit=%s %s | pol=%s | %s' % (c['n'], k, st, (obj.get('classification') or '')[:6], b, a, ','.join(sorted(set(c['lists']))), ','.join(obj.get('canonical_policy_ids') or []), blind[k]['reading'][:90]))
    print('agree stored', dict(agree_stored), 'agree audit', dict(agree_audit))
    print('\n'.join(out))


if __name__ == '__main__':
    main()
