"""Metric-impact crosswalk v2 -> v3. Three layers that must not be mixed: data labels (classification records), policy cells (1,176
coverage and strength statuses), and template behavior (what checkers and hooks do, by direct script runs). Live-host behavior is NOT_RUN.
The v2 results stay as reported in v2; this file states only what moved and why.

Writes V3_METRIC_CROSSWALK.json and V3_METRIC_IMPACT.md. Run after the last gate and the cold audit:
PYTHONPATH=_tools python -B _tools/v3_metrics.py
"""
import json
from collections import Counter

from order import V3_ORDER
from rcommon import CANDIDATES, out_path, read_json, read_jsonl, utf8_stdout, v2_path, write_json, write_text

# Template behavior changes per v3 change, as declared and as measured by each change's own suite (pre on old bytes, post on new).
BEHAVIOR = [
    ('PV2-02-FAILCLOSED-INPUT', 'M, M1', 'stricter', 'Malformed, empty or non-object shell PreToolUse input, and a missing, blank or non-string command, are refused in the script (M: exit 2; M1: deny). Before, M exited 1 on malformed input and M and M1 allowed a missing command.'),
    ('PV2-01-GIT-GATING', 'M, M1, L0, L1, K1', 'stricter', 'Repository-changing Git commands return ask (K0 table, byte-identical block); read-only Git still runs without a prompt; an existing non-Git deny still wins. Before, only K0 asked.'),
    ('PV2-03-K0-CPM-ROOT', 'K0', 'false positive removed', 'A nested Directory.Packages.props managing every project no longer errors (root-only mandate removed); per-project effective CPM still proven by MSBuild.'),
    ('PV2-04-M-FRONTEND-TESTS', 'M', 'stricter (text)', 'M project-structure step 7 bans frontend tests under backend/ (record V3A-M-030, MUST_NOT). No candidate enforces it by a checker.'),
    ('V3-D01-PASS23-OVERLAY', 'all six (data only)', 'none', 'Data overlay from Codex Pass 2/3 adjudication: 18 added scan-prompt records and 14 facet rewordings. No template byte changed.'),
    ('V3-D02-MODALITY86', 'M (data only)', 'none', 'One stored modality corrected (FG-M-8b2c02178e DEFAULT -> MUST_NOT). No template byte changed.'),
    ('PV2-03B-CPM-IMPORT-PROVEN', 'K0, M', 'false positive removed', 'A central file MSBuild imports from outside the project ancestors (DirectoryPackagesPropsPath) is accepted when MSBuild proves CPM on and the file imported; before, K0 errored and M errored and its hook blocked the edit. Without the SDK the static error stays (Q-11).'),
    ('V3-Q10-PACKAGEVERSION-VERSION', 'M1, K0, M', 'stricter (M1, K0); false positive removed (M)', 'A PackageVersion with no version errors in M1 and K0 (before: accepted); K0 reads a Version child element (empty or floating child versions now error); M accepts a valid Version child element (before: error).'),
]


def counts(rows, field):
    out = {}
    for c in CANDIDATES:
        out[c] = dict(Counter(r.get(field) for r in rows if r['candidate'] == c and (r.get('repair') or {}).get('active', True)))
    return out


def delta(a, b):
    out = {}
    for c in CANDIDATES:
        keys = set(a[c]) | set(b[c])
        d = {k: b[c].get(k, 0) - a[c].get(k, 0) for k in keys if b[c].get(k, 0) != a[c].get(k, 0)}
        if d:
            out[c] = d
    return out


def suite_counts(rule):
    res = {}
    for label in ('pre', 'post'):
        p = out_path('_rules', rule, 'suite_%s.jsonl' % label)
        try:
            res[label] = dict(Counter(r['status'] for r in read_jsonl(p)))
        except FileNotFoundError:
            res[label] = None
    return res


