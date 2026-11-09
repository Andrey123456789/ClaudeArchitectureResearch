"""R20: item 9.2 K0 deserialization line read as a security-audit criterion. No template change, no SEC-003 obligation invented."""
from rcommon import input_path, sha256_file, wc_path
from suitelib2 import anchors, check_overlay, overlay_of


def run(ctx):
    f = '.claude/skills/security-scan/references/scan-layers.md'
    ctx.check('K0 scan layers untouched', sha256_file(wc_path('K0', f)) == sha256_file(input_path('K0', f)), candidate='K0', kind='SOURCE')
    anchors(ctx, 'line kept in the risk register', {'K0': (f, ['Investigate polymorphic or type-driven deserialization', 'Untrusted payloads are not deserialized into arbitrary runtime types'])})
    check_overlay(ctx, 'R20-92-K0DESER')
    rows = overlay_of('R20-92-K0DESER')
    ctx.check('no canonical SEC-003 link and no MUST_NOT left on these records', all(r['set']['canonical_coverage'] == [] and r['set']['modality'] == 'DEFAULT' and r['set']['classification'] == 'EXTRA_WORKFLOW' for r in rows), kind='SEMANTIC')
    ctx.check('both K0 records covered', {r['key'] for r in rows} == {'FG-K0-0ef1e5ed3d', 'FG-K0-6d06b21a93'}, kind='DATA')
