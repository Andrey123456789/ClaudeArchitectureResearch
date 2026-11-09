import json
from c07_build import REASSESS
from rcommon import norm_ws, out_path, read_jsonl, read_lines, utf8_stdout, wc_path
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
touched={k for k,r in rows.items() if any(x[:2]=='C0' for x in r['repair']['rules'])}
for a in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl')):
    b=a['case_key'].split('/')[0]
    if b in touched and a['correction_id'] not in REASSESS:
        r=rows[b]
        print('==',a['correction_id'],a['case_key'],a['decision'])
        print(json.dumps({k:a.get(k) for k in a if k not in ('case_key','correction_id','decision')},ensure_ascii=False)[:1400])
        print(' now',r['classification'],r.get('modality'),r.get('strength_vs_canonical'),r.get('strength_resolution_code'),[x['policy_id']+':'+x['coverage'][0] for x in r.get('canonical_coverage') or []],'rules',[x.split(':')[0] for x in r['repair']['rules']])
        print(' claim',r['claim_text'][:300])
        for e in r.get('current_evidence_refs') or []:
            if e.get('start_line'):
                rel=e['path'].split('/template/')[1]; print('  ev',rel,e['start_line'],'|',norm_ws(' '.join(read_lines(wc_path(r['candidate'],rel))[e['start_line']-1:e['end_line']]))[:300])
