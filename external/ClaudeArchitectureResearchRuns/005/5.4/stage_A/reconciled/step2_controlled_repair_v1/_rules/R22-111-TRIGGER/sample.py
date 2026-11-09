"""R22 sample read: 30 records drawn by sha256('R22|'+key), first n per status on the final derivation. Verdicts were written after reading the claim, the original field and the derived status."""


def row(key, status, verdict, why):
    return dict(key=key, status=status, verdict=verdict, why=why)


SAMPLE = [
    row('FG-K0-789f0cb53c', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Path scope is delivery. The preference has no further condition.'),
    row('FG-M-01e6acb472', 'UNKNOWN_NOT_EXTRACTED', 'DEBATABLE', 'The parenthesis of the original field says security scans, which is the real scope. Not extracted.'),
    row('FG-L0-becec9a45b', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Knowledge skill is delivery. The prohibition carries its own limit.'),
    row('FG-K0-410f61c99d', 'UNKNOWN_NOT_EXTRACTED', 'DEBATABLE', 'The parenthesis says new applications, which is the real scope. Not extracted.'),
    row('FG-K0-98882cd099', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Path scope is delivery. The exception sits in the claim.'),
    row('FG-K1-aad27ece18', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Always loaded is delivery. The rule has no narrower condition.'),
    row('FG-K1-7b25a82078', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Always loaded is delivery. The exception sits in the claim.'),
    row('FG-L0-ba8d472dd2', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Workflow is delivery. The subject, container deployments, states the scope.'),
    row('FG-M-0daac01a33', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'When it fits is a hedge at the end, not a trigger.'),
    row('FG-K1-c40b3bda32', 'UNKNOWN_NOT_EXTRACTED', 'RIGHT', 'Knowledge skill is delivery. No opening condition.'),
    row('FG-K1-490b095852', 'STATED_ATTRIBUTED', 'RIGHT', 'Git commits is when the preference applies.'),
    row('FG-L1-8118404735', 'STATED_ATTRIBUTED', 'DEBATABLE', 'Api names a project role, a scope more than a condition.'),
    row('FG-M1-61eb1f085c', 'STATED_ATTRIBUTED', 'RIGHT', 'Build and test repair is when it applies.'),
    row('FG-M-b3e431a714', 'STATED_ATTRIBUTED', 'RIGHT', 'Seed data co-change is when it applies.'),
    row('FG-K0-945547507f', 'STATED_ATTRIBUTED', 'DEBATABLE', 'Names hook inputs. The real condition, a removed manifest, is in the claim.'),
    row('FG-K0-dad12ced24', 'STATED_ATTRIBUTED', 'RIGHT', 'Approved decisions is when it applies.'),
    row('FG-K0-1f1751695b', 'STATED_ATTRIBUTED', 'RIGHT', 'Code review is when it applies.'),
    row('FG-L0-9254dcc973', 'STATED_ATTRIBUTED', 'RIGHT', 'Build and test repair is when it applies.'),
    row('FG-L1-2fa62cb6ff', 'STATED_ATTRIBUTED', 'RIGHT', 'Completion and repair reports is when it applies.'),
    row('FG-M1-c42e6916ba', 'STATED_ATTRIBUTED', 'RIGHT', 'Template content placement is when it applies.'),
    row('FG-L0-18eacd2f3a', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'Opens with After editing. The field names hook events.'),
    row('FG-L0-49eef9847f', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'Opens with a When clause. The hint stops inside the list.'),
    row('FG-K1-5b25bc3b2f', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'For frontend changes is the condition. The hint overruns it.'),
    row('FG-L0-be8fb97b36', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'After a framework upgrade is the condition. The hint overruns it.'),
    row('FG-M-59e187024c', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'Opens with a Whenever clause.'),
    row('FG-M1-542fabeb97', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'Before scanning is the condition. The hint overruns it.'),
    row('FG-L0-fe665ffb2e', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'Opens with a When clause. The hint overruns it.'),
    row('FG-K0-2d70f4fa42', 'CONDITION_IN_CLAIM_TEXT', 'RIGHT', 'Opens with a When clause. The hint overruns it.'),
    row('FG-L1-a73c9ece78', 'STATED_REVIEWED', 'RIGHT', 'Every Bash or PowerShell call is when the hook fires.'),
    row('FG-K1-9c41106afd', 'STATED_REVIEWED', 'RIGHT', 'Asynchronous startup is when the rule applies.'),
]
