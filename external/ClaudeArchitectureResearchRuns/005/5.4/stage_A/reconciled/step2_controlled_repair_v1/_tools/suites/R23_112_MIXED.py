"""R23 regression: item 11.2 cross-method adjudication."""
from collections import Counter

from rcommon import out_path, read_jsonl


def run(ctx):
    rows = read_jsonl(out_path('CROSS_METHOD_ADJUDICATION.jsonl'))
    kinds = Counter(r['kind'] for r in rows)
    ctx.check('five strength cells', kinds['STRENGTH_CELL'] == 5, kinds, kind='DATA')
    ctx.check('three qualified overrides', kinds['QUALIFIED_OVERRIDE'] == 3, kinds, kind='DATA')
    ctx.check('every qualified cell has a counterexample and competing readings', all(r['falsifying_counterexample'] and r['competing_interpretations'] for r in rows if r['kind'] in ('STRENGTH_CELL', 'QUALIFIED_OVERRIDE')), kind='SEMANTIC')
    ctx.check('no qualified cell turned into a parity statement', all(r['result'] == 'QUALIFIER_RETAINED' for r in rows if r['kind'] in ('STRENGTH_CELL', 'QUALIFIED_OVERRIDE')), kind='SEMANTIC')
    ctx.check('partial-witness cells are flagged, not adjudicated by count', all(r['result'].startswith('FLAG_RETAINED') for r in rows if r['kind'] == 'PARTIAL_WITNESS_ONLY'), 'n=%d' % kinds['PARTIAL_WITNESS_ONLY'], kind='SEMANTIC')
    ctx.check('no qualified witness was changed by a template rule', all(r['witnesses_on_current_bytes']['changed_refs'] == 0 for r in rows if r['kind'] in ('STRENGTH_CELL', 'QUALIFIED_OVERRIDE')), kind='DATA')
