# C06B: what was read

## All distinct phrases

`PARENTHESIS_CENSUS.json` holds every distinct part of a parenthesis in the original trigger, on records with no extracted condition. Each part was read, and the C06B suite fails if the view gains one that was not.

That reading changed the filter. The first version kept delivery phrases as scope (`registered in settings.json`, `actual-state.cjs via dispatch.cjs`, `end of turn`, `on delegation`, `manual/verify runs`) and lost real scope where one parenthesis mixed both (`read by project-structure; new applications`). The filter now judges each part around a semicolon alone. The failing tests are in `suite_pre_filter.jsonl`.

## Sample of 30 records

Design: for each candidate, the first 5 hinted records by `sha256('C06B|'+key)`, leaving out the R22 sample. Verdicts and reasons are in `sample.py`. This reads records, not phrases, and it is not an estimate of any population rate.

| Verdict | Count |
|---|---:|
| RIGHT | 25 |
| DEBATABLE | 5 |
| WRONG | 0 |

The five `DEBATABLE` rows share one cause. A hint carries the scope of the workflow or checker that delivers a line, and a line can be narrower: a deprecation check does not apply to removing a package, and a `before pushing` step sits under `any Git operation`. The hint is true of the delivering unit but not always of the line.

## What a hint is

A hint is the parenthesis of the original trigger field, with its source named. Nobody verified it per record. `applicability_status` and `applicability_trigger` do not change, so no count of verified conditions rises. Roughly 3,100 records carry a hint, and only these 30 were read one by one.
