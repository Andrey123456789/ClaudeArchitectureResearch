"""R22 regression: item 11.1 trigger versus delivery. Logic checks on the derivation, the sample read, and the mutation that restores the first-version defect. Dataset counts are reported in REPAIRED_VIEW_MANIFEST.json."""
import importlib.util
import re
from collections import Counter

import triggers
from rcommon import CANDIDATES, baseline, out_path
from triggers import derive


def load_sample():
    spec = importlib.util.spec_from_file_location('r22s', out_path('_rules', 'R22-111-TRIGGER', 'sample.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(ctx):
    a = derive({'trigger': 'on-demand knowledge skill swagger', 'loading_context': 'on-demand knowledge skill swagger', 'trigger_status': 'ATTRIBUTED', 'claim_text': 'When API behavior changes, open the UI.', 'classification': 'CANONICAL_ONLY', 'normativity': 'NORMATIVE'})
    ctx.check('loading context is not taken as a condition', a['applicability_status'] == 'CONDITION_IN_CLAIM_TEXT' and a['applicability_trigger'] is None and a['applicability_hint'].startswith('When API behavior changes'), a, kind='LOGIC')
    b = derive({'trigger': 'workflow verify', 'loading_context': 'workflow verify', 'trigger_status': 'ATTRIBUTED', 'claim_text': 'Build the project.', 'classification': 'CANONICAL_ONLY', 'normativity': 'NORMATIVE'})
    ctx.check('no condition found stays an explicit unknown', b['applicability_status'] == 'UNKNOWN_NOT_EXTRACTED' and b['applicability_trigger'] is None, b, kind='LOGIC')
    c = derive({'trigger': 'A change alters API behavior', 'loading_context': 'workflow verify', 'trigger_status': 'REPAIR', 'claim_text': 'x', 'classification': 'EXTRA_WORKFLOW', 'normativity': 'NORMATIVE'})
    ctx.check('a reviewed condition is kept', c['applicability_status'] == 'STATED_REVIEWED', c, kind='LOGIC')
    d = derive({'trigger': 'x', 'loading_context': 'y', 'classification': 'NON_NORMATIVE', 'normativity': 'NON_NORMATIVE'})
    ctx.check('non-normative has no condition', d['applicability_status'] == 'NOT_APPLICABLE', d, kind='LOGIC')
    ctx.check('original field is always kept', all('trigger_field_original' in x for x in (a, b, c, d)), kind='LOGIC')
    e = derive({'trigger': 'path rule: backend/**/*.cs', 'loading_context': 'rule x', 'trigger_status': 'ATTRIBUTED', 'claim_text': 'Do the thing.', 'classification': 'CANONICAL_ONLY', 'normativity': 'NORMATIVE'})
    ctx.check('a path rule is delivery, not a condition (first-version defect, found by the sample)', e['applicability_status'] == 'UNKNOWN_NOT_EXTRACTED' and e['applicability_trigger'] is None, e, kind='LOGIC')
    saved = triggers.LOADING
    triggers.LOADING = re.compile(r'(on-demand)', re.I)
    try:
        m = derive({'trigger': 'path rule: backend/**/*.cs', 'loading_context': 'rule x', 'trigger_status': 'ATTRIBUTED', 'claim_text': 'Do the thing.', 'classification': 'CANONICAL_ONLY', 'normativity': 'NORMATIVE'})
    finally:
        triggers.LOADING = saved
    ctx.check('mutation: narrowing the delivery pattern lets a path rule pass as a condition', m['applicability_status'] == 'STATED_ATTRIBUTED', m, kind='MUTATION')
    st = Counter(derive(r)['applicability_status'] for cc in CANDIDATES for r in baseline(cc).values())
    ctx.check('explicit unknowns are reported, not hidden', st['UNKNOWN_NOT_EXTRACTED'] > 0, dict(st), kind='DATA', actual=dict(st))
    ctx.check('no record has a condition cut out of its claim by pattern', not any(derive(r)['applicability_status'] == 'DERIVED_FROM_CLAIM' for cc in CANDIDATES for r in baseline(cc).values()), kind='LOGIC')
    s = load_sample().SAMPLE
    ctx.check('the sample read has 30 rows, each with a verdict and a reason', len(s) == 30 and all(x['verdict'] in ('RIGHT', 'WRONG', 'DEBATABLE') and x['why'] for x in s), Counter(x['verdict'] for x in s), kind='SEMANTIC')
    keys = {k for cc in CANDIDATES for k in baseline(cc)}
    ctx.check('sampled keys are baseline identities', all(x['key'] in keys for x in s), kind='DATA')
    ctx.check('the sample is reported as a sample, with its result', 'not a census' in open(out_path('_rules', 'R22-111-TRIGGER', 'BASELINE.md'), encoding='utf-8').read(), kind='DOC')
