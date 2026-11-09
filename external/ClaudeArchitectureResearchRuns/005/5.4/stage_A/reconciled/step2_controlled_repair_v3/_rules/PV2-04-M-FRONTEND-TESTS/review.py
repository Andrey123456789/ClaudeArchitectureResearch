"""PV2-04 source review on current v3 bytes: DEP-024 (separation of backend, frontend workspace, documentation) in M, with the five peers read side by side."""
REVIEW = [
    dict(policy='DEP-024', candidate='M', verdict='HOLDS', quotes=[('.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`.'), ('.claude/skills/project-structure/references/solution-layout.md', 'Frontend test placement: `project-structure` step 7.'), ('CLAUDE.md', 'holds the Angular workspace including its tests')],
         note='DEP-024 keeps backend, frontend workspace and documentation separated (DEFAULT). M now states the marked ban in the step its layout reference names as the owner of frontend-test placement, with the same scope as M1, L0, L1, K0 and K1. No other layout mandate was added.',
         counterexample='A frontend test file under backend/<Name>.Web.Tests/: before PV2-04 M forbade it only implicitly (CLAUDE.md: the workspace holds its tests); now explicitly, as the five peers do.'),
]
