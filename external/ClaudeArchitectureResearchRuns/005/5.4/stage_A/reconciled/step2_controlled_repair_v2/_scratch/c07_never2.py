import json,re
from collections import Counter
from rcommon import CANDIDATES, norm_ws, out_path, read_jsonl, read_lines, utf8_stdout, wc_path, baseline
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
by={r['source_key']:r for r in rows}
for k in ('FG-M1-9030e201b9','FG-L1-75964b0d7f','FG-K0-40e6fc8d29','FG-L0-a2e9e91e8f','FG-K1-4767fd97b1','FG-K1-bc831815a3','FG-L0-6c42674c92'):
    r=by[k]
    print(k,r['classification'],r.get('modality'),r.get('modality_detail'),'str',r.get('strength_vs_canonical'),'code',r.get('strength_resolution_code'),json.dumps(r.get('strength_resolution'))[:120],'mech',r.get('strength_mechanical_mismatch'),'rules',[x.split(':')[0] for x in r['repair']['rules']],'form',r.get('pi012_form'),'|',r['claim_text'][:120])
    print('   extra',r.get('extra_fragment'),'| deliv',(r.get('delivery_context') or '')[:80])
# Reviewed sets, to see whether the opposite direction was ever read.
rev=set()
for f in ('PI012_79_REVIEW.jsonl','PI012_230_REVIEW.jsonl','PI012_EXTENSION_REVIEW.jsonl','PI012_EXTRA_21_REVIEW.jsonl'):
    rev|={x['key'].split('/')[0] for x in read_jsonl(out_path(f))}
adj={x['case_key'].split('/')[0] for x in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))}
marked=re.compile(r'\b(never|must not)\b',re.I)
soft=('DEFAULT','SHOULD','SHOULD_NOT','MAY')
hits=[r for r in rows if r['repair']['active'] and r.get('modality') in soft and r['classification'] not in ('NON_NORMATIVE',) and marked.search(r.get('claim_text') or '')]
print('active, soft modality, claim says never or must not:',len(hits),Counter(r['candidate'] for r in hits))
print(' by modality',Counter(r.get('modality') for r in hits),'by class',Counter(r['classification'] for r in hits))
print(' already read in a PI-012 list or the 103:',sum(1 for r in hits if r['source_key'] in rev or r['source_key'] in adj))
strict=[r for r in hits if re.match(r'^\s*(never|must not)\b',r.get('claim_text') or '',re.I)]
print(' claim opens with the marked form:',len(strict),Counter(r['candidate'] for r in strict))
hard=[r for r in rows if r['repair']['active'] and r.get('modality')=='MUST_NOT' and marked.search(r.get('claim_text') or '')]
print('for scale: stored MUST_NOT with the same words:',len(hard))
import random
rng=random.Random(20261105)
un=[r for r in hits if r['source_key'] not in rev and r['source_key'] not in adj]
print('not read before:',len(un))
for r in sorted(rng.sample(un,min(24,len(un))),key=lambda r:r['candidate']):
    m=marked.search(r['claim_text']); s=max(0,m.start()-70)
    print(' ',r['source_key'],r['classification'],r.get('modality'),(r.get('delivery_context') or '')[:26],'|',r['claim_text'][s:m.end()+70].replace('\n',' '))
