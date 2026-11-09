import json
from collections import Counter
from rcommon import CANDIDATES, out_path, read_jsonl, utf8_stdout, v1_path
utf8_stdout()
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
print('modality vs v1:',[(k,v1[k].get('modality'),v2[k].get('modality'),[x.split(':')[0] for x in v2[k]['repair']['rules'] if x[:2]=='C0']) for k in v1 if k in v2 and v1[k].get('modality')!=v2[k].get('modality')])
print('class vs v1:',[(k,v1[k]['classification'],v2[k]['classification']) for k in v1 if k in v2 and v1[k]['classification']!=v2[k]['classification']])
print('claim by rule:',Counter([x.split(':')[0] for x in v2[k]['repair']['rules'] if x[:2]=='C0'][0] for k in v1 if k in v2 and v1[k].get('claim_text')!=v2[k].get('claim_text')))
print('applic vs v1',Counter((v1[k].get('applicability_status'),v2[k].get('applicability_status')) for k in v1 if k in v2 and v1[k].get('applicability_status')!=v2[k].get('applicability_status')))
rn=read_jsonl(out_path('REVIEW_NEEDED_62.jsonl')); print('62',Counter(x['status'] for x in rn))
pw=read_jsonl(out_path('PARTIAL_WITNESSES_38.jsonl')); print('38',Counter(x['status'] for x in pw),[ (x['candidate'],x['policy_id']) for x in pw if x['status']!='CONFIRMED'])
nc=read_jsonl(out_path('NEW_CLAIMS_42_REVIEW.jsonl')); print('new',len(nc),Counter(x['kind'] for x in nc),Counter(x.get('rule','PROPOSAL') for x in nc))
ex=read_jsonl(out_path('PI012_EXTRA_21_REVIEW.jsonl')); print('21',Counter(x['kind'] for x in ex),Counter(x['decision'] for x in ex),[x['key'] for x in ex if x['decision']!='KEEP'])
ad=read_jsonl(out_path('BLIND_REREAD_ADJUDICATION.jsonl')); print('adj',Counter(x['result'] for x in ad))
un=read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')); print('unresolved',Counter((x['kind'],x['status']) for x in un))
print('open_question',[k for k,r in v2.items() if r['repair'].get('open_question')][:12])
print('uncertain',Counter(r['classification'] for r in v2.values() if r['repair']['active']).get('UNCERTAIN',0))
