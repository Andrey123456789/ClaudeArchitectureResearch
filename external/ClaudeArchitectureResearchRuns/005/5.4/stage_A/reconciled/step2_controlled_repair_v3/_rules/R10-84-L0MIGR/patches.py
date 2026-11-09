"""R10 item 8.4: L0 scaffold line aligned with WF-019. Credentials ban and no-Development-seeding unchanged."""
REASON = '8.4: no automatic Production migration at normal startup by default; separately approved controlled deployment-time steps remain possible'
POLICIES = ['WF-019', 'SEC-001']
PATCHES = [
    ('L0', '.claude/skills/project-structure/SKILL.md', "Never add Production credentials or Production migration automation.",
     "Never add Production credentials, and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to `delivery-pipeline`."),
]
