import json
from rcommon import norm_ws, out_path, read_jsonl, read_lines, utf8_stdout, wc_path
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
for k in ('FG-K1-bc831815a3','FG-K1-4767fd97b1','FG-L0-a2e9e91e8f'):
    r=rows[k]
    print(k,r['classification'],r.get('modality'),r.get('modality_detail'))
    for e in r.get('current_evidence_refs') or []:
        if e.get('start_line'):
            rel=e['path'].split('/template/')[1]
            print('  ',rel,e['start_line'],e['end_line'],'|',norm_ws(' '.join(read_lines(wc_path(r['candidate'],rel))[e['start_line']-1:e['end_line']]))[:420])
for a in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl')):
    if a['correction_id']=='COR-A-K0-0024':
        print({k:str(v)[:420] for k,v in a.items() if k in ('correction_id','decision','case_key','reason','why','proposal','rationale','evidence','note')})
