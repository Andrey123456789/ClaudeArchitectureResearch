"""Deterministic overlay engine: applies correction proposals to baseline records and recomputes coverage.

The strength and coverage logic mirrors Step 2's enrich.py and candidate.py (read-only reference) so a change of modality or
links moves the derived fields in the same way. Nothing here writes; build.py and validate.py call it.
"""
import copy
import re
from collections import defaultdict

from acommon import baseline, policies, read_jsonl

STRENGTH_RANK = {'MUST': 3, 'MUST_NOT': 3, 'DECIDED': 3, 'REQUIRES_APPROVAL': 3, 'DEFAULT': 2, 'SHOULD': 2, 'SHOULD_NOT': 2, 'MAY': 1}
SR_CODES = {'SL': 'SECONDARY_LINK_ONLY', 'PC': 'POLICY_CLAUSE_EQUIVALENT', 'CK': 'CHECK_BY_REFERENCE', 'CR': 'COROLLARY_GUIDANCE', 'PM': 'PERMISSION_WITHIN_POLICY',
            'AM': 'ADVISORY_MECHANISM', 'GR': 'GUIDANCE_RESTATEMENT', 'CN': 'CONDITIONAL_NARROWING'}
NOT_OWNER_CODES = {'CK', 'CR'}
WEAKER_CODES = {'AM', 'GR', 'CN', 'PM'}
EQ = {'SAME': 'EQUIVALENT', 'WEAKER': 'WEAKER_THAN_CANONICAL', 'STRONGER': 'STRONGER_THAN_CANONICAL', 'INCOMPARABLE': 'INCOMPARABLE', 'N/A': 'NOT_APPLICABLE', 'UNDETERMINED': 'INCOMPARABLE'}
RECORD_FIELDS = {'classification', 'normativity', 'domain', 'oracle_relation', 'canonical_coverage', 'modality', 'strength_vs_canonical', 'strength_resolution_code', 'trigger', 'exceptions',
                 'extra_fragment', 'extra_fragment_kind', 'distinguishing_scenario', 'confidence', 'review_needed', 'review_reason', 'future_human_decision', 'related_policy_ids', 'subclauses'}
OVERLAY_ONLY = {'subclauses_add', 'subclause_set'}
DERIVED = ('canonical_policy_ids', 'canonical_semantic_coverage', 'normative_strength_equivalence', 'strength_links', 'strength_mechanical_mismatch', 'strength_resolution')


def strength_relation(modality, policy_strength):
    a, b = STRENGTH_RANK.get(modality), STRENGTH_RANK.get(policy_strength)
    if a is None or b is None:
        return 'NOT_COMPARABLE'
    return 'SAME_CLASS' if a == b else ('RECORD_STRONGER' if a > b else 'RECORD_WEAKER')


def recompute_strength(obj):
    """Refresh the A1.2 axes on a record or subclause after its fields change."""
    cls, st = obj.get('classification'), obj.get('strength_vs_canonical')
    links = []
    for cov in obj.get('canonical_coverage') or []:
        tag = policies()[cov['policy_id']]['normative_strength']
        links.append({'policy_id': cov['policy_id'], 'policy_strength': tag, 'record_modality': obj.get('modality'), 'coverage': cov['coverage'],
                      'mechanical_relation': strength_relation(obj.get('modality'), tag)})
    eq = EQ.get(st, 'NOT_APPLICABLE')
    if cls == 'CANONICAL_PLUS_DELTA' and st == 'SAME':
        eq = 'PORTION_EQUIVALENT_WITH_REMAINDER'
    code = obj.get('strength_resolution_code')
    obj['canonical_policy_ids'] = [c['policy_id'] for c in obj.get('canonical_coverage') or []]
    obj['canonical_semantic_coverage'] = 'NONE' if not links else ('FULL' if all(l['coverage'] == 'FULL' for l in links) else 'PARTIAL')
    obj['normative_strength_equivalence'] = eq
    obj['strength_links'] = links
    obj['strength_mechanical_mismatch'] = any(l['mechanical_relation'] in ('RECORD_STRONGER', 'RECORD_WEAKER') for l in links)
    obj['strength_resolution'] = {'code': code, 'label': SR_CODES.get(code), 'note': None, 'source': 'audit overlay'} if code else None
    return obj


