"""Compile reviewer decisions (_decisions/<C>/B###.dec) into classified records and checkpoint them.

  python -B build.py <C> <B###> [--check]     compile one batch; --check = parse/validate only, write nothing
  python -B build.py <C> <B###> --rebuild     overwrite an already checkpointed batch (logged)
  python -B build.py CAL                      compile _decisions/CALIBRATION.dec -> CALIBRATION.jsonl

Decision DSL (one record per numbered line; numbers are the [n] indices printed by view.py):

  <n> <CODE> [POLICY[~] ...] [m=..] [d=..] [o=..] [c=..] [k=..] [st=..] [fa=..] [cf=P,P] [rel=P,P] [!] [| note]
    x: extra (non-entailed) fragment          s: distinguishing scenario
    t: trigger override                       e: exceptions override        sc: scope override
    r: review reason (sets review_needed)     om: potential Step-1 overmerge note
    fhd: future human decision                ce: canonical entailment rationale override
    ev: path:start-end[;path:start-end]       (reviewer-cited evidence, path relative to template root)
    - <CODE> [POLICY..] [m=..] [d=..] [st=..] | subclause text     (MIXED subclauses)
        x: / s: / ev: / r:                   (indented >= 4: attach to the open subclause)

CODE: CO CANONICAL_ONLY, CD CANONICAL_PLUS_DELTA, XP EXTRA_PRODUCT, XW EXTRA_WORKFLOW,
      IA INTERNAL_ARCHITECTURE, NN NON_NORMATIVE, MX MIXED, UN UNCERTAIN.
POLICY~ = the record evidences only part of that policy (coverage PARTIAL).
m: M MN S SN D Y RA DC N U   d: PE WF IA MX NN UN   o: FE PE NE NA UN   c: H M L
k (delta kind of CD remainder): P W A   st (strength vs canonical): W weaker, S stronger, X incomparable
fa (facets only): AN additional normative obligation, FC factual clarification, UN uncertain
sr (A1 strength resolution): SL secondary link only, PC policy clause equivalent, CK check by reference,
   CR corollary guidance, PM permission within policy, AM advisory mechanism, GR guidance restatement, CN conditional narrowing
"""
import json
import os
import re
import sys
import time

from common import (OUT, ROOT, PROTOCOL_VERSION, KEY_FIELD, CLASS_CODES, DOMAIN_CODES, ORACLE_CODES,
                    MODALITY_CODES, MODALITIES, CONF_CODES, FACET_CODES, DELTA_KIND, POLICY_RE,
                    union_view, source_key, policies, policy_default_domain, record_anchor,
                    record_claim_text, record_evidence_refs, group_primary_clause, normalize_modality,
                    loading_context, facets, file_lines, sha256_file, sha256_text, read_jsonl,
                    write_jsonl_atomic, write_json_atomic, SR_CODES, strength_relation, is_unknown)

NORMATIVE_CLASSES = {'CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA', 'EXTRA_PRODUCT', 'EXTRA_WORKFLOW',
                     'INTERNAL_ARCHITECTURE'}
REC_RE = re.compile(r'^(\d+)\s+(CO|CD|XP|XW|IA|NN|MX|UN)\b(.*)$')
SUB_RE = re.compile(r'^(\s+)-\s+(CO|CD|XP|XW|IA|NN|UN)\b(.*)$')
CONT_RE = re.compile(r'^(\s+)(x|s|t|e|sc|r|om|fhd|ce|ev):\s?(.*)$')
DEFAULT_RATIONALE = {
    'CANONICAL_ONLY': 'Claim restates the cited policy obligation at the same strength, trigger and scope '
                      '(reviewer reading of claim, source text and policy text).',
    'NON_NORMATIVE': 'Explanatory, illustrative or descriptive text; it imposes no independent agent or '
                     'product behavior.',
    'INTERNAL_ARCHITECTURE': "Constrains the candidate's instruction-system architecture (ownership, loading, "
                             'routing, maintenance), not product code or the generated work itself.',
}


class DecErr(Exception):
    pass


