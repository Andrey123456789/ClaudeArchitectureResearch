"""PV2-04 patch: M project-structure step 7 states the frontend-test placement ban the other five already state."""
REASON = 'PV2-04 (approved): add to M the explicit ban on placing frontend tests under backend/, in its owner of frontend-test placement (project-structure step 7).'
POLICIES = ['DEP-024']
EVIDENCE = 'M1, L0, L1, K0 and K1 state the ban in their layout owner and store it MUST_NOT; M had no marked ban (v2 C07 FINDING).'
SKILL = '.claude/skills/project-structure/SKILL.md'
PATCHES = [
    ('M', SKILL,
     """colocated with the code they test, following current Angular conventions; E2E
tests, when used, go under the workspace (for example `frontend/<Name>.Web/e2e/`).
""",
     """colocated with the code they test, following current Angular conventions; E2E
tests, when used, go under the workspace (for example `frontend/<Name>.Web/e2e/`).
Never place frontend tests under `backend/`.
"""),
]
