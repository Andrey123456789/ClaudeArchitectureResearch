import json,hashlib
from rcommon import out_path, read_jsonl, utf8_stdout, norm_ws
utf8_stdout()
rows=read_jsonl(out_path('CROSS_METHOD_ADJUDICATION.jsonl'))
print(sorted(rows[0].keys()))
for r in rows:
    if r['kind'] in ('STRENGTH_CELL','QUALIFIED_OVERRIDE','SOURCE_POLICY_CONFLICT'):
        print(json.dumps(r,ensure_ascii=False)[:520])
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
def h(k): return hashlib.sha256(('R22|'+k).encode()).hexdigest()
by={}
for r in rows:
    if str(r.get('view_record_type') or '').startswith('REPAIR'): continue
    by.setdefault(r['applicability_status'],[]).append(r)
quota={'UNKNOWN_NOT_EXTRACTED':10,'STATED_ATTRIBUTED':10,'DERIVED_FROM_CLAIM':8,'STATED_REVIEWED':2}
print({k:len(v) for k,v in by.items()})
for st,n in quota.items():
    for r in sorted(by[st],key=lambda x:h(x['source_key']))[:n]:
        print(st,r['source_key'],'|TRIG:',norm_ws(str(r['trigger_field_original']))[:80],'|DERIVED:',norm_ws(str(r['applicability_trigger']))[:70],'|DELIV:',norm_ws(str(r['delivery_context']))[:60],'|CLAIM:',norm_ws(r['claim_text'])[:130])