def parse_tokens(rest, where):
    note = None
    if '|' in rest:
        rest, note = rest.split('|', 1)
        note = note.strip() or None
    out = {'pols': [], 'partial': set(), 'kv': {}, 'flag': False}
    for tok in rest.split():
        if tok == '!':
            out['flag'] = True
        elif '=' in tok:
            k, v = tok.split('=', 1)
            if k not in ('m', 'd', 'o', 'c', 'k', 'st', 'fa', 'cf', 'rel', 'sr'):
                raise DecErr('%s: unknown key %s' % (where, k))
            out['kv'][k] = v
        else:
            pid = tok.rstrip('~')
            if not POLICY_RE.match(pid) and pid not in ('GOV-017', 'GOV-018'):
                raise DecErr('%s: bad token %r' % (where, tok))
            if pid not in policies():
                raise DecErr('%s: undefined canonical policy %s' % (where, pid))
            if pid in out['pols']:
                raise DecErr('%s: duplicate policy %s' % (where, pid))
            out['pols'].append(pid)
            if tok.endswith('~'):
                out['partial'].add(pid)
    out['note'] = note
    return out


def parse_dec(path):
    with open(path, encoding='utf-8') as f:
        return parse_dec_lines(f.read().split('\n'), os.path.basename(path))


def parse_dec_lines(lines, label, first_line=1):
    recs, cur, sub = {}, None, None
    for ln, raw in enumerate(lines, first_line):
        where = '%s:%d' % (label, ln)
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        m = REC_RE.match(raw)
        if m:
            n = int(m.group(1))
            if n in recs:
                raise DecErr('%s: duplicate record index %d' % (where, n))
            cur = {'n': n, 'code': m.group(2), 'cont': {}, 'subs': [], 'src': where}
            cur.update(parse_tokens(m.group(3), where))
            recs[n] = cur
            sub = None
            continue
        m = SUB_RE.match(raw)
        if m:
            if cur is None:
                raise DecErr('%s: subclause before record' % where)
            sub = {'code': m.group(2), 'cont': {}, 'src': where}
            sub.update(parse_tokens(m.group(3), where))
            cur['subs'].append(sub)
            continue
        m = CONT_RE.match(raw)
        if m:
            if cur is None:
                raise DecErr('%s: continuation before record' % where)
            indent, key, val = len(m.group(1)), m.group(2), m.group(3).strip()
            target = sub if (sub is not None and indent >= 4) else cur
            if key in target['cont']:
                target['cont'][key] += ' ' + val
            else:
                target['cont'][key] = val
            continue
        raise DecErr('%s: unparseable line %r' % (where, raw[:80]))
    return recs


def parse_ev(cand, spec, where):
    refs = []
    for part in spec.split(';'):
        part = part.strip()
        if not part:
            continue
        m = re.match(r'^(.+?):(\d+)(?:-(\d+))?$', part)
        if not m:
            raise DecErr('%s: bad ev %r' % (where, part))
        p, s = m.group(1), int(m.group(2))
        e = int(m.group(3) or s)
        rel = 'output/template/' + p if not p.startswith('output/') else p
        try:
            n = len(file_lines(cand, rel))
        except FileNotFoundError:
            raise DecErr('%s: ev file not found %s' % (where, p))
        if not (1 <= s <= e <= n):
            raise DecErr('%s: ev range %d-%d outside 1-%d for %s' % (where, s, e, n, p))
        refs.append({'path': 'inputs/%s/%s' % (cand, rel), 'start_line': s, 'end_line': e,
                     'occurrence_id': None, 'excerpt_sha256': None, 'location_status': 'REVIEWER_CITED_RANGE_CHECKED'})
    return refs


def reported_modalities(r):
    if r['view_record_type'] == 'ORIGINAL_GROUP':
        vals = [l.get('reported_modality') for l in r['original_group']['original_labels']]
    elif r['view_record_type'] == 'PROVISIONAL_NEW_CLAUSE':
        vals = [r.get('modality')]
    else:
        vals = []
    return [v for v in vals if v and not str(v).upper().startswith('UNKNOWN')]


def derive_modality(r, d, where):
    if 'm' in d['kv']:
        v = d['kv']['m']
        if v not in MODALITY_CODES:
            raise DecErr('%s: bad modality code %s' % (where, v))
        return MODALITY_CODES[v], 'REVIEWER'
    reps = reported_modalities(r)
    base = {normalize_modality(v) for v in reps}
    base.discard(None) if len(base) > 1 else None
    if len(base) == 1 and None not in base:
        return base.pop(), 'REPORTED_CONSENSUS_REVIEWER_ACCEPTED'
    raise DecErr('%s: modality not derivable from reported %r; give m=' % (where, reps))


