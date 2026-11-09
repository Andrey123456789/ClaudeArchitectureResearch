"""Independent v3 adjudication of Codex Pass 0002 and Pass 0003 (kit 74 Part A). Written after reading every record's cited source with
context (`_adjudication/clusters/*.md`, `view.py`, `near.py`), the overlapping v2 records, the Pass 1 ledger and the census in
`scan_census.py`. Codex labels were inputs, not truth.

Verdicts (kit 74 A.2 categories):
  CANDIDATE_UNREPRESENTED_DUTY  (c) a procedural or normative duty in the source that no same-candidate record states; the same duty is
                                represented in a peer candidate or recurs in the same shared template wording, so it is new to this
                                candidate's records, not a new study-level obligation
  FACET_OF_EXISTING             (d) a same-candidate record cites the passage but drops an atom, a qualifier or a condition
  ALREADY_COVERED               (e) a same-candidate record already states it
  NON_NORMATIVE                 (f) technique table row, permissive or illustrative text, static configuration, implementation detail,
                                checker heuristic or library prerequisite; `kind` names which
  OPEN_HYPOTHESIS               (g) kept open with reason and risk
No record is a study-level new obligation: every normative atom found here exists in at least one candidate's records or in the
identical shared wording. No Codex record is treated as a proven EXTRA or a proven cross-candidate difference.

Overlay actions (applied in change V3-D01-PASS23-OVERLAY, gated):
  ADD      a REPAIR_ADDED_CLAIM in that candidate, classification mirroring the Step 2 label of the same prompt in peer candidates
  APPEND   the dropped atom is appended to the same-candidate record (same actor, action, trigger and modality); classification,
           modality and canonical links unchanged; original claim kept in claim_text_original
  NONE     no data change
"""

