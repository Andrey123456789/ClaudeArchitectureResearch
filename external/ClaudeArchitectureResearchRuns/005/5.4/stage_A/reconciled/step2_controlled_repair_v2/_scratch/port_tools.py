"""One-off port of two v1 tools to v2. Each replacement must match exactly once, or the port stops."""
import os
import sys

T = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_tools'))


def sub(s, old, new):
    if s.count(old) != 1:
        sys.exit('no unique match: ' + old[:120])
    return s.replace(old, new)


p = os.path.join(T, 'final_audit.py')
with open(p, encoding='utf-8') as f:
    s = f.read()
s = sub(s, '"""R27 final cold audit from the final bytes. Reads no gate result or checkpoint. Re-runs hooks and checkers on fresh copies. Status words: PASS, FAIL, NOT_RUN, FINDING."""',
        '"""v1 R27 audit, replayed on v2 bytes as a regression inside each gate. Reads no gate result or checkpoint. Re-runs hooks and checkers on fresh copies. Status words: PASS, FAIL, NOT_RUN, FINDING.\nThe separate v2 cold audit is final_audit_v2.py. Adaptations from v1 are listed in _tools/adaptations.py."""')
s = sub(s, "from rcommon import AUD, CANDIDATES, OUT, SCRATCH, baseline, coverage,", "from rcommon import AUD, CANDIDATES, OUT, SCRATCH, all_change_rows, baseline, coverage,")
s = sub(s, "start = read_json(out_path('BASELINE_MANIFEST.json'))['created_at']", "start = read_json(out_path('V2_BASELINE_MANIFEST.json'))['created_at']")
a = s.index("    newer = []\n")
b = s.index("    e = dict(os.environ, GIT_OPTIONAL_LOCKS='0')")
s = s[:a] + '''    newer = []
    for dp, dn, fn in os.walk(ROOT_55):
        # The Codex area is pruned before it is entered: never listed, read or stat-ed.
        dn[:] = [d for d in dn if 'codex_iterative_search' not in d and os.path.abspath(os.path.join(dp, d)) != os.path.abspath(OUT)]
        for x in fn:
            if 'codex_iterative_search' in x:
                continue
            p = os.path.join(dp, x)
            try:
                if os.path.getmtime(p) > t0:
                    newer.append(os.path.relpath(p, ROOT_55))
            except OSError:
                pass
    kit = [n for n in newer if n.replace(os.sep, '/').startswith('_STAGE_A_KIT/')]
    other = [n for n in newer if n not in kit]
    a.check('A', 'no file outside the run root is newer than the run start, apart from kit files', not other, other[:12])
    if kit:
        a.row('A', 'kit files newer than the run start: fence hashes unchanged', 'PASS' if f['n_errors'] == 0 else 'FAIL', kit[:8])
    writers = []
    for dp, dn, fn in os.walk(os.path.join(OUT, '_tools')):
        for x in fn:
            if x.endswith('.py') and x != 'final_audit.py':
                with open(os.path.join(dp, x), encoding='utf-8') as fh:
                    t = fh.read()
                if re.search(r'zipfile|make_archive|tarfile', t):
                    writers.append(x)
    a.check('A', 'no tool of this run writes an archive', not writers, writers)
''' + s[b:]
s = sub(s, """    for r in read_jsonl(out_path('CHANGE_LOG.jsonl')):
        if r.get('kind') == 'TEMPLATE':
            log[(r['candidate'], r['file'])] = r['after_sha256']""", """    for r in all_change_rows():
        if r.get('kind') == 'TEMPLATE':
            log[(r['candidate'], r['file'])] = r['after_sha256']""")
