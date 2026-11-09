"""V3-D01 data overlay from the Pass 2 + Pass 3 adjudication. ADDED: candidate-level unrepresented security-scan prompts. UPDATES: facets
(dropped atoms or qualifiers written into the claim that already cites the passage). Every entry names its Codex records (or V3_CENSUS)."""
RULE = 'V3-D01-PASS23-OVERLAY'
SCAN = '.claude/skills/security-scan/references/scan-layers.md'
UPDATES = {}
ADDED = []
FACETS = []


def facet(key, cand, path, quote, claim, ids, note):
    FACETS.append(dict(key=key, candidate=cand, path=path, quote=quote, claim=claim, ids=ids, note=note))
    UPDATES[key] = dict(rule=RULE, status='REWORDED', claim=claim, note='V3-D01 facet (%s): %s' % (', '.join(ids), note), set={'codex_pass23_ids': ids}, sub={})


facet('FG-K1-8e0b256c02', 'K1', SCAN, 'account-enumeration behavior, and credential storage', 'Review local-account hashing, reset, lockout, enumeration and credential-storage behaviour; never recommend custom password hashing.', ['CIS-K1-U0036'], 'credential storage was dropped from the same sentence.')
SECRETS = 'Review production debug/development flags, certificate-validation bypasses, URLs carrying credentials, verbose production error configuration and committed .env files as part of the secrets and configuration layer of a security scan.'
SECRETS_NOTE = 'the Pass 1 provisional record held the debug-flags atom only; the other atoms of the same sentence are written in (verbose errors and .env from Pass 3; certificate bypass and credentialed URLs from the v3 census).'
facet('AUG1-NC-CIS-K1-0005-a', 'K1', SCAN, 'overly verbose production error configuration, and accidentally committed `.env` files', SECRETS, ['CIS-K1-U0032', 'CIS-K1-U0033', 'V3_CENSUS'], SECRETS_NOTE)
facet('AUG1-NC-CIS-L1-0009-a', 'L1', SCAN, 'verbose production error configuration, committed `.env` files', SECRETS, ['CIS-L1-U0036', 'CIS-L1-U0037', 'V3_CENSUS'], SECRETS_NOTE)
facet('AUG1-NC-CIS-K0-0012-a', 'K0', SCAN, 'overly verbose production error configuration and accidentally committed `.env` files', SECRETS, ['CIS-K0-U0046', 'CIS-K0-U0047', 'V3_CENSUS'], SECRETS_NOTE)
facet('FG-K1-94b2ab5757', 'K1', SCAN, 'execution/public-serving risks, and authorization', 'Upload execution, public-serving and size risks are inspected.', ['V3_CENSUS'], 'public serving was dropped from the same sentence (v3 census; Codex raised no K1 upload record).')
facet('FG-M1-7c88da0f41', 'M1', SCAN, 'Review duplicate or missing security-relevant logging in context', 'Check logs against security.md; review PII per project requirements; Debug/Trace level is not a security boundary; review duplicate or missing security-relevant logging in context; do not demand logs for every successful request.', ['CIS-M1-U0051', 'CIS-M1-U0052'], 'the duplicate/missing logging atom was dropped from the same passage.')
facet('FG-L1-5821a256da', 'L1', SCAN, 'Review missing or duplicated security-relevant logging in context', 'Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; review missing or duplicated security-relevant logging in context; no demand to log every successful request.', ['CIS-L1-U0043', 'CIS-L1-U0044'], 'the duplicate/missing logging atom was dropped from the same line.')
facet('FG-K1-112ed0f2b3', 'K1', SCAN, 'Review duplicate or missing security-relevant logging in context', 'Logs must not contain passwords, tokens, keys, auth secrets or full payment credentials; PII per project requirements; prefer technical identifiers; Debug/Trace is not a security boundary; review duplicate or missing security-relevant logging in context.', ['CIS-K1-U0037', 'CIS-K1-U0038'], 'the duplicate/missing logging atom was dropped from the same line.')
facet('FG-K1-5953b8f383', 'K1', '.claude/rules/backend/architecture-style.md', 'domain-level encapsulation independent of a particular use case', 'Move behaviour into Domain only for non-trivial invariants materially benefiting from domain-level encapsulation independent of a particular use case; otherwise Rich Domain/DDD tactical patterns require approval unless the specification requires them.', ['CIS-K1-U0011'], 'the K1-only qualifier "independent of a particular use case" was dropped.')
facet('FG-K1-770fc67286', 'K1', '.claude/skills/aspnet-error-handling/SKILL.md', 'perform cleanup that cannot be expressed otherwise', 'Catch only to recover, translate, perform cleanup that cannot be expressed otherwise, or add context while preserving the original; never catch Exception merely to continue; avoid catch/log/rethrow at every layer.', ['CIS-K1-U0012'], 'the qualifier on cleanup was dropped (L0 FG-L0-9856a2b2b0 records it).')
facet('FG-K1-6d5d64d4fe', 'K1', '.claude/skills/aspnet-error-handling/SKILL.md', 'perform cleanup that cannot be expressed otherwise', 'Catch exceptions only to recover, translate into a meaningful abstraction-level outcome, perform cleanup that cannot be expressed otherwise, add context while preserving the original, apply a defined fallback or infrastructure retry; otherwise let them propagate; never swallow external-service failures or catch Exception merely to continue.', ['CIS-K1-U0012'], 'same qualifier, second K1 record of the line.')
facet('FG-M1-064c990ec0', 'M1', '.claude/rules/security.md', 'prefer stable technical identifiers', 'Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need and prefer stable technical identifiers; log level does not make data safe.', ['CIS-M1-U0014'], 'the identifier preference was dropped; M, L0, L1, K0 and K1 record it.')
facet('FG-K0-2f3f94690d', 'K0', '.claude/rules/backend/architecture.md', 'use-case-specific queries stay in concrete repositories', 'Application does not depend on IGenericRepository<T> or another generic CRUD contract; a generic repository/base class may exist only as an Infrastructure detail removing real duplication, not replacing EF Core query capabilities; use-case-specific queries stay in concrete repositories.', ['CIS-K0-U0017'], 'the last clause of the same sentence was dropped (L1 FG-L1-1e3bd505b3 records it).')
facet('FG-M1-28892c03c6', 'M1', 'docs/capability-selection.md', 'read only during capability maintenance', 'Contracts and manifests are maintainer metadata, not auto-loaded, and are read only during capability maintenance.', ['CIS-M1-U0022'], 'the explicit loading restriction was dropped.')


