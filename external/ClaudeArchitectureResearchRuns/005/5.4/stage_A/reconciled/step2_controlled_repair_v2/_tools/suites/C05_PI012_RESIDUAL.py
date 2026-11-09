"""C05 regression: the two K0 scan records and the 21 triggered leads. Data only. Includes mutations that show the checks catch a forced close and a forced relabel."""
import copy
import os
from collections import Counter

import claimgate
import dataset
from order import V2_ORDER
from pi012_scan import scan
from rcommon import CANDIDATES, input_path, norm_ws, out_path, read_jsonl, read_lines, v1_path, wc_path
from roverlay import validate_candidate

K0_KEYS = ('FG-K0-0ef1e5ed3d', 'FG-K0-6d06b21a93')


def readings(rec):
    out = {'': rec.get('strength_resolution')}
    for s in list(rec.get('subclauses') or []) + list(rec.get('audit_subclauses') or []):
        out[s.get('subclause_id') or ''] = s.get('strength_resolution')
    return out


def run(ctx):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by = {r['source_key']: r for r in rows}
    v1 = {r['source_key']: r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    adj = read_jsonl(out_path('PI012_REMAINING_ADJUDICATION.jsonl'))
    ctx.check('four v1 rows over two unique K0 records are adjudicated', len(adj) == 4 and {a['key'] for a in adj} == set(K0_KEYS) and {a['list'] for a in adj} == {'PI012_79_REVIEW.jsonl', 'PI012_230_REVIEW.jsonl'}, kind='DATA', actual=len(adj))
    for k in K0_KEYS:
        r = by[k]
        ctx.check('%s: audit criterion, no canonical link, no strength fact' % k, r['classification'] == 'EXTRA_WORKFLOW' and r['modality'] == 'DEFAULT' and not r.get('canonical_coverage') and r.get('strength_vs_canonical') == 'N/A', r['classification'], 'K0', 'SEMANTIC')
        ctx.check('%s: no open question left, and the close is backed by an adjudication row' % k, not r['repair'].get('open_question') and any(a['key'] == k and a['result'] == 'RESOLVED' for a in adj), candidate='K0', kind='SEMANTIC')
        ctx.check('%s: original claim kept in the view' % k, r.get('claim_text_original') and 'not deserialized' in r['claim_text_original'], candidate='K0', kind='DATA')
    text = norm_ws(' '.join(read_lines(wc_path('K0', '.claude/skills/security-scan/references/scan-layers.md'))))
    ctx.check('K0 source context supports the reading: scan layer, Investigate lead, unmarked declarative', '## Unsafe deserialization Investigate polymorphic' in text and 'Untrusted payloads are not deserialized' in text, candidate='K0', kind='SOURCE')
    k0_rules = []
    for d, _, fs in os.walk(wc_path('K0', '.claude/rules')):
        for n in fs:
            with open(os.path.join(d, n), encoding='utf-8') as f:
                if 'deserializ' in f.read().lower():
                    k0_rules.append(n)
    ctx.check('no K0 rule owns a deserialization prohibition', not k0_rules, k0_rules, 'K0', 'SOURCE')
    # 21 leads
    res = scan()
    ctx.check('the scan reproduces v1: 22, 8, 21', {f: len(v) for f, v in res.items()} == {'do_not_unless': 22, 'only_when': 8, 'do_not_when': 21}, kind='DATA', actual={f: len(v) for f, v in res.items()})
    ex = read_jsonl(out_path('PI012_EXTRA_21_REVIEW.jsonl'))
    want = {x['key'] for x in res['do_not_when']}
    ctx.check('all 21 leads have a row', {x['key'] for x in ex} == want and len(ex) == 21, kind='DATA', actual=len(ex))
    need = ('source_quote', 'frozen_location', 'current_anchor', 'owner', 'applicability_condition', 'equivalent_affirmative', 'kind', 'modality_stored', 'decision', 'reading')
    ctx.check('each lead row has quote, location, owner, condition, affirmative form, modality, decision', all(x.get(f) for x in ex for f in need), kind='DATA')
    ctx.check('each kind is one of the distinguished kinds', all(x['kind'] in ('DESCRIPTIVE', 'NO_OBLIGATION', 'PREFERENCE', 'DEFAULT', 'CONDITIONAL_HARD', 'TRUE_BAN', 'AUDIT_RESTRAINT') for x in ex), Counter(x['kind'] for x in ex), kind='DATA')
    moved = [x['key'] for x in ex if by[x['key']].get('modality') != v1[x['key']].get('modality')]
    ctx.check('no lead changed modality by form alone: addendum A2 rule 3 stands, option D is not imposed', not moved, moved, kind='SEMANTIC')
    gone = [x['key'] for x in ex if norm_ws(x['source_quote'])[:90] not in norm_ws(' '.join(read_lines(input_path(x['candidate'], x['frozen_location'].split(':')[0]))))]
    ctx.check('each quote re-reads from the frozen input', not gone, gone[:5], kind='SOURCE')
    now_gone = [x['key'] for x in ex if norm_ws(x['source_quote'])[:90] not in norm_ws(' '.join(read_lines(wc_path(x['candidate'], x['frozen_location'].split(':')[0]))))]
    ctx.check('each quote stands in the current template', not now_gone, now_gone[:5], kind='SOURCE')
    missing = [x['key'] for x in ex if not by[x['key']].get('applicability_trigger') or by[x['key']].get('applicability_status') != 'STATED_REVIEWED']
    ctx.check('the condition read at source is in the derived applicability field', not missing, missing[:5], kind='DATA')
    orig = [x['key'] for x in ex if by[x['key']].get('trigger_field_original') != v1[x['key']].get('trigger_field_original')]
    ctx.check('the original trigger field is untouched', not orig, orig[:5], kind='DATA')
    ctx.check('the lost condition is restored in FG-K1-d8c34708a7, and the original claim is kept', 'when normal composition is simpler' in by['FG-K1-d8c34708a7']['claim_text'] and by['FG-K1-d8c34708a7']['claim_text_original'] == 'No Scrutor for a single decoration.', candidate='K1', kind='SEMANTIC')
    # A v2 update changes a stored strength reading only when it names the resolution code.
    named = set()
    for rule in V2_ORDER:
        if os.path.exists(out_path('_rules', rule, 'updates.py')):
            for key, e in getattr(dataset.load_py(rule, 'updates.py'), 'UPDATES', {}).items():
                if 'strength_resolution_code' in (e.get('set') or {}) or any('strength_resolution_code' in f for f in (e.get('sub') or {}).values()):
                    named.add(key.split('/')[0])
    silent = [k for k, r in v1.items() if k in by and k not in named and readings(r) != readings(by[k])]
    ctx.check('no v2 update changed a stored strength reading, or its source, without naming the code', not silent, silent[:6], kind='DATA', actual=len(silent))
    ctx.check('FG-M-290b3bdb9e keeps its frozen SL reading with its source', (by['FG-M-290b3bdb9e'].get('strength_resolution') or {}).get('source') == 'STRENGTH.dec:44', by['FG-M-290b3bdb9e'].get('strength_resolution'), 'M', 'DATA')
    stored = {'classification': 'CANONICAL_ONLY', 'modality': 'MUST_NOT', 'strength_vs_canonical': 'SAME', 'canonical_coverage': [{'policy_id': 'API-012', 'coverage': 'FULL'}], 'strength_resolution': {'code': 'SL', 'label': 'SECONDARY_LINK_ONLY', 'note': 'n', 'source': 'STRENGTH.dec:44'}}
    ctx.check('update path: an annotation keeps a stored reading with its source', dataset.apply_v2_set(stored, {'pi012_form': 'X'})['strength_resolution'] == stored['strength_resolution'], kind='LOGIC')
    ctx.check('update path: naming the code as empty clears the reading', dataset.apply_v2_set(stored, {'modality': 'MUST', 'strength_resolution_code': None})['strength_resolution'] is None, kind='LOGIC')
    ctx.check('update path: naming a code sets it', dataset.apply_v2_set(stored, {'strength_resolution_code': 'AM'})['strength_resolution']['code'] == 'AM', kind='LOGIC')
    ctx.check('mutation: the v1 path loses the reading, which is why v2 updates do not use it', dataset.apply_set(stored, {'pi012_form': 'X'})['strength_resolution'] is None, kind='MUTATION')
    ctx.check('mutation: the per-claim gate catches a field a disposition did not declare', claimgate.undeclared(by['FG-M-290b3bdb9e'], dataset.apply_set(by['FG-M-290b3bdb9e'], {'pi012_form': 'X'}), {'pi012_form'}) == ['strength_resolution'], kind='MUTATION')
    # Mutations
    m = copy.deepcopy(by['FG-K0-0ef1e5ed3d'])
    m['strength_vs_canonical'] = 'SAME'
    m['classification'] = 'CANONICAL_ONLY'
    state = {k: r for k, r in by.items() if r['candidate'] == 'K0' and r['repair']['active']}
    state['FG-K0-0ef1e5ed3d'] = m
    ctx.check('mutation: a scan criterion given a canonical label with no policy is caught', any('no policy' in e for e in validate_candidate('K0', state, allow_added=True, removed=[k for k, r in by.items() if r['candidate'] == 'K0' and not r['repair']['active']])), candidate='K0', kind='MUTATION')
    saved = dataset.resolved_open_keys
    dataset.resolved_open_keys = lambda: set()
    try:
        r1, _ = dataset.build()
    finally:
        dataset.resolved_open_keys = saved
    reopened = {r['source_key']: r for r in r1['K0']}
    ctx.check('mutation: with no adjudication row the record reads open again', all(reopened[k]['repair'].get('open_question') for k in K0_KEYS), kind='MUTATION')
    ctx.not_run('a blind second reader for these 23 records', 'one model in one session; a fresh-session or human reader is the next step')
