"""C02: RUN-008 evidence wording in EF Core technique text. One logical rule: a measured or clearly demonstrated need, never speculative use."""
POLICIES = ['RUN-008']
REASON = 'Kit 71 C02 and kit 72: preserve RUN-008, which admits measured or clearly demonstrated need. Technique text in five candidates narrowed it to a measured profile; raw SQL lines narrowed it in all six.'
EVIDENCE = 'inventory.json RUN-008; owner lines M performance.md, M1 performance.md, L0 0-core/runtime-principles.md, L1 0-core/backend-code.md, K0 backend/csharp.md, K1 backend/runtime.md.'
F = '.claude/skills/ef-core/SKILL.md'
TABLE_OLD = '| Measured extremely hot query |'
TABLE_NEW = '| Measured or clearly demonstrated hot query |'
PATCHES = [
    ('M', F, """`EF.CompileQuery`/`EF.CompileAsyncQuery` pay off only on a measured hot
path where profiling shows compilation or cache lookup overhead is material — not
merely because a query runs frequently.""", """`EF.CompileQuery`/`EF.CompileAsyncQuery` pay off only where compilation or cache
lookup overhead is measured, or clearly demonstrated, to be material — not merely
because a query runs frequently; do not add them speculatively
(`.claude/rules/performance.md`)."""),
    ('M', F, """Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it, and prefer""", """Use raw SQL only when EF Core cannot express the query effectively or a measured
or clearly demonstrated performance need justifies it, and prefer"""),
    ('M', F, TABLE_OLD, TABLE_NEW),
    ('M1', F, """`EF.CompileQuery` / `EF.CompileAsyncQuery` fit only a measured hot path
where profiling shows compilation or cache-lookup overhead is material.""", """`EF.CompileQuery` / `EF.CompileAsyncQuery` fit only where compilation or
cache-lookup overhead is measured, or clearly demonstrated, to be material; do not
add them speculatively (`.claude/rules/performance.md`)."""),
    ('M1', F, """Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it. EF Core LINQ""", """Use raw SQL only when EF Core cannot express the query effectively or a measured
or clearly demonstrated performance need justifies it. EF Core LINQ"""),
    ('M1', F, TABLE_OLD, TABLE_NEW),
    ('L0', F, "`EF.CompileAsyncQuery` helps only on a measured hot path where compilation/cache lookup is material.", "`EF.CompileAsyncQuery` helps only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; do not add it speculatively (`0-core/runtime-principles.md`)."),
    ('L0', F, "Use raw SQL only when EF Core cannot express the query effectively or measured performance justifies it.", "Use raw SQL only when EF Core cannot express the query effectively or a measured or clearly demonstrated performance need justifies it."),
    ('L1', F, "`EF.CompileAsyncQuery` is a measured-optimization tool (backend code rule); EF Core already caches query compilation by shape, so it helps only when profiling shows compilation or cache lookup is material.", "`EF.CompileAsyncQuery` is an evidence-gated optimization tool (backend code rule); EF Core already caches query compilation by shape, so it helps only when compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; do not add it speculatively."),
    ('L1', F, "when LINQ cannot express the query effectively or measurement justifies it,", "when LINQ cannot express the query effectively or a measured or clearly demonstrated performance need justifies it,"),
    ('L1', F, TABLE_OLD.replace('|', '|'), TABLE_NEW),
    ('K0', F, "`EF.CompileQuery`/`EF.CompileAsyncQuery` belong to measured hot paths where profiling shows compilation or cache-lookup overhead matters — not to queries that merely run often.", "`EF.CompileQuery`/`EF.CompileAsyncQuery` belong where compilation or cache-lookup overhead is measured, or clearly demonstrated, to matter — not to queries that merely run often; do not add them speculatively (`rules/backend/csharp.md`)."),
    ('K0', F, "Raw SQL fits queries EF Core cannot express effectively or a measured performance need.", "Raw SQL fits queries EF Core cannot express effectively or a measured or clearly demonstrated performance need."),
    ('K0', F, TABLE_OLD, TABLE_NEW),
    ('K1', F, "Use raw SQL only when EF Core cannot express the query effectively or measured performance justifies it, and keep", "Use raw SQL only when EF Core cannot express the query effectively or a measured or clearly demonstrated performance need justifies it, and keep"),
]
