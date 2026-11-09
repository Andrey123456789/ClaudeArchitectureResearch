"""Per-claim gate for data-only dispositions (contract C05): one disposition at a time, in process, with the classification-level checks after each.

python -B _tools/claimgate.py <CHANGE>

_rules/<CHANGE>/claims.py holds CLAIMS: [dict(id, key, path, quote, set, claim, note, kind)] in order. The change's updates.py builds the same dispositions for the full replay.
After each disposition: the quote resolves on current bytes; all-candidate record invariants; coverage on 1,176 cells against the previous state; the 103 corrections and 31 open records;
PI-012 review counts; template bytes unchanged. The first failure stops the sequence and nothing after it runs. Template suites run in the full gate that closes the change: a data disposition cannot change a template byte, and this gate proves that with hashes.
"""
import hashlib
import importlib.util
import json
import os
import sys
from collections import Counter

import dataset
from rcommon import CANDIDATES, append_jsonl, baseline, norm_ws, now, out_path, read_jsonl, read_lines, rec_hash, sha256_file, template_root, utf8_stdout, walk_files, wc_path
from roverlay import coverage_of, effective_status, validate_candidate


def template_fingerprint():
    h = hashlib.sha256()
    for c in CANDIDATES:
        for rel in walk_files(template_root(c)):
            h.update(('%s/%s %s\n' % (c, rel, sha256_file(wc_path(c, rel)))).encode('utf-8'))
    return h.hexdigest()


def load_claims(change):
    spec = importlib.util.spec_from_file_location('claims_' + change.replace('-', '_'), out_path('_rules', change, 'claims.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.CLAIMS


def cells(state):
    out = {}
    for c in CANDIDATES:
        cov = coverage_of([r for r in state[c].values() if r['repair']['active']])
        for pid, row in cov.items():
            out[(c, pid)] = (effective_status(c, pid, row), row['strength_status'])
    return out


def check_103(by):
    adj = read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))
    off = []
    for r in adj:
        if r['decision'] not in ('ACCEPT', 'ACCEPT_MODIFIED'):
            continue
        base, _, sub = r['case_key'].partition('/')
        rec = by[base]
        if sub or not rec['repair']['active']:
            continue
        for f, v in r['applied_set'].items():
            if f in ('subclauses', 'subclauses_add', 'subclause_set'):
                continue
            tag = 'R25-COR103:%s' % r['correction_id']
            later = rec['repair']['rules'][rec['repair']['rules'].index(tag) + 1:] if tag in rec['repair']['rules'] else ['?']
            if rec.get(f) != v and not any(not x.startswith('R01') for x in later):
                off.append((r['case_key'], f))
    return len(adj), off


def check_31(by):
    un = read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl'))
    op = [r for r in un if r['kind'] == 'ORIGINAL_OPEN_RECORD']
    stale = [r['id'] for r in op if by[r['id']]['classification'] == 'UNCERTAIN' or by[r['id']].get('future_human_decision') or any(s.get('classification') == 'UNCERTAIN' for s in by[r['id']].get('subclauses') or [])]
    return len(op), stale


def check_pi012():
    out = {}
    for f, want in (('PI012_79_REVIEW.jsonl', {'CORRECT': 55, 'UPHOLD': 22, 'UNRESOLVED': 2}), ('PI012_230_REVIEW.jsonl', {'CORRECT': 105, 'UPHOLD': 123, 'UNRESOLVED': 2})):
        got = Counter(r['result'] for r in read_jsonl(out_path(f)))
        if dict(got) != want:
            out[f] = dict(got)
    return out


def quote_ok(c, rel, quote):
    p = wc_path(c, rel)
    return os.path.exists(p) and norm_ws(quote).lower() in norm_ws(' '.join(read_lines(p))).lower()


READING_FIELDS = {'classification', 'modality', 'canonical_coverage', 'strength_vs_canonical', 'strength_resolution_code'}
READING_DERIVED = {'modality_detail', 'strength_links', 'strength_mechanical_mismatch', 'strength_resolution', 'normative_strength_equivalence', 'canonical_policy_ids', 'canonical_semantic_coverage'}


def undeclared(before, after, declared):
    """Fields a disposition changed without declaring them. A declared reading field may move the fields derived from it, and nothing else."""
    allowed = set(declared) | {'repair', 'claim_text'}
    if allowed & READING_FIELDS:
        allowed |= READING_DERIVED
    return sorted(f for f in set(before) | set(after) if f not in allowed and before.get(f) != after.get(f))


