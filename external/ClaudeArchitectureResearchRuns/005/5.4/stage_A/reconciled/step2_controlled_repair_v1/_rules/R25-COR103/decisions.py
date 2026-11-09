"""R25: individual decisions on the 103 audit corrections. Rows not listed here are decided by rule in _tools/cor103.py: a PI-012-dependent row is accepted only if its modality equals the R01 reading of that key; every other row must appear here or in ACCEPT_READ."""

SW_TRIGGER = 'A change alters API behavior and the project exposes the UI in Development.'
SW_EXC = 'The project exposes no such UI: the step does not apply. The application cannot run in this environment: reported NOT RUN, never passed.'
SW_EXTRA = 'Open the Development Swagger UI and confirm it loads on an applicable API behavior change, even when startup and composition did not change. Obligation and condition: verify.'
SW = dict(trigger=SW_TRIGGER, exceptions=SW_EXC, extra_fragment=SW_EXTRA)
GIT_SET = dict(classification='CANONICAL_ONLY', oracle_relation='FULLY_ENTAILED', extra_fragment=None, extra_fragment_kind=None, distinguishing_scenario=None, strength_vs_canonical='SAME', review_needed=False, review_reason=None, trigger='Rewriting the history of main, master, or another protected or shared branch.', exceptions='An explicit user request naming that branch, unless another policy forbids it.')
SUP = {'R02': 'Register 9.1 settles the question the audit left open.'}

# decision: ACCEPT_MODIFIED or REJECT, fields added over the proposal, reason, counterexample
SPECIAL = {
    'FG-K1-2b15ea3da2': ('ACCEPT_MODIFIED', SW, 'Reading holds at source. R07 moved the obligation to verify and aligned trigger and action, so the remainder is restated from current text.', 'Controller status change, tests pass, no UI opened: WF-005, WF-006, API-016, TST-010 hold and this step is not done.'),
    'FG-M-268251a6d0': ('ACCEPT_MODIFIED', dict(trigger=SW_TRIGGER, exceptions=SW_EXC), 'Trigger repair holds. Restated from current text after R07.', None),
    'FG-M1-a876ee45ce': ('ACCEPT_MODIFIED', SW, 'Reach of the condition settled. Current text in verify removes the run-in ambiguity for all six.', 'Status code change with no UI opened.'),
    'FG-M1-51dccbe9d9': ('ACCEPT_MODIFIED', SW, 'Compound names the UI step, so CO fails. Restated after R07.', None),
    'FG-L0-084aeff176': ('ACCEPT_MODIFIED', SW, 'The audit kept open-only and API changes as real differences. R07 aligns both, so those fragments of the proposal no longer match the source and are replaced.', 'The proposal says open only; current source says open and confirm it loads.'),
    'FG-L0-ad2b418693': ('ACCEPT_MODIFIED', SW, 'As FG-L0-084aeff176.', None),
    'FG-L1-de692b7c3d': ('ACCEPT_MODIFIED', SW, 'As L0: open-only is gone after R07.', 'The proposal says open only; current source says open and confirm it loads.'),
    'FG-L1-a48ca2a20d': ('ACCEPT_MODIFIED', SW, 'As FG-L1-de692b7c3d.', None),
    'FG-K0-47988fe869': ('ACCEPT_MODIFIED', SW, 'Numbered step reading holds. Heading now says API behavior changes, so the trigger is restated.', None),
    'FG-K0-9522259b92': ('ACCEPT_MODIFIED', SW, 'As FG-K0-47988fe869.', None),
    'FG-K0-6bc04e6316': ('REJECT', None, 'The remainder the audit found (the check is broader than DEP-006) no longer exists after R08: the checker reads the effective value. The record maps to a canonical enforcement claim.', 'CPM enabled in Directory.Build.props: the old check rejected it, the current check accepts it, and real MSBuild agrees.'),
    'FG-M1-159a4ef4c3': ('REJECT', None, 'The proposed INCOMPARABLE rests on the user-confirmation route. R06 removed the route, so STRONGER stands: the hook stops every force install, wider than the policy word merely.', 'npm install x --force # peer-override: approved-by-user is denied now (executed).'),
    'FG-K1-8c2a0fe6ef': ('REJECT', None, 'The remainder (measured only) no longer exists after R09. The line now says measured or clearly demonstrated, so CO on RUN-008 stands on current text.', 'A clearly demonstrated need with no profile: allowed by RUN-008 and by the current line.'),
    'FG-L0-313d81df34': ('REJECT', None, 'The remainder (no migration automation of any form) no longer exists after R10. CO on WF-019 and SEC-001 stands on current text.', 'A controlled deployment-time step with approved credentials: allowed by WF-019 and by the current line.'),
    'FG-K1-d5a92cb349': ('ACCEPT_MODIFIED', dict(extra_fragment='When this work runs against a local database, apply the migration there before any seeding, or drop and recreate it when a fresh dataset is needed.', trigger='Work runs against a local database after a persistence change.', modality='DEFAULT'), 'XW holds: no policy asks to apply migrations locally. R12 made the step conditional, so the fragment is restated.', 'A behavior-only change with no migration: no local apply is due.'),
    'FG-K0-65f36b8cd7': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'] + ' Non-rewritable by default with a named explicit request as the route: entailed by GOV-015. The field fix is moot.', 'Force-push to main with an explicit request naming main: GOV-015 holds and so does the current line.'),
    'FG-K0-93bf76a2fb': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-K1-728e7fa972': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-L0-9fd13469f8': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-L0-bfbd1e049f': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-L1-16ebadbe2b': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-L1-736f7de527': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-M1-456f6c0b26': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'], None),
    'FG-M1-d746992071': ('ACCEPT_MODIFIED', GIT_SET, SUP['R02'] + ' The reported tension between the two sentences is gone.', None),
}

