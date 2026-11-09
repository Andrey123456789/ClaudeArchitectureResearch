# SINGLE-CIS-M1-U0022 (1 records)

## CIS-M1-U0022 (pass 3) M1 docs/capability-selection.md:28-30  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Read slot contracts and implementation manifests only during capability maintenance.
TRIGGER: Deciding whether to read CONTRACT.md or MODULE.md outside capability maintenance | EXC: May describe intended loading rather than impose an absolute prohibition on incidental reading. Does not prohibit ordinary reading of imported planning decisions. | POL: []
CODEX WHY: Temporal loading restriction is a plausible atom distinct from default non-auto-loading; declarative metadata interpretation and replica evidence linkage keep novelty unresolved.
```
  25  
  26  - Planning-time decisions of each selected implementation:
  27    `docs/capabilities/<slot>.md` (imported by `CLAUDE.md`).
  28> - Slot contracts and implementation manifests (maintainer metadata, read only
  29>   during capability maintenance): `.claude/capabilities/<slot>/CONTRACT.md` and
  30>   `.claude/capabilities/<slot>/<implementation>/MODULE.md`.
  31  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-0cc2d0667b [26, 30] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Test-project placement and the frontend workspace location belong to the frame; the persistence leaf binds to frame roles and does not decide placement.
- V2 FG-M1-c42e6916ba [26, 30] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Implementation-independent policy (framework-independent testing and frontend rules) stays outside the modules.
- V2 FG-M1-60a3291da7 [26, 30] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Placement belongs to the architecture frame; technique belongs to leaf capabilities.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0001 -> FG-M1-c1e77ede33 [INTERNAL_ARCHITECTURE] Static composition: each required slot has exactly one selected implementation, the optional slot zero or one; only selected implementations have runtime facets.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0004 -> FG-M1-60a3291da7 [INTERNAL_ARCHITECTURE] Placement belongs to the architecture frame; technique belongs to leaf capabilities.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0010 -> FG-M1-03596d1d45 [INTERNAL_ARCHITECTURE] The capability slots are architecture (required frame), persistence and backend-testing (required leaves) and frontend (optional leaf), selected as clean-architecture, ef-core (pro
