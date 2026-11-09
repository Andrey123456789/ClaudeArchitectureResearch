from jdsl import C, D, P  # noqa: F401

P("GOV-015",
  dims=["D1 no repository-changing Git operation unless the user explicitly requested it or pre-approved it with a named operation and scope (generic workflow approval is not authority)",
        "D2 an explicit request to rewrite a named branch, including main, is valid unless another policy forbids it (HQ-01 approved variation)",
        "D3 hook-level gating of repository-changing Git commands (PV2-01: ask, read-only Git allowed, existing deny wins)"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="The Git section is the same text in root CLAUDE.md of all six (read in full): M :150-169, M1 :113-136, L0 :66-73, L1 :52-57, K0 :52-57, K1 :56-61 — the same verb list, the named-operation-and-scope pre-approval, 'a generic approved workflow ... is not that authority', the named-branch rewrite clause, the task-start check and the destructive-operation re-check. git-workflow skills in all six restate the high-risk list and the authority re-check. Static hook outcomes (inherited v3 SAME_TASK_MATRIX_V3 'git', direct script runs) are identical for all ten fixtures: ask for commit, -c/-C option forms, bash -c clean, chained commit, reset --hard and force-push; allow for status and log; a peer-bypass install chained with a commit is denied/blocked in all six (existing deny wins).",
  diffs=[D("D3", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["K0"], ["M", "M1", "L0", "L1", "K1"]],
           "Q-04: K0 classifies the first recognized tool anywhere in a segment, so it also asks for 'git' after an unrecognized leading word (echo git commit -m x); the other five parse the command position and allow it. An extra prompt in K0, never a missed mutation in the v3 fixtures.",
           root="RC-ENF-GIT-Q04", evidence={"K0": ["FG-K0-3a0bdc2375"], "M": ["V3A-M-010"], "M1": ["V3A-M1-010"], "L0": ["V3A-L0-010"], "L1": ["V3A-L1-010"], "K1": ["V3A-K1-010"]})],
  enforcement="Static: same ask/allow/deny on the v3 fixture matrix in all six (PV2-01). Live host: NOT_RUN — how ask is shown and answered, and what a headless run does when it meets ask (Q-08). Git run indirectly by a script or alias is classified by no candidate.",
  notes="An ask is not authorization in any of the six (git-workflow skills and hook reasons say so; HQ-01/GOV-015 preserved).")

P("GOV-016",
  dims=["D1 parallel implementation work uses separate branches or worktrees; keep unrelated changes out of the current branch"],
  label="FULL_SEMANTIC_PARITY",
  same="Verbatim the same bullet in root CLAUDE.md of all six (M :168-169, M1 :135-136, L0 :73, L1 :57, K0 :57, K1 :61), read in the Git sections above. git-workflow skills add worktree hygiene (one branch per normal worktree in M1, L0) that Git itself enforces; no hook in any.")

P("GOV-019",
  dims=["D1 never discard, overwrite, reset, clean or otherwise destroy user work to make a Git operation easier"],
  label="FULL_SEMANTIC_PARITY",
  same="Same git-workflow bullet in all six (M :29-30, M1 :27-28, L0 :22, L1 :20, K0 :20, K1 :23). L1 and K1 add 'stash away' to the bullet; the other four forbid automatic stash in the task-start step (M :23, M1 :18, L0 :18, K0 :16) and before merge/rebase (M :96, M1 :97, L0 :43, K0 :69), so stashing user work to ease an operation is forbidden in all six. Same skill-level delivery.")

P("GOV-020",
  dims=["D1 before a repository-changing Git operation, inspect relevant state and use the minimum operation",
        "D2 do not silently clean unrelated working-tree changes"],
  label="FULL_SEMANTIC_PARITY",
  same="Same git-workflow bullet in all six: M :31-33, M1 :38-39 (with the authority re-check at :114-115), L0 :23, L1 :21 (also names current branch and upstream), K0 :21, K1 :24. All six add the immediate pre-execution re-check of destructive operations (what will be lost or rewritten).")

P("GOV-021",
  dims=["D1 when an approved CUSTOM_SETTINGS.md value changes, identify and update every affected implementation, validation, configuration, test, documentation and mirrored surface",
        "D2 search for stale references and run normal verification",
        "D3 changing one literal alone does not establish synchronization"],
  label="FULL_SEMANTIC_PARITY",
  cells={"K0": C(owners=["FG-K0-d114883838", "FG-K0-7c20970193"], note="Step 2 override: no direct owner; custom-settings:24, :37-42 and :44 state D1-D3."),
         "K1": C(owners=["FG-K1-406d298b6a", "FG-K1-956744f41c"], note="Step 2 override: no direct owner; custom-settings:28 and :40 state D1-D2; D3 is entailed by 'find every affected surface' and the completion checks, without the literal sentence.")},
  same="All six route the duty from root CLAUDE.md ('then synchronize it (custom-settings)': M :51-55, M1 :36-39, L0 :30, L1 :22, K0 :22, K1 :22) to a custom-settings skill with the same surface list, a stale-reference search and build/test verification (M :33-50/:73-78, M1 :33-43/:63-70, L0 :23-25/:38-42, L1 :23-32/:42-47, K0 :18-24/:37-44, K1 :26-28/:40). The one-literal sentence appears in M :35, M1 :72, L0 :25, L1 :23, K0 :44; K1 states the full procedure instead. Every candidate also reminds on CUSTOM_SETTINGS.md edits (hook or checker), which does not verify synchronization.")
