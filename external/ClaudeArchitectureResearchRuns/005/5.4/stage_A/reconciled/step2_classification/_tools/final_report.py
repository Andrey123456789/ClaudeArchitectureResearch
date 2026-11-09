"""Writes COVERAGE_LIMITATIONS.md and STEP2_CLASSIFICATION_REPORT.md from the final outputs.

Numbers come from CLASSIFICATION_SUMMARY.json and the aggregate files; the prose is fixed text.
Usage: python -B _tools/final_report.py
"""
import json
import os
import sys
from collections import Counter

from common import CANDIDATES, OUT, read_jsonl
import a13_audit

ABBR = [('CANONICAL_ONLY', 'CO'), ('CANONICAL_PLUS_DELTA', 'CD'), ('EXTRA_PRODUCT', 'XP'), ('EXTRA_WORKFLOW', 'XW'),
        ('INTERNAL_ARCHITECTURE', 'IA'), ('MIXED', 'MX'), ('NON_NORMATIVE', 'NN'), ('UNCERTAIN', 'UN')]


def out(*p):
    return os.path.join(OUT, *p)


def table(head, rows):
    lines = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    lines += ['| ' + ' | '.join(str(x) for x in r) + ' |' for r in rows]
    return '\n'.join(lines)


def load():
    s = json.load(open(out('CLASSIFICATION_SUMMARY.json'), encoding='utf-8'))
    d = {'s': s, 'cand': s['by_candidate'], 'total': s['total']}
    d['uncertain'] = read_jsonl(out('UNCERTAIN_CLASSIFICATIONS.jsonl'))
    d['overmerges'] = read_jsonl(out('POTENTIAL_OVERMERGES.jsonl'))
    d['fhd'] = read_jsonl(out('FUTURE_HUMAN_DECISIONS.jsonl'))
    d['queue'] = read_jsonl(out('ORPHAN_REVIEW_QUEUE.jsonl'))
    d['merge'] = read_jsonl(out('STEP1_QUEUE_DISPOSITIONS.jsonl'))
    d['cal'] = read_jsonl(out('CALIBRATION_AGREEMENT.jsonl'))
    d['audit'] = a13_audit.scan()
    d['findings'] = read_jsonl(out('_decisions', 'A13_AUDIT_FINDINGS.jsonl'))
    d['cov'] = {c: read_jsonl(out('per_candidate', c, 'POLICY_COVERAGE.jsonl')) for c in CANDIDATES}
    d['challenges'] = {c: read_jsonl(out('per_candidate', c, 'SEMANTIC_CHALLENGES.jsonl')) for c in CANDIDATES}
    return d


