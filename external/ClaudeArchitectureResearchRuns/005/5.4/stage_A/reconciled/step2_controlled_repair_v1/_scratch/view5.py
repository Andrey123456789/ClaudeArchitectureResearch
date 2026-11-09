import sys,os
from rcommon import out_path, read_jsonl, read_lines, utf8_stdout, norm_ws, wc_path
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
keys=[l.strip() for l in sys.argv[1].split(',') if l.strip()]
for k in keys:
    r=rows['FG-'+k]
    print('##',k,r['classification'],r['modality'],'|',norm_ws(r['claim_text']))
    seen=set()
    for x in r['current_evidence_refs'][:3]:
        if x['status'] in('SAME','MOVED') or not x.get('start_line'): continue
        p=x['path'].split('/template/')[1]
        if (p,x['start_line']) in seen: continue
        seen.add((p,x['start_line']))
        c=x['path'].split('/')[1]
        ls=read_lines(wc_path(c,p))
        print('   @',p,x['start_line'],x['end_line'],':',norm_ws(' '.join(ls[x['start_line']-1:x['end_line']]))[:420])
