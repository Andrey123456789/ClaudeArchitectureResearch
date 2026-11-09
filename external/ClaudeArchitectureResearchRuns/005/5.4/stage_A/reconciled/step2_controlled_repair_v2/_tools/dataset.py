"""Builds REPAIRED_CANDIDATE_DERIVED_VIEW deterministically from the frozen baseline. Ported from v1 R26.

Order: baseline; R01 overlay; rule overlays (R15, R17, R19, R20) in rule order; accepted R25 corrections in row order; R26 post-edit claim updates; v2 change updates in change order; added claims (v1, then v2, with stated v2 replacements); R21 proposals; derived applicability and delivery fields; current evidence mapping; coverage recomputed.
Frozen baseline files are read only. Replay of the same inputs gives the same bytes. V1_TO_V2_CROSSWALK.jsonl compares the result with v1's view, read by reference.
"""
import copy
import importlib.util
import json
import os
import sys
from collections import Counter

from order import V2_ORDER
from rcommon import CANDIDATES, baseline, coverage, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, sha256_file, utf8_stdout, v1_path, wc_path, write_json, write_jsonl
from roverlay import apply_fields, coverage_of, effective_status, recompute_strength, target_of
from triggers import derive
from witness import FileMap, load_dispositions, map_ref, norm_stream, rel_of

OV_RULES = ['R15-85-HTTPTIMEOUT', 'R17-87-SECSCAN', 'R19-87-CIUPDATES', 'R20-92-K0DESER']
OVERLAY_ONLY = {'subclauses_add', 'subclause_set', 'subclauses'}


