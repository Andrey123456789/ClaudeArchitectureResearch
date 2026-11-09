"""C07 regression: the three extras, the corrected ban, recomputed counts, nothing widened, and the blind reread's own integrity. Data only. No live agent ran."""
import copy
import importlib.util
import os
import re

import c07_build
import claimgate
import dataset
from rcommon import CANDIDATES, out_path, policies, read_json, read_jsonl, read_lines, sha256_file, template_root, v1_path, v2_path, walk_files, wc_path
from suitelib import has

RULE = 'C07-PARITY-CLOSE'
SCAN = 'skills/security-scan/references/scan-layers.md'
LAYOUT = '.claude/skills/project-structure/references/solution-layout.md'
QUALIFIED = ('FG-M-bea4987bb6', 'FG-M1-c6cfdc9dbf', 'FG-L0-009161dd35', 'FG-L1-d6ab123b1f', 'FG-K0-0ef1e5ed3d', 'FG-K0-6d06b21a93', 'FG-K1-112617f8b3')
CORRECTED = ('FG-L0-a2e9e91e8f', 'FG-K1-4767fd97b1', 'FG-K1-bc831815a3')
BAN = {'M': ('.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`', 'V3A-M-030'), 'M1': (LAYOUT, 'Do not place frontend tests under `backend/`', 'FG-M1-9030e201b9'), 'L0': ('.claude/rules/3-project/layout.md', 'Never place frontend tests under `backend/`', 'FG-L0-a2e9e91e8f'), 'L1': (LAYOUT, 'never under `backend/`', 'FG-L1-75964b0d7f'), 'K0': (LAYOUT, 'Angular tests never go under `backend/`', 'FG-K0-40e6fc8d29'), 'K1': (LAYOUT, 'Never place frontend tests under `backend/`', 'FG-K1-4767fd97b1')}
WIDEN = re.compile(r'dotnet ef database update|apply (the |all )?(pending )?migrations? (locally|to the local)', re.I)
TEXT = ('.md', '.mjs', '.cjs', '.js', '.json')


def modality_moved(by, v1, keys):
    return [k for k in keys if by[k].get('modality') != v1[k].get('modality') or by[k].get('classification') != v1[k].get('classification')]


def unlabelled(by, keys):
    return [k for k in keys if by[k].get('evaluation_scope') != 'OUT_OF_PRACTICAL_EVALUATION_CI']


def has_full_link(rec, pid):
    return any(x['policy_id'] == pid and x['coverage'] == 'FULL' for o in [rec] + list(rec.get('subclauses') or []) + list(rec.get('audit_subclauses') or []) for x in o.get('canonical_coverage') or [])


