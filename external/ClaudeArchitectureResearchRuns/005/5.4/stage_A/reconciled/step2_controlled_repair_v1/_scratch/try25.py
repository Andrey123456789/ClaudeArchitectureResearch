import importlib.util,sys,json
from collections import Counter
from suitelib import Ctx
from rcommon import utf8_stdout
utf8_stdout()
name=sys.argv[1]
spec=importlib.util.spec_from_file_location('s',sys.argv[2]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ctx=Ctx(name)
m.run(ctx)
print(Counter(x['status'] for x in ctx.rows))
for x in ctx.rows:
    if x['status']!='PASS': print(x['status'],x['test'],x.get('candidate'),str(x.get('detail'))[:400])
