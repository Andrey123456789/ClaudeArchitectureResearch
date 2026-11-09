import re
from collections import Counter
from rcommon import out_path, read_jsonl, utf8_stdout
from triggers import DELIVERY_PAREN
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
kept,dropped=Counter(),Counter()
for r in rows:
    if r.get('applicability_status') in ('UNKNOWN_NOT_EXTRACTED','CONDITION_IN_CLAIM_TEXT'):
        for p in re.findall(r'\(([^()]+)\)', r.get('trigger_field_original') or r.get('trigger') or ''):
            p=p.strip()
            (dropped if DELIVERY_PAREN.search(p) else kept)[p]+=1
print('records with hint',sum(1 for r in rows if r.get('applicability_scope_hint')))
print('KEPT',len(kept),sum(kept.values()))
for p,n in sorted(kept.items(),key=lambda x:-x[1]): print(' ',n,p[:110])
print('DROPPED',len(dropped),sum(dropped.values()))
for p,n in sorted(dropped.items(),key=lambda x:-x[1]): print(' ',n,p[:110])
