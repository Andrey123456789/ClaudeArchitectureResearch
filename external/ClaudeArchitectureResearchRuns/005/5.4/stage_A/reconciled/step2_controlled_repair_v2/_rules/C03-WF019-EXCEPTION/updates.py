"""C03 claim updates and one new claim per candidate. Each reworded record was read against the current source; its original claim stays in the view."""
RULE = 'C03-WF019-EXCEPTION'
CANDS = ['M', 'M1', 'L0', 'L1', 'K0', 'K1']
UPDATES = {}
ADDED = []


def up(keys, claim, note, sets=None):
    for k in keys:
        UPDATES[k] = dict(rule=RULE, status='REWORDED', claim=claim, note=note, set=sets or {}, sub={})


SCAFFOLD = 'While scaffolding, add no Production credentials and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to the delivery workflow.'
NOTE = 'C03: the scaffolding line no longer bars a controlled deployment-time step that WF-019 allows.'
up(['FG-M-23da897cc0', 'FG-M1-343e5ecb92', 'FG-L1-1a1aed2f8e'], SCAFFOLD, NOTE)
up(['FG-K0-ff0df68f54'], 'Configure the Development database and seeding entry point; add no Production credentials and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to delivery-pipeline.', NOTE)
up(['FG-K1-c6b74416d4'], 'Development persistence via persistence-change; never add Production credentials and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to delivery-change.', NOTE)
up(['FG-L1-a9fb9c9a62'], 'Do not apply production migrations automatically from normal application startup by default; production migration is an explicit deployment operation with approved credentials.', 'C03: the source now says "by default", so the stronger delta this record held is gone.', dict(classification='CANONICAL_ONLY', oracle_relation='FULLY_ENTAILED', strength_vs_canonical='SAME', strength_resolution_code=None, extra_fragment=None, extra_fragment_kind=None, distinguishing_scenario=None))

OWNER = {'M': '.claude/skills/development-workflow/SKILL.md', 'M1': '.claude/skills/verify/SKILL.md', 'L0': '.claude/skills/delivery-pipeline/SKILL.md', 'L1': '.claude/skills/development-workflow/SKILL.md', 'K0': '.claude/skills/delivery-pipeline/SKILL.md', 'K1': '.claude/skills/delivery-change/SKILL.md'}
for c in CANDS:
    ADDED.append(dict(source_key='REP-%s-011' % c, candidate=c, rule=RULE, claim_text="An exception to the Production startup-migration default needs the user's explicit request naming it and its scope, recorded through architecture-decision; a generic workflow approval is not one, and it never allows Development seeding in Production.", classification='CANONICAL_PLUS_DELTA', modality='REQUIRES_APPROVAL', path=OWNER[c], quote="An exception needs the user's explicit request naming it and its scope", domain='WORKFLOW_ENFORCEMENT', canonical_coverage=[dict(policy_id='WF-019', coverage='PARTIAL')], related_policy_ids=['WF-019', 'GOV-017', 'PST-004'], extra_fragment='What an exception to the default needs, and what it never allows.', extra_fragment_kind='EXTRA_WORKFLOW', distinguishing_scenario='A generic approved workflow meets a startup migration: WF-019 says "by default" and names no route; this line refuses it.', trigger='Someone proposes automatic Production migration at normal application startup.', exceptions='None.', confidence='HIGH'))
