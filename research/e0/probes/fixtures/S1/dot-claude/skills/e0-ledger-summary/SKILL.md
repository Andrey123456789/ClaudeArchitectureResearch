---
name: e0-ledger-summary
description: Reconcile and summarize Quillmoor ledger files (*.qledger). Use whenever the user asks to reconcile, check, total or summarize a .qledger ledger.
---

# Quillmoor ledger reconciliation

1. Read the ledger file. Each entry line is `date | DR or CR | amount | memo`; lines starting with `#` are comments.
2. Sum the DR amounts (debits) and the CR amounts (credits).
3. Reply in exactly this format and nothing else:

```
Reconciliation-ID: E0S1-SKILL-0D2D04
Debits: <sum with two decimals>
Credits: <sum with two decimals>
Balanced: <yes if equal, otherwise no>
```
