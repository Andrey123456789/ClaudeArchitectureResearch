# V3-D01-PASS23-OVERLAY: declaration

Written before any change of this rule. Authority: kit 74 Part A.6 and Part C ("integrate source-grounded classification improvements without automatically changing candidate template text"). Data only: no candidate byte changes.

**Inputs.** `PASS2_PASS3_ADJUDICATION.jsonl` and `UNIQUE_ISSUE_CLUSTERS.jsonl` (`_adjudication/decisions.py`): 29 Codex records judged CANDIDATE_UNREPRESENTED_DUTY and 18 judged FACET_OF_EXISTING, plus v3 census items for the same shared sentences (labelled V3_CENSUS, not counted as Codex discoveries).

**Change.**

- 18 added records (`V3A-<C>-1NN`): security-scan investigation prompts that a candidate's source states and no same-candidate record states: local accounts (K0, L0, L1), upload execution and public serving (M1, L0, L1, K0), SSRF inspection (M1, L0, L1, K0, K1), raw HTML in server-rendered UI (M, M1, L1, K0, K1), duplicate or missing security logging (K0). Classification mirrors the Step 2 label of the same prompt in peer candidates: EXTRA_WORKFLOW, DEFAULT, no canonical link (peers: FG-M-7c2154e45a, FG-M-da325d3b47, FG-K1-94b2ab5757, FG-M-38fffb80cf, FG-M-56386cff04, NCP-L0-0001, AUG1-NC-*). Related policies are named, never linked, so no coverage or strength cell moves.
- 14 facet updates: the record already cites the passage and states the rest; the dropped atom or qualifier is written into its claim. The original claim stays in `claim_text_original`; classification, modality and canonical links are unchanged; `codex_pass23_ids` names the source records.

**Not changed.** No template text. No canonical policy. No modality or classification of an existing record. The L0 raw-HTML absence (CL15) is a real text difference and stays.

**Expected.** Coverage and strength identical in all 1,176 cells; every added record resolves to a current line and has a CONFIRMED v3 review row; every facet quote resolves; the per-claim gate passes for each update in order.
