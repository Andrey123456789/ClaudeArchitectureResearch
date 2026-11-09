"""V3-D01 regression: the Pass 2 + Pass 3 overlay is applied exactly as adjudicated, moves no coverage or strength cell, and leaves every
security-scan prompt atom represented in each candidate whose source states it. Data and source only."""
import copy
import importlib.util
import re
from collections import Counter

from rcommon import CANDIDATES, input_path, norm_ws, out_path, read_jsonl, read_lines, v2_path, wc_path

RULE = 'V3-D01-PASS23-OVERLAY'
SCAN = '.claude/skills/security-scan/references/scan-layers.md'
# atom: (source pattern, claim pattern)
ATOMS = {'local-account lockout': (r'lockout', r'lockout|brute'), 'local-account credential storage': (r'credential storage', r'credential.storage'),
         'upload execution': (r'execution or public-serving|execution/public-serving', r'execut'), 'upload public serving': (r'public-serving', r'public'),
         'SSRF inspection': (r'influences? (over )?(the )?scheme|users can influence the scheme|user influence over scheme', r'scheme|SSRF via'), 'raw HTML in server-rendered UI': (r'raw HTML', r'raw HTML'),
         'duplicate or missing security logging': (r'(duplicate|duplicated) or missing|missing or duplicated', r'duplicat'),
         'verbose production errors': (r'verbose (production )?error', r'verbose'), 'committed .env files': (r'\.env`? files', r'\.env')}


def load_updates():
    spec = importlib.util.spec_from_file_location('d01u', out_path('_rules', RULE, 'updates.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def census(view):
    out = {}
    for atom, (src, clm) in ATOMS.items():
        for c in CANDIDATES:
            lines = read_lines(wc_path(c, SCAN))
            hits = [n for n in range(1, len(lines) + 1) if re.search(src, norm_ws(' '.join(lines[n - 1:n + 2])), re.I)]
            if not hits:
                out[(atom, c)] = 'NO_SOURCE'
                continue
            recs = [r['source_key'] for r in view if r['candidate'] == c and r['repair']['active'] and re.search(clm, r.get('claim_text') or '', re.I)
                    and any(e.get('start_line') and e['path'].endswith(SCAN) and e['start_line'] <= max(hits) + 3 and e['end_line'] >= min(hits) - 3 for e in r.get('current_evidence_refs') or [])]
            out[(atom, c)] = recs or 'MISSING'
    return out


def run(ctx):
    u = load_updates()
    view = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by = {r['source_key']: r for r in view}
    v2 = {r['source_key']: r for r in read_jsonl(v2_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    adj = read_jsonl(out_path('PASS2_PASS3_ADJUDICATION.jsonl'))
    ctx.check('211 adjudicated Codex records (63 Pass 2, 148 Pass 3)', len(adj) == 211 and Counter(x['pass'] for x in adj) == Counter({2: 63, 3: 148}), kind='DATA', actual=len(adj))
    want_add = {x['overlay_target'] for x in adj if x['overlay_action'] == 'ADD'}
    want_app = {x['overlay_target'] for x in adj if x['overlay_action'] == 'APPEND'}
    ctx.check('every ADD decision is an added record of this rule', want_add <= {a['source_key'] for a in u.ADDED}, sorted(want_add - {a['source_key'] for a in u.ADDED}), kind='DATA')
    ctx.check('every APPEND decision is an update of this rule', want_app <= set(u.UPDATES), sorted(want_app - set(u.UPDATES)), kind='DATA')
    for a in u.ADDED:
        r = by.get(a['source_key'])
        ok = r is not None and r['repair']['active'] and r['classification'] == 'EXTRA_WORKFLOW' and r['modality'] == 'DEFAULT' and not r.get('canonical_coverage') and any(e.get('start_line') for e in r['current_evidence_refs'])
        ctx.check('added scan prompt: EXTRA_WORKFLOW, DEFAULT, no canonical link, current line: %s' % a['source_key'], ok, r and (r['classification'], r['modality'], r.get('canonical_coverage')), a['candidate'], 'DATA')
    for key, e in u.UPDATES.items():
        r, o = by[key], v2[key]
        same = all(r.get(f) == o.get(f) for f in ('classification', 'modality', 'canonical_coverage', 'strength_vs_canonical'))
        ctx.check('facet written in, labels unchanged, original kept: %s' % key, r['claim_text'] == e['claim'] and r['claim_text_original'] == o['claim_text_original'] and same and r.get('codex_pass23_ids') == e['set']['codex_pass23_ids'], key, r['candidate'], 'DATA')
    now = {(x['candidate'], x['policy_id']): (x['status'], x['strength_status']) for x in read_jsonl(out_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    old = {(x['candidate'], x['policy_id']): (x['status'], x['strength_status']) for x in read_jsonl(v2_path('REPAIRED_POLICY_COVERAGE.jsonl'))}
    ctx.check('no coverage or strength cell moved against v2 (1,176)', now == old, sorted(k for k in old if now.get(k) != old[k])[:6], kind='DATA', actual=len(now))
    cen = census(view)
    for (atom, c), v in sorted(cen.items()):
        if v == 'NO_SOURCE':
            ctx.add('scan atom: %s (no such sentence in this candidate)' % atom, 'PASS', 'NO_SOURCE', c, 'SOURCE')
        else:
            ctx.check('scan atom represented where the source states it: %s' % atom, v != 'MISSING', v, c, 'DATA')
    ctx.check('the only scan sentence absent from a candidate is L0 raw HTML (reported text difference)', sorted(k for k, v in cen.items() if v == 'NO_SOURCE') == [('raw HTML in server-rendered UI', 'L0')], sorted(k for k, v in cen.items() if v == 'NO_SOURCE'), kind='SOURCE')
    nc = {x['key']: x for x in read_jsonl(out_path('V3_NEW_CLAIMS_REVIEW.jsonl'))}
    ctx.check('every added record has a CONFIRMED v3 review row', all(nc.get(a['source_key'], {}).get('status') == 'CONFIRMED' for a in u.ADDED), [a['source_key'] for a in u.ADDED if nc.get(a['source_key'], {}).get('status') != 'CONFIRMED'][:5], kind='DATA')
    # Mutation: without one added record the census finds the gap again.
    mut = [r for r in view if r['source_key'] != 'V3A-K0-103']
    ctx.check('mutation: removing an added record reopens its census gap', census(mut)[('SSRF inspection', 'K0')] == 'MISSING', kind='MUTATION')
    mut = copy.deepcopy(by['FG-K1-8e0b256c02'])
    mut['claim_text'] = v2['FG-K1-8e0b256c02']['claim_text']
    ctx.check('mutation: an unapplied facet is caught', mut['claim_text'] != u.UPDATES['FG-K1-8e0b256c02']['claim'], kind='MUTATION')
    ctx.not_run('a fresh-session or independent reader of the 211 adjudications', 'self-review by the same model family; readings are in PASS2_PASS3_ADJUDICATION.jsonl')
