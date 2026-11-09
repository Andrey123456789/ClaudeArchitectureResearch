# R20 item 9.2 K0 deserialization: reading

**Type.** CLASSIFICATION_ONLY. Register: «Чтение как критерия security audit, а не отдельного автономного product-policy; сохранить регистр риска, не объявлять HARD MUST_NOT без owner».

**Source.** K0 `security-scan/references/scan-layers.md:75-77`, under a scan layer: "Investigate polymorphic or type-driven deserialization ... Untrusted payloads are not deserialized into arbitrary runtime types."

**Effect.** `FG-K0-0ef1e5ed3d` and `FG-K0-6d06b21a93`: `EXTRA_WORKFLOW` at `DEFAULT`, SEC-003 as related only. SEC-003 stays covered by K0's other records. Uncertainty stays recorded on each record.

**Six-way note, real source difference.** M and M1 write "Do not deserialize", L0 "never deserialize", K1 "must not deserialize": marked prohibitions in a scan layer, kept under A1.3. L1 lists a pattern with no verb. K0's is the only unmarked declarative. Step 3 should read these lines before counting a difference, because all six sit in a scan layer.
