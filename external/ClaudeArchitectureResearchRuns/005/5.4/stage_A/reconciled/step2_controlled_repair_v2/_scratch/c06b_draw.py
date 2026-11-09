import hashlib,importlib.util
from rcommon import CANDIDATES, norm_ws, out_path, read_jsonl, read_lines, utf8_stdout, wc_path
utf8_stdout()
spec=importlib.util.spec_from_file_location('r22s',out_path('_rules','R22-111-TRIGGER','sample.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ex={x['key'] for x in m.SAMPLE}
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
for c in CANDIDATES:
    pool=[r for r in rows if r['candidate']==c and r.get('applicability_scope_hint') and r['source_key'] not in ex and r['repair']['active']]
    pool.sort(key=lambda r:hashlib.sha256(('C06B|'+r['source_key']).encode()).hexdigest())
    for r in pool[:5]:
        e=next((x for x in r.get('current_evidence_refs') or [] if x.get('start_line')),None)
        src=''
        if e:
            rel=e['path'].split('/template/')[1]
            src=rel+':%d '%e['start_line']+norm_ws(' '.join(read_lines(wc_path(c,rel))[e['start_line']-1:e['end_line']]))[:230]
        print(r['source_key'],r['classification'],r.get('modality'),r['applicability_status'])
        print('  trig:',(r.get('trigger_field_original') or '')[:120])
        print('  hint:',r['applicability_scope_hint'])
        print('  claim:',(r.get('claim_text') or '')[:200])
        print('  src:',src)
