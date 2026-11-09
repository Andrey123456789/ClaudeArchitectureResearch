"""v2 preflight. Verifies v1 and the frozen inputs, copies the v1 repaired candidates and derived data, and writes the fingerprints.

Idempotent for verification; it refuses to replace a candidate tree that already exists. Nothing upstream is written.
The manifests record what came from where, so v2 can be replayed standalone and v1 stays the only source for its history.
"""
import csv
import json
import os
import shutil
import sys

from rcommon import AUD, CANDIDATES, INPUTS, OUT, REC, ROOT, S2, V1, VERSION, now, out_path, read_json, read_jsonl, sha256_file, template_root, utf8_stdout, v1_path, walk_files, write_json, write_jsonl

# Derived v1 data that the replayed suites and dataset read at the same relative path. Each copy is hash-recorded.
DATA = ['CORRECTION_103_ADJUDICATION.jsonl', 'CROSS_METHOD_ADJUDICATION.jsonl', 'EVIDENCE_LIMITS.md', 'NEW_CLAUSES_4_ADJUDICATION.jsonl', 'PI012_230_REVIEW.jsonl', 'PI012_79_REVIEW.jsonl', 'PI012_EXTENSION_REVIEW.jsonl', 'PI012_SENSITIVITY.md', 'PROTOCOL_PI012_APPROVED_ADDENDUM.md',
        'UNRESOLVED_DECISIONS.jsonl', 'TEST_RESULTS/R01_per_record.jsonl']
# v1 outputs v2 regenerates; v1's bytes are kept here only as hashes, so the first replay can be compared with them.
REGENERATED = ['REPAIRED_CLASSIFICATIONS.jsonl', 'REPAIRED_POLICY_COVERAGE.jsonl', 'ORIGINAL_TO_REPAIRED_CLAIMS.jsonl', 'CLAIM_DISPOSITIONS.jsonl', 'POLICY_DEPENDENCY_GRAPH.json', 'SAME_TASK_MATRIX.json', 'FINAL_AUDIT_RESULTS.jsonl', 'WORKING_COPY_MANIFEST.json']
# Referenced, not copied: raw logs and large history stay in v1 under their hashes.
REFERENCED = ['CHANGE_LOG.jsonl', 'GATE_LOG.jsonl', 'FINAL_CONSISTENCY_REPORT.md', 'DECISION_IMPLEMENTATION_MATRIX.md', 'STATUS.json', 'RESUME.md', 'BASELINE_MANIFEST.json', 'FENCE_SNAPSHOT.json', 'REPAIRED_VIEW_MANIFEST.json']


def tree_hashes(root):
    return {rel: sha256_file(os.path.join(root, rel.replace('/', os.sep))) for rel in walk_files(root)}


