# Candidate M — Minimal Modular

## 1. Core idea

M tests the conservative hypothesis:

> A new instruction meta-architecture may not be necessary.
> Preserving V2's mental model and fixing its real defects may be enough.

M = **V2 + the frozen V2 policy oracle + the shared construction constraints + defect-driven refactoring**.

Do not reorganize the corpus merely for architectural elegance.

## 2. Binding rule: V2 lineage

Every runtime artifact must be explainable through V2 lineage.

Allowed change types:

- **Keep** — keep the V2 artifact, removing semantic restatements where needed;
- **Fix in place** — same owner, corrected defect;
- **Split** — one V2 artifact becomes several because it mixes owners, triggers, or responsibilities;
- **Merge** — competing artifacts become one;
- **Move** — content moves to a location with a more reliable trigger;
- **New** — only when a shared requirement genuinely requires a new owner, enforcement artifact, or human map.

Do not rename or move a file without a functional reason.

## 3. What M intentionally does not introduce

Do not introduce:

- stability levels;
- `Level:` classification;
- Kinds × Scopes as a meta-architecture;
- `Kind:` classification;
- capability slots/contracts/manifests/selection records;
- a formal replacement mechanism;
- rule directories organized by level/kind/capability;
- technology-neutral rewriting purely for future replaceability.

Scope must still be explicit through headers and `paths`,
but scope is not a primary architectural axis.

## 4. Ownership

Default heuristic:

> Keep policy with its V2 owner unless a concrete defect requires a move, split, or merge.

If V2 contains several copies of the same rule:

1. choose the owner with the most reliable trigger;
2. the owner must match the moment when the rule is actually needed;
3. replace other copies with pointers or check-by-reference entries.

`.claude/MAP.md` must give a human a simple answer to:

- what each file owns;
- its scope;
- how it loads;
- how it is enforced.

## 5. Decisions

Keep the V2-lineage two-part planning-time decision model:

- architecture defaults, approval gate, and patterns not adopted → always-loaded `CLAUDE.md`;
- approved technology stack and conditional technologies → imported `docs/technology-stack.md`.

Both must be available during planning.

Do not create:

- a K-style single decision register;
- an L-style decision hierarchy by stability level.

ADR history may live under `docs/decisions/`.

## 6. Rules

Expect a **flat** `.claude/rules/` directory.

A reasonable result after defect-driven splitting may resemble:

```text
.claude/rules/
├── architecture.md
├── persistence.md
├── coding-style.md
├── performance.md
├── error-handling.md
├── security.md
├── testing.md
├── dependencies.md
└── angular.md
```

This is illustrative, not a requirement to produce exactly nine files.

Binding properties:

- flat rule directory;
- recognizable V2 topical organization;
- `persistence.md` is allowed as a split from architecture/EF responsibilities;
- `angular.md` provides reliable path-loaded frontend policy;
- every runtime rule has explicit `paths`;
- procedures/technique are separated into skills/references.

## 7. Loading

Use the shared minimal mechanism model:

- always-loaded: `CLAUDE.md` plus imported `docs/technology-stack.md`;
- path-loaded: flat rules;
- hook: process/co-change enforcement;
- explicit workflow read: greenfield/review/verify cases where path loading may not have happened;
- on-demand: knowledge skills.

M may keep broader V2-like path globs when narrowing is not required by a real defect.

Do not turn M into K merely to optimize scope precision.

## 8. Skills and references

Preserve the familiar V2 skill model while fixing responsibility conflicts:

- workflow skill = procedure;
- knowledge skill = technique;
- a private reference is consumed only by its owning skill;
- shared policy must not live only in a private reference;
- `code-reviewer` is a thin wrapper;
- `serilog` does not compete with `logging`;
- `resilience` does not compete with `httpclient-factory`;
- a rule and a skill must not be independent owners of the same policy.

M does not need a formal workflow/knowledge taxonomy as a primary architecture.
The separation may be expressed through responsibility and naming.

## 9. Enforcement

Use deterministic enforcement where it materially improves reliability of mechanically checkable rules.

M must not avoid hooks/settings/checkers merely because V2 did not contain them when the candidate design or shared construction constraints require reliable enforcement.

However, every new artifact must have a clear purpose:
reliability, deterministic enforcement, or human navigation.

## 10. Illustrative top-level shape

```text
template/
├── CLAUDE.md
├── SPECIFICATION.md
├── CUSTOM_SETTINGS.md
├── .editorconfig
├── Directory.Build.props
├── Directory.Packages.props
├── docs/
│   ├── technology-stack.md
│   └── decisions/
└── .claude/
    ├── MAP.md
    ├── settings.json
    ├── hooks/
    ├── scripts/
    ├── rules/                 # flat topical rules
    ├── skills/
    └── agents/
```

Do not create a file merely because it appears in this illustrative tree.

## 11. Leakage checks

The result is no longer M if it introduces:

- `rules/0-core`, `rules/1-architecture`, or `Level:` → leakage toward L;
- a `Kind:` taxonomy or K-style scope-first organization plus a single decision register → leakage toward K;
- capability contracts/manifests/slot selection → leakage toward B1;
- broad reorganization that cannot be justified by a V2 defect or shared requirement;
- technology-neutral rewriting introduced only for replaceability.

## 12. Success criterion

M should look like a **recognizable, well-refactored V2**,
not like a new theory of instruction architecture.

If M physically converges with parts of K0 after fixing the same defects,
that is an acceptable research result.
Do not force artificial differences.
