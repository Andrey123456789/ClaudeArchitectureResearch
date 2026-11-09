import sys,re,os,json
sys.path.insert(0, r"C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4\stage_A\reconciled\step2_controlled_repair_v1\_tools")
from pi012 import *
from rcommon import *
utf8_stdout()
KN=set('httpclient-factory http-api ef-core swagger caching authentication api-versioning dependency-injection logging angular health-check docker aspnet-error-handling configuration dotnet-testing modern-csharp ci-cd'.split())
def kn(path):
    m=re.search(r'\.claude/skills/([^/]+)/(.*)',path)
    return bool(m and (m.group(1) in KN or m.group(2).startswith('references/')))
cases={c['key'].split('/')[0] for c in read_json(out_path(R,'CASES.json'))['cases']}
FORMS={'do_not_unless':re.compile(r"\b(do not|don't)\b[^.;]{0,120}\b(unless|without)\b",re.I),'only_when':re.compile(r"\bonly (when|if)\b|\bcreated only\b|\badded only\b",re.I),'do_not_when':re.compile(r"\b(do not|don't)\b[^.;]{0,120}\b(when|if)\b",re.I)}
out={}
for c in CANDIDATES:
    for k,r in baseline(c).items():
        if k in cases or r.get('modality') not in('MUST_NOT','MUST'): continue
        refs=r.get('evidence_refs') or []
        if not refs or not all(kn(e['path']) for e in refs): continue
        # sentences of the evidence closest to the claim
        claim=set(re.findall(r'\w+',(r.get('claim_text') or '').lower()))
        best=None;bj=0
        for e in refs:
            ls=read_lines(input_path(c,e['path'].split('/template/')[1]))
            t=norm_ws(' '.join(ls[e['start_line']-1:e['end_line']]))
            for s in re.split(r'(?<=[.;])\s+',t):
                w=set(re.findall(r'\w+',s.lower()))
                j=len(w&claim)/max(1,len(w|claim))
                if j>bj: bj,best=j,s
        if not best: continue
        for f,rx in FORMS.items():
            if rx.search(best):
                out.setdefault(f,[]).append((c,k,r['modality'],r['classification'][:6],best[:170]))
                break
for f,v in out.items():
    print(f,len(v))
    for x in v: print('  ',*x)
