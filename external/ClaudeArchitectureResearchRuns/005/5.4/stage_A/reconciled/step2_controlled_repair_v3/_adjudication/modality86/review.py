"""Individual source review of the 86 records in v2 MARKED_NEVER_SOFT_MODALITY.jsonl (kit 74 A.6). Read from `SHEET.md` (claim, canonical
policies with tags, every cited source range on current bytes) and, where needed, the peer records of the same text in other candidates.

Reading rule (approved): Step 2 addendum A1.3 - an unmarked positive imperative in a knowledge skill or private reference is DEFAULT unless the
source says must, never or do not; v2 C07 applied "a marked form" to a ban stored DEFAULT. A record is corrected only when its operative
content is a marked ban that no default marker governs. A compound record keeps the modality of its leading clause.

Reason codes:
  DEFAULT_MARKED        the candidate marks the bullet itself as a default ("Default:", "(default)", "by default"), and the ban sits inside it
  COMPOUND_POLICY       the record restates a DEFAULT-tagged canonical policy whose own text contains the same ban; leading clause is the default
  COMPOUND_TECHNIQUE    knowledge or reference text: a positive technique clause plus a ban atom in one record
  UNMARKED_SOURCE       the cited source has no must, never or do not for this clause; "never" is the claim's paraphrase (A1.3 -> DEFAULT)
  RESULT_CLAUSE         "never" sits in a purpose clause ("so a test can never reach ..."); the imperative is positive
  DESCRIPTIVE           "never" describes a fact or an example comment, not a duty
  TRIGGER_WORDING       "must not" belongs to the trigger ("when a POST must not create duplicate effects")
  CHECK_BY_REFERENCE    a review or check-list item that checks an owner rule
  DUPLICATE_MARKED      the marked ban is already stored as MUST_NOT in another record of the same candidate
  OWNER_MARKED_DEFAULT  the line restates an owner rule that marks it default (and v2 C02 harmonized it in all six)
  MARKED_BAN_ONLY       the record's operative content is a marked ban with no default marker: corrected
  CATALOGUE_BORDERLINE  a status-code catalogue entry; marked word in definitional form; kept and qualified
"""
UPHELD, CORRECTED, QUALIFIED = 'UPHELD', 'CORRECTED', 'QUALIFIED'
ROWS = [
    (1, 'FG-M-8b2c02178e', CORRECTED, 'MARKED_BAN_ONLY', 'M rules/angular.md:19-20 "Do not introduce NgModules for ordinary feature development unless an integration or legacy dependency genuinely requires them." The record holds only that ban, already marked STRONGER than FE-001 (DEFAULT). M1 stores the same sentence MUST_NOT (FG-M1-044b0b5804, FG-M1-4979ad121a). No default marker governs the sentence. Modality DEFAULT -> MUST_NOT; equivalence stays STRONGER, so no coverage or strength cell moves.'),
    (2, 'FG-M-3d4adb9bb8', UPHELD, 'COMPOUND_POLICY', 'FE-008 (DEFAULT) itself says "do not put feature business logic in interceptors"; the record restates the whole policy, led by "Prefer".'),
    (3, 'FG-M-9eb9149a91', UPHELD, 'COMPOUND_POLICY', 'Same as row 2.'),
    (4, 'FG-M-b3b041caea', UPHELD, 'COMPOUND_POLICY', '"... by default. Keep ... stable and safe; clients must not depend on human-readable exception messages." API-002 DEFAULT; compound led by the default clause.'),
    (5, 'FG-M-46692dda34', UPHELD, 'COMPOUND_POLICY', 'SEC-009 (DEFAULT) contains the same never-clause. M writes the ban as a separate "Never" sentence after "by default"; L1, K0 and K1 put the identical ban inside a "Default:" bullet. Stored DEFAULT is the reading consistent with peers; the ban sentence alone reads as marked.'),
    (6, 'FG-M-cbf3f9c7ca', UPHELD, 'COMPOUND_TECHNIQUE', 'Docker knowledge skill: copy order technique plus "do not optimize caching at the cost of" a correct restore graph.'),
    (7, 'FG-M-4c6848938a', UPHELD, 'COMPOUND_TECHNIQUE', 'Docker knowledge skill: exclude list plus two "do not/never exclude" atoms.'),
    (8, 'FG-M-5554cb6a56', UPHELD, 'UNMARKED_SOURCE', 'http-api:87-89 "It ... is not a generic nothing-changed business response" - unmarked.'),
    (9, 'FG-M1-d578d58cec', UPHELD, 'DEFAULT_MARKED', '"By default use ProblemDetails ...; ... do not make human-readable exception messages the machine-readable contract." One default-marked bullet.'),
    (10, 'FG-M1-4041e9946d', UPHELD, 'COMPOUND_POLICY', '"By default configure CORS ... Never combine ..." SEC-009 contains the ban; see row 5.'),
    (11, 'FG-M1-d40a6d8879', UPHELD, 'COMPOUND_TECHNIQUE', 'Docker knowledge skill, as row 6.'),
    (12, 'FG-M1-817d6aa28e', UPHELD, 'RESULT_CLAUSE', '"Configure the Testing environment ... so an integration test can never reach a development or production database."'),
    (13, 'FG-M1-43f86b8d6e', UPHELD, 'UNMARKED_SOURCE', 'Same text as row 8.'),
    (14, 'FG-M1-9c90b5afe5', UPHELD, 'COMPOUND_TECHNIQUE', '429 catalogue entry: positive usage plus "Do not represent validation failure as rate limiting".'),
    (15, 'FG-M1-ea0ffa3ad3', UPHELD, 'TRIGGER_WORDING', '"Repeated POSTs that must not duplicate effects" is the condition; the duty is "consider an Idempotency-Key".'),
    (16, 'FG-M1-10e0d3df19', UPHELD, 'COMPOUND_TECHNIQUE', 'Resilience reference: positive conditional mechanism plus "do not claim exactly-once".'),
    (17, 'FG-M1-e454380f27', UPHELD, 'CHECK_BY_REFERENCE', 'swagger:127-130 is a "Check-by-reference against api.md" list item; SHOULD_NOT kept.'),
    (18, 'FG-L0-43aba8cb71', UPHELD, 'DEFAULT_MARKED', 'runtime-principles.md:29 ends "(default)".'),
    (19, 'FG-L0-e46fe0c51d', UPHELD, 'DEFAULT_MARKED', 'security-principles.md:48 ends "(default)".'),
    (20, 'FG-L0-935de5cafe', UPHELD, 'DEFAULT_MARKED', 'testing-principles.md:22 ends "(default)".'),
    (21, 'FG-L0-b82180d4f0', UPHELD, 'DUPLICATE_MARKED', 'Primary anchor testing-principles.md:22 is "(default)". The marked InMemory ban of dotnet-testing.md:15 is already stored MUST_NOT with code PC in FG-L0-dafd319636. The claim wording "never verifies" is a paraphrase of that ban.'),
    (22, 'FG-L0-cb59306d5a', UPHELD, 'DEFAULT_MARKED', 'angular.md:16 ends "(default)".'),
    (23, 'FG-L0-6c42674c92', UPHELD, 'COMPOUND_POLICY', 'Layout record restating DEP-024 (DEFAULT); the frontend-test ban is stored separately at MUST_NOT (FG-L0-a2e9e91e8f, v2 C07).'),
    (24, 'FG-L0-8fdc2119a4', UPHELD, 'UNMARKED_SOURCE', 'caching:22 "Add a distributed backend such as Redis only when deployment requires it"; :80 is an avoid list.'),
    (25, 'FG-L0-ffb2b22b51', UPHELD, 'UNMARKED_SOURCE', 'configuration:14 "the problem is ordinary services parsing configuration keys" - descriptive; the claim "must not" is stronger than the source (noted).'),
    (26, 'FG-L0-96fb099860', UPHELD, 'RESULT_CLAUSE', 'As row 12.'),
    (27, 'FG-L0-c3af8cbd51', UPHELD, 'DESCRIPTIVE', '"never with a body" comes from the example comment at http-api:26 ("// 204 - never with a body"); the cited line 31 is unmarked.'),
    (28, 'FG-L0-8e69addc81', UPHELD, 'COMPOUND_TECHNIQUE', 'Table row "429 + Retry-After when known (never for validation failures)".'),
    (29, 'FG-L0-958d10ac79', UPHELD, 'COMPOUND_TECHNIQUE', 'List of typical 409 cases plus "409 is never for malformed syntax".'),
    (30, 'FG-L0-fe665ffb2e', UPHELD, 'TRIGGER_WORDING', '"When a repeated POST must not duplicate effects, consider ..." - the claim holds no ban.'),
    (31, 'FG-L0-08f3f22030', UPHELD, 'UNMARKED_SOURCE', 'resilience:22 "Not retried: ..." - a declarative list.'),
    (32, 'FG-L0-d98980588e', UPHELD, 'COMPOUND_TECHNIQUE', 'Swagger knowledge skill: four duties in one record, one of them "never 204 for an endpoint that returns a body".'),
    (33, 'FG-L1-d3d7aff321', UPHELD, 'DEFAULT_MARKED', 'backend-code.md:27 "Default: ...; never retry indefinitely or aggressively."'),
    (34, 'FG-L1-d3d5128af8', UPHELD, 'DEFAULT_MARKED', 'security.md:34 "Default: ..."'),
    (35, 'FG-L1-b81a052976', UPHELD, 'DEFAULT_MARKED', 'security.md:44 "Default: ..."'),
    (36, 'FG-L1-7799d8e5a3', UPHELD, 'DEFAULT_MARKED', 'testing.md:15 "Default: ..."'),
    (37, 'FG-L1-af402598cd', UPHELD, 'DEFAULT_MARKED', 'framework.md:12 "Default: ..."'),
    (38, 'FG-L1-5b3d19f6e1', UPHELD, 'DEFAULT_MARKED', 'decisions.md:23 "Default: ...; never create a separate top-level tests directory."'),
    (39, 'FG-L1-0df90c10a3', UPHELD, 'UNMARKED_SOURCE', 'As row 25.'),
    (40, 'FG-L1-006f30678e', UPHELD, 'RESULT_CLAUSE', 'As row 12.'),
    (41, 'FG-L1-2fcae61e4c', UPHELD, 'RESULT_CLAUSE', 'As row 12.'),
    (42, 'FG-L1-17563c1d71', UPHELD, 'COMPOUND_TECHNIQUE', 'health-check:41: two positive duties plus "never misuse liveness for that".'),
    (43, 'FG-L1-ba40759ad1', UPHELD, 'COMPOUND_TECHNIQUE', 'Same line as row 42; positive readiness duty leads.'),
    (44, 'FG-L1-c619ceab7d', UPHELD, 'DESCRIPTIVE', '"a 204 never carries a body" states the status code semantics.'),
    (45, 'FG-L1-5f5febf5c6', QUALIFIED, 'CATALOGUE_BORDERLINE', 'http-api:23 "304 Not Modified - only for conditional requests ...; never a generic nothing-changed business response." A usage restriction written as a catalogue definition. M, M1, L0, K0 and K1 state the same restriction unmarked ("is not"), all stored DEFAULT. MUST_NOT would also be defensible; not a proved error. Kept DEFAULT; a strictness comparison must not rest on it.'),
    (46, 'FG-L1-0950048568', UPHELD, 'COMPOUND_TECHNIQUE', '400 catalogue entry plus "Never use 400 for authentication failure."'),
    (47, 'FG-L1-cc71eb4b32', UPHELD, 'COMPOUND_TECHNIQUE', '429 catalogue entry plus "Never use it for validation failures."'),
    (48, 'FG-L1-7edf640541', UPHELD, 'TRIGGER_WORDING', 'As row 30.'),
    (49, 'FG-L1-56b4faff0f', UPHELD, 'DEFAULT_MARKED', '"never writes by default".'),
    (50, 'FG-L1-d9e53ef77a', UPHELD, 'COMPOUND_TECHNIQUE', 'As row 16.'),
    (51, 'FG-L1-695833d819', UPHELD, 'COMPOUND_TECHNIQUE', 'modern-csharp:10 "Use a feature when ... - never to demonstrate newer syntax."'),
    (52, 'FG-L1-affc5ed062', UPHELD, 'COMPOUND_TECHNIQUE', 'As row 32.'),
    (53, 'FG-K0-7e828bca09', UPHELD, 'DEFAULT_MARKED', 'testing.md:30 "Default: ... Never claim provider fidelity ..." in the same bullet.'),
    (54, 'FG-K0-0b760dcf90', UPHELD, 'DEFAULT_MARKED', 'caching.md:12 "Default: ..."'),
    (55, 'FG-K0-5b5c4399c8', UPHELD, 'DEFAULT_MARKED', 'csharp.md:16 "Default: ..."'),
    (56, 'FG-K0-a780dcbe8d', UPHELD, 'DEFAULT_MARKED', 'integrations.md:16 "Default: ..."'),
    (57, 'FG-K0-375972cdb2', UPHELD, 'DEFAULT_MARKED', 'security.md:32 "Default: ... Never combine ..." in the same bullet.'),
    (58, 'FG-K0-423d455e8b', UPHELD, 'DEFAULT_MARKED', 'angular.md:26 "Default: ..."'),
    (59, 'FG-K0-cad27bd55a', UPHELD, 'COMPOUND_POLICY', 'DEP-017 (DEFAULT) itself says "do not add the package before the project actually adopts versioning".'),
    (60, 'FG-K0-fc38775ad7', UPHELD, 'COMPOUND_TECHNIQUE', 'dotnet-testing:64: candidates list plus two "do not" atoms.'),
    (61, 'FG-K0-471485d7d2', UPHELD, 'TRIGGER_WORDING', '"When a repeated POST should not create duplicate effects ..."; "unlikely duplicates do not make" is descriptive.'),
    (62, 'FG-K0-71837faed7', UPHELD, 'UNMARKED_SOURCE', 'httpclient-factory:59 "... not business decisions" - unmarked.'),
    (63, 'FG-K0-50cf5b293c', UPHELD, 'DESCRIPTIVE', 'httpclient-factory:115 "mutating shared DefaultRequestHeaders concurrently ... is a race".'),
    (64, 'FG-K0-c37a23e0b6', UPHELD, 'UNMARKED_SOURCE', 'resilience:45 "use it only for operations safe to execute multiple times ... - not writes".'),
    (65, 'FG-K0-3e5746d904', UPHELD, 'UNMARKED_SOURCE', 'logging:65 "keep authorization headers and full request/response bodies out of logs" - a positive imperative pointing to the owner rule.'),
    (66, 'FG-K1-a42b272113', UPHELD, 'DEFAULT_MARKED', 'testing.md:17 "Default: ..."'),
    (67, 'FG-K1-e0ec24eec3', UPHELD, 'DEFAULT_MARKED', 'runtime.md:30 "Default: ..."'),
    (68, 'FG-K1-1741d36123', UPHELD, 'DEFAULT_MARKED', 'security.md:23 "Default: ..."'),
    (69, 'FG-K1-b030eec95c', UPHELD, 'DEFAULT_MARKED', 'security.md:32 "Default: ..."'),
    (70, 'FG-K1-455f584b69', UPHELD, 'DEFAULT_MARKED', 'frontend-framework.md:12 "Default: ... Interceptors stay cross-cutting and never contain feature business logic." in the same bullet.'),
    (71, 'FG-K1-44c62bf76d', UPHELD, 'UNMARKED_SOURCE', 'api-versioning:72 has no ban; :84 lists "silently removing deprecated versions" among things to avoid.'),
    (72, 'FG-K1-27ec97e6b7', UPHELD, 'COMPOUND_TECHNIQUE', 'Docker knowledge skill, as row 6.'),
    (73, 'FG-K1-b52915cf19', UPHELD, 'RESULT_CLAUSE', 'As row 12.'),
    (74, 'FG-K1-43d346afdf', UPHELD, 'COMPOUND_TECHNIQUE', 'dotnet-testing:105: known-state technique list led by a positive clause, plus "Never modify production data." (a marked atom; the binding isolation duty is TST-004, recorded at MUST elsewhere).'),
    (75, 'FG-K1-8c2a0fe6ef', UPHELD, 'OWNER_MARKED_DEFAULT', 'ef-core:128 restates rules/backend/runtime.md (RUN-008, DEFAULT); v2 C02 aligned this wording in all six.'),
    (76, 'FG-K1-79fc01688e', UPHELD, 'COMPOUND_TECHNIQUE', 'ef-core:221: prefer provider strategies, wrap transactions, "Do not apply HTTP retry policies to database operations."'),
    (77, 'FG-K1-e64089621e', UPHELD, 'COMPOUND_TECHNIQUE', 'Same line as row 76.'),
    (78, 'FG-K1-f32882b692', UPHELD, 'COMPOUND_TECHNIQUE', 'As row 42.'),
    (79, 'FG-K1-eb9159dea5', UPHELD, 'COMPOUND_TECHNIQUE', 'Multi-status catalogue record.'),
    (80, 'FG-K1-baa3231f95', UPHELD, 'COMPOUND_POLICY', 'API-002 (DEFAULT) with FE-009 as a second link; resolution SL already stored.'),
    (81, 'FG-K1-b120c4d4ff', UPHELD, 'COMPOUND_TECHNIQUE', '"prefer respecting it ...; never hammer a rate-limited dependency".'),
    (82, 'FG-K1-797447c104', UPHELD, 'DEFAULT_MARKED', '"never for state-changing operations by default".'),
    (83, 'FG-K1-b9ca80d31e', UPHELD, 'COMPOUND_TECHNIQUE', 'As row 16.'),
    (84, 'FG-K1-17425a17b2', UPHELD, 'COMPOUND_TECHNIQUE', 'Log-level catalogue; "never assume sensitive data is safe at these levels" is one atom.'),
    (85, 'FG-K1-112ed0f2b3', UPHELD, 'CHECK_BY_REFERENCE', 'scan-layers:129 "Check for passwords ... in logs"; stored code CK.'),
    (86, 'FG-K1-de49663227', UPHELD, 'COMPOUND_TECHNIQUE', 'scan-layers:141 choose-by-requirement list plus "custom cryptography is never the answer".'),
]
OUT_OF_CLASS_OBSERVATIONS = [
    'The class was found by the words "never" and "must not". Records that say "do not" were not in it. Example: L1 FG-L1-34be702ec3 ("Do not introduce NgModules ...", knowledge skill) is DEFAULT while M (after this change) and M1 store the same ban MUST_NOT. Not reviewed here; raw MUST_NOT counts stay unusable as a strictness measure.',
    'FG-L0-ffb2b22b51 and FG-L1-0df90c10a3 say "ordinary services must not parse configuration keys" where the source says "the problem is ordinary services parsing configuration keys": the claim is stronger than the line; modality DEFAULT is the source reading.',
]
