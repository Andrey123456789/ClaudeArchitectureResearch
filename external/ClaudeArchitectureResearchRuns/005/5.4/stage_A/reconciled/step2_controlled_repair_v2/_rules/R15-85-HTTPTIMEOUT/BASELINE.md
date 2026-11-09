# R15 item 8.5 HTTP timeout: comparison

**Type.** NO_CHANGE_VERIFIED for Markdown, CLASSIFICATION_ONLY for labels. Register: «Не изменять Markdown».

**Six-way source.** All six separate client cancellation, own timeout and upstream timeout, and all six map upstream timeout as intermediary to 504. L1 keeps its details. `FG-M-50cf4c38e7` remains CO with a claim limited to client cancellation; its remainder sits at `FG-M-11afdc75eb`.

**Modality.** Knowledge skill. M 502/504 "Do not convert" and "Do not return" are marked (kept). Others are declaratives at DEFAULT. Differences in the token are form, read under `A2-PI012`.

**Label drift.** Same claim: CO in L0, K0, K1; XP in M1; CD proposed for L1 by the audit. CD is the supported reading: client cancellation is entailed, own-versus-upstream is not. Overlay corrects L0, K0, K1, M1.

**502/504 mapping.** Stays source-grounded as extras (`FG-M-11afdc75eb`, `FG-M1-62a4f62030`, `FG-L0-c0a8a0e349`, `FG-L1-7ff7ea7553`, and the K0 and K1 status-semantics groups).
