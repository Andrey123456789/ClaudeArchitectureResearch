---
name: angular
description: Use when creating, modifying or reviewing Angular code — standalone components, feature folders, routing and lazy loading, signals and RxJS, HttpClient data-access services, functional interceptors, forms, guards, ProblemDetails handling, Angular Material, generated API clients, frontend tests.
---
<!-- Kind: KNW | Scope: frontend | Owns: Angular implementation technique and examples | Loads: on demand (model-invoked) -->
# Angular

Standards: `rules/frontend/angular.md` (structure, components, state, HTTP boundary, error contract, forms, RxJS lifetime) and `rules/frontend/security.md`; server authority: `rules/common/security.md`. Stack: DEC-WEB-01, DEC-WEB-02, DEC-WEB-03.

## Suggested Structure

```text
src/app/
  core/
    auth/
    http/
    layout/

  shared/
    components/
    directives/
    pipes/

  features/
    books/
      pages/
      components/
      data-access/
      models/
      books.routes.ts

    account/
      pages/
      data-access/
      account.routes.ts

  app.config.ts
  app.routes.ts
```

Which directories to create: `rules/frontend/angular.md` § Structure.

## Standalone Components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

## Feature Organization

A feature owns the UI and frontend-specific data-access logic it needs. A global layout of technical buckets (`components/`, `services/`, `models/`) spreads one feature across unrelated directories. Code used by two components of the same feature stays in that feature rather than moving to `shared`.

## Pages and Components

Route-level/page components coordinate UI behavior. Reusable presentation components receive data through explicit inputs and emit meaningful UI events.

## Signals

For state that is naturally synchronous and local to the UI:

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state, and avoid `effect()` when `computed`, a template binding or explicit event handling expresses the dependency more clearly.

## RxJS

RxJS earns its place for `HttpClient`, debounced search, cancellation/switching, combining asynchronous sources and event streams. Compose with operators (`switchMap`, `combineLatest`, `takeUntilDestroyed`) instead of nesting subscriptions.

## HTTP

API communication lives in feature data-access services:

```ts
@Injectable({ providedIn: 'root' })
export class BooksApi {
  private readonly http = inject(HttpClient);

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('/api/books');
  }
}
```

Presentation components see typed results, not raw HTTP details.

## HttpClient Configuration

Provider-based configuration with functional interceptors:

```ts
provideHttpClient(
  withInterceptors([
    authInterceptor,
    errorInterceptor,
  ]),
);
```

Class-based interceptors need a reason.

## Authentication

A frontend may attach an access token, display authenticated state, hide actions the user cannot normally perform, and protect navigation with route guards — all UI/UX concerns; the backend stays authoritative. Server-side semantics: `authentication` skill.

## HTTP Errors

When backend errors use `ProblemDetails`, centralize reusable parsing/mapping (for example in an error interceptor or shared error mapper) and branch on stable codes or contract fields. Backend status semantics: `http-api` skill.

## Forms

Reactive forms suit non-trivial forms where explicit state, validation and testability help. Keep transport/request mapping explicit.

## Routing

Route-level lazy loading for meaningful features:

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () =>
      import('./features/books/books.routes')
        .then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` also fits individual standalone route components.

## State Management

Escalation path: component state → signals → a feature service/store → RxJS composition. Introducing a state-management library: `rules/frontend/angular.md` § Components and State and DEC-WEB-02.

## Shared Components

`shared` fits reusable UI primitives or behavior that genuinely crosses features — a confirmation dialog, a generic loading indicator, a reusable table primitive, a formatting pipe — not a dumping ground.

## Angular Material

When the project has chosen Angular Material (DEC-WEB-01), use its components consistently for common UI primitives where they satisfy the requirement; wrapping every Material component in a custom abstraction needs a concrete reason.

## API Client Generation

When OpenAPI client generation is adopted: treat generated code as generated, keep it separate from handwritten feature logic, and regenerate it when the API contract changes (generated-output repair: `build-fix`; contract documentation: `swagger` skill).

## Testing

Useful targets: meaningful component behavior, validation, data-access request mapping, important route/auth behavior, complex reactive state. Framework internals need no tests. End-to-end tests (Playwright, DEC-WEB-03) focus on a small number of important user workflows unless the project requires broader E2E coverage; avoid duplicating the same behavior at every test level. Use the workspace's configured runner (Vitest for new workspaces).

## Performance

Start with route lazy loading and sensible rendering/data access; specialized memoization, virtual scrolling or custom change-detection work comes after identifying a real need.

## Anti-Patterns

Avoid new NgModules without a reason, HTTP calls scattered through components, global service folders of unrelated feature services, NgRx or state frameworks by default, manual subscriptions without lifecycle handling, complex business logic in interceptors, frontend authorization as the only authorization, parsing human-readable backend error strings, giant `shared` directories, converting every Observable to a Signal, and choosing Signals or RxJS merely because one is newer.
