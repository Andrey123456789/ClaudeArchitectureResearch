from jdsl import C, D, P  # noqa: F401

_FIVE = [["K1", "L0", "L1", "M1", "K0"]]

P("GOV-017",
  dims=["D1 classify every decision as Decided, Delegated or Reserved; Decided is followed and not reopened without approval; Delegated is decided without asking",
        "D2 Reserved changes need explicit approval through a Decision Request; an unclear case with any 'yes' to the five questions is Reserved",
        "D3 headless/autonomous runs implement only a Reserved change the user approved beforehand by name and scope; they never make a new Reserved decision",
        "D4 mechanical feedback when a Reserved change (project or reference-graph change) appears",
        "D5 pre-execution gate on project-reference commands"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1-D3 read side by side in each root CLAUDE.md (always loaded): the three classes, the five-question test and the approval exceptions in M :100-134, M1 :65-98, L0 :35-51, L1 :33-36, K0 :34-48, K1 :28-43; the headless pre-approval paragraph (approved decision HQ-04: approval names the change and its scope, a broad or vague instruction is not approval, never make a new Reserved decision headless) in M :136-147, M1 :100-110, L0 :53-55, L1 :37-39, K0 :48-49, K1 :45-46; each architecture-decision skill carries the Decision Request procedure. The decision protocol is the same text as ARC-020 D1-D3, where the side-by-side reading is recorded.",
  diffs=[D("D4", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["K1"], ["M", "M1", "L0", "L1", "K0"]],
           "Same source fact as ARC-020 D4 (root counted once): all six give some mechanical feedback on a project or reference-graph change; only K1 compares it with accepted decisions in the register (actual-state.cjs:107-120, check-manifests.cjs:336-379). M1 check-architecture.js:77 warns on a project outside the frame; L0 claude-hook.mjs:520-524 reminds to confirm an approved decision; M, L1 and K0 remind or give notices.",
           root="RC-ENF-RESERVED-GRAPH",
           evidence={"K1": ["FG-K1-90e374b694"], "M1": ["FG-M1-aa1d48d81a"], "L0": ["FG-L0-35173bd6d4"], "K0": ["FG-K0-0e76080725"], "L1": ["FG-L1-262cafe6e7"]}),
         D("D5", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, _FIVE + [["M"]],
           "Same source fact as ARC-020 D5 (root counted once; PROBE-HOOK-01): before a `dotnet add/remove reference` runs, K1 blocks unless the edge is an accepted decision, L0 blocks every reference command, L1 asks the user, M1 and K0 deny until a self-written marker is added, M allows and reminds afterwards. The five gated candidates release on different conditions, so they are mutually incomparable. The dependency-command gate, which also bears on Reserved question 1, is scored once at DEP-004 (RC-ENF-DEP-INSTALL-GATE).",
           counterexample="Same task as ARC-020: in a headless run the agent decides to add an outward reference to make a build pass. M executes the command; L0 and K1 block it; L1 asks (headless handling of ask NOT_RUN, Q-08); M1 and K0 deny until the agent adds the marker, which a headless agent can add without any approval.",
           incomparable=[[a, b] for i, a in enumerate(_FIVE[0]) for b in _FIVE[0][i + 1:]],
           root="RC-ENF-REFERENCE-CMD-GATE",
           evidence={"K1": ["FG-K1-69e6bb3a6a"], "L0": ["FG-L0-523f094683"], "L1": ["FG-L1-213bcfa303"], "M1": ["FG-M1-65a26a7288"], "K0": ["FG-K0-f3f3a8f451"], "M": ["FG-M-02ec6ad273"]})],
  enforcement="D4 source-read; D5 executed statically (PROBE-HOOK-01); live host and headless behavior NOT_RUN.",
  challenge="GOV-017 and ARC-020 share their text and both enforcement roots; the per-policy labels both count, the root-cause summary counts each root once. Sensitivity: if the shared-research invariant is scored on text only (enforcement attributed to ARC-020), GOV-017 becomes FULL_SEMANTIC_PARITY.")

P("GOV-018",
  dims=["D1 before implementing a questionable request, name the concrete concern and propose an alternative; never silently rewrite or ignore the requirement"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST with the same concern list (duplication, cohesion, trigger/loading, context cost, architecture or policy conflict, unnecessary complexity) in each always-loaded root CLAUDE.md: M :69-73, M1 :57-61, L0 :59, L1 :43, K0 :30, K1 :53; development-workflow skills in all six repeat it as a step.")
