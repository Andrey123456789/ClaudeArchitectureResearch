"""R12 item 8.7: K1 persistence-change step 5 no longer makes a local database change a duty of its own. Everything else stays."""
REASON = '8.7 K1 local migrations: remove the standalone mandatory local database mutation, keep migration creation and review, schema before seed, validation'
POLICIES = ['PST-005', 'PST-006', 'PST-009', 'PST-010']
PATCHES = [
    ('K1', '.claude/skills/persistence-change/SKILL.md', "5. Apply locally (`dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`), or drop and recreate the local database when a fresh dataset is needed.",
     "5. When this work runs against a local database, apply the migration there before any seeding (`dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`), or drop and recreate it when a fresh dataset is needed. Changing the local database is not a goal of its own."),
]