def apply_set(rec, sets, sub_key=None):
    """Apply one correction to a deep copy of a baseline record. Returns the changed record."""
    out = copy.deepcopy(rec)
    target = out
    if sub_key:
        target = next(s for s in out['subclauses'] if s.get('subclause_id') == sub_key)
    for f, v in sets.items():
        if f in OVERLAY_ONLY:
            continue
        if f not in RECORD_FIELDS:
            raise ValueError('illegal field %s' % f)
        target[f] = copy.deepcopy(v)
    if 'trigger' in sets and not sub_key:
        out['trigger_status'] = 'AUDIT'
    if 'exceptions' in sets and not sub_key:
        out['exceptions_status'] = 'AUDIT'
    if 'modality' in sets:
        target['modality_detail'] = sets['modality'] if 'modality_detail' in target else target.get('modality_detail')
    if sets.get('normativity') == 'NON_NORMATIVE' and not sub_key:
        out['trigger_status'] = 'NOT_APPLICABLE'
        out['exceptions_status'] = 'NOT_APPLICABLE'
    for sc in sets.get('subclauses') or []:
        pass
    if 'subclauses' in sets and not sub_key:
        out['subclauses'] = [recompute_strength(dict(s, origin='AUDIT_OVERLAY')) for s in copy.deepcopy(sets['subclauses'])]
    for sid, fields in (sets.get('subclause_set') or {}).items():
        s = next(x for x in out['subclauses'] if x.get('subclause_id') == sid)
        s.update(copy.deepcopy(fields))
        recompute_strength(s)
    if sets.get('subclauses_add'):
        out['audit_subclauses'] = [recompute_strength(dict(s, origin='AUDIT_OVERLAY')) for s in copy.deepcopy(sets['subclauses_add'])]
    if not set(sets) <= OVERLAY_ONLY:
        recompute_strength(target)
    return out


def links_of(rows):
    links = defaultdict(list)
    for r in rows:
        for sub in [None] + list(r.get('subclauses') or []):
            obj = sub or r
            cls = obj.get('classification')
            res = obj.get('strength_resolution') or {}
            for l in obj.get('strength_links') or []:
                kind = 'UNCERTAIN_LINK' if cls == 'UNCERTAIN' else l['coverage']
                if kind == 'FULL' and res.get('code') in NOT_OWNER_CODES:
                    kind = 'PARTIAL'
                links[l['policy_id']].append({'source_key': r['source_key'], 'classification': cls, 'link': kind, 'confidence': r['confidence'],
                                              'equivalence': obj.get('normative_strength_equivalence'), 'resolution': res.get('code')})
    return links


def coverage_of(rows):
    """Same computation as candidate.py coverage(), without overrides. Returns policy -> derived fields."""
    links = links_of(rows)
    out = {}
    for pid in policies():
        ls = links.get(pid, [])
        canon = [l for l in ls if l['classification'] in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA')]
        full = [l for l in canon if l['link'] == 'FULL' and l['confidence'] in ('HIGH', 'MEDIUM')]
        part = [l for l in ls if l['link'] in ('PARTIAL', 'FULL') and l not in full and l['classification'] != 'UNCERTAIN']
        unc = [l for l in ls if l['link'] == 'UNCERTAIN_LINK']
        status = 'DIRECT_EVIDENCE' if full else ('PARTIAL_EVIDENCE' if part else ('UNCERTAIN' if unc else 'NOT_EVIDENCED'))
        same = sorted({l['source_key'] for l in canon if l['equivalence'] in ('EQUIVALENT', 'PORTION_EQUIVALENT_WITH_REMAINDER') and l['resolution'] not in NOT_OWNER_CODES})
        weaker = sorted({l['source_key'] for l in canon if l['equivalence'] == 'WEAKER_THAN_CANONICAL'})
        stronger = sorted({l['source_key'] for l in canon if l['equivalence'] == 'STRONGER_THAN_CANONICAL'})
        strength = ('EQUIVALENT_EVIDENCE_PRESENT' if same else 'STRONGER_AND_WEAKER_EVIDENCE' if weaker and stronger else 'ONLY_WEAKER_EVIDENCE' if weaker
                    else 'ONLY_STRONGER_EVIDENCE' if stronger else 'NO_STRENGTH_EVIDENCE')
        out[pid] = {'computed_status': status, 'direct_source_keys': sorted({l['source_key'] for l in full}), 'partial_source_keys': sorted({l['source_key'] for l in part}),
                    'uncertain_source_keys': sorted({l['source_key'] for l in unc}), 'strength_status': strength, 'strength_equivalent_source_keys': same,
                    'weaker_source_keys': weaker, 'stronger_source_keys': stronger, 'n_links': len(ls)}
    return out


def replay(corrections, cands):
    """Rebuild effective records for the given candidates from baseline plus correction rows, in row order."""
    eff = {c: dict(baseline(c)) for c in cands}
    for cor in corrections:
        c = cor['candidate']
        if c not in eff:
            continue
        base, _, sub = cor['case_key'].partition('/')
        eff[c][base] = apply_set(eff[c][base], cor['set'], sub or None)
    return eff
