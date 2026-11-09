from jdsl import C, D, P  # noqa: F401

P("ARC-017",
  dims=["D1 repositories in one use case share the same scoped Unit of Work/DbContext",
        "D2 IUnitOfWork must not become a repository container or service locator"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts, with 'inject repositories explicitly', in each rule: M architecture.md:120-123, M1 :125-129, L0 persistence-boundary.md:28, L1 frame/boundaries.md:40, K0 architecture.md:49, K1 architecture-style.md:41.")

P("ARC-018",
  dims=["D1 no explicit transaction APIs until a concrete use case needs control beyond normal SaveChangesAsync (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M architecture.md:124-125, M1 persistence-technology.md:32-34, L0 persistence-boundary.md:29, L1 boundaries.md:41, K0 architecture.md:50, K1 persistence-technology.md:16. ef-core skills in all six add the same technique (BeginTransactionAsync inside Infrastructure; no distributed transactions).")

P("ARC-019",
  dims=["D1 EF Core is used fully inside Infrastructure and its concepts do not leak into Application",
        "D2 mechanical detection of EF Core leaking into Application"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 in each rule, including 'do not cripple repositories to keep a generic abstraction': M architecture.md:129-133, M1 persistence-technology.md:18-20, L0 persistence-boundary.md:15, L1 persistence/access.md:10, K0 architecture.md:54, K1 persistence-technology.md:14.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "L1", "K1"], ["M", "L0", "K0"]],
           "Same mechanism as ARC-008 (one source fact, counted once as RC-ENF-INNER-LAYER): L1 and K1 reject EF Core packages in Application/Domain, M1 rejects EF Core namespaces there; M, L0 and K0 have no check.",
           counterexample="Same task as ARC-008: an EF Core package or namespace in Application is flagged by M1, L1 and K1 only.",
           root="RC-ENF-INNER-LAYER",
           evidence={"L1": ["FG-L1-f0cf2d0f61"], "K1": ["FG-K1-7edee8b535"], "M1": ["FG-M1-f85a80b231"], "M": ["FG-M-d4fb000494"], "L0": ["FG-L0-4fa7724bc8"], "K0": ["FG-K0-c3538d9112"]})],
  enforcement="Source-read checker code; not executed on a shared fixture.")

