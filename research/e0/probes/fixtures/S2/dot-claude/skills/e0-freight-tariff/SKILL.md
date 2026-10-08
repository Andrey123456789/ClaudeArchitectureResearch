---
name: e0-freight-tariff
description: Compute Brindlewick freight tariffs for shipments. Use when the user asks for a Brindlewick tariff, freight charge or shipping cost.
---

# Brindlewick freight tariff

1. Read the rate table in `references/rates.md`, located in this skill's own directory. The rates are private to this skill and are not repeated anywhere else.
2. Tariff = base fee + (weight in kg × the rate of the shipment's zone).
3. Reply in exactly this format:

```
Tariff: <amount with two decimals> BWC
Rate-table: <the verification code printed in the rate table>
Skill: E0S2-SKILL-AD8956
```
