import re
from collections import Counter
from rcommon import out_path, read_jsonl, utf8_stdout
from triggers import DELIVERY_PAREN
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
kept,dropped=Counter(),Counter()
nop=0
for r in rows:
    if r.get('applicability_status') in ('UNKNOWN_NOT_EXTRACTED','CONDITION_IN_CLAIM_TEXT'):
        t=r.get('trigger_field_original') or r.get('trigger') or ''
        gs=re.findall(r'\(([^()]+)\)',t)
        if not gs: nop+=1
        for g in gs:
            for p in g.split(';'):
                p=p.strip()
                if p: (dropped if DELIVERY_PAREN.search(p) else kept)[p]+=1
n=[r for r in rows if r.get('applicability_scope_hint')]
print('records with hint',len(n),'no parenthesis',nop,'distinct kept',len(kept),'dropped',len(dropped))
print('KEPT:',' | '.join('%d %s'%(c,p[:60]) for p,c in sorted(kept.items(),key=lambda x:-x[1])))
print('DROPPED:',' | '.join('%d %s'%(c,p[:60]) for p,c in sorted(dropped.items(),key=lambda x:-x[1])))
