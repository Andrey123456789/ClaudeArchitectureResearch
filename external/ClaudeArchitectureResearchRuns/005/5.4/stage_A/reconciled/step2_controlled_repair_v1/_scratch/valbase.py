import sys
sys.path.insert(0, r"C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4\stage_A\reconciled\step2_controlled_repair_v1\_tools")
from rcommon import *; from roverlay import *
from collections import Counter
utf8_stdout()
m=Counter()
for c in CANDIDATES:
    for r in baseline(c).values():
        for o in [r]+list(r.get('subclauses') or []): m[o.get('modality')]+=1
print(m)
for c in CANDIDATES:
    e=validate_candidate(c,dict(baseline(c)))
    print(c,len(e),e[:6])
    cov=coverage_of(baseline(c).values())
    d=[p for p,x in cov.items() if x['strength_status']!=coverage(c)[p]['strength_status'] or x['direct_source_keys']!=coverage(c)[p]['direct_source_keys']]
    print(' coverage engine diffs vs stored:',len(d),d[:5])
