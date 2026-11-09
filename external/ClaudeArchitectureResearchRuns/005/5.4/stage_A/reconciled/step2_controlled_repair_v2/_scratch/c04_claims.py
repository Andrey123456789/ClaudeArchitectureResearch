import re
from rcommon import out_path, read_jsonl, utf8_stdout
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
pat=re.compile(r'commit',re.I)
pk=re.compile(r'package|lock|manifest|npm',re.I)
for r in rows:
    t=(r.get('claim_text') or '')
    if pat.search(t) and pk.search(t):
        ev=r.get('evidence') or r.get('locations') or r.get('path')
        print(r['source_key'],r['classification'],r.get('modality'),'|',t[:260].replace('\n',' '))
