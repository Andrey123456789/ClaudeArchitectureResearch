"""One-off tool port for C05, applied only after C04's checkpoint. Each replacement must match exactly once, or the port stops."""
import os
import sys

T = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_tools'))


def edit(name, pairs):
    p = os.path.join(T, *name.split('/'))
    with open(p, encoding='utf-8') as f:
        s = f.read()
    for old, new in pairs:
        if s.count(old) != 1:
            sys.exit('no unique match in %s: %s' % (name, old[:120]))
        s = s.replace(old, new)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)


edit('dataset.py', [
    ('''def build(per_record=None):
    state = {c: dict(baseline(c)) for c in CANDIDATES}''', '''def resolved_open_keys():
    """Open PI-012 records a v2 adjudication closed. A record reopens if its adjudication row is removed."""
    return {r['key'] for r in read_jsonl(out_path('PI012_REMAINING_ADJUDICATION.jsonl')) if r.get('result') == 'RESOLVED'}


def build(per_record=None, skip=()):
    state = {c: dict(baseline(c)) for c in CANDIDATES}'''),
    ('''    for rule in V2_ORDER:
        if not os.path.exists(out_path('_rules', rule, 'updates.py')):
            continue''', '''    for rule in V2_ORDER:
        if rule in skip or not os.path.exists(out_path('_rules', rule, 'updates.py')):
            continue'''),
    ('''    open_keys = {r['id'].split('/')[0]: r['kind'] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r['status'] == 'OPEN'}
''', '''    closed = resolved_open_keys()
    open_keys = {r['id'].split('/')[0]: r['kind'] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r['status'] == 'OPEN' and r['id'].split('/')[0] not in closed}
'''),
])
edit('triggers.py', [
    ('''    flagged = reads_as_loading(trig, loading)
''', '''    if rec.get('applicability_override'):
        # A condition a reviewer read at source. The original trigger field stays as it is.
        out.update(applicability_trigger=rec['applicability_override'], applicability_status='STATED_REVIEWED')
        return out
    flagged = reads_as_loading(trig, loading)
'''),
])
edit('suites/R26_DATASET.py', [
    ('''    open_rows = {r['id'].split('/')[0] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r['status'] == 'OPEN'}
    ctx.check('PI-012 unresolved records stay marked open in the view', open_rows and all(trail[k]['repair'].get('open_question') for k in open_rows), sorted(open_rows), kind='SEMANTIC')
''', '''    open_rows = {r['id'].split('/')[0] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r['status'] == 'OPEN'} - dataset.resolved_open_keys()
    ctx.check('PI-012 unresolved records stay marked open in the view, unless a v2 adjudication row closed them', all(trail[k]['repair'].get('open_question') for k in open_rows), sorted(open_rows), kind='SEMANTIC')
'''),
])
edit('adaptations.py', [
    ('''    {'file': 'suites/R08_82_K0CPM.py', 'kind': 'TEST_UPDATED',''', '''    {'file': 'triggers.py', 'kind': 'PATH_PORT', 'change': 'C05-PI012-RESIDUAL', 'why': 'A condition a reviewer read at source now reaches applicability_trigger through a separate field, so the original trigger field stays untouched.'},
    {'file': 'suites/R26_DATASET.py', 'kind': 'TEST_UPDATED', 'change': 'C05-PI012-RESIDUAL', 'why': 'R26 required the K0 scan records to stay open, because at the end of v1 they were. Register 9.2 and the kit 71 C05 task close them when source context supports it, and it does. The test now subtracts only keys with an adjudication row; everything else still has to be open.', 'negative': 'C05 mutation "with no adjudication row the record reads open again", and C05 checks that the record has no canonical link and no strength fact.'},
    {'file': 'suites/R08_82_K0CPM.py', 'kind': 'TEST_UPDATED','''),
])
print('ported')