def limitations(d):
    c = d['cand']
    overrides = sum(c[x]['coverage_reviewer_overrides'] for x in CANDIDATES)
    n_ch = sum(len(d['challenges'][x]) for x in CANDIDATES)
    revised = sum(1 for x in CANDIDATES for y in d['challenges'][x] if y['outcome'] == 'REVISED_NEEDED')
    flat = Counter(x['category'] for x in d['audit'])['N']
    corrected = Counter(x['category'] for x in d['findings'] if x['category'] in 'ABC')
    non_eq = ['%s: %s' % (x, ', '.join(y['policy_id'] for y in d['cov'][x] if y['strength_status'] != 'EQUIVALENT_EVIDENCE_PRESENT'))
              for x in CANDIDATES if any(y['strength_status'] != 'EQUIVALENT_EVIDENCE_PRESENT' for y in d['cov'][x])]
    mech = Counter(x['disposition'] for x in d['merge'])
    mx = ', '.join('%s %d' % (x, c[x]['by_class'].get('MIXED', 0)) for x in CANDIDATES)
    ia = ', '.join('%s %d' % (x, c[x]['by_class'].get('INTERNAL_ARCHITECTURE', 0)) for x in CANDIDATES)
    om = Counter(x['basis'] for x in d['overmerges'])
    cal_mod = [x for x in d['cal'] if x['classification_agrees'] and not x['agrees']]
    return f"""# Coverage limitations: Stage A / Step 2

Protocol step2-v1 with Addendum A1. Read this before using any count from this folder.

**Structural coverage does not prove semantic completeness.** Every one of the {d['total']['n_records']:,} records has a label and every policy row has a status. That does not show that all normative content of the candidates was found, or that every label is right. This run does not claim "zero remaining normative orphans".

## What the coverage does and does not cover

1. **The classified universe is the Pass 1 augmented union.** Step 2 did no new global extraction. A normative clause that neither Step 1 nor Pass 1 surfaced is not in these files unless a reader met it in an open-item review.
2. **Codex Pass 2 is still running and was not used.** Its findings may add clauses or facets that this dataset lacks.
3. **`DIRECT_EVIDENCE` means traceable evidence in this dataset.** It is not a compliance or freeze-readiness result, and `NOT_EVIDENCED` would not have meant a violation.
4. **{overrides} of the 1,176 rows are `DIRECT_EVIDENCE` by a written reviewer override.** No single record fully covered those policies, so the reviewer checked several partial records clause by clause under C13. The note is in `reviewer_override_note` on each row.
5. **Hooks, scripts and settings were read statically (C10).** Nothing was executed. Reported bypasses and parser gaps, such as the guard gap noted at `FG-K1-e32ee646e0`, remain unverified.

## Strength and modality

6. **Rows with no equal-strength evidence:** {'; '.join(non_eq)}. These have stronger and weaker evidence only, shown as `STRONGER_AND_WEAKER_EVIDENCE`. The record may restate the policy's content while differing in force.
7. **The end-of-run A1.3 audit gives a floor for this defect class, not a full count.** It found records at MUST or MUST_NOT whose whole evidence, in a knowledge skill or private reference, has no must-like word. It changed the modality of {sum(corrected.values())} of them ({corrected['A']} A, {corrected['B']} B and {corrected['C']} C). A record is not reached if a must-like word appears anywhere in its evidence, including in another clause of a broad group.
8. **{flat} flat negatives stay at MUST_NOT,** 4 of them in M1 now coded as check by reference. They say "no X", "not X", "only when" or "without", with no must, never or do not. A1.3 addresses positive imperatives and does not settle these (PI-012, still open). The list is category N in `_decisions/A13_AUDIT_FINDINGS.jsonl`.
9. **The audit changed modality and strength, not classification.** Its corrections moved no record to another label, and all 1,176 rows kept their coverage status.

## Reader and process limits

10. **One reader made these decisions.** An independent review covered candidate M only, and this session applied its lessons to the rest. M1, L0, L1, K0 and K1 have had no independent review.
11. **Label use may have drifted during the run, so counts need care across candidates.** MIXED counts rise in processing order ({mx}), and INTERNAL_ARCHITECTURE counts also vary ({ia}). Part of this may come from the sources and part from the reader splitting compound records more readily later on. This run did not separate the two. Do not treat these counts as a difference between candidates without re-reading the records.
12. **Correction counts measure process, not quality.** M has the most corrections because it was read before Addendum A1 and then audited. Its batches stayed as checkpointed, with fixes applied as an overlay.
13. **Semantic challenges are samples.** {n_ch} frozen samples were challenged, and {revised} needed a revised reading. They show kinds of defects and are not an accuracy rate.
14. **NON_NORMATIVE was missed by the first challenge round in five candidates.** The round-1 pool asked for HIGH confidence, and every NN record in M1, L0, L1, K0 and K1 is MEDIUM. The validator found this, and a frozen round 2 added 5 NN samples per candidate, all upheld (PI-013). Five samples per candidate is thin.
15. **Reading-consistency aids were hints only.** `prior.py`, and scratch search scripts used late in the run, showed how finished candidates read similar text. They were used to keep readings consistent and are not a strictness comparison. Notes such as "Same reading as M1" record that consistency check. Each label still rests on the candidate's own source.
16. **The primary anchor of a broad Step-1 group can be its first clause,** not the clause the claim rests on (for example `FG-K0-aa5d11a7f5`). Use `evidence_refs` for the full evidence.
17. **Calibration:** {sum(x['agrees'] for x in d['cal'])} of {len(d['cal'])} keys agree on class and modality. {', '.join('`%s` agrees on class but reads %s where calibration read %s' % (x['source_key'], x['final_modality'], x['calibration_modality']) for x in cal_mod) or 'None differ.'}. `CALIBRATION.jsonl` was recompiled after a schema addition, and `PROTOCOL_FREEZE.json` records this as an amendment beside the original hash.

## Step-1 queue

18. **Only {sum(1 for x in d['merge'] if x['item_type'] in ('APPARENT_CONFLICT', 'UNRESOLVED'))} of the {len(d['merge']):,} queue items were adjudicated one by one** (the conflicts and unresolved items). The other {mech['GROUPS_CLASSIFIED_SEPARATELY'] + mech['GROUPS_CLASSIFIED_FROM_SOURCE']:,} (relations and attribution disagreements) are recorded mechanically in `STEP1_QUEUE_DISPOSITIONS.jsonl`. The reviewer saw them in batch views, and every named group is classified, but none received its own decision.
19. **Overmerge review is shallow.** `POTENTIAL_OVERMERGES.jsonl` holds {om['EXPLICIT_REVIEWER_FLAG']} explicit flag and {om['MIXED_RECORD_WITH_SEVERAL_SOURCE_RANGES']} MIXED records with several source ranges, found by rule. Groups whose members share a label were not examined for overmerging, and no Step-1 group was split.

## Known reading differences kept on purpose

These are recorded so that later work does not mistake them for candidate differences. They are not strictness findings.

| Records | Difference | Why it stays |
|---|---|---|
| `FG-M-2dfeb68001` and the Delegated records of M1 to K1 | M: CO with a permission code. The others: CD on GOV-005 | M carries the narrowed Delegated scope at the sibling record `FG-M-ae349c2f55`, and this record claims only the permission |
| `FG-L0-59496c6b6d` and `FG-K0-0865f7332f` | L0: CO advisory reminder. K0: XP on a Reserved reference graph | The wording differs. L0's hook asks to confirm the mapped layout or an approved decision; K0's says the change is Reserved |
| `FG-K1-2b15ea3da2` and the Swagger step in M1, L0, L1, K0 | K1: CO with a note. The others: UN on how far a condition reaches | The others hold a separate reported record on the question, and K1 has none. The same doubt may apply to K1 |
| `FG-M-567f30944c`, `FG-K0-77da905ab7` and `FG-K1-05e23d2c2a` | CO where the source keeps a "concrete requirement" exception. CD where it does not | The source text differs |
"""


