# C06B-R22-APPLICABILITY: declaration (contract section 2, step A)

Written before the extractor change. Data only: no candidate byte changes.

**Question.** `R22-UNDER-EXTRACTION`: does the derived applicability view lose a scope written in a parenthesis of the original `trigger`?

**Finding on v1 data.** 5,050 records have no extracted condition (`UNKNOWN_NOT_EXTRACTED` or `CONDITION_IN_CLAIM_TEXT`). 3,978 of them have a parenthesis in the trigger, with 139 distinct texts. Some state real scope ("failing build or tests", "adding, updating or removing NuGet/npm packages"). Some state delivery ("read by project-structure", "imported by CLAUDE.md", "CLAUDE.md is always loaded").

**Change.** `derive` adds `applicability_scope_hint` and `applicability_scope_source`, from the non-delivery parentheses only. The original `trigger` field stays. `applicability_status` and `applicability_trigger` stay, so no count of verified conditions rises. Register 11.1 keeps applicability and delivery apart: a path scope such as "backend" is reported as scope, under a name that says it came from the original field.

**Evidence.** A seeded sample of 30, 5 per candidate, not overlapping the R22 sample, read one by one in `SAMPLE_READING.md`. A sample, not a census.

**Negative cases.** A delivery phrase must not become a hint. A record with a reviewed condition must not get a hint in its place. A record with no parenthesis stays an explicit unknown. The status counts must not move.
