import json,os,hashlib
from collections import Counter
from rcommon import AUD, out_path, read_jsonl, utf8_stdout, norm_ws
utf8_stdout()
led = read_jsonl(os.path.join(AUD,'AUDIT_LEDGER.jsonl'))
for r in led:
    if r.get('open') and r['case_id'].split(':')[0] in ('ORP','QUE'):
        print(r['case_id'],r.get('candidate'),'|',r.get('decision'),'|',norm_ws(r.get('rationale') or '')[:170],'|',r.get('canonical_policies'))
print('----- 31 question types')
uq = read_jsonl(os.path.join(AUD,'UNRESOLVED_QUEUE.jsonl'))
print(Counter(r['question_type'].split(' ')[0] for r in uq))
print('----- cross method qualified rows')
for r in read_jsonl(out_path('CROSS_METHOD_ADJUDICATION.jsonl')):
    if r['kind']!='PARTIAL_WITNESS_ONLY':
        print(json.dumps({k:r.get(k) for k in ('kind','candidate','policy_id','key','result')},ensure_ascii=False), norm_ws(str(r.get('semantic_reading') or ''))[:200])
print('----- sample')
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
def h(k): return hashlib.sha256(('R22|'+k).encode()).hexdigest()
by={}
for r in rows:
    if r.get('view_record_type'): continue
    by.setdefault(r['applicability_status'],[]).append(r)
quota={'UNKNOWN_NOT_EXTRACTED':10,'STATED_ATTRIBUTED':10,'DERIVED_FROM_CLAIM':8,'STATED_REVIEWED':2}
for st,n in quota.items():
    for r in sorted(by[st],key=lambda x:h(x['source_key']))[:n]:
        print(st,r['source_key'],'|TRIG:',norm_ws(str(r['trigger_field_original']))[:80],'|DERIVED:',norm_ws(str(r['applicability_trigger']))[:70],'|DELIV:',norm_ws(str(r['delivery_context']))[:60],'|CLAIM:',norm_ws(r['claim_text'])[:130])
