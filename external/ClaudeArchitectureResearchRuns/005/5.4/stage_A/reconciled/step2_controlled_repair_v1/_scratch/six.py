import re,sys
from rcommon import CANDIDATES, norm_ws, read_lines, utf8_stdout, walk_files, wc_path, template_root
utf8_stdout()
ANCH=[('GOV-015 authority', r'generic .?approved workflow.?, general task approval'),('TASK-START',r'Task-start check: before a task'),('RUN-021',r'Invalidating after commit is not by itself atomic'),('RUN-021 before',r'Invalidating before the mutation'),('DEP-003',r'\*\*Explicit exception'),('DEP-025',r'No confirmation, comment marker, or'),('GOV-017',r'implement a Reserved change only when the user explicitly approved'),('SWAGGER',r'API behavior change: when a change alters API behavior'),('CUSTOM',r'CUSTOM_SETTINGS\.md')]
which=sys.argv[1]
for name,pat in ANCH:
    if name!=which: continue
    for c in CANDIDATES:
        hits=[]
        for rel in walk_files(template_root(c)):
            if not rel.endswith('.md'): continue
            if which=='CUSTOM' and 'development-workflow' not in rel: continue
            ls=read_lines(wc_path(c,rel))
            text=' '.join(x.strip() for x in ls)
            for m in re.finditer(pat,text):
                hits.append((rel,text[max(0,m.start()-30):m.end()+460]))
        print('##',c,len(hits))
        for rel,t in hits[:2]:
            print('  ',rel,':',t)
