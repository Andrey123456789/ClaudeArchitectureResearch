"""Read-only: prints bounded review sets with current source text, for individual reading. Uses the current v2 view and candidate bytes.

  setview.py review_needed [C ...]   the v1 review_needed records
  setview.py partial                 cells with no FULL direct witness, with their witnesses
  setview.py added [rule ...]        added claims and proposals
"""
import sys

from rcommon import CANDIDATES, norm_ws, out_path, policies, read_jsonl, read_lines, utf8_stdout, v1_path, wc_path


def src(ref, pad=0, width=420):
    p = ref.get('path') or ''
    if '/template/' not in p or not ref.get('start_line'):
        return '(no current line)'
    c = p.split('/')[1]
    rel = p.split('/template/')[1]
    ls = read_lines(wc_path(c, rel))
    a, b = max(1, ref['start_line'] - pad), min(len(ls), ref['end_line'] + pad)
    return '%s:%d-%d %s' % (rel.replace('.claude/', ''), ref['start_line'], ref['end_line'], norm_ws(' '.join(ls[a - 1:b]))[:width])


def show(r, width=420):
    cov = ','.join('%s:%s' % (x['policy_id'], x['coverage'][:1]) for x in r.get('canonical_coverage') or [])
    print('%s %s %s str=%s code=%s [%s] rules=%s' % (r['source_key'], r['classification'], r.get('modality'), r.get('strength_vs_canonical'), r.get('strength_resolution_code'), cov, ','.join(t.split(':')[0] for t in r['repair']['rules'])))
    print('   claim: %s' % (r.get('claim_text') or '')[:300].replace('\n', ' '))
    if r.get('review_reason'):
        print('   why flagged: %s' % r['review_reason'][:300])
    for ref in (r.get('current_evidence_refs') or [])[:2]:
        print('   src: %s' % src(ref, 0, width))
    if r.get('subclauses'):
        for s in r['subclauses'][:4]:
            print('   sub %s %s %s: %s' % ((s.get('subclause_id') or '').split('/')[-1], s.get('classification'), s.get('modality'), (s.get('claim_text') or s.get('text') or '')[:150]))


def main():
    utf8_stdout()
    cmd = sys.argv[1]
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by = {r['source_key']: r for r in rows}
    if cmd == 'review_needed':
        v1 = [r['source_key'] for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl')) if r.get('review_needed')]
        for k in v1:
            if by[k]['candidate'] in (sys.argv[2:] or CANDIDATES):
                print('-' * 3, by[k]['candidate'])
                show(by[k])
    elif cmd == 'partial':
        pol = policies()
        cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
        for x in cov:
            if x['direct_source_keys']:
                continue
            if sys.argv[2:] and x['candidate'] not in sys.argv[2:]:
                continue
            print('=' * 3, x['candidate'], x['policy_id'], pol[x['policy_id']]['normative_strength'], '|', pol[x['policy_id']]['normalized_policy'][:330])
            print('   override: %s' % (x.get('reviewer_override_note') or '')[:400])
            for k in x['partial_source_keys'][:5]:
                r = by[k]
                print('   w %s %s %s | %s' % (k, r['classification'][:9], r.get('modality'), (r.get('claim_text') or '')[:190].replace('\n', ' ')))
                for ref in (r.get('current_evidence_refs') or [])[:1]:
                    print('      src: %s' % src(ref, 0, 260))
    elif cmd == 'added':
        for r in rows:
            if str(r.get('view_record_type') or '').startswith('REPAIR'):
                if sys.argv[2:] and not any(t in sys.argv[2:] for t in r['repair']['rules']):
                    continue
                print('---', r['candidate'], r.get('view_record_type'))
                show(r, 300)


if __name__ == '__main__':
    main()
