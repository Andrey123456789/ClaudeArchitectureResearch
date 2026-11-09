import importlib.util,json
from rcommon import out_path, read_jsonl, utf8_stdout, v1_path
utf8_stdout()
s=importlib.util.spec_from_file_location('rn',out_path('_rules','C06-REVIEW-SETS','review_needed.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
for x in m.ROWS:
    if x.get('test','') and x['test'].startswith('fail closed'):
        r=v2[x['key']]
        print(x['key'],x['status'],'| test:',x['test'],'\n  claim:',r['claim_text'][:260],'\n  v1 reason:',(r.get('review_reason') or '')[:260])
