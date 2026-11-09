import sys
from gate import *
utf8_stdout()
rows=[]
for r in rules_upto(sys.argv[1]):
    rows.extend(load_review(r))
errs,ret=review_quotes(rows,superseded_quotes())
print('review rows',len(rows),'errs',len(errs),'retired',len(ret))
for e in errs: print(e[:260])
