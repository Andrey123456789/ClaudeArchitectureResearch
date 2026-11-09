"""Writes the C07 outputs from reviewed rows and the current view: BLIND_REREAD_ADJUDICATION.jsonl, BLIND_REREAD_SUMMARY.md, MARKED_NEVER_SOFT_MODALITY.jsonl, CORRECTIONS_REASSESSED.jsonl, EXTRAS_RECONCILIATION.md. Counts are recomputed, not typed. Candidate files are not touched."""
import importlib.util
import re
from collections import Counter

import claimgate
import dataset
from rcommon import CANDIDATES, norm_ws, out_path, read_json, read_jsonl, sha256_file, utf8_stdout, write_jsonl, write_text

RULE = 'C07-PARITY-CLOSE'
MARKED = re.compile(r'\b(never|must not)\b', re.I)
SOFT = ('DEFAULT', 'SHOULD', 'SHOULD_NOT', 'MAY')
# Each 103 correction or original open record a v2 change touched, read against the current record. The build fails if the computed overlap differs.
REASSESS = {
    'COR-A-K1-0001': 'C06 changed only the review flag. The accepted classification and fields stand.',
    'COR-A-M1-0001': 'C06 changed only the review flag. The accepted classification and fields stand.',
    'COR-A-L0-0001': 'C06 changed only the review flag. The accepted classification and fields stand.',
    'COR-A-L1-0001': 'C06 changed only the review flag. The accepted classification and fields stand.',
    'COR-A-L0-0013': 'ACCEPT stands: C07-D8 adds only the out-of-evaluation label. R25 corrected this record, and R19\'s overlay did not list it, which is why v1 left it unlabelled.',
    'COR-A-K0-0024': 'REJECT stands, and C01 strengthens its reason: the checker reads the effective value, now by MSBuild evaluation in all six.',
    'FG-K0-0ef1e5ed3d': 'Closed by C05 under register 9.2 as an audit criterion. C07 adds a qualifier only.',
    'FG-K0-6d06b21a93': 'Closed by C05 under register 9.2 as an audit criterion. C07 adds a qualifier only.',
}


def load(name):
    spec = importlib.util.spec_from_file_location('c07b_' + name, out_path('_rules', RULE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def marked_soft(rows):
    return [r for r in rows if r['repair']['active'] and r.get('modality') in SOFT and r['classification'] != 'NON_NORMATIVE' and MARKED.search(r.get('claim_text') or '')]


def read_earlier():
    out = set()
    for f in ('PI012_79_REVIEW.jsonl', 'PI012_230_REVIEW.jsonl', 'PI012_EXTENSION_REVIEW.jsonl', 'PI012_EXTRA_21_REVIEW.jsonl'):
        out |= {x['key'].split('/')[0] for x in read_jsonl(out_path(f))}
    return out | {x['case_key'].split('/')[0] for x in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))}


def class_rows(rows):
    earlier = read_earlier()
    bans = [r for r in rows if r['repair']['active'] and r.get('modality') == 'MUST_NOT' and MARKED.search(r.get('claim_text') or '')]
    out = []
    for r in marked_soft(rows):
        pols = {x['policy_id'] for x in r.get('canonical_coverage') or []}
        sib = [b['source_key'] for b in bans if b['candidate'] != r['candidate'] and pols & {x['policy_id'] for x in b.get('canonical_coverage') or []}]
        m = MARKED.search(r['claim_text'])
        out.append({'key': r['source_key'], 'candidate': r['candidate'], 'classification': r['classification'], 'modality': r['modality'], 'clause': norm_ws(r['claim_text'][max(0, m.start() - 70):m.end() + 70]), 'delivery_context': r.get('delivery_context'), 'read_earlier': r['source_key'] in earlier, 'n_other_candidate_bans_on_same_policy': len(sib), 'status': 'NOT_VERIFIED', 'status_note': 'Listed by a word match on the claim text, and not read one by one in this run. The match cannot tell a marked ban from a description such as "never verifies".'})
    return out


