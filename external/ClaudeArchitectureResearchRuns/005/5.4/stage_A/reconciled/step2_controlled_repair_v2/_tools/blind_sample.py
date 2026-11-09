"""Targeted stratified reread of records no earlier review touched, for falsification. Not an unbiased error rate: strata are equal-sized, so their counts cannot be scaled to the population.

  blind_sample.py draw     seeded draw; writes _rules/C07-PARITY-CLOSE/BLIND_VIEW.txt (claim and current source, no stored label, modality or policy)
  blind_sample.py compare  reads BLIND_READING.txt, logs its hash first, and writes BLIND_REREAD_SAMPLE.jsonl

The reader is the same model family that wrote the labels, and it sees the claim text, so this is a weak check. The hash proves the order of writing, not freedom from prior belief.
"""
import importlib.util
import json
import os
import random
import sys
from collections import Counter

from pi012_scan import scan
from rcommon import CANDIDATES, baseline, norm_ws, now, out_path, read_json, read_jsonl, read_lines, sha256_file, utf8_stdout, wc_path, write_json, write_jsonl, write_text

RULE = 'C07-PARITY-CLOSE'
# The first draw (seed 20261103) listed records in stratum order, which leaked the label group by position. It was viewed, not read, and is kept as BLIND_PLAN_BURNED.json; its records are excluded here.
SEED = 20261104
PER_STRATUM = 2
STRATA = {'CANONICAL': ('CANONICAL_ONLY',), 'DELTA_OR_MIXED': ('CANONICAL_PLUS_DELTA', 'MIXED'), 'EXTRA': ('EXTRA_PRODUCT', 'EXTRA_WORKFLOW', 'INTERNAL_ARCHITECTURE'), 'NON_NORMATIVE': ('NON_NORMATIVE',)}
GROUP = {'CANONICAL_ONLY': 'CANONICAL', 'CANONICAL_PLUS_DELTA': 'DELTA_OR_MIXED', 'MIXED': 'DELTA_OR_MIXED', 'EXTRA_PRODUCT': 'EXTRA', 'EXTRA_WORKFLOW': 'EXTRA', 'INTERNAL_ARCHITECTURE': 'EXTRA', 'NON_NORMATIVE': 'NON_NORMATIVE', 'UNCERTAIN': 'UNCERTAIN'}
FORCE = {'MUST': 'BINDING', 'MUST_NOT': 'BINDING', 'DECIDED': 'BINDING', 'REQUIRES_APPROVAL': 'BINDING', 'DEFAULT': 'DEFAULT_CLASS', 'SHOULD': 'DEFAULT_CLASS', 'SHOULD_NOT': 'DEFAULT_CLASS', 'MAY': 'PERMISSION', 'NONE': 'NONE', 'MIXED': 'MIXED'}


def excluded():
    """Everything an earlier review already read, so the sample does not repeat it."""
    out = set()
    for f in ('PI012_79_REVIEW.jsonl', 'PI012_230_REVIEW.jsonl', 'PI012_EXTENSION_REVIEW.jsonl'):
        out |= {r['key'].split('/')[0] for r in read_jsonl(out_path(f))}
    for v in scan().values():
        out |= {x['key'] for x in v}
    out |= {r['case_key'].split('/')[0] for r in read_jsonl(out_path('CORRECTION_103_ADJUDICATION.jsonl'))}
    out |= {r['id'].split('/')[0] for r in read_jsonl(out_path('UNRESOLVED_DECISIONS.jsonl')) if r.get('id')}
    out |= {r['key'] for r in read_jsonl(out_path('REVIEW_NEEDED_62.jsonl'))}
    spec = importlib.util.spec_from_file_location('r22s_b', out_path('_rules', 'R22-111-TRIGGER', 'sample.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out |= {x['key'] for x in m.SAMPLE}
    rows = read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))
    out |= {r['source_key'] for r in rows if r['repair']['rules']}
    burned = out_path('_rules', RULE, 'BLIND_PLAN_BURNED.json')
    if os.path.exists(burned):
        out |= {x['key'] for x in read_json(burned)['plan']}
    return out, rows


