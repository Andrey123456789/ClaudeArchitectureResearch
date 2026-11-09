# SINGLE-CIS-M-U0034 (1 records)

## CIS-M-U0034 (pass 3) M .claude/skills/aspnet-error-handling/SKILL.md:40-46  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The client-cancellation decision guide may direct use of the illustrated 499 response status when OperationCanceledException coincides with RequestAborted cancellation.
TRIGGER: using this skill decision guide for client/request cancellation; table line237 says handle as shown above | EXC: Example code is not installed or executed; table-to-example incorporation is uncertain. Not a claim that every cancellation must send a response or that the disconnected client receives it. | POL: []
CODEX WHY: Source-grounded residual compared with specific prior records across all3 runs; omitted action or permission may have independent content, but example/guidance status and broader-policy subsumption remain unresolved.
```
  37          Exception exception,
  38          CancellationToken cancellationToken)
  39      {
  40>         if (exception is OperationCanceledException &&
  41>             httpContext.RequestAborted.IsCancellationRequested)
  42>         {
  43>             httpContext.Response.StatusCode =
  44>                 StatusCodes.Status499ClientClosedRequest;
  45> 
  46>             return true;
  47          }
  48  
  49          logger.LogError(
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/M/constraints.jsonl/RULE-M-0267 -> FG-M-0470806005 [CANONICAL_ONLY] Normal client-request cancellation is not mapped to a generic 500 or logged as an unhandled failure.
- NAMED replica/M/constraints.jsonl/RULE-M-0079 -> FG-M-0470806005 [CANONICAL_ONLY] Normal client-request cancellation is not mapped to a generic 500 or logged as an unhandled failure.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0049 -> FG-M-9c9b366c29 [EXTRA_PRODUCT] If a project adopts a Result pattern, it must use typed errors rather than arbitrary strings passed through every layer (reported as a requirement).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0050 -> FG-M-ee0a1287bf [CANONICAL_PLUS_DELTA] Typed exceptions for selected cases only as a consistent project-level decision, not a per-feature habit.
