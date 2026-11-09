# R22 item 11.1: applicability versus delivery

**Type.** CLASSIFICATION_ONLY. No template edit. Derived fields only; `trigger_field_original` keeps the stored value.

**Fields added by `_tools/triggers.py`.** `applicability_trigger`, `applicability_status`, `applicability_hint`, `delivery_context`, `delivery_status`.

| Status | Meaning |
|---|---|
| `STATED_REVIEWED` | A reviewer wrote the condition, and it does not read as loading context |
| `STATED_ATTRIBUTED` | Attributed text that does not read as loading context, not re-derived |
| `CONDITION_IN_CLAIM_TEXT` | The field reads as loading context and the claim opens with a condition word. The condition is not separated; the hint is unverified |
| `UNKNOWN_NOT_EXTRACTED` | The field reads as loading context and the claim has no opening condition |
| `NOT_APPLICABLE` | Non-normative record |

**This is not a census.** Most records were not read. The status records how a value was obtained, never that it was verified. Counts are in `REPAIRED_VIEW_MANIFEST.json`.

## Sample read

A deterministic sample of 30 records, drawn by hash per status, was read by hand: `sample.py`.

**First version, defects found by the read.**
- It cut the condition out of the claim by pattern. 5 of 8 sampled cuts had the wrong boundary, for example "After a framework upgrade distinguish compile from runtime changes". Cutting was removed, so there is now a status and an unverified hint.
- `path rule: ...` passed as a condition, for 479 records. It is delivery.
- `all NuGet package references (MSBuild import)` passed as a condition. It is delivery.

**Final version, same draw.** 26 right, 4 debatable, 0 wrong.
- Two debatable rows are `UNKNOWN_NOT_EXTRACTED` with a usable scope in a parenthesis of the original field, such as "(security scans)" and "(new applications)". The derivation under-extracts these. The original field keeps the text.
- Two debatable rows are `STATED_ATTRIBUTED` where the field is a project role or a hook event, not a condition.

**Limits of this sample.** The pattern was corrected on this same draw, so 0 wrong is not an error rate. 30 records say nothing reliable about the rare cases in about 6,400. Hints often overrun the real condition and must not be quoted as conditions.

**Scope and modality.** The derived fields change neither modality nor classification.
