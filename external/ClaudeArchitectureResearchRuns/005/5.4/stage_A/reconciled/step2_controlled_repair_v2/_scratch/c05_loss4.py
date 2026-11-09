import json
from rcommon import CANDIDATES, baseline, read_jsonl, utf8_stdout, v1_path
from dataset import load_py
utf8_stdout()
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
base={k:r for c in CANDIDATES for k,r in baseline(c).items()}
for k,rule in (('FG-M-f19c99c143','R17-87-SECSCAN'),('FG-K0-341d9608ae','R19-87-CIUPDATES')):
    b,v=base[k],v1[k]
    print('==',k)
    print(' claim',v['claim_text'][:300])
    print(' frozen',{f:b.get(f) for f in ('classification','modality','strength_vs_canonical')},json.dumps(b.get('strength_resolution'))[:300])
    print(' v1    ',{f:v.get(f) for f in ('classification','modality','strength_vs_canonical','strength_mechanical_mismatch')},json.dumps(v.get('strength_resolution'))[:200])
    print(' cov',b.get('canonical_coverage'),'->',v.get('canonical_coverage'))
    for o in load_py(rule,'overlay.py').OVERLAY:
        if o['key'].split('/')[0]==k: print(' overlay',json.dumps(o['set'],ensure_ascii=False)[:500])
