from rcommon import out_path, read_jsonl, utf8_stdout
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
def v2rules(r): return [x.split(':')[0] for x in r['repair']['rules'] if x[:2] in ('C0',)]
touched={k for k,r in rows.items() if v2rules(r)}
adj=read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))
print('103 total',len(adj),{d:sum(1 for a in adj if a['decision']==d) for d in {a['decision'] for a in adj}})
o=[a for a in adj if a['case_key'].split('/')[0] in touched]
print('103 touched by v2',len(o))
for a in o:
    r=rows[a['case_key'].split('/')[0]]
    print(' ',a['correction_id'],a['case_key'],a['decision'],'applied',sorted((a.get('applied_set') or {}).keys())[:6],'| v2',v2rules(r),'|',r['classification'],r.get('modality'),'|',r['claim_text'][:120])
un=read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
op=[x for x in un if x['kind']=='ORIGINAL_OPEN_RECORD']
print('31 total',len(op))
o2=[x for x in op if x['id'].split('/')[0] in touched]
print('31 touched by v2',len(o2))
for x in o2:
    r=rows[x['id'].split('/')[0]]; print(' ',x['id'],x['status'],v2rules(r),r['classification'],r.get('modality'),'|',r['claim_text'][:120])
