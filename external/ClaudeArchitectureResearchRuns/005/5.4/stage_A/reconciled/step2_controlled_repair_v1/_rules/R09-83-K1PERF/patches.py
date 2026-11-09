"""R09 item 8.3: K1 ef-core technique matches RUN-008: measured or clearly demonstrated need, nothing speculative."""
REASON = '8.3: compiled-query optimization justified by measurement or clearly demonstrated need; no unjustified speculative optimization'
POLICIES = ['RUN-008']
PATCHES = [
    ('K1', '.claude/skills/ef-core/SKILL.md', "`EF.CompileQuery`/`EF.CompileAsyncQuery` fit only a measured hot path where compilation/cache lookup overhead is material.",
     "`EF.CompileQuery`/`EF.CompileAsyncQuery` fit only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; do not add them speculatively (`.claude/rules/backend/runtime.md`)."),
    ('K1', '.claude/skills/ef-core/SKILL.md', "| Measured extremely hot query | Consider a compiled query |", "| Measured or clearly demonstrated hot query | Consider a compiled query |"),
]
