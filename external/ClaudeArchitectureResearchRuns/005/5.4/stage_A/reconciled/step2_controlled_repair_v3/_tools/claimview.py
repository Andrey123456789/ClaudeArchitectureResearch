"""Read-only helper: shows the records behind disturbed evidence ranges, or named records, with their current claim, label and modality.

  claimview.py ranges [C ...]   every CHANGED range with no disposition, plus dispositions whose quote no longer resolves
  claimview.py keys KEY ...     named records
"""
import sys

from rcommon import CANDIDATES, input_path, norm_ws, out_path, read_jsonl, read_lines, utf8_stdout
from witness import check_dispositions, changed_ranges, load_dispositions


def view():
    return {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}


def show(r):
    cov = ','.join('%s:%s' % (x['policy_id'], x['coverage'][:1]) for x in r.get('canonical_coverage') or [])
    print('  %s %s %s [%s] rules=%s' % (r['source_key'], r['classification'], r.get('modality'), cov, ','.join(t.split(':')[0] for t in r['repair']['rules'])))
    print('     claim: %s' % (r.get('claim_text') or '')[:420].replace('\n', ' '))
    if r.get('extra_fragment'):
        print('     extra: %s' % r['extra_fragment'][:240])


def main():
    utf8_stdout()
    cmd = sys.argv[1]
    v = view()
    if cmd == 'keys':
        for k in sys.argv[2:]:
            show(v[k])
        return
    cands = sys.argv[2:] or CANDIDATES
    errs, ranges = check_dispositions(cands)
    for k, row in sorted(ranges.items()):
        if row['disposition']:
            continue
        c, rel, a, b = k
        print('%s %s:%d-%d' % (c, rel, a, b))
        print('   OLD: %s' % norm_ws(' '.join(read_lines(input_path(c, rel))[a - 1:b]))[:260])
        for key in row['keys']:
            show(v[key])
    print('--- dispositions whose quote is gone')
    for e in errs:
        if e.startswith('disposition quote'):
            print(e[:200])
    disp = load_dispositions()
    for (c, rel, a, b), d in disp.items():
        if d['disposition'] == 'REMOVED':
            continue
        from witness import FileMap
        fm = FileMap()
        s = fm.stream(c, rel)
        if s is None or norm_ws(d['new_quote']) not in s[0]:
            print('%s %s:%d-%d [%s] %s' % (c, rel, a, b, d.get('rule'), d['new_quote'][:120]))
            for key in (ranges.get((c, rel, a, b)) or {}).get('keys', []):
                show(v[key])


if __name__ == '__main__':
    main()
