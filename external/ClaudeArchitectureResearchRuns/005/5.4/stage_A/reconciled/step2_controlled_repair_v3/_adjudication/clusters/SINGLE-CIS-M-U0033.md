# SINGLE-CIS-M-U0033 (1 records)

## CIS-M-U0033 (pass 3) M .claude/skills/angular/SKILL.md:67-68  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Reusable presentation components emit meaningful UI events.
TRIGGER: designing reusable presentation components with relevant UI interactions while using the Angular skill | EXC: Descriptive technique in a no-policy knowledge skill; no requirement to invent events for inert components. Distinct from explicit data inputs in existing U0005. | POL: []
CODEX WHY: Source-grounded residual compared with specific prior records across all3 runs; omitted action or permission may have independent content, but example/guidance status and broader-policy subsumption remain unresolved.
```
  64  
  65  ## Pages and Components
  66  
  67> Route-level/page components coordinate UI behavior. Reusable presentation
  68> components receive data through explicit inputs and emit meaningful UI events.
  69  
  70  ## Signals
  71  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED replica/M/constraints.jsonl/RULE-M-0017 -> FG-M-e68db02c37 [CANONICAL_ONLY] Keep backend communication in explicit feature data-access services/HTTP boundary; no HttpClient calls scattered in presentation components; no backend Domain entities in Angular; 
- NAMED replica/M/constraints.jsonl/RULE-M-0015 -> FG-M-759af2acdb [CANONICAL_ONLY] Signals for synchronous local UI state, RxJS for async streams/HTTP composition/cancellation/event pipelines; avoid mechanical conversions.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0044 -> FG-M-6b0516f62c [EXTRA_PRODUCT] Use computed for derived state and avoid unnecessary effect() when computed, template binding or explicit event handling is clearer.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0046 -> FG-M-ffec7c1599 [CANONICAL_ONLY] Test frontend behaviour at the appropriate level (component behaviour, validation, data-access mapping, route/auth behaviour, complex state); do not test Angular internals; E2E cov
- PASS1 CIS-M-U0005 NOT_AN_INDEPENDENT_CONSTRAINT [67, 68]: Reusable presentation components use explicit inputs for their data.
