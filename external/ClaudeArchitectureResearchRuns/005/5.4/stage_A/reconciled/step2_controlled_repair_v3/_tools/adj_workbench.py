"""Part A workbench: one evidence row per effective Codex Pass 2 / Pass 3 record, for independent adjudication.

PYTHONPATH=_tools python -B _tools/adj_workbench.py

Reads (never writes) Codex pass_0002 and pass_0003, the applied revisions, the immutable inputs, the Pass 1 augmented union and ledger,
and v2's final view by reference. Writes _adjudication/WORKBENCH.jsonl and _adjudication/clusters/<cluster>.md.
For each record: effective Codex fields (revisions applied), the cited source with context, every v2 view record whose frozen evidence
range overlaps the cited range (same file), the union groups Codex named as baseline comparisons and their v2 labels, Pass 1 ledger
rows at the same place, and whether v1/v2 changed the cited lines. The cluster key is a provisional theme for reading; the adjudicator
assigns the final semantic cluster.
"""
import json
import os
import re
from collections import defaultdict

from rcommon import CANDIDATES, CODEX, INPUTS, REC, input_path, norm_ws, read_jsonl, read_lines, sha256_file, utf8_stdout, v2_path, wc_path, write_jsonl, write_text

P1 = os.path.join(REC, 'step1_union_augmented_pass1')
PASSES = (2, 3)


def codex_records():
    state = json.load(open(os.path.join(CODEX, 'STATE.json'), encoding='utf-8-sig'))
    revs = state.get('finding_revisions', {})
    out = []
    for pid in PASSES:
        d = os.path.join(CODEX, 'PASSES', 'pass_%04d' % pid)
        for x in read_jsonl(os.path.join(d, 'CANDIDATE_CLAIMS.jsonl')):
            eff = dict(x)
            applied = []
            if x['id'] in revs:
                rev = json.load(open(os.path.join(CODEX, revs[x['id']]['revision'].replace('/', os.sep)), encoding='utf-8-sig'))
                eff.update(rev.get('field_updates') or {})
                eff['comparison_status'] = rev['effective_status']
                applied.append(rev['revision_id'])
            eff['_pass'] = pid
            eff['_revisions'] = applied
            out.append(eff)
    return out


def key_to_unit(k):
    run, c, f, rid = k.split('/', 3)
    if f == 'constraints.jsonl':
        return '%s:%s:CONSTRAINT:%s' % (run.upper(), c, rid)
    if f == 'BLIND_FINDINGS.jsonl':
        return 'CODEX:%s:BLIND_FINDING:%s' % (c, rid)
    return None


THEMES = [
    ('HOOK-TIMEOUT', lambda r: r['path'].endswith('settings.json') or 'timeout=15000' in r['claim']),
    ('ERROR-CONTRACT-FIELDS', lambda r: 'aspnet-error-handling' in r['path'] and re.search(r'error (contract|response)', r['claim'], re.I)),
    ('OPTIONS-DECISION-GUIDE', lambda r: 'configuration/SKILL.md' in r['path'] or 'BindConfiguration' in r['claim']),
    ('SERILOG-DECISION-GUIDE', lambda r: 'serilog.md' in r['path']),
    ('LOGGING-SCOPE-GUIDE', lambda r: r['path'].endswith('logging/SKILL.md')),
    ('DI-DECISION-GUIDE', lambda r: 'dependency-injection' in r['path']),
    ('EF-DECISION-GUIDE', lambda r: 'ef-core/SKILL.md' in r['path'] and ('FindAsync' in r['claim'] or 'ExecuteUpdate' in r['claim'])),
    ('CACHING-DECISION-GUIDE', lambda r: 'caching/SKILL.md' in r['path']),
    ('HEDGING-GUIDE', lambda r: 'resilience.md' in r['path']),
    ('SCAN-LOCAL-ACCOUNTS', lambda r: 'scan-layers' in r['path'] and re.search(r'password|lockout|enumeration|credential storage|local account', r['claim'], re.I)),
    ('SCAN-SECRETS-CONFIG', lambda r: 'scan-layers' in r['path'] and re.search(r'\.env|debug|verbose', r['claim'], re.I)),
    ('SCAN-UPLOADS', lambda r: 'scan-layers' in r['path'] and re.search(r'upload', r['claim'], re.I)),
    ('SCAN-SSRF', lambda r: 'scan-layers' in r['path'] and re.search(r'SSRF|outbound', r['claim'], re.I)),
    ('SCAN-RAW-HTML', lambda r: 'scan-layers' in r['path'] and re.search(r'raw HTML', r['claim'], re.I)),
    ('SCAN-LOGGING', lambda r: 'scan-layers' in r['path'] and re.search(r'logging', r['claim'], re.I)),
    ('SCAN-TARGETED-PRIORITY', lambda r: 'security-scan/SKILL.md' in r['path']),
]


