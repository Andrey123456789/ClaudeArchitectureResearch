"""Builds the Part A deliverables from the workbench and the written decisions. Deterministic; re-runnable.

PYTHONPATH=_tools python -B _tools/adj_build.py

Writes PASS2_PASS3_ADJUDICATION.jsonl (one row per effective Codex record), UNIQUE_ISSUE_CLUSTERS.jsonl (one row per semantic cluster),
ADJUDICATION_COUNTS.json, and ADJUDICATION_CHECKPOINTS/<cluster>.json (hash of the decision input and the rows, so a resumed session
can prove a batch is final). Fails if any record lacks a decision, a cluster, or a resolvable target.
"""
import importlib.util
import json
import os
import sys
from collections import Counter, defaultdict

from rcommon import CANDIDATES, OUT, now, out_path, read_jsonl, rec_hash, sha256_file, utf8_stdout, v2_path, write_json, write_jsonl

DEFAULT_ACTION = {'NON_NORMATIVE': 'NONE', 'ALREADY_COVERED': 'NONE'}
KIT_CATEGORY = {'CANDIDATE_UNREPRESENTED_DUTY': '(c) new to this candidate records; not a study-level new obligation', 'FACET_OF_EXISTING': '(d) facet or correction of an existing obligation', 'ALREADY_COVERED': '(e) already covered',
                'NON_NORMATIVE': '(f) non-normative example, technique or implementation fact', 'OPEN_HYPOTHESIS': '(g) unverified hypothesis'}


