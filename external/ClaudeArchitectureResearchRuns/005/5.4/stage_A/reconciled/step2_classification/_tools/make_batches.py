"""Freeze the per-candidate batch plan (ordering by primary source location).

  python -B make_batches.py        -> writes ../_batches/<C>.json for all candidates (never overwrites)

Order: by primary anchor path, then start line, then key. A facet overlay follows its target group;
a provisional new clause is placed at its own evidence location. A batch closes at 60 records, or at a
file boundary once it holds >= 40 records.
"""
import os
import sys

from common import (OUT, CANDIDATES, union_view, source_key, record_anchor, facets, write_json_atomic,
                    sha256_text)
import json

MAX, SOFT = 60, 40


def plan(cand):
    recs = [r for r in union_view() if r['candidate'] == cand]
    anchors = {}
    for r in recs:
        if r['view_record_type'] != 'PROVISIONAL_FACET_OVERLAY':
            p, s, e = record_anchor(r)
            anchors[source_key(r)] = (p, s, 0, source_key(r))
    for r in recs:
        if r['view_record_type'] == 'PROVISIONAL_FACET_OVERLAY':
            tgt = r['target_group_id']
            p, s, _, k = anchors[tgt]
            anchors[source_key(r)] = (p, s, 1, k + '|' + source_key(r))
    order = sorted(recs, key=lambda r: anchors[source_key(r)])
    batches, cur, cur_path = [], [], None
    for r in order:
        p = anchors[source_key(r)][0]
        if cur and (len(cur) >= MAX or (p != cur_path and len(cur) >= SOFT)):
            batches.append(cur); cur = []
        cur.append({'source_key': source_key(r), 'view_record_type': r['view_record_type'],
                    'anchor_path': p, 'anchor_start_line': anchors[source_key(r)][1]})
        cur_path = p
    if cur:
        batches.append(cur)
    out = []
    for i, b in enumerate(batches, 1):
        out.append({'batch_id': 'B%03d' % i, 'n': len(b), 'records': b})
    return out


def main():
    for c in CANDIDATES:
        target = os.path.join(OUT, '_batches', c + '.json')
        if os.path.exists(target):
            print(c, 'exists, kept'); continue
        b = plan(c)
        body = {'candidate': c, 'protocol_version': 'step2-v1', 'n_records': sum(x['n'] for x in b),
                'n_batches': len(b), 'batches': b}
        body['plan_sha256'] = sha256_text(json.dumps(b, sort_keys=True))
        write_json_atomic(target, body)
        print(c, body['n_records'], 'records', len(b), 'batches')


if __name__ == '__main__':
    main()