def verify_input_csv():
    p = os.path.join(INPUTS, 'INPUT_MANIFEST_SHA256.csv')
    n, bad = 0, []
    with open(p, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            n += 1
            fp = os.path.join(INPUTS, row['relative_path'].replace('/', os.sep))
            if not os.path.exists(fp) or sha256_file(fp) != row['sha256']:
                bad.append(row['relative_path'])
    return {'n_checked': n, 'mismatch': bad}


def verify_v1():
    """v1 final state: working copies, view manifest, last-logged hashes and checkpoints. Returns problems, plus facts for the fingerprint."""
    problems = []
    wc = read_json(v1_path('WORKING_COPY_MANIFEST.json'))
    n = 0
    for c in CANDIDATES:
        root = v1_path('candidates', c, 'template')
        cur = set(walk_files(root))
        want = wc['candidates'][c]
        if cur != set(want):
            problems.append('%s: working copy path set differs from v1 manifest: %s' % (c, sorted(cur ^ set(want))[:5]))
        for rel, e in want.items():
            n += 1
            if sha256_file(os.path.join(root, rel.replace('/', os.sep))) != e['sha256']:
                problems.append('%s %s: hash differs from v1 manifest' % (c, rel))
    last = {}
    for r in read_jsonl(v1_path('CHANGE_LOG.jsonl')):
        if r.get('kind') == 'TEMPLATE':
            last[(r['candidate'], r['file'])] = r['after_sha256']
    for (c, rel), h in last.items():
        if sha256_file(v1_path('candidates', c, 'template', *rel.split('/'))) != h:
            problems.append('%s %s: differs from the last v1 change-log hash' % (c, rel))
    view = read_json(v1_path('REPAIRED_VIEW_MANIFEST.json'))
    for f, h in view['sha256'].items():
        if sha256_file(v1_path(f)) != h:
            problems.append('%s differs from REPAIRED_VIEW_MANIFEST' % f)
    gates = read_jsonl(v1_path('GATE_LOG.jsonl'))
    cps = {}
    for name in sorted(os.listdir(v1_path('CHECKPOINTS'))):
        cps[name] = read_json(v1_path('CHECKPOINTS', name)).get('gate')
    if len(cps) != 27 or set(cps.values()) - {'PASS', 'PASS_WITH_NOT_RUN'}:
        problems.append('v1 checkpoints are not 27 passes: %s' % cps)
    if gates[-1]['rule'] != 'R27-FINAL':
        problems.append('v1 last gate is not R27-FINAL')
    status = read_json(v1_path('STATUS.json'))
    return problems, {'n_working_files': n, 'n_change_log_files': len(last), 'final_gate': gates[-1]['gate'], 'final_tally': gates[-1]['steps']['CUMULATIVE']['tally'], 'status': status['status'], 'step3_started': status['step3_started'], 'checkpoints': len(cps)}


def main():
    utf8_stdout()
    problems, facts = verify_v1()
    csvr = verify_input_csv()
    print('v1 facts', facts, 'problems', problems[:10])
    print('input csv', csvr['n_checked'], 'bad', len(csvr['mismatch']))
    if problems or csvr['mismatch']:
        print('STOP: predecessor or inputs do not verify')
        return 2
    zc = os.path.join(OUT, '_scratch', 'v1_zip_compare.json')
    fp = {'version': VERSION, 'at': now(), 'predecessor': 'stage_A/reconciled/step2_controlled_repair_v1', 'facts': facts, 'archive_comparison': read_json(zc) if os.path.exists(zc) else None, 'archive_sha256': sha256_file(os.path.join(REC, 'step2_controlled_repair_v1.zip')),
          'v1_tree_sha256': tree_hashes(V1), 'candidates_tree_sha256': {c: tree_hashes(v1_path('candidates', c, 'template')) for c in CANDIDATES}, 'regenerated_output_sha256': {f: sha256_file(v1_path(f)) for f in REGENERATED}, 'referenced_sha256': {f: sha256_file(v1_path(f)) for f in REFERENCED}, 'known_v1_fence_note': 'v1 fence.verify reports 2 removed kit files (63_README_CONTROLLED_CORRECTIONS_RU.md, 62_APPROVED_DECISIONS_AND_GATES_RU.md): the user replaced them with the English kit before this run. Not a v1 defect and not caused here.'}
    write_json('PREDECESSOR_V1_FINGERPRINT.json', fp)
    man = {'version': VERSION, 'created_at': now(), 'input_csv_verification': {'n_checked': csvr['n_checked'], 'mismatch': csvr['mismatch']}, 'authoritative_inputs_sha256': {c: {'CANDIDATE.md': sha256_file(os.path.join(INPUTS, c, 'CANDIDATE.md')), 'REFINEMENT_TASK.md': sha256_file(os.path.join(INPUTS, c, 'REFINEMENT_TASK.md')), 'inventory.json': sha256_file(os.path.join(INPUTS, c, 'source', 'inventory.json')), 'shared-research-invariants.json': sha256_file(os.path.join(INPUTS, c, 'source', 'shared-research-invariants.json')), 'baseline/TASK.md': sha256_file(os.path.join(INPUTS, c, 'baseline', 'TASK.md')) if os.path.exists(os.path.join(INPUTS, c, 'baseline', 'TASK.md')) else None} for c in CANDIDATES},
           'inventories_identical': len({sha256_file(os.path.join(INPUTS, c, 'source', 'inventory.json')) for c in CANDIDATES}) == 1, 'frozen_classification_sha256': {c: {n: sha256_file(os.path.join(S2, 'per_candidate', c, n)) for n in ('CLASSIFICATIONS.jsonl', 'POLICY_COVERAGE.jsonl')} for c in CANDIDATES}, 'candidates': {}, 'data_copied_from_v1': {}, 'codex_area': 'not read, listed, hashed or stat-ed'}
    if not man['inventories_identical']:
        print('STOP: inventories differ')
        return 2
    for c in CANDIDATES:
        src, dst = v1_path('candidates', c, 'template'), template_root(c)
        if os.path.exists(dst) and os.listdir(dst):
            print('candidate tree exists, verifying only:', c)
            if tree_hashes(dst) != tree_hashes(src):
                print('note: %s differs from v1 baseline (expected after a change)' % c)
        else:
            for rel in walk_files(src):
                s = os.path.join(src, rel.replace('/', os.sep))
                d = os.path.join(dst, rel.replace('/', os.sep))
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(s, d)
                if sha256_file(s) != sha256_file(d):
                    print('STOP: copy mismatch', c, rel)
                    return 2
        man['candidates'][c] = {'origin': 'stage_A/reconciled/step2_controlled_repair_v1/candidates/%s/template' % c, 'working_root': 'candidates/%s/template' % c, 'n_files': len(walk_files(src)), 'files': tree_hashes(src)}
    for f in DATA:
        d = out_path(*f.split('/'))
        if not os.path.exists(d):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(v1_path(*f.split('/')), d)
        man['data_copied_from_v1'][f] = sha256_file(v1_path(*f.split('/')))
    # v1 rule folders: overlays, updates, reviews, dispositions and notes. `before/` snapshots and suite run files stay in v1.
    rules = {}
    for rule in sorted(os.listdir(v1_path('_rules'))):
        for rel in walk_files(v1_path('_rules', rule)):
            if rel.startswith('before/') or rel.startswith('suite_') or rel.startswith('blind/'):
                continue
            d = out_path('_rules', rule, *rel.split('/'))
            if not os.path.exists(d):
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(v1_path('_rules', rule, *rel.split('/')), d)
            rules['%s/%s' % (rule, rel)] = sha256_file(d)
    man['v1_rule_data_sha256'] = rules
    man['v1_tools_sha256'] = {rel: sha256_file(v1_path('_tools', *rel.split('/'))) for rel in walk_files(v1_path('_tools'))}
    write_json('V2_BASELINE_MANIFEST.json', man)
    print('baseline manifest written;', {c: man['candidates'][c]['n_files'] for c in CANDIDATES}, 'data', len(man['data_copied_from_v1']), 'rule files', len(rules))
    return 0


if __name__ == '__main__':
    sys.exit(main())
