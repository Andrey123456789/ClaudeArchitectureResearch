# PV2-04-M-FRONTEND-TESTS: declaration

Written before the first edit of this change. Authority: kit 74 Part B PV2-04 and decision D-PV2-04 (approved; no further approval needed).

**Change.** M gets the explicit ban the other five already have: "Never place frontend tests under `backend/`." It goes into M's own owner of frontend-test placement, `project-structure` step 7 ("Add Test Projects"); M's layout reference already points there ("Frontend test placement: `project-structure` step 7."). Wording as L0 and K1.

**Peers (scope, authority, modality).** M1 `solution-layout.md` "Do not place frontend tests under `backend/`."; L0 rule `layout.md` "Never place frontend tests under `backend/`."; L1 `solution-layout.md` "... never under `backend/`"; K0 `solution-layout.md` "Angular tests never go under `backend/`."; K1 `solution-layout.md` "Never place frontend tests under `backend/`." All five are stored `MUST_NOT`, linked to `DEP-024` (PARTIAL) with resolution PC or SL. M's owner is a project-structure procedure step: the same placement scope, the same marked form, read when tests are placed. The ban applies to frontend unit, component and E2E tests alike, as in the peers.

**Not added.** No other layout mandate: backend test projects, the workspace location, colocated tests and the E2E example are unchanged. CLAUDE.md is not edited (it already says the workspace holds its tests).

**Claims and policies.** `DEP-024`. One added claim in M, classified as M1 `FG-M1-9030e201b9` and K0 `FG-K0-40e6fc8d29`: CANONICAL_ONLY, MUST_NOT, DEP-024 PARTIAL, strength SAME with resolution PC (the ban restates a clause inside the separation policy; DEP-024's own tag is DEFAULT).

**Expected behavior.** The text model of the same placement task gives the same answer in all six: tests inside the workspace (colocated or under `e2e/`) acceptable; any frontend test under `backend/` forbidden. No checker in any candidate enforces this placement; that stays a text duty in all six (reported).

**Regression adaptation.** v2 `C07_PARITY_CLOSE.py` asserted "M has no such ban: a real text difference, left as it is". This approved change removes exactly that difference; the test now includes M in the six-candidate ban table and requires `MUST_NOT`. Negative test: this change's mutation that removes the M sentence.