def main():
    utf8_stdout()
    v2 = read_jsonl(v2_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    v3 = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    m = {'semantics': 'Three layers, never mixed: data labels, policy cells, template behavior. Live host NOT_RUN. v2 results are not overwritten.'}
    lab2, lab3 = counts(v2, 'classification'), counts(v3, 'classification')
    mod2, mod3 = counts(v2, 'modality'), counts(v3, 'modality')
    m['data_labels'] = {
        'rows': {'v2': len(v2), 'v3': len(v3)},
        'active_rows': {'v2': sum(1 for r in v2 if (r.get('repair') or {}).get('active', True)), 'v3': sum(1 for r in v3 if (r.get('repair') or {}).get('active', True))},
        'rows_by_candidate': {c: {'v2': sum(1 for r in v2 if r['candidate'] == c), 'v3': sum(1 for r in v3 if r['candidate'] == c)} for c in CANDIDATES},
        'classification_delta': delta(lab2, lab3), 'modality_delta': delta(mod2, mod3)}
    x = read_jsonl(out_path('V2_TO_V3_CROSSWALK.jsonl'))
    m['data_labels']['crosswalk_status'] = dict(Counter(r['status'] for r in x))
    by_rule = Counter()
    for r in x:
        for rule in r.get('v3_rules') or []:
            by_rule[(rule, r['status'])] += 1
    m['data_labels']['crosswalk_by_rule'] = {'%s/%s' % k: v for k, v in sorted(by_rule.items())}
    m['data_labels']['classification_changed'] = [{'key': r['source_key'], 'candidate': r['candidate'], 'v2': [r['classification_v2'], r['modality_v2']], 'v3': [r['classification_v3'], r['modality_v3']], 'rules': r['v3_rules']} for r in x if r['status'] != 'ADDED_V3' and (r['status'] == 'CLASSIFICATION_CHANGED' or r.get('modality_v2') != r.get('modality_v3'))]
    c2 = {(r['candidate'], r['policy_id']): r for r in read_jsonl(v2_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    c3 = {(r['candidate'], r['policy_id']): r for r in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    moved = sorted('%s/%s' % k for k in c2 if (c2[k]['computed_status'], c2[k]['strength_status']) != (c3[k]['computed_status'], c3[k]['strength_status']))
    links = sorted('%s/%s' % k for k in c2 if (set(c2[k]['direct_source_keys']), set(c2[k]['partial_source_keys'])) != (set(c3[k]['direct_source_keys']), set(c3[k]['partial_source_keys'])))
    m['policy_cells'] = {'n': {'v2': len(c2), 'v3': len(c3)}, 'computed_status_v3': dict(Counter(r['computed_status'] for r in c3.values())), 'strength_status_v3': dict(Counter(r['strength_status'] for r in c3.values())),
                         'strength_status_v2': dict(Counter(r['strength_status'] for r in c2.values())), 'cells_status_or_strength_moved': moved, 'cells_with_changed_witness_links': links}
    m['template_behavior'] = [{'change': rule, 'candidates': cands, 'direction': d, 'what': what, 'own_suite': suite_counts(rule)} for rule, cands, d, what in BEHAVIOR]
    man = read_json(out_path('V3_FINAL_MANIFEST.json'))['candidates']
    m['template_files_changed_vs_v2'] = {c: man[c]['n_changed_vs_v2'] for c in CANDIDATES}
    m['live_host'] = 'NOT_RUN: ask display and answer, deny, exit 2, onFailure, headless behavior, a live agent task, real application, registry, CI.'
    write_json('V3_METRIC_CROSSWALK.json', m)
    t = ['# Metric impact, v2 to v3\n',
         'Three layers, never mixed: data labels (classification records), policy cells (1,176 coverage and strength statuses) and template behavior (checker and hook outcomes from direct script runs). Live-host behavior is NOT_RUN. v2 results stay as reported in v2. Machine-readable: `V3_METRIC_CROSSWALK.json`.\n',
         '## 1. Data labels\n',
         'Rows: %d in v2, %d in v3; active: %d in v2, %d in v3.\n' % (len(v2), len(v3), m['data_labels']['active_rows']['v2'], m['data_labels']['active_rows']['v3']),
         '| Candidate | Rows v2 | Rows v3 | Classification change | Modality change |', '|---|---:|---:|---|---|']
    for c in CANDIDATES:
        t.append('| %s | %d | %d | %s | %s |' % (c, m['data_labels']['rows_by_candidate'][c]['v2'], m['data_labels']['rows_by_candidate'][c]['v3'], ', '.join('%s %+d' % kv for kv in sorted(m['data_labels']['classification_delta'].get(c, {}).items())) or 'none', ', '.join('%s %+d' % kv for kv in sorted(m['data_labels']['modality_delta'].get(c, {}).items())) or 'none'))
    t += ['', 'Crosswalk statuses (`V2_TO_V3_CROSSWALK.jsonl`): ' + ', '.join('%s %d' % kv for kv in sorted(m['data_labels']['crosswalk_status'].items())) + '.', '',
          'By change: ' + '; '.join('%s %d' % kv for kv in m['data_labels']['crosswalk_by_rule'].items()) + '.', '',
          'Classification or modality changed on an existing record: ' + ('; '.join('%s (%s) %s -> %s by %s' % (r['key'], r['candidate'], '/'.join(r['v2']), '/'.join(r['v3']), ', '.join(r['rules'])) for r in m['data_labels']['classification_changed']) or 'none') + '. Added records carry their own labels (ADDED_V3).', '',
          'Raw label or modality counts are not a strictness metric: the "do not" records were not reviewed (Q-06), and the counts depend on extraction granularity (Codex Pass 2/3 showed uneven scan-prompt extraction).', '',
          '## 2. Policy cells (1,176)\n',
          'Cells whose coverage status or strength status moved against v2: **%d**. Cells whose witness links changed (more or other source records, same statuses): %d (%s).' % (len(moved), len(links), ', '.join(links) or 'none'), '',
          'Strength statuses in v3: ' + ', '.join('%s %d' % kv for kv in sorted(m['policy_cells']['strength_status_v3'].items())) + '. Same labels do not prove semantic parity: see `POLICY_PARITY_MATRIX.jsonl` check levels.', '',
          '## 3. Template behavior\n',
          '| Change | Candidates | Direction | What changed | Own suite pre (old bytes) | Own suite post (new bytes) |', '|---|---|---|---|---|---|']
    for b in m['template_behavior']:
        s = b['own_suite']
        fmt = lambda d: 'n/a' if not d else ', '.join('%s %d' % kv for kv in sorted(d.items()))
        t.append('| %s | %s | %s | %s | %s | %s |' % (b['change'], b['candidates'], b['direction'], b['what'], fmt(s['pre']), fmt(s['post'])))
    t += ['', 'Template files changed against v2: ' + ', '.join('%s %d' % (c, n) for c, n in m['template_files_changed_vs_v2'].items()) + ' (total %d).' % sum(m['template_files_changed_vs_v2'].values()), '',
          'Enforcement metrics that compare candidates must use the v3 behavior above, not v2: Git gating (ask) now exists in all six hooks; invalid shell PreToolUse input (malformed, empty, array, no command, non-string command) is refused in the script by all six (cold audit section E), while a blank command and event/tool mismatches still differ (Q-02, Q-03); central-package checks agree in all six with the .NET SDK and differ without it (Q-11).', '',
          '## 4. Live behavior\n', m['live_host'], '']
    write_text('V3_METRIC_IMPACT.md', '\n'.join(t))
    print({'moved': len(moved), 'links_changed': len(links), 'crosswalk': m['data_labels']['crosswalk_status']})


if __name__ == '__main__':
    main()
