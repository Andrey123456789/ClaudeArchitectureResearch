"""v3 bootstrap: an immutable copy of the verified v2 final state into v3 (kit 74 Part C, first bullet).

python -B _tools/bootstrap_v3.py

Requires PREFLIGHT_RESULT.json status PASS. Copies the six v2 candidate trees, v2's rule data and the derived data files the replayed
suites and the dataset read at the same relative path. Logs, checkpoints, gate outputs, audit outputs and reports stay in v2 and are
recorded here by hash only, so v2 remains the one source of its history. Refuses to overwrite a candidate tree that already exists.
Writes V3_BASELINE_MANIFEST.json. Nothing upstream is written.
Re-runnable before the first v3 change: an existing copy is verified against its v2 origin, never overwritten.
v2 rule folders are copied whole, including before/ snapshots: C01's patches.py reads its snapshot when loaded.
"""
import os
import shutil
import sys

from rcommon import CANDIDATES, OUT, V2, VERSION, now, out_path, read_json, sha256_file, template_root, utf8_stdout, v2_path, walk_files, write_json

# v2 files that stay in v2: logs, checkpoints and per-gate outputs (history), the final audit's outputs, and v2's own reports.
REFERENCED = ['CHANGE_LOG.jsonl', 'GATE_LOG.jsonl', 'CLAIM_GATE_LOG.jsonl', 'STATUS.json', 'RESUME.md', 'FINAL_PARITY_AND_CONSISTENCY_REPORT.md', 'REGRESSION_MATRIX.md', 'FINAL_AUDIT_RESULTS.jsonl', 'FINAL_SUITE_TALLY.json',
              'V2_FINAL_MANIFEST.json', 'WORKING_COPY_MANIFEST.json', 'V1_TO_V2_CROSSWALK.jsonl', 'SAME_TASK_MATRIX.json', 'SAME_TASK_MATRIX_V2.json', 'INTERACTION_MATRIX.json', 'POLICY_PARITY_MATRIX.jsonl', 'POLICY_IMPACT_GRAPH.json',
              'R27_AUDIT_REPLAY_RESULTS.jsonl', 'FENCE_SNAPSHOT.json', 'APPROVED_SCOPE_AND_DECISIONS.md']
REFERENCED_DIRS = ['CHECKPOINTS', 'POLICY_CHECKS', '_scratch', '_tools', 'candidates']
# TEST_RESULTS files that suites read as data. The rest of TEST_RESULTS is v2 gate output.
TEST_DATA = ['TEST_RESULTS/R01_per_record.jsonl', 'TEST_RESULTS/R25_per_record.jsonl']
# Derived files every gate rebuilds from the frozen baseline and rule data. Their v2 hash is recorded; a v3 rebuild may differ (timestamps, v3 changes).
REGENERATED = ['REPAIRED_CLASSIFICATIONS.jsonl', 'REPAIRED_POLICY_COVERAGE.jsonl', 'ORIGINAL_TO_REPAIRED_CLAIMS.jsonl', 'CLAIM_DISPOSITIONS.jsonl', 'POLICY_DEPENDENCY_GRAPH.json', 'DATASET_MANIFEST.json', 'REPAIRED_VIEW_MANIFEST.json']


def main():
    utf8_stdout()
    pf = read_json(out_path('PREFLIGHT_RESULT.json'))
    if pf.get('status') != 'PASS':
        print('STOP: preflight did not pass')
        return 2
    man = {'version': VERSION, 'created_at': now(), 'predecessor': 'stage_A/reconciled/step2_controlled_repair_v2', 'preflight_sha256': sha256_file(out_path('PREFLIGHT_RESULT.json')),
           'candidates': {}, 'data_copied_from_v2': {}, 'v2_rule_data_sha256': {}, 'referenced_v2_sha256': {}, 'v2_tools_sha256': {}}
    for c in CANDIDATES:
        src, dst = v2_path('candidates', c, 'template'), template_root(c)
        exists = os.path.exists(dst) and os.listdir(dst)
        if exists and read_json(out_path('V3_BASELINE_MANIFEST.json')).get('created_at') and os.path.exists(out_path('CHANGE_LOG.jsonl')):
            print('STOP: v3 changes exist; the baseline is frozen')
            return 2
        files = {}
        for rel in walk_files(src):
            s = os.path.join(src, rel.replace('/', os.sep))
            d = os.path.join(dst, rel.replace('/', os.sep))
            files[rel] = sha256_file(s)
            if not exists:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(s, d)
            if sha256_file(d) != files[rel]:
                print('STOP: copy differs from v2', c, rel)
                return 2
        if exists and set(walk_files(dst)) != set(files):
            print('STOP: copy file set differs from v2', c)
            return 2
        man['candidates'][c] = {'origin': 'stage_A/reconciled/step2_controlled_repair_v2/candidates/%s/template' % c, 'working_root': 'candidates/%s/template' % c, 'n_files': len(files), 'files': files}
    v2final = read_json(v2_path('V2_FINAL_MANIFEST.json'))['candidates']
    for c in CANDIDATES:
        bad = [rel for rel, h in man['candidates'][c]['files'].items() if v2final[c]['files'][rel]['sha256'] != h]
        if bad or set(man['candidates'][c]['files']) != set(v2final[c]['files']):
            print('STOP: copied tree differs from V2_FINAL_MANIFEST', c, bad[:4])
            return 2
    for name in sorted(os.listdir(V2)):
        p = v2_path(name)
        if os.path.isdir(p):
            continue
        if name in REFERENCED or name.endswith('.zip'):
            man['referenced_v2_sha256'][name] = sha256_file(p)
            continue
        d = out_path(name)
        if not os.path.exists(d):
            shutil.copyfile(p, d)
        if name not in REGENERATED and sha256_file(d) != sha256_file(p):
            print('STOP: copy differs from v2', name)
            return 2
        man['data_copied_from_v2'][name] = sha256_file(p)
    for rel in TEST_DATA:
        d = out_path(*rel.split('/'))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if not os.path.exists(d):
            shutil.copyfile(v2_path(*rel.split('/')), d)
        man['data_copied_from_v2'][rel] = sha256_file(v2_path(*rel.split('/')))
    for rule in sorted(os.listdir(v2_path('_rules'))):
        for rel in walk_files(v2_path('_rules', rule)):
            if rel.startswith('suite_'):
                continue
            src_p = v2_path('_rules', rule, *rel.split('/'))
            d = out_path('_rules', rule, *rel.split('/'))
            if not os.path.exists(d):
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(src_p, d)
            if sha256_file(d) != sha256_file(src_p):
                print('STOP: rule copy differs from v2', rule, rel)
                return 2
            man['v2_rule_data_sha256']['%s/%s' % (rule, rel)] = sha256_file(d)
    man['v2_tools_sha256'] = {rel: sha256_file(v2_path('_tools', *rel.split('/'))) for rel in walk_files(v2_path('_tools'))}
    man['referenced_v2_dirs'] = {dname: {rel: sha256_file(v2_path(dname, *rel.split('/'))) for rel in walk_files(v2_path(dname))} for dname in ('CHECKPOINTS', 'POLICY_CHECKS') if os.path.isdir(v2_path(dname))}
    write_json('V3_BASELINE_MANIFEST.json', man)
    print('v3 baseline written;', {c: man['candidates'][c]['n_files'] for c in CANDIDATES}, 'data', len(man['data_copied_from_v2']), 'rule files', len(man['v2_rule_data_sha256']), 'referenced', len(man['referenced_v2_sha256']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
