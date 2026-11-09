import re
from collections import Counter
from dataset import load_py
from rcommon import CANDIDATES, baseline, out_path, read_jsonl, utf8_stdout
utf8_stdout()
rows=read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
print('labelled',Counter(r['candidate'] for r in rows if r.get('evaluation_scope')),Counter(r.get('evaluation_scope') for r in rows if r.get('evaluation_scope')))
ov=load_py('R19-87-CIUPDATES','overlay.py').OVERLAY
base={k:c for c in CANDIDATES for k in baseline(c)}
for o in ov: print(' overlay',base.get(o['key'].split('/')[0]),o['key'],'scope' if 'evaluation_scope' in o['set'] else 'no-scope',sorted(o['set'])[:5])
pat=re.compile(r'(upgrade|update).{0,30}(package|dependenc).{0,40}(CI|automatic)|automatic.{0,30}(package|dependency) update|(package|dependency).{0,30}(upgrade|update).{0,30}\bCI\b',re.I)
for r in rows:
    if r['repair']['active'] and pat.search(r.get('claim_text') or ''):
        print(' ',r['candidate'],r['source_key'],r['classification'],r.get('modality'),'scope=',r.get('evaluation_scope'),'|',r['claim_text'][:130])
