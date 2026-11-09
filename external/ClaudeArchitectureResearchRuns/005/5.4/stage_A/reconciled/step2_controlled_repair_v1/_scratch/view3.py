import re
from collections import Counter
from rcommon import out_path, read_jsonl, utf8_stdout, norm_ws
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
cnt=Counter(); ex={}
for r in rows:
    if r['applicability_status']=='STATED_ATTRIBUTED':
        t=norm_ws(str(r['trigger_field_original']))
        key=re.split(r'[:(]',t)[0][:40].strip().lower()
        cnt[key]+=1; ex.setdefault(key,t)
print(len(cnt), sum(cnt.values()))
for k,v in cnt.most_common(70): print(v,'|',k,'|',ex[k][:90])
