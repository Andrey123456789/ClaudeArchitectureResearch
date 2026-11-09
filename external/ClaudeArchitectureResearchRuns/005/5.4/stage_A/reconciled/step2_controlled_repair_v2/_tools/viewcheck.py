"""Whole-view invariants of REPAIRED_CANDIDATE_DERIVED_VIEW. Used by the R26 suite and the final audit. Returns a list of errors; never edits anything."""
import re
from collections import Counter

from rcommon import CANDIDATES, baseline, coverage, norm_ws, policies, read_lines, rec_hash, wc_path
from roverlay import coverage_of, validate_candidate

NEW_ID = re.compile(r'^(REP|NCP)-(M|M1|L0|L1|K0|K1)-\d{3,4}$')
REF_OK = {'SAME', 'MOVED', 'REWORDED', 'SPLIT', 'ADDED', 'REMOVED', 'MOVED_FILE'}


class Lines:
    def __init__(self):
        self.cache = {}

    def get(self, ref):
        p = ref['path']
        if p not in self.cache:
            c, rel = p.split('/')[1], p.split('/template/')[1]
            self.cache[p] = read_lines(wc_path(c, rel))
        return self.cache[p]


def check_rows(rows):
    errs = []
    keys = [r['source_key'] for r in rows]
    if len(set(keys)) != len(keys):
        errs.append('duplicate ids: %s' % [k for k, n in Counter(keys).items() if n > 1][:5])
    frozen = {k: r for c in CANDIDATES for k, r in baseline(c).items()}
    lost = set(frozen) - set(keys)
    if lost:
        errs.append('lost baseline ids: %s' % sorted(lost)[:5])
    lines = Lines()
    for r in rows:
        k = r['source_key']
        rep = r.get('repair') or {}
        for f in ('applicability_status', 'trigger_field_original', 'delivery_context'):
            if f not in r:
                errs.append('%s: missing %s' % (k, f))
        if k in frozen:
            if rep.get('baseline_sha256') != rec_hash(frozen[k]):
                errs.append('%s: baseline hash differs' % k)
            if r.get('claim_text_original') != frozen[k].get('claim_text'):
                errs.append('%s: original claim lost' % k)
        elif not NEW_ID.match(k):
            errs.append('%s: new row without a new stable id' % k)
        refs = r.get('current_evidence_refs') or []
        for x in refs:
            if x['status'] not in REF_OK:
                errs.append('%s: evidence status %s' % (k, x['status']))
                continue
            if x['status'] == 'REMOVED':
                continue
            if not x.get('start_line'):
                errs.append('%s: evidence with no line %s' % (k, x['status']))
                continue
            text = norm_ws(' '.join(lines.get(x)[x['start_line'] - 1:x['end_line']]))
            if x.get('new_quote') and norm_ws(x['new_quote']).lower() not in text.lower():
                errs.append('%s: quote not at its lines: %s' % (k, x['new_quote'][:70]))
        if rep.get('active') and refs and all(x['status'] == 'REMOVED' for x in refs):
            errs.append('%s: active row with only removed evidence' % k)
    return errs


def check_coverage(rows, cov):
    errs = []
    if len(cov) != 1176 or len({(c['candidate'], c['policy_id']) for c in cov}) != 1176:
        errs.append('coverage is not 1,176 unique cells: %d' % len(cov))
    active = {r['source_key']: r for r in rows if r['repair']['active']}
    for c in CANDIDATES:
        act = [r for r in active.values() if r['candidate'] == c]
        fresh = coverage_of(act)
        for cell in (x for x in cov if x['candidate'] == c):
            f = fresh[cell['policy_id']]
            for fld in ('computed_status', 'strength_status', 'direct_source_keys', 'partial_source_keys'):
                if f[fld] != cell[fld]:
                    errs.append('%s %s: stored %s differs from recomputed' % (c, cell['policy_id'], fld))
            if not cell['witnesses']:
                errs.append('%s %s: no witness' % (c, cell['policy_id']))
            if not any(w.get('path') and w.get('start_line') for w in cell['witnesses']):
                errs.append('%s %s: no witness with a current line' % (c, cell['policy_id']))
            for w in cell['witnesses']:
                if w['source_key'] not in active:
                    errs.append('%s %s: inactive witness %s' % (c, cell['policy_id'], w['source_key']))
            if cell['status'] != cell['baseline_status'] and not cell.get('status_changed'):
                errs.append('%s %s: status move not flagged' % (c, cell['policy_id']))
            if coverage(c)[cell['policy_id']]['status'] != cell['baseline_status']:
                errs.append('%s %s: baseline status misquoted' % (c, cell['policy_id']))
    return errs


def check_invariants(rows):
    errs = []
    for c in CANDIDATES:
        act = {r['source_key']: r for r in rows if r['candidate'] == c and r['repair']['active']}
        removed = [r['source_key'] for r in rows if r['candidate'] == c and not r['repair']['active']]
        errs.extend(validate_candidate(c, act, allow_added=True, removed=removed))
    if len(policies()) != 196:
        errs.append('policy set is not 196')
    return errs


def check_crosswalk(rows, cross):
    errs = []
    frozen = {k for c in CANDIDATES for k in baseline(c)}
    orig = [x['original_key'] for x in cross if x['original_key']]
    if len(orig) != len(set(orig)) or set(orig) != frozen:
        errs.append('crosswalk does not hold each baseline id once: %d' % len(orig))
    keys = {r['source_key'] for r in rows}
    for x in cross:
        if x['status'] == 'REMOVED':
            if x['repaired_key'] is not None:
                errs.append('%s: removed row keeps a repaired key' % x['original_key'])
        elif x['repaired_key'] not in keys:
            errs.append('%s: repaired key %s not in the view' % (x['original_key'], x['repaired_key']))
        if x['status'] == 'ADDED' and (x['original_key'] is not None or not x['new_ids']):
            errs.append('%s: added row without a new id' % x['repaired_key'])
    if len(cross) != len(rows):
        errs.append('crosswalk rows %d, view rows %d' % (len(cross), len(rows)))
    return errs


def check_all(rows, cross, cov):
    return check_rows(rows) + check_invariants(rows) + check_coverage(rows, cov) + check_crosswalk(rows, cross)