def load_py(rule, name):
    p = out_path('_rules', rule, name)
    spec = importlib.util.spec_from_file_location('m_' + rule.replace('-', '_') + name.replace('.', '_'), p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def split_key(k):
    return (k.split('/')[0], k.split('/')[1] if '/' in k else None)


def apply_set(rec, sets, sub=None):
    plain = {k: v for k, v in sets.items() if k not in OVERLAY_ONLY}
    out = apply_fields(rec, plain, sub) if plain else copy.deepcopy(rec)
    if sets.get('subclauses') is not None and not sub:
        out['subclauses'] = [recompute_strength(dict(s, origin='REPAIR')) for s in copy.deepcopy(sets['subclauses'])]
    for sid, fields in (sets.get('subclause_set') or {}).items():
        t = target_of(out, sid)
        t.update(copy.deepcopy(fields))
        recompute_strength(t)
    if sets.get('subclauses_add'):
        out['audit_subclauses'] = [recompute_strength(dict(s, origin='REPAIR')) for s in copy.deepcopy(sets['subclauses_add'])]
    return out


def apply_v2_set(rec, sets, sub=None):
    """For v2 updates. A stored strength reading stays, with its source, unless the update names strength_resolution_code. v1 rules keep apply_set, so they replay byte for byte."""
    out = apply_set(rec, sets, sub)
    if 'strength_resolution_code' not in sets:
        target_of(out, sub)['strength_resolution'] = copy.deepcopy(target_of(rec, sub).get('strength_resolution'))
    for sid, fields in (sets.get('subclause_set') or {}).items():
        if 'strength_resolution_code' not in fields:
            target_of(out, sid)['strength_resolution'] = copy.deepcopy(target_of(rec, sid).get('strength_resolution'))
    return out


def locate_quote(c, rel, quote, fm):
    s = fm.stream(c, rel)
    if not s:
        return None
    i = s[0].lower().find(norm_ws(quote).lower())
    if i < 0:
        return None
    return s[1][i], s[1][i + len(norm_ws(quote)) - 1]


def resolved_open_keys():
    """Open PI-012 records a v2 adjudication closed. A record reopens if its adjudication row is removed."""
    return {r['key'] for r in read_jsonl(out_path('PI012_REMAINING_ADJUDICATION.jsonl')) if r.get('result') == 'RESOLVED'}


def build(per_record=None, skip=()):
    state = {c: dict(baseline(c)) for c in CANDIDATES}
    trail = {}
    cand_of = {k: c for c in CANDIDATES for k in baseline(c)}

    def step(key, sets, tag, apply=apply_set):
        base, sub = split_key(key)
        c = cand_of[base]
        before = state[c][base]
        state[c][base] = apply(before, sets, sub)
        trail.setdefault(base, []).append(tag)
        if per_record is not None:
            per_record(c, base, tag)

    for o in read_jsonl(out_path('_rules', 'R01-HQ06-PI012', 'OVERLAY.jsonl')):
        step(o['key'], o['set'], 'R01-HQ06-PI012')
    for rule in OV_RULES:
        for o in load_py(rule, 'overlay.py').OVERLAY:
            step(o['key'], o['set'], rule)
    for o in read_jsonl(out_path('_rules', 'R25-COR103', 'OVERLAY.jsonl')):
        step(o['key'], o['set'], 'R25-COR103:%s' % o['correction_id'])
    u = load_py('R26-DATASET', 'updates.py')
    inactive = {}
    claims = {}
    added = [dict(a) for a in u.ADDED]

    def run_updates(updates, apply=apply_set):
        for key, e in updates.items():
            base, _ = split_key(key)
            sets = dict(e['set'])
            if e['sub']:
                sets['subclause_set'] = e['sub']
            if sets:
                step(key, sets, e['rule'], apply)
            else:
                trail.setdefault(base, []).append(e['rule'])
            if e['status'] == 'REMOVED':
                inactive[base] = e
            if e.get('claim') or e.get('append'):
                claims[base] = e

    run_updates(u.UPDATES)
    for rule in V2_ORDER:
        if rule in skip or not os.path.exists(out_path('_rules', rule, 'updates.py')):
            continue
        m = load_py(rule, 'updates.py')
        run_updates(getattr(m, 'UPDATES', {}), apply_v2_set)
        for a in added:
            if a['source_key'] in getattr(m, 'REPLACE_ADDED', {}):
                a.update(m.REPLACE_ADDED[a['source_key']])
                a['rule'] = rule
        added.extend(getattr(m, 'ADDED', []))
    closed = resolved_open_keys()
    open_keys = {r['id'].split('/')[0]: r['kind'] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r['status'] == 'OPEN' and r['id'].split('/')[0] not in closed}
    fm = FileMap()
    disp = load_dispositions()
    rows = {c: [] for c in CANDIDATES}
    crosswalk = []
    for c in CANDIDATES:
        for key, r in state[c].items():
            base_rec = baseline(c)[key]
            out = copy.deepcopy(r)
            refs, stat = [], Counter()
            for ref in base_rec.get('evidence_refs') or []:
                m = map_ref(fm, c, ref)
                rel = rel_of(ref['path'])
                entry = {'original_path': ref['path'], 'original_start_line': ref['start_line'], 'original_end_line': ref['end_line'], 'path': 'candidates/%s/template/%s' % (c, rel), 'status': m['status']}
                if m['status'] in ('SAME', 'MOVED'):
                    entry.update(start_line=m['start'], end_line=m['end'])
                else:
                    d = disp.get((c, rel, ref['start_line'], ref['end_line']))
                    entry['status'] = d['disposition'] if d else 'UNREVIEWED'
                    if d and d['disposition'] != 'REMOVED':
                        loc = locate_quote(c, rel, d['new_quote'], fm)
                        if loc:
                            entry.update(start_line=loc[0], end_line=loc[1], new_quote=d['new_quote'])
                        else:
                            entry['status'] = 'UNRESOLVED_QUOTE'
                refs.append(entry)
                stat[entry['status']] += 1
            status = 'UNCHANGED'
            if stat.get('MOVED'):
                status = 'MOVED'
            if stat.get('REWORDED') or stat.get('SPLIT'):
                status = 'REWORDED_CONTEXT'
            if key in claims:
                status = 'REWORDED'
            if key in inactive:
                status = 'REMOVED'
            out['claim_text_original'] = base_rec.get('claim_text')
            if key in claims:
                out['claim_text'] = claims[key].get('claim') or (base_rec.get('claim_text') + claims[key]['append'])
            out['current_evidence_refs'] = refs
            out['repair'] = {'status': status, 'rules': trail.get(key, []), 'note': (claims.get(key) or inactive.get(key) or {}).get('note'), 'active': key not in inactive, 'view': 'REPAIRED_CANDIDATE_DERIVED_VIEW', 'baseline_sha256': rec_hash(base_rec), 'open_question': open_keys.get(key)}
            out.update(derive(out))
            rows[c].append(out)
            crosswalk.append({'original_key': key, 'candidate': c, 'status': status, 'repaired_key': key if key not in inactive else None, 'new_ids': [], 'rules': trail.get(key, []), 'classification_before': base_rec['classification'], 'classification_after': out['classification'], 'modality_before': base_rec.get('modality'), 'modality_after': out.get('modality'),
                              'claim_changed': key in claims, 'range_status': dict(stat), 'original_primary_anchor': (base_rec.get('evidence_refs') or [{}])[0].get('path'), 'baseline_sha256': rec_hash(base_rec), 'repaired_sha256': rec_hash(out)})
    # added claims and proposals: new stable ids
    for a in added:
        c = a['candidate']
        loc = locate_quote(c, a['path'], a['quote'], fm)
        rec = {'protocol_version': 'step2-v1', 'protocol_addendum': 'A1+A2-PI012', 'candidate': c, 'source_key': a['source_key'], 'view_record_type': 'REPAIR_ADDED_CLAIM', 'classification': a['classification'], 'normativity': 'NORMATIVE', 'domain': a['domain'],
               'oracle_relation': {'CANONICAL_PLUS_DELTA': 'PARTIALLY_ENTAILED'}.get(a['classification'], 'NOT_ENTAILED'), 'canonical_coverage': a['canonical_coverage'], 'modality': a['modality'], 'trigger': a['trigger'], 'trigger_status': 'REPAIR', 'exceptions': a['exceptions'], 'exceptions_status': 'REPAIR', 'scope': a['path'], 'loading_context': a['path'],
               'claim_text': a['claim_text'], 'claim_text_original': None, 'extra_fragment': a['extra_fragment'], 'extra_fragment_kind': a['extra_fragment_kind'], 'distinguishing_scenario': a['distinguishing_scenario'], 'related_policy_ids': a['related_policy_ids'], 'confidence': a['confidence'], 'subclauses': [], 'review_needed': False, 'strength_vs_canonical': 'SAME' if a['canonical_coverage'] else 'N/A', 'strength_resolution_code': None,
               'current_evidence_refs': [{'path': 'candidates/%s/template/%s' % (c, a['path']), 'status': 'ADDED' if loc else 'UNRESOLVED_QUOTE', 'start_line': loc[0] if loc else None, 'end_line': loc[1] if loc else None, 'new_quote': a['quote']}],
               'repair': {'status': 'ADDED', 'rules': [a['rule']], 'note': None, 'active': True, 'view': 'REPAIRED_CANDIDATE_DERIVED_VIEW'}}
        recompute_strength(rec)
        rec.update(derive(rec))
        rows[c].append(rec)
        crosswalk.append({'original_key': None, 'candidate': c, 'status': 'ADDED', 'repaired_key': a['source_key'], 'new_ids': [a['source_key']], 'rules': [a['rule']], 'classification_before': None, 'classification_after': a['classification'], 'modality_before': None, 'modality_after': a['modality'], 'claim_changed': True, 'repaired_sha256': rec_hash(rec)})
    for p in read_jsonl(out_path('NEW_CLAUSES_4_ADJUDICATION.jsonl')):
        c = p['candidate']
        rec = {'protocol_version': 'step2-v1', 'protocol_addendum': 'A1+A2-PI012', 'candidate': c, 'source_key': p['proposal_id'], 'view_record_type': 'REPAIR_PROPOSED_CANDIDATE_SPECIFIC_CLAUSE', 'classification': p['classification'], 'normativity': 'NORMATIVE', 'domain': 'PRODUCT_ENGINEERING' if p['classification'] == 'EXTRA_PRODUCT' else 'WORKFLOW_ENFORCEMENT', 'oracle_relation': 'NOT_ENTAILED', 'canonical_coverage': [], 'modality': p['modality'], 'trigger': None, 'trigger_status': 'REPAIR', 'scope': p['current_evidence']['path'], 'loading_context': p['current_evidence']['path'],
               'claim_text': p['proposed_clause'], 'claim_text_original': None, 'related_policy_ids': p['related_policy_ids'], 'confidence': p['confidence'], 'subclauses': [], 'strength_vs_canonical': 'N/A', 'strength_resolution_code': None, 'distinguishing_scenario': p['distinguishing_scenario'], 'current_evidence_refs': [p['current_evidence']], 'repair': {'status': 'ADDED', 'rules': ['R21-10-NEWCLAUSES'], 'note': 'Proposal, not promoted.', 'active': True, 'view': 'REPAIRED_CANDIDATE_DERIVED_VIEW'}}
        recompute_strength(rec)
        rec.update(derive(rec))
        rows[c].append(rec)
        crosswalk.append({'original_key': None, 'candidate': c, 'status': 'ADDED', 'repaired_key': p['proposal_id'], 'new_ids': [p['proposal_id']], 'rules': ['R21-10-NEWCLAUSES'], 'classification_before': None, 'classification_after': p['classification'], 'modality_before': None, 'modality_after': p['modality'], 'claim_changed': True, 'repaired_sha256': rec_hash(rec)})
    return rows, crosswalk


def coverage_rows(rows):
    out, moved = [], []
    for c in CANDIDATES:
        active = [r for r in rows[c] if r['repair']['active']]
        by = {r['source_key']: r for r in active}
        cov = coverage_of(active)
        for pid, row in cov.items():
            st = effective_status(c, pid, row)
            base = coverage(c)[pid]
            keys = sorted(set(row['direct_source_keys']) | set(row['partial_source_keys']) | set(row['strength_equivalent_source_keys']))
            wit = []
            for k in keys[:40]:
                r = by[k]
                refs = [x for x in r['current_evidence_refs'] if x.get('start_line')]
                wit.append({'source_key': k, 'status': r['repair']['status'], 'path': refs[0]['path'] if refs else None, 'start_line': refs[0]['start_line'] if refs else None, 'delivery_context': r.get('delivery_context')})
            line = dict(row, candidate=c, policy_id=pid, policy_name=policies()[pid]['name'], normative_strength=policies()[pid]['normative_strength'], status=st, reviewer_override_note=base.get('reviewer_override_note'), baseline_status=base['status'], baseline_strength_status=base['strength_status'], strength_status_changed=row['strength_status'] != base['strength_status'], status_changed=st != base['status'], witnesses=wit, semantics='Witnesses and their delivery_context show traceability and technical reachability. strength_status is the semantic descriptor. Neither is parity or compliance.', view='REPAIRED_CANDIDATE_DERIVED_VIEW')
            out.append(line)
            if st != base['status'] or row['strength_status'] != base['strength_status']:
                moved.append('%s %s: status %s -> %s; strength %s -> %s' % (c, pid, base['status'], st, base['strength_status'], row['strength_status']))
    return out, moved


def v1_to_v2(rows):
    """One row per v2 record: what changed against v1's view. Fields come from the two stored views; nothing is inferred."""
    v1 = {r['source_key']: r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    out = []
    seen = set()
    for r in rows:
        k = r['source_key']
        seen.add(k)
        o = v1.get(k)
        if o is None:
            out.append({'source_key': k, 'candidate': r['candidate'], 'status': 'ADDED_V2', 'v2_rules': r['repair']['rules'], 'changed_fields': [], 'v1_sha256': None, 'v2_sha256': rec_hash(r)})
            continue
        changed = sorted(f for f in set(o) | set(r) if o.get(f) != r.get(f))
        semantic = [f for f in changed if f not in ('current_evidence_refs', 'repair')]
        repair_rules = o['repair']['rules'] != r['repair']['rules']
        if not changed:
            status = 'UNCHANGED'
        elif o['repair'].get('active') != r['repair'].get('active'):
            status = 'ACTIVE_STATE_CHANGED'
        elif 'claim_text' in semantic:
            status = 'CLAIM_REWORDED'
        elif any(f in semantic for f in ('classification', 'modality', 'canonical_coverage', 'normativity', 'strength_vs_canonical', 'subclauses')):
            status = 'CLASSIFICATION_CHANGED'
        elif semantic:
            status = 'FIELD_CHANGED'
        elif repair_rules:
            status = 'RULE_TRAIL_CHANGED'
        else:
            status = 'ANCHOR_SHIFT_ONLY'
        out.append({'source_key': k, 'candidate': r['candidate'], 'status': status, 'v2_rules': [t for t in r['repair']['rules'] if t not in o['repair']['rules']], 'changed_fields': changed, 'classification_v1': o.get('classification'), 'classification_v2': r.get('classification'), 'modality_v1': o.get('modality'), 'modality_v2': r.get('modality'), 'v1_sha256': rec_hash(o), 'v2_sha256': rec_hash(r)})
    for k, o in v1.items():
        if k not in seen:
            out.append({'source_key': k, 'candidate': o['candidate'], 'status': 'LOST', 'v2_rules': [], 'changed_fields': [], 'v1_sha256': rec_hash(o), 'v2_sha256': None})
    return out


def main():
    utf8_stdout()
    rows, cross = build()
    cov, moved = coverage_rows(rows)
    all_rows = [r for c in CANDIDATES for r in rows[c]]
    write_jsonl('REPAIRED_CLASSIFICATIONS.jsonl', all_rows)
    write_jsonl('REPAIRED_POLICY_COVERAGE.jsonl', cov)
    write_jsonl('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl', cross)
    cs = Counter(r['status'] for r in cross)
    labels_before = Counter(baseline(c)[k]['classification'] for c in CANDIDATES for k in baseline(c))
    active = [r for r in all_rows if r['repair']['active']]
    man = {'version': 'step2-controlled-repair-v2', 'at': now(), 'view': 'REPAIRED_CANDIDATE_DERIVED_VIEW', 'frozen_baseline_reference': 'FROZEN_BASELINE_REFERENCE is step2_classification/per_candidate/*, unchanged: 6,402 classification identities and 1,176 policy rows with original anchors', 'counts': {'baseline_records': 6402, 'repaired_rows': len(all_rows), 'active_rows': len(active), 'inactive_removed_rows': len(all_rows) - len(active), 'added_claims': sum(1 for r in all_rows if r.get('view_record_type') == 'REPAIR_ADDED_CLAIM'), 'proposed_clauses': sum(1 for r in all_rows if r.get('view_record_type') == 'REPAIR_PROPOSED_CANDIDATE_SPECIFIC_CLAUSE'),
           'by_crosswalk_status': dict(cs), 'by_candidate': {c: len(rows[c]) for c in CANDIDATES}, 'labels_baseline': dict(labels_before), 'labels_repaired_active': dict(Counter(r['classification'] for r in active)), 'modality_repaired_active': dict(Counter(r.get('modality') for r in active)), 'applicability_status': dict(Counter(r.get('applicability_status') for r in all_rows)), 'delivery_status': dict(Counter(r.get('delivery_status') for r in all_rows)), 'coverage_rows': len(cov), 'coverage_status': dict(Counter(r['status'] for r in cov)), 'coverage_or_strength_moved': moved, 'evaluation_scope_marked': sum(1 for r in all_rows if r.get('evaluation_scope'))},
           'not_verified_statement': 'The applicability fields are derived, not individually verified. Most records were not re-read in this run.', 'replay': 'PYTHONPATH=_tools python -B _tools/dataset.py', 'sha256': {n: sha256_file(out_path(n)) for n in ('REPAIRED_CLASSIFICATIONS.jsonl', 'REPAIRED_POLICY_COVERAGE.jsonl', 'ORIGINAL_TO_REPAIRED_CLAIMS.jsonl')}}
    write_json('REPAIRED_VIEW_MANIFEST.json', man)
    v1v2 = v1_to_v2(all_rows)
    write_jsonl('V1_TO_V2_CROSSWALK.jsonl', v1v2)
    write_json('DATASET_MANIFEST.json', dict(man, v1_to_v2={'by_status': dict(Counter(r['status'] for r in v1v2)), 'rows': len(v1v2), 'sha256': sha256_file(out_path('V1_TO_V2_CROSSWALK.jsonl'))}, views={'FROZEN_BASELINE_REFERENCE': 'stage_A/reconciled/step2_classification/per_candidate/*: original anchors, untouched', 'V1_REPAIRED_VIEW': 'stage_A/reconciled/step2_controlled_repair_v1/REPAIRED_*.jsonl: anchors on v1 candidate bytes, untouched', 'V2_REPAIRED_VIEW': 'REPAIRED_*.jsonl in this folder: anchors on candidates/<C>/template/ in this folder'}, warning='Line anchors of the three views are not interchangeable. Never mix them in one count.'))
    print(json.dumps(man['counts'], ensure_ascii=False)[:2500])


if __name__ == '__main__':
    main()
