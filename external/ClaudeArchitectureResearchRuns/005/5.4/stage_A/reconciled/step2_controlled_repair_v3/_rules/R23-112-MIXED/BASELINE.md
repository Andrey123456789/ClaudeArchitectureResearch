# R23 item 11.2: mixed evidence and cross-method adjudication

**Type.** CLASSIFICATION_ONLY. No template edit.

**Input.** The audit's five strength cells, three qualified overrides, partial-witness cells, and the source-policy conflict field. Output: `CROSS_METHOD_ADJUDICATION.jsonl`, written by `_tools/crossmethod.py`.

**Method.** Each qualified cell records its semantic reading, a falsifying counterexample, the executable test if one applies, and the competing readings. No cell is decided by counting models or witnesses. Each row's witnesses are re-checked on current bytes.

**Result.**
- 5 strength cells and 3 qualified overrides: `QUALIFIER_RETAINED`. All are instruction text that no hook decides, so `executable_test` says so. None becomes a parity statement.
- 50 partial-witness cells: `FLAG_RETAINED`. A partial witness count is not evidence of completeness, and these cells were not adjudicated one by one.
- The stored `canonical_conflict_ids` field is empty on every baseline record. Source-policy tensions were carried as `UNCERTAIN` or as future human decisions, and R02 to R06 resolve them or `UNRESOLVED_DECISIONS.jsonl` lists them.

**Limit.** `DIRECT_EVIDENCE` is traceability. Coverage rows do not show that two candidates are equally strict.