def norm_exc(x):
    if x is None:
        return 'NOT_REPORTED'
    s = ' '.join(str(x).split())
    if s.lower().rstrip('.') in ('', 'none', 'none stated', 'n/a', 'na', 'no exceptions', 'none reported', '-'):
        return 'NONE'
    return s


def domain_from_pols(pols):
    ds = [policy_default_domain(p) for p in pols]
    return ds[0] if ds else None


STRICT = False  # Addendum A1: set for batches compiled after the M review (see main)


def strength_check(cls, mod, pols, kv, where):
    """A1: a CANONICAL_* claim whose modality class differs from a cited policy tag needs an explicit decision."""
    if 'sr' in kv and kv['sr'] not in SR_CODES:
        raise DecErr('%s: bad sr=%s' % (where, kv['sr']))
    if not STRICT or cls not in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA'):
        return
    st = kv.get('st')
    rels = [strength_relation(mod, policies()[p]['normative_strength']) for p in pols]
    if cls == 'CANONICAL_ONLY' and st == 'S':
        raise DecErr('%s: CANONICAL_ONLY cannot be stronger than its policy (use CD)' % where)
    if st == 'W' and 'sr' not in kv:
        raise DecErr('%s: st=W needs sr=AM|GR|CN|PM' % where)
    if st is None and 'sr' not in kv and any(r in ('RECORD_STRONGER', 'RECORD_WEAKER') for r in rels):
        raise DecErr('%s: modality %s differs from %s; give st= or sr=' % (
            where, mod, [(p, policies()[p]['normative_strength']) for p, r in zip(pols, rels) if r != 'SAME_CLASS']))


def sub_record(cand, d, rec_mod, idx, where):
    cls = CLASS_CODES[d['code']]
    pols = d['pols']
    kv = d['kv']
    if cls in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA') and not pols:
        raise DecErr('%s: %s subclause needs policy ids' % (where, cls))
    if cls in ('CANONICAL_PLUS_DELTA', 'EXTRA_PRODUCT', 'EXTRA_WORKFLOW') and not d['cont'].get('s'):
        raise DecErr('%s: %s subclause needs s: scenario' % (where, cls))
    if cls == 'CANONICAL_PLUS_DELTA' and not d['cont'].get('x'):
        raise DecErr('%s: CD subclause needs x:' % where)
    if not d['note']:
        raise DecErr('%s: subclause needs | text' % where)
    if 'm' in kv:
        mod = MODALITY_CODES[kv['m']]
    elif cls == 'NON_NORMATIVE':
        mod = 'NONE'
    elif cls == 'UNCERTAIN':
        mod = rec_mod or 'UNCERTAIN'
    else:
        mod = rec_mod
    if mod is None:
        raise DecErr('%s: subclause modality needed (m=)' % where)
    dom = DOMAIN_CODES[kv['d']] if 'd' in kv else (
        {'EXTRA_PRODUCT': 'PRODUCT_ENGINEERING', 'EXTRA_WORKFLOW': 'WORKFLOW_ENFORCEMENT',
         'INTERNAL_ARCHITECTURE': 'INSTRUCTION_ARCHITECTURE', 'NON_NORMATIVE': 'NON_NORMATIVE',
         'UNCERTAIN': 'UNCERTAIN'}.get(cls) or domain_from_pols(pols))
    rel = {'CANONICAL_ONLY': 'FULLY_ENTAILED', 'CANONICAL_PLUS_DELTA': 'PARTIALLY_ENTAILED',
           'EXTRA_PRODUCT': 'NOT_ENTAILED', 'EXTRA_WORKFLOW': 'NOT_ENTAILED',
           'INTERNAL_ARCHITECTURE': 'NOT_APPLICABLE', 'NON_NORMATIVE': 'NOT_APPLICABLE',
           'UNCERTAIN': 'UNCERTAIN'}[cls]
    strength_check(cls, mod, pols, kv, where)
    st = {'W': 'WEAKER', 'S': 'STRONGER', 'X': 'INCOMPARABLE'}.get(kv.get('st'), 'SAME' if pols else 'N/A')
    ev = parse_ev(cand, d['cont']['ev'], where) if d['cont'].get('ev') else None
    if cls == 'EXTRA_PRODUCT' or cls == 'EXTRA_WORKFLOW':
        xf = d['cont'].get('x') or d['note']
    else:
        xf = d['cont'].get('x')
    return {
        'subclause_id': 'S%d' % idx, 'text': d['note'], 'classification': cls,
        'normativity': 'NON_NORMATIVE' if cls == 'NON_NORMATIVE' else ('UNCERTAIN' if cls == 'UNCERTAIN' else 'NORMATIVE'),
        'domain': dom, 'oracle_relation': rel, 'canonical_policy_ids': pols,
        'canonical_coverage': [{'policy_id': p, 'coverage': 'PARTIAL' if (p in d['partial'] or st == 'WEAKER') else 'FULL'} for p in pols],
        'modality': mod, 'strength_vs_canonical': st,
        'extra_fragment': xf, 'extra_fragment_kind': DELTA_KIND.get(kv.get('k')) if cls == 'CANONICAL_PLUS_DELTA' else None,
        'distinguishing_scenario': d['cont'].get('s'),
        'review_reason': d['cont'].get('r'),
        'strength_resolution_code': kv.get('sr'),
        'evidence_refs': ev,
    }


