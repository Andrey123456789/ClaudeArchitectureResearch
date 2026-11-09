"""Read-only query helper over the frozen classification and the audit overlay.

  q.py pol <POLICY> [C...]     records linked to a policy (key, label, modality, strength, claim, primary evidence)
  q.py key <KEY> [...]         one record in full key fields, baseline and effective, plus its correction row if any
  q.py grep <REGEX> [C...]     records whose claim matches
  q.py src <path> <a> <b>      print source lines of an input or working-copy file
"""
import json
import os
import re
import sys

from rcommon import AUD, CANDIDATES, ROOT, baseline, effective, policies, read_jsonl, read_lines, utf8_stdout


def brief(r, width=260):
    ev = (r.get('evidence_refs') or [{}])[0]
    p = (ev.get('path') or '').split('/template/')[-1]
    return '%s %s/%s st=%s | %s | %s:%s' % (r['source_key'], r['classification'][:14], r.get('modality'), (r.get('normative_strength_equivalence') or '')[:10],
                                            (r.get('claim_text') or '')[:width].replace('\n', ' '), p, ev.get('start_line'))


def main():
    utf8_stdout()
    cmd = sys.argv[1]
    if cmd == 'pol':
        pid = sys.argv[2]
        print(json.dumps(policies()[pid], ensure_ascii=False)[:900])
        for c in sys.argv[3:] or CANDIDATES:
            print('==', c)
            for k, r in baseline(c).items():
                objs = [r] + list(r.get('subclauses') or [])
                if any(pid in (o.get('canonical_policy_ids') or []) for o in objs) or pid in (r.get('related_policy_ids') or []):
                    print(brief(r))
    elif cmd == 'key':
        cors = {x['case_key']: x for x in read_jsonl(os.path.join(AUD, 'CORRECTION_PROPOSALS.jsonl'))}
        for key in sys.argv[2:]:
            base = key.split('/')[0]
            c = re.match(r'^(?:FG|PROP|FACET|NCP)-([A-Z0-9]+)-', base)
            for cc in CANDIDATES:
                if base in baseline(cc):
                    r = baseline(cc)[base]
                    keep = {k: r.get(k) for k in ('source_key', 'classification', 'modality', 'domain', 'oracle_relation', 'canonical_policy_ids', 'normative_strength_equivalence', 'claim_text', 'trigger',
                                                  'exceptions', 'extra_fragment', 'review_reason', 'rationale', 'future_human_decision', 'confidence')}
                    keep['evidence'] = ['%s:%s-%s' % (e['path'].split('/template/')[-1], e['start_line'], e['end_line']) for e in r.get('evidence_refs') or []]
                    keep['subclauses'] = [{k: s.get(k) for k in ('subclause_id', 'classification', 'modality', 'canonical_policy_ids', 'text', 'claim_text')} for s in r.get('subclauses') or []]
                    print(json.dumps(keep, ensure_ascii=False, indent=0))
                    if base in cors or key in cors:
                        x = cors.get(key) or cors.get(base)
                        print('CORRECTION', json.dumps({k: x[k] for k in ('correction_id', 'ratification', 'set', 'rationale', 'quotes', 'alternatives', 'remaining_ambiguity')}, ensure_ascii=False)[:2500])
    elif cmd == 'grep':
        rx = re.compile(sys.argv[2], re.I)
        for c in sys.argv[3:] or CANDIDATES:
            for k, r in baseline(c).items():
                if rx.search(r.get('claim_text') or ''):
                    print(c, brief(r))
    elif cmd == 'src':
        p = sys.argv[2]
        a, b = int(sys.argv[3]), int(sys.argv[4])
        fp = p if os.path.isabs(p) else os.path.join(ROOT, p)
        ls = read_lines(fp)
        for i in range(a - 1, min(b, len(ls))):
            print('%d: %s' % (i + 1, ls[i]))


if __name__ == '__main__':
    main()
