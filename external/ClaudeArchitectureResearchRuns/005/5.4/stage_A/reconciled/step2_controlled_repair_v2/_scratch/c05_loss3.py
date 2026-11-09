import json
from collections import Counter
from rcommon import CANDIDATES, baseline, out_path, read_jsonl, utf8_stdout, v1_path
from roverlay import NOT_OWNER_CODES
utf8_stdout()
print('NOT_OWNER_CODES',NOT_OWNER_CODES)
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
base={k:r for c in CANDIDATES for k,r in baseline(c).items()}
# Did v1 itself lose a frozen reading with no rule naming the code?
ov={}
for o in read_jsonl(out_path('_rules','R01-HQ06-PI012','OVERLAY.jsonl'))+read_jsonl(out_path('_rules','R25-COR103','OVERLAY.jsonl')):
    ov.setdefault(o['key'].split('/')[0],[]).append(o['set'])
lost=Counter(); rows=[]; src=Counter()
for k,b in base.items():
    bs=b.get('strength_resolution'); vs=v1[k].get('strength_resolution')
    if bs and not vs:
        named=any('strength_resolution_code' in s for s in ov.get(k,[]))
        lost['named' if named else 'not_named']+=1
        if not named:
            rows.append((k,bs.get('code'),v1[k]['classification'],v1[k].get('strength_vs_canonical'),v1[k].get('strength_mechanical_mismatch'),v1[k]['repair']['rules'][:4]))
    if bs and vs and bs!=vs:
        src[(bs.get('source','')[:12],vs.get('source','')[:16],'code same' if bs.get('code')==vs.get('code') else 'code differs')]+=1
print('frozen reading gone in v1:',dict(lost))
for r in rows[:30]: print(' ',r)
print('frozen reading rewritten in v1:',dict(src))
# Witness effect of the wipe on the current view.
cov={(x['candidate'],x['policy_id']):x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
cov1={(x['candidate'],x['policy_id']):x for x in read_jsonl(v1_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
print('M API-012 v2 direct',cov[('M','API-012')]['direct_source_keys'],'v1 direct',cov1[('M','API-012')]['direct_source_keys'])
print('M API-012 v2 status',cov[('M','API-012')].get('effective_status') or cov[('M','API-012')].get('status'),'strength',cov[('M','API-012')]['strength_status'])
mv=[k for k in cov if k in cov1 and (set(cov[k]['direct_source_keys'])-set(cov1[k]['direct_source_keys']))]
print('cells with a direct witness added since v1:',len(mv))
for k in mv: print(' ',k,sorted(set(cov[k]['direct_source_keys'])-set(cov1[k]['direct_source_keys'])))