def attempt_of(change):
    """Logs are append-only. A re-run after a repair gets a higher attempt number, and its rows supersede the earlier ones."""
    return 1 + max([r.get('attempt', 1) for r in read_jsonl(out_path('CLAIM_GATE_LOG.jsonl')) if r['change'] == change] or [0])


def run(change):
    claims = load_claims(change)
    attempt = attempt_of(change)
    rows, _ = dataset.build(skip={change})
    state = {c: {r['source_key']: r for r in rows[c]} for c in CANDIDATES}
    prev = cells(state)
    fp0 = template_fingerprint()
    done = []
    for i, cl in enumerate(claims, 1):
        key = cl['key']
        base, _, sub = key.partition('/')
        c = next(cc for cc in CANDIDATES if base in state[cc])
        before = state[c][base]
        after = dataset.apply_v2_set(before, cl.get('set') or {}, sub or None)
        if cl.get('claim'):
            after['claim_text'] = cl['claim']
        after = dict(after, repair=dict(after['repair'], rules=list(after['repair']['rules']) + [change]))
        state[c][base] = after
        errs = []
        extra = undeclared(before, after, (cl.get('set') or {}).keys() | ({'subclauses'} if sub else set()))
        if extra:
            errs.append('fields changed without being declared: %s' % extra)
        if not quote_ok(c, cl['path'], cl['quote']):
            errs.append('quote not in current %s: %s' % (cl['path'], cl['quote'][:80]))
        active = {k: r for k, r in state[c].items() if r['repair']['active']}
        removed = [k for k, r in state[c].items() if not r['repair']['active']]
        errs.extend(validate_candidate(c, active, allow_added=True, removed=removed)[:5])
        cur = cells(state)
        moved = sorted('%s %s' % k for k in cur if cur[k] != prev[k])
        if moved:
            errs.append('coverage or strength moved: %s' % moved[:5])
        by = {k: r for cc in CANDIDATES for k, r in state[cc].items()}
        n103, off = check_103(by)
        if off:
            errs.append('103 corrections disturbed: %s' % off[:4])
        n31, stale = check_31(by)
        if stale:
            errs.append('31 open records disturbed: %s' % stale[:4])
        pi = check_pi012()
        if pi:
            errs.append('PI-012 counts changed: %s' % pi)
        fp = template_fingerprint()
        if fp != fp0:
            errs.append('template bytes changed')
        row = {'at': now(), 'change': change, 'attempt': attempt, 'id': cl['id'], 'key': key, 'candidate': c, 'kind': cl.get('kind'), 'before_sha256': rec_hash(before), 'after_sha256': rec_hash(after), 'n_cells_checked': len(cur), 'n_103_checked': n103, 'n_31_checked': n31, 'template_fingerprint': fp, 'status': 'FAIL' if errs else 'PASS', 'errors': errs}
        append_jsonl('CLAIM_GATE_LOG.jsonl', row)
        if not errs:
            append_jsonl('CHANGE_LOG.jsonl', {'at': row['at'], 'rule': change, 'attempt': attempt, 'id': cl['id'], 'candidate': c, 'key': key, 'action': cl.get('kind'), 'before_sha256': row['before_sha256'], 'after_sha256': row['after_sha256'], 'file': cl['path'], 'source_evidence': cl['quote'], 'reason': cl['note'], 'affected_policies': [x['policy_id'] for x in after.get('canonical_coverage') or []] or after.get('related_policy_ids') or [], 'kind': 'DATA'})
        if errs:
            print('STOP at %s %s:' % (cl['id'], key))
            for e in errs:
                print('  ', e)
            return 1
        done.append(key)
        prev = cur
    rows2, _ = dataset.build()
    full = {r['source_key']: r for c in CANDIDATES for r in rows2[c]}
    drift = []
    for cl in claims:
        base = cl['key'].partition('/')[0]
        c = next(cc for cc in CANDIDATES if base in state[cc])
        for f in ('classification', 'modality', 'claim_text', 'applicability_override', 'strength_resolution'):
            if state[c][base].get(f) != full[base].get(f):
                drift.append((cl['id'], f))
    if drift:
        print('STOP: per-claim state differs from the full replay:', drift[:6])
        return 1
    print(json.dumps({'change': change, 'dispositions': len(done), 'status': 'PASS', 'template_fingerprint': fp0}))
    return 0


if __name__ == '__main__':
    utf8_stdout()
    sys.exit(run(sys.argv[1]))
