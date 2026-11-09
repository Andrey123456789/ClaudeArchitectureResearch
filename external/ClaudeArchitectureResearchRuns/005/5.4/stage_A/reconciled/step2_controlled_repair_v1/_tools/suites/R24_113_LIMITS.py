"""R24 regression: item 11.3 limits stated."""
from rcommon import out_path


def run(ctx):
    t = open(out_path('EVIDENCE_LIMITS.md'), encoding='utf-8').read()
    for phrase in ('Same-family reviewer', 'Targeted sampling', 'Runtime NOT_RUN', 'not an unbiased error rate', 'self-audit'):
        ctx.check('limit stated: %s' % phrase, phrase in t, kind='DOC')
