"""Deterministic overlay and coverage engine for the repaired view.

The strength and coverage logic mirrors the audit's overlay.py and Step 2's enrich.py and candidate.py (read-only references), so a
modality change moves the derived fields in the same way. A Step 2 reviewer override keeps its DIRECT status only while its witnesses are live.
"""
import copy
from collections import defaultdict

from rcommon import CANDIDATES, baseline, coverage, policies

STRENGTH_RANK = {'MUST': 3, 'MUST_NOT': 3, 'DECIDED': 3, 'REQUIRES_APPROVAL': 3, 'DEFAULT': 2, 'SHOULD': 2, 'SHOULD_NOT': 2, 'MAY': 1}
SR_CODES = {'SL': 'SECONDARY_LINK_ONLY', 'PC': 'POLICY_CLAUSE_EQUIVALENT', 'CK': 'CHECK_BY_REFERENCE', 'CR': 'COROLLARY_GUIDANCE', 'PM': 'PERMISSION_WITHIN_POLICY', 'AM': 'ADVISORY_MECHANISM', 'GR': 'GUIDANCE_RESTATEMENT', 'CN': 'CONDITIONAL_NARROWING'}
NOT_OWNER_CODES = {'CK', 'CR'}
EQ = {'SAME': 'EQUIVALENT', 'WEAKER': 'WEAKER_THAN_CANONICAL', 'STRONGER': 'STRONGER_THAN_CANONICAL', 'INCOMPARABLE': 'INCOMPARABLE', 'N/A': 'NOT_APPLICABLE', 'UNDETERMINED': 'INCOMPARABLE'}
ALLOWED_MODALITY = {'MUST', 'MUST_NOT', 'SHOULD', 'SHOULD_NOT', 'DEFAULT', 'MAY', 'REQUIRES_APPROVAL', 'DECIDED', 'NONE', 'MIXED', 'UNCERTAIN', None}


def strength_relation(modality, policy_strength):
    a, b = STRENGTH_RANK.get(modality), STRENGTH_RANK.get(policy_strength)
    if a is None or b is None:
        return 'NOT_COMPARABLE'
    return 'SAME_CLASS' if a == b else ('RECORD_STRONGER' if a > b else 'RECORD_WEAKER')


def recompute_strength(obj):
    cls, st = obj.get('classification'), obj.get('strength_vs_canonical')
    links = []
    for cov in obj.get('canonical_coverage') or []:
        tag = policies()[cov['policy_id']]['normative_strength']
        links.append({'policy_id': cov['policy_id'], 'policy_strength': tag, 'record_modality': obj.get('modality'), 'coverage': cov['coverage'], 'mechanical_relation': strength_relation(obj.get('modality'), tag)})
    eq = EQ.get(st, 'NOT_APPLICABLE')
    if cls == 'CANONICAL_PLUS_DELTA' and st == 'SAME':
        eq = 'PORTION_EQUIVALENT_WITH_REMAINDER'
    code = obj.get('strength_resolution_code')
    obj['canonical_policy_ids'] = [c['policy_id'] for c in obj.get('canonical_coverage') or []]
    obj['canonical_semantic_coverage'] = 'NONE' if not links else ('FULL' if all(l['coverage'] == 'FULL' for l in links) else 'PARTIAL')
    obj['normative_strength_equivalence'] = eq
    obj['strength_links'] = links
    obj['strength_mechanical_mismatch'] = any(l['mechanical_relation'] in ('RECORD_STRONGER', 'RECORD_WEAKER') for l in links)
    obj['strength_resolution'] = {'code': code, 'label': SR_CODES.get(code), 'note': None, 'source': 'repair overlay'} if code else None
    return obj


def target_of(rec, sub):
    if not sub:
        return rec
    for s in rec.get('subclauses') or []:
        sid = s.get('subclause_id') or ''
        if sid == sub or sid.endswith('/' + sub):
            return s
    raise KeyError(sub)


def apply_fields(rec, fields, sub=None):
    out = copy.deepcopy(rec)
    t = target_of(out, sub)
    for f, v in fields.items():
        t[f] = copy.deepcopy(v)
    if 'trigger' in fields and not sub:
        out['trigger_status'] = 'REPAIR'
    if 'exceptions' in fields and not sub:
        out['exceptions_status'] = 'REPAIR'
    if 'modality' in fields and 'modality_detail' in t:
        t['modality_detail'] = fields['modality']
    if fields.get('normativity') == 'NON_NORMATIVE' and not sub:
        out['trigger_status'] = 'NOT_APPLICABLE'
        out['exceptions_status'] = 'NOT_APPLICABLE'
    recompute_strength(t)
    return out