def load_decisions():
    spec = importlib.util.spec_from_file_location('decisions', out_path('_adjudication', 'decisions.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    utf8_stdout()
    dec = load_decisions()
    wb = read_jsonl(out_path('_adjudication', 'WORKBENCH.jsonl'))
    v2keys = {}
    for r in read_jsonl(v2_path('REPAIRED_CLASSIFICATIONS.jsonl')):
        v2keys[r['source_key']] = r
    spec = importlib.util.spec_from_file_location('d01', out_path('_rules', 'V3-D01-PASS23-OVERLAY', 'updates.py'))
    d01 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d01)
    d01_added = {a['source_key'] for a in d01.ADDED}
    d01_updates = set(d01.UPDATES)
    rows, errs = [], []
    for x in wb:
        o = dec.R.get(x['id'], {})
        cluster = o.get('cluster') or dec.THEME_TO_CLUSTER.get(x['theme'])
        if not cluster or cluster not in dec.CLUSTERS:
            errs.append('%s: no cluster' % x['id'])
            continue
        cl = dec.CLUSTERS[cluster]
        verdict = o.get('verdict') or (cl['verdict'] if cl['verdict'] != 'MIXED' else None)
        if not verdict:
            errs.append('%s: no verdict' % x['id'])
            continue
        action = o.get('action') or DEFAULT_ACTION.get(verdict, 'NONE')
        target = o.get('target')
        if action == 'APPEND' and target not in v2keys:
            errs.append('%s: APPEND target %s not in v2 view' % (x['id'], target))
        if action == 'ADD' and target not in d01_added:
            errs.append('%s: ADD target %s not in V3-D01 updates.py' % (x['id'], target))
        if action == 'APPEND' and target not in d01_updates:
            errs.append('%s: APPEND target %s not in V3-D01 updates.py' % (x['id'], target))
        overlap = sorted({v['key'] for v in x['v2_overlapping_records']})
        p1 = [p['claim_id'] + ':' + str(p['disposition']) for p in x['pass1_same_place']]
        absent = {'CANDIDATE_UNREPRESENTED_DUTY': 'YES: no same-candidate record of any run states this duty at or for this line' + ('; only records of a different action cite the line' if overlap else ''),
                  'FACET_OF_EXISTING': 'PARTLY: the passage is recorded (%s) but this atom or qualifier is not' % target,
                  'ALREADY_COVERED': 'NO: recorded', 'NON_NORMATIVE': 'NOT_APPLICABLE: not an independent obligation', 'OPEN_HYPOTHESIS': 'UNDETERMINED'}[verdict]
        rows.append({'codex_id': x['id'], 'pass': x['pass'], 'candidate': x['candidate'], 'path': x['path'], 'start_line': x['start_line'], 'end_line': x['end_line'], 'quote': x['quote'],
                     'codex_claim': x['claim'], 'codex_actor': x['actor'], 'codex_trigger': x['trigger'], 'codex_modality': x['modality'], 'codex_domain': x['domain'], 'codex_exceptions': x['exceptions'], 'codex_enforcement_effect': x['enforcement_effect'],
                     'codex_effective_status': x['comparison_status'], 'codex_effective_closest_policy_ids': x['closest_policy_ids'], 'codex_revisions_applied': x['revisions'], 'codex_open_question': x['open_question'],
                     'verdict': verdict, 'kit_category': KIT_CATEGORY[verdict], 'kind': o.get('kind') or cl['kind'], 'cluster': cluster, 'overlay_action': action, 'overlay_target': target, 'note': o.get('note') or '',
                     'reasoning': cl['reading'], 'evidence': {'existed_in_frozen_inputs': 'YES: exact quote at the cited lines (preflight check and Codex validator)', 'absent_or_mislabeled_in_three_runs': absent,
                                                               'handled_by_pass1': ('YES: ' + ', '.join(p1)) if p1 else ('PARTLY: Pass 1 provisional record %s' % target if (target or '').startswith('AUG1') else 'NO'),
                                                               'still_in_v2_and_v3_bytes': 'YES' if x['cited_text_still_in_v3_bytes'] else 'NO: cited text changed in v1/v2', 'file_changed_in_v1_v2': x['file_changed_v1_v2']},
                     'v2_relation': {'overlapping_v2_records': overlap, 'named_baseline_groups': sorted({n['group'] for n in x['codex_named_baselines'] if n['group']})},
                     'provenance': 'stage_A/codex_iterative_search/PASSES/pass_%04d/CANDIDATE_CLAIMS.jsonl#%s; decision _adjudication/decisions.py' % (x['pass'], x['id']), 'adjudicated_by': 'v3 session (same model family as Step 2 and v1/v2; self-review, not independent)'})
    if errs:
        for e in errs:
            print('ERROR', e)
        return 1
    rows.sort(key=lambda r: (r['pass'], CANDIDATES.index(r['candidate']), r['codex_id']))
    write_jsonl('PASS2_PASS3_ADJUDICATION.jsonl', rows)
    by = defaultdict(list)
    for r in rows:
        by[r['cluster']].append(r)
    census = defaultdict(list)
    for c in dec.CENSUS:
        census[c['cluster']].append(c)
    crows = []
    for cid, cl in dec.CLUSTERS.items():
        mem = by.get(cid, [])
        crows.append({'cluster': cid, 'title': cl['title'], 'kind': cl['kind'], 'reading': cl['reading'], 'significance': cl['significance'], 'n_codex_records': len(mem),
                      'codex_ids': [m['codex_id'] for m in mem], 'by_pass': dict(Counter(m['pass'] for m in mem)), 'candidates': sorted({m['candidate'] for m in mem}, key=CANDIDATES.index),
                      'verdicts': dict(Counter(m['verdict'] for m in mem)), 'overlay_actions': sorted({'%s %s' % (m['overlay_action'], m['overlay_target']) for m in mem if m['overlay_action'] != 'NONE'}),
                      'cross_pass_duplicates': len(mem) > 1 and len({m['pass'] for m in mem}) > 1, 'v3_census_additions': census.get(cid, []),
                      'study_level_new_obligation': False})
    write_jsonl('UNIQUE_ISSUE_CLUSTERS.jsonl', crows)
    added = sorted({r['overlay_target'] for r in rows if r['overlay_action'] == 'ADD'} | {c['target'] for c in dec.CENSUS if c['action'] == 'ADD'})
    appended = sorted({r['overlay_target'] for r in rows if r['overlay_action'] == 'APPEND'} | {c['target'] for c in dec.CENSUS if c['action'] == 'APPEND'})
    counts = {'at': now(), 'codex_records': {'pass2': sum(1 for r in rows if r['pass'] == 2), 'pass3': sum(1 for r in rows if r['pass'] == 3), 'total': len(rows)},
              'by_verdict': dict(Counter(r['verdict'] for r in rows)), 'by_verdict_and_pass': {'%s/p%d' % k: v for k, v in Counter((r['verdict'], r['pass']) for r in rows).items()}, 'by_kind': dict(Counter(r['kind'] for r in rows)),
              'unique_semantic_clusters': len(crows), 'clusters_by_kind': dict(Counter(c['kind'] for c in crows)), 'clusters_with_normative_effect': sum(1 for c in crows if any(v in c['verdicts'] for v in ('CANDIDATE_UNREPRESENTED_DUTY', 'FACET_OF_EXISTING'))),
              'study_level_new_independent_obligations': 0, 'candidate_level_unrepresented_duty_records_codex': sum(1 for r in rows if r['verdict'] == 'CANDIDATE_UNREPRESENTED_DUTY'),
              'distinct_added_records': added, 'n_added_records': len(added), 'distinct_appended_records': appended, 'n_appended_records': len(appended), 'census_items': len(dec.CENSUS),
              'open_hypotheses': [r['codex_id'] for r in rows if r['verdict'] == 'OPEN_HYPOTHESIS'], 'open_observations': ['CL21-M1-SECTION-REF-HEURISTIC', 'CL15 L0 raw-HTML sentence absent', 'CL01 hook budgets differ by candidate; host behavior NOT_RUN'],
              'needs_user_decision': [], 'pass1_overlap': sum(1 for r in rows if r['evidence']['handled_by_pass1'] != 'NO')}
    write_json('ADJUDICATION_COUNTS.json', counts)
    dh = sha256_file(out_path('_adjudication', 'decisions.py'))
    wh = sha256_file(out_path('_adjudication', 'WORKBENCH.jsonl'))
    for cid, mem in by.items():
        write_json(os.path.join('ADJUDICATION_CHECKPOINTS', cid + '.json'), {'cluster': cid, 'at': now(), 'n_records': len(mem), 'rows_sha256': rec_hash(mem), 'decisions_sha256': dh, 'workbench_sha256': wh, 'status': 'FINAL'})
    print(json.dumps({k: counts[k] for k in ('codex_records', 'by_verdict', 'unique_semantic_clusters', 'n_added_records', 'n_appended_records', 'clusters_with_normative_effect')}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
