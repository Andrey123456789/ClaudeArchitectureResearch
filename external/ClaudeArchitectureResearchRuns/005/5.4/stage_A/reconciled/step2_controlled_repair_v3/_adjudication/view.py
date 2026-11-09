import json, sys
rows=[json.loads(l) for l in open('_adjudication/WORKBENCH.jsonl',encoding='utf-8')]
themes=sys.argv[1].split(',')
ctxw=int(sys.argv[2]) if len(sys.argv)>2 else 0
for x in rows:
    if x['theme'] not in themes and x['id'] not in themes: continue
    print('## %s p%d %s %s:%d-%d [%s]' % (x['id'], x['pass'], x['candidate'], x['path'], x['start_line'], x['end_line'], x['modality']))
    print('  CLAIM:', x['claim'][:260])
    for l in x['context']:
        if '>' in l[:6] or ctxw: print('  ', l[:230])
    seen=set()
    for o in x['v2_overlapping_records']:
        if o['key'] in seen: continue
        seen.add(o['key'])
        print('   V2 %s %s/%s pol=%s rel=%s: %s' % (o['key'], o['classification'], o['modality'], o['policies'], o['related'], o['claim'][:200]))
    for p in x['pass1_same_place']:
        print('   P1 %s %s: %s' % (p['claim_id'], p['disposition'], p['claim'][:140]))
