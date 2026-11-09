import json
from collections import Counter
from rcommon import out_path, read_json, utf8_stdout
utf8_stdout()
m=read_json(out_path('SAME_TASK_MATRIX.json'))
for k,v in m['hook_tasks'].items():
    print(k,'|',v['command'],'|',v['expectation'],'|',{c:(v[c]['first'],v[c]['second']) for c in ('M','M1','L0','L1','K0','K1')})
for k,v in m['manifest_tasks'].items():
    print(k,'|',{c:(v[c]['left_pad_rejected'],v[c]['other_lib_rejected']) for c in v})
for k,v in m['text_tasks'].items():
    print(k,'|',{c:sorted({x['loading'] for x in v[c]}) for c in v})
w=read_json(out_path('WORKING_COPY_MANIFEST.json'))
print({c:sum(1 for f in w['candidates'][c].values() if f['origin']=='MODIFIED') for c in w['candidates']})
