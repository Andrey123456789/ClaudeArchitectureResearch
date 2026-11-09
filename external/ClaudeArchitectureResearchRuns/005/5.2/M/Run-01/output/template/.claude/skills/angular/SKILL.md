---
name: angular
description: >
  Use for Angular code: standalone components, feature folders, routes and
  lazy loading, signals and RxJS, HttpClient data access, interceptors, forms,
  guards, ProblemDetails, frontend tests.
---

> Knowledge skill. Owns: Angular implementation technique and examples · Scope: frontend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/angular.md, .claude/rules/security.md

# Angular

Rules: `angular.md` (structure, components, HTTP boundary, interceptors, error
contract, state, routing, forms) and `security.md` (server-authoritative
authorization, browser credentials). Baseline stack: `docs/technology-stack.md`.

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

Create directories only when they contain meaningful code. A feature owns the
UI and the frontend-specific data-access logic it needs.

## Standalone Components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

## Pages and Components

Route-level page components coordinate UI behavior. Reusable presentation
components receive data through explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state, and avoid `effect()` when `computed`, template
binding, or explicit event handling expresses the dependency more clearly.

## RxJS

RxJS earns its place with `HttpClient`, debounced search,
cancellation/switching (`switchMap`), combining asynchronous sources, and event
streams. Prefer composition operators over nested subscriptions; for manual
subscriptions in components, `takeUntilDestroyed()` ties the lifetime to the
component.

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

Keep raw HTTP details out of presentation components; frontend API models
mirror the published HTTP contract.

## HttpClient Configuration

```ts
provideHttpClient(
  withInterceptors([
    authInterceptor,
    errorInterceptor,
  ]),
);
```

Class-based interceptors need a reason in new code.

## Authentication UX

A frontend may attach an access token, display authenticated state, hide
actions the user cannot perform, and protect navigation with route guards —
all UX. Server-side semantics: `authentication` skill.

## HTTP Errors

When backend errors use `ProblemDetails`, a shared parser/mapper (for example in
an error interceptor or a small `core/http` helper) turns them into UI-friendly
errors; business decisions use stable codes or fields from the documented
contract.

## Forms

Reactive forms suit non-trivial forms that need explicit state, validation, and
testability. Keep transport/request mapping explicit, and duplicate a complex
Domain rule in TypeScript only when the UI genuinely needs an equivalent
user-facing rule.

## Routing

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

Start with component state, signals, a feature service/store, and RxJS
composition. A dedicated state-management library is added only when
application complexity demonstrates the need (`docs/technology-stack.md`).

## Shared Components

`shared` suits reusable UI primitives that genuinely cross features — a
confirmation dialog, a generic loading indicator, a reusable table primitive, a
formatting pipe — not a dumping ground.

## Angular Material

When the project uses Angular Material, use its components consistently for
common UI primitives where they satisfy the requirement; do not wrap every
Material component in a custom abstraction without a concrete reason.

## API Client Generation

When OpenAPI client generation is adopted, treat generated code as generated:
keep it separate from handwritten feature logic and regenerate it when the
contract changes (`build-fix`, Generated Code; `swagger` skill).

## Testing

Useful targets: meaningful component behavior, validation, data-access request
mapping, important route/auth behavior, complex reactive state. Do not test
Angular framework internals. Keep E2E tests to a small number of important user
workflows unless the project requires broader coverage, and avoid duplicating
the same behavior at every test level.

## Performance

Start with route lazy loading and sensible rendering and data access; add
memoization, virtual scrolling, custom change-detection work, or similar
optimizations after identifying a real need.

## Anti-Patterns

- global service folders containing unrelated feature services;
- complex business logic in interceptors;
- frontend authorization as the only authorization;
- parsing human-readable backend error strings;
- giant `shared` directories;
- using Signals or RxJS merely because one is newer than the other.
