"""Global finalization and mechanical validation of Stage A / Step 2 (protocol step2-v1 with Addendum A1).

  python -B _tools/finalize.py build     writes the aggregate files from per_candidate/ and the immutable inputs
  python -B _tools/finalize.py validate  runs every gate and writes VALIDATION_RESULT.json; exit 1 on any FAIL

A PASS here is structural: it does not prove that a reading is right. Nothing outside step2_classification/ is
written, and the running Codex Pass 2 search is neither read nor hashed.
"""
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

from common import (AUG, CANDIDATES, OUT, P1, ROOT, S1, TOOLS, PROTOCOL_VERSION, facets, policies, proposals, read_jsonl,
                    sha256_file, source_key, union_view, write_json_atomic, write_jsonl_atomic)
from candidate import orphan_items, validate as validate_candidate
from enrich import rows_needing_strength_review, verify_record
import a13_audit

EXPECTED = {'records': 6402, 'ORIGINAL_GROUP': 6347, 'PROVISIONAL_NEW_CLAUSE': 26, 'PROVISIONAL_FACET_OVERLAY': 29,
            'coverage_rows': 1176, 'policies': 196, 'pending_orphans': 223, 'conflicts': 43, 'unresolved': 4,
            'pass1_issues': 17, 'merge_queue': 4915}
STATUSES = ('DIRECT_EVIDENCE', 'PARTIAL_EVIDENCE', 'NOT_EVIDENCED', 'UNCERTAIN')


def out(*p):
    return os.path.join(OUT, *p)


def rows_of(c):
    return read_jsonl(out('per_candidate', c, 'CLASSIFICATIONS.jsonl'))


def anchor_of(r):
    a = r.get('primary_anchor') or {}
    return {'path': a.get('path'), 'start_line': a.get('start_line'), 'end_line': a.get('end_line')}


def short(r):
    return {'candidate': r['candidate'], 'source_key': r['source_key'], 'view_record_type': r['view_record_type'],
            'classification': r['classification'], 'domain': r['domain'], 'modality': r['modality'], 'confidence': r['confidence'],
            'claim_text': r['claim_text'], 'primary_anchor': anchor_of(r), 'primary_quote': r.get('primary_quote'),
            'canonical_policy_ids': r['canonical_policy_ids'], 'related_policy_ids': r['related_policy_ids'],
            'protocol_version': PROTOCOL_VERSION}


def distinct_ranges(r):
    return sorted({(e['path'], e['start_line'], e['end_line']) for e in r['evidence_refs']})


