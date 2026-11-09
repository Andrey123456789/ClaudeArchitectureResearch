# Six reviewer readings

From v1 `FINAL_CONSISTENCY_REPORT.md` section 6. Each is adjudicated on current v2 source. These are readings by the same model family that wrote the text, so a human or fresh-session reviewer can still overturn them.

## 1. `R02-TASK-SCOPE`: CONFIRMED

**Question.** Does the pre-existing dirty-tree check apply to read-only reviews?

**Reading.** No. All six say: "before a task that will change files or repository state in a Git working tree". The condition is in the sentence, so a read-only review falls outside it with no hidden expansion. `code-reviewer` agents have Write and Edit disallowed, and `git status` is not denied by K0's hook.

**Consequence.** A reader who applies the check to every task would stop a read-only review on a dirty tree. The text does not ask for that.

**Limit.** A build creates ignored output, which `git status --porcelain` does not show, so verification alone does not trip the check. Whether a live agent reads it this way is NOT_RUN.

**Evidence.** C06 suite `R02-TASK-SCOPE` rows; R02 fixtures; C04 "a read-only task is outside the task-start check".

## 2. `R02-HEADLESS-DIRTY`: CONFIRMED, and carried into the Step 3 conditions

**Question.** Does an approved Reserved headless action bypass the dirty-tree pause?

**Reading.** No. The headless Reserved sentence grants authority for a Reserved change. It says nothing about Git and does not name the dirty tree. The Git clause pauses a headless run with no already adequate choice. The two do not conflict, because they answer different questions, and the pause comes first in order of work.

**Consequence.** Step 3 needs a clean initial tree or an explicit standing choice, or every run stops at its first step.

**Evidence.** R02 fixtures, `porcelain_gate`; R27 replay section E; C06 suite `R02-HEADLESS-DIRTY` rows.

## 3. `R04-RECORD-FORGERY`: CONFIRMED as a limit, no change

**Question.** Is an agent-writable marker proof of user consent?

**Reading.** No, and nothing in the text claims it is. The rule is the instruction: a floating or prerelease version is "allowed only on an explicit, bounded user request". The record gives traceability: it names package, version and manifest, and it shows in a diff. The checker cannot verify who asked, and `requested_by` and `request` are self-attested.

**What was tested.** A record written with no request is accepted by the checker, in all six. That is shown as a limit, not as a pass of a proof-of-origin test. No candidate's text says the checker proves or verifies who asked. The checkers in M, M1, K0 and K1 print "approved exception recorded", which reports the record, not an authentication. L0 and L1 do not print that phrase.

**Why no change.** The contract asks not to add security infrastructure. A signature scheme would be out of scope for this C# research, and any local secret the agent can read gives no real proof either.

**Evidence.** C06 suite `R04-RECORD-FORGERY` rows.

## 4. `R01-COMMON-VALUE`: approved reading kept, both shown

**Question.** Unmarked `only when` in knowledge text: `DEFAULT` or binding?

**Readings and consequences.** See `PI012_SENSITIVITY_V2.md` for counts on the current view.

| Reading | Consequence |
|---|---|
| Approved addendum: `DEFAULT` | An agent may deviate from a technique line with a concrete, reported reason. Force stays with rule owners. |
| Option D: binding | The same technique lines become violations if not followed, including those with no owner. |

**Decision.** Keep the approved reading. No source contradicts it. No coverage or strength cell moves under either reading, because coverage does not read modality. Strength comparison across candidates still needs reviewed text.

## 5. `R01-TRIGGERED-CLASS`: individually read, modality kept

**Question.** The 21 `do not X when Y` leads, not read in v1.

**Result.** All 21 are in `PI012_EXTRA_21_REVIEW.jsonl`, with quote, location, owner, condition, affirmative form, modality and decision. The scan was reproduced exactly from v1's script (22, 8, 21). No modality moved. One claim got its lost condition back (`FG-K1-d8c34708a7`). One lead is a scan artifact (`FG-M1-14b23b94ae`). Three are restraints on the auditor, not product prohibitions.

**Why not move them to `DEFAULT`.** Addendum A2 rule 3 keeps them at A1.3 force because the condition raises a ban and does not grant a permission. Most also apply a binding policy to a case (`DEP-001`, `SEC-016`, `API-016`). Moving them would apply option D's logic in reverse, with no decision behind it.

## 6. `R22-UNDER-EXTRACTION`: real, fixed in the derived field only

**Question.** Does the extractor lose a scope written in a parenthesis of the original trigger?

**Finding.** Yes. Of 5,050 v1 records with no extracted condition, 3,978 have a parenthesis in the original trigger. Many are real scope ("failing build or tests", "adding, updating or removing NuGet/npm packages"), and many are delivery ("read by project-structure", "imported by CLAUDE.md").

**Fix.** `_tools/triggers.py` now derives `applicability_scope_hint` from the parenthesis, leaving out delivery phrases, and judges each part around a semicolon alone. The original trigger field is untouched, `applicability_status` does not change, and the source is named on the record.

**What was read.** All 144 distinct parts, which changed the filter: the first version kept delivery phrases as scope and lost real scope in mixed parentheses. Then a seeded sample of 30 records: 25 right, 5 debatable, 0 wrong. The debatable ones carry the scope of the delivering workflow, which can be wider than the line. A hint is not a verified condition.

**Evidence.** C06B suite; `_rules/C06B-R22-APPLICABILITY/PARENTHESIS_CENSUS.json` and `SAMPLE_READING.md`; `DATASET_MANIFEST.json` counts.
