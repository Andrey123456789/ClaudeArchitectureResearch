import json
from rcommon import out_path, read_jsonl, utf8_stdout, input_path
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
r=rows['FG-M-95efcc9a8b']
print({k:(v if not isinstance(v,(list,dict)) else json.dumps(v)[:160]) for k,v in r.items() if k in ('classification','modality','oracle_relation','strength_vs_canonical','related_policy_ids','canonical_coverage','extra_fragment','trigger','exceptions')})
