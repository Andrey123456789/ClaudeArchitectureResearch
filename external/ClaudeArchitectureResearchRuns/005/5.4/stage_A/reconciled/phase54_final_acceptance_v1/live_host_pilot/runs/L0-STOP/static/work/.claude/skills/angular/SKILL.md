---
name: angular
description: >
  Use when writing or reviewing Angular code: standalone components, routes,
  Signals/RxJS, HttpClient data access, interceptors, reactive forms, guards, error
  handling, frontend tests.
---

> Level: 2 Technology · Owns: Angular implementation technique and examples (knowledge) · Scope: frontend · Loads: on invocation · Depends on: .claude/rules/1-architecture/frontend-structure.md, .claude/rules/2-technology/angular.md

# Angular

Policy owners: feature organization, component responsibility, HTTP boundary, state, error contract, validation role → `.claude/rules/1-architecture/frontend-structure.md`; standalone APIs, Signals/RxJS, subscriptions, interceptors, forms → `2-technology/angular.md`; server authorization → `0-core/security-principles.md`; stack and libraries not added by default → `3-project/decisions.md`. This skill is technique only.

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

Create directories only when they contain meaningful code. A feature owns its UI and frontend data-access; do not move feature code to `shared` just because two components of the same feature use it. `shared` suits reusable primitives that genuinely cross features (confirmation dialog, loading indicator, table primitive, formatting pipe).

## Standalone components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Route-level/page components coordinate UI behavior; reusable presentation components take explicit inputs and emit meaningful events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);
readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state; avoid `effect()` when `computed`, a template binding, or an explicit event handler expresses the dependency more clearly.

## RxJS

Typical fits: `HttpClient`, debounced search, cancellation/switching (`switchMap`), combining asynchronous sources, event streams. For manual subscriptions in framework-managed code, `takeUntilDestroyed()` (or `DestroyRef`) ties the lifetime to the component or service.

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

```ts
provideHttpClient(
  withInterceptors([authInterceptor, errorInterceptor]),
);
```

## Authentication in the frontend

The frontend may attach an access token, display authenticated state, hide actions the user cannot normally perform, and guard navigation — all user experience. Server-side semantics: `authentication` skill.

## HTTP errors

When the backend returns ProblemDetails, centralize parsing/mapping (for example in an error interceptor or a small mapping service) and branch on stable codes or fields, not on message text. Backend semantics: `http-api` skill.

## Forms

Reactive forms give explicit state, validation, and testability for non-trivial forms. Keep request mapping explicit. Duplicate a complex Domain rule in TypeScript only when the UI genuinely needs an equivalent user-facing rule.

## Routing

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () =>
      import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` also fits individual standalone route components.

## State

Start with component state, Signals, a feature service/store, and RxJS composition; introduce a state library only when application complexity demonstrates the need.

## Angular Material

When the project uses Angular Material, use its components consistently for common UI primitives; do not wrap every Material component in a custom abstraction without a concrete reason.

## Generated API clients

When OpenAPI client generation is adopted: treat generated code as generated, keep it separate from handwritten feature logic, regenerate it when the contract changes, and do not patch generated files unless the generation workflow requires it (`swagger` skill for contract concerns).

## Testing

Useful targets: meaningful component behavior, validation, data-access request mapping, important route/auth behavior, complex reactive state. Do not test framework internals or duplicate the same behavior at every level. E2E tests (Playwright, when adopted) focus on a small number of important user workflows unless broader coverage is required.

## Performance

Do not prematurely optimize. Use route lazy loading and sensible rendering/data access first; add memoization, virtual scrolling, or custom change-detection work after identifying a real need.

