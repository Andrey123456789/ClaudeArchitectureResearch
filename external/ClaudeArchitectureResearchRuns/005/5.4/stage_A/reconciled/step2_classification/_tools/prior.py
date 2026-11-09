"""Reviewer aid: for each record of a batch, show how already-finished candidates classified near-identical text.

  python -B prior.py <C> B### [--min 0.72]

Consistency hint only. It writes nothing, and every decision still comes from reading the source in view.py.
Only finished candidates that come earlier in the run order are consulted.
"""
import json
import os
import re
import sys
from collections import defaultdict

from common import OUT, union_view, source_key, record_claim_text

ORDER = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
CODE = {'CANONICAL_ONLY': 'CO', 'CANONICAL_PLUS_DELTA': 'CD', 'EXTRA_PRODUCT': 'XP', 'EXTRA_WORKFLOW': 'XW',
        'INTERNAL_ARCHITECTURE': 'IA', 'NON_NORMATIVE': 'NN', 'MIXED': 'MX', 'UNCERTAIN': 'UN'}
STOP = set('a an and are as at be by for from in is it not of on or the to when with this that do does than'.split())


def tokens(t):
    return {w for w in re.findall(r'[a-z0-9_.+#/-]+', (t or '').lower()) if w not in STOP and len(w) > 1}


def load(c):
    p = os.path.join(OUT, 'per_candidate', c, 'CLASSIFICATIONS.jsonl')
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding='utf-8')]


def fmt(r):
    pols = ' '.join(x['policy_id'] + ('' if x['coverage'] == 'FULL' else '~') for x in r.get('canonical_coverage') or [])
    bits = [CODE.get(r['classification'], r['classification']), pols, 'm=' + str(r.get('modality'))]
    st = r.get('strength_vs_canonical')
    if st in ('WEAKER', 'STRONGER', 'INCOMPARABLE'):
        bits.append('st=' + st[0])
    res = r.get('strength_resolution')
    if res:
        bits.append('sr=' + res['code'])
    d = r.get('domain')
    if d == 'WORKFLOW_ENFORCEMENT':
        bits.append('d=WF')
    return ' '.join(b for b in bits if b)


def main():
    cand, batch = sys.argv[1], sys.argv[2]
    thr = float(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 0.72
    idx = defaultdict(list)
    rows = []
    for c in ORDER[:ORDER.index(cand)]:
        for r in load(c):
            t = tokens((r.get('claim_text') or '') + ' ' + (r.get('primary_quote') or ''))
            rows.append((c, r, t))
            for w in t:
                idx[w].append(len(rows) - 1)
    plan = json.load(open(os.path.join(OUT, '_batches', cand + '.json'), encoding='utf-8'))
    b = next(x for x in plan['batches'] if x['batch_id'] == batch)
    view = {source_key(v): v for v in union_view() if v['candidate'] == cand}
    for n, item in enumerate(b['records'], 1):
        key = item if isinstance(item, str) else (item.get('source_key') or item.get('key'))
        rec = view[key]
        q = tokens(record_claim_text(rec))
        hits = defaultdict(int)
        for w in q:
            ids = idx.get(w, [])
            if len(ids) < 400:
                for i in ids:
                    hits[i] += 1
        best = []
        for i, h in sorted(hits.items(), key=lambda kv: -kv[1])[:60]:
            c, r, t = rows[i]
            claim = tokens(r.get('claim_text') or '')
            union = len(q | claim) or 1
            sim = len(q & claim) / union
            if sim >= thr:
                best.append((sim, c, r))
        best.sort(key=lambda x: -x[0])
        seen, out = set(), []
        for sim, c, r in best:
            f = fmt(r)
            if (c, f) in seen:
                continue
            seen.add((c, f))
            out.append('%s %.2f %s' % (c, sim, f))
            if len(out) == 3:
                break
        print('[%d] %s %s' % (n, key, ' || '.join(out) if out else '-'))


if __name__ == '__main__':
    main()