def build_record(r, d, batch_id, where):
    cand = r['candidate']
    t = r['view_record_type']
    cls = CLASS_CODES[d['code']]
    kv, cont, pols = d['kv'], d['cont'], d['pols']
    for k, table in (('d', DOMAIN_CODES), ('o', ORACLE_CODES), ('c', CONF_CODES), ('k', DELTA_KIND),
                     ('fa', FACET_CODES)):
        if k in kv and kv[k] not in table:
            raise DecErr('%s: bad %s=%s' % (where, k, kv[k]))
    if t == 'PROVISIONAL_FACET_OVERLAY' and 'fa' not in kv:
        raise DecErr('%s: facet needs fa=' % where)
    if t != 'PROVISIONAL_FACET_OVERLAY' and 'fa' in kv:
        raise DecErr('%s: fa= only for facets' % where)
    # --- classification-specific requirements
    if cls in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA') and not pols:
        raise DecErr('%s: %s needs canonical policy ids' % (where, cls))
    if cls == 'CANONICAL_PLUS_DELTA' and not (cont.get('x') and cont.get('s')):
        raise DecErr('%s: CD needs x: and s:' % where)
    if cls in ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW') and not cont.get('s'):
        raise DecErr('%s: %s needs s: distinguishing scenario' % (where, cls))
    if cls in ('CANONICAL_PLUS_DELTA', 'EXTRA_PRODUCT', 'EXTRA_WORKFLOW', 'MIXED', 'UNCERTAIN') and not d['note']:
        raise DecErr('%s: %s needs a | rationale note' % (where, cls))
    if cls == 'UNCERTAIN' and not cont.get('r'):
        raise DecErr('%s: UNCERTAIN needs r: precise blocker' % where)
    if cls == 'MIXED' and len(d['subs']) < 2:
        raise DecErr('%s: MIXED needs >= 2 subclauses' % where)
    if cls != 'MIXED' and d['subs']:
        raise DecErr('%s: subclauses only allowed for MIXED' % where)
    if cls in ('NON_NORMATIVE', 'INTERNAL_ARCHITECTURE', 'EXTRA_PRODUCT', 'EXTRA_WORKFLOW') and pols:
        raise DecErr('%s: %s must not carry entailing policy ids (use rel=)' % (where, cls))
    if d['flag'] and not (cont.get('r') or d['note']):
        raise DecErr('%s: ! needs a reason' % where)
    # --- modality
    if cls == 'NON_NORMATIVE':
        mod, mod_src = ('NONE', 'CLASS_DEFAULT') if 'm' not in kv else (MODALITY_CODES[kv['m']], 'REVIEWER')
    elif cls == 'MIXED':
        mod, mod_src = None, None
    elif cls == 'UNCERTAIN':
        try:
            mod, mod_src = derive_modality(r, d, where)
        except DecErr:
            mod, mod_src = 'UNCERTAIN', 'UNDETERMINED'
    else:
        mod, mod_src = derive_modality(r, d, where)
    subs = []
    if cls == 'MIXED':
        try:
            rec_mod = derive_modality(r, d, where)[0]
        except DecErr:
            rec_mod = None
        subs = [sub_record(cand, s, rec_mod, i, s['src']) for i, s in enumerate(d['subs'], 1)]
        mods = []
        for s in subs:
            if s['modality'] not in mods:
                mods.append(s['modality'])
        mod, mod_src = 'MIXED', 'SUBCLAUSES'
        mod_detail = '; '.join('%s=%s' % (s['subclause_id'], s['modality']) for s in subs)
    else:
        mod_detail = '; '.join(sorted(set(reported_modalities(r))))[:400] or None
    if mod not in MODALITIES and mod != 'MIXED':
        raise DecErr('%s: modality %s invalid' % (where, mod))
    if cls in NORMATIVE_CLASSES and mod == 'NONE':
        raise DecErr('%s: normative class with modality NONE' % where)
    # --- normativity / domain / oracle relation
    if cls == 'MIXED':
        norms = {s['normativity'] for s in subs}
        normativity = 'NORMATIVE' if 'NORMATIVE' in norms else ('UNCERTAIN' if 'UNCERTAIN' in norms else 'NON_NORMATIVE')
        doms = []
        for s in subs:
            if s['domain'] not in doms and s['classification'] != 'NON_NORMATIVE':
                doms.append(s['domain'])
        domain = doms[0] if len(doms) == 1 else 'MIXED'
        rels = [s['oracle_relation'] for s in subs if s['classification'] != 'NON_NORMATIVE']
        if rels and all(x == 'FULLY_ENTAILED' for x in rels):
            oracle = 'FULLY_ENTAILED'
        elif any(x in ('FULLY_ENTAILED', 'PARTIALLY_ENTAILED') for x in rels):
            oracle = 'PARTIALLY_ENTAILED'
        elif 'NOT_ENTAILED' in rels:
            oracle = 'NOT_ENTAILED'
        elif 'UNCERTAIN' in rels:
            oracle = 'UNCERTAIN'
        else:
            oracle = 'NOT_APPLICABLE'
    else:
        normativity = {'NON_NORMATIVE': 'NON_NORMATIVE', 'UNCERTAIN': 'UNCERTAIN'}.get(cls, 'NORMATIVE')
        if cls == 'UNCERTAIN' and 'm' in kv and kv['m'] != 'U':
            normativity = 'NORMATIVE' if kv['m'] != 'N' else 'NON_NORMATIVE'
        domain = {'EXTRA_PRODUCT': 'PRODUCT_ENGINEERING', 'EXTRA_WORKFLOW': 'WORKFLOW_ENFORCEMENT',
                  'INTERNAL_ARCHITECTURE': 'INSTRUCTION_ARCHITECTURE', 'NON_NORMATIVE': 'NON_NORMATIVE',
                  'UNCERTAIN': 'UNCERTAIN'}.get(cls) or domain_from_pols(pols)
        oracle = {'CANONICAL_ONLY': 'FULLY_ENTAILED', 'CANONICAL_PLUS_DELTA': 'PARTIALLY_ENTAILED',
                  'EXTRA_PRODUCT': 'NOT_ENTAILED', 'EXTRA_WORKFLOW': 'NOT_ENTAILED',
                  'INTERNAL_ARCHITECTURE': 'NOT_APPLICABLE', 'NON_NORMATIVE': 'NOT_APPLICABLE',
                  'UNCERTAIN': 'UNCERTAIN'}[cls]
    if 'd' in kv:
        domain = DOMAIN_CODES[kv['d']]
    if 'o' in kv:
        oracle = ORACLE_CODES[kv['o']]
    # --- strength and coverage
    strength_check(cls, mod, pols, kv, where)
    st = {'W': 'WEAKER', 'S': 'STRONGER', 'X': 'INCOMPARABLE'}.get(kv.get('st'))
    if st is None:
        st = 'SAME' if (pols and cls in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA')) else ('N/A' if not pols else 'UNDETERMINED')
    cov = [{'policy_id': p, 'coverage': 'PARTIAL' if (p in d['partial'] or st == 'WEAKER') else 'FULL'}
           for p in pols]
    # --- trigger / exceptions / scope
    anchor = record_anchor(r)
    prov = {}
    if t == 'ORIGINAL_GROUP':
        pc = group_primary_clause(r['original_group'])
        rep_t = pc.get('reported_trigger_scope') if pc else None
        rep_e = pc.get('reported_exceptions') if pc else None
    elif t == 'PROVISIONAL_NEW_CLAUSE':
        rep_t, rep_e = r.get('trigger_scope'), None
    else:
        rep_t = rep_e = 'as the target group %s' % r['target_group_id']
    if is_unknown(rep_t):
        rep_t = None
    if is_unknown(rep_e):
        rep_e = None
    if STRICT and normativity == 'NORMATIVE' and rep_t is None and not cont.get('t'):
        raise DecErr('%s: no reported trigger for a normative record; give t: (or t: NONE)' % where)
    if cont.get('t'):
        trig, prov['trigger'] = cont['t'], 'REVIEWER'
    else:
        trig = ' '.join(str(rep_t).split()) if rep_t else 'NOT_REPORTED'
        prov['trigger'] = 'REPORTED_SEED_ATTRIBUTED' if rep_t else 'NONE_AVAILABLE'
    if cont.get('e'):
        exc, prov['exceptions'] = cont['e'], 'REVIEWER'
    elif rep_e is None and (cont.get('t') or STRICT):
        exc, prov['exceptions'] = 'NONE_STATED_IN_CITED_SOURCE', 'REVIEWER_READ_OF_CITED_SOURCE'
    else:
        exc = norm_exc(rep_e)
        prov['exceptions'] = 'REPORTED_SEED_ATTRIBUTED' if rep_e is not None else 'NONE_AVAILABLE'
    lc = loading_context(cand, anchor[0])
    if cont.get('sc'):
        scope, prov['scope'] = cont['sc'], 'REVIEWER'
    else:
        scope, prov['scope'] = lc, 'MECHANICAL_LOADING_CONTEXT'
    prov['modality'] = mod_src
    # --- rationale texts
    note = d['note']
    rationale = note or DEFAULT_RATIONALE.get(cls) or ''
    if cls in ('NON_NORMATIVE', 'INTERNAL_ARCHITECTURE') and not note:
        prov['rationale'] = 'CLASS_DEFAULT_TEXT'
    elif cls == 'CANONICAL_ONLY' and not note:
        prov['rationale'] = 'CLASS_DEFAULT_TEXT'
    else:
        prov['rationale'] = 'REVIEWER'
    pol_quotes = '; '.join('%s: "%s"' % (p, policies()[p]['normalized_policy']) for p in pols)
    if cls == 'CANONICAL_ONLY':
        ce = cont.get('ce') or ('%s Claim: "%s". Policy text: %s' % (rationale, record_claim_text(r), pol_quotes))
    elif cls == 'CANONICAL_PLUS_DELTA':
        ce = cont.get('ce') or ('Canonical portion entailed by %s. Non-entailed remainder: %s' % (pol_quotes, cont['x']))
    elif cls == 'MIXED':
        parts = []
        for s in subs:
            if s['canonical_policy_ids']:
                parts.append('%s %s by %s' % (s['subclause_id'], s['classification'], ', '.join(s['canonical_policy_ids'])))
        ce = cont.get('ce') or ('; '.join(parts) if parts else None)
    elif cls == 'UNCERTAIN' and pols:
        ce = cont.get('ce') or ('Candidate (unconfirmed) policies: %s' % pol_quotes)
    else:
        ce = cont.get('ce')
    if cls in ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW'):
        xf = cont.get('x') or record_claim_text(r)
    else:
        xf = cont.get('x')
    # --- evidence
    ev = record_evidence_refs(r)
    anchor_path = 'inputs/%s/%s' % (cand, anchor[0])
    ev.sort(key=lambda e: 0 if (e['path'], e['start_line'], e['end_line']) == (anchor_path, anchor[1], anchor[2]) else 1)
    primary_anchor = {'path': anchor_path, 'start_line': anchor[1], 'end_line': anchor[2],
                      'basis': 'seed claim unit first verified clause' if t == 'ORIGINAL_GROUP' else 'Pass-1 evidence'}
    if cont.get('ev'):
        ev = parse_ev(cand, cont['ev'], where) + ev
    review_reason = cont.get('r')
    review = bool(d['flag'] or review_reason or cls == 'UNCERTAIN' or any(s.get('review_reason') for s in subs))
    if review and not review_reason:
        review_reason = note if d['flag'] else '; '.join(s['review_reason'] for s in subs if s.get('review_reason'))
    conf = CONF_CODES[kv['c']] if 'c' in kv else ('LOW' if cls == 'UNCERTAIN' else 'HIGH')
    rec = {
        'protocol_version': PROTOCOL_VERSION, 'candidate': cand, 'source_key': source_key(r),
        KEY_FIELD[t]: source_key(r), 'view_record_type': t, 'batch_id': batch_id,
        'claim_text': record_claim_text(r),
        'classification': cls, 'normativity': normativity, 'domain': domain, 'oracle_relation': oracle,
        'canonical_policy_ids': pols, 'canonical_coverage': cov, 'strength_vs_canonical': st,
        'related_policy_ids': [x for x in kv.get('rel', '').split(',') if x],
        'canonical_conflict_ids': [x for x in kv.get('cf', '').split(',') if x],
        'strength_resolution_code': kv.get('sr'),
        'modality': mod, 'modality_detail': mod_detail, 'scope': scope, 'trigger': trig, 'exceptions': exc,
        'loading_context': lc, 'field_provenance': prov,
        'rationale': rationale, 'canonical_entailment_rationale': ce,
        'extra_fragment': xf, 'extra_fragment_kind': (DELTA_KIND.get(kv.get('k')) or
                                                       {'PRODUCT_ENGINEERING': 'EXTRA_PRODUCT',
                                                        'WORKFLOW_ENFORCEMENT': 'EXTRA_WORKFLOW',
                                                        'INSTRUCTION_ARCHITECTURE': 'INTERNAL_ARCHITECTURE'}.get(domain, 'EXTRA_PRODUCT'))
        if cls == 'CANONICAL_PLUS_DELTA' else (cls if cls in ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW') else None),
        'distinguishing_scenario': cont.get('s'),
        'subclauses': subs,
        'review_needed': review, 'review_reason': review_reason,
        'potential_overmerge': bool(cont.get('om')), 'overmerge_note': cont.get('om'),
        'future_human_decision': cont.get('fhd'),
        'confidence': conf,
        'evidence_refs': ev,
        'primary_anchor': primary_anchor,
        'decision_src': d['src'],
    }
    for p in rec['related_policy_ids'] + rec['canonical_conflict_ids']:
        if p not in policies():
            raise DecErr('%s: undefined policy in rel/cf: %s' % (where, p))
    if t == 'ORIGINAL_GROUP':
        g = r['original_group']
        rec['provenance'] = {
            'source_record_keys': g['source_record_keys'], 'supporting_runs': g['supporting_runs'],
            'merge_type': g['merge_type'], 'facet_overlay_ids': r.get('facet_overlay_ids') or [],
            'attributed_labels_not_truth': ['%s:%s/%s%s' % (l['run'], l['reported_label'], l.get('reported_modality'),
                                                            ('[' + ','.join(l.get('reported_policy_ids') or []) + ']'))
                                            for l in g['original_labels']],
            'original_raw_sha256': r.get('original_raw_sha256')}
    elif t == 'PROVISIONAL_NEW_CLAUSE':
        rec['provenance'] = {'source_claim_id': r['source_claim_id'],
                             'same_candidate_groups_compared': r.get('same_candidate_groups_compared'),
                             'pass1_modality_attributed': r.get('modality'), 'status_note': r.get('status_note')}
        rec['new_relative_to_oracle'] = {
            'FULLY_ENTAILED': 'NO_ENTAILED_BY_ORACLE', 'PARTIALLY_ENTAILED': 'PARTIAL_REMAINDER_NOT_ENTAILED',
            'NOT_ENTAILED': 'YES_NOT_ENTAILED', 'NOT_APPLICABLE': ('NOT_NORMATIVE' if normativity == 'NON_NORMATIVE'
                                                                  else 'OUTSIDE_ORACLE_SCOPE'),
            'UNCERTAIN': 'UNCERTAIN'}[oracle]
    else:
        f = facets()[r['facet_id']]
        rec['target_group_id'] = r['target_group_id']
        rec['facet_assessment'] = FACET_CODES[kv['fa']]
        rec['provenance'] = {'source_claim_id': r['source_claim_id'], 'facet_kind': f['facet_kind'],
                             'pass1_reviewer_confidence_attributed': f.get('reviewer_confidence')}
    return rec


def load_plan(cand):
    return json.load(open(os.path.join(OUT, '_batches', cand + '.json'), encoding='utf-8'))


def by_key():
    return {source_key(r): r for r in union_view()}


def compile_items(cand, items, dec_path, batch_id):
    recs = parse_dec(dec_path)
    bk = by_key()
    want = set(range(1, len(items) + 1))
    have = set(recs)
    if want != have:
        raise DecErr('%s: decisions missing %s extra %s' % (dec_path, sorted(want - have)[:30], sorted(have - want)[:30]))
    out = []
    for i, k in enumerate(items, 1):
        r = bk[k]
        if r['candidate'] != cand:
            raise DecErr('key %s not of candidate %s' % (k, cand))
        out.append(build_record(r, recs[i], batch_id, recs[i]['src']))
    return out


def verify_written(path, items, cand, bk):
    rows = read_jsonl(path)
    if [x['source_key'] for x in rows] != items:
        raise DecErr('written keys differ from plan')
    for x in rows:
        r = bk[x['source_key']]
        if x['candidate'] != cand or x['view_record_type'] != r['view_record_type'] or x['protocol_version'] != 'step2-v1':
            raise DecErr('written record mismatch %s' % x['source_key'])
    return len(rows)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1] == 'CAL':
        dec = os.path.join(OUT, '_decisions', 'CALIBRATION.dec')
        spec = json.load(open(os.path.join(OUT, '_decisions', 'CALIBRATION_KEYS.json'), encoding='utf-8'))
        rows = []
        for cand, keys in spec['by_candidate'].items():
            sub = os.path.join(OUT, '_decisions', 'CALIBRATION_%s.dec' % cand)
            for x in compile_items(cand, keys, sub, 'CAL'):
                x['calibration'] = spec['notes'].get(x['source_key'], {})
                rows.append(x)
        write_jsonl_atomic(os.path.join(OUT, 'CALIBRATION.jsonl'), rows)
        print('CALIBRATION.jsonl', len(rows))
        return
    cand, bid = sys.argv[1], sys.argv[2]
    global STRICT
    STRICT = cand != 'M'  # M was compiled before Addendum A1; its fixes go through CORRECTIONS.dec
    plan = load_plan(cand)
    b = [x for x in plan['batches'] if x['batch_id'] == bid][0]
    items = [x['source_key'] for x in b['records']]
    dec = os.path.join(OUT, '_decisions', cand, bid + '.dec')
    rows = compile_items(cand, items, dec, bid)
    if '--check' in sys.argv:
        from collections import Counter
        print('OK (check only)', len(rows), dict(Counter(r['classification'] for r in rows)))
        return
    target = os.path.join(OUT, 'per_candidate', cand, 'batches', bid + '.jsonl')
    ck = os.path.join(OUT, 'CHECKPOINTS', cand, bid + '.checkpoint.json')
    if os.path.exists(ck) and '--rebuild' not in sys.argv:
        print('checkpoint exists for %s %s; use --rebuild to overwrite' % (cand, bid)); sys.exit(2)
    if os.path.exists(ck):
        with open(os.path.join(OUT, 'CHECKPOINTS', 'REBUILD_LOG.jsonl'), 'a', encoding='utf-8') as f:
            f.write(json.dumps({'candidate': cand, 'batch_id': bid, 'at': time.strftime('%Y-%m-%dT%H:%M:%S'),
                                'previous': json.load(open(ck, encoding='utf-8'))}) + '\n')
    write_jsonl_atomic(target, rows)
    n = verify_written(target, items, cand, by_key())
    from collections import Counter
    write_json_atomic(ck, {
        'protocol_version': PROTOCOL_VERSION, 'candidate': cand, 'batch_id': bid, 'n_records': n,
        'status': 'COMPLETE', 'batch_file': os.path.relpath(target, OUT).replace(os.sep, '/'),
        'batch_file_sha256': sha256_file(target), 'decision_file_sha256': sha256_file(dec),
        'keys_sha256': sha256_text('\n'.join(items)), 'plan_sha256': plan['plan_sha256'],
        'class_counts': dict(Counter(r['classification'] for r in rows)),
        'verified_at': time.strftime('%Y-%m-%dT%H:%M:%S')})
    print('%s %s: %d records written, parsed, key-verified, checkpointed %s' % (
        cand, bid, n, dict(Counter(r['classification'] for r in rows))))


if __name__ == '__main__':
    try:
        main()
    except DecErr as e:
        print('ERROR:', e); sys.exit(1)
