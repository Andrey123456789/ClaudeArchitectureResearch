"""Applied together with V3-D02 (not before): every record of the v2 class must have a v3 review row. The v2-view recompute of the class was
already applied at PV2-04 (see adaptations.py)."""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(BASE, '_tools', 'suites', 'C07_PARITY_CLOSE.py')
s = open(p, encoding='utf-8').read()
old = [l for l in s.split('\n') if l.startswith("    ctx.check('the listed class is the recomputed one (v2 view)")]
assert len(old) == 1
add = ("\n    rv = {x['key'] for x in read_jsonl(out_path('MARKED_NEVER_86_REVIEW.jsonl'))}"
       "\n    ctx.check('v3: every record of the class was read at source (MARKED_NEVER_86_REVIEW.jsonl)', rv == {x['key'] for x in read_jsonl(out_path('MARKED_NEVER_SOFT_MODALITY.jsonl'))}, len(rv), kind='SEMANTIC')")
s = s.replace(old[0], old[0] + add)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
p = os.path.join(BASE, '_tools', 'adaptations.py')
s = open(p, encoding='utf-8').read()
a = "(the new M DEP-024 ban counts for L0 and L1 class rows)."
assert s.count(a) == 1
s = s.replace(a, a + " V3-D02: every class record must also have a v3 review row (MARKED_NEVER_86_REVIEW.jsonl).")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('applied')
