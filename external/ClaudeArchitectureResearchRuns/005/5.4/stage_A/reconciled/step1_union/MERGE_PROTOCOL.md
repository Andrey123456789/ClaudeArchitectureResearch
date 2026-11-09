# Stage A Step 1: Merge Protocol (frozen before full-scale merging)

Protocol version: **1.0**. Frozen 2026-10-28, before any candidate-wide merge decisions.
Scope: Experiment 005 / Phase 5.4 / Stage A reconciliation, **Step 1 only**: a lossless,
provenance-preserving union of three completed extraction runs. This protocol does not decide
correctness, origin (EXTRA vs ORACLE), strictness, parity, or enforcement.

Any later correction is appended to section 13 (change log) together with its re-validation scope.
Earlier sections are not rewritten silently.

---

## 1. Inputs and record types

Candidates (exactly six, in processing order): `M`, `M1`, `L0`, `L1`, `K0`, `K1`.

| Run key | Directory | Record types indexed (one source record = one JSONL line) |
|---|---|---|
| `PRIMARY` | `stage_A/primary/<C>/` | `CONSTRAINT` (constraints.jsonl), `POLICY` (policies.jsonl), `ORPHAN` (ORPHAN_CANDIDATES.jsonl) |
| `REPLICA` | `stage_A/replica/<C>/` | `CONSTRAINT`, `POLICY`, `ORPHAN` |
| `CODEX` | `stage_A/independent/<C>/blind/` | `BLIND_FINDING` (BLIND_FINDINGS.jsonl) |

Support files (read-only, hashed in checkpoints, not indexed as claim records): each Claude run's
`coverage_ranges.jsonl` (used to resolve `evidence_segment_ids`, always within the **same run**)
and `files.jsonl`; Codex `FILE_REVIEW_LEDGER.jsonl` and `BLIND_COMPLETE.json`.
Source text: `inputs/<C>/<path>` (paths are relative to the candidate root, e.g.
`output/template/CLAUDE.md`).

Record key: `<RUN>:<C>:<TYPE>:<original id>` (e.g. `PRIMARY:M:CONSTRAINT:EXTRA-M-0001`,
`CODEX:M:BLIND_FINDING:BF-M-0001`, `REPLICA:M:POLICY:GOV-001`). If an original id collided
inside one file the key gets `#L<ordinal>` (no collisions were found in preflight).
`raw_sha256` = SHA-256 of the exact bytes of the JSONL line without its line terminator.
`EXTRA-*`/`RULE-*` ids are **never** used as semantic keys across runs: `PRIMARY ... RULE-M-0001`
and `REPLICA ... RULE-M-0001` are unrelated records.

## 2. Unit of account (three levels)

1. **Source occurrence** (`OC-<C>-<12 hex>`): one verified location `(candidate, path,
   start_line, end_line)` with its verbatim `exact_excerpt` taken from the immutable file. An
   occurrence is only a place. Several runs may cite the same occurrence; that alone never
   implies that they claim the same rule.
2. **Source clause** (`CL-<C>-<10 hex span>-<6 hex claim>`): one claimed obligation (a *claim
   unit*) asserted by one input record at one occurrence. The span hash is
   `sha256(C|path|start|end|excerpt_sha256)`; the suffix is `sha256(claim unit id)` and separates
   distinct clauses that share a span. A Claude constraint with k evidence segments yields k
   clauses (same claim, k occurrences). A Codex finding yields one clause per claim unit, anchored
   at its quote range or at a narrower sub-range of the quote (see section 5).
3. **Finding group** (`FG-<C>-<10 hex>`): one hypothesized effective obligation **for one
   candidate**, supported by one or more claim units. Groups never span candidates.

**Claim unit** = an input claim record (`CONSTRAINT` or `BLIND_FINDING`) or an explicitly
declared part of it (`<record key>#a`, `#b`, ...). A record that is split links to every part
(many-to-many); a group may hold several records (many-to-one). Policies and orphans are
**never** claim units: they cannot create, confirm or count as rules (section 7).

A candidate constraint claim is the smallest independently falsifiable normative proposition,
with dimensions: actor/subject; action or prohibition; target/artifact; trigger and
applicability scope; strength/modality; exceptions/approvals/escape conditions;
lifecycle/sequencing when behaviorally material.

