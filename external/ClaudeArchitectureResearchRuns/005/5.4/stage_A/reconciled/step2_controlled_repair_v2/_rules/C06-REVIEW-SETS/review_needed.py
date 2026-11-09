"""The 62 v1 review_needed records, each read on current source. Status: CONFIRMED, CORRECTED, QUALIFIED, UNRESOLVED, NOT_VERIFIED.

CONFIRMED, CORRECTED and QUALIFIED clear the flag: the question it asked now has an answer on the record. NOT_VERIFIED and UNRESOLVED keep the flag and state what is still open.
`test` names the executed check in the C06 suite. Where the only open part is how the host applies a hook decision, the script's behavior ran here and the host's did not.
"""
HOST = 'The script behavior ran directly in the C06 suite. How the host applies the decision (onFailure, exit code, block) did not run: no live host here.'
READ = 'Read on current source.'


def r(key, status, reason, test=None):
    return dict(key=key, status=status, reason=reason, test=test)


ROWS = [
    r('FG-M-f268d4b313', 'NOT_VERIFIED', 'Ran directly: the script exits 1 on malformed or empty input, so only the declared `onFailure: block` can make that a block. The claim says so, and how a host applies it did not run: no live host here. M is the one candidate whose input-error path rests on that setting alone; M1, L0, L1, K0 and K1 refuse in the script itself.', 'documented difference: malformed input'),
    r('FG-M1-701faea2b7', 'NOT_VERIFIED', HOST, 'fail closed: no tool name'),
    r('FG-M1-30119e9885', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-M1-10ddb441f8', 'QUALIFIED', 'Read: M1 says typed exceptions "are a consistent project-level decision when used". M, K0, K1 and L1 carry the same idea in their error-handling skill. The sentence asks for consistency and does not by itself route to Reserved; a project-wide convention other code must follow is Reserved under CLAUDE.md item 7. Which applies depends on the use, so the record stays descriptive and adds no duty.'),
    r('FG-M1-6a4037ede3', 'NOT_VERIFIED', HOST + ' Gating of peer bypass and dependency commands ran in R06.', 'R06 hook suite'),
    r('FG-M1-a876ee45ce', 'CONFIRMED', 'R07 settled the reach this flag asked about: the line now points to `verify`, which owns the obligation and its condition. The alternative reading, that opening the UI follows only a startup change, no longer fits the text. DEFAULT stays on the pointer line; the owner is REP-M1-007.'),
    r('FG-L0-69195df14f', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-L0-c01d9476db', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-L0-29b2fd6409', 'NOT_VERIFIED', 'Registration read in settings.json. The host applying exec-form args, the timeout and onFailure did not run.'),
    r('FG-L0-084aeff176', 'CONFIRMED', 'As FG-M1-a876ee45ce; owner REP-L0-007.'),
    r('FG-L0-d9641a4b5e', 'CONFIRMED', 'The reported risk is not borne out, now by execution: `git check-ignore` ignores `.env` and `appsettings.Production.local.json`, and not `.env.example` or `appsettings.Development.json`.', 'git check-ignore: local overrides only'),
    r('FG-L1-7630c2d979', 'NOT_VERIFIED', HOST, 'stop hook: reminds once per state'),
    r('FG-L1-76b897a07d', 'NOT_VERIFIED', HOST, 'stop hook: reminds once per state'),
    r('FG-L1-8592937cba', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-L1-97559abbc9', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-L1-16c04bed44', 'NOT_VERIFIED', HOST, 'stop hook: reminds once per state'),
    r('FG-L1-fb077cb94f', 'QUALIFIED', 'Read against TST-004 (isolated from shared mutable state). A per-fixture host is shared process state, and TST-004 is about mutable state and data. The same rule leaves tests owning their data, so no conflict is established, and none is proved absent for a test that mutates host state. No runtime ran.'),
    r('FG-L1-f0cf2d0f61', 'CONFIRMED', 'The overmatch and blind spots are facts about what the check can see. The checker line is as reported. ' + READ),
    r('FG-L1-a73c9ece78', 'NOT_VERIFIED', 'Registration read in settings.json. The host applying exec-form args, the timeout and onFailure did not run.'),
    r('FG-L1-6b0ea79346', 'CONFIRMED', 'The sentence ends "to make a Git operation easier". An explicitly requested stash has a different purpose, so the reported categorical limit does not follow. ' + READ),
    r('FG-L1-de692b7c3d', 'CONFIRMED', 'As FG-M1-a876ee45ce; owner REP-L1-007.'),
    r('FG-L1-e844fb51b6', 'CONFIRMED', 'The rule keys on the async modifier at suggestion severity: a coverage fact about the analyzer, not a stricter duty. ' + READ),
    r('FG-L1-f6aff9e6f1', 'CONFIRMED', 'As FG-L0-d9641a4b5e, executed on L1 .gitignore.', 'git check-ignore: local overrides only'),
    r('FG-K0-2d8a0332f6', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-K0-a8a9deed7a', 'NOT_VERIFIED', HOST, 'K0 post-tool feedback emits a block decision'),
    r('FG-K0-2d15df1383', 'NOT_VERIFIED', HOST, 'K0 reference command: denied, marker opens it'),
    r('FG-K0-83aa75a850', 'NOT_VERIFIED', HOST, 'stop hook: reminds once per state'),
    r('FG-K0-209f40a1ff', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-K0-0f7b627b11', 'CORRECTED', 'C04 made the source line conditional on an authorized commit, so the reported conflict with the Git rule is gone from the text. The claim follows the source.'),
    r('FG-K0-715834e23c', 'CONFIRMED', 'The stricter-than-"normally" report is answered by the override route: `VersionOverride` stays open with a reported reason, as a notice. Checked in the C01 fixtures. ' + READ),
    r('FG-K0-6bc04e6316', 'CORRECTED', 'C01 replaced the literal check this flag described with the evaluated value, so a props file no longer has to enable CPM locally.'),
    r('FG-K0-dad9dffcde', 'NOT_VERIFIED', 'Registration read in settings.json. The host applying exec-form args and onFailure did not run.'),
    r('FG-K0-172287a31c', 'CONFIRMED', 'The list stops a loop on a blocker and hides no failure, as WF-008 asks. Independent repair stays possible after reassessing; nothing bars it. ' + READ),
    r('FG-K0-2e898e846a', 'QUALIFIED', 'A real but small sample issue: the text asks for deterministic ordering and the sample orders only by `CreatedAt`. The same sample is in M, M1, K1; L1 adds a tie-break and L0 comments on it. It is an example, the duty stands in the text, and no decision covers an edit. Not changed. Recorded as a wording difference.'),
    r('FG-K0-a597444d44', 'NOT_VERIFIED', HOST, 'K0 reference command: denied, marker opens it'),
    r('FG-K0-7a6b967b57', 'NOT_VERIFIED', HOST, 'K0 reference command: denied, marker opens it'),
    r('FG-K0-0ef1e5ed3d', 'CORRECTED', 'Closed in C05 under register 9.2: an audit criterion, with no product owner. The source section and its "Investigate" lead support that reading.'),
    r('FG-K0-6d06b21a93', 'CORRECTED', 'Same line as FG-K0-0ef1e5ed3d, closed in C05.'),
    r('FG-K0-93075d9f2a', 'CONFIRMED', 'The opening sentence limits the bullet to accidental artifacts; the reported drift against maintained generated output does not follow. ' + READ),
    r('FG-K0-878f7ff771', 'CONFIRMED', 'The matrix is an example. The sentence above it keeps FAIL and NOT RUN and says never to imply an unchecked area passed. ' + READ),
    r('FG-K0-08599e05a7', 'CONFIRMED', 'A specification may still request the change; the sentence bars silent override only. ' + READ),
    r('FG-K0-8e7d5328ee', 'CONFIRMED', 'The tension with Delegated is settled by the text: Delegated needs no material change, and the unclear-case test applies only to unclear cases. ' + READ),
    r('FG-K0-4d963cfe24', 'CONFIRMED', 'The line speaks of changing a decision, not of editing its wording. ' + READ),
    r('FG-K1-c1d46b03f7', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-K1-c4602c1553', 'NOT_VERIFIED', HOST, 'fail closed: malformed input'),
    r('FG-K1-85ff947903', 'NOT_VERIFIED', HOST, 'K1 reference command: blocked unless the edge is accepted'),
    r('FG-K1-69e6bb3a6a', 'NOT_VERIFIED', HOST, 'K1 reference command: blocked unless the edge is accepted'),
    r('FG-K1-eda1ffecb7', 'NOT_VERIFIED', HOST, 'stop hook: reminds once per state'),
    r('FG-K1-d74f68ee1a', 'CORRECTED', 'C04 made the source line conditional on an authorized commit.'),
    r('FG-K1-5baad49862', 'NOT_VERIFIED', HOST, 'K1 npm spec forms'),
    r('FG-K1-891a447fdc', 'NOT_VERIFIED', HOST, 'K1 removal, bulk update and force forms'),
    r('FG-K1-23a2f5e23c', 'NOT_VERIFIED', HOST, 'K1 removal, bulk update and force forms'),
    r('FG-K1-b0cc0892a5', 'NOT_VERIFIED', HOST, 'K1 removal, bulk update and force forms'),
    r('FG-K1-b8551d715e', 'NOT_VERIFIED', HOST, 'K1 removal, bulk update and force forms'),
    r('FG-K1-e32ee646e0', 'NOT_VERIFIED', HOST, 'K1 npm spec forms'),
    r('FG-K1-183ff2ff90', 'NOT_VERIFIED', HOST, 'K1 nested shell wrappers'),
    r('FG-K1-5a2b257bee', 'CORRECTED', 'C04 made the source line conditional on an authorized commit.'),
    r('FG-K1-94f1c38f5c', 'CONFIRMED', 'The source lists these names as Application semantics and bars the HTTP names. Whether NotFound and Conflict also read as HTTP words is a naming observation, already reviewed at orphan close; API-009 is satisfied. ' + READ),
    r('FG-K1-58ebd4b327', 'CORRECTED', 'C04 made the source line conditional on an authorized commit.'),
    r('FG-K1-c8396a981b', 'NOT_VERIFIED', HOST, 'K1 reference command: blocked unless the edge is accepted'),
    r('FG-K1-2b15ea3da2', 'CONFIRMED', 'As FG-M1-a876ee45ce; owner REP-K1-007. The alternative reading no longer fits: the line now points to `verify` for the obligation and its condition.'),
    r('FG-K1-31c818bc5a', 'CONFIRMED', 'As FG-K0-4d963cfe24: the line speaks of changing an entry, meaning a decision. ' + READ),
]
assert len(ROWS) == 62, len(ROWS)
