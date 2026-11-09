"""Writes the C05 outputs from the reviewed rows: PI012_EXTRA_21_REVIEW.jsonl, PI012_REMAINING_ADJUDICATION.jsonl, PI012_SENSITIVITY_V2.md. Counts are recomputed from the current view, not typed."""
import importlib.util
from collections import Counter

from pi012_scan import scan
from rcommon import CANDIDATES, baseline, input_path, norm_ws, now, out_path, read_jsonl, read_lines, utf8_stdout, write_jsonl, write_text

RULE = 'C05-PI012-RESIDUAL'


def load(name):
    spec = importlib.util.spec_from_file_location('c05b_' + name, out_path('_rules', RULE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def current_anchor(rec):
    for e in rec.get('current_evidence_refs') or []:
        if e.get('start_line'):
            return {'path': e['path'], 'start_line': e['start_line'], 'end_line': e['end_line'], 'status': e['status']}
    return None


def main():
    utf8_stdout()
    rows = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    ex = load('extra21')
    sc = {x['key']: x for x in scan()['do_not_when']}
    out = []
    for row in ex.ROWS:
        x = sc[row['key']]
        rec = rows[row['key']]
        out.append({'key': row['key'], 'candidate': x['candidate'], 'source_quote': x['sentence'], 'frozen_location': '%s:%d-%d' % (x['path'], x['start_line'], x['end_line']), 'current_anchor': current_anchor(rec), 'owner': row['owner'], 'applicability_condition': row['condition'], 'equivalent_affirmative': row['affirmative'], 'kind': row['kind'], 'modality_stored': rec.get('modality'), 'classification': rec.get('classification'), 'decision': row['decision'], 'change': row.get('change'), 'reading': row['reading'], 'six_way_overlap': row['overlap'], 'alternative_reading': ex.ONLY_WHEN if rec.get('modality') == 'MUST_NOT' and row['kind'] != 'AUDIT_RESTRAINT' and row['key'] != 'FG-M1-14b23b94ae' else 'Not applicable to this form.', 'source_read_at': now()[:10]})
    write_jsonl('PI012_EXTRA_21_REVIEW.jsonl', out)
    un = read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
    k0line = norm_ws(' '.join(read_lines(input_path('K0', '.claude/skills/security-scan/references/scan-layers.md'))[74:77]))
    adj = []
    for r in un:
        if r['kind'] != 'PI012_UNRESOLVED':
            continue
        rec = rows[r['id']]
        adj.append({'key': r['id'], 'candidate': r['candidate'], 'list': r['list'], 'v1_status': r['status'], 'result': 'RESOLVED', 'resolved_as': 'AUDIT_CRITERION', 'authority': 'Register 9.2; HQ-06 in kit 72', 'source_context': k0line, 'current_anchor': current_anchor(rec), 'evidence': ['The line sits under the heading "Unsafe deserialization" in the security-scan layer file, a private reference of a workflow.', 'The sentence before it is an imperative to the scanner: "Investigate".', 'The sentence is an unmarked present-tense declarative, unlike the marked forms in M, M1, L0, K1.', 'No K0 rule file mentions deserialization (searched on current bytes). SEC-003 does not name it.'], 'modality_after': rec.get('modality'), 'classification_after': rec.get('classification'), 'strength_fact': 'None: no canonical link, strength_vs_canonical N/A. It does not count as MUST_NOT.', 'alternative_kept': 'Read as a product prohibition, K0 would match M, M1, L0, K1 in force. No source in K0 supports that reading, and the user decided against it without an owner. The risk stays registered through the scan layer itself.'})
    write_jsonl('PI012_REMAINING_ADJUDICATION.jsonl', adj)
    # Sensitivity on the current view.
    active = [r for r in rows.values() if r['repair']['active']]
    must_not = Counter(r['candidate'] for r in active if r.get('modality') == 'MUST_NOT')
    reviews = {}
    for f in ('PI012_79_REVIEW.jsonl', 'PI012_230_REVIEW.jsonl', 'PI012_EXTENSION_REVIEW.jsonl'):
        for r in read_jsonl(out_path(f)):
            reviews[r['key']] = r
    opt_d = Counter()
    for k, r in reviews.items():
        base = k.split('/')[0]
        if r['form'] == 'PERMISSION_CONDITION' and r['result'] == 'CORRECT' and base in rows and rows[base]['repair']['active'] and rows[base].get('modality') != 'MUST_NOT' and baseline(r['candidate']).get(base, {}).get('modality') == 'MUST_NOT' and '/' not in k:
            opt_d[r['candidate']] += 1
    trig_21 = Counter(x['candidate'] for x in out if x['modality_stored'] == 'MUST_NOT' and x['kind'] != 'AUDIT_RESTRAINT' and x['key'] != 'FG-M1-14b23b94ae')
    kinds = Counter(x['kind'] for x in out)
    t = ['# PI-012 sensitivity on the v2 view\n', 'Recomputed from `REPAIRED_CLASSIFICATIONS.jsonl`, the v1 review files and `PI012_EXTRA_21_REVIEW.jsonl`. Label and modality counts of active top-level records, not a strictness comparison. `PI012_SENSITIVITY.md` is v1\'s file, kept as written.\n', '## `R01-COMMON-VALUE`: the two readings of unmarked `only when` in knowledge text\n', '- **Approved addendum (kept):** `only when` and `do not ... unless` without `must` or `never` are `DEFAULT` in a knowledge skill. Consequence: an agent may deviate with a concrete, reported reason, as the vocabulary of each candidate says.', '- **Option D (shown, not imposed):** both forms stay binding. Consequence: the same lines become violations if not followed, including technique lines with no owner.', '\nNo source was found that contradicts the approved reading, so it stands. No coverage or strength cell moves under either reading.\n', '| Candidate | `MUST_NOT` now | Option D adds | Triggered forms reading `only when` would remove |', '|---|---:|---:|---:|']
    for c in CANDIDATES:
        t.append('| %s | %d | %d | %d |' % (c, must_not[c], opt_d[c], trig_21[c]))
    t.append('\n## `R01-TRIGGERED-CLASS`: the 21 leads\n')
    t.append('All 21 were read individually (`PI012_EXTRA_21_REVIEW.jsonl`). Kinds: %s. Decisions: %s.\n' % (', '.join('%s %d' % kv for kv in sorted(kinds.items())), ', '.join('%s %d' % kv for kv in sorted(Counter(x['decision'] for x in out).items()))))
    t.append('One lead (`FG-M1-14b23b94ae`) is a scan artifact: the `when` belongs to the next clause. The three scan restraints on `TokenValidationParameters` are addressed to the auditor and create no product prohibition.\n')
    t.append('## Not strictness facts\n')
    t.append('- Docker exclusion clause: L0, L1 store it as its own `MUST_NOT` record; M, M1, K1 hold the same clause inside a compound stored `DEFAULT`; K0 says "Keep". Record granularity.')
    t.append('- Custom JWT line: M, M1, L0, L1 `MUST_NOT`; K0, K1 inside a compound stored `DEFAULT`. `SEC-016` is owned elsewhere in both.')
    t.append('- `EnsureSuccessStatusCode` line: K0 writes "too blunt" where five write "do not". A real wording difference.')
    t.append('- Scrutor line: K0 writes "not worth adding" where five write "do not". A real wording difference.')
    t.append('- Deserialization line: all six sit in a scan layer; see `REVIEWER_SIX_READINGS.md`.')
    t.append('\n## Bounds\n')
    t.append('The scan is the same heuristic as v1: the closest sentence on knowledge-only records. A sentence it does not pick is missed. These 21 are a bound, not a census of the form.')
    write_text('PI012_SENSITIVITY_V2.md', '\n'.join(t) + '\n')
    print('extra21', len(out), dict(kinds), 'adj', len(adj), 'must_not', dict(must_not))


if __name__ == '__main__':
    main()
