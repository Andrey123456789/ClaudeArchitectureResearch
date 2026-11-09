"""V3-D02 regression: the 86 v2 records with "never"/"must not" at a soft modality were each read at source; one proved error corrected,
one qualified, 84 upheld with a reason code. Data only."""
import copy
from collections import Counter

import m86_build
from rcommon import CANDIDATES, norm_ws, out_path, read_jsonl, read_lines, v2_path, wc_path

RULE = 'V3-D02-MODALITY86'


def cells(path):
    return {(x['candidate'], x['policy_id']): (x['status'], x['strength_status']) for x in read_jsonl(path)}


def run(ctx):
    rows, m = m86_build.rows()
    stored = read_jsonl(out_path('MARKED_NEVER_86_REVIEW.jsonl'))
    ctx.check('the review file is the one built from the written review', stored == rows, kind='DATA', actual=len(stored))
    cls = read_jsonl(v2_path('MARKED_NEVER_SOFT_MODALITY.jsonl'))
    ctx.check('every one of the 86 v2 records has one review row', sorted(x['key'] for x in rows) == sorted(x['key'] for x in cls) and len(rows) == 86, kind='DATA', actual=len(rows))
    res = Counter(x['result'] for x in rows)
    ctx.check('results: 1 corrected, 1 qualified, 84 upheld', res == Counter({'UPHELD': 84, 'CORRECTED': 1, 'QUALIFIED': 1}), dict(res), kind='SEMANTIC', actual=dict(res))
    ctx.check('every row has a reason code and a source reading', all(x['reason_code'] and x['reading'].strip() for x in rows), kind='SEMANTIC')
    for x in rows:
        if x['result'] == 'CORRECTED':
            ctx.check('corrected record now MUST_NOT: %s' % x['key'], x['modality_v3'] == 'MUST_NOT' and x['modality_v2'] != 'MUST_NOT', (x['modality_v2'], x['modality_v3']), x['candidate'], 'DATA')
        else:
            ctx.check('upheld or qualified record keeps its v2 modality: %s' % x['key'], x['modality_v3'] == x['modality_v2'], (x['modality_v2'], x['modality_v3']), x['candidate'], 'DATA')
    view = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    r = view['FG-M-8b2c02178e']
    ctx.check('the correction keeps classification, FE-001 link and STRONGER equivalence', r['classification'] == 'CANONICAL_PLUS_DELTA' and [x['policy_id'] for x in r['canonical_coverage']] == ['FE-001'] and r['normative_strength_equivalence'] == 'STRONGER_THAN_CANONICAL', candidate='M', kind='DATA')
    ctx.check('the corrected ban still stands in the source', 'do not introduce ngmodules for ordinary feature development unless an integration or legacy dependency genuinely requires them' in norm_ws(' '.join(read_lines(wc_path('M', '.claude/rules/angular.md')))).lower(), candidate='M', kind='SOURCE')
    ctx.check('M1 stores the same ban MUST_NOT (the peer the correction follows)', view['FG-M1-044b0b5804']['modality'] == 'MUST_NOT', candidate='M1', kind='DATA')
    now, v2 = cells(out_path('REPAIRED_POLICY_COVERAGE.jsonl')), cells(v2_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    moved = sorted(k for k in v2 if now.get(k) != v2[k])
    ctx.check('no coverage or strength cell moved against v2 (1,176)', not moved and len(now) == 1176, moved[:6], kind='DATA', actual=len(now))
    # Mutations.
    mut = copy.deepcopy(rows)
    mut.pop(0)
    ctx.check('mutation: a dropped review row is caught', sorted(x['key'] for x in mut) != sorted(x['key'] for x in cls), kind='MUTATION')
    mut = copy.deepcopy(rows)
    up = next(x for x in mut if x['result'] == 'UPHELD')
    up['modality_v3'] = 'MUST_NOT'
    ctx.check('mutation: an upheld record whose modality moved is caught', up['modality_v3'] != up['modality_v2'], kind='MUTATION')
    ctx.not_run('a fresh-session or human reader of the 86 readings', 'one model family read and decided; the readings are in the file for that reader')