# Cluster definitions. `members` are filled by adj_build.py from THEME_TO_CLUSTER and per-record overrides.
CLUSTERS = {
    'CL01-HOOK-BUDGETS': dict(title='Configured hook and helper timeouts', verdict='NON_NORMATIVE', kind='STATIC_CONFIGURATION',
                              reading='Timeout values in settings.json registrations of advisory hooks (60 s; L1 30 s and 15 s) and execFileSync helper budgets (15 s with a null fallback). They bound how long a host waits for a hook; they impose nothing on the agent. Registration form, positive-timeout checks and onFailure policy are already recorded (e.g. FG-L0-a9a5a79d44, FG-M-ddd9d93ab6). Pass 1 recorded the PreToolUse 30 s budget as already represented (CIS-P0001-M-C0004) and treated silent helper failure modes as not independent.',
                              significance='None for policy parity. The values differ by candidate (L1 30/15, others 60); that is a delivery-implementation fact, and how a host applies a timeout is untested (NOT_RUN).'),
    'CL02-ERROR-CONTRACT-FIELDS': dict(title='Fields a useful error contract may contain', verdict='NON_NORMATIVE', kind='PERMISSIVE_GUIDANCE',
                                       reading='One sentence, the same in all six aspnet-error-handling knowledge skills: "A useful error contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation/trace identifier". L1 says "carries", still describing a useful contract. Permissive and descriptive; the binding part (ProblemDetails, stable safe machine-readable contract, API-002/API-008) is already recorded in every candidate. Pass 1 ruled two atoms of the same sentence (code, trace id) not independent in K1, L1 and K0; the remaining atoms take the same ruling.',
                                       significance='None. Identical wording in all six, so no cross-candidate difference.'),
    'CL03-OPTIONS-TABLE': dict(title='Configuration decision-table rows (IOptions*, BindConfiguration, ValidateOnStart)', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                               reading='Rows of the "situation -> API" table in the configuration knowledge skill (DI skill for M U0012). Pass 1 convention: IOptions* decision tables are technique, not rules. The binding duty (strongly typed options validated at startup, RUN-022) is recorded in all six.',
                               significance='None.'),
    'CL04-SERILOG-TABLE': dict(title='Serilog technique table rows, sink options and library prerequisites', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                               reading='Rows of the Serilog decision table and sink notes in serilog.md references (storage choices, UseSerilogRequestLogging, LogContext.PushProperty, Serilog.Expressions, AuditTo, MinimumLevel.Override, OTLP sink), plus the "requires Enrich.FromLogContext / Serilog.Expressions package" prerequisites. Technique and library prerequisites (Pass 1 convention). The binding logging duties (RUN-013, DEP-021, API-012, DEP-004 deprecated sink) are recorded in all six.',
                               significance='None.'),
    'CL05-LOG-SCOPE-TABLE': dict(title='Logging decision table: BeginScope for shared context', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                                 reading='One row of the logging knowledge-skill table. Technique; RUN-013 structured logging is recorded.', significance='None.'),
    'CL06-DI-TABLE': dict(title='DI decision-table rows (lifetimes per situation, Decorator, Scrutor, factory delegate)', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                          reading='Rows of the DI knowledge-skill decision table. The binding duties are recorded: valid lifetimes and no captive dependency (ARC-022), explicit registration unless a real composition problem exists (GOV-012/GOV-013).',
                          significance='None.'),
    'CL07-SCRUTOR-EXAMPLE': dict(title='Scrutor decoration example conditioned on Scrutor already in use', verdict='NON_NORMATIVE', kind='ILLUSTRATIVE_EXAMPLE',
                                 reading='The "if Scrutor is already used" lead-in scopes a code example. The adjacent binding line "do not add Scrutor for one decoration when normal composition is simpler" is the rule, recorded where extracted (K1 FG-K1-d8c34708a7); the example condition adds no duty.',
                                 significance='None.'),
    'CL08-EF-TABLE': dict(title='EF Core technique rows (FindAsync, ExecuteUpdate/Delete)', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                          reading='Pass 1 convention: technique contrasts such as FindAsync are not rules. "When its semantics fit / when appropriate" makes them technique choices.', significance='None.'),
    'CL09-CACHING-TABLE': dict(title='Caching decision-table rows', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                               reading='Rows naming candidate cache technologies per situation. The binding duties are recorded: caching only for a clear need with the implementation chosen from deployment, consistency and staleness (RUN-007), and distributed caching as new infrastructure is Reserved (ARC-020, e.g. FG-M-809acdb398, which also covers M row 146 "(Reserved: new infrastructure)").',
                               significance='None.'),
    'CL10-HEDGING': dict(title='Consider hedging for latency-sensitive idempotent reads after measurement', verdict='NON_NORMATIVE', kind='TECHNIQUE_TABLE',
                         reading='Resilience reference table row; "consider ... after measurement" is technique gated by the recorded measured-need duty (RUN-008/RUN-015).', significance='None.'),
    'CL11-SCAN-LOCAL-ACCOUNTS': dict(title='Security scan: review local-account mechanisms (hashing, reset, lockout, enumeration, credential storage)', verdict='MIXED', kind='SCAN_PROMPT',
                                     reading='A security-scan investigation prompt in the workflow skill private reference (procedural duty under the Pass 1 convention), same wording in all six. M (FG-M-7c2154e45a, FG-M-4cc9877f3c), M1 (FG-M1-f0a2f2becf) and K1 (FG-K1-8e0b256c02, without credential storage) record it; K0 scan-layers.md:107, L0 :38 and L1 :37 have no record at all - all three original runs skipped the line. The product duties behind it (SEC-016, SEC-018) are recorded in every candidate.',
                                     significance='Classification completeness, not a template difference: EXTRA_WORKFLOW counts per candidate were uneven for identical text. No coverage cell moves (the added records carry no canonical link, like M peer record).'),
    'CL12-SCAN-SECRETS-CONFIG': dict(title='Security scan: also review debug flags, certificate-validation bypass, credentialed URLs, verbose production errors, committed .env files', verdict='MIXED', kind='SCAN_PROMPT',
                                     reading='One "also review" sentence in all six. M (FG-M-2a4248c467), M1 (FG-M1-f69450f03c) and L0 (v1 proposal NCP-L0-0001) record every atom. Pass 1 added only the debug-flags atom for L1, K0 and K1 (AUG1-NC-CIS-L1-0009-a, -K0-0012-a, -K1-0005-a). Pass 3 found the verbose-error and .env atoms; the v3 census found the credentialed-URL and certificate-bypass atoms of the same sentence also missing there (certificate bypass is separately recorded through SEC-007 scan records).',
                                     significance='Facets of the Pass 1 provisional records; no coverage cell moves.'),
    'CL13-SCAN-UPLOADS': dict(title='Security scan: inspect upload execution and public-serving risks', verdict='MIXED', kind='SCAN_PROMPT',
                              reading='Same upload prompt in all six. M records it whole (FG-M-da325d3b47); K1 records execution only (FG-K1-94b2ab5757). M1 205-207 and K0 129 have only the SEC-015 MIME-type record on the line; L0 46 and L1 45 have nothing.',
                              significance='Classification completeness; no coverage cell moves.'),
    'CL14-SCAN-SSRF': dict(title='Security scan: inspect outbound requests whose scheme, host, port, URL or redirect users influence', verdict='MIXED', kind='SCAN_PROMPT',
                           reading='Same SSRF prompt in all six. Only M records the positive inspection duty (FG-M-38fffb80cf). M1, L0 and L1 record only the false-positive half ("a query parameter alone is not SSRF"); K0 and K1 record nothing on the line. L0 was not raised by Codex; the v3 census found it.',
                           significance='Classification completeness; no coverage cell moves.'),
    'CL15-SCAN-RAW-HTML': dict(title='Security scan: review deliberate raw HTML handling in any server-rendered UI', verdict='MIXED', kind='SCAN_PROMPT',
                               reading='M, M1, L1, K0 and K1 carry the sentence; no candidate records it. L0 has no such sentence (its XSS prompt is Angular-only): a real text difference, kept as written. M was not raised by Codex; the v3 census found it.',
                               significance='Classification completeness for five; L0 difference recorded as a residual, not homogenized (no approved policy requires it).'),
    'CL16-SCAN-LOGGING': dict(title='Security scan: review duplicate or missing security-relevant logging in context', verdict='MIXED', kind='SCAN_PROMPT',
                              reading='Same logging prompt in all six. M (FG-M-56386cff04) and L0 (FG-L0-041f2fee65) record it. M1 (FG-M1-7c88da0f41), L1 (FG-L1-5821a256da) and K1 (FG-K1-112ed0f2b3) record the same sentence without the atom; K0 139 has only the SEC-010 never-log rule record.',
                              significance='Facets for three, one added record for K0; no coverage cell moves.'),
    'CL17-SCAN-TARGETED-PRIORITY': dict(title='Targeted scan priority table row: a database/query change prioritizes access control', verdict='NON_NORMATIVE', kind='PROCEDURAL_TABLE_DETAIL',
                                        reading='A row of the "change -> priority layers" table. The binding duty, a targeted change starts with the affected layers and expands across security boundaries (WF-007), is recorded (FG-K1-ba3da08dba, FG-L1-e52b9bf6fd). The row is a starting heuristic, not an independent duty.',
                                        significance='None.'),
    'CL18-K1-DOMAIN-QUALIFIER': dict(title='K1: Domain behavior only when the encapsulation benefit is independent of a particular use case', verdict='FACET_OF_EXISTING', kind='QUALIFIER',
                                     reading='K1 architecture-style.md:28. FG-K1-5953b8f383 states the sentence without "independent of a particular use case". The qualifier narrows when Domain behavior is justified (ARC-004). K1-only wording; no other candidate has it.',
                                     significance='Candidate-specific nuance, kept as K1 wording; not a parity item.'),
    'CL19-CATCH-CLEANUP-QUALIFIER': dict(title='Catch for cleanup only when the cleanup cannot be expressed otherwise', verdict='FACET_OF_EXISTING', kind='QUALIFIER',
                                         reading='K1 aspnet-error-handling:114 (and L0 :109 in the census) say "perform cleanup that cannot be expressed otherwise". K1 records FG-K1-770fc67286 and FG-K1-6d5d64d4fe drop the qualifier. API-007 context.',
                                         significance='Facet; no cell moves. L0 already records the qualifier (FG-L0-9856a2b2b0: "perform otherwise inexpressible cleanup"), so the K1 append brings K1 in line with L0.'),
    'CL20-LOG-TECH-IDS': dict(title='Prefer stable technical identifiers in logs', verdict='FACET_OF_EXISTING', kind='DROPPED_ATOM',
                              reading='M1 security.md:98-102. FG-M1-064c990ec0 omits "prefer stable technical identifiers"; the same atom is in the corresponding SEC-010 records of M, L0, L1, K0 and K1.',
                              significance='Brings M1 in line with its peers; no cell moves.'),
    'CL21-M1-SECTION-REF-HEURISTIC': dict(title='M1 checker accepts a section reference whose leading words match a heading', verdict='NON_NORMATIVE', kind='CHECKER_HEURISTIC',
                                          reading='check-instructions.js:209-218 tries the captured words from longest to shortest prefix, which deliberately tolerates trailing prose after "§ Section". Side effect: a stale reference whose first words match another heading passes. An enforcement-strength observation on an internal-architecture rule (FG-M1-ea34763ee6), not a policy obligation.',
                                          significance='Low. Kept OPEN as an observation; no approved policy authorizes changing M1 checker semantics.'),
    'CL22-K0-USECASE-QUERIES': dict(title='K0: use-case-specific queries stay in concrete repositories', verdict='FACET_OF_EXISTING', kind='DROPPED_ATOM',
                                    reading='K0 rules/backend/architecture.md:44 ends with "and use-case-specific queries stay in concrete repositories". FG-K0-2f3f94690d states the rest of the sentence (ARC-015). L1 records the same atom (FG-L1-1e3bd505b3).',
                                    significance='Facet; no cell moves.'),
    'CL23-K0-PROGRAM-EXPOSURE': dict(title='Expose Program for host integration tests when top-level statements hide it', verdict='NON_NORMATIVE', kind='TECHNIQUE',
                                     reading='dotnet-testing knowledge skill technique ("public partial Program" as an example mechanism). The binding test-isolation duties (TST-004) are recorded.', significance='None.'),
    'CL24-L0-XSRF-NAMES': dict(title='Angular XSRF support needs matching cookie/header names', verdict='NON_NORMATIVE', kind='TECHNIQUE',
                               reading='Configuration detail of the recorded SEC-011 mechanism (FG-L0-cb9a81a22c names Angular XSRF support). Not an independent duty.', significance='None.'),
    'CL25-L0-MIGRATION-ARTIFACTS': dict(title='Idempotent scripts or bundles are often preferable for controlled production deployment', verdict='NON_NORMATIVE', kind='ADVISORY_TECHNIQUE',
                                        reading='"Often preferable" in the ef-core knowledge skill. The binding production-migration default and its exception (WF-019) were made consistent in v2 C03.', significance='None.'),
    'CL26-L0-MALFORMED-MESSAGE': dict(title='L0 hook message asks to fix malformed manifest XML', verdict='NON_NORMATIVE', kind='IMPLEMENTATION_DETAIL',
                                      reading='Wording of a hook feedback message. The fail-closed treatment of malformed manifests is recorded (v2 C01).', significance='None.'),
    'CL27-M-PRESENTATION-EVENTS': dict(title='M: reusable presentation components emit meaningful UI events', verdict='NON_NORMATIVE', kind='TECHNIQUE',
                                       reading='Component-design guidance in the M angular knowledge skill. No canonical policy requires it; the recorded component duties (focused components, data-access boundary) are unaffected.', significance='None.'),
    'CL28-M-499-EXAMPLE': dict(title='M: client-cancellation example returns 499', verdict='NON_NORMATIVE', kind='ILLUSTRATIVE_EXAMPLE',
                               reading='Code example in a knowledge skill.', significance='None.'),
    'CL29-M1-CAPABILITY-METADATA': dict(title='M1: read slot contracts and module manifests only during capability maintenance', verdict='FACET_OF_EXISTING', kind='LOADING_RESTRICTION',
                                        reading='M1 docs/capability-selection.md:28-30 and MAP.md. FG-M1-28892c03c6 says the files are maintainer metadata, not auto-loaded; the source also limits reading them to capability maintenance (Pass 1 convention: an explicit loading restriction is an instruction-architecture duty).',
                                        significance='M1-only architecture; no parity item.'),
    'CL30-M1-CREATEDAT': dict(title='M1: prefer CreatedAtAction/CreatedAtRoute when a canonical resource URL exists', verdict='ALREADY_COVERED', kind='TECHNIQUE_OF_COVERED_DUTY',
                              reading='The duty, a 201 carries Location when a stable resource URI exists (API-003), is recorded (FG-M1-0d82a465e2, FG-M1-b77b89232d); CreatedAt* is the technique. Pass 3 report notes the same for K0 primary0541.', significance='None.'),
}

