"""Compile reader files into every audit deliverable except the hand-written notes.

  python -B _tools/build.py

Reads upstream and _decisions/ only. Writes only inside step2_semantic_audit_v1/. Deterministic: reruns give identical output
apart from the at field in the manifest.
"""
import hashlib
import json
import os
import re
import shutil
import sys
import time
from collections import Counter, defaultdict

from acommon import (AUDIT_VERSION, CANDIDATES, DEC, OUT, ROOT, S2, baseline, canon, cand_of, coverage, file_lines_abs, out_path, policies, policy_text, read_jsonl, rec_hash, sha256_file,
                     sha256_text, source_range, utf8_stdout, write_json, write_jsonl)
from dsl import full_path, load_blind, load_decisions, verify_quote
from overlay import DERIVED, NOT_OWNER_CODES, OVERLAY_ONLY, RECORD_FIELDS, apply_set, coverage_of, links_of, replay
from targets import SPECIAL_CELLS, SWAGGER_RE

PREV_FIELDS = ('classification', 'normativity', 'domain', 'oracle_relation', 'canonical_coverage', 'modality', 'strength_vs_canonical', 'normative_strength_equivalence', 'strength_resolution_code',
               'trigger', 'exceptions', 'extra_fragment', 'extra_fragment_kind', 'distinguishing_scenario', 'confidence', 'review_needed', 'review_reason', 'future_human_decision', 'related_policy_ids')
LOADING_RE = re.compile(r'^(on-demand|private reference|workflow |skill |rule |Claude Code|always|hook |path[- ]|loaded|executable|NOT_APPLICABLE)', re.I)
QUESTIONS = [
    ('HQ-01', r'approved workflow (may )?authorize', 'May an approved workflow authorize destructive Git operations without a per-operation explicit request (GOV-015)?'),
    ('HQ-02', r'pre-mutation cache invalidation', 'Is workflow-accepted pre-mutation cache invalidation compatible with RUN-021?'),
    ('HQ-03', r'explicit-request exception|honou?r DEP-003', "Should a manifest checker honor DEP-003's explicit-request exception for floating versions?"),
    ('HQ-04', r'headless', 'Does an explicit approval in the original request of a headless run authorize a Reserved change?'),
    ('HQ-05', r'peer-dependency bypass', 'May explicit user confirmation permit a peer-dependency bypass that DEP-025 forbids?'),
]
HQ_DETAIL = {
    'HQ-01': {'why_human': 'GOV-015 says unless explicitly requested. Candidate text adds an approved-workflow branch. Whether that is the same thing depends on what approved means, which neither text defines. A choice of policy, not a reading.',
              'options': ['An approved workflow counts as an explicit request: the records become entailed.', 'It does not: the records widen GOV-015 and need treatment as weaker or conflicting.'],
              'step3_rule': 'Treat all six candidates as carrying the same open branch. Do not rank them on it.'},
    'HQ-02': {'why_human': "RUN-021's phrase can be read two ways. Accepting early invalidation is a design position on the policy, and text does not settle it.",
              'options': ['Compatible: a failed mutation only leaves a cache miss.', 'An exception the policy does not grant.'],
              'step3_rule': 'L1 words it as must be a deliberate choice; the others as acceptable or only when. Keep the wording; do not rank on it.'},
    'HQ-03': {'why_human': 'The reading is settled: these checkers have no explicit-request branch, so they are stronger than DEP-003. What remains is a design choice about whether a checker should follow the policy exception.',
              'options': ['Align checkers with the exception.', 'Keep them stricter as a deliberate choice.'],
              'step3_rule': 'Count as stronger with the static-reading caveat; execution was not done.'},
    'HQ-04': {'why_human': 'Text gives an explicit-instruction rule and a headless rule with no stated precedence. Flagged in M only by Step 2, but all six have a headless sentence, and they differ: M says never make a Reserved decision, M1 and L1 say continue or take only a non-Reserved path, L0, K0 and K1 add silently.',
              'options': ['Prompt approval counts in a headless run.', 'Headless runs never perform Reserved changes.'],
              'step3_rule': 'M is UNCERTAIN. The others are not flagged, but do not assume they resolve the question. The word silently is a real text difference to keep.'},
    'HQ-05': {'why_human': 'Reading is settled for the text: a user-confirmation route exists in M1 and L1. DEP-025 has no such route when the purpose is to bypass peers. Whether user confirmation may override is a policy matter.',
              'options': ['Confirmation may override.', 'It may not: the route is a weakening.'],
              'step3_rule': 'Keep INCOMPARABLE on those records. K1 has no route, which is a real difference.'},
}
METHODOLOGY_HQ = {'question_id': 'HQ-06', 'question': 'Accept the proposed PI-012 reading rule for flat negatives in knowledge-skill and private-reference text?', 'status': 'OPEN', 'type': 'METHODOLOGY',
                  'why_human': 'The rule amends how frozen A1.3 is read. It should not be applied silently. All dependent corrections are marked PROPOSED, and the sensitivity tables show both outcomes.',
                  'options': ['Accept: use the effective view for those records.', 'Reject: read those records at their baseline MUST_NOT.', 'Accept in part: for example keep security-content only-when lines binding.'],
                  'step3_rule': 'Prepare both views. Do not use a modality that depends on this as a fact until decided.', 'candidates': CANDIDATES, 'source_keys': [], 'see': 'METHODOLOGY_NOTE.md'}