def extras(ctx, by, v1):
    # R13
    spec = importlib.util.spec_from_file_location('r13_c07', out_path('_rules', 'R13-87-TESTPRIORITY', 'review.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for row in m.REVIEW:
        for rel, q in row['quotes']:
            ctx.check('R13: the source line still stands', has(row['candidate'], rel, q), q[:60], row['candidate'], 'SOURCE')
    for c in ('M1', 'L0', 'L1'):
        ctx.check('R13: no prioritize sentence here, and TST-011 holds through the testing rule', not has(c, '.claude/skills/dotnet-testing/SKILL.md', 'prioritize meaningful'), candidate=c, kind='SOURCE')
    cov = {(x['candidate'], x['policy_id']): x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    ctx.check('R13: TST-011 has a direct witness in all six', all(cov[(c, 'TST-011')]['direct_source_keys'] for c in CANDIDATES), kind='DATA')
    # R19
    ov = dataset.load_py('R19-87-CIUPDATES', 'overlay.py').OVERLAY
    labelled = [o['key'].split('/')[0] for o in ov] + ['FG-L0-29a3230807']
    ctx.check('R19: every CI update record carries the out-of-evaluation label', not unlabelled(by, labelled), unlabelled(by, labelled), kind='DATA')
    ctx.check('R19: each of the six has a labelled record', {by[k]['candidate'] for k in labelled} == set(CANDIDATES), sorted({by[k]['candidate'] for k in labelled}), kind='DATA')
    mut = copy.deepcopy(by['FG-L0-29a3230807'])
    mut['evaluation_scope'] = None
    ctx.check('mutation: a dropped CI label is caught', unlabelled({'FG-L0-29a3230807': mut}, ['FG-L0-29a3230807']) == ['FG-L0-29a3230807'], kind='MUTATION')
    # R20
    for c in CANDIDATES:
        root = template_root(c)
        stray = []
        for rel in walk_files(root):
            if rel.endswith(SCAN) or not rel.endswith(TEXT):
                continue
            text = ' '.join(read_lines(wc_path(c, rel)))
            if re.search(r'BinaryFormatter|TypeNameHandling|arbitrary runtime types', text) or ((rel == 'CLAUDE.md' or rel.startswith('.claude/rules/')) and re.search(r'deserializ', text, re.I)):
                stray.append(rel)
        ctx.check('R20: no prohibition outside the scan layer', not stray, stray[:4], c, 'SOURCE')
    ctx.check('R20: all seven records carry the qualifier', all('not a strictness fact' in (by[k].get('comparison_qualifier') or '') for k in QUALIFIED), kind='DATA')
    ctx.check('R20: the qualifier moved no modality or classification', not modality_moved(by, v1, QUALIFIED[:4] + QUALIFIED[6:]), kind='SEMANTIC')
    ctx.check('R20: the qualifier invented no condition on the lines that state none', all(not by[k].get('applicability_trigger') for k in ('FG-M-bea4987bb6', 'FG-M1-c6cfdc9dbf', 'FG-L0-009161dd35', 'FG-K1-112617f8b3')), kind='SEMANTIC')
    mut = {k: copy.deepcopy(by[k]) for k in QUALIFIED[:1]}
    mut['FG-M-bea4987bb6']['modality'] = 'DEFAULT'
    ctx.check('mutation: a qualifier that moves a modality is caught', modality_moved(mut, v1, QUALIFIED[:1]) == ['FG-M-bea4987bb6'], kind='MUTATION')


def ban(ctx, by, v1):
    for c, (rel, phrase, key) in BAN.items():
        ctx.check('the marked ban stands in the source', has(c, rel, phrase), phrase, c, 'SOURCE')
        ctx.check('the same marked ban is stored as MUST_NOT', by[key]['modality'] == 'MUST_NOT', by[key]['modality'], c, 'DATA')
    # v3 PV2-04 (approved) adds the M ban; M is now in BAN above and checked like the other five. v2 asserted its absence here.
    ctx.check('M states the ban in its placement owner (v3 PV2-04)', has('M', '.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`') and by.get('V3A-M-030', {}).get('modality') == 'MUST_NOT', candidate='M', kind='SOURCE')
    for k in CORRECTED:
        r = by[k]
        ctx.check('%s: corrected from DEFAULT, with a resolution code for the mismatch' % k, v1[k]['modality'] == 'DEFAULT' and r['strength_vs_canonical'] == 'SAME' and r['strength_mechanical_mismatch'] and (r.get('strength_resolution') or {}).get('code') in ('SL', 'PC'), r.get('strength_resolution'), r['candidate'], 'DATA')
        ctx.check('%s: the claim text did not change' % k, r['claim_text'] == v1[k]['claim_text'], candidate=r['candidate'], kind='DATA')
    cov = {(x['candidate'], x['policy_id']): x for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    cov1 = {(x['candidate'], x['policy_id']): x for x in read_jsonl(v1_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    ctx.check('DEP-024 keeps its status and strength cell in all six', all((cov[(c, 'DEP-024')]['strength_status'], cov[(c, 'DEP-024')]['direct_source_keys']) == (cov1[(c, 'DEP-024')]['strength_status'], cov1[(c, 'DEP-024')]['direct_source_keys']) for c in CANDIDATES), kind='DATA')
    rec = by['FG-L0-a2e9e91e8f']
    ctx.check('per-claim gate: a declared modality may move only what derives from it', claimgate.undeclared(v1['FG-L0-a2e9e91e8f'], dataset.apply_v2_set(v1['FG-L0-a2e9e91e8f'], {'modality': 'MUST_NOT'}), {'modality'}) == [], kind='LOGIC')
    ctx.check('mutation: the per-claim gate catches any other field moved with a modality', claimgate.undeclared(rec, dict(rec, domain='X'), {'modality'}) == ['domain'], kind='MUTATION')


def counts(ctx, rows, by):
    m = read_json(out_path('DATASET_MANIFEST.json'))['counts']
    want ={'repaired_rows': len(rows), 'active_rows': sum(1 for r in rows if r['repair']['active']), 'inactive_removed_rows': sum(1 for r in rows if not r['repair']['active']), 'added_claims': sum(1 for r in rows if str(r.get('view_record_type') or '').startswith('REPAIR') and not r['source_key'].startswith('NCP-')), 'proposed_clauses': sum(1 for r in rows if r['source_key'].startswith('NCP-'))}
    off = {k: (m.get(k), v) for k, v in want.items() if m.get(k) != v}
    ctx.check('dataset counts in the manifest are the recomputed ones', not off, off, kind='DATA', actual=want)
    v1_rows = len(read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl')))
    ctx.check('the count was not assumed from v1', want['repaired_rows'] != v1_rows, kind='DATA', actual={'v1': v1_rows, 'v2': want['repaired_rows']})
    ctx.check('no strictness total in the manifest', not [k for k in m if 'strict' in k.lower()], kind='DOC')
    props = [r for r in rows if r['source_key'].startswith('NCP-')]
    ctx.check('the four proposals stay proposals: no canonical link, inventory still 196', len(props) == 4 and not [r for r in props if r.get('canonical_coverage')] and len(policies()) == 196, kind='SEMANTIC')
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    ctx.check('196 x 6 cells', len(cov) == 1176, kind='DATA', actual=len(cov))
    weak = [(x['candidate'], x['policy_id'], k) for x in cov for k in x['direct_source_keys'] if not has_full_link(by[k], x['policy_id'])]
    ctx.check('a partial witness is never counted as direct', not weak, weak[:5], kind='SEMANTIC', actual=len(weak))
    widened = []
    for c in CANDIDATES:
        root = template_root(c)
        for rel in walk_files(root):
            if not rel.endswith(TEXT):
                continue
            old = v1_path('candidates', c, 'template', *rel.split('/'))
            before = set(read_lines(old)) if os.path.exists(old) else set()
            widened += ['%s %s: %s' % (c, rel, ln.strip()[:80]) for ln in read_lines(wc_path(c, rel)) if ln not in before and WIDEN.search(ln)]
    ctx.check('v2 added no local database migration duty in any candidate', not widened, widened[:4], kind='SEMANTIC')


def blind(ctx, rows):
    plan = read_json(out_path('_rules', RULE, 'BLIND_PLAN.json'))
    burned = read_json(out_path('_rules', RULE, 'BLIND_PLAN_BURNED.json'))
    ctx.check('the read draw is shuffled, unlike the burned one', [p['stratum'] for p in plan['plan']] != [p['stratum'] for p in burned['plan']], kind='DATA')
    ctx.check('no burned record is in the read draw', not {p['key'] for p in plan['plan']} & {p['key'] for p in burned['plan']}, kind='DATA')
    sample = read_jsonl(out_path('BLIND_REREAD_SAMPLE.jsonl'))
    h = sha256_file(out_path('_rules', RULE, 'BLIND_READING.txt'))
    with open(out_path('_rules', RULE, 'BLIND_READING.sha256'), encoding='utf-8') as f:
        stored = f.read().strip()
    ctx.check('the reading is the bytes hashed before the comparison', h == stored and all(x['reading_sha256'] == h for x in sample), kind='DATA')
    ctx.check('48 records, 2 per group per candidate', len(sample) == 48, kind='DATA', actual=len(sample))
    adj = read_jsonl(out_path('BLIND_REREAD_ADJUDICATION.jsonl'))
    dis = {x['id'] for x in sample if not (x['group_agrees'] and x['force_agrees'])}
    ctx.check('every disagreement was read at source, with a result and a reason', {x['id'] for x in adj} == dis and all(x['result'] in ('STORED_UPHELD', 'CORRECTED', 'QUALIFIED', 'UNRESOLVED') and x['why'] for x in adj), sorted(dis ^ {x['id'] for x in adj})[:5], kind='SEMANTIC', actual=len(adj))
    v2rows = read_jsonl(v2_path('REPAIRED_CLASSIFICATIONS.jsonl'))  # v3: the class file is v2's; recompute it on the view that produced it (later bans change derived counts)
    ctx.check('the listed class is the recomputed one (v2 view), with none of the corrected records in it', read_jsonl(out_path('MARKED_NEVER_SOFT_MODALITY.jsonl')) == c07_build.class_rows(v2rows) and not {x['key'] for x in c07_build.class_rows(v2rows)} & set(CORRECTED), kind='DATA', actual=len(c07_build.class_rows(v2rows)))
    rv = {x['key'] for x in read_jsonl(out_path('MARKED_NEVER_86_REVIEW.jsonl'))}
    ctx.check('v3: every record of the class was read at source (MARKED_NEVER_86_REVIEW.jsonl)', rv == {x['key'] for x in read_jsonl(out_path('MARKED_NEVER_SOFT_MODALITY.jsonl'))}, len(rv), kind='SEMANTIC')
    ctx.check('the class is not reported as read or cleared', all(x['status'] == 'NOT_VERIFIED' for x in read_jsonl(out_path('MARKED_NEVER_SOFT_MODALITY.jsonl'))), kind='SEMANTIC')
    ctx.check('the 103 and 31 overlap is the computed one, each row with a reading', read_jsonl(out_path('CORRECTIONS_REASSESSED.jsonl')) == c07_build.reassessed(rows), kind='DATA', actual=len(c07_build.reassessed(rows)))
    with open(out_path('EVIDENCE_LIMITS.md'), encoding='utf-8') as f:
        limits = f.read()
    ctx.check('the evidence limits have a v2 section naming the blind reread and the open class', '## v2' in limits and 'MARKED_NEVER_SOFT_MODALITY.jsonl' in limits, kind='DOC')
    for name in ('BLIND_REREAD_SUMMARY.md', 'EXTRAS_RECONCILIATION.md'):
        ctx.check('%s exists' % name, os.path.exists(out_path(name)), kind='DOC')


def run(ctx):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by = {r['source_key']: r for r in rows}
    v1 = {r['source_key']: r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    extras(ctx, by, v1)
    ban(ctx, by, v1)
    counts(ctx, rows, by)
    blind(ctx, rows)
    ctx.not_run('a fresh-session or human blind reader', 'one model in one session; the sample and the reading are there for that reader')
