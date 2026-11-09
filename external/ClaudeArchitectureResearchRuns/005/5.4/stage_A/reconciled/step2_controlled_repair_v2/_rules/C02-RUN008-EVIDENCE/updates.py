"""C02 claim updates: records whose own claim stated the narrowed reading. Modality, label and policy links stay; RUN-008 is DEFAULT, and these lines stay DEFAULT."""
RULE = 'C02-RUN008-EVIDENCE'
NOTE = 'C02: the source now admits a measured or clearly demonstrated need, as RUN-008 does.'
UPDATES = {}


def up(key, claim):
    UPDATES[key] = dict(rule=RULE, status='REWORDED', claim=claim, note=NOTE, set={}, sub={})


up('FG-M-e2cfa4d43d', 'Normal LINQ is default; compiled queries only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material, not merely because a query runs frequently; not speculatively.')
up('FG-M-9882974f66', 'Use raw SQL only when EF cannot express the query effectively or a measured or clearly demonstrated performance need justifies it; prefer parameterization-preserving APIs (FromSql, FromSqlInterpolated, SqlQuery); avoid raw SQL merely to appear performant.')
up('FG-M1-b46ff1246e', 'Normal LINQ by default; compiled queries only where compilation or cache-lookup overhead is measured, or clearly demonstrated, to be material; no compiled queries or raw SQL without evidence.')
up('FG-M1-c824e41d5d', 'Raw SQL only when EF cannot express the query effectively or a measured or clearly demonstrated performance need justifies it.')
up('FG-L0-6d400bcdbc', 'EF.CompileAsyncQuery only where compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; not speculatively.')
up('FG-L0-61849fa4be', 'Use raw SQL only when EF Core cannot express the query effectively or a measured or clearly demonstrated performance need justifies it.')
up('FG-L1-57c9fda618', 'EF.CompileAsyncQuery is an evidence-gated optimization tool, helpful only when compilation or cache lookup overhead is measured, or clearly demonstrated, to be material; not speculatively.')
up('FG-L1-224f34f214', 'Raw SQL only when LINQ cannot express the query effectively or a measured or clearly demonstrated performance need justifies it.')
up('FG-K0-4622d88e39', 'Normal LINQ is the default; compiled queries belong where compilation or cache-lookup overhead is measured, or clearly demonstrated, to matter, not to queries that merely run often; not speculatively.')
up('FG-K0-f14c8d2c42', 'Compiled queries belong where compilation or cache-lookup overhead is measured, or clearly demonstrated, to matter.')
up('FG-K0-4007e28c14', 'Raw SQL fits queries EF Core cannot express effectively or a measured or clearly demonstrated performance need.')
up('FG-K1-74de609c68', 'Raw SQL only when EF Core cannot express the query effectively or a measured or clearly demonstrated performance need justifies it.')