THEME_TO_CLUSTER = {'HOOK-TIMEOUT': 'CL01-HOOK-BUDGETS', 'ERROR-CONTRACT-FIELDS': 'CL02-ERROR-CONTRACT-FIELDS', 'OPTIONS-DECISION-GUIDE': 'CL03-OPTIONS-TABLE', 'SERILOG-DECISION-GUIDE': 'CL04-SERILOG-TABLE',
                    'LOGGING-SCOPE-GUIDE': 'CL05-LOG-SCOPE-TABLE', 'DI-DECISION-GUIDE': 'CL06-DI-TABLE', 'EF-DECISION-GUIDE': 'CL08-EF-TABLE', 'CACHING-DECISION-GUIDE': 'CL09-CACHING-TABLE', 'HEDGING-GUIDE': 'CL10-HEDGING',
                    'SCAN-LOCAL-ACCOUNTS': 'CL11-SCAN-LOCAL-ACCOUNTS', 'SCAN-SECRETS-CONFIG': 'CL12-SCAN-SECRETS-CONFIG', 'SCAN-UPLOADS': 'CL13-SCAN-UPLOADS', 'SCAN-SSRF': 'CL14-SCAN-SSRF', 'SCAN-RAW-HTML': 'CL15-SCAN-RAW-HTML',
                    'SCAN-LOGGING': 'CL16-SCAN-LOGGING', 'SCAN-TARGETED-PRIORITY': 'CL17-SCAN-TARGETED-PRIORITY'}