def theme(r):
    for name, f in THEMES:
        if f(r):
            return name
    return 'SINGLE-%s' % r['id']


def overlaps(a1, b1, a2, b2, slack=0):
    return a1 <= b2 + slack and a2 <= b1 + slack


def main():
    utf8_stdout()
    recs = codex_records()
    v2rows = read_jsonl(v2_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    by_file = defaultdict(list)
    unit_to_group = {}
    for r in v2rows:
        for ref in r.get('evidence_refs') or []:
            by_file[(r['candidate'], ref['path'].split('/output/template/', 1)[-1])].append((ref['start_line'], ref['end_line'], r))
        for u in (r.get('provenance') or {}).get('source_record_keys') or []:
            unit_to_group[u] = r['source_key']
        if not r.get('evidence_refs'):
            # Added claims and proposals (v1/v2) carry only anchors on v2 bytes. Map each back to frozen lines by its quote.
            for ref in r.get('current_evidence_refs') or []:
                q = ref.get('new_quote')
                rel = ref['path'].split('/template/', 1)[-1]
                if not os.path.exists(input_path(r['candidate'], rel)):
                    continue
                if not q:
                    v2file = v2_path('candidates', r['candidate'], 'template', *rel.split('/'))
                    if ref.get('start_line') and sha256_file(v2file) == sha256_file(input_path(r['candidate'], rel)):
                        by_file[(r['candidate'], rel)].append((ref['start_line'], ref['end_line'], r))
                    continue
                orig = read_lines(input_path(r['candidate'], rel))
                hit = [n for n in range(1, len(orig) + 1) if norm_ws(q)[:60].lower() in norm_ws(' '.join(orig[n - 1:n + 3])).lower()]
                if hit:
                    by_file[(r['candidate'], rel)].append((hit[0], hit[0] + max(0, len(q) // 90), r))
    by_key = {r['source_key']: r for r in v2rows}
    ledger = read_jsonl(os.path.join(P1, 'PASS1_REVIEW_LEDGER.jsonl'))
    p1claims = {x['id']: x for x in read_jsonl(os.path.join(CODEX, 'PASSES', 'pass_0001', 'CANDIDATE_CLAIMS.jsonl'))}
    p1_by_file = defaultdict(list)
    for l in ledger:
        cid = l.get('claim_id') or l.get('id')
        c = p1claims.get(cid)
        if c:
            p1_by_file[(c['candidate'], c['path'].replace('output/template/', ''))].append((c['start_line'], c['end_line'], l, c))
    rows = []
    for r in recs:
        c, rel = r['candidate'], r['path'].replace('output/template/', '')
        a, b = r['start_line'], r['end_line']
        lines = read_lines(input_path(c, rel))
        ctx = ['%4d%s %s' % (n, '>' if a <= n <= b else ' ', lines[n - 1]) for n in range(max(1, a - 3), min(len(lines), b + 3) + 1)]
        over = []
        for s, e, v in by_file.get((c, rel), []):
            if overlaps(a, b, s, e):
                over.append({'key': v['source_key'], 'range': [s, e], 'classification': v['classification'], 'modality': v.get('modality'), 'policies': [x['policy_id'] for x in v.get('canonical_coverage') or []], 'related': v.get('related_policy_ids'), 'claim': (v.get('claim_text') or '')[:260], 'active': v['repair']['active'], 'rules': v['repair']['rules']})
        named = []
        for comp in r.get('baseline_comparisons') or []:
            for k in comp.get('baseline_keys') or []:
                u = key_to_unit(k)
                g = unit_to_group.get(u) if u else None
                named.append({'baseline_key': k, 'assessment': comp.get('assessment'), 'group': g, 'group_claim': (by_key[g]['claim_text'][:200] if g in by_key else None), 'group_classification': by_key[g]['classification'] if g in by_key else None})
        p1 = [{'claim_id': l.get('claim_id') or l.get('id'), 'disposition': l.get('disposition'), 'range': [s, e], 'claim': c1['claim'][:200]} for s, e, l, c1 in p1_by_file.get((c, rel), []) if overlaps(a, b, s, e, 2)]
        cur = wc_path(c, rel)
        changed = sha256_file(cur) != sha256_file(input_path(c, rel))
        same_text = norm_ws(' '.join(lines[a - 1:b])) in norm_ws(' '.join(read_lines(cur)))
        rows.append({'id': r['id'], 'pass': r['_pass'], 'candidate': c, 'path': rel, 'start_line': a, 'end_line': b, 'theme': theme(r), 'claim': r['claim'], 'actor': r.get('actor'), 'trigger': r.get('trigger'), 'modality': r.get('modality'), 'domain': r.get('domain'),
                     'exceptions': r.get('exceptions'), 'enforcement_effect': r.get('enforcement_effect'), 'closest_policy_ids': r.get('closest_policy_ids'), 'comparison_status': r.get('comparison_status'), 'revisions': r['_revisions'], 'comparison_reason': r.get('comparison_reason'),
                     'open_question': r.get('open_question'), 'scenario': r.get('distinguishing_behavioral_scenario'), 'quote': r['quote'], 'context': ctx, 'v2_overlapping_records': over, 'codex_named_baselines': named, 'pass1_same_place': p1,
                     'file_changed_v1_v2': changed, 'cited_text_still_in_v3_bytes': same_text})
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_adjudication', 'clusters'), exist_ok=True)
    write_jsonl(os.path.join('_adjudication', 'WORKBENCH.jsonl'), rows)
    by_theme = defaultdict(list)
    for x in rows:
        by_theme[x['theme']].append(x)
    for t, xs in by_theme.items():
        out = ['# %s (%d records)\n' % (t, len(xs))]
        for x in sorted(xs, key=lambda x: (CANDIDATES.index(x['candidate']), x['path'], x['start_line'])):
            out.append('## %s (pass %d) %s %s:%d-%d  [%s %s]' % (x['id'], x['pass'], x['candidate'], x['path'], x['start_line'], x['end_line'], x['modality'], x['comparison_status']))
            out.append('CLAIM: %s' % x['claim'])
            out.append('TRIGGER: %s | EXC: %s | POL: %s' % (x['trigger'], (x['exceptions'] or '')[:200], x['closest_policy_ids']))
            out.append('CODEX WHY: %s' % (x['comparison_reason'] or '')[:400])
            out.append('```')
            out.extend(l[:220] for l in x['context'])
            out.append('```')
            out.append('v3 bytes: file changed in v1/v2=%s, cited text still present=%s' % (x['file_changed_v1_v2'], x['cited_text_still_in_v3_bytes']))
            for o in x['v2_overlapping_records']:
                out.append('- V2 %s %s %s/%s pol=%s rel=%s: %s' % (o['key'], o['range'], o['classification'], o['modality'], o['policies'], o['related'], o['claim'][:230]))
            for n in x['codex_named_baselines']:
                if n['group']:
                    out.append('- NAMED %s -> %s [%s] %s' % (n['baseline_key'], n['group'], n['group_classification'], (n['group_claim'] or '')[:180]))
            for p in x['pass1_same_place']:
                out.append('- PASS1 %s %s %s: %s' % (p['claim_id'], p['disposition'], p['range'], p['claim'][:150]))
            out.append('')
        write_text(os.path.join('_adjudication', 'clusters', t + '.md'), '\n'.join(out))
    print({t: len(v) for t, v in sorted(by_theme.items())})
    print('records', len(rows))


if __name__ == '__main__':
    main()
