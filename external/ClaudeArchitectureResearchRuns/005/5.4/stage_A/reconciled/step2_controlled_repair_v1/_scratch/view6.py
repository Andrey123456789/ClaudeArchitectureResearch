import hashlib
from collections import Counter
from rcommon import out_path, read_jsonl, utf8_stdout, norm_ws
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
def h(k): return hashlib.sha256(('R22|'+k).encode()).hexdigest()
by={}
for r in rows:
    if str(r.get('view_record_type') or '').startswith('REPAIR'): continue
    by.setdefault(r['applicability_status'],[]).append(r)
print({k:len(v) for k,v in by.items()})
quota={'UNKNOWN_NOT_EXTRACTED':10,'STATED_ATTRIBUTED':10,'CONDITION_IN_CLAIM_TEXT':8,'STATED_REVIEWED':2}
for st,n in quota.items():
    for r in sorted(by[st],key=lambda x:h(x['source_key']))[:n]:
        print(st[:12],r['source_key'],'|TRIG:',norm_ws(str(r['trigger_field_original']))[:70],'|HINT:',norm_ws(str(r['applicability_hint']))[:60],'|CLAIM:',norm_ws(r['claim_text'])[:120])
