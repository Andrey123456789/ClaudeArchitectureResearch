# Label drift diagnostic (Section F)

This compares how the classification criteria were applied. It is not a strictness ranking, and raw label counts are not candidate differences.

## Short answer

- **`INTERNAL_ARCHITECTURE`:** the variation reads mainly as a source difference. No same-file comparison pair differed on it, and the count broadly follows how many files hold such claims. K0 is the exception (70 records on 9 files), which this diagnostic did not explain. The evidence covers same-file pairs only.
- **`MIXED`:** the rise from M 6 to K1 40 has no single cause, and part of it is reader drift. Same-file comparisons rarely flip on `MIXED`, but where they do, equal semantics were read differently.
- **Most drift found is a lesson that did not propagate.** A reading settled for one candidate was not carried to the same text in another. Proposed corrections address the cases found. No sweep was run, so the number of remaining cases is unknown.

## Counts

| Candidate | Records | `MIXED` | Average source ranges per `MIXED` | `INTERNAL_ARCHITECTURE` | Distinct files holding `INTERNAL_ARCHITECTURE` anchors |
|---|---:|---:|---:|---:|---:|
| M | 1003 | 6 | 1.5 | 47 | 7 |
| M1 | 1113 | 13 | 2.0 | 72 | 15 |
| L0 | 972 | 23 | 1.5 | 49 | 9 |
| L1 | 1037 | 23 | 2.3 | 61 | 13 |
| K0 | 1077 | 30 | 1.8 | 70 | 9 |
| K1 | 1200 | 40 | 2.2 | 91 | 18 |

## Same-file comparison

The frozen rule pairs records on the same relative file with similar claims (token overlap at least 0.6). This is a lead, not an error count, because group boundaries differ.

| Pair | Similar pairs | Same label | Different label | One side `MIXED` | One side `INTERNAL_ARCHITECTURE` | Other |
|---|---:|---:|---:|---:|---:|---:|
| M ~ K1 | 168 | 152 | 16 | 4 | 0 | 12 |
| M1 ~ K0 | 187 | 181 | 6 | 2 | 0 | 4 |
| L0 ~ L1 | 285 | 282 | 3 | 1 | 0 | 2 |
| M ~ L0 | 178 | 166 | 12 | 2 | 0 | 10 |

Two points follow:

- In M ~ K1, at most 4 of K1's 40 `MIXED` records flip against a same-file M record. The rest are either unmatched or match nothing similar enough. K1 also holds more groups. The similarity threshold misses claims worded differently, so this undercounts flips and does not rule out wider drift.
- No pair flips on `INTERNAL_ARCHITECTURE`. This covers only same-path pairs, so it says nothing about capability files unique to one candidate.

## Frozen pair outcomes

17 pairs were compared and all were read at source. Outcomes are in `_decisions/F_PAIRS.json`.

| Outcome | Count | Meaning |
|---|---:|---|
| Source differs | 4 | Different labels are warranted |
| Group boundaries differ | 4 | Labels are not comparable |
| Equal semantics read differently | 9 | Criteria drift or a fair C2 alternative |

**Source differs:**

- `FG-M-d0b6a09cce` and `FG-K1-a9e7f2614e`: K1's line adds that production migration is an explicit deployment step.
- `FG-M1-440753ba6e` and `FG-K0-0bd6751e04`: same-change timing appears only in M1's group.
- `FG-L0-d42eeb59b8` and `FG-L1-708b6de8c5`: L0 says when tunable values are involved.
- `FG-M-b5f7b8480b` and `FG-L0-60fa521e22`: L0 adds in the same change.

**Equal semantics read differently:**

| Records | Reading | Action |
|---|---|---|
| `FG-M-22cae42396`, `FG-K1-8a61b0db25` (and `FG-K0-9146b82c8d`) | M is `MIXED` after its review; K1 and K0 stayed CO on the same sentence | Correction proposed |
| `FG-M-b00f9a8f1a`, `FG-K1-73cb1f8b21` | M is CO; five other candidates separate the version check as an extra | Correction proposed |
| `FG-M1-b82958affd`, `FG-K0-15ece1f846` | M1's unconditional line was CO; K0's conditional line was CD. This ran backwards | Correction proposed for M1 |
| `FG-L0-53de46c9e2`, `FG-L1-f7f4433e5e` | L0 is `MIXED`; L1 was CO and absorbed the remainder | Correction proposed |
| `FG-M-6477324ec2`, `FG-K1-5240a5b9d6` | Suite-scope clause: CD against XW | None; both hold the remainder |
| `FG-M-604133c8ba`, `FG-K1-9161d09cdd` | Approval recording: CD against XW | None |
| `FG-L0-b126a9719d`, `FG-L1-f05f0a9037` | Ask for a dataset: CD against XW | None |
| `FG-M-8732c932a4`, `FG-L0-6730a8eb68` | PR content: CD against `MIXED` | None |
| `FG-M-ade51003dd`, `FG-L0-e8e7ecedc4` | Deprecated sink: XP against CD | None |