def build_summary(all_rows):
    def tally(rows):
        res = {'n_records': len(rows)}
        for name, fn in [('by_class', lambda r: r['classification']), ('by_domain', lambda r: r['domain']),
                         ('by_oracle_relation', lambda r: r['oracle_relation']), ('by_certainty', lambda r: r['confidence']),
                         ('by_modality', lambda r: r['modality']), ('by_normativity', lambda r: r['normativity']),
                         ('by_view_record_type', lambda r: r['view_record_type']),
                         ('by_strength_equivalence', lambda r: r['normative_strength_equivalence']),
                         ('by_semantic_coverage', lambda r: r['canonical_semantic_coverage']),
                         ('by_quote_verification', lambda r: r['source_quote_verification']['status']),
                         ('by_primary_anchor_status', lambda r: r['source_quote_verification']['primary_anchor_status'])]:
            res[name] = dict(sorted(Counter(fn(r) for r in rows).items()))
        refs = Counter()
        locs = Counter()
        for r in rows:
            refs.update(r['source_quote_verification']['ref_status_counts'])
            locs.update(e.get('location_status') or 'NOT_RECORDED' for e in r['evidence_refs'])
        res['evidence_quality'] = {'reference_check_status': dict(sorted(refs.items())), 'reference_location_status': dict(sorted(locs.items())),
                                   'records_with_single_range': sum(len(distinct_ranges(r)) == 1 for r in rows),
                                   'records_with_multiple_ranges': sum(len(distinct_ranges(r)) > 1 for r in rows)}
        res['subclauses'] = dict(sorted(Counter(s['classification'] for r in rows for s in r.get('subclauses') or []).items()))
        res['facets'] = dict(sorted(Counter(r.get('facet_assessment') for r in rows if r['view_record_type'] == 'PROVISIONAL_FACET_OVERLAY').items()))
        res['review_needed'] = sum(bool(r['review_needed']) for r in rows)
        res['corrected_records'] = sum(bool(r['correction_history']) for r in rows)
        return res

    summary = {'protocol_version': PROTOCOL_VERSION, 'protocol_addendum': 'A1',
               'note': 'Counts describe this classified dataset. They are not a strictness comparison or a quality ranking of candidates.',
               'total': tally([r for c in CANDIDATES for r in all_rows[c]]), 'by_candidate': {}}
    for c in CANDIDATES:
        t = tally(all_rows[c])
        cov = read_jsonl(out('per_candidate', c, 'POLICY_COVERAGE.jsonl'))
        t['policy_coverage'] = dict(sorted(Counter(x['status'] for x in cov).items()))
        t['policy_strength_status'] = dict(sorted(Counter(x['strength_status'] for x in cov).items()))
        t['coverage_reviewer_overrides'] = sum(bool(x.get('reviewer_override_note')) for x in cov)
        od = read_jsonl(out('per_candidate', c, 'ORPHAN_DISPOSITIONS.jsonl'))
        t['open_item_dispositions'] = dict(sorted(Counter(x['disposition'] for x in od).items()))
        ch = read_jsonl(out('per_candidate', c, 'SEMANTIC_CHALLENGES.jsonl'))
        t['semantic_challenges'] = {'n': len(ch), 'outcomes': dict(sorted(Counter(x['outcome'] for x in ch).items())),
                                    'resolutions': dict(sorted(Counter(x['resolution'] for x in ch).items()))}
        cor = out('per_candidate', c, 'CORRECTIONS.jsonl')
        ledger = read_jsonl(cor) if os.path.exists(cor) else []
        t['corrections'] = {'n': len(ledger), 'by_finding': dict(sorted(Counter(re.sub(r'-\d+$', '', x['finding_ref']) for x in ledger).items())),
                            'classification_changes': sum(x['classification_before'] != x['classification_after'] for x in ledger)}
        div = out('per_candidate', c, 'STRENGTH_DIVERGENCES.jsonl')
        t['strength_divergences'] = len(read_jsonl(div)) if os.path.exists(div) else 0
        summary['by_candidate'][c] = t
    return summary


def build_uncertain(all_rows):
    res = []
    for c in CANDIDATES:
        for r in all_rows[c]:
            reasons = []
            if r['classification'] == 'UNCERTAIN':
                reasons.append('UNCERTAIN_RECORD')
            subs = [s for s in r.get('subclauses') or [] if s['classification'] == 'UNCERTAIN']
            if subs:
                reasons.append('UNCERTAIN_SUBCLAUSE')
            if r['confidence'] == 'LOW':
                reasons.append('LOW_CONFIDENCE')
            if r['review_needed']:
                reasons.append('REVIEW_NEEDED')
            if not reasons:
                continue
            row = short(r)
            row.update({'reasons': reasons, 'review_reason': r['review_reason'], 'future_human_decision': r['future_human_decision'],
                        'uncertain_subclauses': [{'subclause_id': s['subclause_id'], 'text': s['text'], 'review_reason': s.get('review_reason')} for s in subs]})
            res.append(row)
    return res


def build_overmerges(all_rows):
    res = []
    for c in CANDIDATES:
        for r in all_rows[c]:
            ranges = distinct_ranges(r)
            if r['potential_overmerge']:
                basis = 'EXPLICIT_REVIEWER_FLAG'
            elif r['classification'] == 'MIXED' and len(ranges) > 1:
                basis = 'MIXED_RECORD_WITH_SEVERAL_SOURCE_RANGES'
            else:
                continue
            row = short(r)
            row.update({'basis': basis, 'overmerge_note': r['overmerge_note'], 'n_distinct_ranges': len(ranges),
                        'subclauses': [{'subclause_id': s['subclause_id'], 'classification': s['classification'], 'text': s['text']} for s in r.get('subclauses') or []],
                        'status': 'FOR_LATER_REVIEW: Step 1 groups stay unchanged; no split was performed in Step 2.'})
            res.append(row)
    return res


