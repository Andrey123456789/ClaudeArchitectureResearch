"""Per-rule gate (contract §2 steps E to H).

python -B gate.py <RULE> [--touched C,C] [--note "text"]

Runs, in order:
  FENCE         immutable trees unchanged
  STATE         working-copy bytes match the running CHANGE_LOG, and untouched files match the frozen inputs
  STRUCTURE     every candidate: its own checkers, node --check on all scripts, JSON parse, import resolution, always-loaded size report
  INVARIANTS    architecture identity for every candidate
  DISPOSITIONS  every changed evidence range has a reviewed disposition with a resolvable new quote
  POLICY        196 rows per touched candidate (all six when none is touched), joined with source reviews
  REVIEWS       every source-review quote of this rule and of all earlier rules resolves in the current bytes
  CUMULATIVE    the regression suite of every rule up to this one, on current bytes, including their mutation tests
A rule gate is PASS only when nothing fails. NOT_RUN rows are carried and reported; they never count as PASS. A failed gate writes no checkpoint.
"""
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import Counter

from fence import verify as fence_verify
from invariants import check_all
from order import ORDER
from rcommon import CANDIDATES, OUT, append_jsonl, input_path, norm_ws, now, out_path, read_json, read_jsonl, read_lines, sha256_file, template_root, utf8_stdout, walk_files, wc_path, write_json, write_jsonl, write_text
from sandbox import cleanup_runs, fresh_copy, run_checkers, run_node
from suitelib import Ctx
from witness import check_dispositions, policy_rows, rel_of