# Per-record decisions where the cluster default does not settle it. action: ADD / APPEND / NONE; target: the v2 key for APPEND, or the new key for ADD.
R = {}


def d(ids, verdict, cluster=None, action='NONE', target=None, kind=None, note=''):
    for i in ids.split():
        R[i] = dict(verdict=verdict, cluster=cluster, action=action, target=target, kind=kind, note=note)


# CL02: two L0 records whose claim text did not match the theme pattern.
d('CIS-L0-U0033 CIS-L0-U0036', 'NON_NORMATIVE', 'CL02-ERROR-CONTRACT-FIELDS', kind='PERMISSIVE_GUIDANCE')
# CL04 library prerequisites.
d('CIS-M1-U0020 CIS-M-U0026', 'NON_NORMATIVE', 'CL04-SERILOG-TABLE', kind='LIBRARY_PREREQUISITE', note='A library prerequisite of a technique (Pass 1 convention: not promoted).')
# CL07 Scrutor examples.
d('CIS-L0-U0038 CIS-M-U0043 CIS-K1-U0021 CIS-M1-U0033', 'NON_NORMATIVE', 'CL07-SCRUTOR-EXAMPLE', kind='ILLUSTRATIVE_EXAMPLE')
# CL09 M caching row with the Reserved annotation: the Reserved part is covered.
d('CIS-M-U0042', 'NON_NORMATIVE', 'CL09-CACHING-TABLE', kind='TECHNIQUE_TABLE', note='The "(Reserved: new infrastructure)" annotation is covered by FG-M-809acdb398 (ARC-020: distributed caching is Reserved).')
# CL11 local accounts.
d('CIS-K0-U0022 CIS-K0-U0023 CIS-K0-U0024 CIS-K0-U0025 CIS-K0-U0026', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL11-SCAN-LOCAL-ACCOUNTS', 'ADD', 'V3A-K0-101', 'SCAN_PROMPT', 'K0 scan-layers.md:107 has no record; one added record carries the whole prompt.')
d('CIS-L0-U0018 CIS-L0-U0019 CIS-L0-U0020 CIS-L0-U0021 CIS-L0-U0022', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL11-SCAN-LOCAL-ACCOUNTS', 'ADD', 'V3A-L0-101', 'SCAN_PROMPT', 'L0 scan-layers.md:38 has no record (records exist at 35, 36, 37, 39).')
d('CIS-L1-U0040', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL11-SCAN-LOCAL-ACCOUNTS', 'ADD', 'V3A-L1-101', 'SCAN_PROMPT', 'L1 scan-layers.md:37 has no record (records at 35, 36, 38); Codex raised only the credential-storage atom, the whole line is unrepresented.')
d('CIS-K1-U0036', 'FACET_OF_EXISTING', 'CL11-SCAN-LOCAL-ACCOUNTS', 'APPEND', 'FG-K1-8e0b256c02', 'DROPPED_ATOM', 'Credential storage dropped from the K1 record of the same sentence.')
# CL12 secrets/config.
d('CIS-L0-U0042 CIS-L0-U0043 CIS-L0-U0044', 'ALREADY_COVERED', 'CL12-SCAN-SECRETS-CONFIG', note='NCP-L0-0001 (v1 R21 proposal record) states every atom of L0 scan-layers.md:20.')
d('CIS-K1-U0032 CIS-K1-U0033', 'FACET_OF_EXISTING', 'CL12-SCAN-SECRETS-CONFIG', 'APPEND', 'AUG1-NC-CIS-K1-0005-a', 'DROPPED_ATOM')
d('CIS-L1-U0036 CIS-L1-U0037', 'FACET_OF_EXISTING', 'CL12-SCAN-SECRETS-CONFIG', 'APPEND', 'AUG1-NC-CIS-L1-0009-a', 'DROPPED_ATOM')
d('CIS-K0-U0046 CIS-K0-U0047', 'FACET_OF_EXISTING', 'CL12-SCAN-SECRETS-CONFIG', 'APPEND', 'AUG1-NC-CIS-K0-0012-a', 'DROPPED_ATOM')
# CL13 uploads.
d('CIS-M1-U0049 CIS-M1-U0050', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL13-SCAN-UPLOADS', 'ADD', 'V3A-M1-101', 'SCAN_PROMPT', 'Only the SEC-015 MIME record (MUST_NOT, a different action) cites 205-207.')
d('CIS-L0-U0045 CIS-L0-U0046', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL13-SCAN-UPLOADS', 'ADD', 'V3A-L0-102', 'SCAN_PROMPT', 'L0 scan-layers.md:46 has no record.')
d('CIS-L1-U0041 CIS-L1-U0042', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL13-SCAN-UPLOADS', 'ADD', 'V3A-L1-102', 'SCAN_PROMPT', 'L1 scan-layers.md:45 has no record.')
d('CIS-K0-U0050 CIS-K0-U0051', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL13-SCAN-UPLOADS', 'ADD', 'V3A-K0-102', 'SCAN_PROMPT', 'Only the SEC-015 MIME record cites K0 129.')
# CL14 SSRF.
d('CIS-M1-U0047', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL14-SCAN-SSRF', 'ADD', 'V3A-M1-102', 'SCAN_PROMPT', 'M1 100-104 records only the false-positive guards (different action and modality).')
d('CIS-L1-U0038', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL14-SCAN-SSRF', 'ADD', 'V3A-L1-103', 'SCAN_PROMPT', 'FG-L1-844366a741 on line 26 states only the false-positive half.')
d('CIS-K0-U0048', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL14-SCAN-SSRF', 'ADD', 'V3A-K0-103', 'SCAN_PROMPT', 'K0 scan-layers.md:69 has no record.')
d('CIS-K1-U0034', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL14-SCAN-SSRF', 'ADD', 'V3A-K1-101', 'SCAN_PROMPT', 'K1 scan-layers.md:63 has no record.')
# CL15 raw HTML.
d('CIS-M1-U0048', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL15-SCAN-RAW-HTML', 'ADD', 'V3A-M1-103', 'SCAN_PROMPT', 'FG-M1-9856d9cf83 (false-positive guard) is the only record near 108-112.')
d('CIS-L1-U0039', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL15-SCAN-RAW-HTML', 'ADD', 'V3A-L1-104', 'SCAN_PROMPT', 'L1 scan-layers.md:27 has no record.')
d('CIS-K0-U0049', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL15-SCAN-RAW-HTML', 'ADD', 'V3A-K0-104', 'SCAN_PROMPT', 'K0 scan-layers.md:73 has no record.')
d('CIS-K1-U0035', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL15-SCAN-RAW-HTML', 'ADD', 'V3A-K1-102', 'SCAN_PROMPT', 'K1 scan-layers.md:67 has no record.')
# CL16 logging.
d('CIS-M1-U0051 CIS-M1-U0052', 'FACET_OF_EXISTING', 'CL16-SCAN-LOGGING', 'APPEND', 'FG-M1-7c88da0f41', 'DROPPED_ATOM')
d('CIS-L1-U0043 CIS-L1-U0044', 'FACET_OF_EXISTING', 'CL16-SCAN-LOGGING', 'APPEND', 'FG-L1-5821a256da', 'DROPPED_ATOM')
d('CIS-K1-U0037 CIS-K1-U0038', 'FACET_OF_EXISTING', 'CL16-SCAN-LOGGING', 'APPEND', 'FG-K1-112ed0f2b3', 'DROPPED_ATOM')
d('CIS-K0-U0052 CIS-K0-U0053', 'CANDIDATE_UNREPRESENTED_DUTY', 'CL16-SCAN-LOGGING', 'ADD', 'V3A-K0-105', 'SCAN_PROMPT', 'Only the SEC-010 never-log rule (MUST_NOT, a different action) cites K0 139.')
# CL17.
d('CIS-K1-U0013 CIS-L1-U0016', 'NON_NORMATIVE', 'CL17-SCAN-TARGETED-PRIORITY', kind='PROCEDURAL_TABLE_DETAIL')
# Singletons.
d('CIS-K1-U0011', 'FACET_OF_EXISTING', 'CL18-K1-DOMAIN-QUALIFIER', 'APPEND', 'FG-K1-5953b8f383', 'QUALIFIER')
d('CIS-K1-U0012', 'FACET_OF_EXISTING', 'CL19-CATCH-CLEANUP-QUALIFIER', 'APPEND', 'FG-K1-770fc67286', 'QUALIFIER', 'FG-K1-6d5d64d4fe gets the same qualifier.')
d('CIS-M1-U0014', 'FACET_OF_EXISTING', 'CL20-LOG-TECH-IDS', 'APPEND', 'FG-M1-064c990ec0', 'DROPPED_ATOM')
d('CIS-M1-U0021', 'NON_NORMATIVE', 'CL21-M1-SECTION-REF-HEURISTIC', kind='CHECKER_HEURISTIC', note='Kept OPEN as an enforcement-strength observation.')
d('CIS-K0-U0017', 'FACET_OF_EXISTING', 'CL22-K0-USECASE-QUERIES', 'APPEND', 'FG-K0-2f3f94690d', 'DROPPED_ATOM')
d('CIS-K0-U0018', 'NON_NORMATIVE', 'CL23-K0-PROGRAM-EXPOSURE', kind='TECHNIQUE')
d('CIS-L0-U0010', 'NON_NORMATIVE', 'CL24-L0-XSRF-NAMES', kind='TECHNIQUE')
d('CIS-L0-U0017', 'NON_NORMATIVE', 'CL25-L0-MIGRATION-ARTIFACTS', kind='ADVISORY_TECHNIQUE')
d('CIS-L0-U0047', 'NON_NORMATIVE', 'CL26-L0-MALFORMED-MESSAGE', kind='IMPLEMENTATION_DETAIL')
d('CIS-M-U0033', 'NON_NORMATIVE', 'CL27-M-PRESENTATION-EVENTS', kind='TECHNIQUE')
d('CIS-M-U0034', 'NON_NORMATIVE', 'CL28-M-499-EXAMPLE', kind='ILLUSTRATIVE_EXAMPLE')
d('CIS-M1-U0022', 'FACET_OF_EXISTING', 'CL29-M1-CAPABILITY-METADATA', 'APPEND', 'FG-M1-28892c03c6', 'LOADING_RESTRICTION')
d('CIS-M1-U0053', 'ALREADY_COVERED', 'CL30-M1-CREATEDAT', kind='TECHNIQUE_OF_COVERED_DUTY')

# Census additions: same shared prompt, not raised by Codex, verified at source in v3 (scan_census.py). Reported separately from Codex counts.
CENSUS = [
    dict(id='V3C-L0-SSRF', candidate='L0', cluster='CL14-SCAN-SSRF', action='ADD', target='V3A-L0-103', note='L0 scan-layers.md:27 SSRF prompt; only the false-positive half is recorded (FG-L0-003b744c82).'),
    dict(id='V3C-M-RAWHTML', candidate='M', cluster='CL15-SCAN-RAW-HTML', action='ADD', target='V3A-M-101', note='M scan-layers.md:120-121 raw HTML sentence; no record.'),
    dict(id='V3C-L1-CREDURL', candidate='L1', cluster='CL12-SCAN-SECRETS-CONFIG', action='APPEND', target='AUG1-NC-CIS-L1-0009-a', note='Credentialed-URL and certificate-bypass atoms of the same sentence.'),
    dict(id='V3C-K0-CREDURL', candidate='K0', cluster='CL12-SCAN-SECRETS-CONFIG', action='APPEND', target='AUG1-NC-CIS-K0-0012-a', note='Credentialed-URL and certificate-bypass atoms of the same sentence.'),
    dict(id='V3C-K1-CREDURL', candidate='K1', cluster='CL12-SCAN-SECRETS-CONFIG', action='APPEND', target='AUG1-NC-CIS-K1-0005-a', note='Credentialed-URL and certificate-bypass atoms of the same sentence.'),
    dict(id='V3C-K1-UPLOADPUB', candidate='K1', cluster='CL13-SCAN-UPLOADS', action='APPEND', target='FG-K1-94b2ab5757', note='Public-serving atom dropped from the K1 upload record.'),
    dict(id='V3C-L0-RAWHTML-ABSENT', candidate='L0', cluster='CL15-SCAN-RAW-HTML', action='NONE', target=None, note='L0 has no raw-HTML sentence: a real text difference, recorded, not homogenized.'),
    dict(id='V3C-L0-CLEANUP', candidate='L0', cluster='CL19-CATCH-CLEANUP-QUALIFIER', action='NONE', target=None, note='L0 aspnet-error-handling:109 carries the same qualifier and FG-L0-9856a2b2b0 already records it.'),
]