def build_fhd(all_rows):
    res = []
    for c in CANDIDATES:
        for r in all_rows[c]:
            if r['future_human_decision']:
                row = short(r)
                row.update({'future_human_decision': r['future_human_decision'], 'review_reason': r['review_reason']})
                res.append(row)
    return res


def build_orphan_queue(all_rows):
    res = []
    for c in CANDIDATES:
        by = {r['source_key']: r for r in all_rows[c]}
        for x in read_jsonl(out('per_candidate', c, 'ORPHAN_DISPOSITIONS.jsonl')):
            if x['disposition'] != 'QUEUE':
                continue
            linked = sorted(set((x.get('co_located_group_ids') or []) + (x.get('attached_source_keys') or [])) & set(by))
            noted = sorted(set(re.findall(r'FG-%s-[0-9a-f]{10}|AUG1-[A-Z]{2}-CIS-%s-\d{4}-[a-z]' % (c, c), x.get('note') or '')) & set(by))
            linked = sorted(set(linked) | set(noted))
            res.append({'candidate': c, 'item_id': x['item_id'], 'item_type': x['item_type'], 'text': x['text'], 'prior': x['prior'],
                        'review_note': x['note'], 'evidence_ref': x.get('evidence_ref'),
                        'related_evidence': [{'source_key': k, 'classification': by[k]['classification'], 'primary_anchor': anchor_of(by[k]),
                                              'primary_quote': by[k].get('primary_quote')} for k in linked],
                        'status': 'OPEN_FOR_LATER_REVIEW', 'protocol_version': PROTOCOL_VERSION})
    return res


def build_queue_dispositions(all_rows):
    keys = {c: {r['source_key']: r for r in all_rows[c]} for c in CANDIDATES}
    disp = {}
    for c in CANDIDATES:
        for x in read_jsonl(out('per_candidate', c, 'ORPHAN_DISPOSITIONS.jsonl')):
            disp[x['item_id']] = x
    res = []
    for q in read_jsonl(os.path.join(S1, 'MERGE_REVIEW_QUEUE.jsonl')):
        c = q['candidate']
        groups = (q.get('group_ids_a') or []) + (q.get('group_ids_b') or [])
        missing = [g for g in groups if g not in keys[c]]
        row = {'queue_id': q['queue_id'], 'candidate': c, 'item_type': q['item_type'], 'subtype': q.get('subtype'), 'group_ids_a': q.get('group_ids_a') or [],
               'group_ids_b': q.get('group_ids_b') or [], 'open_question': q.get('open_question'),
               'classifications': {g: keys[c][g]['classification'] for g in groups if g in keys[c]}, 'missing_group_ids': missing,
               'protocol_version': PROTOCOL_VERSION}
        if q['item_type'] in ('APPARENT_CONFLICT', 'UNRESOLVED'):
            d = disp.get(q['queue_id'])
            row['disposition'] = d['disposition'] if d else 'MISSING'
            row['disposition_basis'] = 'Reviewed one by one: per_candidate/%s/ORPHAN_DISPOSITIONS.jsonl' % c
            row['note'] = d['note'] if d else None
        else:
            row['disposition'] = 'GROUPS_CLASSIFIED_SEPARATELY' if q['item_type'] == 'RELATED_BUT_DISTINCT' else 'GROUPS_CLASSIFIED_FROM_SOURCE'
            row['disposition_basis'] = ('Mechanical record: every named group is classified. The batch view showed this item to the reviewer; '
                                        'it did not receive its own adjudication.')
        res.append(row)
    return res


def calibration_rows(all_rows):
    keys = {c: {r['source_key']: r for r in all_rows[c]} for c in CANDIDATES}
    res = []
    for cal in read_jsonl(out('CALIBRATION.jsonl')):
        final = keys[cal['candidate']][cal['source_key']]
        same_class = final['classification'] == cal['classification']
        same_subs = [s['classification'] for s in final.get('subclauses') or []] == [s['classification'] for s in cal.get('subclauses') or []]
        same_mod = final['modality'] == cal['modality']
        res.append({'candidate': cal['candidate'], 'source_key': cal['source_key'], 'calibration_classification': cal['classification'],
                    'final_classification': final['classification'], 'calibration_modality': cal['modality'], 'final_modality': final['modality'],
                    'agrees': same_class and same_subs and same_mod, 'classification_agrees': same_class and same_subs,
                    'correction_ids': [h['correction_id'] for h in final['correction_history']]})
    return res