# Source-supported rows accepted after reading the proposal and the source; the source text is unchanged by any template rule unless noted.
ACCEPT_READ = {
    'FG-K0-9e13b040f1': 'Evaluative "not worth adding": SHOULD_NOT under A1.4. R01 reads the same.',
    'FG-K0-c0ccb8af1b': 'Explicit "by default": frozen rule 5. R01 reads the same.',
    'FG-K0-eeea8f4dda/S2': 'Same line at subclause level.',
    'FG-L1-f93f0c7c0d': 'Positive imperative: A1.3. R01 reads the same.',
    'FG-L1-159d2e5920': 'Explicit "not added by default": frozen rule 5.',
    'FG-M1-2a030a5f1e': 'Removes an obligation: C6. Coverage of ARC-027 holds through M1 rules.',
    'FG-L0-3f6d42031c': 'Source line tags (default); stored MUST strengthened it. Sibling reads the same rule at DEFAULT.',
    'FG-M1-e3684cb036': 'Facet read at source: the reporting clause is real and no subclause held it.',
    'FG-K1-e64089621e': 'Marked do-not sentence separate from the tagged preference, read at source.',
    'FG-L0-a3477280c6': 'Line 38 is a negative imperative in always-loaded policy; remainder is agent process.',
    'FG-L0-29a3230807': 'No part follows from WF-018, WF-020 or GOV-014. R19 applies the same reading to same-content lines.',
    'FG-L1-3ac9d1544d': 'As FG-L0-a3477280c6.',
    'FG-L1-bb27864162': 'Allowance inside the routing gate. Deny-once for ordinary dependency changes survives R06; force flags no longer reach it.',
    'FG-L1-56c0d959e5': 'Source: applies after a framework upgrade and to APIs that can be verified. Stored fields lost that.',
    'FG-L1-f79dc1b843': 'Own-versus-upstream is not in API-021 or RUN-019. R15 applies the same reading to same-claim lines.',
    'FG-M1-bbde8b1664': 'The cited policies bind implementation; this line binds what a scan recommends. R17 applies the same reading to the other five.',
    'FG-L1-51237abb7d': 'No dependency checks at all is narrower than API-019, at DEFAULT in a skill. R16.',
    'FG-K1-8a61b0db25': 'Same sentence as M after COR-M-0001. R13.',
    'FG-K0-9146b82c8d': 'Same sentence as M after COR-M-0001. R13.',
    'FG-M-b00f9a8f1a': 'Confirm-first is not in DEP-008 or RUN-009. R14.',
    'FG-L1-f7f4433e5e': 'Slow-test separation is not in TST-004; siblings hold it separately. R18.',
    'FG-K1-aeb672431c': 'Same sentence is NN in M, M1, L0; RUN-005 does not mention tests.',
    'FG-M1-b82958affd': 'M1 line is unconditional; GOV-002 and GOV-008 do not ask to read CUSTOM_SETTINGS before every plan. R11 brings L0, K0, K1 to the same text and the same label.',
    'FG-M-cf0b72f861': 'Only-when in a knowledge skill; M1 identical text reads DEFAULT. R01 reads the same.',
    'FG-L0-c21644a775': 'Removes an assumed need; bans nothing.',
    'FG-L1-be0e9eb7f6': 'Same sentence as FG-L0-c21644a775.',
    'FG-L1-96c278fc07': 'Removes a need; PST-006 ban sits elsewhere in L1.',
    'FG-K1-05e649abd6': 'Removes a duty; fits WF-007.',
    'FG-L0-4dc7013ec9': 'Only-when; not a checklist is descriptive. R01 reads the same.',
}
