"""Witness engine: maps each original evidence range to the current working copy.

For a range [a,b] of an original file:
  SAME     the file is unchanged, or the same lines hold the same text
  MOVED    the same normalized text exists elsewhere in the current file
  CHANGED  the text no longer exists; a disposition row in CLAIM_DISPOSITIONS.jsonl is required
A disposition is keyed by (candidate, path, start, end) and says REWORDED, REMOVED or SPLIT with the rule that caused it and the
new quote. The new quote must exist in the current file. A mechanical check, never semantic proof.
"""
import os
import re

from rcommon import CANDIDATES, OUT, baseline, coverage, input_path, norm_ws, out_path, policies, read_jsonl, read_lines, sha256_file, wc_path


def rel_of(path):
    return path.split('/output/template/', 1)[1]


def norm_stream(lines):
    """Normalized text plus, for each char, its 1-based source line."""
    chars, index = [], []
    for n, line in enumerate(lines, 1):
        s = norm_ws(line)
        if not s:
            continue
        if chars:
            chars.append(' ')
            index.append(n)
        chars.append(s)
        index.extend([n] * len(s))
    return ''.join(chars), index


class FileMap:
    def __init__(self):
        self.orig, self.cur, self.hash = {}, {}, {}

    def orig_lines(self, c, rel):
        k = (c, rel)
        if k not in self.orig:
            self.orig[k] = read_lines(input_path(c, rel))
        return self.orig[k]

    def cur_lines(self, c, rel):
        k = (c, rel)
        if k not in self.cur:
            p = wc_path(c, rel)
            self.cur[k] = read_lines(p) if os.path.exists(p) else None
        return self.cur[k]

    def changed(self, c, rel):
        k = (c, rel)
        if k not in self.hash:
            p = wc_path(c, rel)
            self.hash[k] = (not os.path.exists(p)) or sha256_file(p) != sha256_file(input_path(c, rel))
        return self.hash[k]

    def stream(self, c, rel):
        k = ('s', c, rel)
        if k not in self.cur:
            ls = self.cur_lines(c, rel)
            self.cur[k] = norm_stream(ls) if ls is not None else None
        return self.cur[k]


def map_ref(fm, c, ref):
    rel, a, b = rel_of(ref['path']), ref['start_line'], ref['end_line']
    if not fm.changed(c, rel):
        return {'status': 'SAME', 'start': a, 'end': b}
    cur = fm.cur_lines(c, rel)
    if cur is None:
        return {'status': 'CHANGED', 'why': 'file removed'}
    want = norm_ws(' '.join(fm.orig_lines(c, rel)[a - 1:b]))
    if not want:
        return {'status': 'SAME', 'start': a, 'end': b}
    if norm_ws(' '.join(cur[a - 1:b])) == want:
        return {'status': 'SAME', 'start': a, 'end': b}
    text, idx = fm.stream(c, rel)
    i = text.find(want)
    if i >= 0:
        return {'status': 'MOVED', 'start': idx[i], 'end': idx[i + len(want) - 1]}
    return {'status': 'CHANGED', 'why': 'text not found'}


def load_dispositions():
    d = {}
    for r in read_jsonl(out_path('CLAIM_DISPOSITIONS.jsonl')):
        d[(r['candidate'], r['path'], r['start_line'], r['end_line'])] = r
    return d


def changed_ranges(cands=None):
    """Every CHANGED evidence range with the records citing it."""
    fm = FileMap()
    disp = load_dispositions()
    out = {}
    for c in cands or CANDIDATES:
        for key, r in baseline(c).items():
            for ref in r.get('evidence_refs') or []:
                rel = rel_of(ref['path'])
                if not fm.changed(c, rel):
                    continue
                m = map_ref(fm, c, ref)
                if m['status'] == 'CHANGED':
                    k = (c, rel, ref['start_line'], ref['end_line'])
                    row = out.setdefault(k, {'candidate': c, 'path': rel, 'start_line': ref['start_line'], 'end_line': ref['end_line'], 'keys': [], 'disposition': disp.get(k)})
                    row['keys'].append(key)
    return out


