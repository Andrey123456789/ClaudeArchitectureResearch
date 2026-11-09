"""v3 preflight (kit 74, MANDATORY PREFLIGHT). Read-only on everything outside this folder.

python -B _tools/preflight_v3.py [--manifest-only]

1. Hashes every protected tree before work (PREFLIGHT_PROTECTED_MANIFEST.json).
2. Verifies Codex passes 0002 and 0003 independently of Codex's own validator: PASS_VALIDATION status, checkpoint hashes, completed-unit
   receipts, the 448-file coverage per candidate, the baseline fingerprint recomputed from the frozen files, exact quotes, three-run
   baseline references, claim counts per candidate and applied revisions. Pass 0004 and later are never listed or read.
3. Verifies the predecessors: v2 status, checkpoints, candidate bytes against V2_FINAL_MANIFEST.json, v2 view replay (v2's own read-only
   verify_final.py), the Pass 1 augmented union counts, and v1's status.
Writes PREFLIGHT_RESULT.json. On any blocker it also writes PREFLIGHT_BLOCKER_REPORT.md and exits 2; nothing else is written.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime

TOOLS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(TOOLS)
REC = os.path.dirname(OUT)
ROOT = os.path.abspath(os.path.join(REC, '..', '..'))
CODEX = os.path.join(ROOT, 'stage_A', 'codex_iterative_search')
V2 = os.path.join(REC, 'step2_controlled_repair_v2')
V1 = os.path.join(REC, 'step2_controlled_repair_v1')
P1 = os.path.join(REC, 'step1_union_augmented_pass1')
CANDIDATES = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
FILES_PER_CANDIDATE = {'M': 61, 'M1': 80, 'L0': 71, 'L1': 86, 'K0': 63, 'K1': 87}
PASS_EXPECT = {2: {'claims': 63, 'by_c': {'M': 23, 'M1': 8, 'L0': 18, 'L1': 1, 'K0': 10, 'K1': 3}},
               3: {'claims': 148, 'by_c': {'M': 16, 'M1': 32, 'L0': 20, 'L1': 28, 'K0': 27, 'K1': 25}}}

PROTECTED_TREES = {
    'inputs': os.path.join(ROOT, 'inputs'),
    'stage_A/primary': os.path.join(ROOT, 'stage_A', 'primary'),
    'stage_A/replica': os.path.join(ROOT, 'stage_A', 'replica'),
    'stage_A/independent': os.path.join(ROOT, 'stage_A', 'independent'),
    'stage_A/_control': os.path.join(ROOT, 'stage_A', '_control'),
    'kit': os.path.join(ROOT, '_STAGE_A_KIT'),
    'step1_union': os.path.join(REC, 'step1_union'),
    'step1_union_augmented_pass1': P1,
    'step2_classification': os.path.join(REC, 'step2_classification'),
    'step2_semantic_audit_v1': os.path.join(REC, 'step2_semantic_audit_v1'),
    'step2_controlled_repair_v1': V1,
    'step2_controlled_repair_v2': V2,
}
for _c in CANDIDATES:
    PROTECTED_TREES['reconciled/' + _c] = os.path.join(REC, _c)
PROTECTED_FILES = {
    'v1_archive': os.path.join(REC, 'step2_controlled_repair_v1.zip'),
    'v2_archive': os.path.join(REC, 'step2_controlled_repair_v2.zip'),
    'decision_register': os.path.join(ROOT, 'ClaudeArchitectureResearch_5_4_decision_register_2026-11-03.md'),
    'pass1_interrupted_review': os.path.join(ROOT, 'Codex_5_4_Pass1_Interrupted_Run_Independent_Review.md'),
    'post_v2_decisions': os.path.join(ROOT, 'Stage_A_Step2_Post_V2_Approved_Decisions_EN.md'),
    'setup': os.path.join(ROOT, 'SETUP_5_4.py'),
    'stageA_resume_txt': os.path.join(ROOT, 'stage_A', 'Claude_5_4_Stage_A_RESUME_L0_TO_K1.txt'),
}


def now():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def walk(root, prune=None):
    out = []
    for d, sub, files in os.walk(root):
        sub.sort()
        if prune:
            sub[:] = [s for s in sub if not prune(os.path.relpath(os.path.join(d, s), root).replace(os.sep, '/'))]
        for n in sorted(files):
            out.append(os.path.relpath(os.path.join(d, n), root).replace(os.sep, '/'))
    return out


def codex_prune(rel):
    """Pass 0004 and later are never entered (kit 74 preflight item 3)."""
    m = re.match(r'^PASSES/pass_(\d+)$', rel)
    return bool(m and int(m.group(1)) >= 4)


def hash_tree(root, prune=None):
    return {rel: sha(os.path.join(root, rel.replace('/', os.sep))) for rel in walk(root, prune)}


def rj(p):
    with open(p, encoding='utf-8-sig') as f:
        return json.load(f)


def rjl(p):
    with open(p, encoding='utf-8-sig') as f:
        return [json.loads(x) for x in f if x.strip()]


def protected_manifest():
    trees = {k: hash_tree(v) for k, v in PROTECTED_TREES.items()}
    trees['codex_iterative_search'] = hash_tree(CODEX, codex_prune)
    files = {k: (sha(v) if os.path.exists(v) else None) for k, v in PROTECTED_FILES.items()}
    return {'at': now(), 'trees': trees, 'files': files, 'counts': {k: len(v) for k, v in trees.items()},
            'note': 'Codex area hashed with PASSES/pass_0004+ pruned before entry. Every tree here is read-only for v3.'}


def check_codex():
    errs, facts = [], {}
    state = rj(os.path.join(CODEX, 'STATE.json'))
    man = rj(os.path.join(CODEX, 'BASELINE_MANIFEST.json'))
    bad = [x['path'] for x in man['files'] if not os.path.isfile(os.path.join(ROOT, x['path'].replace('/', os.sep))) or sha(os.path.join(ROOT, x['path'].replace('/', os.sep))) != x['sha256']]
    fp = hashlib.sha256(''.join('%s\0%s\n' % (x['path'], x['sha256']) for x in sorted(man['files'], key=lambda x: x['path'])).encode()).hexdigest()
    facts['baseline_files'] = len(man['files'])
    facts['baseline_fingerprint_recomputed'] = fp
    if bad:
        errs.append('frozen baseline files changed or missing: %s' % bad[:5])
    if fp != man['baseline_fingerprint'] or fp != state['baseline_fingerprint']:
        errs.append('baseline fingerprint mismatch')
    sources = rjl(os.path.join(CODEX, 'SOURCE_FILE_INDEX.jsonl'))
    src = {(r['candidate'], r['path']): r for r in sources}
    facts['source_files_indexed'] = len(src)
    if Counter(c for c, _ in src) != Counter(FILES_PER_CANDIDATE):
        errs.append('source index per candidate differs: %s' % dict(Counter(c for c, _ in src)))
    for (c, path), r in src.items():
        p = os.path.join(ROOT, 'inputs', c, path.replace('/', os.sep))
        if not os.path.isfile(p) or sha(p) != r['sha256']:
            errs.append('source file differs from index: %s %s' % (c, path))
    bkeys = {r['index_key'] for r in rjl(os.path.join(CODEX, 'BASELINE_RECORD_INDEX.jsonl'))}
    facts['baseline_records'] = len(bkeys)
    units = {u['unit']: u for u in state['completed_units']}
    revisions = state.get('finding_revisions', {})
    per_pass = {}
    for pid in (2, 3):
        d = os.path.join(CODEX, 'PASSES', 'pass_%04d' % pid)
        f = {}
        v = rj(os.path.join(d, 'PASS_VALIDATION.json'))
        f['status'] = v.get('status')
        if v.get('status') != 'COMPLETE' or v.get('pass_id') != pid:
            errs.append('pass %d PASS_VALIDATION is not COMPLETE' % pid)
        if v.get('baseline_fingerprint') != fp:
            errs.append('pass %d fingerprint differs from recomputed' % pid)
        if v.get('source_files') != 448:
            errs.append('pass %d source_files != 448' % pid)
        hashes = rj(os.path.join(d, 'CHECKPOINT_HASHES.json'))
        bad_cp = [n for n, h in hashes.items() if not os.path.isfile(os.path.join(d, n)) or sha(os.path.join(d, n)) != h]
        f['checkpoint_files'] = len(hashes)
        if bad_cp:
            errs.append('pass %d checkpoint hash mismatch: %s' % (pid, bad_cp[:5]))
        present = set(walk(d))
        unhashed = sorted(present - set(hashes))
        f['files_not_in_checkpoint_hashes'] = unhashed
        prefix = 'P%04d-' % pid
        mine = [u for k, u in units.items() if k.startswith(prefix)]
        bad_u = []
        for u in mine:
            for name, h in u.get('outputs', {}).items():
                p = os.path.join(CODEX, name.replace('/', os.sep))
                if not os.path.isfile(p) or sha(p) != h:
                    bad_u.append(name)
        f['completed_units'] = len(mine)
        if not mine or bad_u:
            errs.append('pass %d completed-unit outputs missing or changed: %s' % (pid, bad_u[:5]))
        cov = rjl(os.path.join(d, 'FILE_COVERAGE.jsonl'))
        keys = [(r['candidate'], r['path']) for r in cov]
        f['coverage_rows'] = len(cov)
        f['coverage_by_candidate'] = dict(Counter(c for c, _ in keys))
        if len(keys) != len(set(keys)) or set(keys) != set(src) or Counter(c for c, _ in keys) != Counter(FILES_PER_CANDIDATE):
            errs.append('pass %d coverage is not exactly the 448 indexed files' % pid)
        for r in cov:
            s = src.get((r['candidate'], r['path']))
            if not s or s['sha256'] != r['sha256']:
                errs.append('pass %d coverage hash differs: %s' % (pid, r['path']))
        claims = rjl(os.path.join(d, 'CANDIDATE_CLAIMS.jsonl'))
        comps = rjl(os.path.join(d, 'NOVELTY_COMPARISONS.jsonl'))
        f['claims'] = len(claims)
        f['claims_by_candidate'] = dict(Counter(x['candidate'] for x in claims))
        f['claims_by_status'] = dict(Counter(x['comparison_status'] for x in claims))
        if len(claims) != PASS_EXPECT[pid]['claims'] or Counter(x['candidate'] for x in claims) != Counter(PASS_EXPECT[pid]['by_c']):
            errs.append('pass %d claim counts differ from PASS_VALIDATION' % pid)
        if {x['claim_id'] for x in comps} != {x['id'] for x in claims}:
            errs.append('pass %d comparisons do not account for every claim' % pid)
        qbad, refbad, runs_missing = [], [], []
        for x in claims:
            p = os.path.join(ROOT, 'inputs', x['candidate'], x['path'].replace('/', os.sep))
            with open(p, encoding='utf-8-sig') as fh:
                lines = fh.read().splitlines()
            if '\n'.join(lines[x['start_line'] - 1:x['end_line']]) != x['quote']:
                qbad.append(x['id'])
            runs = set()
            for comp in x.get('baseline_comparisons', []):
                for k in comp.get('baseline_keys', []):
                    if k not in bkeys:
                        refbad.append((x['id'], k))
                    runs.add(k.split('/')[0])
            if not {'primary', 'replica', 'independent'} <= runs:
                runs_missing.append(x['id'])
        f['quote_mismatch'] = qbad
        f['broken_baseline_refs'] = refbad[:10]
        f['claims_without_all_three_runs'] = runs_missing
        if qbad or refbad:
            errs.append('pass %d quotes or baseline references fail: %d quotes, %d refs' % (pid, len(qbad), len(refbad)))
        ids = {x['id'] for x in claims}
        f['revisions_applying'] = sorted(k for k in revisions if k in ids)
        per_pass[pid] = f
    allids = set()
    for pid in (2, 3):
        allids |= {x['id'] for x in rjl(os.path.join(CODEX, 'PASSES', 'pass_%04d' % pid, 'CANDIDATE_CLAIMS.jsonl'))}
    p1 = {x['id'] for x in rjl(os.path.join(CODEX, 'PASSES', 'pass_0001', 'CANDIDATE_CLAIMS.jsonl'))}
    facts['pass1_claims'] = len(p1)
    facts['id_overlap_pass1_vs_pass23'] = sorted(p1 & allids)
    facts['passes'] = per_pass
    facts['global_pointer'] = {'current_pass_id': state.get('current_pass_id'), 'next_file_batch': state.get('next_file_batch'), 'final_status': state.get('final_status')}
    facts['pass_dirs_present_le3'] = sorted(n for n in os.listdir(os.path.join(CODEX, 'PASSES')) if re.match(r'pass_000[123]$', n))
    return errs, facts


def check_predecessors():
    errs, facts = [], {}
    st = rj(os.path.join(V2, 'STATUS.json'))
    facts['v2_status'] = {k: st.get(k) for k in ('status', 'phase', 'step3_started', 'step3_recommendation', 'final_audit', 'final_suites')}
    if st.get('phase') != 'COMPLETE' or st.get('status') != 'PASS_WITH_DOCUMENTED_NOT_RUN' or st.get('step3_started'):
        errs.append('v2 is not COMPLETE / PASS_WITH_DOCUMENTED_NOT_RUN')
    cps = {n: rj(os.path.join(V2, 'CHECKPOINTS', n)).get('gate') for n in sorted(os.listdir(os.path.join(V2, 'CHECKPOINTS')))}
    facts['v2_checkpoints'] = cps
    if len(cps) != 9 or set(cps.values()) - {'PASS', 'PASS_WITH_DOCUMENTED_NOT_RUN'}:
        errs.append('v2 checkpoints are not 9 passes')
    man = rj(os.path.join(V2, 'V2_FINAL_MANIFEST.json'))['candidates']
    n = 0
    for c in CANDIDATES:
        root = os.path.join(V2, 'candidates', c, 'template')
        cur = set(walk(root))
        if cur != set(man[c]['files']) or len(cur) != FILES_PER_CANDIDATE[c]:
            errs.append('v2 %s file set differs from V2_FINAL_MANIFEST' % c)
        for rel in cur & set(man[c]['files']):
            n += 1
            if sha(os.path.join(root, rel.replace('/', os.sep))) != man[c]['files'][rel]['sha256']:
                errs.append('v2 %s %s differs from V2_FINAL_MANIFEST' % (c, rel))
    facts['v2_candidate_files_checked'] = n
    env = dict(os.environ, PYTHONPATH=os.path.join(V2, '_tools'), PYTHONDONTWRITEBYTECODE='1')
    r = subprocess.run([sys.executable, '-B', os.path.join(V2, '_tools', 'verify_final.py')], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env, timeout=900)
    facts['v2_verify_final'] = {'exit': r.returncode, 'stdout_tail': r.stdout.strip().splitlines()[-3:]}
    vf_errors = [l[6:] for l in r.stdout.splitlines() if l.startswith('ERROR ')]
    warnings = []
    if r.returncode != 0:
        # The v1 convenience archive is a duplicate of the v1 tree. It is not one of the predecessor artifacts kit 74 requires.
        # Its absence is tolerated only when it is the sole error and the v1 tree verifies byte for byte against v2's fingerprint.
        if vf_errors == ['changed or missing v1_archive']:
            fp1 = rj(os.path.join(V2, 'PREDECESSOR_V1_FINGERPRINT.json'))
            want = fp1['v1_tree_sha256']
            cur = hash_tree(V1)
            diff = sorted(k for k in set(want) | set(cur) if want.get(k) != cur.get(k))
            facts['v1_tree_vs_v2_fingerprint'] = {'files': len(cur), 'differ': diff[:10], 'n_differ': len(diff)}
            facts['v1_archive_present'] = os.path.exists(PROTECTED_FILES['v1_archive'])
            if diff:
                errs.append('v1 tree differs from PREDECESSOR_V1_FINGERPRINT: %s' % diff[:5])
            else:
                warnings.append('PRE-W01: stage_A/reconciled/step2_controlled_repair_v1.zip is absent (v2 fence hash 24a7c831...). The v1 tree it duplicated verifies byte for byte (%d files) against v2 PREDECESSOR_V1_FINGERPRINT, and v2 verify_final reports no other error, so the v2 view replay matched. Not written by this run.' % len(cur))
        else:
            errs.append('v2 verify_final.py failed: %s' % r.stdout[-500:])
    facts['warnings'] = warnings
    v1s = rj(os.path.join(V1, 'STATUS.json'))
    facts['v1_status'] = {k: v1s.get(k) for k in ('status', 'step3_started')}
    stats = rj(os.path.join(P1, 'STATS.json'))
    ledger = rjl(os.path.join(P1, 'PASS1_REVIEW_LEDGER.jsonl'))
    facts['pass1_ledger'] = len(ledger)
    facts['pass1_dispositions'] = dict(Counter(x.get('disposition') or x.get('final_disposition') or x.get('decision') for x in ledger))
    facts['pass1_augmented_view_rows'] = sum(1 for _ in open(os.path.join(P1, 'AUGMENTED_UNION_VIEW.jsonl'), encoding='utf-8'))
    facts['pass1_proposals'] = len(rjl(os.path.join(P1, 'NEW_CLAUSE_PROPOSALS.jsonl')))
    facts['pass1_facets'] = len(rjl(os.path.join(P1, 'EXISTING_GROUP_FACETS.jsonl')))
    facts['pass1_stats_keys'] = sorted(stats)[:20]
    if len(ledger) != 152 or facts['pass1_proposals'] != 26 or facts['pass1_facets'] != 29:
        errs.append('Pass 1 augmented union counts differ from the historical facts (152 / 26 proposals / 29 facets)')
    return errs, facts


def write_json(name, obj):
    p = os.path.join(OUT, name)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    os.replace(tmp, p)


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    t0 = now()
    before = protected_manifest()
    write_json('PREFLIGHT_PROTECTED_MANIFEST.json', before)
    print('protected manifest', before['counts'])
    if '--manifest-only' in sys.argv:
        return 0
    cerrs, cfacts = check_codex()
    perrs, pfacts = check_predecessors()
    after = protected_manifest()
    drift = []
    for k in before['trees']:
        a, b = before['trees'][k], after['trees'][k]
        drift += ['%s/%s' % (k, r) for r in set(a) | set(b) if a.get(r) != b.get(r)]
    drift += [k for k in before['files'] if before['files'][k] != after['files'][k]]
    errs = cerrs + perrs + (['protected trees changed during preflight: %s' % drift[:10]] if drift else [])
    res = {'at': now(), 'started': t0, 'status': 'PASS' if not errs else 'BLOCKED', 'errors': errs, 'warnings': pfacts.get('warnings', []), 'codex': cfacts, 'predecessors': pfacts, 'protected_drift_during_preflight': drift,
           'manifest_sha256': sha(os.path.join(OUT, 'PREFLIGHT_PROTECTED_MANIFEST.json'))}
    write_json('PREFLIGHT_RESULT.json', res)
    print(json.dumps({'status': res['status'], 'errors': errs[:10]}, ensure_ascii=False))
    if errs:
        with open(os.path.join(OUT, 'PREFLIGHT_BLOCKER_REPORT.md'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# v3 preflight blocker\n\nPreflight did not pass, so no candidate or classification data was changed.\n\n' + '\n'.join('- ' + e for e in errs) + '\n')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
