# Running the Stage A / Step 2 Residual-Parity Correction

1. Confirm the completed predecessor exists at:
   `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4\stage_A\reconciled\step2_controlled_repair_v1\`.
2. Extract **all five English-language kit files** (`70`, `71`, `62`, `72`, `73`) into:
   `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4\_STAGE_A_KIT\`.
3. Open a NEW Claude Code session (preferably Opus Extra) with working directory:
   `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.
4. Send the contents of `70_CLAUDE_STEP2_PARITY_CLOSURE_START_EN.txt` as an ordinary user message (not `/goal`).
5. Claude must write only to the NEW output directory:
   `stage_A\reconciled\step2_controlled_repair_v2\`.
   Original candidate trees, prior Step 2 outputs, and v1 must remain unchanged. Parallel Codex work must not be inspected or modified.
6. On completion, ZIP the ENTIRE `step2_controlled_repair_v2` folder for independent review.

**Decision-source precedence:** Follow the latest explicitly approved CPM choice in `72_APPROVAL_AND_HANDOFF_EN.md`; use `62_APPROVED_DECISIONS_AND_GATES_EN.md` for the detailed test cases, without silently modifying earlier decisions.

## Scope

- CPM: all six candidates validate effective MSBuild state, respecting legitimate inheritance instead of rejecting it on a literal-XML-only basis.
- Compiled queries: align all six candidates with `RUN-008`.
- Production migrations: align default restrictions and explicitly approved exceptions.
- Git: eliminate unconditional commit steps that conflict with the authorization contract, without building an elaborate Git policy subsystem.
- PI-012: individually adjudicate 21 residual candidates and two unique unresolved K0 cases, alongside the remaining reviewer readings.
- Review 62 `review_needed` flags, 38 qualified witnesses, and 42 new claims against current source text.
- After EVERY logical change, run the full gate for related policies, affected candidate architectures, cross-candidate parity, and all preceding regressions.
- After all changes, conduct an independent cold, full-system final audit and report. Do NOT start Step 3.

NOT_RUN categories (live agent, real database/cache, Swagger UI, package registry, CI) must remain explicitly reported if not executed. A passing parser test does not prove semantic correctness.