def build(all_rows=None):
    all_rows = all_rows or {c: rows_of(c) for c in CANDIDATES}
    write_json_atomic(out('CLASSIFICATION_SUMMARY.json'), build_summary(all_rows))
    for name, rows in [('UNCERTAIN_CLASSIFICATIONS.jsonl', build_uncertain(all_rows)), ('POTENTIAL_OVERMERGES.jsonl', build_overmerges(all_rows)),
                       ('FUTURE_HUMAN_DECISIONS.jsonl', build_fhd(all_rows)), ('ORPHAN_REVIEW_QUEUE.jsonl', build_orphan_queue(all_rows)),
                       ('STEP1_QUEUE_DISPOSITIONS.jsonl', build_queue_dispositions(all_rows)), ('CALIBRATION_AGREEMENT.jsonl', calibration_rows(all_rows))]:
        write_jsonl_atomic(out(name), rows)
        print(name, len(rows))


class Gates:
    def __init__(self):
        self.items = []

    def add(self, gate, errors, detail=None):
        errors = list(errors)
        self.items.append({'gate': gate, 'status': 'PASS' if not errors else 'FAIL', 'n_errors': len(errors), 'errors': errors[:40], 'detail': detail})
        print('%-44s %s %s' % (gate, 'PASS' if not errors else 'FAIL %d' % len(errors), (str(errors[:3]) if errors else '')[:240]))


def gate_inputs(g):
    hashes = json.load(open(out('INPUT_HASHES.json'), encoding='utf-8'))
    table = hashes.get('files', hashes)
    bad = [p for p, h in table.items() if isinstance(h, str) and (not os.path.exists(os.path.join(ROOT, p)) or sha256_file(os.path.join(ROOT, p)) != h)]
    g.add('INPUT_SHA256_UNCHANGED', bad, {'n_files': len(table), 'covers': 'inputs/, step1_union key files, step1_union_augmented_pass1 key files'})


def gate_records(g, all_rows):
    errs = []
    view = union_view()
    if len(view) != EXPECTED['records']:
        errs.append('union view has %d records' % len(view))
    want = {(r['candidate'], source_key(r), r['view_record_type']) for r in view}
    have = []
    for c in CANDIDATES:
        for r in all_rows[c]:
            have.append((r['candidate'], r['source_key'], r['view_record_type']))
            if r['candidate'] != c:
                errs.append('wrong candidate file ' + r['source_key'])
    dup = [k for k, n in Counter(have).items() if n > 1]
    errs += ['duplicate %s' % (k,) for k in dup]
    errs += ['missing %s' % (k,) for k in want - set(have)]
    errs += ['unexpected %s' % (k,) for k in set(have) - want]
    types = Counter(k[2] for k in have)
    for t in ('ORIGINAL_GROUP', 'PROVISIONAL_NEW_CLAUSE', 'PROVISIONAL_FACET_OVERLAY'):
        if types[t] != EXPECTED[t]:
            errs.append('%s: %d, expected %d' % (t, types[t], EXPECTED[t]))
    g.add('ALL_6402_RECORDS_EXACTLY_ONCE', errs, {'total': len(have), 'by_type': dict(types), 'by_candidate': dict(Counter(k[0] for k in have))})


def gate_coverage(g, all_rows):
    errs = []
    pol = policies()
    if len(pol) != EXPECTED['policies']:
        errs.append('%d policies' % len(pol))
    total = 0
    status = Counter()
    for c in CANDIDATES:
        keys = {r['source_key'] for r in all_rows[c]}
        cov = read_jsonl(out('per_candidate', c, 'POLICY_COVERAGE.jsonl'))
        total += len(cov)
        if sorted(x['policy_id'] for x in cov) != sorted(pol):
            errs.append('%s: rows are not the 196 policies exactly once' % c)
        for x in cov:
            status[x['status']] += 1
            if x['status'] not in STATUSES:
                errs.append('%s %s: bad status %s' % (c, x['policy_id'], x['status']))
            cited = x['direct_source_keys'] + x['partial_source_keys'] + x['uncertain_source_keys']
            for k in cited:
                if k not in keys:
                    errs.append('%s %s cites unknown key %s' % (c, x['policy_id'], k))
            if x['status'] == 'DIRECT_EVIDENCE' and not cited:
                errs.append('%s %s DIRECT with no key' % (c, x['policy_id']))
            if x['status'] == 'DIRECT_EVIDENCE' and not x['direct_source_keys'] and not x.get('reviewer_override_note'):
                errs.append('%s %s DIRECT with no FULL link and no written override' % (c, x['policy_id']))
    if total != EXPECTED['coverage_rows']:
        errs.append('%d coverage rows' % total)
    g.add('ALL_1176_COVERAGE_ROWS_EXACTLY_ONCE', errs, {'total': total, 'by_status': dict(status)})