def sensitivity(rows):
    """What a stored MUST_NOT on every listed record would change. Coverage status does not read modality, so a zero there says nothing by itself; the number that could matter is the strength facts that would need a resolution."""
    state = {c: {r['source_key']: r for r in rows if r['candidate'] == c} for c in CANDIDATES}
    base = claimgate.cells(state)
    need = []
    for r in marked_soft(rows):
        after = dataset.apply_v2_set(r, {'modality': 'MUST_NOT'})
        state[r['candidate']][r['source_key']] = after
        if after.get('strength_vs_canonical') == 'SAME' and after.get('strength_mechanical_mismatch') and not after.get('strength_resolution'):
            need.append(r['source_key'])
    cur = claimgate.cells(state)
    return {'cells_moved': sum(1 for k in cur if cur[k] != base[k]), 'would_need_resolution': len(need), 'must_not_now': dict(Counter(r['candidate'] for r in rows if r['repair']['active'] and r.get('modality') == 'MUST_NOT')), 'listed': dict(Counter(r['candidate'] for r in marked_soft(rows)))}


def reassessed(rows):
    by = {r['source_key']: r for r in rows}
    touched = {k for k, r in by.items() if any(x[:2] == 'C0' for x in r['repair']['rules'])}
    out = []
    for a in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl')):
        base = a['case_key'].split('/')[0]
        if base in touched:
            out.append({'id': a['correction_id'], 'set': '103', 'key': a['case_key'], 'decision': a['decision'], 'v2_changes': [x for x in by[base]['repair']['rules'] if x[:2] == 'C0'], 'reading': REASSESS[a['correction_id']]})
    for u in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')):
        if u['kind'] == 'ORIGINAL_OPEN_RECORD' and u['id'].split('/')[0] in touched:
            out.append({'id': u['id'], 'set': '31', 'key': u['id'], 'decision': u['status'], 'v2_changes': [x for x in by[u['id'].split('/')[0]]['repair']['rules'] if x[:2] == 'C0'], 'reading': REASSESS[u['id']]})
    return out


