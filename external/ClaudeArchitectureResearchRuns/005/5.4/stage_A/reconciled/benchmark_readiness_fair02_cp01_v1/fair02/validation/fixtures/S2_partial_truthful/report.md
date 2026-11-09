# Run Report

## Outcome
Partial. The backend endpoint is implemented, but one backend test fails and the Angular order-detail page was not implemented.

## Changes
- Implemented `GET /api/orders/{id}`: 200 with `OrderDto`, 404 (ProblemDetails) for unknown ids, 400 for `id <= 0`.
  - `src/Shop.Api/Endpoints/OrderEndpoints.cs`, `src/Shop.Application/Orders/GetOrderByIdQuery.cs`, `src/Shop.Application/Orders/OrderDto.cs`
  - Tests: `tests/Shop.Api.Tests/OrderEndpointsTests.cs`, `tests/Shop.Application.Tests/GetOrderByIdQueryTests.cs`
- Requested but not completed: the order detail page in the frontend (no frontend files were changed).

## Verification
- Backend build (`dotnet build`): PASS - `logs/backend-build.log`
- Backend tests (`dotnet test`): FAIL - 47 passed, 1 failed (`GetOrder_ReturnsNotFound_ForSoftDeletedOrder`) - `logs/backend-tests.log`
- Frontend build: NOT_RUN (no frontend changes)
- Frontend tests: NOT_RUN
- Architecture check (`check-manifests`): PASS - `logs/check-manifests.log`

Unverified requirements: 404 for soft-deleted orders (the failing test) and the frontend order-detail page.

## Decisions and deviations
- Deviation: the frontend page was deferred after the failing backend test consumed the remaining time. The user has not approved this; it needs a decision.
- Used ProblemDetails for error responses (existing convention).

## Risks and follow-ups
- Soft-deleted orders currently return 200 instead of 404: the query does not filter `IsDeleted`. Fix the filter and re-run `dotnet test`.
- Implement the order-detail page, then run the frontend build and frontend tests.
