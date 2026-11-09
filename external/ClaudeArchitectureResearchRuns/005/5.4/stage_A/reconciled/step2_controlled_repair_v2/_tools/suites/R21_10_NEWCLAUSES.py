"""R21 regression: item 10, four proposed clauses."""
from rcommon import out_path, policies, read_jsonl


def run(ctx):
    rows = read_jsonl(out_path('NEW_CLAUSES_4_ADJUDICATION.jsonl'))
    ctx.check('four rows', len(rows) == 4 and {r['proposal_id'] for r in rows} == {'NCP-M-0001', 'NCP-M1-0001', 'NCP-M1-0002', 'NCP-L0-0001'}, kind='DATA')
    ctx.check('every quote verified in the frozen input and found in the current copy', all(r['original_evidence']['verified_in_frozen_input'] and r['current_evidence']['status'] != 'NOT_FOUND' for r in rows), kind='DATA')
    ctx.check('no promotion to the canonical set', all(r['promotion'].startswith('NOT_PROMOTED') and r['proposal_id'] not in policies() for r in rows) and len(policies()) == 196, kind='SEMANTIC')
    ctx.check('no replication: only the candidates that hold the proposal', {r['candidate'] for r in rows} == {'M', 'M1', 'L0'}, kind='SEMANTIC')
