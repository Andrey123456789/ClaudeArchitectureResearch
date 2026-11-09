"""Source anchors and record checks for no-change and classification-only rules."""
import importlib.util
import os

from rcommon import CANDIDATES, baseline, out_path
from suitelib import has


def anchors(ctx, name, table):
    """table: {candidate: (rel, [phrases])}. Each phrase must stand in the current working copy."""
    for c, (rel, phrases) in table.items():
        miss = [p for p in phrases if not has(c, rel, p)]
        ctx.check('%s: source anchor present' % name, not miss, 'missing=%s' % miss, c, 'SOURCE')


def overlay_of(rule):
    p = out_path('_rules', rule, 'overlay.py')
    spec = importlib.util.spec_from_file_location('ov_' + rule.replace('-', '_'), p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.OVERLAY


def check_overlay(ctx, rule):
    rows = overlay_of(rule)
    all_keys = {c: baseline(c) for c in CANDIDATES}
    bad = []
    for r in rows:
        base = r['key'].split('/')[0]
        if not any(base in all_keys[c] for c in CANDIDATES) or not r.get('reading') or not r.get('quote'):
            bad.append(r['key'])
    ctx.check('overlay rows resolve and carry a reading and a quote', not bad, str(bad[:5]), kind='DATA', actual=len(rows))
