---
name: angular
description: Use when creating, modifying or reviewing Angular code — standalone components, feature folders, routes and lazy loading, Signals and RxJS, HttpClient data-access services, functional interceptors, reactive forms, guards, ProblemDetails handling, Angular Material, generated API clients or frontend tests.
---
Kind: KNW | Scope: frontend | Capability: frontend/angular | Loading: on invocation

# Angular

Technique for the frontend implementation. Rules: `.claude/rules/frontend/frontend.md` (structure, data access, errors, forms, browser security) and `.claude/rules/frontend/frontend-framework.md` (standalone APIs, Signals and RxJS, interceptors, subscriptions). Procedures (scaffolding, build, test, build-fix, E2E): the frontend workflow facet `.claude/capabilities/frontend/angular/workflow-facet.md`.

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

Create directories only when they contain meaningful code. A feature owns its UI and frontend-specific data access. Do not move feature-specific code into `shared` merely because two components of the same feature use it.

## Standalone components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

## Pages and components

Route-level page components coordinate UI behavior. Reusable presentation components receive data through explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state. Prefer `computed`, template binding or explicit event handling over `effect()` when they express the dependency more clearly.

## RxJS

RxJS fits `HttpClient`, debounced search, cancellation and switching, combining asynchronous sources, and event streams. Compose instead of nesting subscriptions, and tie manual subscriptions to the lifecycle:

```ts
private readonly destroyRef = inject(DestroyRef);

ngOnInit(): void {
  this.searchTerms.pipe(
    debounceTime(300),
    switchMap(term => this.booksApi.search(term)),
    takeUntilDestroyed(this.destroyRef),
  ).subscribe(results => this.results.set(results));
}
```

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

Introduce a class-based interceptor only for a concrete reason.

## Authentication in the frontend

A frontend may attach an access token, display authenticated state, hide actions the user cannot normally perform and protect navigation with route guards. These are UX concerns; server-side behavior: `authentication` skill.

## HTTP errors

When the backend returns `ProblemDetails`, centralize reusable parsing and mapping (for example in an error interceptor or a small mapping function) and branch on stable fields such as `status` or a documented error code. HTTP semantics: `http-api` skill.

## Forms

Use reactive forms where explicit state, validation and testability help. Keep transport/request mapping explicit. Do not duplicate complex Domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule.

## Routing

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () => import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` is appropriate for individual standalone route components.

## State management

Start with component state, Signals, a feature service or store, and RxJS composition. A dedicated state-management library is a decision-register matter ("Not added by default").

## Shared components

`shared` suits reusable UI primitives that genuinely cross features: a confirmation dialog, a generic loading indicator, a reusable table primitive, a formatting pipe. It is not a dumping ground.

## Angular Material

Use Material components consistently for common UI primitives where they satisfy the requirement. Do not wrap every Material component in a custom abstraction without a concrete reason.

## API client generation

When OpenAPI client generation is adopted, treat generated code as generated, keep it separate from handwritten feature logic, and regenerate it when the API contract changes (`build-fix` → Generated output). Backend contract documentation: `swagger` skill.

## Deployment as static assets

When the frontend is deployed as a static application, build it in a Node build stage and serve the generated assets with the selected hosting strategy; Nginx is not mandatory, because the platform may host static files directly. Keep API base URLs and environment configuration compatible with that strategy. Container technique: `docker` skill.

## Testing

Useful targets: meaningful component behavior, validation, data-access request mapping, important route and auth behavior, complex reactive state. Do not test Angular framework internals. Keep E2E tests to a small number of important user workflows unless the project requires broader coverage, and do not duplicate the same behavior at every test level.

## Performance

Do not prematurely optimize normal Angular code. Use route lazy loading and sensible rendering and data access first; add memoization, virtual scrolling, custom change-detection work or similar optimizations after identifying a real need.

## Anti-patterns

Review checks; the named standard owns each rule:

- New NgModules without a reason, or every Observable converted to a Signal? (`frontend-framework.md`)
- HTTP calls scattered through components, or global service folders holding unrelated feature services? (`frontend.md`)
- NgRx or another state framework added by default? (decision register)
- Manual subscriptions without lifecycle handling, or business logic in interceptors? (`frontend-framework.md`)
- Frontend authorization treated as the only authorization? (`.claude/rules/common/security.md`)
- Business behavior inferred from human-readable backend error strings, or a giant `shared` directory? (`frontend.md`)
