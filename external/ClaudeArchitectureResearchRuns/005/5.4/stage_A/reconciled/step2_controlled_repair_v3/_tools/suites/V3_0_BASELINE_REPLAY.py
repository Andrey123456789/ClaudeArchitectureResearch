"""V3-0 regression: v3 starts as an exact copy of v2's final state, and the ported tools reproduce v2's view. Data and bytes only."""
import os

import dataset
from rcommon import CANDIDATES, out_path, read_json, read_jsonl, rec_hash, sha256_file, template_root, v2_path, walk_files, wc_path
from witness import FileMap

RULE = 'V3-0-BASELINE-REPLAY'
VIEW = ('REPAIRED_CLASSIFICATIONS.jsonl', 'REPAIRED_POLICY_COVERAGE.jsonl', 'ORIGINAL_TO_REPAIRED_CLAIMS.jsonl')


def run(ctx):
    from order import V3_ORDER
    later = V3_ORDER[V3_ORDER.index(RULE) + 1:]
    touched = [r for r in read_jsonl(out_path('CHANGE_LOG.jsonl')) if r.get('rule') in later]
    base = read_json(out_path('V3_BASELINE_MANIFEST.json'))
    v2final = read_json(v2_path('V2_FINAL_MANIFEST.json'))['candidates']
    for c in CANDIDATES:
        files = set(walk_files(template_root(c)))
        ctx.check('the file set equals v2 final', files == set(v2final[c]['files']), sorted(files ^ set(v2final[c]['files']))[:4], c, 'DATA')
        if not touched:
            bad = [rel for rel in files if sha256_file(wc_path(c, rel)) != v2final[c]['files'][rel]['sha256']]
            ctx.check('every file equals its v2 final bytes (before any v3 change)', not bad, bad[:4], c, 'DATA')
        ctx.check('the baseline manifest records v2 final bytes', all(base['candidates'][c]['files'][rel] == v2final[c]['files'][rel]['sha256'] for rel in files), candidate=c, kind='DATA')
    for name, h in base['data_copied_from_v2'].items():
        p = v2_path(*name.split('/'))
        ctx.check('copied data still equals v2 at origin: %s' % name, os.path.exists(p) and sha256_file(p) == h, kind='DATA')
    if not later or not any(os.path.exists(out_path('_rules', r, 'updates.py')) for r in later):
        rows, cross = dataset.build()
        mine = [r for c in CANDIDATES for r in rows[c]]
        v2rows = read_jsonl(v2_path('REPAIRED_CLASSIFICATIONS.jsonl'))
        ctx.check('the replay equals v2 view record for record', rec_hash(mine) == rec_hash(v2rows), kind='DATA', actual=len(mine))
        ctx.check('the crosswalk equals v2 crosswalk', rec_hash(cross) == rec_hash(read_jsonl(v2_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))), kind='DATA')
        cov, moved = dataset.coverage_rows(rows)
        ctx.check('1,176 coverage cells equal v2 cells', rec_hash(cov) == rec_hash(read_jsonl(v2_path('REPAIRED_POLICY_COVERAGE.jsonl'))) and len(cov) == 1176, kind='DATA')
        x = dataset.v2_to_v3(mine)
        ctx.check('every v2-to-v3 crosswalk row is UNCHANGED', all(r['status'] == 'UNCHANGED' for r in x) and len(x) == len(v2rows), sorted({r['status'] for r in x}), kind='DATA')
        # Mutation: one changed field in one record must surface in the crosswalk.
        mut = [dict(r) for r in mine]
        mut[0] = dict(mut[0], modality='MAY' if mut[0].get('modality') != 'MAY' else 'MUST')
        ctx.check('mutation: a changed modality appears as CLASSIFICATION_CHANGED', dataset.v2_to_v3(mut)[0]['status'] == 'CLASSIFICATION_CHANGED', kind='MUTATION')
    else:
        # After v3 updates exist, every difference from v2 must be attributable to a declared v3 change or be an anchor shift from a logged template edit.
        rows, _ = dataset.build()
        x = dataset.v2_to_v3([r for c in CANDIDATES for r in rows[c]])
        bad = [r['source_key'] for r in x if r['status'] not in ('UNCHANGED', 'ANCHOR_SHIFT_ONLY') and not r.get('v3_rules')]
        ctx.check('every difference from v2 view names the v3 change that made it', not bad, bad[:6], kind='DATA', actual=len(x))
        ctx.check('no v2 record is lost', not [r for r in x if r['status'] == 'LOST'], kind='DATA')
    fm = FileMap()
    ctx.check('the witness engine maps against v3 bytes', fm.cur_lines('M', 'CLAUDE.md') is not None, kind='LOGIC')
