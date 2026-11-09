from collections import Counter
from rcommon import CANDIDATES, out_path, read_jsonl, utf8_stdout, v1_path
from suites_loader import load_suite
utf8_stdout()
cov={(x['candidate'],x['policy_id']):x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
cv1={(x['candidate'],x['policy_id']):x for x in read_jsonl(v1_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
print('cell status or strength differs from v1:',[k for k in cov if (cov[k]['status'],cov[k]['strength_status'])!=(cv1[k]['status'],cv1[k]['strength_status'])])
print('direct set differs from v1:',len([k for k in cov if set(cov[k]['direct_source_keys'])!=set(cv1[k]['direct_source_keys'])]),[k for k in cov if set(cov[k]['direct_source_keys'])!=set(cv1[k]['direct_source_keys'])][:12])
print('stronger_and_weaker',[k for k,x in cov.items() if x['strength_status']=='STRONGER_AND_WEAKER_EVIDENCE'])
cw=read_jsonl(out_path('V1_TO_V2_CROSSWALK.jsonl'))
print(cw[0].keys())
print('class changed rows',[ (x.get('source_key') or x.get('key')) for x in cw if x['status']=='CLASSIFICATION_CHANGED'])
fc=[x for x in cw if x['status']=='FIELD_CHANGED']
print('field changed fields',Counter(f for x in fc for f in (x.get('changed_fields') or x.get('fields') or [])).most_common(10))
c01=load_suite('C01_CPM_EFFECTIVE'); print('C01 cases',len(c01.CASES))
un=read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
print('parity leads',[x['id'] for x in un if x['kind']=='PARITY_LEAD'])
print('interp',[x['id'] for x in un if x['kind']=='INTERPRETATION'])
import subprocess; print(subprocess.run(['dotnet','--version'],capture_output=True,text=True).stdout.strip(), subprocess.run(['node','--version'],capture_output=True,text=True).stdout.strip())
