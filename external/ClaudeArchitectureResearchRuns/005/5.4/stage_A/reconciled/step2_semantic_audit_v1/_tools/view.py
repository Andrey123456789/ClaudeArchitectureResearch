"""Reviewer views with an enforced reading order.

  python -B _tools/view.py batch NAME KEY [KEY ...]   define a review batch (refuses to change an existing one)
  python -B _tools/view.py blind NAME [--ctx N]       source, claim, loading context; no stored Step 2 classification fields
  python -B _tools/view.py reveal NAME                stored fields; refuses unless every key has a line in _decisions/NAME.blind,
                                                      and logs that file's SHA-256 to CHECKPOINTS/BLIND_LOG.jsonl first
  python -B _tools/view.py pol ID [ID ...]            canonical policy text
  python -B _tools/view.py src PATH A B               immutable source lines (PATH relative to repo root)
  python -B _tools/view.py cov C POLICY [...]         stored coverage row and witnesses
"""
import json
import os
import re
import sys
import time

from acommon import (CANDIDATES, DEC, ROOT, S2, all_baseline, baseline, cand_of, coverage, file_lines_abs, out_path, policies, sha256_file,
                     utf8_stdout, write_json)


def batch_path(name):
    return os.path.join(DEC, name + '.batch.json')


def load_batch(name):
    return json.load(open(batch_path(name), encoding='utf-8'))['keys']


def show_range(rel, a, b, ctx):
    ls = file_lines_abs(rel)
    lo = max(1, a - ctx)
    hi = min(len(ls), b + ctx)
    for i in range(lo, hi + 1):
        mark = '>' if a <= i <= b else ' '
        print('  %s%4d| %s' % (mark, i, ls[i - 1][:900]))


def merged_refs(r):
    seen, out = set(), []
    for e in r['evidence_refs']:
        k = (e['path'], e['start_line'], e['end_line'])
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


MAXR = int(os.environ.get('AUDIT_MAX_RANGES', '6'))


def rec_of(b, key):
    base, _, sub = key.partition('/')
    r = b[base]
    s = next((x for x in r.get('subclauses') or [] if x.get('subclause_id') == sub), None) if sub else None
    return r, s


def blind(name, ctx):
    b = all_baseline()
    for k in load_batch(name):
        r, sc = rec_of(b, k)
        print('\n### %s [%s] %s | %s' % (k, r['candidate'], r['view_record_type'], r.get('loading_context') or ''))
        print('CLAIM:', r['claim_text'])
        if sc:
            print('SUBCLAUSE %s: %s' % (sc['subclause_id'], sc.get('text')))
        refs = merged_refs(r)
        for (p, s, e) in refs[:MAXR]:
            print(' EV %s:%d-%d' % (re.sub(r'^inputs/[A-Z0-9]+/output/template/', '', p), s, e))
            show_range(p, s, e, ctx)
        if len(refs) > MAXR:
            print(' ... %d more ranges (use src)' % (len(refs) - MAXR))


def short_cov(r):
    return ','.join(c['policy_id'] + ('~' if c['coverage'] == 'PARTIAL' else '') for c in r.get('canonical_coverage') or []) or '-'


def reveal(name):
    keys = load_batch(name)
    p = os.path.join(DEC, name + '.blind')
    if not os.path.exists(p):
        raise SystemExit('no blind file for %s: read the source first' % name)
    have = set()
    for raw in open(p, encoding='utf-8'):
        if raw.strip() and not raw.startswith('#'):
            have.add(raw.split('||')[0].strip())
    missing = [k for k in keys if k not in have]
    if missing:
        raise SystemExit('blind reading missing for: %s' % missing)
    log = out_path('CHECKPOINTS', 'BLIND_LOG.jsonl')
    with open(log, 'a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps({'batch': name, 'blind_sha256': sha256_file(p), 'n_keys': len(keys), 'revealed_at': time.strftime('%Y-%m-%dT%H:%M:%S')}) + '\n')
    b = all_baseline()
    for k in keys:
        r, sc = rec_of(b, k)
        if sc:
            print('\n## %s SUBCLAUSE of a %s record: %s pol=%s mod=%s st=%s eq=%s res=%s conf=%s' % (
                k, r['classification'], sc.get('classification'), short_cov(sc), sc.get('modality'), sc.get('strength_vs_canonical'),
                sc.get('normative_strength_equivalence'), sc.get('strength_resolution_code'), r['confidence']))
            print(' trig=%s | exc=%s | extra=%s | scen=%s' % ((sc.get('trigger') or '')[:170], (sc.get('exceptions') or '')[:170], (sc.get('extra_fragment') or '')[:200], (sc.get('distinguishing_scenario') or '')[:200]))
            print(' parent_rat=%s' % (r.get('rationale') or '')[:300])
            continue
        print('\n## %s %s/%s/%s pol=%s mod=%s st=%s eq=%s res=%s conf=%s rn=%s' % (
            k, r['classification'], r['domain'], r['oracle_relation'], short_cov(r), r['modality'], r['strength_vs_canonical'],
            r['normative_strength_equivalence'], (r.get('strength_resolution') or {}).get('code'), r['confidence'], r['review_needed']))
        print(' trig=%s | exc=%s' % ((r.get('trigger') or '')[:170], (r.get('exceptions') or '')[:170]))
        if r.get('related_policy_ids'):
            print(' related=%s' % r['related_policy_ids'])
        if r.get('canonical_conflict_ids'):
            print(' conflict=%s' % r['canonical_conflict_ids'])
        if r.get('extra_fragment'):
            print(' extra[%s]=%s' % (r.get('extra_fragment_kind'), r['extra_fragment'][:300]))
        if r.get('distinguishing_scenario'):
            print(' scen=%s' % r['distinguishing_scenario'][:300])
        print(' rat=%s' % (r.get('rationale') or '')[:380])
        if r.get('review_reason'):
            print(' review=%s' % r['review_reason'][:300])
        if r.get('future_human_decision'):
            print(' fhd=%s' % r['future_human_decision'][:300])
        for s in r.get('subclauses') or []:
            print('  - %s %s pol=%s mod=%s eq=%s: %s' % (s.get('subclause_id'), s.get('classification'), short_cov(s), s.get('modality'), s.get('normative_strength_equivalence'), (s.get('text') or '')[:230]))


def main():
    utf8_stdout()
    a = sys.argv[1:]
    cmd = a[0] if a else ''
    if cmd == 'batch':
        p = batch_path(a[1])
        keys = a[2:]
        if os.path.exists(p):
            raise SystemExit('batch exists: %s' % a[1])
        b = all_baseline()
        bad = [k for k in keys if k.split('/')[0] not in b]
        if bad:
            raise SystemExit('unknown keys %s' % bad)
        write_json(os.path.join('_decisions', a[1] + '.batch.json'), {'keys': keys})
        print('batch', a[1], len(keys))
    elif cmd == 'blind':
        ctx = int(a[a.index('--ctx') + 1]) if '--ctx' in a else 1
        blind(a[1], ctx)
    elif cmd == 'reveal':
        reveal(a[1])
    elif cmd == 'pol':
        for i in a[1:]:
            p = policies()[i]
            print(i, '[' + p['normative_strength'] + ']', p['normalized_policy'])
    elif cmd == 'src':
        show_range(a[1], int(a[2]), int(a[3]), 0)
    elif cmd == 'cov':
        r = coverage(a[1])[a[2]]
        print(json.dumps(r, ensure_ascii=False, indent=0))
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
