"""Phase 0: enumerate the audit universe and freeze the sampling plan, before any sampled source is opened.

  python -B _tools/targets.py freeze   writes SAMPLING_PLAN.json and AUDIT_TARGETS.jsonl (refuses to overwrite the plan)
  python -B _tools/targets.py check    recomputes the selection and compares it with the frozen plan

Selection uses stored fields only to place a record in a stratum, then a SHA-256 sort of seed|stratum|source_key. Records already
targeted by sections A-C, and records the Step 2 reader already challenged or calibrated on, are excluded where availability permits.
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

from acommon import AUDIT_VERSION, CANDIDATES, S2, baseline, coverage, out_path, read_jsonl, source_range, utf8_stdout, write_json, write_jsonl

SEED = 'step2-semantic-audit-v1|seed-2026-11-03'
SAMPLE_CANDS = ['M1', 'L0', 'L1', 'K0', 'K1']
M_FIXED = ['FG-M-22cae42396', 'FG-M-1c4fc44b5e', 'FG-M-d0b6a09cce']
SPECIAL_CELLS = [('K0', 'API-014'), ('K0', 'API-019'), ('K1', 'GOV-007'), ('K1', 'API-014'), ('K1', 'API-019')]
SWAGGER_RE = re.compile(r'swagger ?ui|swagger-ui|swagger/index', re.I)
EXC_RE = re.compile(r'\b(exception|except|unless|explicit(ly)? request|narrow)', re.I)
EXEC_RE = re.compile(r'\.claude/(hooks|scripts)/|settings\.json$')
PAIRS = [('M', 'K1'), ('M1', 'K0'), ('L0', 'L1'), ('M', 'L0')]


def h(stratum, key):
    return hashlib.sha256(('%s|%s|%s' % (SEED, stratum, key)).encode('utf-8')).hexdigest()


def ranked(stratum, keys):
    return sorted(keys, key=lambda k: h(stratum, k))


def lists():
    n = [x for x in read_jsonl(os.path.join(S2, '_decisions', 'A13_AUDIT_FINDINGS.jsonl')) if x['category'] == 'N']
    om = read_jsonl(os.path.join(S2, 'POTENTIAL_OVERMERGES.jsonl'))
    unc = read_jsonl(os.path.join(S2, 'UNCERTAIN_CLASSIFICATIONS.jsonl'))
    orp = read_jsonl(os.path.join(S2, 'ORPHAN_REVIEW_QUEUE.jsonl'))
    fhd = read_jsonl(os.path.join(S2, 'FUTURE_HUMAN_DECISIONS.jsonl'))
    return n, om, unc, orp, fhd


def swagger_family():
    fam = {}
    for c in CANDIDATES:
        for k, r in baseline(c).items():
            txt = r['claim_text'] + ' ' + (r.get('primary_quote') or '')
            for e in r['evidence_refs']:
                txt += ' ' + source_range(e['path'], e['start_line'], e['end_line'])
            if SWAGGER_RE.search(txt):
                fam[k] = c
    return fam


def override_rows():
    return [(c, p) for c in CANDIDATES for p, r in coverage(c).items() if r.get('reviewer_override_note')]


def override_witnesses():
    w = set()
    for c, p in override_rows() + SPECIAL_CELLS:
        r = coverage(c)[p]
        w |= set(re.findall(r'FG-[A-Z0-9]+-[0-9a-f]{10}', r.get('reviewer_override_note') or ''))
        for f in ('direct_source_keys', 'partial_source_keys', 'strength_equivalent_source_keys', 'weaker_source_keys', 'stronger_source_keys', 'uncertain_source_keys'):
            w |= set(r.get(f) or [])
    return w


def challenged_keys():
    s = set()
    for c in CANDIDATES:
        for x in read_jsonl(os.path.join(S2, 'per_candidate', c, 'SEMANTIC_CHALLENGES.jsonl')):
            s.add(x.get('source_key'))
    for x in read_jsonl(os.path.join(S2, 'CALIBRATION.jsonl')):
        s.add(x.get('source_key'))
    return s


def take(stratum, pool, n, chosen):
    picked = [k for k in ranked(stratum, pool) if k not in chosen][:n]
    chosen.update(picked)
    return picked


def primary_path(r):
    return (r.get('primary_anchor') or {}).get('path') or r['evidence_refs'][0]['path']


def sample_candidate(c, excluded, soft_excluded):
    b = baseline(c)
    chosen = set()
    out = []
    shortfalls = []

    def pick(stratum, label, pred, n, fallback=None):
        hard = [k for k, r in b.items() if k not in excluded and pred(r)]
        pool = [k for k in hard if k not in soft_excluded]
        got = take('%s|%s' % (c, stratum), pool, n, chosen)
        note = None
        if len(got) < n and hard:
            more = take('%s|%s|soft' % (c, stratum), hard, n - len(got), chosen)
            got += more
            if more:
                note = 'took %d record(s) the Step 2 reader had challenged or calibrated on: pool exhausted' % len(more)
        if len(got) < n and fallback:
            more = [k for k in ranked('%s|%s|fb' % (c, stratum), [k for k, r in b.items() if k not in excluded and fallback(r)]) if k not in chosen][:n - len(got)]
            chosen.update(more)
            got += more
            if more:
                note = 'substituted %d by fallback rule' % len(more)
        if len(got) < n:
            shortfalls.append({'candidate': c, 'stratum': stratum, 'wanted': n, 'got': len(got)})
        for k in got:
            out.append({'source_key': k, 'stratum': stratum, 'label_group': label, 'selection_note': note})

    cls = lambda name: (lambda r: r['classification'] == name)
    cd = cls('CANONICAL_PLUS_DELTA')
    pick('CD_STRENGTH', 'CANONICAL_PLUS_DELTA', lambda r: cd(r) and r['normative_strength_equivalence'] == 'STRONGER_THAN_CANONICAL'
         and not EXC_RE.search((r.get('extra_fragment') or '') + ' ' + (r.get('exceptions') or '')), 2, cd)
    pick('CD_EXCEPTION', 'CANONICAL_PLUS_DELTA', lambda r: cd(r) and EXC_RE.search((r.get('extra_fragment') or '') + ' ' + (r.get('rationale') or '') + ' ' + (r.get('exceptions') or '')), 2, cd)
    pick('XP', 'EXTRA_PRODUCT', cls('EXTRA_PRODUCT'), 4)
    xw = cls('EXTRA_WORKFLOW')
    pick('XW_EXECUTABLE', 'EXTRA_WORKFLOW', lambda r: xw(r) and EXEC_RE.search(primary_path(r)), 2, xw)
    pick('XW_TEXT', 'EXTRA_WORKFLOW', lambda r: xw(r) and not EXEC_RE.search(primary_path(r)), 2, xw)
    pick('MX', 'MIXED', cls('MIXED'), 4)
    co = cls('CANONICAL_ONLY')
    pick('CO_WEAKER', 'CANONICAL_ONLY', lambda r: co(r) and r['normative_strength_equivalence'] == 'WEAKER_THAN_CANONICAL', 1, co)
    pick('CO_PARTIAL', 'CANONICAL_ONLY', lambda r: co(r) and r['canonical_semantic_coverage'] == 'PARTIAL' and r['normative_strength_equivalence'] == 'EQUIVALENT', 1, co)
    pick('CO_FULL', 'CANONICAL_ONLY', lambda r: co(r) and r['canonical_semantic_coverage'] == 'FULL' and r['normative_strength_equivalence'] == 'EQUIVALENT', 1, co)
    pick('NN', 'NON_NORMATIVE', cls('NON_NORMATIVE'), 2)
    pick('IA', 'INTERNAL_ARCHITECTURE', cls('INTERNAL_ARCHITECTURE'), 2)
    pick('UN_OR_BORDERLINE', 'UNCERTAIN_OR_DEFAULT_SHOULD_BORDERLINE', cls('UNCERTAIN'), 1,
         lambda r: r['normativity'] == 'NORMATIVE' and r['modality'] in ('DEFAULT', 'SHOULD') and r.get('strength_mechanical_mismatch') and r['confidence'] == 'MEDIUM')
    return out, shortfalls


def sample_m(excluded, soft_excluded):
    b = baseline('M')
    chosen = set(M_FIXED)
    out = [{'source_key': k, 'stratum': 'M_FIXED_REVISED', 'label_group': 'FIXED', 'selection_note': 'named in the task'} for k in M_FIXED]
    for stratum, pred in (('CD', lambda r: r['classification'] == 'CANONICAL_PLUS_DELTA'),
                          ('XP', lambda r: r['classification'] == 'EXTRA_PRODUCT'),
                          ('XW', lambda r: r['classification'] == 'EXTRA_WORKFLOW'),
                          ('CO_WEAKER', lambda r: r['classification'] == 'CANONICAL_ONLY' and r['normative_strength_equivalence'] == 'WEAKER_THAN_CANONICAL'),
                          ('NN', lambda r: r['classification'] == 'NON_NORMATIVE')):
        pool = [k for k, r in b.items() if k not in excluded and k not in soft_excluded and pred(r)]
        for k in take('M|' + stratum, pool, 1, chosen):
            out.append({'source_key': k, 'stratum': 'M_' + stratum, 'label_group': stratum, 'selection_note': None})
    return out


def queue_sample(excl_keys):
    q = read_jsonl(os.path.join(S2, 'STEP1_QUEUE_DISPOSITIONS.jsonl'))
    closed = [x for x in q if x['disposition'].startswith('GROUPS_CLASSIFIED')]
    out, short = [], []
    for c in CANDIDATES:
        items = [x for x in closed if x['candidate'] == c]
        chosen = set()

        def sides_differ(x):
            return len(set(x['classifications'].values())) > 1

        def pick(stratum, pred, n, fallback=None):
            pool = [x['queue_id'] for x in items if pred(x)]
            got = take('%s|Q|%s' % (c, stratum), pool, n, chosen)
            note = None
            if len(got) < n and fallback:
                more = take('%s|Q|%s|fb' % (c, stratum), [x['queue_id'] for x in items if fallback(x)], n - len(got), chosen)
                got += more
                note = 'substituted %d by fallback' % len(more)
            if len(got) < n:
                short.append({'candidate': c, 'stratum': stratum, 'wanted': n, 'got': len(got)})
            for k in got:
                out.append({'queue_id': k, 'candidate': c, 'stratum': stratum, 'selection_note': note})

        ad = lambda x: x['item_type'] == 'ATTRIBUTION_DISAGREEMENT'
        rd = lambda x: x['item_type'] == 'RELATED_BUT_DISTINCT'
        pick('ATTR_LABEL_AND_POLICY', lambda x: ad(x) and x['subtype'] == 'LABEL+POLICY_IDS', 1)
        pick('ATTR_OTHER', lambda x: ad(x) and x['subtype'] != 'LABEL+POLICY_IDS', 1)
        pick('BROAD_NARROW', lambda x: rd(x) and x['subtype'] == 'BROADER_NARROWER', 2, lambda x: rd(x) and x['subtype'] in ('DETAIL_DIFFERENCE', 'DIFFERENT_SCOPE'))
        pick('STRENGTH_SAME_LABEL', lambda x: rd(x) and x['subtype'] == 'DIFFERENT_STRENGTH' and not sides_differ(x), 1, lambda x: rd(x) and x['subtype'] == 'DIFFERENT_STRENGTH')
        pick('STRENGTH_DIFF_LABEL', lambda x: rd(x) and x['subtype'] == 'DIFFERENT_STRENGTH' and sides_differ(x), 1, lambda x: rd(x) and x['subtype'] == 'DIFFERENT_STRENGTH')
        pick('COMPOUND_PART', lambda x: rd(x) and x['subtype'] == 'COMPOUND_PART' and sides_differ(x), 1, lambda x: rd(x) and x['subtype'] == 'COMPOUND_PART')
        pick('RELATED_OTHER_DIFF_LABEL', lambda x: rd(x) and x['subtype'] in ('OVERLAP', 'EXAMPLE_GENERAL', 'DIFFERENT_LAYER') and sides_differ(x), 1)
    return out, short


def toks(s):
    return set(re.findall(r'[a-z0-9]{3,}', s.lower()))


def rel_template(p):
    return re.sub(r'^inputs/[A-Z0-9]+/output/template/', '', p)


def drift_sample():
    """Same relative file, similar claim, different label: chosen by rule, without looking at which side is right."""
    out = []
    stats = {}
    for a, b in PAIRS:
        ra, rb = baseline(a), baseline(b)
        by_path = defaultdict(list)
        for k, r in rb.items():
            by_path[rel_template(primary_path(r))].append(k)
        cands = {'MIXED': [], 'INTERNAL_ARCHITECTURE': [], 'OTHER_LABEL': []}
        compared = same = 0
        seen = set()
        for k, r in ra.items():
            ta = toks(r['claim_text'])
            best, bj = None, 0
            for k2 in by_path.get(rel_template(primary_path(r)), []):
                tb = toks(rb[k2]['claim_text'])
                j = len(ta & tb) / max(1, len(ta | tb))
                if j > bj:
                    best, bj = k2, j
            if not best or bj < 0.6 or best in seen:
                continue
            seen.add(best)
            compared += 1
            la, lb = r['classification'], rb[best]['classification']
            if la == lb:
                same += 1
                continue
            bucket = 'MIXED' if 'MIXED' in (la, lb) else 'INTERNAL_ARCHITECTURE' if 'INTERNAL_ARCHITECTURE' in (la, lb) else 'OTHER_LABEL'
            cands[bucket].append({'a': k, 'b': best, 'jaccard': round(bj, 3), 'label_a': la, 'label_b': lb})
        stats['%s~%s' % (a, b)] = {'similar_pairs_compared': compared, 'same_label': same, 'different_label': compared - same,
                                   'by_bucket': {x: len(v) for x, v in cands.items()},
                                   'note': 'Greedy similar-claim matching on the same relative file; claim wording and group boundaries differ, so this is a lead, not a count of errors.'}
        for bucket, n in (('MIXED', 4), ('INTERNAL_ARCHITECTURE', 3), ('OTHER_LABEL', 2)):
            for row in sorted(cands[bucket], key=lambda x: h('DRIFT|%s|%s|%s' % (a, b, bucket), x['a']))[:n]:
                out.append(dict(row, pair='%s~%s' % (a, b), bucket=bucket))
    return out, stats


def compute():
    n, om, unc, orp, fhd = lists()
    fam = swagger_family()
    targeted = {x['key'] for x in n} | {x['source_key'] for x in om} | {x['source_key'] for x in unc} | {x['source_key'] for x in fhd} | set(fam)
    wit = override_witnesses()
    related = {e.get('source_key') for x in orp for e in (x.get('related_evidence') or [])}
    soft = wit | related | challenged_keys()
    samples, shortfalls = {}, []
    for c in SAMPLE_CANDS:
        s, sf = sample_candidate(c, targeted, soft)
        samples[c] = s
        shortfalls += sf
    m = sample_m(targeted, soft)
    qs, qshort = queue_sample(targeted)
    drift, dstats = drift_sample()
    plan = {'audit_version': AUDIT_VERSION, 'seed': SEED,
            'method': 'Stored fields place a record in a stratum; SHA-256 of seed|candidate|stratum|source_key orders the pool. Frozen before any sampled source is opened.',
            'not_a_statistical_sample': 'Risk-enriched and non-random in the sense relevant here. It supplies no unbiased error rate.',
            'hard_exclusions': {'rule': 'records in PI-012 N, overmerge, uncertain or human-decision lists, or the Swagger UI family', 'n': len(targeted)},
            'soft_exclusions': {'rule': 'override witnesses, orphan related evidence, Step 2 challenge and calibration records; used only if a pool runs out', 'n': len(soft)},
            'strata_per_candidate': {'CD_STRENGTH': 2, 'CD_EXCEPTION': 2, 'XP': 4, 'XW_EXECUTABLE': 2, 'XW_TEXT': 2, 'MX': 4, 'CO_WEAKER': 1, 'CO_PARTIAL': 1, 'CO_FULL': 1, 'NN': 2, 'IA': 2, 'UN_OR_BORDERLINE': 1},
            'samples': samples, 'm_calibration': m, 'shortfalls': shortfalls,
            'queue_sample': qs, 'queue_shortfalls': qshort,
            'queue_strata_per_candidate': {'ATTR_LABEL_AND_POLICY': 1, 'ATTR_OTHER': 1, 'BROAD_NARROW': 2, 'STRENGTH_SAME_LABEL': 1, 'STRENGTH_DIFF_LABEL': 1, 'COMPOUND_PART': 1, 'RELATED_OTHER_DIFF_LABEL': 1},
            'drift_sample': drift, 'drift_pair_stats': dstats,
            'counts': {'per_candidate': {c: len(samples[c]) for c in SAMPLE_CANDS}, 'by_stratum': {c: dict(Counter(x['stratum'] for x in samples[c])) for c in SAMPLE_CANDS},
                       'm_calibration': len(m), 'queue': len(qs), 'queue_per_candidate': dict(Counter(x['candidate'] for x in qs)), 'drift_pairs': len(drift)}}
    return plan, (n, om, unc, orp, fhd, fam)


def build_targets(plan, parts):
    n, om, unc, orp, fhd, fam = parts
    cases = {}

    def add(case_type, c, key, member, ref=None):
        cid = {'RECORD': 'REC:', 'COVERAGE_ROW': 'COV:', 'ORPHAN_ITEM': 'ORP:', 'QUEUE_ITEM': 'QUE:'}[case_type] + key
        row = cases.setdefault(cid, {'case_id': cid, 'case_type': case_type, 'candidate': c, 'key': key, 'memberships': [], 'list_refs': {}})
        if member not in row['memberships']:
            row['memberships'].append(member)
        if ref is not None:
            row['list_refs'].setdefault(member, []).append(ref)

    for k, c in fam.items():
        add('RECORD', c, k, 'SWAGGER_A')
    for x in n:
        add('RECORD', x['candidate'], x['key'], 'PI012_N', {'first_path': x['first_path'], 'policies': x['policies'], 'classification': x['classification']})
    for x in om:
        add('RECORD', x['candidate'], x['source_key'], 'OVERMERGE', {'basis': x['basis']})
    for x in unc:
        add('RECORD', x['candidate'], x['source_key'], 'UNCERTAIN_LIST', {'reasons': x['reasons']})
        if 'UNCERTAIN_RECORD' in x['reasons']:
            add('RECORD', x['candidate'], x['source_key'], 'UNCERTAIN_RECORD')
        if 'UNCERTAIN_SUBCLAUSE' in x['reasons']:
            add('RECORD', x['candidate'], x['source_key'], 'UNCERTAIN_SUBCLAUSE')
        if 'LOW_CONFIDENCE' in x['reasons']:
            add('RECORD', x['candidate'], x['source_key'], 'LOW_CONFIDENCE')
        if 'REVIEW_NEEDED' in x['reasons']:
            add('RECORD', x['candidate'], x['source_key'], 'REVIEW_NEEDED')
    for x in fhd:
        add('RECORD', x['candidate'], x['source_key'], 'FHD', {'question': x['future_human_decision']})
    for x in orp:
        add('ORPHAN_ITEM', x['candidate'], x['item_id'], 'ORPHAN', {'item_type': x['item_type'], 'status': x.get('status')})
    for c, p in override_rows():
        add('COVERAGE_ROW', c, '%s:%s' % (c, p), 'COVERAGE_OVERRIDE')
    for c, p in SPECIAL_CELLS:
        add('COVERAGE_ROW', c, '%s:%s' % (c, p), 'STRENGTH_SPECIAL_5')
    for c, xs in plan['samples'].items():
        for x in xs:
            add('RECORD', c, x['source_key'], 'SAMPLE_D', {'stratum': x['stratum']})
    for x in plan['m_calibration']:
        add('RECORD', 'M', x['source_key'], 'M_CALIBRATION', {'stratum': x['stratum']})
    for x in plan['queue_sample']:
        add('QUEUE_ITEM', x['candidate'], x['queue_id'], 'QUEUE_E', {'stratum': x['stratum']})
    for x in plan['drift_sample']:
        ca, cb = x['pair'].split('~')
        add('RECORD', ca, x['a'], 'DRIFT_F', {'pair': x['pair'], 'bucket': x['bucket'], 'other': x['b']})
        add('RECORD', cb, x['b'], 'DRIFT_F', {'pair': x['pair'], 'bucket': x['bucket'], 'other': x['a']})
    rows = sorted(cases.values(), key=lambda r: r['case_id'])
    counts = Counter()
    for r in rows:
        for m in r['memberships']:
            counts[m] += 1
    return rows, dict(counts)


def main():
    utf8_stdout()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    plan, parts = compute()
    if cmd == 'freeze':
        if os.path.exists(out_path('SAMPLING_PLAN.json')):
            raise SystemExit('SAMPLING_PLAN.json is frozen; use check.')
        rows, counts = build_targets(plan, parts)
        plan['audit_targets_membership_counts'] = counts
        plan['audit_targets_unique_cases'] = len(rows)
        write_json('SAMPLING_PLAN.json', plan)
        write_jsonl('AUDIT_TARGETS.jsonl', rows)
        print(json.dumps(plan['counts'], indent=0))
        print('shortfalls', plan['shortfalls'], plan['queue_shortfalls'])
        print('memberships', counts, 'unique cases', len(rows))
        print(json.dumps(plan['drift_pair_stats'], indent=0))
    elif cmd == 'check':
        frozen = json.load(open(out_path('SAMPLING_PLAN.json'), encoding='utf-8'))
        same = all(frozen[k] == plan[k] for k in ('samples', 'm_calibration', 'queue_sample', 'drift_sample'))
        print('selection reproducible:', same)
        raise SystemExit(0 if same else 1)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