s = sub(s, "write_json('WORKING_COPY_MANIFEST.json', {'version': 'step2-controlled-repair-v1', 'at': now(), 'candidates': man})", "write_json('WORKING_COPY_MANIFEST.json', {'version': 'step2-controlled-repair-v2', 'at': now(), 'candidates': man})")
s = sub(s, "write_jsonl('FINAL_AUDIT_RESULTS.jsonl', a.rows)", "write_jsonl('R27_AUDIT_REPLAY_RESULTS.jsonl', a.rows)")
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

p = os.path.join(T, 'dataset.py')
with open(p, encoding='utf-8') as f:
    s = f.read()
s = sub(s, '''"""R26: builds REPAIRED_CANDIDATE_DERIVED_VIEW deterministically from the frozen baseline.

Order: baseline; R01 overlay; rule overlays (R15, R17, R19, R20) in rule order; accepted R25 corrections in row order; R26 post-edit claim updates; added claims; R21 proposals; derived applicability and delivery fields; current evidence mapping; coverage recomputed.
Frozen baseline files are read only. Replay of the same inputs gives the same bytes.
"""''', '''"""Builds REPAIRED_CANDIDATE_DERIVED_VIEW deterministically from the frozen baseline. Ported from v1 R26.

Order: baseline; R01 overlay; rule overlays (R15, R17, R19, R20) in rule order; accepted R25 corrections in row order; R26 post-edit claim updates; v2 change updates in change order; added claims (v1, then v2, with stated v2 replacements); R21 proposals; derived applicability and delivery fields; current evidence mapping; coverage recomputed.
Frozen baseline files are read only. Replay of the same inputs gives the same bytes. V1_TO_V2_CROSSWALK.jsonl compares the result with v1's view, read by reference.
"""''')
s = sub(s, "from rcommon import CANDIDATES, baseline, coverage, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, sha256_file, utf8_stdout, wc_path, write_json, write_jsonl",
        "from order import V2_ORDER\nfrom rcommon import CANDIDATES, baseline, coverage, input_path, norm_ws, now, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, sha256_file, utf8_stdout, v1_path, wc_path, write_json, write_jsonl")
