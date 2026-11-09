---
name: angular
description: Use when creating or reviewing Angular code — standalone components, feature folders, routing, signals/RxJS, HttpClient data access, interceptors, forms, guards, error handling, Material, tests.
---

> Kind: KNW | Scope: frontend | Owner: Angular implementation technique with examples | Loading: on demand (model-invoked knowledge)

# Angular

Rules: `rules/frontend/angular.md`, `rules/common/security.md` § Authorization authority. Stack: D-09; libraries not added by default: D-10; E2E: D-13.

## Suggested structure

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

Create directories only when they contain meaningful code. A feature owns its UI and frontend-specific data access.

## Standalone components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Route-level/page components coordinate UI behavior; reusable presentation components receive data through explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state, and avoid `effect()` when `computed`, template binding or explicit event handling expresses the dependency more clearly.

## RxJS

RxJS earns its place for `HttpClient`, debounced search, cancellation/switching, combining asynchronous sources and event streams. Compose with operators (`switchMap`, `combineLatest`, ...) instead of nesting subscriptions, and tie manual subscriptions to the lifecycle with the current Angular facilities (for example `takeUntilDestroyed`).

## HTTP data access

```ts
@Injectable({ providedIn: 'root' })
export class BooksApi {
  private readonly http = inject(HttpClient);

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('/api/books');
  }
}
```

## HttpClient configuration

```ts
provideHttpClient(
  withInterceptors([
    authInterceptor,
    errorInterceptor,
  ]),
);
```

Interceptor rules: `rules/frontend/angular.md` § Components and data access.

## Authentication in the UI

A frontend may attach access tokens, display authenticated state, hide actions the user is not permitted to perform and guard navigation — all UX. Server-side semantics: `authentication`.

## HTTP errors

Error-contract rule: `rules/frontend/angular.md` § Errors and forms. A common shape: a shared error interceptor or utility maps `ProblemDetails` into typed errors (status, error code, validation errors) that features consume. Backend status semantics: `http-api`.

## Forms

Reactive forms give explicit state, validation and testability for non-trivial forms; keep transport/request mapping explicit. Duplicate a complex Domain rule in TypeScript only when the UI genuinely needs an equivalent user-facing rule.

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

## State management

Start with component state, signals, a feature service/store and RxJS composition; a dedicated state library needs demonstrated application complexity (D-10).

## Shared components

`shared` suits reusable UI primitives or behavior that genuinely crosses features — a confirmation dialog, a loading indicator, a reusable table primitive, a formatting pipe — not a dumping ground.

## Angular Material

Use Material components consistently for common UI primitives where they meet the requirement; wrap a Material component in a custom abstraction only for a concrete reason.

## Generated API clients

When OpenAPI client generation is adopted, keep generated code separate from handwritten feature logic and regenerate it when the API contract changes (generated-output handling: `build-fix` § Generated code; contract considerations: `swagger`).

## Testing

Useful targets: meaningful component behavior, validation, data-access request mapping, important route/auth behavior, complex reactive state — not Angular framework internals. Run the workspace's configured test runner. E2E tests cover a small number of important user workflows unless the project requires more, and the same behavior is not duplicated at every level.

## Performance

Start with route lazy loading and sensible rendering and data access; specialized memoization, virtual scrolling or custom change-detection work follows an identified need.

## Common mistakes

New NgModules without a reason; HTTP calls throughout components; global service folders of unrelated feature services; state frameworks by default; manual subscriptions without lifecycle handling; business logic in interceptors; frontend-only authorization; parsing human-readable backend error strings; giant `shared` directories; converting every Observable to a Signal; choosing Signals or RxJS because one is newer.
