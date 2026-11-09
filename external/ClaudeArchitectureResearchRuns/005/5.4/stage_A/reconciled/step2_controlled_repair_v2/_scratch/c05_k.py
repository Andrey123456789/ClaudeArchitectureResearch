import json
from rcommon import out_path, read_jsonl, utf8_stdout, v1_path, policies
utf8_stdout()
k='FG-M-290b3bdb9e'
v2={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}[k]
v1={r['source_key']:r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}[k]
for f in sorted(set(v1)|set(v2)):
    if v1.get(f)!=v2.get(f): print('DIFF',f,'\n  v1',json.dumps(v1.get(f),ensure_ascii=False)[:400],'\n  v2',json.dumps(v2.get(f),ensure_ascii=False)[:400])
for f in ('classification','modality','strength_vs_canonical','strength_resolution_code','canonical_coverage','claim_text','applicability_trigger','applicability_status','trigger_field_original'):
    print(f,json.dumps(v2.get(f),ensure_ascii=False)[:300])
for x in v2.get('canonical_coverage') or []:
    p=policies()[x['policy_id']]; print(x['policy_id'],p['normative_strength'],p['normalized_policy'][:240])
