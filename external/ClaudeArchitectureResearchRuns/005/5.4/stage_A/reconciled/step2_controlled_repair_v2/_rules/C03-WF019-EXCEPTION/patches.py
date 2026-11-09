"""C03: WF-019 default and approved exception. One logical rule: the default stays, a controlled deployment-time step stays possible, and an explicit recorded exception is not made impossible."""
POLICIES = ['WF-019']
REASON = 'Kit 71 C03, kit 72, register 8.4: preserve the WF-019 default; absolute scaffolding and workflow wording must not make an explicitly authorized exception impossible; explicit exceptions need recorded scope; generic workflow approval is not one.'
EVIDENCE = 'inventory.json WF-019 ("by default"); v1 R10 line in L0 project-structure as the approved shape.'
PS = '.claude/skills/project-structure/SKILL.md'
EXC = "An exception needs the user's explicit request naming it and its scope, recorded through `architecture-decision`; a generic workflow approval is not one, and it never allows Development seeding in Production."
EXC_WRAP = """An exception needs the user's explicit request naming it and its scope, recorded
  through `architecture-decision`; a generic workflow approval is not one, and it
  never allows Development seeding in Production."""
PATCHES = [
    ('M', PS, """Development seeding implementation: `ef-core` skill. Do not add Production
credentials or Production migration automation.""", """Development seeding implementation: `ef-core` skill. Do not add Production
credentials, and do not wire automatic Production migration at normal application
startup; a separately approved, controlled deployment-time migration step belongs
to `development-workflow` § CI/CD and deployment."""),
    ('M1', PS, "Do not add Production credentials or Production migration automation.", """Do not add Production credentials, and do not wire automatic Production migration
at normal application startup; a separately approved, controlled deployment-time
migration step belongs to `verify` § Delivery Changes."""),
    ('L1', PS, "no Production credentials or Production migration automation.", "no Production credentials, and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to `development-workflow`."),
    ('K0', PS, "Add no Production credentials and no automatic production migration step (`delivery-pipeline` § 3).", "Add no Production credentials, and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to `delivery-pipeline` § 3."),
    ('K1', PS, "Never add Production credentials or Production migration automation.", "Never add Production credentials, and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to `delivery-change`."),
    ('L1', '.claude/skills/development-workflow/SKILL.md', "- Never apply production database migrations automatically from normal application startup: production migration is an explicit deployment operation using approved credentials, and Development seeding never runs in Production.", "- Do not apply production database migrations automatically from normal application startup by default: production migration is an explicit deployment operation using approved credentials, and Development seeding never runs in Production. " + EXC),
    ('M', '.claude/skills/development-workflow/SKILL.md', """  failing visibly, and deployment never runs Development seeding in Production.
  Technique: `ci-cd`, `docker`.""", """  failing visibly, and deployment never runs Development seeding in Production.
  """ + EXC_WRAP + """
  Technique: `ci-cd`, `docker`."""),
    ('M1', '.claude/skills/verify/SKILL.md', """  deployment operation that uses approved credentials, and Development seeding
  never runs in Production.
""", """  deployment operation that uses approved credentials, and Development seeding
  never runs in Production. """ + EXC_WRAP + """
"""),
    ('L0', '.claude/skills/delivery-pipeline/SKILL.md', "- Do not apply production database migrations automatically from normal application startup by default — in containers or anywhere else.\n", "- Do not apply production database migrations automatically from normal application startup by default — in containers or anywhere else. " + EXC + "\n"),
    ('K0', '.claude/skills/delivery-pipeline/SKILL.md', "- Do not apply production database migrations automatically from normal application startup by default. A production migration", "- Do not apply production database migrations automatically from normal application startup by default. " + EXC + " A production migration"),
    ('K1', '.claude/skills/delivery-change/SKILL.md', "- Production database migrations must not run automatically from normal application startup by default. A production migration", "- Production database migrations must not run automatically from normal application startup by default. " + EXC + " A production migration"),
]
