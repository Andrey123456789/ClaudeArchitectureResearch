import json, sys, re
sys.path.insert(0, '_tools')
from rcommon import policies, read_lines, wc_path
P = policies()
rows = {}
for l in open('REPAIRED_CLASSIFICATIONS.jsonl', encoding='utf-8'):
    r = json.loads(l); rows[r['source_key']] = r
cls = [json.loads(l) for l in open('MARKED_NEVER_SOFT_MODALITY.jsonl', encoding='utf-8')]
out = []
for i, m in enumerate(cls, 1):
    r = rows[m['key']]
    out.append('## %02d %s %s %s/%s conf=%s sv=%s res=%s' % (i, m['key'], r['candidate'], r['classification'], r['modality'], r.get('confidence'), r.get('strength_vs_canonical'), (r.get('strength_resolution') or {}).get('code')))
    out.append('CLAIM: ' + r['claim_text'])
    for c in r.get('canonical_coverage') or []:
        p = P[c['policy_id']]
        out.append('  POL %s [%s %s] %s' % (c['policy_id'], p['normative_strength'], c['coverage'], p['normalized_policy']))
    for s in r.get('subclauses') or []:
        out.append('  SUB %s %s/%s: %s' % (s.get('subclause_id'), s.get('classification'), s.get('modality'), (s.get('claim_text') or s.get('text') or '')[:160]))
    for e in (r.get('current_evidence_refs') or [])[:3]:
        if not e.get('start_line'): continue
        rel = e['path'].split('/template/')[1]
        ls = read_lines(wc_path(r['candidate'], rel))
        a, b = e['start_line'], min(e['end_line'], e['start_line'] + 6)
        out.append('  SRC %s:%d-%d  %s' % (rel, a, e['end_line'], ' / '.join(x.strip() for x in ls[a - 1:b])[:600]))
    out.append('')
open('_adjudication/modality86/SHEET.md', 'w', encoding='utf-8').write('\n'.join(out))
print(len(cls))