def load_review(rule):
    p = out_path('_rules', rule, 'review.py')
    if not os.path.exists(p):
        return []
    spec = importlib.util.spec_from_file_location('review_' + rule.replace('-', '_'), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows = []
    for r in mod.REVIEW:
        rows.append(dict(r, rule=rule))
    return rows


def rules_upto(rule):
    return ORDER[:ORDER.index(rule) + 1]


def check_state():
    """Current bytes of each file equal the last CHANGE_LOG after-hash, or the frozen input when never touched."""
    last = {}
    for r in read_jsonl(out_path('CHANGE_LOG.jsonl')):
        if r.get('kind') == 'TEMPLATE':
            last[(r['candidate'], r['file'])] = r['after_sha256']
    errors, changed = [], {}
    for c in CANDIDATES:
        for rel in walk_files(template_root(c)):
            cur = sha256_file(wc_path(c, rel))
            want = last.get((c, rel)) or sha256_file(input_path(c, rel))
            if cur != want:
                errors.append('%s %s differs from its logged state' % (c, rel))
            if cur != sha256_file(input_path(c, rel)):
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
                    json.load(open(os.path.join(root, rel), encoding='utf-8'))
                except ValueError as e:
                    errors.append('%s bad JSON %s: %s' % (c, rel, e))
        seen, missing = imports_of(c)
        if missing:
            errors.append('%s unresolved imports: %s' % (c, missing))
        chars = sum(len(' '.join(read_lines(wc_path(c, r)))) for r in seen if os.path.exists(wc_path(c, r)))
        rows.append({'candidate': c, 'checker': 'always-loaded chars (CLAUDE.md plus imports)', 'exit': 0, 'tail': [chars]})
    return rows, errors


def review_quotes(rows):
    errs = []
    for r in rows:
        if r.get('superseded'):
            continue
        for rel, quote in r.get('quotes') or []:
            c = r['candidate']
            p = wc_path(c, rel)
            if not os.path.exists(p) or norm_ws(quote).lower() not in norm_ws(' '.join(read_lines(p))).lower():
                errs.append('%s %s %s: quote not in current %s: %s' % (r['rule'], r['policy'], c, rel, quote[:110]))
    return errs


def run_suites(rule):
    rows = []
    for r in rules_upto(rule):
        p = os.path.join(OUT, '_tools', 'suites', r.replace('-', '_') + '.py')
        if not os.path.exists(p):
            continue
        spec = importlib.util.spec_from_file_location('suite_' + r.replace('-', '_'), p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ctx = Ctx(r)
        try:
            mod.run(ctx)
        except Exception as e:  # a crashed suite is a failed suite
            ctx.add('suite crashed', 'FAIL', repr(e))
        rows.extend(ctx.rows)
    return rows


def main():
    utf8_stdout()
    rule = sys.argv[1]
    args = sys.argv[2:]
    touched = None
    note = ''
    if '--touched' in args:
        touched = args[args.index('--touched') + 1].split(',')
    if '--note' in args:
        note = args[args.index('--note') + 1]
    i = ORDER.index(rule)
    for r in ORDER[:i]:
        cp = out_path('CHECKPOINTS', r + '.checkpoint.json')
        if not os.path.exists(cp) or read_json(cp).get('gate') not in ('PASS', 'PASS_WITH_NOT_RUN'):
            raise SystemExit('refused: earlier rule %s has no PASS checkpoint' % r)
    steps = {}
    fence = fence_verify()
    steps['FENCE'] = {'status': 'PASS' if fence['n_errors'] == 0 else 'FAIL', 'detail': fence}
    state_errs, changed = check_state()
    steps['STATE'] = {'status': 'PASS' if not state_errs else 'FAIL', 'errors': state_errs, 'changed_files': {c: len(v) for c, v in changed.items()}}
    srows, serrs = structure()
    steps['STRUCTURE'] = {'status': 'PASS' if not serrs else 'FAIL', 'rows': srows, 'errors': serrs}
    inv = check_all()
    steps['INVARIANTS'] = {'status': 'PASS' if not any(inv.values()) else 'FAIL', 'errors': {c: v for c, v in inv.items() if v}}
    derrs, ranges = check_dispositions()
    steps['DISPOSITIONS'] = {'status': 'PASS' if not derrs else 'FAIL', 'errors': derrs[:60], 'n_changed_ranges': len(ranges), 'n_errors': len(derrs)}
    all_reviews = []
    for r in rules_upto(rule):
        all_reviews.extend(load_review(r))
    by = {}
    for x in all_reviews:
        by.setdefault((x['policy'], x['candidate']), []).append(x)
    pcands = touched or CANDIDATES
    pfails, pcount = [], Counter()
    os.makedirs(out_path('POLICY_CHECKS', rule), exist_ok=True)
    for c in pcands:
        prows = policy_rows(c, by, rule)
        write_jsonl(os.path.join('POLICY_CHECKS', rule, c + '.jsonl'), prows)
        for p in prows:
            pcount[(c, p['check_level'])] += 1
            if p['status'] != 'PASS':
                pfails.append('%s %s: %s' % (c, p['policy'], p['fails']))
    if any(len(read_jsonl(out_path('POLICY_CHECKS', rule, c + '.jsonl'))) != 196 for c in pcands):
        pfails.append('policy row count is not 196')
    steps['POLICY'] = {'status': 'PASS' if not pfails else 'FAIL', 'candidates': pcands, 'n_rows': 196 * len(pcands), 'levels': {'%s/%s' % k: v for k, v in pcount.items()}, 'errors': pfails[:60]}
    qerrs = review_quotes(all_reviews)
    steps['REVIEWS'] = {'status': 'PASS' if not qerrs else 'FAIL', 'n_review_rows': len(all_reviews), 'errors': qerrs[:60]}
    write_jsonl(os.path.join('POLICY_CHECKS', rule, 'SOURCE_REVIEWS.jsonl'), [x for x in all_reviews if x['rule'] == rule])
    suite = run_suites(rule)
    write_jsonl(os.path.join('TEST_RESULTS', rule + '.jsonl'), suite)
    tally = Counter(x['status'] for x in suite)
    fails = [x for x in suite if x['status'] == 'FAIL']
    steps['CUMULATIVE'] = {'status': 'PASS' if not fails else 'FAIL', 'tally': dict(tally), 'by_suite': {r: dict(Counter(x['status'] for x in suite if x['suite'] == r)) for r in rules_upto(rule) if any(x['suite'] == r for x in suite)},
                           'failures': [{k: x[k] for k in ('suite', 'test', 'candidate', 'detail')} for x in fails[:40]], 'not_run': [{k: x[k] for k in ('suite', 'test', 'candidate', 'detail')} for x in suite if x['status'] == 'NOT_RUN'][:60]}
    ok = all(s['status'] == 'PASS' for s in steps.values())
    has_not_run = tally.get('NOT_RUN', 0) > 0
    gate = ('PASS_WITH_NOT_RUN' if has_not_run else 'PASS') if ok else 'FAIL'
    hashes = {c: {rel: sha256_file(wc_path(c, rel)) for rel in changed.get(c, [])} for c in CANDIDATES}
    row = {'at': now(), 'rule': rule, 'gate': gate, 'note': note, 'steps': steps, 'tools_sha256': {os.path.basename(p): sha256_file(p) for p in glob.glob(os.path.join(OUT, '_tools', '*.py'))}, 'changed_file_hashes': hashes,
           'command': 'python -B _tools/gate.py ' + ' '.join(sys.argv[1:])}
    append_jsonl('GATE_LOG.jsonl', row)
    if ok:
        write_json(os.path.join('CHECKPOINTS', rule + '.checkpoint.json'), {'rule': rule, 'gate': gate, 'at': row['at'], 'changed_file_hashes': hashes, 'test_tally': dict(tally), 'n_policy_rows': 196 * len(pcands)})
    next_rule = ORDER[i + 1] if ok and i + 1 < len(ORDER) else (rule if not ok else None)
    write_json('STATUS.json', {'version': 'step2-controlled-repair-v1', 'at': row['at'], 'phase': 'RULE_GATES', 'rule': rule, 'rule_index': i + 1, 'n_rules': len(ORDER), 'gate': gate, 'status': 'PASS' if ok else 'FAIL',
                               'resume_point': next_rule, 'resume': 'See RESUME.md. Trust CHECKPOINTS/ and GATE_LOG.jsonl, not chat.', 'source_hashes': 'BASELINE_MANIFEST.json, WORKING_COPY_MANIFEST.json, FENCE_SNAPSHOT.json'})
    cleanup_runs()
    print(json.dumps({'gate': gate, 'steps': {k: v['status'] for k, v in steps.items()}, 'tally': dict(tally), 'next': next_rule}, ensure_ascii=False))
    for k, v in steps.items():
        if v['status'] != 'PASS':
            print('---', k, json.dumps({x: v[x] for x in v if x in ('errors', 'failures', 'detail')}, ensure_ascii=False)[:6000])
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
