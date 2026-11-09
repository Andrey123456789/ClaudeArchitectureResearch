"""Addendum A1 enrichment applied at assembly to every record (no reviewer judgment except _decisions/<C>/STRENGTH.dec).

Adds:
  canonical_semantic_coverage      FULL | PARTIAL | NONE            what the claim covers of the cited policies
  normative_strength_equivalence   EQUIVALENT | WEAKER_THAN_CANONICAL | STRONGER_THAN_CANONICAL | INCOMPARABLE |
                                   PORTION_EQUIVALENT_WITH_REMAINDER | NOT_APPLICABLE
  strength_links                   per link: policy tag, record modality, mechanical relation
  strength_resolution              reviewer code and label for any mismatch or non-equivalence
  source_quote_verification        mechanical re-reading of the immutable file for every evidence reference
  primary_quote                    exact source text at primary_anchor (truncated for storage, hash covers the whole range)
  trigger_status / exceptions_status   REVIEWER | ATTRIBUTED | NOT_APPLICABLE | MISSING
  protocol_addendum                'A1'
"""
import os
import re
import unicodedata

from common import (OUT, ROOT, SR_CODES, WEAKER_CODES, policies, occurrences, facets, proposals, sha256_text,
                    strength_relation, is_unknown)

MAX_QUOTE = 600


def read_range(path, s, e):
    with open(os.path.join(ROOT, path.replace('/', os.sep)), encoding='utf-8', errors='replace') as f:
        lines = f.read().split('\n')
    if not (1 <= s <= e <= len(lines)):
        return None
    return '\n'.join(lines[s - 1:e])


def norm(t):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', t.replace('\r', ''))).strip()


def verify_ref(ref, expected):
    text = read_range(ref['path'], ref['start_line'], ref['end_line'])
    if text is None:
        return 'FAILED_RANGE_OUTSIDE_FILE', None
    sha = sha256_text(text)
    if not expected:
        return 'RANGE_CHECKED_NO_QUOTE', sha
    if text.replace('\r', '') == expected.replace('\r', ''):
        return 'EXACT_RANGE_MATCH', sha
    if norm(text) == norm(expected):
        return 'EXACT_AFTER_WHITESPACE_NORMALIZATION', sha
    if norm(expected) in norm(text):
        return 'QUOTE_WITHIN_RANGE', sha
    return 'FAILED_QUOTE_MISMATCH', sha


def expected_quote(rec, ref):
    if ref.get('occurrence_id'):
        return occurrences()[ref['occurrence_id']].get('exact_excerpt')
    t = rec['view_record_type']
    if t == 'PROVISIONAL_FACET_OVERLAY':
        e = facets()[rec['source_key']]['evidence']
        return e.get('exact_excerpt') or e.get('quote') if (ref['start_line'], ref['end_line']) == (e['start_line'], e['end_line']) else None
    if t == 'PROVISIONAL_NEW_CLAUSE':
        e = proposals()[rec['source_key']]['evidence']
        return e.get('quote') if (ref['start_line'], ref['end_line']) == (e['start_line'], e['end_line']) else None
    return None


def verify_record(rec):
    counts, fails = {}, []
    for ref in rec['evidence_refs']:
        st, sha = verify_ref(ref, expected_quote(rec, ref))
        counts[st] = counts.get(st, 0) + 1
        if st.startswith('FAILED'):
            fails.append('%s:%s-%s %s' % (ref['path'], ref['start_line'], ref['end_line'], st))
    a = rec.get('primary_anchor') or {}
    anchor_ref = next((r for r in rec['evidence_refs'] if (r['path'], r['start_line'], r['end_line']) == (a.get('path'), a.get('start_line'), a.get('end_line'))), None)
    if anchor_ref is not None:
        anchor_status = verify_ref(anchor_ref, expected_quote(rec, anchor_ref))[0]
    else:
        anchor_status = 'FAILED_ANCHOR_NOT_IN_EVIDENCE'
        fails.append('primary anchor is not among evidence refs')
    text = read_range(a['path'], a['start_line'], a['end_line']) if a else None
    status = 'FAILED' if fails else ('VERIFIED' if not counts.get('RANGE_CHECKED_NO_QUOTE') else 'VERIFIED_WITH_RANGE_ONLY_REFS')
    return {
        'status': status, 'primary_anchor_status': anchor_status, 'ref_status_counts': counts, 'failures': fails,
        'method': 'mechanical re-read of the immutable file per reference; exact excerpt comparison where Step-1 or Pass-1 recorded one',
        'primary_quote_sha256': sha256_text(text) if text is not None else None,
    }, (text or '')