P("ARC-020",
  dims=["D1 the Reserved list: changing accepted decisions, new style/pattern (Rich Domain, CQRS/mediator/VSA, event sourcing, microservices), new project/layer/reference graph, persistence boundaries or technology, infrastructure categories, major library or baseline replacement, project-wide convention (Result), auth architecture, breaking API/versioning, undefined product values",
        "D2 unclear case: any 'yes' of the five questions makes it Reserved",
        "D3 Reserved needs a Decision Request and explicit approval; headless runs implement only pre-approved named changes",
        "D4 mechanical feedback when a new project or reference-graph change appears",
        "D5 pre-execution gate on project-reference commands (dotnet add/remove reference)"],
  label="MEANINGFUL_DIVERGENCE",
  cells={c: C(note="Step 2 override: no direct owner; the Reserved list in root CLAUDE.md was read in full.") for c in ["M1", "L0", "L1", "K0", "K1"]},
  same="Read side by side in root CLAUDE.md: the same ten Reserved items and the same five-question test in M :112-134, M1 :70-98, L0 :37-51, L1 :33-36 (one paragraph), K0 :34-47, K1 :30-43; the same Decision Request and headless pre-approval paragraph in all six (M :136-147, M1 :100-110, L0 :53 + headless text, L1 :37-39, K0 :48-49, K1 :45-46). Approval exceptions are equivalent: M and K0 say 'unless already required by the specification or established structure'; M1, L0 and K1 classify such choices as Decided; L1 Decided names product sources and recorded decisions.",
  diffs=[D("D1", "NORMATIVE", "CANDIDATE_SPECIFIC_TECHNIQUE", False, [["M", "M1", "L0", "L1", "K0", "K1"]],
           "M1, L1 and K1 add 'changing a capability selection' (L1: also requires an ADR) because only these three have a capability-module mechanism; M, L0 and K0 have no such object. Architecture-specific, not a strictness difference.",
           evidence={"L1": ["FG-L1-399f7fe97a"]}),
         D("D4", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["K1"], ["M", "M1", "L0", "L1", "K0"]],
           "All six give mechanical feedback on a new project or project-reference change, at different levels: K1 actual-state.cjs:107-120 reports project additions/removals and reference edges not matched by an accepted decision in the register (check-manifests.cjs:336-379); M1 check-architecture.js:77 warns on a project outside the frame; K0 check-dependencies.cjs:148-158 gives notices; M dependency-guard.mjs:282-285, L0 claude-hook.mjs:520-524 and L1 post-change-checks.mjs:338 remind to confirm an approved decision. Only K1 compares the change against recorded approvals.",
           root="RC-ENF-RESERVED-GRAPH",
           evidence={"K1": ["FG-K1-90e374b694"], "M1": ["FG-M1-aa1d48d81a"], "K0": ["FG-K0-0e76080725"], "L0": ["FG-L0-35173bd6d4"], "L1": ["FG-L1-262cafe6e7"]}),
         D("D5", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["K1", "L0", "L1", "M1", "K0"], ["M"]],
           "PROBE-HOOK-01 (direct PreToolUse runs, inward Shop.Application->Shop.Domain and outward Shop.Application->Shop.Infrastructure): K1 blocks (exit 2) unless each edge is recorded as an accepted decision in the register (dispatch.cjs:74-81, classify-command.cjs:320); L0 blocks every reference command (claude-hook.mjs:461-462; project files are edited instead and reported after the edit); L1 returns ask (pre-shell-command.mjs:79); M1 and K0 deny until the command carries a self-written marker ('# project-reference: checked', dependency-commands.js:16/:517; '# project-references: approved', hook.cjs:19/:284); M allows and reminds afterwards (dependency-guard.mjs:282-285). The five gated candidates release the gate on different conditions (recorded approval, file edit, human answer, self-attested marker), so they are mutually incomparable; only M has no pre-execution gate. Added in Step 3 after the probe (amendment A1).",
           counterexample="Same task: the agent runs `dotnet add src/Shop.Application reference src/Shop.Infrastructure` to make a build pass. M executes it and reminds afterwards; L0 and K1 block it; M1 and K0 deny until the agent adds the marker; L1 asks the user. Live-host display of ask/deny NOT_RUN.",
           incomparable=[[a, b] for i, a in enumerate(["K1", "L0", "L1", "M1", "K0"]) for b in ["K1", "L0", "L1", "M1", "K0"][i + 1:]],
           root="RC-ENF-REFERENCE-CMD-GATE",
           evidence={"K1": ["FG-K1-69e6bb3a6a"], "L0": ["FG-L0-523f094683"], "L1": ["FG-L1-213bcfa303"], "M1": ["FG-M1-65a26a7288"], "K0": ["FG-K0-f3f3a8f451"], "M": ["FG-M-02ec6ad273"]})],
  enforcement="D4 source-read. D5 executed statically (PROBE-HOOK-01); live effect NOT_RUN.")

P("ARC-021",
  dims=["D1 constructor injection for required dependencies by default; avoid service locator and property injection"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each backend rule: M architecture.md:137-138, M1 rules/composition.md:17-18, L0 backend-layers.md:47, L1 rules/0-core/backend-code.md:41, K0 architecture.md:58, K1 rules/backend/architecture.md:19.")

P("ARC-022",
  dims=["D1 respect dependency lifetimes; never capture a shorter-lived dependency in a longer-lived service"],
  label="FULL_SEMANTIC_PARITY",
  same="Same 'never capture' rule in each backend rule: M architecture.md:139-140, M1 composition.md:19-21, L0 backend-layers.md:48, L1 backend-code.md:42, K0 architecture.md:59, K1 architecture.md:20. Stored modality MUST vs MUST_NOT is the same ban phrased two ways. dependency-injection skills in all six add the create-a-scope technique for singletons and hosted services.")

P("ARC-023",
  dims=["D1 registration stays with the owning layer: Application registers Application services, Infrastructure persistence/adapters, Api composes"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M architecture.md:141-143, M1 :138-140, L0 backend-layers.md:46, L1 boundaries.md:33, K0 architecture.md:60, K1 architecture-style.md:46. L0 fluentvalidation.md:11 places validator registration in Application's own registration, an application of the same default.")

P("ARC-024",
  dims=["D1 cache technology stays out of Domain; infrastructure cache APIs do not leak into Application without a deliberate boundary abstraction"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M architecture.md:156-157, M1 :133-134, L0 backend-layers.md:41, L1 rules/1-architecture/roles.md:30, K0 rules/backend/caching.md:13, K1 rules/backend/architecture.md:24. caching skills in all six add the same technique (HybridCache behind an Application abstraction only when a use case needs cache-aware behavior).")
