import json, sys
rows=[json.loads(l) for l in open('_adjudication/WORKBENCH.jsonl',encoding='utf-8')]
v2=[json.loads(l) for l in open(r'..\step2_controlled_repair_v2\REPAIRED_CLASSIFICATIONS.jsonl',encoding='utf-8')]
idx={}
for r in v2:
    for e in r.get('evidence_refs') or []:
        idx.setdefault((r['candidate'], e['path'].split('/output/template/')[-1]),[]).append((e['start_line'],e['end_line'],r))
    if not r.get('evidence_refs'):
        for e in r.get('current_evidence_refs') or []:
            if e.get('start_line'):
                idx.setdefault((r['candidate'], e['path'].split('/template/')[-1]),[]).append((e['start_line'],e['end_line'],r))
themes=sys.argv[1].split(','); w=int(sys.argv[2]) if len(sys.argv)>2 else 4
for x in rows:
    if x['theme'] not in themes and x['id'] not in themes: continue
    print('## %s p%d %s %s:%d-%d | %s' % (x['id'], x['pass'], x['candidate'], x['path'].split('/')[-1], x['start_line'], x['end_line'], x['claim'][:150]))
    for l in x['context']:
        if '>' in l[:6]: print('   ', l[:250])
    seen=set()
    for s,e,r in sorted(idx.get((x['candidate'],x['path']),[]), key=lambda t:t[0]):
        if s<=x['end_line']+w and e>=x['start_line']-w and r['source_key'] not in seen:
            seen.add(r['source_key'])
            print('    V2 %d-%d %s %s/%s pol=%s: %s' % (s,e,r['source_key'],r['classification'],r.get('modality'),[c['policy_id'] for c in r.get('canonical_coverage') or []],r['claim_text'][:150]))
