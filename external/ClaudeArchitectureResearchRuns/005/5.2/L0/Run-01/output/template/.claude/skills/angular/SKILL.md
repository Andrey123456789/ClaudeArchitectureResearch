---
name: angular
description: >
  Use for Angular code: standalone components, features, routing, signals, RxJS, data-access services, interceptors, forms, errors, tests.
---

> Level: 2 Technology | Owns: Angular implementation technique | Scope: frontend | Loads: knowledge skill (on demand) | Depends on: 1-architecture/frontend-structure.md, 2-technology/angular.md

# Angular Technique

Policy owners (routing): structural boundary → `1-architecture/frontend-structure.md`;
Angular conventions and bindings → `2-technology/angular.md`; server
authorization → `0-core/security-principles.md`; extra libraries →
`3-project/decisions.md`.

## Suggested Structure

```text
src/app/
  core/          auth/  http/  layout/
  shared/        components/  directives/  pipes/
  features/
    books/       pages/  components/  data-access/  models/  books.routes.ts
    account/     pages/  data-access/  account.routes.ts
  app.config.ts
  app.routes.ts
```

Create directories only when they contain code. Do not move feature code into
`shared` because two components of the same feature use it; `shared` is for
genuinely cross-feature primitives (confirmation dialog, loading indicator,
table primitive, formatting pipe).

## Standalone Components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Route-level pages coordinate UI behavior; reusable presentation components take
explicit inputs and emit meaningful events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);
readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state; avoid `effect()` when `computed`, a template
binding, or an event handler expresses the dependency more clearly.

## RxJS

RxJS fits `HttpClient`, debounced search, switching/cancellation, combining
asynchronous sources, and event streams. Typical composition operators are
`switchMap` (latest request wins), `concatMap` (ordered), `combineLatest`, and
`debounceTime`; `takeUntilDestroyed()` ties a manual subscription to the
injection context's lifetime.

## HTTP Data Access

```ts
@Injectable({ providedIn: 'root' })
export class BooksApi {
  private readonly http = inject(HttpClient);

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('/api/books');
  }
}
```

```ts
provideHttpClient(withInterceptors([authInterceptor, errorInterceptor]));
```

A functional interceptor is a plain function `(req, next) => next(req)` that can
`inject()` services; register it with `withInterceptors`.

## Authentication in the Client

A frontend may attach access tokens, show authenticated state, hide actions,
and guard navigation — all UX. Server-side semantics: `authentication` skill.

## Errors

A reusable `ProblemDetails` parser fits an error interceptor or a shared mapper
that exposes `status`, a stable `code`, and field errors from
`ValidationProblemDetails`. Backend HTTP semantics: `http-api` skill.

## Forms

Reactive forms give explicit state, validation, and testability for non-trivial
forms; keep transport/request mapping explicit; mirror backend constraints only
where the UI needs an equivalent user-facing rule.

## Routing

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () => import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` suits individual standalone route components.

## State

Lightweight options, in increasing weight: component fields, signals and
`computed`, a feature service exposing signals (a small store), RxJS
composition. A state-management library is an approval-gated addition
(→ `3-project/decisions.md`).

## Angular Material

When the project has chosen Material, use its components consistently for
common primitives; do not wrap every Material component in a custom abstraction
without a reason.

## Generated API Clients

Treat generated code as generated: keep it separate from handwritten feature
code and regenerate it when the contract changes (repair rules: `build-fix`).

## Testing

Test meaningful component behavior, validation, data-access request mapping,
important route/auth behavior, and complex reactive state with the workspace's
configured runner (Vitest for new workspaces); do not test framework internals.
E2E tests (Playwright, when required) cover a few important user workflows.
Avoid duplicating the same behavior at every test level.

## Performance

Lazy routes and sensible data access first; memoization, virtual scrolling, or
custom change-detection work only after a real need appears.
