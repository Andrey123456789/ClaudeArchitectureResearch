# SINGLE-CIS-K1-U0012 (1 records)

## CIS-K1-U0012 (pass 2) K1 .claude/skills/aspnet-error-handling/SKILL.md:114-114  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When cleanup is the justification for catching an exception, the cleanup must not be expressible otherwise.
TRIGGER: Adding a local catch for cleanup, without another listed recovery, translation or contextual purpose. | EXC: Other listed justifications for catching still apply; this is not a prohibition on all local catches. | POL: ['API-007', 'RUN-018']
CODEX WHY: Source qualifies the cleanup purpose more narrowly than the closest general permission. The uncertain issue is semantic subsumption by 'necessary cleanup', not failure to quote the same line.
```
 111  
 112  ## Catching exceptions
 113  
 114> Catch when you can recover, translate into a meaningful abstraction-level outcome, perform cleanup that cannot be expressed otherwise, or add context while preserving the original exception. Never catch `Exception`
 115  
 116  ```csharp
 117  try { await service.ProcessAsync(cancellationToken); }
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-6d5d64d4fe [114, 114] MIXED/MIXED pol=[] rel=[]: Catch exceptions only to recover, translate into a meaningful abstraction-level outcome, perform necessary cleanup, add context while preserving the original, apply a defined fallback or infrastructure retry; otherwise let them pr
- V2 FG-K1-ed187accde [110, 114] CANONICAL_ONLY/DEFAULT pol=['API-007'] rel=[]: Local catch purposes are enumerated; otherwise exceptions propagate.
- V2 FG-K1-770fc67286 [114, 114] CANONICAL_PLUS_DELTA/MUST_NOT pol=['API-007', 'API-012'] rel=[]: Catch only to recover, translate, clean up or add context while preserving the original; never catch Exception merely to continue; avoid catch/log/rethrow at every layer.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0270 -> FG-K1-770fc67286 [CANONICAL_PLUS_DELTA] Catch only to recover, translate, clean up or add context while preserving the original; never catch Exception merely to continue; avoid catch/log/rethrow at every layer.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0180 -> FG-K1-6d5d64d4fe [MIXED] Catch exceptions only to recover, translate into a meaningful abstraction-level outcome, perform necessary cleanup, add context while preserving the original, apply a defined fallb
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0108 -> FG-K1-f4bcad1e5b [EXTRA_PRODUCT] If a Result pattern is adopted use typed errors rather than string arrays.