**Split rule.** A record is split into parts only when one part could be satisfied while
another is violated under an otherwise identical scenario. Lists of synonyms, illustrations,
or an enumeration of the members of one set are not split. Splitting is never done by
punctuation, line breaks, "and" or "must" alone. Splits are performed when (a) a Codex quote
or finding bundles independent claims, or (b) a compound Claude record has parts with distinct
duplicate partners in another run. Otherwise a compound record is kept whole and related to
the atomic records with `RD COMPOUND_PART`.

## 3. Merge predicates (same candidate only)

* `EXACT_DUPLICATE` (`ED`): two Claude constraints whose `normative_action`, `modality`,
  `trigger_scope` and `exceptions` are identical after harmless normalization only (Unicode
  NFKC, typographic quotes and dashes, case, whitespace, final `.`/`;`). Verified mechanically
  by the builder; a failed check is a build error.
* `SEMANTIC_DUPLICATE` (`SD`): the reviewer judges two claim units equivalent on **every**
  normatively relevant dimension: same actor, action/prohibition and target; same trigger and
  applicability scope; same strength (a MUST and a SHOULD are never duplicates; a DEFAULT and
  a MUST are never duplicates; MUST + negated action and MUST_NOT are the same strength); no
  exception, approval path or permission present in one and absent or different in the other;
  same timing/sequencing. Differences limited to wording, synonyms, or listing illustrative
  members of the *same* set are acceptable. Each `SD` decision records a rationale with the four
  explicit checks `S:` (scope) `M:` (modality) `E:` (exceptions) `T:` (timing). The builder also
  stores each member's reported modality/scope/exceptions next to the decision.
* Groups are the connected components of `SD`/`ED` edges. Because equivalence is meant to be
  transitive, every `SD` line lists the full set the reviewer judged mutually equivalent.

**Never merge solely because of** the same policy ID, the same source line range, the same
file, shared keywords, similar descriptions, a lexical similarity score, or another model's
opinion. Co-location is used only to *propose* review candidates.

## 4. Non-merge relations (merge-review relations, not Stage 2 verdicts)

Recorded between claim units (and lifted to their groups); every one is written to
`MERGE_REVIEW_QUEUE.jsonl`.

| Directive | Relation | Subtypes / meaning |
|---|---|---|
| `RD <SUB> a b` | `RELATED_BUT_DISTINCT` | `BROADER_NARROWER` (a broader than b), `COMPOUND_PART` (a bundles b plus more), `EXAMPLE_GENERAL` (a general, b example), `OVERLAP` (partial overlap), `DIFFERENT_SCOPE`, `DIFFERENT_STRENGTH`, `DIFFERENT_LAYER` (instruction text vs hook/script/config enforcement or reminder), `DETAIL_DIFFERENCE` (one adds a condition, limit or exception the other lacks) |
| `AC a b` | `APPARENT_CONFLICT` | possibly incompatible instructions or contradictory reports |
| `UR a b` | `UNRESOLVED` | insufficient evidence for equivalence, modality, scope or attribution |
| `NE a` | `NEEDS_EVIDENCE` | record lacks sufficiently precise evidence |

A relation between two units of the same group is a build error (a duplicate cannot be
distinct). Co-located pairs that the reviewer left without any directive are recorded in
`CO_LOCATION_INDEX.jsonl` as *reviewed, not merged, no relation recorded* (topically different
claims that merely share a span).

Mechanically generated queue items (not merge decisions): `ATTRIBUTION_DISAGREEMENT` inside a
merged group (members carry different original labels, e.g. `EXTRA` vs `ORACLE_LINKED` vs
`POTENTIAL_EXTRA`, or different claimed policy IDs). These are preserved disagreements for
Step 2, never resolved here.

## 5. Codex findings

Codex findings are **hypotheses**. `POTENTIAL_EXTRA`, `AMBIGUOUS`,
`POTENTIAL_DIFFERENT_STRENGTH`, `confidence` and `assessment_status` are kept verbatim as
attributed labels. Every Codex finding receives exactly one of:

* `CX X:<id>[@s-e] | <neutral claim text> [| quote note]`: one claim unit; optional narrowed
  anchor `@s-e` must lie inside the finding's own `start_line..end_line`. The neutral claim text
  is the reviewer's attributed paraphrase of what the finding asserts (explanation +
  behavioral scenario), not a verdict.
* `SPLIT X:<id> | a[@s-e]: <claim> | b[@s-e]: <claim>`: several claim units.