def rd(*p):
    return read_jsonl(os.path.join(S2, *p))


def anchor_src(r):
    a = r['primary_anchor']
    text = source_range(a['path'], a['start_line'], a['end_line'])
    return {'path': a['path'], 'start_line': a['start_line'], 'end_line': a['end_line'], 'quote': text[:600], 'quote_truncated': len(text) > 600, 'range_sha256': sha256_text(text), 'verified_by': 'mechanical re-read of the immutable file'}


def quote_rows(cand, quotes):
    out = []
    for q in quotes:
        q2, ok = verify_quote(cand, q)
        out.append({'path': q2['path'], 'start_line': q2['start_line'], 'end_line': q2['end_line'], 'quote': q2['quote'], 'verified': ok,
                    'range_sha256': sha256_text(source_range(q2['path'], q2['start_line'], q2['end_line'])) if ok else None})
    return out


def prev_of(obj):
    return {f: obj.get(f) for f in PREV_FIELDS if f in obj}


def pols(ids):
    return [policy_text(p) for p in sorted(set(ids)) if p in policies()]


def cov_ids(o):
    return [c['policy_id'] for c in o.get('canonical_coverage') or []]


def open_question_type(row):
    t = ' '.join([row.get('rationale') or '', row.get('remaining_ambiguity') or ''] + (row.get('alternatives') or []) + (row.get('human_questions') or []))
    if re.search(r'non-rewritable', t, re.I):
        return 'NON_REWRITABLE_READING (no human decision entry; only the authors can say whether an explicit request also unlocks main and master)'
    if 'headless' in t.lower():
        return 'HQ-04'
    if 'RUN-021' in t:
        return 'HQ-02'
    if re.search(r'approved.workflow|GOV-015', t, re.I):
        return 'HQ-01'
    if 'deserializ' in t.lower() or 'SEC-003' in t:
        return 'SCAN_LINE_READING (a source reading that cannot be settled from the line)'
    return 'OTHER'


def ratification(x):
    if x['extra'].get('dep') == 'PI012':
        return 'PROPOSED_PENDING_METHODOLOGY_PI012'
    if x['extra'].get('open') == '1':
        return 'PROPOSED_FIELD_FIX_OPEN_QUESTION_RETAINED'
    return 'PROPOSED_SOURCE_SUPPORTED'


