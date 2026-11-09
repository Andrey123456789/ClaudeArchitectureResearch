import re
from rcommon import CANDIDATES, norm_ws, out_path, read_jsonl, read_lines, utf8_stdout, wc_path, walk_files, template_root
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
pat=re.compile(r'frontend tests under|under `?backend/?`?|tests? .{0,40}under backend|never under backend',re.I)
for c in CANDIDATES:
    print('=====',c,'source lines')
    for rel in walk_files(template_root(c)):
        if not rel.endswith('.md'): continue
        for i,l in enumerate(read_lines(wc_path(c,rel)),1):
            if re.search(r'frontend tests under',norm_ws(l),re.I) or (re.search(r'under `?backend',l,re.I) and re.search(r'frontend',l,re.I) and re.search(r'never|do not',l,re.I)):
                m=re.search(r'[^.]*(frontend tests under|under `?backend)[^.]*\.',norm_ws(l),re.I)
                print('  ',rel,i,'|',(m.group(0) if m else norm_ws(l))[:170])
    print('  records:')
    for r in rows:
        if r['candidate']!=c or not r['repair']['active']: continue
        t=r.get('claim_text') or ''
        if pat.search(t):
            subs=[(s.get('classification'),s.get('modality'),(s.get('claim_text') or s.get('text') or '')[:80]) for s in r.get('subclauses') or []]
            print('  ',r['source_key'],r['classification'],r.get('modality'),r.get('strength_vs_canonical'),[x['policy_id']+':'+x['coverage'][0] for x in r.get('canonical_coverage') or []],'|',t[:190],'|',subs if subs else '')