def gate_policy_ids(g, all_rows):
    pol = policies()
    errs = []
    for c in CANDIDATES:
        for r in all_rows[c]:
            ids = r['canonical_policy_ids'] + r['related_policy_ids'] + r['canonical_conflict_ids']
            for s in r.get('subclauses') or []:
                ids = ids + s['canonical_policy_ids']
            errs += ['%s: undefined %s' % (r['source_key'], p) for p in ids if p not in pol]
    g.add('NO_UNDEFINED_CANONICAL_IDS', errs)


def gate_evidence(g, all_rows):
    errs = []
    high = 0
    for c in CANDIDATES:
        for r in all_rows[c]:
            if not r['evidence_refs']:
                errs.append('no evidence ' + r['source_key'])
            qv, _ = verify_record(r)
            if qv['status'] not in ('VERIFIED', 'VERIFIED_WITH_RANGE_ONLY_REFS'):
                errs.append('%s: %s' % (r['source_key'], qv['failures'][:2]))
            if qv['primary_quote_sha256'] != r['source_quote_verification']['primary_quote_sha256']:
                errs.append('primary quote differs from the stored check ' + r['source_key'])
            if r['confidence'] == 'HIGH':
                high += 1
                if qv['primary_anchor_status'].startswith('FAILED'):
                    errs.append('HIGH with failed anchor ' + r['source_key'])
    g.add('EVIDENCE_RE_READ_FROM_IMMUTABLE_FILES', errs, {'high_confidence_records': high})


def gate_provisional(g, all_rows):
    errs = []
    keys = {r['source_key']: r for c in CANDIDATES for r in all_rows[c]}
    prop, fac = proposals(), facets()
    if len(prop) != EXPECTED['PROVISIONAL_NEW_CLAUSE']:
        errs.append('%d proposals in the Pass 1 file' % len(prop))
    if len(fac) != EXPECTED['PROVISIONAL_FACET_OVERLAY']:
        errs.append('%d facets in the Pass 1 file' % len(fac))
    errs += ['proposal not classified ' + k for k in prop if k not in keys]
    errs += ['facet not classified ' + k for k in fac if k not in keys]
    errs += ['facet without assessment ' + k for k in fac if k in keys and not keys[k].get('facet_assessment')]
    g.add('NO_SILENT_DROP_OF_PROPOSALS_OR_FACETS', errs, {'proposals': len(prop), 'facets': len(fac)})


def gate_open_items(g, all_rows):
    errs = []
    types = Counter()
    disp_total = Counter()
    queue_ids = set()
    for c in CANDIDATES:
        keys = {r['source_key'] for r in all_rows[c]}
        rows = read_jsonl(out('per_candidate', c, 'ORPHAN_DISPOSITIONS.jsonl'))
        want = {x['item_id'] for x in orphan_items(c)}
        have = [x['item_id'] for x in rows]
        if len(have) != len(set(have)) or set(have) != want:
            errs.append('%s: dispositions differ from the open items' % c)
        for x in rows:
            types[x['item_type']] += 1
            disp_total[x['disposition']] += 1
            if not (x.get('note') or '').strip():
                errs.append('%s has no note' % x['item_id'])
            if x['disposition'] in ('ATTACH', 'RESOLVED'):
                att = x.get('attached_source_keys') or []
                if not att:
                    errs.append('%s has no attached key' % x['item_id'])
                errs += ['%s attaches unknown key %s' % (x['item_id'], k) for k in att if k not in keys]
            if x['disposition'] == 'QUEUE':
                queue_ids.add(x['item_id'])
    for name, n in [('STEP1_ORPHAN_PENDING_REVIEW', EXPECTED['pending_orphans']), ('STEP1_QUEUE_APPARENT_CONFLICT', EXPECTED['conflicts']),
                    ('STEP1_QUEUE_UNRESOLVED', EXPECTED['unresolved']), ('PASS1_UNRESOLVED', EXPECTED['pass1_issues'])]:
        if types[name] != n:
            errs.append('%s: %d, expected %d' % (name, types[name], n))
    q = read_jsonl(out('ORPHAN_REVIEW_QUEUE.jsonl'))
    if {x['item_id'] for x in q} != queue_ids:
        errs.append('ORPHAN_REVIEW_QUEUE differs from the QUEUE dispositions')
    for x in q:
        if not x.get('evidence_ref') and not x.get('related_evidence'):
            errs.append('queue entry without evidence ' + x['item_id'])
    g.add('ORPHANS_CONFLICTS_UNRESOLVED_AND_PASS1_ISSUES_CLOSED', errs, {'item_types': dict(types), 'dispositions': dict(disp_total), 'open_queue': len(queue_ids)})


