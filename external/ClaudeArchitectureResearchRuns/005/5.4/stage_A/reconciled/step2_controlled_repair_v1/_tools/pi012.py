"""PI-012 review tooling (R01).

  pi012.py plan                      freeze the deduplicated case list to _rules/R01-HQ06-PI012/CASES.json
  pi012.py blind <from> <to>         print cases without stored modality, label or policies
  pi012.py reveal <from> <to>        print the stored fields and the audit suggestion for the same cases
  pi012.py build                     compile _rules/R01-HQ06-PI012/blind/*.dec and final.dec into the review files and run per-record invariants

Case key = the original stable key (record or record/subclause). A record in both lists is one case with both memberships.
Decision line (blind): KEY | MODALITY | CONF | reading | counterexample
MODALITY: MUST MUST_NOT DEFAULT SHOULD SHOULD_NOT MAY NONE UNRESOLVED. CONF: HIGH MEDIUM LOW.
"""
import json
import os
import re
import sys

from rcommon import AUD, CANDIDATES, baseline, effective, input_path, norm_ws, out_path, policies, read_json, read_jsonl, read_lines, utf8_stdout, write_json, write_jsonl

R = '_rules/R01-HQ06-PI012'


def split_key(k):
    return (k.split('/')[0], k.split('/')[1] if '/' in k else None)


def cand_of(base):
    for c in CANDIDATES:
        if base in baseline(c):
            return c
    raise KeyError(base)


def obj_of(key):
    base, sub = split_key(key)
    rec = baseline(cand_of(base))[base]
    if sub:
        for s in rec.get('subclauses') or []:
            if s.get('subclause_id') == key or s.get('subclause_id') == sub or s.get('subclause_id', '').endswith('/' + sub):
                return rec, s
        raise KeyError(key)
    return rec, rec


def plan():
    n79 = read_jsonl(os.path.join(AUD, 'PI012_NEGATIVE_MODALITY_REVIEW.jsonl'))
    n230 = read_jsonl(os.path.join(AUD, 'A13_RESIDUAL_LEADS.jsonl'))
    cases = {}
    for r in n79:
        cases.setdefault(r['key'], {'key': r['key'], 'lists': [], 'closest': None})['lists'].append('N79')
        if r.get('source', {}).get('quote'):
            cases[r['key']]['closest'] = r['source']['quote'][:300]
            cases[r['key']]['ref'] = {k: r['source'][k] for k in ('path', 'start_line', 'end_line')}
    keys79_base = {split_key(r['key'])[0]: r['key'] for r in n79}
    for r in n230:
        k = r['source_key']
        target = k if k in cases else None
        if target is None:
            target = k
            cases.setdefault(k, {'key': k, 'lists': [], 'closest': r['closest_sentence']})
        cases[target]['lists'].append('L230')
        cases[target]['closest_230'] = r['closest_sentence']
    rows = sorted(cases.values(), key=lambda x: (CANDIDATES.index(cand_of(split_key(x['key'])[0])), x['key']))
    for i, r in enumerate(rows, 1):
        r['n'] = i
    write_json(os.path.join(R, 'CASES.json'), {'n_cases': len(rows), 'n79': len(n79), 'n230': len(n230), 'cases': rows})
    print(len(rows), 'cases; both lists', sum(1 for r in rows if len(set(r['lists'])) == 2))


def role(path):
    m = re.search(r'\.claude/skills/([^/]+)/(.*)', path)
    if m:
        return ('REF' if m.group(2).startswith('references/') else 'SKILL') + ':' + m.group(1)
    return path.split('/template/')[-1]


def heading(lines, a):
    for i in range(a - 2, -1, -1):
        if lines[i].startswith('#'):
            return lines[i].strip()[:70]
    return ''


def locate(rec, closest):
    """Find the evidence ref holding the closest sentence; fall back to the first ref."""
    refs = rec.get('evidence_refs') or []
    want = norm_ws(closest or '').lower()[:60]
    for ref in refs:
        ls = read_lines(input_path(rec['candidate'], ref['path'].split('/template/')[1]))
        text = norm_ws(' '.join(ls[max(0, ref['start_line'] - 1):ref['end_line']])).lower()
        if want and want in text:
            return ref, ls
    # search the whole file of each ref
    for ref in refs:
        ls = read_lines(input_path(rec['candidate'], ref['path'].split('/template/')[1]))
        for i, l in enumerate(ls):
            if want and want[:40] in norm_ws(l).lower():
                return dict(ref, start_line=i + 1, end_line=i + 1), ls
    ref = refs[0]
    return ref, read_lines(input_path(rec['candidate'], ref['path'].split('/template/')[1]))


def show_case(r, reveal=False):
    rec, obj = obj_of(r['key'])
    c = rec['candidate']
    closest = r.get('closest') or r.get('closest_230')
    ref, ls = locate(rec, closest)
    a, b = ref['start_line'], ref['end_line']
    src = ' '.join(x.strip() for x in ls[a - 1:b])
    if len(src) > 420:
        want = norm_ws(closest or '')[:50].lower()
        i = src.lower().find(want) if want else -1
        src = ('…' + src[max(0, i - 120):i + 300] + '…') if i >= 0 else src[:420] + '…'
    prev = ls[a - 2].strip()[:110] if a >= 2 else ''
    nxt = ls[b].strip()[:110] if b < len(ls) else ''
    claim = (obj.get('claim_text') or obj.get('text') or rec.get('claim_text') or '')[:200]
    print('#%d %s [%s] %s:%d %s %s' % (r['n'], r['key'], ','.join(sorted(set(r['lists']))), role(ref['path']), a, heading(ls, a), ''))
    print('  C: ' + claim)
    print('  S: ' + src)
    if prev or nxt:
        print('  ~ ' + prev + ' // ' + nxt)
    if reveal:
        print('  STORED %s/%s st=%s pol=%s' % (obj.get('classification'), obj.get('modality'), obj.get('normative_strength_equivalence'), obj.get('canonical_policy_ids')))


def blind(a, b, reveal=False):
    cases = read_json(out_path(R, 'CASES.json'))['cases']
    for r in cases[a - 1:b]:
        show_case(r, reveal)


if __name__ == '__main__':
    utf8_stdout()
    cmd = sys.argv[1]
    if cmd == 'plan':
        plan()
    elif cmd == 'blind':
        blind(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'reveal':
        blind(int(sys.argv[2]), int(sys.argv[3]), True)
