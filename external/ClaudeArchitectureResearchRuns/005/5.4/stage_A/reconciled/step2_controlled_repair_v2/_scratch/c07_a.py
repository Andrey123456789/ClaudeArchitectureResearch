from rcommon import out_path, read_jsonl, utf8_stdout
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
for k in ('FG-M-bea4987bb6','FG-M1-c6cfdc9dbf','FG-L0-009161dd35','FG-L1-d6ab123b1f','FG-K1-112617f8b3'):
    r=rows[k]; print(k,r['applicability_status'],'|hint',r.get('applicability_scope_hint'),'|trig',r.get('applicability_trigger'),'|deliv',r.get('delivery_context'),'|str',r.get('strength_vs_canonical'),'|form',r.get('pi012_form'),'|rules',[x.split(':')[0] for x in r['repair']['rules']])