def links_of(rows):
    links = defaultdict(list)
    for r in rows:
        for sub in [None] + list(r.get('subclauses') or []) + list(r.get('audit_subclauses') or []):
            obj = sub or r
            cls = obj.get('classification')
            res = obj.get('strength_resolution') or {}
            for l in obj.get('strength_links') or []:
                kind = 'UNCERTAIN_LINK' if cls == 'UNCERTAIN' else l['coverage']
                if kind == 'FULL' and res.get('code') in NOT_OWNER_CODES:
                    kind = 'PARTIAL'
                links[l['policy_id']].append({'source_key': r['source_key'], 'classification': cls, 'link': kind, 'confidence': r['confidence'], 'equivalence': obj.get('normative_strength_equivalence'), 'resolution': res.get('code')})
    return links


def coverage_of(rows):
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
        strength = 'EQUIVALENT_EVIDENCE_PRESENT' if same else 'STRONGER_AND_WEAKER_EVIDENCE' if weaker and stronger else 'ONLY_WEAKER_EVIDENCE' if weaker else 'ONLY_STRONGER_EVIDENCE' if stronger else 'NO_STRENGTH_EVIDENCE'
        out[pid] = {'computed_status': status, 'direct_source_keys': sorted({l['source_key'] for l in full}), 'partial_source_keys': sorted({l['source_key'] for l in part}), 'uncertain_source_keys': sorted({l['source_key'] for l in unc}),
                    'strength_status': strength, 'strength_equivalent_source_keys': same, 'weaker_source_keys': weaker, 'stronger_source_keys': stronger, 'n_links': len(ls)}
    return out


def effective_status(c, pid, computed):
    """A Step 2 written override keeps DIRECT only while a partial or direct witness remains."""
    base = coverage(c)[pid]
    if base.get('reviewer_override_note') and computed['computed_status'] in ('PARTIAL_EVIDENCE', 'DIRECT_EVIDENCE') and base['status'] == 'DIRECT_EVIDENCE':
        return 'DIRECT_EVIDENCE'
    return computed['computed_status']


def validate_candidate(c, rows_by_key, allow_added=False, removed=()):
    """Whole-dataset invariants for one candidate. Returns errors. rows_by_key holds active rows; removed lists baseline keys marked inactive."""
    errs = []
    if set(rows_by_key) - set(baseline(c)) and not allow_added:
        errs.append('%s: unknown keys %s' % (c, sorted(set(rows_by_key) - set(baseline(c)))[:5]))
    if set(baseline(c)) - set(rows_by_key) - set(removed):
        errs.append('%s: lost keys %s' % (c, sorted(set(baseline(c)) - set(rows_by_key) - set(removed))[:5]))
    pol = policies()
    for k, r in rows_by_key.items():
        for obj in [r] + list(r.get('subclauses') or []) + list(r.get('audit_subclauses') or []):
            if obj.get('modality') not in ALLOWED_MODALITY:
                errs.append('%s: bad modality %s' % (k, obj.get('modality')))
            for pid in obj.get('canonical_policy_ids') or []:
                if pid not in pol:
                    errs.append('%s: unknown policy %s' % (k, pid))
            if obj.get('classification') == 'CANONICAL_ONLY':
                if obj.get('normative_strength_equivalence') == 'STRONGER_THAN_CANONICAL':
                    errs.append('%s: CANONICAL_ONLY cannot be STRONGER' % k)
                if not obj.get('canonical_policy_ids'):
                    errs.append('%s: CANONICAL_ONLY with no policy' % k)
            if obj.get('normative_strength_equivalence') == 'WEAKER_THAN_CANONICAL' and not obj.get('strength_resolution') and obj.get('classification') in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA'):
                errs.append('%s: WEAKER without a resolution code' % k)
    cov = coverage_of(rows_by_key.values())
    if len(cov) != 196:
        errs.append('%s: coverage rows %d' % (c, len(cov)))
    for pid, row in cov.items():
        st = effective_status(c, pid, row)
        if st != 'DIRECT_EVIDENCE':
            errs.append('%s %s: coverage moved to %s' % (c, pid, st))
    return errs