def gate_merge_queue(g):
    errs = []
    src = {q['queue_id'] for q in read_jsonl(os.path.join(S1, 'MERGE_REVIEW_QUEUE.jsonl'))}
    rows = read_jsonl(out('STEP1_QUEUE_DISPOSITIONS.jsonl'))
    ids = [x['queue_id'] for x in rows]
    if len(ids) != len(set(ids)) or set(ids) != src or len(ids) != EXPECTED['merge_queue']:
        errs.append('queue dispositions differ from MERGE_REVIEW_QUEUE (%d vs %d)' % (len(set(ids)), len(src)))
    errs += ['%s names unclassified groups %s' % (x['queue_id'], x['missing_group_ids']) for x in rows if x['missing_group_ids']]
    errs += ['%s has no disposition' % x['queue_id'] for x in rows if x['disposition'] == 'MISSING']
    g.add('STEP1_MERGE_QUEUE_ACCOUNTED', errs, {'n': len(ids), 'by_disposition': dict(Counter(x['disposition'] for x in rows))})


def gate_checkpoints(g, all_rows):
    errs = []
    n_batches = 0
    for c in CANDIDATES:
        plan = json.load(open(out('_batches', c + '.json'), encoding='utf-8'))
        batches = plan['batches']
        planned = set()
        for b in batches:
            bid = b['batch_id']
            n_batches += 1
            planned.update(x['source_key'] for x in b['records'])
            p = out('CHECKPOINTS', c, bid + '.checkpoint.json')
            if not os.path.exists(p):
                errs.append('%s %s: no checkpoint' % (c, bid))
                continue
            cp = json.load(open(p, encoding='utf-8'))
            if cp['status'] != 'COMPLETE':
                errs.append('%s %s: %s' % (c, bid, cp['status']))
            if sha256_file(out(cp['batch_file'])) != cp['batch_file_sha256']:
                errs.append('%s %s: batch file changed after its checkpoint' % (c, bid))
            if sha256_file(out('_decisions', c, bid + '.dec')) != cp['decision_file_sha256']:
                errs.append('%s %s: decision file changed after its checkpoint' % (c, bid))
            if cp['plan_sha256'] != plan['plan_sha256']:
                errs.append('%s %s: plan hash differs' % (c, bid))
        if planned != {r['source_key'] for r in all_rows[c]}:
            errs.append('%s: batch plan keys differ from the classification keys' % c)
        cc = json.load(open(out('CHECKPOINTS', c, 'CANDIDATE.checkpoint.json'), encoding='utf-8'))
        if cc['status'] not in ('PASS', 'COMPLETE') or cc['errors']:
            errs.append('%s: candidate checkpoint %s' % (c, cc['status']))
        cls = out('per_candidate', c, 'CLASSIFICATIONS.jsonl')
        want = (cc.get('files') or {}).get('CLASSIFICATIONS.jsonl')
        if want and sha256_file(cls) != want:
            errs.append('%s: CLASSIFICATIONS.jsonl differs from its candidate checkpoint' % c)
    g.add('CHECKPOINT_INTEGRITY', errs, {'batches': n_batches})


