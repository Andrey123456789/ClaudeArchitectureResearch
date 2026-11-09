"""Per-change gate for v2 (contract section 2, steps D to H).

python -B gate.py <CHANGE> [--note "text"]

Runs, in order, always on all six candidates:
  FENCE         immutable trees unchanged (v1, inputs, Step 2, audit, kit)
  TOOL_INTEGRITY each v1 tool and suite is byte-identical to v1 or has a stated reason in adaptations.py
  STATE        every working-copy file equals its last logged hash across both history levels, or the frozen input when never touched
  STRUCTURE     each candidate's own checkers, node --check on all scripts, JSON parse, import resolution, always-loaded size report
  INVARIANTS    architecture identity for every candidate, against the frozen baseline
  DISPOSITIONS  every changed evidence range has a reviewed disposition with a resolvable new quote
  DATASET       dispositions, derived view, coverage and graph rebuilt from the frozen baseline; whole-view invariants; replay equality
  POLICY        196 rows per candidate, 1,176 in all, joined with source reviews
  REVIEWS       every source-review quote of this and all earlier changes resolves in the current bytes, unless a change superseded it with a stated reason
  CUMULATIVE    all 27 v1 regression suites plus every v2 suite up to this change, on current bytes, including their mutation tests

A change is PASS only when nothing fails. NOT_RUN rows are carried and reported; they never count as PASS. A failed gate writes no checkpoint.
v1's 27 checkpoints stay in v1; CHECKPOINTS/ here holds v2 changes only.
"""
import glob
import importlib.util
import json
import os
import re
import sys
import time
from collections import Counter

import dataset
import depgraph
import disposition
import viewcheck
from fence import verify as fence_verify
from invariants import check_all
from order import ALL, ORDER, V2_ORDER
from rcommon import CANDIDATES, OUT, all_change_rows, append_jsonl, input_path, norm_ws, now, out_path, read_json, read_jsonl, read_lines, sha256_file, template_root, utf8_stdout, walk_files, wc_path, write_json, write_jsonl, write_text
from sandbox import cleanup_runs, fresh_copy, run_checkers, run_node
from suitelib import Ctx
from witness import check_dispositions, policy_rows


