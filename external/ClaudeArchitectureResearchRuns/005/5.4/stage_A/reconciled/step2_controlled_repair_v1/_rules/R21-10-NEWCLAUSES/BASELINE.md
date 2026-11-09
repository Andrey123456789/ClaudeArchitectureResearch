# R21 item 10: four new clause proposals

**Type.** CLASSIFICATION_ONLY. No template edit.

**Input.** `step2_semantic_audit_v1/NEW_CLAUSE_PROPOSALS.jsonl`, four rows: output-cache metadata in M and M1, Arrange/Act/Assert default in M1, security scan checks in L0.

**Method.** `_tools/newclauses.py` reads each proposal, verifies its quote in the frozen input and finds it again in the current working copy. Output: `NEW_CLAUSES_4_ADJUDICATION.jsonl`.

**Result.** All four are accepted as candidate-specific extra proposals. Each stays in its own candidate. None joins the canonical set, which stays at 196 policies, and none is copied to another candidate.

**Six-way note.** The proposals are not a parity claim. The other candidates may hold related text under other records; this rule does not compare them.