def report(d):
    c = d['cand']
    t = d['total']
    res = json.load(open(out('VALIDATION_RESULT.json'), encoding='utf-8')) if os.path.exists(out('VALIDATION_RESULT.json')) else {'gates': []}
    rows = [[x, c[x]['n_records']] + [c[x]['by_class'].get(k, 0) for k, _ in ABBR] for x in CANDIDATES]
    rows.append(['**Total**', '**%d**' % t['n_records']] + ['**%d**' % t['by_class'].get(k, 0) for k, _ in ABBR])
    cls = table(['Candidate', 'Records'] + [a for _, a in ABBR], rows)
    str_rows = []
    for x in CANDIDATES:
        e = c[x]['by_strength_equivalence']
        str_rows.append([x, e.get('EQUIVALENT', 0), e.get('WEAKER_THAN_CANONICAL', 0), e.get('STRONGER_THAN_CANONICAL', 0), e.get('PORTION_EQUIVALENT_WITH_REMAINDER', 0),
                         e.get('INCOMPARABLE', 0), c[x]['strength_divergences']])
    strength = table(['Candidate', 'Equivalent', 'Weaker', 'Stronger', 'Portion + remainder', 'Incomparable', 'Divergence rows'], str_rows)
    cov = table(['Candidate', 'DIRECT', 'of which by override', 'Equal-strength evidence', 'Stronger and weaker only'],
                [[x, c[x]['policy_coverage'].get('DIRECT_EVIDENCE', 0), c[x]['coverage_reviewer_overrides'], c[x]['policy_strength_status'].get('EQUIVALENT_EVIDENCE_PRESENT', 0),
                  c[x]['policy_strength_status'].get('STRONGER_AND_WEAKER_EVIDENCE', 0)] for x in CANDIDATES])
    open_rows = table(['Candidate', 'ATTACH', 'NON_NORMATIVE', 'RESOLVED', 'QUEUE'],
                      [[x] + [c[x]['open_item_dispositions'].get(k, 0) for k in ('ATTACH', 'NON_NORMATIVE', 'RESOLVED', 'QUEUE')] for x in CANDIDATES])
    ch_rows = table(['Candidate', 'Challenged', 'Upheld', 'Revised', 'Corrections', 'Label changes from corrections'],
                    [[x, c[x]['semantic_challenges']['n'], c[x]['semantic_challenges']['outcomes'].get('UPHELD', 0), c[x]['semantic_challenges']['outcomes'].get('REVISED_NEEDED', 0),
                      c[x]['corrections']['n'], c[x]['corrections']['classification_changes']] for x in CANDIDATES])
    gates = table(['Gate', 'Status'], [['`%s`' % g['gate'], g['status']] for g in res['gates']]) if res['gates'] else '(run `finalize.py validate`)'
    un_keys = [x['source_key'] for x in d['uncertain'] if 'UNCERTAIN_RECORD' in x['reasons']]
    un_sub = [x['source_key'] for x in d['uncertain'] if 'UNCERTAIN_SUBCLAUSE' in x['reasons']]
    reasons = Counter(r for x in d['uncertain'] for r in x['reasons'])
    domain = table(['Domain', 'Records'], sorted(t['by_domain'].items()))
    relation = table(['Oracle relation', 'Records'], sorted(t['by_oracle_relation'].items()))
    certainty = table(['Confidence', 'Records'], sorted(t['by_certainty'].items()))
    all_ch = sum(len(d['challenges'][x]) for x in CANDIDATES)
    all_cor = sum(c[x]['corrections']['n'] for x in CANDIDATES)
    all_chg = sum(c[x]['corrections']['classification_changes'] for x in CANDIDATES)
    eor = sum(c[x]['corrections']['by_finding'].get('END-OF-RUN-CONSISTENCY', 0) for x in CANDIDATES)
    audit = sum(c[x]['corrections']['by_finding'].get('AUDIT-A1-KNOWLEDGE', 0) for x in CANDIDATES)
    return f"""# Stage A / Step 2 classification report

Protocol step2-v1 with Addendum A1. Experiment 005, Phase 5.4.

## Result

All {t['n_records']:,} records of the augmented union are classified and all 1,176 policy rows are filled. The mechanical validator status is **{res.get('status', 'NOT RUN')}**. That is a structural result, and it does not prove the readings are right. `COVERAGE_LIMITATIONS.md` lists what remains weak.

Step 2 stops here. This run made no cross-candidate strictness comparison, changed no candidate template and started no unification. It did not read the running Codex Pass 2 search.

## Classification

{cls}

CO canonical only, CD canonical plus delta, XP extra product, XW extra workflow, IA internal architecture, MX mixed, NN non-normative, UN uncertain.

These counts describe labels in this dataset. They do not rank the candidates, and label use may have drifted during the run (limitation 11).

{domain}

{relation}

{certainty}

All {t['n_records']:,} records passed a re-read of their evidence from the immutable files, covering {sum(t['evidence_quality']['reference_check_status'].values()):,} references. The full breakdown by candidate is in `CLASSIFICATION_SUMMARY.json`.

### Normative strength against the policies

{strength}

## Policy coverage

{cov}

`DIRECT_EVIDENCE` means traceable evidence, not compliance.

## Open items from Step 1 and Pass 1

All 223 pending orphans, 43 apparent conflicts, 4 unresolved items and 17 Pass 1 issues have a recorded outcome, as do all 26 proposals and all 29 facets (7 additional obligations, 22 factual clarifications).

{open_rows}

## Corrections and semantic challenges

{ch_rows}

Every correction goes through `_decisions/<C>/CORRECTIONS.dec`, with the full record before the change and a hash after it in `per_candidate/<C>/CORRECTIONS.jsonl`. Batch files stayed as checkpointed. In all there are {all_cor} corrections, {all_chg} of which changed a label.

The end of the run added two sets:

- **{eor} consistency corrections** on reading differences listed during the run: health-check grading, the unconditional validation-package ban, the stated trade-off, the servicing-release clause, the reviewer checker, frontend test locations and the ASP.NET package check in inner layers.
- **{audit} A1.3 audit corrections** from a scan for MUST or MUST_NOT on knowledge-skill and private-reference text with no must-like word: {audit - 4} modality changes and 4 check-by-reference codes in M1. Each was read by hand. No label changed and every coverage status held.

{all_ch} frozen samples were challenged against the source and a counterexample. The validator found that round 1 had sampled no NON_NORMATIVE record in five candidates, so a round 2 was added for them.

## What stays unresolved

- **{len(un_keys)} UNCERTAIN records and {len(un_sub)} records with an UNCERTAIN subclause.** They fall into four questions:
  1. May an approved workflow authorize destructive Git operations without an explicit request (GOV-015)? All six candidates.
  2. Is a deliberate pre-mutation cache invalidation compatible with RUN-021? M, M1, L1, K1.
  3. How far does the condition on the Swagger UI step reach? M1, L0, L1, K0.
  4. Does explicit approval in a headless run's original request allow a Reserved change? M.
- **{len(d['fhd'])} future human decisions** in `FUTURE_HUMAN_DECISIONS.jsonl`. They are the questions above, plus whether a checker should honour DEP-003's explicit-request exception for floating versions (M, M1, K1).
- **{len(d['queue'])} open review items** in `ORPHAN_REVIEW_QUEUE.jsonl`, each with evidence. Most point to the questions above. The rest are prescriptive fragments that no group holds, such as output-cache metadata technique and the AAA "useful default".
- **{reasons['LOW_CONFIDENCE']} LOW-confidence records and {reasons['REVIEW_NEEDED']} flagged for review,** with reasons, in `UNCERTAIN_CLASSIFICATIONS.jsonl`.
- **{len(d['overmerges'])} potential overmerges** in `POTENTIAL_OVERMERGES.jsonl`. No group was split.
- **PI-012 is open:** how to read flat negatives in technique text. The affected records stay at MUST_NOT.

## Validation

{gates}

To re-run:

```bash
python -B _tools/finalize.py build
python -B _tools/final_report.py
python -B _tools/finalize.py validate
```

## Files

- Per candidate: `per_candidate/<C>/` holds `CLASSIFICATIONS.jsonl`, `POLICY_COVERAGE.jsonl`, `CANDIDATE_REPORT.md`, `SEMANTIC_CHALLENGES.jsonl`, `ORPHAN_DISPOSITIONS.jsonl`, `CORRECTIONS.jsonl` and `STRENGTH_DIVERGENCES.jsonl`.
- Protocol: `CLASSIFICATION_PROTOCOL.md`, `PROTOCOL_ADDENDUM_A1.md`, `PROTOCOL_ISSUES.jsonl`, `PROTOCOL_FREEZE.json`, `CALIBRATION.jsonl`, `CALIBRATION_AGREEMENT.jsonl`.
- Aggregates: `CLASSIFICATION_SUMMARY.json`, `UNCERTAIN_CLASSIFICATIONS.jsonl`, `POTENTIAL_OVERMERGES.jsonl`, `FUTURE_HUMAN_DECISIONS.jsonl`, `ORPHAN_REVIEW_QUEUE.jsonl`, `STEP1_QUEUE_DISPOSITIONS.jsonl`, `COVERAGE_LIMITATIONS.md`, `VALIDATION_RESULT.json`.
- Reproducibility: `CHECKPOINTS/`, `_batches/`, `_decisions/`, `_tools/`, `INPUT_HASHES.json`.
"""


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    d = load()
    with open(out('COVERAGE_LIMITATIONS.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(limitations(d))
    with open(out('STEP2_CLASSIFICATION_REPORT.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(report(d))
    print('reports written')


if __name__ == '__main__':
    main()
