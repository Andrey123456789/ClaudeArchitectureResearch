import sys,json
from witness import changed_ranges
from rcommon import *
rule=sys.argv[1]; table=json.loads(sys.argv[2])
rows=[]
for k,row in sorted(changed_ranges().items()):
    if row['disposition']: continue
    c,rel,a,b=k
    old=norm_ws(' '.join(read_lines(input_path(c,rel))[a-1:b]))
    hit=None
    for t in table:
        if (t.get('path') in (None,rel)) and (t.get('cand') in (None,c)) and t['old'].lower() in old.lower():
            hit=t;break
    if not hit:
        print('UNMATCHED',c,rel,a,b,old[:160]);continue
    rows.append(dict(candidate=c,path=rel,start_line=a,end_line=b,disposition=hit.get('disp','REWORDED'),new_quote=hit['new'],note=hit['note'],n_records=len(row['keys']),keys=row['keys']))
p=out_path('_rules',rule,'dispositions.py')
with open(p,'w',encoding='utf-8',newline='\n') as f:
    f.write('"""Evidence dispositions for %s. Generated from a reviewed mapping, kept as literal data."""\nDISPOSITIONS = '%rule)
    f.write(json.dumps(rows,ensure_ascii=False,indent=0).replace('null','None').replace('true','True').replace('false','False'))
    f.write('\n')
print('wrote',len(rows))
