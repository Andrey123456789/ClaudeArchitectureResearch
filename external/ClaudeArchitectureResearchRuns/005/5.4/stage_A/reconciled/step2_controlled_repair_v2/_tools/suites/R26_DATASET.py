"""R26 regression: the repaired derived view, its crosswalk, replay and whole-view invariants. Mutations show that the checks catch damage."""
import copy
import json
import os
from collections import Counter

import dataset
import viewcheck
from rcommon import AUD, CANDIDATES, baseline, norm_ws, out_path, policies, read_json, read_jsonl, read_lines, rec_hash, wc_path


def run(ctx):
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    cross = read_jsonl(out_path('ORIGINAL_TO_REPAIRED_CLAIMS.jsonl'))
    cov = read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))
    man = read_json(out_path('REPAIRED_VIEW_MANIFEST.json'))
    errs = viewcheck.check_all(rows, cross, cov)
    ctx.check('whole-view invariants: ids, evidence lines, coverage, crosswalk', not errs, errs[:12], kind='DATA', actual=len(errs))
    # replay
    r1, c1 = dataset.build()
    r2, c2 = dataset.build()
    flat = [r for c in CANDIDATES for r in r1[c]]
    ctx.check('replay twice gives identical records', rec_hash(flat) == rec_hash([r for c in CANDIDATES for r in r2[c]]) and rec_hash(c1) == rec_hash(c2), kind='DATA')
    ctx.check('replay equals the files on disk', rec_hash(flat) == rec_hash(rows) and rec_hash(c1) == rec_hash(cross), kind='DATA')
    cv, moved = dataset.coverage_rows(r1)
    ctx.check('coverage replay equals the file on disk', rec_hash(cv) == rec_hash(cov), kind='DATA')
    # counts
    frozen = sum(len(baseline(c)) for c in CANDIDATES)
    cs = Counter(x['status'] for x in cross)
    ctx.check('6,402 baseline identities kept; the view count is reported, not assumed', frozen == 6402 and man['counts']['repaired_rows'] == len(rows) == frozen + cs['ADDED'], {'rows': len(rows), 'status': dict(cs)}, kind='DATA', actual=dict(cs))
    ctx.check('manifest counts equal the files', man['counts']['by_crosswalk_status'] == dict(cs) and man['counts']['coverage_rows'] == 1176 and man['counts']['active_rows'] == sum(1 for r in rows if r['repair']['active']), kind='DATA')
    # coverage moved
    ctx.check('coverage or strength moves are listed, not hidden', man['counts']['coverage_or_strength_moved'] == moved, moved[:10], kind='DATA', actual=len(moved))
    # uncertainty
    un = [r['source_key'] for r in rows if r['classification'] == 'UNCERTAIN' or any(s.get('classification') == 'UNCERTAIN' for s in r.get('subclauses') or [])]
    ctx.check('no UNCERTAIN record remains silently: each baseline one has a rule and a current reading', not un, un[:6], kind='SEMANTIC')
    trail = {r['source_key']: r for r in rows}
    base_unc = [k for c in CANDIDATES for k, r in baseline(c).items() if r['classification'] == 'UNCERTAIN']
    ctx.check('all 19 baseline UNCERTAIN records carry a repair rule', len(base_unc) == 19 and all(trail[k]['repair']['rules'] for k in base_unc), kind='SEMANTIC')
    open_rows = {r['id'].split('/')[0] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r['status'] == 'OPEN'} - dataset.resolved_open_keys()
    ctx.check('PI-012 unresolved records stay marked open in the view, unless a v2 adjudication row closed them', all(trail[k]['repair'].get('open_question') for k in open_rows), sorted(open_rows), kind='SEMANTIC')
    ctx.check('no other record is marked open', sum(1 for r in rows if r['repair'].get('open_question')) == len(open_rows), kind='DATA')
    # claims
    reworded = [r for r in rows if r['repair']['status'] == 'REWORDED']
    ctx.check('every reworded record keeps its original claim and differs from it or carries a rule', all(r['claim_text_original'] and r['repair']['rules'] for r in reworded), len(reworded), kind='DATA', actual=len(reworded))
    stale = [r['source_key'] for r in rows if r['repair']['active'] and r['repair']['status'] != 'REWORDED' and 'approved workflow' in (r['claim_text'] or '').lower() and any(('R02' in t) for t in r['repair']['rules'])]
    ctx.check('no active Git claim under R02 still relies on an approved workflow', not stale, stale[:6], kind='SEMANTIC')
    # removed
    rem = {r['source_key']: r for r in rows if not r['repair']['active']}
    ctx.check('three removed rows, all under R06', set(rem) == {'FG-M1-668bf4f9ad', 'FG-K0-a769f55ff5', 'FG-L0-149e95678a'} and all('R06-HQ05-DEP025' in r['repair']['rules'] for r in rem.values()), sorted(rem), kind='DATA')
    ctx.check('M1 no longer holds the peer-override marker', 'peer-override' not in ' '.join(read_lines(wc_path('M1', '.claude/scripts/lib/dependency-commands.js'))).lower(), candidate='M1', kind='SEMANTIC')
    # added
    added = [r for r in rows if str(r.get('view_record_type') or '').startswith('REPAIR')]
    ctx.check('added ids are new and never reuse a baseline id', all(r['source_key'] not in baseline(r['candidate']) and viewcheck.NEW_ID.match(r['source_key']) for r in added), len(added), kind='DATA', actual=len(added))
    ctx.check('every added claim resolves to a current line', all(x.get('start_line') for r in added for x in r['current_evidence_refs']), kind='DATA')
    ncp = [r for r in added if r['source_key'].startswith('NCP-')]
    ctx.check('four proposals, not promoted, in their own candidate only', len(ncp) == 4 and not any(r['source_key'] in policies() for r in ncp) and len(policies()) == 196 and {r['candidate'] for r in ncp} == {'M', 'M1', 'L0'}, kind='SEMANTIC')
    per = Counter(r['candidate'] for r in added if r['source_key'].startswith('REP-'))
    ctx.check('added claims follow all-six rules: equal counts across candidates', len(set(per.values())) == 1, dict(per), kind='SEMANTIC')
    # labels
    scope = [r['source_key'] for r in rows if r.get('evaluation_scope')]
    ctx.check('evaluation scope labels survive the replay', len(scope) >= 6, scope[:8], kind='DATA', actual=len(scope))
    ctx.check('derived applicability keeps the original field and does not touch modality', all(r['trigger_field_original'] == r.get('trigger') for r in rows), kind='DATA')
    # graph
    if os.path.exists(out_path('POLICY_DEPENDENCY_GRAPH.json')):
        g = read_json(out_path('POLICY_DEPENDENCY_GRAPH.json'))
        ok = all(len(g['per_candidate'][c]) == 196 for c in CANDIDATES) and all(v['owners'] or v['partial_witnesses'] for c in CANDIDATES for v in g['per_candidate'][c].values())
        ctx.check('dependency graph: 196 policies per candidate, each with an owner or witness', ok, kind='DATA')
    else:
        ctx.check('dependency graph exists', False, kind='DATA')
    # mutations
    m = copy.deepcopy(rows)
    m[0]['repair']['baseline_sha256'] = 'x'
    ctx.check('mutation: a tampered baseline hash is caught', any('baseline hash' in e for e in viewcheck.check_rows(m)), kind='MUTATION')
    m = copy.deepcopy(rows)
    t = next(r for r in m if any(x.get('new_quote') for x in r['current_evidence_refs']))
    next(x for x in t['current_evidence_refs'] if x.get('new_quote'))['new_quote'] = 'a sentence that exists nowhere in the template'
    ctx.check('mutation: a quote not at its lines is caught', any('quote not at' in e for e in viewcheck.check_rows(m)), kind='MUTATION')
    m = copy.deepcopy(rows)
    m[5]['source_key'] = 'FG-M-counterfeit'
    ctx.check('mutation: a counterfeit id is caught', any('new stable id' in e or 'lost baseline' in e for e in viewcheck.check_rows(m)), kind='MUTATION')
    m = copy.deepcopy(cross)[1:]
    ctx.check('mutation: a lost crosswalk row is caught', viewcheck.check_crosswalk(rows, m) != [], kind='MUTATION')
    m = copy.deepcopy(rows)
    tgt = next(cell for cell in cov if cell['candidate'] == 'K1' and len(cell['direct_source_keys']) == 1 and not cell['partial_source_keys'])
    for r in m:
        if r['source_key'] == tgt['direct_source_keys'][0]:
            r['repair']['active'] = False
    ctx.check('mutation: deactivating the only witness is caught by coverage', viewcheck.check_coverage(m, cov) != [], tgt['policy_id'], kind='MUTATION')