def scan(cand, n, claim, quote, ids, related, peers, trigger):
    ADDED.append(dict(source_key='V3A-%s-%03d' % (cand, n), candidate=cand, rule=RULE, classification='EXTRA_WORKFLOW', modality='DEFAULT', domain='WORKFLOW_ENFORCEMENT', claim_text=claim, path=SCAN, quote=quote,
                      canonical_coverage=[], related_policy_ids=related, extra_fragment='A security-scan investigation prompt stated in the source and in peer candidates.', extra_fragment_kind='EXTRA_WORKFLOW',
                      distinguishing_scenario='A security scan of an application with this surface: the prompt directs the reviewer to inspect it; no record of this candidate stated it before v3 (%s).' % ', '.join(ids),
                      trigger=trigger, exceptions='The layer does not apply when the surface does not exist; prompts are not automatic vulnerability declarations.', confidence='MEDIUM',
                      codex_pass23_ids=ids,
                      review_reading='Source-read in v3 (scan_census.py, _adjudication/clusters). Same prompt as peer records %s. Codex or census: %s.' % (', '.join(peers), ', '.join(ids)), review_phrases=[quote]))


ACCT = 'When the security scan covers an application that owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.'
ACCT_T = 'Security-scan workflow, authentication and access-control layer, when the application owns local accounts.'
ACCT_P = ['FG-M-7c2154e45a', 'FG-M1-f0a2f2becf', 'FG-K1-8e0b256c02']
scan('K0', 101, ACCT, 'When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.', ['CIS-K0-U0022', 'CIS-K0-U0023', 'CIS-K0-U0024', 'CIS-K0-U0025', 'CIS-K0-U0026'], ['SEC-016', 'SEC-018', 'WF-020'], ACCT_P, ACCT_T)
scan('L0', 101, ACCT, '**Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.', ['CIS-L0-U0018', 'CIS-L0-U0019', 'CIS-L0-U0020', 'CIS-L0-U0021', 'CIS-L0-U0022'], ['SEC-016', 'SEC-018', 'WF-020'], ACCT_P, ACCT_T)
scan('L1', 101, ACCT, '**Local accounts** — password hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.', ['CIS-L1-U0040'], ['SEC-016', 'SEC-018', 'WF-020'], ACCT_P, ACCT_T)
UPLOAD = 'When uploads exist, the security scan inspects whether uploaded content can execute and the risks of serving it publicly.'
for cand, n, quote, ids in (('M1', 101, 'execution or public-serving risks, and authorization', ['CIS-M1-U0049', 'CIS-M1-U0050']), ('L0', 102, 'execution or public-serving risk, authorization', ['CIS-L0-U0045', 'CIS-L0-U0046']),
                            ('L1', 102, 'execution or public-serving risks, authorization', ['CIS-L1-U0041', 'CIS-L1-U0042']), ('K0', 102, 'execution or public-serving risks and authorization', ['CIS-K0-U0050', 'CIS-K0-U0051'])):
    scan(cand, n, UPLOAD, quote, ids, ['SEC-015', 'SEC-003', 'WF-020'], ['FG-M-da325d3b47', 'FG-K1-94b2ab5757'], 'Security-scan workflow, upload layer, when the application accepts uploads.')
