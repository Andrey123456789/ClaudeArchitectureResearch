# SINGLE-CIS-L0-U0047 (1 records)

## CIS-L0-U0047 (pass 3) L0 .claude/hooks/manifest-checks.mjs:246-249  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a parsed PackageReference, ProjectReference or PackageVersion item is marked malformed, hook feedback instructs the agent to fix its XML so the declaration can be checked.
TRIGGER: reportMalformed called on relevant parsed item types by project or central-package validation | EXC: Only items the bounded reader recognizes and marks malformed; not complete XML validity enforcement, not a claim that runtime execution is blocked. Quoted attribute and spacing details explain well-fo | POL: ['DEP-006']
CODEX WHY: An imperative repair message exists inside implementation-labeled code. Its separate normative significance versus routine syntax validity remains unresolved; no EXTRA conclusion.
```
 243    return (item.attrs.Include ?? item.attrs.Update)?.trim();
 244  }
 245  
 246> function reportMalformed(items, location, problems) {
 247>   for (const item of items.filter(entry => entry.malformed)) {
 248>     problems.push(`${location}: <${item.type}> at line ${item.line} is not well-formed XML (each attribute once, its value in " or ' quotes, attributes separated by whitespace); fix it so the declaration can be che
 249>   }
 250  }
 251  
 252  // <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally> outside comments (element name and
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0225 -> FG-L0-5d2fbbf043 [CANONICAL_ONLY] After successful and failed shell calls and after edits, added/changed manifests of the active worktree are validated with the manifest checks (first observation validates all; out
- NAMED replica/L0/constraints.jsonl/RULE-L0-0019 -> FG-L0-79ba8dd753 [CANONICAL_ONLY] The effective ManagePackageVersionsCentrally that MSBuild evaluates must be true for each project in each evaluated context; a false or unset value, a central manifest that is not 
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0048 -> FG-L0-ddc393f714 [NON_NORMATIVE] The manifest check infers project roles from names and reads MSBuild XML without evaluation (reported accuracy limits for conditional and property-expanded references).
