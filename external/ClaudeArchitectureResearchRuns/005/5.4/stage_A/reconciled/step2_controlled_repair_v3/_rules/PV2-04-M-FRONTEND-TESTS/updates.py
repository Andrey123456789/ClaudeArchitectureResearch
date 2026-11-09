"""PV2-04 added claim: the M frontend-test placement ban, classified as the identical peer records (M1 FG-M1-9030e201b9, K0 FG-K0-40e6fc8d29)."""
RULE = 'PV2-04-M-FRONTEND-TESTS'
UPDATES = {}
ADDED = [
    dict(source_key='V3A-M-030', candidate='M', rule=RULE, classification='CANONICAL_ONLY', modality='MUST_NOT', domain='PRODUCT_ENGINEERING',
         claim_text='Never place frontend tests under backend/.', path='.claude/skills/project-structure/SKILL.md', quote='Never place frontend tests under `backend/`.',
         canonical_coverage=[dict(policy_id='DEP-024', coverage='PARTIAL')], related_policy_ids=['DEP-024'], strength_resolution_code='PC', extra_fragment=None, extra_fragment_kind=None,
         distinguishing_scenario='A frontend spec file placed under backend/App.Web.Tests/: before PV2-04 M had no marked ban (only "the workspace holds its tests"); now it is forbidden, as in the other five.',
         trigger='Workflow project-structure, step 7: placing test projects and frontend tests.', exceptions='None.', confidence='HIGH',
         review_reading='M project-structure step 7 places Angular unit/component tests colocated and E2E tests under the workspace, then states the ban; M solution-layout.md defers frontend-test placement to this step. Same scope and marked form as the five peers.',
         review_phrases=['Never place frontend tests under `backend/`.', 'tests, when used, go under the workspace (for example `frontend/<Name>.Web/e2e/`).']),
]