def draw():
    ex, rows = excluded()
    rng = random.Random(SEED)
    picked = []
    for c in CANDIDATES:
        for stratum, labels in STRATA.items():
            pool = sorted(r['source_key'] for r in rows if r['candidate'] == c and r['repair']['active'] and r['classification'] in labels and r['source_key'] not in ex and r['source_key'] in baseline(c))
            picked.extend((c, stratum, k) for k in rng.sample(pool, min(PER_STRATUM, len(pool))))
    # Without this, the id order gives away the stratum, and so the stored label group.
    rng.shuffle(picked)
    by = {r['source_key']: r for r in rows}
    lines = ['# Blind view: seed %d. Claim and current source only. Write one line per record in BLIND_READING.txt: id | GROUP | FORCE | note' % SEED, '# GROUP: CANONICAL, DELTA_OR_MIXED, EXTRA, NON_NORMATIVE. FORCE: BINDING, DEFAULT_CLASS, PERMISSION, NONE, MIXED.', '']
    plan = []
    for i, (c, stratum, k) in enumerate(picked, 1):
        r = by[k]
        e = next(x for x in r['current_evidence_refs'] if x.get('start_line'))
        rel = e['path'].split('/template/')[1]
        src = read_lines(wc_path(c, rel))
        a, b = max(1, e['start_line'] - 1), min(len(src), e['end_line'] + 1)
        plan.append({'id': 'B%02d' % i, 'candidate': c, 'stratum': stratum, 'key': k, 'path': rel, 'start_line': e['start_line'], 'end_line': e['end_line']})
        lines.append('B%02d %s %s:%d-%d' % (i, c, rel, e['start_line'], e['end_line']))
        lines.append('  claim: %s' % (r.get('claim_text') or '')[:400])
        lines.append('  source: %s' % norm_ws(' '.join(src[a - 1:b]))[:900])
        lines.append('')
    write_text(os.path.join('_rules', RULE, 'BLIND_VIEW.txt'), '\n'.join(lines))
    write_json(os.path.join('_rules', RULE, 'BLIND_PLAN.json'), {'seed': SEED, 'per_stratum': PER_STRATUM, 'n': len(plan), 'n_excluded': len(ex), 'plan': plan, 'design': 'Equal draws per candidate and label group from records no earlier review read. Not proportional, so not an unbiased estimate of any population rate.'})
    print('drew', len(plan), 'excluded', len(ex), Counter(p['stratum'] for p in plan))


def compare():
    p = out_path('_rules', RULE, 'BLIND_READING.txt')
    h = sha256_file(p)
    plan = read_json(out_path('_rules', RULE, 'BLIND_PLAN.json'))
    rows = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    reads = {}
    with open(p, encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = [x.strip() for x in line.split('|')]
                reads[parts[0]] = parts
    out = []
    for x in plan['plan']:
        r = rows[x['key']]
        g = GROUP[r['classification']]
        fo = FORCE.get(r.get('modality'), 'NONE')
        rd = reads.get(x['id'])
        if not rd:
            raise SystemExit('no reading for ' + x['id'])
        out.append(dict(x, stored_group=g, stored_force=fo, stored_classification=r['classification'], stored_modality=r.get('modality'), read_group=rd[1], read_force=rd[2], note=rd[3] if len(rd) > 3 else '', group_agrees=rd[1] == g, force_agrees=rd[2] == fo, reading_sha256=h))
    write_jsonl('BLIND_REREAD_SAMPLE.jsonl', out)
    print(Counter((x['group_agrees'], x['force_agrees']) for x in out))
    for x in out:
        if not (x['group_agrees'] and x['force_agrees']):
            print(x['id'], x['candidate'], x['key'], 'stored', x['stored_classification'], x['stored_modality'], 'read', x['read_group'], x['read_force'], '|', x['note'][:160])


if __name__ == '__main__':
    utf8_stdout()
    {'draw': draw, 'compare': compare}[sys.argv[1]]()