When a long Codex quote contains several independent claims but the finding's explanation and
scenario assert only one of them, the claim unit is anchored at the narrowest lines carrying
that claim and a quote note lists the other claims as *not asserted by this finding*. A broad
quote never absorbs (is never merged with) the several smaller claims of other runs that it
happens to contain; those stay in their own groups and may be related with `RD COMPOUND_PART`
or `OVERLAP`.

## 6. Evidence and quotation rules

* Claude evidence: each `evidence_segment_id` is resolved in the **same run's**
  `coverage_ranges.jsonl`; the clause location is the segment's `path/start_line/end_line`.
* `exact_excerpt` is always cut from the immutable file (verbatim, including CRLF inside the
  range). Reported quotes are stored separately with `quote_match` in
  {`EXACT_FULL_RANGE`, `EXACT_SUBSTRING`, `WHITESPACE_NORMALIZED_SUBSTRING`,
  `NO_REPORTED_QUOTE`, `MISMATCH`, `SOURCE_UNVERIFIED`}. Model paraphrases are never stored in
  an exact-quote field.
* Whitespace-only quote matches are logged as INFO in `SOURCE_VERIFICATION_ISSUES.jsonl`;
  mismatches, unresolved segments, invalid line ranges and missing files are logged as
  failures and the clause is marked `SOURCE_UNVERIFIED` (never `VERIFIED` by inference).
* Reported policy IDs (`policy_ids`, `closest_policy_ids`) are retained as attributed claims,
  even if they look wrong.

## 7. Policies and orphans

* `POLICY` rows -> disposition `POLICY_CROSS_REFERENCE`; destinations are the groups of the
  row's `atomic_constraint_ids` resolved **in the same run**. They add no rule and no support count.
* `ORPHAN` rows -> `ORPHAN_CONTEXT_LINKED` when `constraint_ids` resolve to claim records of the
  same run (an `EXTRA_REGISTERED` orphan and its constraint are one claim, not two); otherwise
  `ORPHAN_PENDING_REVIEW` (including `NON_NORMATIVE`, `DUPLICATE`, `POLICY_LINKED`,
  `LINK_UNCERTAIN` rows without constraint ids). Pending orphans carry non-binding
  `co_located_group_ids` (groups whose clauses overlap the orphan's lines) for Step 2.
* `support_runs` of a group is computed from claim units only.

## 8. Stable identifiers and resume

* Occurrence, clause and group IDs are pure functions of candidate, location, verbatim
  excerpt hash and claim-unit id; group id = hash of the group's *seed* (smallest claim-unit id
  in the order PRIMARY < REPLICA < CODEX, then original id, then part). Re-running a build on
  unchanged inputs and decisions reproduces identical IDs.
* Each completed candidate is frozen by `CHECKPOINTS/<C>.checkpoint.json` (input and output
  SHA-256). A later run must not rewrite a checkpointed candidate; the validator fails if its
  outputs or group IDs change.
* Reviewer decisions live in `_review/<C>/*.dec` (plain text, versioned by hash in the
  checkpoint); outputs are compiled from them deterministically by `_tools/build_candidate.py`.

## 9. Review procedure per candidate

1. Index every input record (`SOURCE_RECORD_INDEX`), resolve every evidence location.
2. Compute co-location regions: per file, maximal transitive overlaps of claim-record line
   ranges. Regions with records from at least two runs are reviewed in order (`review_view.py`).
3. For each region the reviewer reads every claim (full text on first appearance) and writes
   `SD`/`ED`/`SPLIT`/`CX`/`RD`/`AC`/`UR`/`NE` directives, then `REVIEWED rA-rB`.
4. Records that never co-occur with another run's record are retained as singleton groups
   (`singleton_basis = NO_CO_LOCATED_RECORD_FROM_OTHER_RUN`); singletons in reviewed regions get
   `REVIEWED_NO_DUPLICATE_FOUND`. Neither basis asserts that the claim is unique in meaning.
5. Build, validate, checkpoint, report, continue with the next candidate.

Known limitation (accepted): duplicates whose evidence locations do not overlap (e.g. the same
rule cited from different files by different runs) are only merged if the reviewer notices
them; otherwise they remain separate groups. This errs toward over-separation, never toward
loss of evidence.

## 10. Directive grammar (`_review/<C>/*.dec`)