def main():
    utf8_stdout()
    blind, dec = load_blind(), load_decisions()
    plan = json.load(open(out_path('SAMPLING_PLAN.json'), encoding='utf-8'))
    frozen_targets = out_path('PREFLIGHT', 'AUDIT_TARGETS_FROZEN.jsonl')
    if not os.path.exists(frozen_targets):
        shutil.copyfile(out_path('AUDIT_TARGETS.jsonl'), frozen_targets)
    targets = {t['case_id']: t for t in read_jsonl(frozen_targets)}
    all_base = {}
    for c in CANDIDATES:
        all_base.update(baseline(c))
    logged = defaultdict(set)
    for row in read_jsonl(out_path('CHECKPOINTS', 'BLIND_LOG.jsonl')):
        logged[row['batch']].add(row['blind_sha256'])

    # ------- corrections, in deterministic file order
    corrections, per_cand = [], Counter()
    for case, x in dec.items():
        if case.startswith(('COV:', 'ORP:', 'QUE:')) or not x['set']:
            continue
        base = case.split('/')[0]
        c = all_base[base]['candidate']
        per_cand[c] += 1
        before_rec = all_base[base]
        sub = case.split('/')[1] if '/' in case else None
        before_obj = next(s for s in before_rec['subclauses'] if s['subclause_id'] == sub) if sub else before_rec
        after_rec = apply_set(before_rec, x['set'], sub)
        after_obj = next(s for s in after_rec['subclauses'] if s['subclause_id'] == sub) if sub else after_rec
        changed = {}
        for f in sorted(set(PREV_FIELDS) | {'subclauses', 'audit_subclauses', 'canonical_semantic_coverage', 'strength_links', 'strength_mechanical_mismatch', 'strength_resolution'}):
            a, b = before_obj.get(f), after_obj.get(f)
            if canon(a) != canon(b):
                changed[f] = {'before': a, 'after': b}
        quotes = quote_rows(c, x['quotes'])
        corrections.append({'correction_id': 'COR-A-%s-%04d' % (c, per_cand[c]), 'audit_version': AUDIT_VERSION, 'candidate': c, 'case_key': case, 'source_key': base, 'subclause_id': sub,
                            'correction_class': x['extra'].get('cls'), 'decision': x['decision'], 'ratification': ratification(x), 'depends_on': x['extra'].get('dep'), 'rationale': x['why'], 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[x['extra']['conf']],
                            'quotes': quotes, 'set': x['set'], 'changed_fields': changed, 'baseline_record_sha256': rec_hash(before_rec), 'after_record_sha256': rec_hash(after_rec), 'alternatives': x['alt'], 'remaining_ambiguity': x['amb'], 'source_of_decision': x['src'], 'note': 'PROPOSED, not RATIFIED. Baseline is unchanged.'})
    write_jsonl('CORRECTION_PROPOSALS.jsonl', corrections)

    eff = replay(corrections, CANDIDATES)
    cor_by_key = defaultdict(list)
    for co in corrections:
        cor_by_key[co['source_key']].append(co['correction_id'])
    # PI-012-free variant for sensitivity
    no_pi = [c for c in corrections if c['depends_on'] != 'PI012']
    eff_no_pi = replay(no_pi, CANDIDATES)

    # ------- leads
    leads = read_jsonl(out_path('_work', 'A13_RESIDUAL_LEADS.jsonl')) if os.path.exists(out_path('_work', 'A13_RESIDUAL_LEADS.jsonl')) else read_jsonl(out_path('A13_RESIDUAL_LEADS.jsonl'))
    lead_read = set(json.load(open(out_path('_work', 'A13_LEAD_READ.json')))) if os.path.exists(out_path('_work', 'A13_LEAD_READ.json')) else set(r['source_key'] for r in leads if r.get('read_in_audit'))
    lead_keys = {r['source_key'] for r in leads}
    write_jsonl('A13_RESIDUAL_LEADS.jsonl', [dict(r, audited=r['source_key'] in dec, read_in_audit=r['source_key'] in lead_read, meaning='A heuristic lead, not a finding: stored MUST or MUST_NOT on knowledge text where the sentence closest to the claim has no must-like word.') for r in leads])

    # ------- swagger comparables
    comparable = set(json.load(open(os.path.join(DEC, 'A1.batch.json'), encoding='utf-8'))['keys'])

    # ------- ledger
    ledger, added = [], []
    mem_of = {t['key']: t['memberships'] for t in targets.values() if t['case_type'] == 'RECORD'}
    seen_cases = set()
    def ledger_record(case, x, memberships, added_reason=None):
        base = case.split('/')[0]
        r = all_base[base]
        sub = case.split('/')[1] if '/' in case else None
        obj = next(s for s in r['subclauses'] if s['subclause_id'] == sub) if sub else r
        b = blind.get(case)
        c = r['candidate']
        after = next(s for s in eff[c][base]['subclauses'] if s['subclause_id'] == sub) if sub else eff[c][base]
        pol_ids = set(cov_ids(obj)) | set(cov_ids(after)) | set(obj.get('related_policy_ids') or r.get('related_policy_ids') or [])
        if b:
            pol_ids |= set(cov_ids(b))
        row = {'case_id': 'REC:' + case, 'case_type': 'RECORD', 'candidate': c, 'key': case, 'memberships': memberships, 'added_after_freeze': added_reason,
               'source': [anchor_src(r)] + quote_rows(c, x['quotes']) if x else [anchor_src(r)], 'canonical_policies': pols(pol_ids), 'claim_text': r['claim_text'] if not sub else obj.get('text'), 'previous': prev_of(obj)}
        if x:
            row.update({'independent': ({k: b[k] for k in ('classification', 'modality', 'domain', 'oracle_relation', 'canonical_coverage', 'confidence')} | {'facts': b['facts']}) if b else None,
                        'entailment_test': b['entailment_test'] if b else None, 'blind_reading': {'batch': b['batch'], 'logged_before_reveal': bool(logged.get(b['batch']))} if b else {'status': 'NOT_PERFORMED', 'via': x['extra'].get('via')},
                        'agreement': {'label': b['classification'] == obj.get('classification'), 'modality': b['modality'] == obj.get('modality')} if b else None,
                        'decision': x['decision'], 'rationale': x['why'], 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[x['extra']['conf']], 'remaining_ambiguity': x['amb'], 'alternatives': x['alt'], 'human_questions': x['hd'],
                        'correction_ids': cor_by_key.get(base, []), 'open': x['decision'] == 'UNRESOLVED' or x['extra'].get('open') == '1', 'source_of_decision': x['src'], 'tokens': {k: v for k, v in x['extra'].items() if k not in ('conf', 'notes')}})
        return row

    for tid, t in sorted(targets.items()):
        if t['case_type'] != 'RECORD':
            continue
        case = t['key']
        seen_cases.add(case)
        x = dec.get(case)
        row = ledger_record(case, x, t['memberships'])
        if not x:
            ms = set(t['memberships'])
            if ms == {'SWAGGER_A'}:
                r = all_base[case]
                hits = []
                for e in r['evidence_refs']:
                    for i in range(e['start_line'], e['end_line'] + 1):
                        l = file_lines_abs(e['path'])[i - 1]
                        if SWAGGER_RE.search(l):
                            hits.append({'path': e['path'], 'line': i, 'text': l.strip()[:240]})
                row.update({'decision': None, 'audit_status': 'TRIAGED_NOT_A_VERIFICATION_STEP', 'rationale': 'Source line mentions Swagger UI, but the claim is not a UI verification step. Read in the one-line triage for Section A; no label reviewed.', 'triage_hits': hits[:3]})
            elif ms <= {'SWAGGER_A', 'DRIFT_F'}:
                row.update({'decision': None, 'audit_status': 'COMPARED_IN_DRIFT_DIAGNOSTIC', 'rationale': 'Read as one side of a frozen drift pair. See DRIFT_DIAGNOSTIC.md.'})
            else:
                row.update({'decision': None, 'audit_status': 'MISSING_DECISION', 'rationale': None})
        ledger.append(row)
    for case, x in dec.items():
        if case.startswith(('COV:', 'ORP:', 'QUE:')) or case in seen_cases:
            continue
        reason = x['extra'].get('via', 'PI012_SUBCLAUSE_PARENT')
        base = case.split('/')[0]
        row = ledger_record(case, x, sorted(set(mem_of.get(base, [])) | {reason}), added_reason=reason)
        ledger.append(row)
        added.append(row)

    # ------- PI-012 review
    n_rows = [x for x in rd('_decisions', 'A13_AUDIT_FINDINGS.jsonl') if x['category'] == 'N']
    cov_base = {c: coverage(c) for c in CANDIDATES}
    cov_eff = {c: coverage_of(list(eff[c].values())) for c in CANDIDATES}
    cov_no = {c: coverage_of(list(eff_no_pi[c].values())) for c in CANDIDATES}
    pi_rows = []
    for x in n_rows:
        k = x['key']
        d = dec[k]
        base = k.split('/')[0]
        r = all_base[base]
        sub = k.split('/')[1] if '/' in k else None
        o = next(s for s in r['subclauses'] if s['subclause_id'] == sub) if sub else r
        c = r['candidate']
        a = next(s for s in eff[c][base]['subclauses'] if s['subclause_id'] == sub) if sub else eff[c][base]
        b = blind[k]
        impact = []
        for p in cov_ids(o):
            be, ef = cov_base[c][p]['strength_status'], cov_eff[c][p]['strength_status']
            if be != ef:
                impact.append({'policy_id': p, 'strength_status_baseline': be, 'strength_status_effective': ef})
        mod_new = a.get('modality')
        direction = 'UNCHANGED' if mod_new == o.get('modality') else 'WEAKER_READING'
        pi_rows.append({'candidate': c, 'key': k, 'outcome': d['decision'] if d['decision'] in ('UPHOLD', 'CORRECT', 'UNRESOLVED') else 'CORRECT', 'negative_form': d['extra'].get('neg'), 'needs_pi012_rule': d['extra'].get('dep') == 'PI012',
                        'normativity_reading': a.get('normativity', r.get('normativity')) if not sub else 'NORMATIVE', 'modality_old': o.get('modality'), 'modality_suggested': mod_new, 'classification_old': o.get('classification'), 'classification_suggested': a.get('classification'),
                        'strength_old': o.get('normative_strength_equivalence'), 'strength_suggested': a.get('normative_strength_equivalence'), 'direction': direction,
                        'actor': b['facts']['actor'], 'behavior': b['facts']['behavior'], 'trigger': a.get('trigger') or b['facts']['trigger'], 'scope': b['facts']['scope'], 'exceptions': b['facts']['exception'],
                        'source': anchor_src(r), 'verified_quotes': quote_rows(c, d['quotes']), 'falsifiable_scenario_or_test': b['entailment_test'], 'rationale': d['why'], 'alternatives': d['alt'], 'remaining_ambiguity': d['amb'], 'coverage_strength_impact': impact, 'ratification': 'PROPOSED' if d['decision'] == 'CORRECT' else None,
                        'first_path': x['first_path'], 'source_kinds': x.get('source_kinds')})
    write_jsonl('PI012_NEGATIVE_MODALITY_REVIEW.jsonl', pi_rows)

    # ------- overmerge
    om_rows = []
    for x in rd('POTENTIAL_OVERMERGES.jsonl'):
        k = x['source_key']
        d = dec[k]
        om_rows.append({'candidate': x['candidate'], 'source_key': k, 'basis': x['basis'], 'decision': d['decision'], 'verdict': d['extra'].get('om'), 'rationale': d['why'], 'remaining_ambiguity': d['amb'], 'stored_subclauses': [{'subclause_id': s['subclause_id'], 'classification': s['classification'], 'modality': s.get('modality'), 'text': s.get('text')} for s in x.get('subclauses') or []],
                        'overlay_subclauses': (d['set'].get('subclauses_add') or []), 'correction_ids': cor_by_key.get(k, []), 'upstream_group_changed': False, 'primary_anchor': x['primary_anchor']})
    write_jsonl('OVERMERGE_REVIEW.jsonl', om_rows)

    # ------- orphans and new clauses
    orp_rows, ncp_rows = [], []
    for x in rd('ORPHAN_REVIEW_QUEUE.jsonl'):
        cid = 'ORP:' + x['item_id']
        d = dec[cid]
        c = x['candidate']
        ev = x.get('evidence_ref')
        row = {'candidate': c, 'item_id': x['item_id'], 'item_type': x['item_type'], 'decision': d['decision'], 'outcome': d['extra'].get('out'), 'reference': d['extra'].get('ref') or d['extra'].get('ncp'), 'rationale': d['why'], 'remaining_ambiguity': d['amb'], 'evidence_ref': ev, 'verified_quotes': quote_rows(c, d['quotes']), 'text': x.get('text'), 'prior_step2_note': x.get('review_note')}
        orp_rows.append(row)
        ledger.append({'case_id': cid, 'case_type': 'ORPHAN_ITEM', 'candidate': c, 'key': x['item_id'], 'memberships': targets[cid]['memberships'], 'decision': d['decision'], 'rationale': d['why'], 'tokens': {k: v for k, v in d['extra'].items() if k not in ('conf', 'notes')}, 'source': quote_rows(c, d['quotes']), 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[d['extra']['conf']], 'open': d['decision'] == 'UNRESOLVED', 'previous': {'status': x.get('status'), 'prior': x.get('prior')}})
        if d['extra'].get('out') == 'NEW_CLAUSE_PROPOSAL':
            ncp_rows.append({'proposal_id': d['extra']['ncp'], 'candidate': c, 'status': 'PROPOSED, separate from the 6,402 identities', 'proposed_clause': d['set']['proposed_clause'], 'classification': d['set']['classification'], 'modality': d['set']['modality'], 'trigger': d['set']['trigger'], 'related_policy_ids': d['set']['related_policy_ids'], 'distinguishing_scenario': d['set']['distinguishing_scenario'],
                             'evidence': quote_rows(c, d['quotes']), 'provenance': {'origin_item': x['item_id'], 'origin_type': x['item_type']}, 'rationale': d['why'], 'remaining_ambiguity': d['amb'], 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[d['extra']['conf']]})
    write_jsonl('ORPHAN_REVIEW.jsonl', orp_rows)
    write_jsonl('NEW_CLAUSE_PROPOSALS.jsonl', ncp_rows)

    # ------- queue sample
    q_all = {x['queue_id']: x for x in rd('STEP1_QUEUE_DISPOSITIONS.jsonl')}
    q_rows = []
    for s in plan['queue_sample']:
        qid = s['queue_id']
        x = q_all[qid]
        d = dec['QUE:' + qid]
        sides = []
        for side in ('group_ids_a', 'group_ids_b'):
            for k in x[side]:
                r = all_base[k]
                sides.append({'side': side[-1], 'source_key': k, 'classification': r['classification'], 'modality': r['modality'], 'claim_text': r['claim_text'], 'source': anchor_src(r)})
        row = {'candidate': s['candidate'], 'queue_id': qid, 'stratum': s['stratum'], 'item_type': x['item_type'], 'subtype': x['subtype'], 'open_question': x.get('open_question'), 'mechanical_disposition': x['disposition'], 'decision': d['decision'], 'outcome': d['extra'].get('out'), 'reference': d['extra'].get('ref'), 'rationale': d['why'], 'lost_normative_subclause': False, 'incorrect_dedup': False, 'sides': sides, 'overlap_with_other_targets': sorted({m for c in sides for m in mem_of.get(c['source_key'], [])})}
        q_rows.append(row)
        ledger.append({'case_id': 'QUE:' + qid, 'case_type': 'QUEUE_ITEM', 'candidate': s['candidate'], 'key': qid, 'memberships': ['QUEUE_E'], 'decision': d['decision'], 'rationale': d['why'], 'tokens': {k: v for k, v in d['extra'].items() if k not in ('conf', 'notes')}, 'source': [c['source'] for c in sides], 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[d['extra']['conf']], 'open': d['decision'] == 'UNRESOLVED', 'previous': {'disposition': x['disposition']}})
    write_jsonl('QUEUE_SAMPLE_REVIEW.jsonl', q_rows)
    sampled = {s['queue_id'] for s in plan['queue_sample']}
    ext = []
    for x in q_all.values():
        if x['subtype'] == 'BROADER_NARROWER' and x['queue_id'] not in sampled:
            keys = x['group_ids_a'] + x['group_ids_b']
            hit = [k for k in keys if k in dec and dec[k]['decision'] == 'CORRECT']
            ext.append({'candidate': x['candidate'], 'queue_id': x['queue_id'], 'open_question': x.get('open_question'), 'group_keys': keys, 'lost_normative_subclause': False, 'incorrect_dedup': False, 'linked_corrections': hit,
                        'reviewed_as': 'Enlarged stratum after two label findings in the sampled broad-narrow items. All 76 items of this subtype were read as a list of paired claims with stored labels. No per-item decision besides the linked corrections.'})
    write_jsonl('QUEUE_BROAD_NARROW_EXTENSION.jsonl', ext)

    # ------- coverage review
    def cov_witnesses(c, p, note):
        names = re.findall(r'FG-[A-Z0-9]+-[0-9a-f]{10}', note or '')
        if not names:
            r = cov_base[c][p]
            names = sorted(set(r['strength_equivalent_source_keys'] + r['weaker_source_keys'] + r['stronger_source_keys']))[:8]
        out = []
        for k in dict.fromkeys(names):
            x = all_base.get(k)
            if not x:
                continue
            o = next((s for s in x.get('subclauses') or [] if p in cov_ids(s)), x)
            lnk = next((cc['coverage'] for cc in o.get('canonical_coverage') or [] if cc['policy_id'] == p), None)
            out.append({'source_key': k, 'classification': o.get('classification'), 'modality': o.get('modality'), 'link': lnk, 'strength_equivalence': o.get('normative_strength_equivalence'), 'source': anchor_src(x), 'corrected_by_audit': k in cor_by_key})
        return out
    cov_rows = []
    specials = set(SPECIAL_CELLS)
    for c in CANDIDATES:
        for p, r in cov_base[c].items():
            if not r.get('reviewer_override_note') and (c, p) not in specials:
                continue
            d = dec['COV:%s:%s' % (c, p)]
            ev = cov_eff[c][p]
            cov_rows.append({'candidate': c, 'policy_id': p, 'policy': policy_text(p), 'memberships': targets['COV:%s:%s' % (c, p)]['memberships'], 'baseline_status': r['status'], 'baseline_computed_status': r['computed_status'], 'baseline_strength_status': r['strength_status'], 'baseline_override_note': r.get('reviewer_override_note'),
                             'decision': d['decision'], 'outcome': d['extra'].get('out'), 'clause_review': d['why'], 'qualifier': (d['extra'].get('notes') or [None])[0], 'verified_quotes': quote_rows(c, d['quotes']), 'witnesses': cov_witnesses(c, p, r.get('reviewer_override_note')),
                             'effective_computed_status': ev['computed_status'], 'effective_strength_status': ev['strength_status'], 'parity_statement': 'DIRECT_EVIDENCE is traceability, not parity or compliance.', 'equivalent_asserted': False if (c, p) in specials else None, 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[d['extra']['conf']]})
            ledger.append({'case_id': 'COV:%s:%s' % (c, p), 'case_type': 'COVERAGE_ROW', 'candidate': c, 'key': '%s:%s' % (c, p), 'memberships': targets['COV:%s:%s' % (c, p)]['memberships'], 'decision': d['decision'], 'rationale': d['why'], 'tokens': {k: v for k, v in d['extra'].items() if k not in ('conf', 'notes')}, 'source': quote_rows(c, d['quotes']), 'canonical_policies': pols([p]), 'confidence': {'H': 'HIGH', 'M': 'MEDIUM', 'L': 'LOW'}[d['extra']['conf']], 'open': False, 'previous': {'status': r['status'], 'strength_status': r['strength_status']}})
    write_jsonl('COVERAGE_OVERRIDE_REVIEW.jsonl', cov_rows)

    ledger.sort(key=lambda r: r['case_id'])
    write_jsonl('AUDIT_LEDGER.jsonl', ledger)

    # ------- targets (frozen rows, then cases added while reading)
    t_rows = [dict(t, added_after_freeze=None) for t in targets.values()]
    for row in added:
        t_rows.append({'case_id': row['case_id'], 'case_type': 'RECORD', 'candidate': row['candidate'], 'key': row['key'], 'memberships': row['memberships'], 'list_refs': {}, 'added_after_freeze': row['added_after_freeze']})
    write_jsonl('AUDIT_TARGETS.jsonl', sorted(t_rows, key=lambda r: r['case_id']))

    # ------- queues
    unresolved = []
    for row in ledger:
        if row.get('open') and row['case_type'] == 'RECORD':
            unresolved.append({'case_id': row['case_id'], 'candidate': row['candidate'], 'key': row['key'], 'decision': row['decision'], 'reason': row['rationale'], 'alternatives': row.get('alternatives'), 'remaining_ambiguity': row.get('remaining_ambiguity'), 'stored_classification': row['previous'].get('classification'), 'stored_modality': row['previous'].get('modality'), 'correction_ids': row.get('correction_ids'), 'source': row['source'][-1] if row['source'] else None, 'question_type': open_question_type(row), 'step3_rule': 'Do not use as a strictness fact.'})
    write_jsonl('UNRESOLVED_QUEUE.jsonl', unresolved)
    hq = {q[0]: {'question_id': q[0], 'question': q[2], 'status': 'OPEN', 'type': 'POLICY', 'source_keys': [], 'candidates': set(), 'step2_fhd_entries': 0, **HQ_DETAIL[q[0]]} for q in QUESTIONS}
    for row in read_jsonl(os.path.join(S2, 'FUTURE_HUMAN_DECISIONS.jsonl')):
        t = row['future_human_decision']
        for qid, pat, _ in QUESTIONS:
            if re.search(pat, t, re.I):
                hq[qid]['step2_fhd_entries'] += 1
                break
    for case, x in dec.items():
        for h in x['hd']:
            for qid, pat, _ in QUESTIONS:
                if re.search(pat, h, re.I):
                    hq[qid]['source_keys'].append(case)
                    hq[qid]['candidates'].add(all_base[case.split('/')[0]]['candidate'] if case in all_base else '')
                    break
    fhd_map = []
    for row in rd('FUTURE_HUMAN_DECISIONS.jsonl'):
        t = row['future_human_decision']
        qid = next((q for q, pat, _ in QUESTIONS if re.search(pat, t, re.I)), None)
        fhd_map.append({'candidate': row['candidate'], 'source_key': row['source_key'], 'step2_question': t, 'genuine_human_decision': bool(qid), 'mapped_to': qid or 'RESOLVED_AS_SOURCE_READING', 'audit_decision': dec[row['source_key']]['decision']})
    write_jsonl('FHD_REVIEW.jsonl', fhd_map)
    rows = []
    for q in hq.values():
        q['candidates'] = sorted(q['candidates'], key=CANDIDATES.index)
        q['source_keys'] = sorted(set(q['source_keys']))
        rows.append(q)
    rows.append(METHODOLOGY_HQ)
    write_jsonl('HUMAN_DECISION_QUEUE.jsonl', rows)

    # ------- effective view
    overrides = {c: {p: r for p, r in cov_base[c].items() if r.get('reviewer_override_note')} for c in CANDIDATES}
    eff_rows_total = 0
    eff_all = []
    for c in CANDIDATES:
        for r0 in read_jsonl(os.path.join(S2, 'per_candidate', c, 'CLASSIFICATIONS.jsonl')):
            k = r0['source_key']
            r = eff[c][k]
            d = dec.get(k)
            subs_d = {case: dec[case] for case in dec if case.startswith(k + '/')}
            mems = mem_of.get(k, [])
            cids = cor_by_key.get(k, [])
            rat = sorted({co['ratification'] for co in corrections if co['source_key'] == k})
            if cids:
                st = 'PROPOSED_CORRECTION_APPLIED'
            elif d and d['decision'] == 'UNRESOLVED':
                st = 'UNRESOLVED_BASELINE_RETAINED'
            elif d or subs_d:
                st = 'AUDITED_UPHELD'
            else:
                st = 'BASELINE_NOT_AUDITED'
            ov = {'audit_version': AUDIT_VERSION, 'status': st, 'correction_ids': cids, 'ratification': rat, 'decision': d['decision'] if d else None, 'memberships': mems, 'alternatives': d['alt'] if d else [], 'remaining_ambiguity': d['amb'] if d else None,
                  'open_question': bool(d and (d['decision'] == 'UNRESOLVED' or d['extra'].get('open') == '1')), 'baseline_record_sha256': rec_hash(r0), 'modality_lead_a13': k in lead_keys, 'trigger_field_reads_as_loading_context': bool(LOADING_RE.match(r0.get('trigger') or '')) and r0.get('normativity') == 'NORMATIVE' and 'trigger' not in (d['set'] if d else {}),
                  'static_only': bool(re.search(r'\.claude/(hooks|scripts)/|settings\.json$', r0['primary_anchor']['path']))}
            out = dict(r)
            out['audit_overlay'] = ov
            eff_all.append(out)
            eff_rows_total += 1
    p = out_path('EFFECTIVE_CLASSIFICATIONS.jsonl')
    with open(p + '.tmp', 'w', encoding='utf-8', newline='\n') as f:
        for r in eff_all:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')
    os.replace(p + '.tmp', p)

    # ------- effective coverage
    review_by_cell = {(x['candidate'], x['policy_id']): x for x in cov_rows}
    cov_out, moved = [], []
    open_keys = {r['key'].split('/')[0] for r in ledger if r.get('open') and r['case_type'] == 'RECORD'}
    for c in CANDIDATES:
        eff_links = links_of(list(eff[c].values()))
        for r0 in read_jsonl(os.path.join(S2, 'per_candidate', c, 'POLICY_COVERAGE.jsonl')):
            p_ = r0['policy_id']
            ev, nop = cov_eff[c][p_], cov_no[c][p_]
            flags = []
            status_eff = r0['status'] if r0.get('reviewer_override_note') else ev['computed_status']
            rv = review_by_cell.get((c, p_))
            if rv:
                flags.append(rv['outcome'])
            if ev['strength_status'] != r0['strength_status']:
                flags.append('STRENGTH_STATUS_MOVED_BY_PROPOSAL')
            if nop['strength_status'] != ev['strength_status']:
                flags.append('DEPENDS_ON_PI012_RULE')
            if ev['computed_status'] != r0['computed_status']:
                flags.append('COMPUTED_STATUS_MOVED_BY_PROPOSAL')
            if flags and any(x in flags for x in ('STRENGTH_STATUS_MOVED_BY_PROPOSAL', 'COMPUTED_STATUS_MOVED_BY_PROPOSAL')):
                flags.append('REVIEW_REQUIRED')
            changed_links = sorted(k for k in set(ev['direct_source_keys'] + ev['partial_source_keys'] + ev['strength_equivalent_source_keys'] + ev['weaker_source_keys'] + ev['stronger_source_keys'] + r0['direct_source_keys'] + r0['partial_source_keys'] + r0['strength_equivalent_source_keys'] + r0['weaker_source_keys'] + r0['stronger_source_keys']) if k in cor_by_key)
            same_links = [l for l in eff_links.get(p_, []) if l['classification'] in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA') and l['equivalence'] in ('EQUIVALENT', 'PORTION_EQUIVALENT_WITH_REMAINDER') and l['resolution'] not in NOT_OWNER_CODES]
            basis = 'NONE' if not same_links else ('FULL_LINK' if any(l['link'] == 'FULL' for l in same_links) else 'PARTIAL_LINKS_ONLY')
            only_open = bool(same_links) and all(l['source_key'] in open_keys for l in same_links)
            row = dict(r0)
            row.update({k: ev[k] for k in ('computed_status', 'direct_source_keys', 'partial_source_keys', 'uncertain_source_keys', 'strength_status', 'strength_equivalent_source_keys', 'weaker_source_keys', 'stronger_source_keys', 'n_links')})
            row['status'] = status_eff
            row['audit_overlay'] = {'audit_version': AUDIT_VERSION, 'baseline': {k: r0[k] for k in ('status', 'computed_status', 'strength_status', 'direct_source_keys', 'partial_source_keys', 'uncertain_source_keys', 'strength_equivalent_source_keys', 'weaker_source_keys', 'stronger_source_keys', 'n_links', 'reviewer_override_note')},
                                    'baseline_row_sha256': rec_hash(r0), 'flags': flags, 'equal_strength_basis': basis, 'equal_strength_only_from_open_records': only_open, 'strength_status_without_pi012': nop['strength_status'], 'computed_status_without_pi012': nop['computed_status'], 'corrected_witnesses': changed_links,
                                    'support_level': 'CONDITIONALLY_SUPPORTED' if ('REVIEW_REQUIRED' in flags or 'OVERRIDE_CONFIRMED_WITH_QUALIFIER' in flags or 'STRENGTH_QUALIFIER_RETAINED' in flags) else 'TRACEABLE_NOT_PARITY', 'semantics': 'Traceability only. Not parity or compliance.'}
            if 'REVIEW_REQUIRED' in flags:
                moved.append({'candidate': c, 'policy_id': p_, 'baseline_strength': r0['strength_status'], 'effective_strength': ev['strength_status'], 'without_pi012': nop['strength_status'], 'baseline_computed': r0['computed_status'], 'effective_computed': ev['computed_status'], 'corrected_witnesses': changed_links})
            cov_out.append(row)
    write_jsonl('EFFECTIVE_POLICY_COVERAGE.jsonl', cov_out)

    # ------- PI-012 sensitivity
    def mod_count(rows):
        return dict(Counter(r.get('modality') for r in rows))
    sens = {'meaning': 'What moves if the proposed rule is accepted against not accepted. Not a strictness ranking. Counts of modality labels do not compare candidates.',
            'by_candidate': {}, 'cells_moved_vs_baseline': moved, 'n_pi012_dependent_corrections': sum(1 for co in corrections if co['depends_on'] == 'PI012')}
    for c in CANDIDATES:
        sens['by_candidate'][c] = {'baseline': mod_count(baseline(c).values()), 'rule_not_accepted': mod_count(eff_no_pi[c].values()), 'rule_accepted': mod_count(eff[c].values()),
                                   'n79_in_candidate': sum(1 for x in pi_rows if x['candidate'] == c), 'n79_corrected_needing_rule': sum(1 for x in pi_rows if x['candidate'] == c and x['needs_pi012_rule'] and x['outcome'] == 'CORRECT'), 'n79_corrected_no_rule': sum(1 for x in pi_rows if x['candidate'] == c and not x['needs_pi012_rule'] and x['outcome'] == 'CORRECT'), 'n79_upheld': sum(1 for x in pi_rows if x['candidate'] == c and x['outcome'] == 'UPHOLD'), 'n79_unresolved': sum(1 for x in pi_rows if x['candidate'] == c and x['outcome'] == 'UNRESOLVED')}
    write_json('PI012_SENSITIVITY.json', sens)

    # ------- sample agreement
    agree = {}
    for c, xs in list(plan['samples'].items()) + [('M', plan['m_calibration'])]:
        rows_ = []
        for s in xs:
            k = s['source_key']
            b = blind[k]
            r = all_base[k]
            rows_.append({'source_key': k, 'stratum': s['stratum'], 'blind_label': b['classification'], 'stored_label': r['classification'], 'label_agree': b['classification'] == r['classification'], 'blind_modality': b['modality'], 'stored_modality': r['modality'], 'modality_agree': b['modality'] == r['modality'], 'decision': dec[k]['decision'], 'corrected': k in cor_by_key})
        agree[c] = {'n': len(rows_), 'label_agree': sum(x['label_agree'] for x in rows_), 'modality_agree': sum(x['modality_agree'] for x in rows_), 'upheld': sum(x['decision'] == 'UPHOLD' for x in rows_), 'corrected': sum(x['corrected'] for x in rows_), 'rows': rows_}
    write_json('SAMPLE_AGREEMENT.json', {'meaning': 'Blind readings logged before stored fields were shown. Disagreement on a blind label does not mean a correction: many were fair alternatives under C2. Not an error rate.', 'by_candidate': agree})

    # ------- manifest
    files = ['EFFECTIVE_CLASSIFICATIONS.jsonl', 'EFFECTIVE_POLICY_COVERAGE.jsonl', 'CORRECTION_PROPOSALS.jsonl']
    base_files = {c: {'CLASSIFICATIONS.jsonl': sha256_file(os.path.join(S2, 'per_candidate', c, 'CLASSIFICATIONS.jsonl')), 'POLICY_COVERAGE.jsonl': sha256_file(os.path.join(S2, 'per_candidate', c, 'POLICY_COVERAGE.jsonl'))} for c in CANDIDATES}
    write_json('EFFECTIVE_VIEW_MANIFEST.json', {'audit_version': AUDIT_VERSION, 'status': 'PROPOSED QA OVERLAY, not a frozen baseline', 'baseline_sha256': base_files, 'view_sha256': {f: sha256_file(out_path(f)) for f in files},
                                                 'overlay_protocol': {'order': 'CORRECTION_PROPOSALS.jsonl row order', 'apply': 'overlay.apply_set(baseline record, set, subclause) then overlay.recompute_strength', 'coverage': 'overlay.coverage_of(effective records); override status kept where the row had a Step 2 override and the audit confirmed it', 'strip_rule': 'Removing audit_overlay and audit_subclauses from an unchanged row gives the baseline row exactly.'},
                                                 'counts': {'records': len(eff_all), 'coverage_rows': len(cov_out), 'corrections': len(corrections), 'by_ratification': dict(Counter(c['ratification'] for c in corrections)), 'by_class': dict(Counter(c['correction_class'] for c in corrections)), 'by_candidate': dict(Counter(c['candidate'] for c in corrections)),
                                                            'status_by_record': dict(Counter(r['audit_overlay']['status'] for r in eff_all)), 'effective_labels': dict(Counter(r['classification'] for r in eff_all)), 'baseline_labels': dict(Counter(r['classification'] for c in CANDIDATES for r in baseline(c).values()))}})
    print(json.dumps({'corrections': len(corrections), 'ledger': len(ledger), 'moved_cells': len(moved), 'ncp': len(ncp_rows), 'unresolved': len(unresolved), 'missing': sum(1 for r in ledger if r.get('audit_status') == 'MISSING_DECISION')}))
    print('labels', dict(Counter(r['classification'] for r in eff_all)))
    print('by ratification', dict(Counter(c['ratification'] for c in corrections)))
    print('by class', dict(Counter(c['correction_class'] for c in corrections)))
    print('by cand', dict(Counter(c['candidate'] for c in corrections)))
    print('moved', json.dumps(moved, ensure_ascii=False)[:1800])
    print('missing', [r['key'] for r in ledger if r.get('audit_status') == 'MISSING_DECISION'][:20])


if __name__ == '__main__':
    main()