def main():
    utf8_stdout()
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    sample = read_jsonl(out_path('BLIND_REREAD_SAMPLE.jsonl'))
    adj = load('blind_adjudication').ROWS
    dis = [x for x in sample if not (x['group_agrees'] and x['force_agrees'])]
    write_jsonl('BLIND_REREAD_ADJUDICATION.jsonl', [dict(id=x['id'], candidate=x['candidate'], key=x['key'], stored_at_reading=[x['stored_classification'], x['stored_modality']], read=[x['read_group'], x['read_force']], group_agrees=x['group_agrees'], force_agrees=x['force_agrees'], **adj[x['id']]) for x in dis])
    results = Counter(adj[x['id']]['result'] for x in dis)
    plan = read_json(out_path('_rules', RULE, 'BLIND_PLAN.json'))
    cls = class_rows(rows)
    write_jsonl('MARKED_NEVER_SOFT_MODALITY.jsonl', cls)
    sen = sensitivity(rows)
    write_jsonl('CORRECTIONS_REASSESSED.jsonl', reassessed(rows))
    t = ['# Blind reread\n', '## Design\n', 'A seeded stratified draw (seed %d): 2 records per label group per candidate, %d in all, from records no earlier review read. The groups are equal-sized, so these counts cannot be scaled to a population rate.\n' % (plan['seed'], plan['n']), 'The first draw listed records in stratum order, and the reader knew that order, so a record\'s position gave away its stored group. It was viewed but not read. It is kept as `_rules/C07-PARITY-CLOSE/BLIND_PLAN_BURNED.json`, and its records were excluded from this shuffled draw.\n', 'The reader is the same model family that wrote the labels, and it sees the claim text, so this is a weak check. The reading was written and hashed before the comparison (`%s`). The hash proves the order of writing, not freedom from prior belief.\n' % sha256_file(out_path('_rules', RULE, 'BLIND_READING.txt')), '## Result\n', '| Outcome | Records |', '|---|---:|', '| Agreed on group and force | %d |' % (len(sample) - len(dis)), '| Disagreed on group only | %d |' % sum(1 for x in dis if x['force_agrees']), '| Disagreed on group and force | %d |' % sum(1 for x in dis if not x['force_agrees']), '']
    t += ['Each disagreement was read at source with the stored fields and the policy text (`BLIND_REREAD_ADJUDICATION.jsonl`):\n', '| Result | Records |', '|---|---:|'] + ['| %s | %d |' % kv for kv in sorted(results.items())] + ['']
    t += ['Most group disagreements are limits of the reading: the reader did not have the policy text, so it could not tell `CANONICAL_ONLY` from `CANONICAL_PLUS_DELTA`, or see that no policy covered a line.\n', '## What it found\n', 'The same marked ban, "Never place frontend tests under `backend/`", was stored as `MUST_NOT` in M1, L1 and K0 and as `DEFAULT` in L0 and K1, with no text difference behind it. No coverage cell shows this. `C07-N1` to `C07-N3` correct the three records. M has no such ban: its text only says the workspace holds its tests, and that real difference stays.\n', '## An open class it points to\n', '`MARKED_NEVER_SOFT_MODALITY.jsonl` lists %d active normative records whose claim says "never" or "must not" while their modality is a soft one. They were found by a word match and were not read one by one. Many are compounds such as "positive step; never X", and some are descriptions such as "never verifies". They stay as stored, with status `NOT_VERIFIED`. The contract asks for no sweep of this class, and relabeling by word match would be the mechanical closing it forbids.\n' % len(cls)]
    t += ['If all were stored as `MUST_NOT`:\n', '| Candidate | `MUST_NOT` now | Listed |', '|---|---:|---:|'] + ['| %s | %d | %d |' % (c, sen['must_not_now'].get(c, 0), sen['listed'].get(c, 0)) for c in CANDIDATES] + ['', '- Coverage or strength cells moved: %d. Coverage does not read modality, so this zero is true by construction and is not evidence of agreement.' % sen['cells_moved'], '- Records that would read `SAME` with a modality above the policy and no resolution code: %d.\n' % sen['would_need_resolution'], '**Consequence for Step 3:** do not use raw `MUST_NOT` counts as a strictness measure between candidates. Label counts carry this noise. Coverage and strength cells do not depend on it.\n']
    write_text('BLIND_REREAD_SUMMARY.md', '\n'.join(t))
    e = ['# Extras reconciled\n', 'The three extras from v1 report section 6, checked on current v2 bytes by the C07 suite.\n', '## `R13-TEST-PRIORITY`: `NO_CHANGE_VERIFIED`\n', 'The prioritize sentence appears in M, K0 and K1. `TST-011` holds in all six through the "low-value tests" line of their testing rules. The sentence adds no obligation the other three lack, so no text changes, as kit 62 item 8.7 directs.\n', '## `R19-CI-RULE-SPREAD`: `NO_CHANGE_VERIFIED`\n', 'The CI dependency update rule stays in all six, as kit 62 item 8.7 directs. CI/CD stays out of practical benchmarks. No text changes. One data fix: the v1 report says the rule is labelled out of practical evaluation in all six, but L0\'s record `FG-L0-29a3230807` had no label. `C07-D8` adds it.\n', '## `R20-DESER-FORMS`: qualifier added, modality unchanged\n', 'All six lines sit in the private scan layer of `security-scan`, and no candidate states the prohibition in a rule file or `CLAUDE.md`. M, M1, L0 and K1 mark it, K0 is an audit criterion, and L1 is a list item. `comparison_qualifier` on each record says this is not a strictness fact. No condition was added to the applicability field: the lines state none, and a scan is how they are delivered, not when they apply.\n']
    write_text('EXTRAS_RECONCILIATION.md', '\n'.join(e))
    print('adjudicated', dict(results), 'class', len(cls), 'sensitivity', {k: sen[k] for k in ('cells_moved', 'would_need_resolution')}, 'reassessed', len(reassessed(rows)))


if __name__ == '__main__':
    main()
