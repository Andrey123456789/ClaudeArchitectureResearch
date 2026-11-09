import json,os
from collections import Counter
from rcommon import AUD, CANDIDATES, baseline, out_path, read_jsonl, utf8_stdout
utf8_stdout()
uq = read_jsonl(os.path.join(AUD,'UNRESOLVED_QUEUE.jsonl'))
print(len(uq), uq[0].keys() if uq else None)
print(Counter(r.get('status') for r in uq))
print(json.dumps(uq[0],ensure_ascii=False)[:600])
led = read_jsonl(os.path.join(AUD,'AUDIT_LEDGER.jsonl'))
print(led[0].keys())
print(Counter(r.get('open') for r in led if 'open' in r))
op=[r for r in led if r.get('open') or r.get('resolution')=='OPEN' or r.get('status')=='OPEN']
print(len(op), [r.get('case_id') or r.get('key') for r in op][:40])
rep={r['source_key']:r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
base={k:r for c in CANDIDATES for k,r in baseline(c).items()}
print('baseline UNCERTAIN',[k for k,r in base.items() if r['classification']=='UNCERTAIN'])
print('still UNCERTAIN top',[k for k,r in rep.items() if r['classification']=='UNCERTAIN'])
print('still sub UNCERTAIN',[(k,s.get('subclause_id')) for k,r in rep.items() for s in r.get('subclauses') or [] if s.get('classification')=='UNCERTAIN'])
print('review_needed base',sum(1 for r in base.values() if r.get('review_needed')),'rep',sum(1 for r in rep.values() if r.get('review_needed')))
print('fhd base',sum(1 for r in base.values() if r.get('future_human_decision')),'rep',[k for k,r in rep.items() if r.get('future_human_decision')][:40])
