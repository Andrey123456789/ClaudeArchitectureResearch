import json,re
from rcommon import norm_ws, out_path, policies, read_jsonl, read_lines, utf8_stdout, wc_path
utf8_stdout()
rows={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
B=read_jsonl(out_path('BLIND_REREAD_SAMPLE.jsonl'))
for x in B:
    if x['group_agrees'] and x['force_agrees']: continue
    r=rows[x['key']]
    print('=== %s %s %s | stored %s %s str=%s rel=%s | read %s %s'%(x['id'],x['candidate'],x['key'],r['classification'],r.get('modality'),r.get('strength_vs_canonical'),r.get('oracle_relation'),x['read_group'],x['read_force']))
    print(' claim:',r['claim_text'][:300])
    if r.get('extra_fragment'): print(' extra:',r['extra_fragment'][:260],'|',r.get('extra_fragment_kind'))
    if r.get('distinguishing_scenario'): print(' scen:',r['distinguishing_scenario'][:220])
    for c in r.get('canonical_coverage') or []:
        p=policies()[c['policy_id']]; print('  pol',c['policy_id'],c['coverage'],p['normative_strength'],'|',p['normalized_policy'][:230])
    if r.get('related_policy_ids'): print('  related',r['related_policy_ids'])
    if r.get('subclauses'):
        for s in r['subclauses']: print('  sub',s.get('subclause_id'),s.get('classification'),s.get('modality'),'|',(s.get('text') or s.get('claim_text') or '')[:170])
    for e in r.get('current_evidence_refs') or []:
        if e.get('start_line'):
            rel=e['path'].split('/template/')[1]; L=read_lines(wc_path(x['candidate'],rel))
            print('  ev',rel,e['start_line'],e['end_line'],'|',norm_ws(' '.join(L[e['start_line']-1:e['end_line']]))[:360])
    print(' deliv:',r.get('delivery_context'))
