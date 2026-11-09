"""PV2-04 regression: M states the frontend-test placement ban in its placement owner, with the scope, authority and modality of the
five peers (kit 74 Part B PV2-04). Text and data checks; no checker in any candidate enforces placement, so the layout fixtures below are a
model of the reading, not agent behavior.
"""
import os
import shutil

from rcommon import CANDIDATES, norm_ws, out_path, read_jsonl, read_lines, wc_path
from suitelib import has, mutate_text

RULE = 'PV2-04-M-FRONTEND-TESTS'
LAYOUT = '.claude/skills/project-structure/references/solution-layout.md'
BAN = {'M': ('.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`', 'V3A-M-030'),
       'M1': (LAYOUT, 'Do not place frontend tests under `backend/`', 'FG-M1-9030e201b9'), 'L0': ('.claude/rules/3-project/layout.md', 'Never place frontend tests under `backend/`', 'FG-L0-a2e9e91e8f'),
       'L1': (LAYOUT, 'never under `backend/`', 'FG-L1-75964b0d7f'), 'K0': (LAYOUT, 'Angular tests never go under `backend/`', 'FG-K0-40e6fc8d29'), 'K1': (LAYOUT, 'Never place frontend tests under `backend/`', 'FG-K1-4767fd97b1')}
# Layouts for the placement task; the reading forbids any frontend test under backend/ and accepts tests in the workspace.
LAYOUTS = [('frontend/App.Web/src/app/orders/order-list.component.spec.ts', 'ACCEPTABLE'), ('frontend/App.Web/e2e/orders.spec.ts', 'ACCEPTABLE'),
           ('backend/App.Web.Tests/order-list.component.spec.ts', 'FORBIDDEN'), ('backend/App.Api/ClientApp/e2e/orders.spec.ts', 'FORBIDDEN'),
           ('backend/App.Application.Tests/OrderServiceTests.cs', 'NOT_FRONTEND')]


def verdict(c, path, root=None):
    """Model of the placement reading: a frontend test under backend/ is forbidden when the candidate's owner states the ban."""
    rel, phrase, _ = BAN[c]
    if not path.endswith(('.ts', '.js')):
        return 'NOT_FRONTEND'
    stated = has(c, rel, phrase, root)
    if path.startswith('backend/'):
        return 'FORBIDDEN' if stated else 'NOT_STATED'
    return 'ACCEPTABLE'


def run(ctx):
    by = {r['source_key']: r for r in read_jsonl(out_path('REPAIRED_CLASSIFICATIONS.jsonl'))}
    for c, (rel, phrase, key) in BAN.items():
        ctx.check('the marked ban stands in the placement owner', has(c, rel, phrase), phrase, c, 'SOURCE')
        r = by.get(key)
        ctx.check('the ban is stored MUST_NOT, linked to DEP-024, with a resolution for the DEFAULT tag', r is not None and r['modality'] == 'MUST_NOT' and any(x['policy_id'] == 'DEP-024' for x in r.get('canonical_coverage') or []) and (r.get('strength_resolution') or {}).get('code') in ('PC', 'SL'),
                  r and (r['modality'], r.get('canonical_coverage'), r.get('strength_resolution')), c, 'DATA')
        for path, want in LAYOUTS:
            got = verdict(c, path)
            ctx.check('same placement task: %s -> %s' % (path, want), got == want, got, c, 'MODEL', want, got)
    ctx.check('M: the layout reference still names step 7 as the placement owner', has('M', LAYOUT, 'Frontend test placement: `project-structure` step 7.'), candidate='M', kind='SOURCE')
    ctx.check('M: no other layout mandate came with the ban (step 7 otherwise unchanged)', has('M', '.claude/skills/project-structure/SKILL.md', 'tests, when used, go under the workspace (for example `frontend/<Name>.Web/e2e/`). Never place frontend tests under `backend/`.') and not has('M', '.claude/skills/project-structure/SKILL.md', 'must be colocated'), candidate='M', kind='SOURCE')
    n = sum(1 for c in CANDIDATES for rel in [BAN[c][0]] if 'backend/`' in norm_ws(' '.join(read_lines(wc_path(c, rel)))))
    ctx.check('six of six candidates carry the ban', n == 6, n, kind='SOURCE', actual=n)
    m = mutate_text('M', '.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`.', '')
    got = verdict('M', 'backend/App.Web.Tests/order-list.component.spec.ts', m) if m else 'n/a'
    ctx.check('mutation: the M sentence removed is caught (the placement is no longer forbidden)', got == 'NOT_STATED', got, 'M', 'MUTATION', 'NOT_STATED', got)
    if m:
        shutil.rmtree(m, ignore_errors=True)
    ctx.not_run('a checker that blocks a frontend test under backend/', 'no candidate has one; the duty is text in all six', None)
    ctx.not_run('a live agent placing frontend tests', 'no live agent ran', None)