def check_dispositions(cands=None):
    """Returns errors: CHANGED range without disposition, or disposition whose new quote is not in the current file."""
    errors = []
    fm = FileMap()
    ranges = changed_ranges(cands)
    for k, row in ranges.items():
        if not row['disposition']:
            errors.append('no disposition for %s:%s:%s-%s (%d records)' % (row['candidate'], row['path'], row['start_line'], row['end_line'], len(row['keys'])))
    for k, r in load_dispositions().items():
        if cands and r['candidate'] not in cands:
            continue
        if r['disposition'] == 'REMOVED':
            continue
        s = fm.stream(r['candidate'], r['path'])
        if s is None or norm_ws(r['new_quote']) not in s[0]:
            errors.append('disposition quote not found: %s %s: %s' % (r['candidate'], r['path'], r['new_quote'][:120]))
    return errors, ranges


def policy_rows(c, reviews, rule):
    """196 rows for one candidate. reviews: {(policy, candidate): [review rows]} from this rule and earlier rules."""
    fm = FileMap()
    disp = load_dispositions()
    base = baseline(c)
    cov = coverage(c)
    rows = []
    for pid, pol in policies().items():
        row = cov[pid]
        keys = sorted(set(row.get('direct_source_keys') or []) | set(row.get('partial_source_keys') or []) | set(row.get('strength_equivalent_source_keys') or []) | set(row.get('weaker_source_keys') or []) | set(row.get('stronger_source_keys') or []))
        direct = set(row.get('direct_source_keys') or [])
        counts = {'SAME': 0, 'MOVED': 0, 'CHANGED_REVIEWED': 0, 'CHANGED_UNREVIEWED': 0, 'REMOVED': 0}
        live_direct = 0
        files = set()
        for key in keys:
            rec = base[key]
            statuses = []
            for ref in rec.get('evidence_refs') or []:
                rel = rel_of(ref['path'])
                files.add(rel)
                m = map_ref(fm, c, ref)
                if m['status'] == 'CHANGED':
                    d = disp.get((c, rel, ref['start_line'], ref['end_line']))
                    if not d:
                        statuses.append('CHANGED_UNREVIEWED')
                    elif d['disposition'] == 'REMOVED':
                        statuses.append('REMOVED')
                    else:
                        statuses.append('CHANGED_REVIEWED')
                else:
                    statuses.append(m['status'])
            for s in statuses:
                counts[s] += 1
            if key in direct and any(s != 'REMOVED' for s in statuses):
                live_direct += 1
        missing = [f for f in files if not os.path.exists(wc_path(c, f))]
        fails = []
        if counts['CHANGED_UNREVIEWED']:
            fails.append('unreviewed changed witness range')
        if direct and live_direct == 0:
            fails.append('no live direct witness')
        if not keys:
            fails.append('no witness')
        if missing:
            fails.append('witness file removed: %s' % missing)
        rv = reviews.get((pid, c), [])
        for x in rv:
            if x.get('verdict') not in ('HOLDS', 'HOLDS_WITH_NOTE', 'NOT_AFFECTED'):
                fails.append('semantic review verdict %s' % x.get('verdict'))
        touched = any(fm.changed(c, f) for f in files)
        rows.append({'rule': rule, 'candidate': c, 'policy': pid, 'strength': pol['normative_strength'], 'trigger_class': pol['trigger_class'], 'scope': pol['scope'], 'n_witness_keys': len(keys),
                     'n_live_direct': live_direct, 'range_counts': counts, 'witness_file_touched': touched, 'semantic_review_rows': [{'rule': x['rule'], 'verdict': x['verdict']} for x in rv],
                     'check_level': 'SOURCE_REVIEWED' if rv else ('MECHANICAL_TOUCHED_FILE' if touched else 'MECHANICAL_UNCHANGED_WITNESS'), 'status': 'FAIL' if fails else 'PASS', 'fails': fails})
    return rows