def gate_protocol(g):
    errs = []
    fr = json.load(open(out('PROTOCOL_FREEZE.json'), encoding='utf-8'))
    if sha256_file(out('CLASSIFICATION_PROTOCOL.md')) != fr['CLASSIFICATION_PROTOCOL.md']:
        errs.append('CLASSIFICATION_PROTOCOL.md differs from the frozen hash')
    cal = sha256_file(out('CALIBRATION.jsonl'))
    amended = [a.get('CALIBRATION.jsonl') for a in fr.get('amendments') or []]
    if cal != fr['CALIBRATION.jsonl'] and cal not in amended:
        errs.append('CALIBRATION.jsonl matches neither the frozen hash nor a recorded amendment')
    add = [a.get('PROTOCOL_ADDENDUM_A1.md') for a in fr.get('amendments') or []]
    if sha256_file(out('PROTOCOL_ADDENDUM_A1.md')) not in add:
        errs.append('PROTOCOL_ADDENDUM_A1.md hash is not recorded')
    g.add('PROTOCOL_FROZEN', errs, {'amendments': len(fr.get('amendments') or [])})


def gate_calibration(g, all_rows):
    rows = calibration_rows(all_rows)
    errs = ['%s: %s to %s with no correction' % (x['source_key'], x['calibration_classification'], x['final_classification'])
            for x in rows if not x['classification_agrees'] and not x['correction_ids']]
    g.add('CALIBRATION_AGREES_OR_HAS_A_CORRECTION', errs, {'n': len(rows), 'class_and_modality_agree': sum(x['agrees'] for x in rows),
                                                           'class_agree': sum(x['classification_agrees'] for x in rows),
                                                           'modality_differs': [x['source_key'] for x in rows if x['classification_agrees'] and not x['agrees']]})


def gate_semantic(g):
    errs = []
    detail = {}
    for c in CANDIDATES:
        ch = read_jsonl(out('per_candidate', c, 'SEMANTIC_CHALLENGES.jsonl'))
        fam = Counter()
        for x in ch:
            cl = x['classification_challenged']
            fam['EXTRA' if cl.startswith('EXTRA') else cl] += 1
            if x['resolution'] == 'OPEN_UNRESOLVED':
                errs.append('%s: open failed challenge %s' % (c, x['source_key']))
            if x['outcome'] == 'REVISED_NEEDED' and not x['resolved_by_corrections']:
                errs.append('%s: REVISED_NEEDED with no correction %s' % (c, x['source_key']))
        for need in ('CANONICAL_ONLY', 'NON_NORMATIVE', 'INTERNAL_ARCHITECTURE', 'EXTRA'):
            if not fam[need]:
                errs.append('%s: no challenge on %s' % (c, need))
        detail[c] = {'n': len(ch), 'revised': sum(x['outcome'] == 'REVISED_NEEDED' for x in ch)}
    g.add('SEMANTIC_CHALLENGES_RUN_AND_CLOSED', errs, detail)


def gate_strength(g, all_rows):
    errs = []
    for c in CANDIDATES:
        errs += ['%s %s: %s' % (c, k, why) for k, why in rows_needing_strength_review(all_rows[c])]
        for r in all_rows[c]:
            if r['trigger_status'] == 'MISSING':
                errs.append('no trigger ' + r['source_key'])
            if r['exceptions_status'] == 'MISSING':
                errs.append('no exceptions statement ' + r['source_key'])
    g.add('STRENGTH_TRIGGER_AND_EXCEPTIONS_RESOLVED', errs)
    rows = a13_audit.scan()
    cats = Counter(x['category'] for x in rows)
    errs = []
    for x in rows:
        if x['category'] != 'N' and not x['evidence_text'].startswith('Check-by-reference'):
            errs.append('%s still at %s with no marker' % (x['key'], x['modality']))
    g.add('A1_3_AUDIT_NO_UNMARKED_MUST_ON_TECHNIQUE_TEXT', errs, {'retained_flat_negatives': cats['N']})