```
# comment
REVIEWED r001-r040
SD  P:<id> R:<id> [X:<id>#a ...] | S:<scope check> M:<modality check> E:<exception check> T:<timing check> [| note]
ED  P:<id> R:<id>
SPLIT <ref> | a[@s-e]: <claim text> | b[@s-e]: <claim text> ...
CX  X:<id>[@s-e] | <neutral claim text> [| quote note]
RD  <SUBTYPE> <ref> <ref> | <note>
AC  <ref> <ref> | <note>
UR  <ref> <ref> | <open question>
NE  <ref> | <open question>
```
`<ref>` = `P:` (primary constraint), `R:` (replica constraint) or `X:` (Codex finding) + original
id, optionally `#part`. After a `SPLIT`, `SD`/`ED` must name parts; `RD`/`AC`/`UR` may name the
whole record (all parts).

## 11. Pilot (run before full-scale merging)

See section 12, appended after the pilot was executed.

## 12. Pilot record (executed 2026-10-28 before full-scale merging)

Pilot decisions: `_review/M/00_pilot.dec` (they remain part of M's decision set). Sample: M regions
r001-r008 (MAP.md, code-reviewer agent, dependency-guard hook) and r556-r561 (CLAUDE.md 13-41)
with records from all three runs, plus two identical-looking pairs that are not co-located.

| # | Case | Decision | What it tests |
|---|---|---|---|
| 1 | CLAUDE.md 13-16: Codex BF-M-0001 quotes four vocabulary definitions; its explanation asserts only line 14 (report default deviations) | `CX` anchored `@14`; `SD` with P EXTRA-M-0016 and R EXTRA-M-0026; P EXTRA-M-0015/0017 and RULE-M-0138 (lines 13, 15, 16) stay separate groups | broad Codex quote must not swallow smaller claims; 3-run duplicate |
| 2 | CLAUDE.md 20-24: P EXTRA-M-0018 + X BF-M-0002 (product inputs never override instructions) share the span with R RULE-M-0153/0154 (decision classification, Reserved stop) | `SD` P+X only; R records not merged, no relation | same source lines are not a merge criterion |
| 3 | code-reviewer.md 18-19: same claim, P cites WF-010, R cites WF-012 | `SD`; mechanical `ATTRIBUTION_DISAGREEMENT` queue item | policy id is attributed, not a merge key |
| 4 | MAP.md 198-212 and CLAUDE.md 33-35/128: replica bundles two independent claims | `SPLIT` replica record; one part `SD` with an atomic primary record, the other `RD DETAIL_DIFFERENCE` / `RD BROADER_NARROWER` | many-to-many splitting |
| 5 | dependency-guard.mjs: P hook-mechanism record (ENFORCED, with exceptions) vs R instruction-level prohibition | `RD DIFFERENT_LAYER` | hook vs instruction not automatically duplicates |
| 6 | Codex says `npm config set force false` is blocked; P says `=false` flag values are not treated as bypass | `AC` | conflicts kept, not resolved |
| 7 | Identical-looking, differently scoped: P RULE-M-0057 (path-scoped backend rule, adds "no HttpResponseMessage in Application") vs P RULE-M-0493 (on-demand httpclient-factory skill); P RULE-M-0238 vs P RULE-M-0547 (same command, different trigger) | `RD DIFFERENT_SCOPE` x2 | identical-looking text with different applicability is not a duplicate |

Pilot outcome: 10 semantic-duplicate groups, 9 relations (1 apparent conflict), 3 mechanical
attribution-disagreement items, 0 build errors, validator 0 errors.

Failure modes found and the resulting clarifications (adopted **before** full-scale merging;
they do not change any merge predicate):

* F1 (builder bug): singletons were labelled `REVIEWED_NO_DUPLICATE_FOUND` although their
  regions were not yet reviewed. Fixed: draft builds label them `PENDING_REGION_REVIEW`; a
  final build requires every multi-run region to be reviewed.
* F2: split parts of a Claude record inherit **all** evidence occurrences of the record,
  because the record does not say which segment supports which part. Clauses of parts therefore
  do not assert a part-to-location mapping (`anchor_basis = EVIDENCE_SEGMENT`, inherited).
* F3: replica records cite many locations and appear in many regions; a pair is decided once,
  repeated appearances are shown in short form. Decisions are global per candidate.
* F4: paraphrase completeness. Rule applied: if one claim adds a condition, limit, exception,
  approval path, scope restriction or a second obligation, the pair is `RD DETAIL_DIFFERENCE`
  or `RD COMPOUND_PART`, not `SD`; wording, synonyms and illustrative members of the same set
  do not block `SD`.
* F5: the identical-looking pairs in case 7 are not co-located, so region review would not
  propose them; they confirm that lexical similarity alone is not a merge criterion and
  illustrate the accepted limitation in section 9.

## 13. Change log

* v1.0 (2026-10-28): initial frozen protocol; pilot clarifications F1-F5 recorded in section 12
  before full-scale merging.
* v1.1 (2026-10-28, adopted after the pilot and before any non-pilot decision of M): two
  clarifications of the `SD` predicate. Neither relaxes the requirement that all dimensions be
  equivalent; they fix how equivalence is judged when runs use different vocabularies.
  * **F6 (provenance of an extra exception/condition).** If only one of two claims states an
    exception, condition or scope restriction, `SD` is blocked when that text comes from a
    source location the other claim does not cite (genuinely additional content: use
    `RD DETAIL_DIFFERENCE` or `COMPOUND_PART`). If the exception lies inside source text cited by
    both claims and the other claim neither states nor contradicts it, it does not block `SD`;
    the `E:` check must then say so explicitly. For Codex findings (which report no modality,
    scope or exceptions) the finding's own quote counts as its cited text. F6 permits but never
    forces a merge.
  * **F7 (cross-run modality vocabulary).** Reported strengths are compared by meaning:
    `MUST` + negated action = `MUST_NOT`; primary `ENFORCED` (blocking hook/check) = replica
    `MUST/MUST NOT (... deny/block ...)`; primary `ENFORCED_ADVISORY` = replica
    `SHOULD (PostToolUse/Stop reminder ...)` when both describe the same hook message.
    `PREFER`/`AVOID` (guidance), `DEFAULT` (deviation needs reason and report), `MUST`,
    `REQUIRES_APPROVAL` and `DEFINITION` are pairwise **different** strengths: the same sentence
    reported as `PREFER` by one run and `DEFAULT` by another is `RD DIFFERENT_STRENGTH`, never `SD`.
  * Re-validation scope: every pilot decision was re-checked against F6/F7. Every pilot `SD`
    already satisfied them (exceptions absent or stated by both); the conservative pilot `RD`
    decisions stay valid because F6 never forces a merge. No decision changed.
* v1.2 (2026-10-28, adopted before M decision batch 4, i.e. from region M r151 onward, and
  applied unchanged to all later candidates):
  * **F8 (same obligation stated in several documents).** The document and loading mechanism
    of an occurrence (path-scoped rule, always-loaded CLAUDE.md, on-demand skill, private
    reference, hook, script) is a property of the *occurrence*, not of the claim's
    applicability. Claims anchored in different documents may be `SD` when actor, action,
    target, applicability (the situations the obligation governs), strength, exceptions and
    timing match. Every occurrence stays its own clause with its own location, so loading
    differences remain visible to later stages. A narrower restatement (an example, a subset,
    an added permission, a different trigger) remains `RD`. A checker or hook that *enforces* a
    rule is a different layer (`RD DIFFERENT_LAYER`), not a restatement.
  * Re-validation scope: decisions in the pilot and M batches 1-3 were re-checked. No earlier
    `SD` depends on F8 except merges of replica records whose own evidence already spans
    several documents with the same applicability. The pilot's `DIFFERENT_SCOPE` pairs differ
    in content or trigger and remain `RD`. No decision changed.
* v1.2.1 (2026-10-28, documentation correction after the M checkpoint; no merge predicate
  changed, no decision changed): section 4 said co-located pairs without a directive are
  "topically different claims that merely share a span". That over-states the record. The
  accurate meaning, already written into every `CO_LOCATION_INDEX` row by the builder, is:
  *reviewed and not merged; a relation was recorded only where the reviewer judged it
  informative for Step 2*. Relation recording is not exhaustive (M records many
  `EXAMPLE_GENERAL`/`OVERLAP` pairs; later candidates record them more selectively, always
  recording `DIFFERENT_STRENGTH`, `DETAIL_DIFFERENCE`, `COMPOUND_PART`,
  `BROADER_NARROWER`, `APPARENT_CONFLICT` and `UNRESOLVED` where observed). Step 2 should use
  `CO_LOCATION_INDEX.jsonl` to find every co-located pair.
* v1.2.2 (2026-10-28, editorial correction after all six checkpoints; no merge predicate,
  decision or ledger changed): the relation subtype in the v1.2.1 note was misspelled
  `DETAIL_DIFFERENT`-type; the defined subtype is `DETAIL_DIFFERENCE`. Checkpoints M..K1 record the
  protocol hash in force when each was written; this edit post-dates all of them.