s = sub(s, '''    u = load_py('R26-DATASET', 'updates.py')
    inactive = {}
    claims = {}
    for key, e in u.UPDATES.items():
        base, _ = split_key(key)
        sets = dict(e['set'])
        if e['sub']:
            sets['subclause_set'] = e['sub']
        if sets:
            step(key, sets, e['rule'])
        else:
            trail.setdefault(base, []).append(e['rule'])
        if e['status'] == 'REMOVED':
            inactive[base] = e
        if e.get('claim') or e.get('append'):
            claims[base] = e
''', '''    u = load_py('R26-DATASET', 'updates.py')
    inactive = {}
    claims = {}
    added = [dict(a) for a in u.ADDED]

    def run_updates(updates):
        for key, e in updates.items():
            base, _ = split_key(key)
            sets = dict(e['set'])
            if e['sub']:
                sets['subclause_set'] = e['sub']
            if sets:
                step(key, sets, e['rule'])
            else:
                trail.setdefault(base, []).append(e['rule'])
            if e['status'] == 'REMOVED':
                inactive[base] = e
            if e.get('claim') or e.get('append'):
                claims[base] = e

    run_updates(u.UPDATES)
    for rule in V2_ORDER:
        if not os.path.exists(out_path('_rules', rule, 'updates.py')):
            continue
        m = load_py(rule, 'updates.py')
        run_updates(getattr(m, 'UPDATES', {}))
        for a in added:
            if a['source_key'] in getattr(m, 'REPLACE_ADDED', {}):
                a.update(m.REPLACE_ADDED[a['source_key']])
                a['rule'] = rule
        added.extend(getattr(m, 'ADDED', []))
''')
s = sub(s, "    for a in u.ADDED:\n        c = a['candidate']", "    for a in added:\n        c = a['candidate']")
s = sub(s, "    man = {'version': 'step2-controlled-repair-v1', 'at': now()", "    man = {'version': 'step2-controlled-repair-v2', 'at': now()")
s = sub(s, "'replay': 'python -B _tools/dataset.py'", "'replay': 'PYTHONPATH=_tools python -B _tools/dataset.py'")
s = sub(s, '''    write_json('REPAIRED_VIEW_MANIFEST.json', man)
    print(json.dumps(man['counts'], ensure_ascii=False)[:2500])
''', '''    write_json('REPAIRED_VIEW_MANIFEST.json', man)
    v1v2 = v1_to_v2(all_rows)
    write_jsonl('V1_TO_V2_CROSSWALK.jsonl', v1v2)
    write_json('DATASET_MANIFEST.json', dict(man, v1_to_v2={'by_status': dict(Counter(r['status'] for r in v1v2)), 'rows': len(v1v2), 'sha256': sha256_file(out_path('V1_TO_V2_CROSSWALK.jsonl'))}, views={'FROZEN_BASELINE_REFERENCE': 'stage_A/reconciled/step2_classification/per_candidate/*: original anchors, untouched', 'V1_REPAIRED_VIEW': 'stage_A/reconciled/step2_controlled_repair_v1/REPAIRED_*.jsonl: anchors on v1 candidate bytes, untouched', 'V2_REPAIRED_VIEW': 'REPAIRED_*.jsonl in this folder: anchors on candidates/<C>/template/ in this folder'}, warning='Line anchors of the three views are not interchangeable. Never mix them in one count.'))
    print(json.dumps(man['counts'], ensure_ascii=False)[:2500])
''')
s = sub(s, '''def main():
    utf8_stdout()
    rows, cross = build()''', '''def v1_to_v2(rows):
    """One row per v2 record: what changed against v1's view. Fields come from the two stored views; nothing is inferred."""
    v1 = {r['source_key']: r for r in read_jsonl(v1_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    out = []
    seen = set()
    for r in rows:
        k = r['source_key']
        seen.add(k)
        o = v1.get(k)
        if o is None:
            out.append({'source_key': k, 'candidate': r['candidate'], 'status': 'ADDED_V2', 'v2_rules': r['repair']['rules'], 'changed_fields': [], 'v1_sha256': None, 'v2_sha256': rec_hash(r)})
            continue
        changed = sorted(f for f in set(o) | set(r) if o.get(f) != r.get(f))
        semantic = [f for f in changed if f not in ('current_evidence_refs', 'repair')]
        repair_rules = o['repair']['rules'] != r['repair']['rules']
        if not changed:
            status = 'UNCHANGED'
        elif o['repair'].get('active') != r['repair'].get('active'):
            status = 'ACTIVE_STATE_CHANGED'
        elif 'claim_text' in semantic:
            status = 'CLAIM_REWORDED'
        elif any(f in semantic for f in ('classification', 'modality', 'canonical_coverage', 'normativity', 'strength_vs_canonical', 'subclauses')):
            status = 'CLASSIFICATION_CHANGED'
        elif semantic:
            status = 'FIELD_CHANGED'
        elif repair_rules:
            status = 'RULE_TRAIL_CHANGED'
        else:
            status = 'ANCHOR_SHIFT_ONLY'
        out.append({'source_key': k, 'candidate': r['candidate'], 'status': status, 'v2_rules': [t for t in r['repair']['rules'] if t not in o['repair']['rules']], 'changed_fields': changed, 'classification_v1': o.get('classification'), 'classification_v2': r.get('classification'), 'modality_v1': o.get('modality'), 'modality_v2': r.get('modality'), 'v1_sha256': rec_hash(o), 'v2_sha256': rec_hash(r)})
    for k, o in v1.items():
        if k not in seen:
            out.append({'source_key': k, 'candidate': o['candidate'], 'status': 'LOST', 'v2_rules': [], 'changed_fields': [], 'v1_sha256': rec_hash(o), 'v2_sha256': None})
    return out


def main():
    utf8_stdout()
    rows, cross = build()''')
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('ported')