SSRF = 'During the security scan, inspect outbound requests where users influence the scheme, host, port, full URL or redirect destination, especially when the server can reach internal networks, metadata endpoints or privileged services (SSRF).'
for cand, n, quote, ids in (('M1', 102, 'Inspect outbound requests where users can influence the scheme, host, port, full URL, or redirect destination', ['CIS-M1-U0047']), ('L0', 103, 'outbound requests where users influence scheme, host, port, full URL, or redirect destination', ['V3_CENSUS']),
                            ('L1', 103, 'user influence over scheme, host, port, full URL, or redirects', ['CIS-L1-U0038']), ('K0', 103, 'Inspect outbound requests where users influence scheme, host, port, full URL or redirect destination', ['CIS-K0-U0048']),
                            ('K1', 101, 'Inspect outbound requests where users influence scheme, host, port, full URL, or redirect destination', ['CIS-K1-U0034'])):
    scan(cand, n, SSRF, quote, ids, ['SEC-003', 'WF-020'], ['FG-M-38fffb80cf'], 'Security-scan workflow, injection layer, when outbound requests exist.')
RAW = 'During the security scan, review deliberate raw HTML handling in any server-rendered UI.'
for cand, n, quote, ids in (('M', 101, 'Review deliberate raw HTML handling in any server-rendered UI as well.', ['V3_CENSUS']), ('M1', 103, 'Review deliberate raw HTML handling in any server-rendered UI as well.', ['CIS-M1-U0048']),
                            ('L1', 104, 'Review raw HTML handling in any server-rendered UI.', ['CIS-L1-U0039']), ('K0', 104, 'Review deliberate raw HTML handling in any server-rendered UI as well.', ['CIS-K0-U0049']),
                            ('K1', 102, 'Review deliberate raw HTML handling in any server-rendered UI as well.', ['CIS-K1-U0035'])):
    scan(cand, n, RAW, quote, ids, ['SEC-003', 'WF-020'], ['(none recorded before v3; L0 has no such sentence)'], 'Security-scan workflow, XSS layer, when a server-rendered UI exists.')
scan('K0', 105, 'During the security scan, review duplicate or missing security-relevant logging in context, without demanding logs for every successful request.', 'duplicate or missing security-relevant logging in context', ['CIS-K0-U0052', 'CIS-K0-U0053'], ['SEC-010', 'WF-012', 'WF-020'], ['FG-M-56386cff04', 'FG-L0-041f2fee65'], 'Security-scan workflow, logging and sensitive-data layer.')
