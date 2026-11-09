# Run Report

## Outcome
Partial: backend endpoint done; one backend test fails; the order-detail page is not implemented.

## Changes
| Area | Files | State |
|---|---|---|
| `GET /api/orders/{id}` (200, 404 ProblemDetails, 400 for `id <= 0`) | `src/Shop.Api/Endpoints/OrderEndpoints.cs`, `src/Shop.Application/Orders/GetOrderByIdQuery.cs` | done |
| Tests | `tests/Shop.Api.Tests/OrderEndpointsTests.cs` | done, one failing |
| Frontend order-detail page | none | not implemented |

## Verification
| Check | Result | Evidence |
|---|---|---|
| Backend build | ✅ PASS | `logs/backend-build.log` |
| Backend tests | ❌ FAIL (47 passed, 1 failed) | `logs/backend-tests.log` |
| Frontend build | ⏭ NOT RUN | - |
| Frontend tests | ⏭ NOT RUN | - |
| Architecture check | ✅ PASS | `logs/check-manifests.log` |

Unverified: soft-deleted orders returning 404; the order-detail page.

## Decisions and deviations
Frontend page deferred (no user approval yet). ProblemDetails for errors.

## Risks and follow-ups
- Soft-deleted orders return 200: add the `IsDeleted` filter, re-run backend tests.
- Build the order-detail page; run frontend build and frontend tests.