def load_strength_dec(cand):
    out = {}
    p = os.path.join(OUT, '_decisions', cand, 'STRENGTH.dec')
    if not os.path.exists(p):
        return out
    for ln, raw in enumerate(open(p, encoding='utf-8'), 1):
        raw = raw.strip()
        if not raw or raw.startswith('#'):
            continue
        m = re.match(r'^(\S+)\s+([A-Z]{2})\s*\|\s*(.+)$', raw)
        if not m or m.group(2) not in SR_CODES:
            raise SystemExit('bad STRENGTH.dec line %d: %s' % (ln, raw))
        out[m.group(1)] = (m.group(2), m.group(3), 'STRENGTH.dec:%d' % ln)
    return out


EQ = {'SAME': 'EQUIVALENT', 'WEAKER': 'WEAKER_THAN_CANONICAL', 'STRONGER': 'STRONGER_THAN_CANONICAL',
      'INCOMPARABLE': 'INCOMPARABLE', 'N/A': 'NOT_APPLICABLE', 'UNDETERMINED': 'INCOMPARABLE'}


def strength_fields(obj, key, table):
    """Compute the strength axes for a record or subclause object."""
    cls, st = obj['classification'], obj.get('strength_vs_canonical')
    links = []
    for cov in obj.get('canonical_coverage') or []:
        tag = policies()[cov['policy_id']]['normative_strength']
        links.append({'policy_id': cov['policy_id'], 'policy_strength': tag, 'record_modality': obj.get('modality'),
                      'coverage': cov['coverage'], 'mechanical_relation': strength_relation(obj.get('modality'), tag)})
    mismatch = any(l['mechanical_relation'] in ('RECORD_STRONGER', 'RECORD_WEAKER') for l in links)
    code, note, src = None, None, None
    if key in table:
        code, note, src = table[key]
    elif obj.get('strength_resolution_code'):
        code, note, src = obj['strength_resolution_code'], None, 'decision token sr='
    eq = EQ.get(st, 'NOT_APPLICABLE')
    if cls == 'CANONICAL_PLUS_DELTA' and st == 'SAME':
        eq = 'PORTION_EQUIVALENT_WITH_REMAINDER'
    if not links:
        cov_state = 'NONE'
    else:
        cov_state = 'FULL' if all(l['coverage'] == 'FULL' for l in links) else 'PARTIAL'
    res = {'code': code, 'label': SR_CODES.get(code), 'note': note, 'source': src} if code else None
    return {'canonical_semantic_coverage': cov_state, 'normative_strength_equivalence': eq, 'strength_links': links,
            'strength_mechanical_mismatch': mismatch, 'strength_resolution': res}


def field_status(rec, field):
    if rec['normativity'] == 'NON_NORMATIVE':
        return 'NOT_APPLICABLE'
    if is_unknown(rec[field]):
        return 'MISSING'
    src = (rec.get('field_provenance') or {}).get('trigger' if field == 'trigger' else 'exceptions', '')
    return 'REVIEWER' if src.startswith('REVIEWER') else 'ATTRIBUTED'


def enrich(rec, table):
    rec.update(strength_fields(rec, rec['source_key'], table))
    for s in rec.get('subclauses') or []:
        s.update(strength_fields(s, '%s/%s' % (rec['source_key'], s['subclause_id']), table))
    qv, text = verify_record(rec)
    rec['source_quote_verification'] = qv
    rec['primary_quote'] = text[:MAX_QUOTE]
    rec['primary_quote_truncated'] = len(text) > MAX_QUOTE
    rec['trigger_status'] = field_status(rec, 'trigger')
    rec['exceptions_status'] = field_status(rec, 'exceptions')
    if rec['normativity'] == 'NON_NORMATIVE':
        for f in ('trigger', 'exceptions'):
            if is_unknown(rec[f]):
                rec[f] = 'NOT_APPLICABLE (non-normative record)'
    rec['protocol_addendum'] = 'A1'
    return rec


def rows_needing_strength_review(rows):
    """Records (or subclauses) that are mismatched or non-equivalent and still carry no resolution."""
    out = []
    for r in rows:
        for key, obj in [(r['source_key'], r)] + [('%s/%s' % (r['source_key'], s['subclause_id']), s) for s in r.get('subclauses') or []]:
            if obj['classification'] not in ('CANONICAL_ONLY', 'CANONICAL_PLUS_DELTA'):
                continue
            st = obj.get('strength_vs_canonical')
            if st == 'WEAKER' and not (obj.get('strength_resolution') and obj['strength_resolution']['code'] in WEAKER_CODES):
                out.append((key, 'WEAKER without a weaker-kind code'))
            elif st == 'SAME' and obj.get('strength_mechanical_mismatch') and not obj.get('strength_resolution'):
                out.append((key, 'mechanical mismatch without resolution'))
            elif obj['classification'] == 'CANONICAL_ONLY' and st == 'STRONGER':
                out.append((key, 'CANONICAL_ONLY cannot be stronger'))
    return out