def gate_corrections(g, all_rows):
    errs = []
    total = 0
    for c in CANDIDATES:
        p = out('per_candidate', c, 'CORRECTIONS.jsonl')
        if not os.path.exists(p):
            continue
        by = {r['source_key']: r for r in all_rows[c]}
        ledger = read_jsonl(p)
        total += len(ledger)
        for l in ledger:
            if not l.get('before_record') or not l.get('reason') or not l.get('after_record_sha256'):
                errs.append('%s lacks before, reason or after' % l['correction_id'])
            if not l.get('fields_changed'):
                errs.append('%s changes nothing' % l['correction_id'])
            if l['correction_id'] not in [h['correction_id'] for h in by[l['source_key']]['correction_history']]:
                errs.append('%s is not in the record history' % l['correction_id'])
    g.add('CORRECTIONS_HAVE_BEFORE_AFTER_PROVENANCE', errs, {'n': total})


def gate_candidates(g):
    errs = []
    for c in CANDIDATES:
        e, w, _, _ = validate_candidate(c)
        errs += ['%s: %s' % (c, x) for x in e]
    g.add('CANDIDATE_VALIDATORS', errs)


def gate_scope(g):
    errs = []
    needle = 'codex_' + 'iterative_search'
    for f in sorted(os.listdir(TOOLS)):
        if f.endswith('.py') and needle in open(os.path.join(TOOLS, f), encoding='utf-8').read():
            errs.append('%s names the running Codex search' % f)
    g.add('CODEX_PASS2_NOT_CONSUMED', errs, 'No tool in _tools names the path; the running search was not read or hashed.')


def gate_files(g):
    files = ['CLASSIFICATION_PROTOCOL.md', 'PROTOCOL_ADDENDUM_A1.md', 'CALIBRATION.jsonl', 'CLASSIFICATION_SUMMARY.json', 'ORPHAN_REVIEW_QUEUE.jsonl',
             'UNCERTAIN_CLASSIFICATIONS.jsonl', 'POTENTIAL_OVERMERGES.jsonl', 'FUTURE_HUMAN_DECISIONS.jsonl', 'COVERAGE_LIMITATIONS.md',
             'STEP2_CLASSIFICATION_REPORT.md', 'STEP1_QUEUE_DISPOSITIONS.jsonl', 'CALIBRATION_AGREEMENT.jsonl']
    for c in CANDIDATES:
        files += ['per_candidate/%s/%s' % (c, f) for f in ('CLASSIFICATIONS.jsonl', 'POLICY_COVERAGE.jsonl', 'CANDIDATE_REPORT.md', 'SEMANTIC_CHALLENGES.jsonl', 'ORPHAN_DISPOSITIONS.jsonl')]
    errs = ['missing ' + f for f in files if not os.path.exists(out(f))]
    errs += ['empty ' + f for f in files if os.path.exists(out(f)) and os.path.getsize(out(f)) == 0 and f != 'POTENTIAL_OVERMERGES.jsonl']
    g.add('DELIVERABLES_PRESENT', errs, {'n_files': len(files)})


def validate():
    all_rows = {c: rows_of(c) for c in CANDIDATES}
    g = Gates()
    gate_inputs(g)
    gate_records(g, all_rows)
    gate_coverage(g, all_rows)
    gate_policy_ids(g, all_rows)
    gate_evidence(g, all_rows)
    gate_provisional(g, all_rows)
    gate_open_items(g, all_rows)
    gate_merge_queue(g)
    gate_checkpoints(g, all_rows)
    gate_protocol(g)
    gate_calibration(g, all_rows)
    gate_semantic(g)
    gate_strength(g, all_rows)
    gate_corrections(g, all_rows)
    gate_candidates(g)
    gate_scope(g)
    gate_files(g)
    failed = [x['gate'] for x in g.items if x['status'] != 'PASS']
    res = {'protocol_version': PROTOCOL_VERSION, 'protocol_addendum': 'A1', 'validator': '_tools/finalize.py validate',
           'status': 'PASS' if not failed else 'FAIL', 'failed_gates': failed, 'at': time.strftime('%Y-%m-%dT%H:%M:%S'),
           'meaning': 'A structural PASS. It does not prove substantive accuracy; see COVERAGE_LIMITATIONS.md and SEMANTIC_CHALLENGES.',
           'gates': g.items}
    write_json_atomic(out('VALIDATION_RESULT.json'), res)
    print('OVERALL', res['status'], failed)
    return 0 if not failed else 1


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'build':
        build()
    elif cmd == 'validate':
        raise SystemExit(validate())
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