The last five are fair under C2, which leaves room between CD, XW and `MIXED`. Do not count those labels as differences in Step 3. Compare the extra fragment.

## Identical text across candidates

Grouping records by the exact normalized text of the primary anchor (60 characters or more):

- 144 texts are shared by at least two candidates.
- 11 of those texts carry different labels. Most come from different group boundaries over the same line.
- 13 carry the same label but different modality.

Findings from reading them:

| Text | Reading | Action |
|---|---|---|
| "Constructing `HttpClient` directly in a focused test is fine" | NN in M, M1, L0; CO at MAY in K1 | Correction proposed for K1 |
| "Add a distributed backend such as Redis only when deployment requirements justify it." | `DEFAULT` in M; `MUST_NOT` in L1 | PI-012 proposal aligns them |
| "Only for a conditional request ..." | `MUST_NOT` in M; `DEFAULT` in M1 | PI-012 proposal aligns them |
| "Machine-readable clients rely on stable error codes ..." | `DEFAULT` in M1; `MUST_NOT` in K0 | PI-012 proposal aligns them |
| "Include only dependencies required for meaningful readiness" | `MUST` in M; `DEFAULT` in M1 | Correction proposed for M |
| 428 line | `MUST` in M; `DEFAULT` in M1 | Correction proposed for M |
| Finding format and "When evidence is incomplete" | `MUST` and `DEFAULT` across M, M1, L0, L1 | None; equivalence is what to compare |

The PI-012 proposal removes three of these splits, which is independent support for it.

## Other coding drift

- **Remainder kind on agent process.** Five candidates recorded the non-rewritable-branch remainder as `EXTRA_PRODUCT`, while M recorded it as `EXTRA_WORKFLOW`. L0 and L1 did the same on do-not-ask-for-approval. C4 makes these workflow. Field corrections are proposed.
- **Sibling groups on one line carry different modality.** `FG-M1-ae7b6c7526` and `FG-M1-b95ccac9b7`; `FG-L0-1fbbe47cb4` and `FG-L0-3ed43fa3b6`; `FG-K0-551da95e06` and `FG-K0-65ed9a2f90`; `FG-L0-0e49657a3e` and `FG-L0-081a8af01e`. The cause is that modality defaulted from reported labels group by group. Not corrected: equivalence on the links is the same, so read equivalence, not the token.
- **Peer-bypass strength.** M1 was STRONGER and L1 was INCOMPARABLE on the same structure of a hook plus a user-confirmation route. M1 is corrected. K1 has no such route, so STRONGER stays there; that contrast is real.
- **Do-not-wrap sentence.** M1 reads CO on `GOV-012` at `MUST_NOT`; L1 reads XP at `SHOULD_NOT`. The texts differ by one word. Left open: normalizing it needs a decision on how a marked negative stands against a `DEFAULT` policy, which is a related but separate question from PI-012.
- **Trigger field.** On 4,617 of 6,251 normative baseline records the `trigger` field reads as loading context (a heuristic), such as "on-demand knowledge skill swagger", and not the operative condition. C12 allowed this default. Do not compare triggers from this field. Read the claim or the source. Records with this pattern are flagged `trigger_field_reads_as_loading_context`.

## Targeted scans run

Each scan started from a pattern noticed during reading. All are bounded and non-exhaustive.

| Scan | Hits | Result |
|---|---:|---|
| `MUST` or `MUST_NOT` where every evidence range says default and no marker | 12 | Already in PI-012; or the policy text itself says by default under a binding tag (`DEP-015`); or the word default belongs to another clause of the line. No further correction |
| `MUST` or `MUST_NOT` where the claim says not required, need not or similar | 57 | Most are do-not-require duties or compound records. 4 corrections beyond `FG-M1-2a030a5f1e` |
| Knowledge-text `MUST` with no marker in the closest sentence | 230 | Leads only. 24 read; most have a marker nearby or are check-by-reference. 3 not settled by that reading: `FG-M-b4d7cde21c`, `FG-K1-c5a2ed7f59`, `FG-K1-5cf38cddbd` |

## What to do with this in Step 3

1. Compare content and extra fragments, not label or modality counts.
2. Use the effective view with its flags.
3. Before any claim that one candidate differs from another on a clause, read both source lines. This audit found several apparent contrasts that were only labels.
