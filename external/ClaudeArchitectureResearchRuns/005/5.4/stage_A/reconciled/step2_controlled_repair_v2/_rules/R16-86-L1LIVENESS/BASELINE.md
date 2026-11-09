# R16 item 8.6 L1 liveness: comparison

**Type.** NO_CHANGE_VERIFIED.

**Source.** L1 `rules/0-core/http-api.md:37`: "Liveness avoids external dependencies whose outage could cause restart loops; readiness may depend on capabilities required to serve traffic" meets API-019. L1 `health-check:22-25`: "an endpoint that runs no dependency checks" with `Predicate = _ => false`.

**PI-012 reading.** The skill line is a declarative in a knowledge skill plus a code sample. Authority: technique, with the rule as owner. Modality: `DEFAULT` (already stored). It is not `MUST_NOT`, and it is not deleted. It is narrower than API-019 in scope (no dependency checks at all, not only external ones that risk restart loops), so audit proposal `FG-L1-51237abb7d` to CD at `DEFAULT` is the right label; adjudicated in R25.

**Six-way note.** Not a difference in required behavior: the rule binds, and the example is technique.
