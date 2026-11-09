# R14 item 8.7 C# language version: comparison

**Type.** CLASSIFICATION_ONLY. No template change.

**Six-way source.** All six `modern-csharp` skills say to confirm the configured language version supports a feature before using it, and all six gate changing `LangVersion`: M "do not change", M1 "is a stack decision", L0 "Reserved", L1 "requires approval", K0 "is a decision", K1 "never silently change ... Reserved". The wording differs and the permitted behavior does not: a change needs a decision or approval.

**Canonical baseline.** No policy names the confirm-first step, so it is a DEFAULT extra in all six. The Step 2 labels split it inconsistently: `FG-M-b00f9a8f1a` CO, M1 and L0, L1 separate XP records, K0 and K1 MIXED. Audit proposal `FG-M-b00f9a8f1a` to MIXED (R25) removes the only false CO. Step 3 should compare fragments.