def load_review(rule):
    p = out_path('_rules', rule, 'review.py')
    if not os.path.exists(p):
        return []
    spec = importlib.util.spec_from_file_location('review_' + rule.replace('-', '_'), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [dict(r, rule=rule) for r in mod.REVIEW]


def superseded_quotes():
    """(rule, policy, candidate, quote) rows a later change retired on purpose. Each row names who retired it and why."""
    out = {}
    for rule in V2_ORDER:
        p = out_path('_rules', rule, 'supersede.py')
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location('sup_' + rule.replace('-', '_'), p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for r in mod.SUPERSEDE:
                out[(r['rule'], r['policy'], r['candidate'], norm_ws(r['quote']).lower())] = dict(r, by=rule)
    return out


def rules_upto(rule):
    return ORDER + V2_ORDER[:V2_ORDER.index(rule) + 1]


def check_state():
    """Current bytes of each file equal the last logged after-hash across v1 and v2, or the frozen input when never touched."""
    last = {}
    for r in all_change_rows():
        if r.get('kind') == 'TEMPLATE':
            last[(r['candidate'], r['file'])] = r['after_sha256']
    errors, changed = [], {}
    for c in CANDIDATES:
        for rel in walk_files(template_root(c)):
            cur = sha256_file(wc_path(c, rel))
            base = sha256_file(input_path(c, rel)) if os.path.exists(input_path(c, rel)) else None
            want = last.get((c, rel)) or base
            if cur != want:
                errors.append('%s %s differs from its logged state' % (c, rel))
            if cur != base:
                changed.setdefault(c, []).append(rel)
    return errors, changed


def imports_of(c):
    root = template_root(c)
    seen, stack, missing = set(), ['CLAUDE.md'], []
    while stack:
        rel = stack.pop()
        if rel in seen:
            continue
        seen.add(rel)
        p = os.path.join(root, rel.replace('/', os.sep))
        if not os.path.exists(p):
            missing.append(rel)
            continue
        for line in read_lines(p):
            m = re.match(r'^@(\S+)\s*$', line.strip())
            if m:
                stack.append(m.group(1)[2:] if m.group(1).startswith('./') else m.group(1))
    return seen, missing


def structure():
    rows, errors = [], []
    for c in CANDIDATES:
        root = fresh_copy(c, 'struct')
        for r in run_checkers(c, root):
            bad = r['exit'] != 0
            rows.append({k: r[k] for k in ('candidate', 'checker', 'exit', 'tail')})
            if bad:
                errors.append('%s %s exit %s: %s' % (c, r['checker'], r['exit'], r['full'][-600:]))
        for rel in walk_files(root):
            if rel.endswith(('.js', '.mjs', '.cjs')):
                code, out, err = run_node(root, ['--check', rel])
                if code != 0:
                    errors.append('%s node --check %s: %s' % (c, rel, err[-300:]))
            if rel.endswith('.json'):
                try:
                    with open(os.path.join(root, rel), encoding='utf-8') as f:
                        json.load(f)
                except ValueError as e:
                    errors.append('%s bad JSON %s: %s' % (c, rel, e))
        seen, missing = imports_of(c)
        if missing:
            errors.append('%s unresolved imports: %s' % (c, missing))
        chars = sum(len(' '.join(read_lines(wc_path(c, r)))) for r in seen if os.path.exists(wc_path(c, r)))
        rows.append({'candidate': c, 'checker': 'always-loaded chars (CLAUDE.md plus imports)', 'exit': 0, 'tail': [chars]})
    return rows, errors


def review_quotes(rows, sup):
    errs, retired = [], []
    for r in rows:
        if r.get('superseded'):
            continue
        for rel, quote in r.get('quotes') or []:
            c = r['candidate']
            p = wc_path(c, rel)
            if not os.path.exists(p) or norm_ws(quote).lower() not in norm_ws(' '.join(read_lines(p))).lower():
                k = (r['rule'], r['policy'], c, norm_ws(quote).lower())
                if k in sup:
                    retired.append({'rule': r['rule'], 'policy': r['policy'], 'candidate': c, 'quote': quote[:120], 'by': sup[k]['by'], 'why': sup[k]['why']})
                else:
                    errs.append('%s %s %s: quote not in current %s: %s' % (r['rule'], r['policy'], c, rel, quote[:110]))
    return errs, retired


def run_suites(rule):
    rows = []
    timing = {}
    for r in rules_upto(rule):
        p = os.path.join(OUT, '_tools', 'suites', r.replace('-', '_') + '.py')
        if not os.path.exists(p):
            continue
        spec = importlib.util.spec_from_file_location('suite_' + r.replace('-', '_'), p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ctx = Ctx(r)
        t0 = time.time()
        try:
            mod.run(ctx)
        except Exception as e:  # a crashed suite is a failed suite
            ctx.add('suite crashed', 'FAIL', repr(e))
        timing[r] = round(time.time() - t0, 1)
        rows.extend(ctx.rows)
    return rows, timing


def tool_integrity():
    """Each v1 tool and regression suite is byte-identical to v1, or has a stated reason in adaptations.py."""
    from adaptations import ADAPTATIONS
    v1 = read_json(out_path('V2_BASELINE_MANIFEST.json'))['v1_tools_sha256']
    listed = {a['file']: a for a in ADAPTATIONS}
    errs, identical, differ = [], 0, []
    for rel, h in v1.items():
        p = out_path('_tools', *rel.split('/'))
        same = os.path.exists(p) and sha256_file(p) == h
        identical += same
        if same:
            continue
        differ.append(rel)
        if rel not in listed:
            errs.append('%s differs from v1 with no stated reason' % rel)
        elif not os.path.exists(p) and listed[rel]['kind'] != 'REMOVED':
            errs.append('%s is missing but not marked REMOVED' % rel)
    for a in ADAPTATIONS:
        if a['kind'] == 'TEST_UPDATED' and not (a.get('negative') and a.get('why')):
            errs.append('%s: an updated test needs a reason and a negative test' % a['file'])
    return errs, {'v1_files': len(v1), 'identical': identical, 'differ': differ}


def dataset_step():
    """Rebuilds everything derived and checks it. dataset.main writes the view; a second build must equal the files."""
    disposition.build()
    dataset.main()
    depgraph.main()
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    cross = read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    errs = viewcheck.check_all(rows, cross, cov)
    moved = [x for x in cov if x['status_changed'] or x['strength_status_changed']]
    return errs, {'rows': len(rows), 'active': sum(1 for r in rows if r['repair']['active']), 'coverage_cells': len(cov), 'moved_cells': ['%s %s' % (x['candidate'], x['policy_id']) for x in moved]}


def main():
    utf8_stdout()
    rule = sys.argv[1]
    args = sys.argv[2:]
    note = args[args.index('--note') + 1] if '--note' in args else ''
    i = V2_ORDER.index(rule)
    for r in V2_ORDER[:i]:
        cp = out_path('CHECKPOINTS', r + '.checkpoint.json')
        if not os.path.exists(cp) or read_json(cp).get('gate') not in ('PASS', 'PASS_WITH_NOT_RUN', 'PASS_WITH_DOCUMENTED_NOT_RUN'):
            raise SystemExit('refused: earlier change %s has no PASS checkpoint' % r)
    t0 = time.time()
    steps = {}
    fence = fence_verify()
    steps['FENCE'] = {'status': 'PASS' if fence['n_errors'] == 0 else 'FAIL', 'detail': fence}
    terrs, tfacts = tool_integrity()
    steps['TOOL_INTEGRITY'] = {'status': 'PASS' if not terrs else 'FAIL', 'errors': terrs, 'facts': tfacts}
    state_errs, changed = check_state()
    steps['STATE'] = {'status': 'PASS' if not state_errs else 'FAIL', 'errors': state_errs, 'changed_files_vs_frozen': {c: len(v) for c, v in changed.items()}}
    srows, serrs = structure()
    steps['STRUCTURE'] = {'status': 'PASS' if not serrs else 'FAIL', 'rows': srows, 'errors': serrs}
    inv = check_all()
    steps['INVARIANTS'] = {'status': 'PASS' if not any(inv.values()) else 'FAIL', 'errors': {c: v for c, v in inv.items() if v}}
    disposition.build()
    derrs, ranges = check_dispositions()
    steps['DISPOSITIONS'] = {'status': 'PASS' if not derrs else 'FAIL', 'errors': derrs[:60], 'n_changed_ranges': len(ranges), 'n_errors': len(derrs)}
    derr, dfacts = dataset_step()
    steps['DATASET'] = {'status': 'PASS' if not derr else 'FAIL', 'errors': derr[:60], 'facts': dfacts}
    all_reviews = []
    for r in rules_upto(rule):
        all_reviews.extend(load_review(r))
    by = {}
    for x in all_reviews:
        by.setdefault((x['policy'], x['candidate']), []).append(x)
    pfails, pcount = [], Counter()
    os.makedirs(out_path('POLICY_CHECKS', rule), exist_ok=True)
    for c in CANDIDATES:
        prows = policy_rows(c, by, rule)
        write_jsonl(os.path.join('POLICY_CHECKS', rule, c + '.jsonl'), prows)
        for p in prows:
            pcount[(c, p['check_level'])] += 1
            if p['status'] != 'PASS':
                pfails.append('%s %s: %s' % (c, p['policy'], p['fails']))
    if any(len(read_jsonl(out_path('POLICY_CHECKS', rule, c + '.jsonl'))) != 196 for c in CANDIDATES):
        pfails.append('policy row count is not 196')
    steps['POLICY'] = {'status': 'PASS' if not pfails else 'FAIL', 'candidates': CANDIDATES, 'n_rows': 196 * len(CANDIDATES), 'levels': {'%s/%s' % k: v for k, v in pcount.items()}, 'errors': pfails[:60]}
    qerrs, retired = review_quotes(all_reviews, superseded_quotes())
    steps['REVIEWS'] = {'status': 'PASS' if not qerrs else 'FAIL', 'n_review_rows': len(all_reviews), 'errors': qerrs[:60], 'retired_on_purpose': retired}
    write_jsonl(os.path.join('POLICY_CHECKS', rule, 'SOURCE_REVIEWS.jsonl'), [x for x in all_reviews if x['rule'] == rule])
    suite, timing = run_suites(rule)
    write_jsonl(os.path.join('TEST_RESULTS', rule + '.jsonl'), suite)
    tally = Counter(x['status'] for x in suite)
    fails = [x for x in suite if x['status'] == 'FAIL']
    steps['CUMULATIVE'] = {'status': 'PASS' if not fails else 'FAIL', 'tally': dict(tally), 'by_suite': {r: dict(Counter(x['status'] for x in suite if x['suite'] == r)) for r in rules_upto(rule) if any(x['suite'] == r for x in suite)}, 'seconds_by_suite': timing,
                           'failures': [{k: x[k] for k in ('suite', 'test', 'candidate', 'detail')} for x in fails[:40]], 'not_run': [{k: x[k] for k in ('suite', 'test', 'candidate', 'detail')} for x in suite if x['status'] == 'NOT_RUN'][:60]}
    ok = all(s['status'] == 'PASS' for s in steps.values())
    has_not_run = tally.get('NOT_RUN', 0) > 0
    gate = ('PASS_WITH_DOCUMENTED_NOT_RUN' if has_not_run else 'PASS') if ok else 'FAIL'
    hashes = {c: {rel: sha256_file(wc_path(c, rel)) for rel in changed.get(c, [])} for c in CANDIDATES}
    v2_changed = {}
    base = read_json(out_path('V2_BASELINE_MANIFEST.json'))['candidates']
    for c in CANDIDATES:
        v2_changed[c] = [rel for rel in walk_files(template_root(c)) if sha256_file(wc_path(c, rel)) != base[c]['files'].get(rel)]
    row = {'at': now(), 'rule': rule, 'gate': gate, 'note': note, 'seconds': round(time.time() - t0), 'steps': steps, 'tools_sha256': {os.path.basename(p): sha256_file(p) for p in glob.glob(os.path.join(OUT, '_tools', '*.py'))}, 'suites_sha256': {os.path.basename(p): sha256_file(p) for p in glob.glob(os.path.join(OUT, '_tools', 'suites', '*.py'))},
           'changed_files_vs_v1': v2_changed, 'changed_file_hashes_vs_frozen': hashes, 'command': 'python -B _tools/gate.py ' + ' '.join(sys.argv[1:])}
    append_jsonl('GATE_LOG.jsonl', row)
    if ok:
        write_json(os.path.join('CHECKPOINTS', rule + '.checkpoint.json'), {'change': rule, 'gate': gate, 'at': row['at'], 'changed_files_vs_v1': v2_changed, 'candidate_hashes_vs_v1': {c: {rel: sha256_file(wc_path(c, rel)) for rel in v2_changed[c]} for c in CANDIDATES}, 'test_tally': dict(tally), 'n_policy_rows': 196 * len(CANDIDATES), 'dataset': dfacts, 'view_sha256': {n: sha256_file(out_path(n)) for n in ('REPAIRED_CLASSIFICATIONS.jsonl', 'REPAIRED_POLICY_COVERAGE.jsonl', 'ORIGINAL_TO_REPAIRED_CLAIMS.jsonl')}})
    next_change = V2_ORDER[i + 1] if ok and i + 1 < len(V2_ORDER) else (rule if not ok else None)
    write_json('STATUS.json', {'version': 'step2-controlled-repair-v2', 'at': row['at'], 'phase': 'CHANGE_GATES', 'change': rule, 'change_index': i + 1, 'n_declared_changes': len(V2_ORDER), 'gate': gate, 'status': 'PASS' if ok else 'FAIL',
                               'resume_point': next_change or 'next change per RESUME.md', 'resume': 'See RESUME.md. Trust CHECKPOINTS/ and GATE_LOG.jsonl, not chat.', 'step3_started': False})
    cleanup_runs()
    print(json.dumps({'gate': gate, 'seconds': row['seconds'], 'steps': {k: v['status'] for k, v in steps.items()}, 'tally': dict(tally), 'not_run': tally.get('NOT_RUN', 0), 'next': next_change, 'timing': timing}, ensure_ascii=False))
    for k, v in steps.items():
        if v['status'] != 'PASS':
            print('---', k, json.dumps({x: v[x] for x in v if x in ('errors', 'failures', 'detail')}, ensure_ascii=False)[:7000])
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
