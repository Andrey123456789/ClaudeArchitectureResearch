import sys,re
sys.path.insert(0, r"C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4\stage_A\reconciled\step2_controlled_repair_v1\_tools")
from pi012 import *
from pi012_compare import load_blind
from rcommon import *
utf8_stdout()
MARK=re.compile(r"\b(must|mustn't|never|do not|don't|shall|forbid\w*|forbidden|cannot|can't|may not|requires?|required)\b",re.I)
RANK={'MUST':3,'MUST_NOT':3,'DEFAULT':2,'SHOULD':2,'SHOULD_NOT':2,'MAY':1,'NONE':0,'DECIDED':3,'REQUIRES_APPROVAL':3}
cases=read_json(out_path(R,'CASES.json'))['cases']
blind=load_blind()
for c in cases:
    k=c['key']; rec,obj=obj_of(k); st=obj.get('modality'); b=blind[k]['modality']
    if b=='UNRESOLVED' or RANK.get(st)==RANK.get(b): continue
    parts=[]
    for ref in rec['evidence_refs']:
        ls=read_lines(input_path(rec['candidate'],ref['path'].split('/template/')[1]))
        t=norm_ws(' '.join(ls[ref['start_line']-1:ref['end_line']]))
        for s in re.split(r'(?<=[.;:])\s+',t):
            if MARK.search(s): parts.append(s[:170])
    if parts:
        print('#%d %s %s->%s nrefs=%d'%(c['n'],k,st,b,len(rec['evidence_refs'])))
        for p in list(dict.fromkeys(parts))[:5]: print('    '+p)
