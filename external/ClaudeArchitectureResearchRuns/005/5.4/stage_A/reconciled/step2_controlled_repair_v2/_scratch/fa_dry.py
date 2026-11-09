import sys
from collections import Counter
import final_audit_v2 as f
from rcommon import utf8_stdout
from sandbox import cleanup_runs
utf8_stdout()
a=f.Audit()
for name in sys.argv[1:]:
    fn=getattr(f,'sec_'+name)
    try:
        fn(a)
    except Exception as e:
        import traceback; traceback.print_exc(); a.row(name.upper(),'section crashed','FAIL',repr(e))
    print(name,Counter(r['status'] for r in a.rows),flush=True)
for r in a.rows:
    if r['status']=='FAIL': print('FAIL',r['section'],r['candidate'],r['test'][:120],'|',r['detail'][:420])
    if r['status']=='FINDING': print('FINDING',r['section'],r['test'][:200],'|',r['detail'][:500])
cleanup_runs()
