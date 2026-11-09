# XC04 X0181-X0240 (DEP-012..DEP-026, FE, GOV-003..005). Analyst: Step 3.
_FC = ("Fail-closed PreToolUse handling of unreadable/malformed input: approved decision PV2-02 covers M and M1 (v3 review PV2-02-FAILCLOSED-INPUT holds); L0, L1, K0 and K1 fail closed by their own design "
       "(M dependency-guard.mjs:364 + settings onFailure block, M1 pre-tool-use.js:30-40, L0 claude-hook.mjs:46-61, L1 pre-shell-command.mjs:241-249, "
       "K0 hook.cjs:2-9 (X0142), K1 dispatch.cjs:5-12 (X0146)). M1's registrations carry no timeout (host default, NOT_RUN).")

A(["X0181-X0189", "X0192-X0198", "X0200-X0202", "X0204", "X0205", "X0207-X0221", "X0223", "X0224", "X0230", "X0232-X0239"])
X("X0190", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "NgModule exception restates canonical FE-001 (FULL in P1).", task="none")
X("X0191", "SAME_NORM_DIFFERENT_PACKAGING", "Frontend test locations (colocated unit tests, e2e/ inside the workspace) are part of the layout description in all six (DEP-024 D1; X0192 shows M1, L0, L1 copies).", task="none")
X("X0199", "SAME_NORM_DIFFERENT_PACKAGING", "Same .dockerignore list and 'do not exclude tests the image build runs or files restore/build needs' in all six docker skills (M :136-151, M1 :124-139 read; L0, L1, K0, K1 here).", task="none")
X("X0203", "SAME_NORM_DIFFERENT_PACKAGING", "Environment configuration stays external: L0 containers-ci path rule; docker skills of M1, K0, K1 (X0194) and M, L1 (docker skills) state the same.", task="none")
X("X0206", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Direct Polly as a documented exception: canonical DEP-020 (FULL in P1).", task="none")
X("X0222", "SAME_NORM_DIFFERENT_PACKAGING", "Copy only existing repository build files restore needs: M/K0 X0217, K1 X0219, L0 X0195, L1 here; M1 docker skill has the same Dockerfile section.", task="none")
X("X0225", "SAME_NORM_DIFFERENT_PACKAGING", _FC + " Not identical at the edges: a blank command (valid JSON, empty string) is allowed by L0, K0, K1 and blocked by M, M1, L1 (Q-02); event/tool mismatches are handled differently (Q-03). Neither executes anything.", task="none: all six block unreadable or malformed PreToolUse input; the blank-command edge (Q-02) runs nothing", links=["PV2-02", "Q-02", "Q-03"])
X("X0226", "SAME_NORM_DIFFERENT_PACKAGING", _FC, task="none", links=["PV2-02"])
X("X0227", "SAME_NORM_DIFFERENT_PACKAGING", _FC, task="none", links=["PV2-02"])
X("X0228", "SAME_NORM_DIFFERENT_PACKAGING", _FC, task="none", links=["PV2-02"])
X("X0229", "SAME_NORM_DIFFERENT_PACKAGING", _FC, task="none", links=["PV2-02"])
X("X0231", "SAME_NORM_DIFFERENT_PACKAGING", "Scaffold verification inspects project references with the candidate's checker and the final tree in all six project-structure skills (e.g. K1 SKILL.md:41, M :119-125).", task="none")
X("X0240", "SAME_NORM_DIFFERENT_PACKAGING", "Five-question test (including 'removes a dependency') is in every root CLAUDE.md (GOV-017 D2, FULL text).", task="none")
