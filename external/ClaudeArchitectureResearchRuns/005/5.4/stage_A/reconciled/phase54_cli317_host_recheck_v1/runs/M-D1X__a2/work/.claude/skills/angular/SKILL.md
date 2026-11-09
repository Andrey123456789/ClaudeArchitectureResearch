---
name: angular
description: >
  Use when writing or reviewing Angular code: standalone components, feature
  folders, routing and lazy loading, signals and RxJS, data-access services,
  interceptors, forms, API errors, tests.
---

> Owns: Angular implementation technique and examples (no policy) | Scope: frontend | Loads: on demand (knowledge skill)

# Angular

Policy owners: Angular structure, components, HTTP boundary, state, routing,
forms, interceptors, and RxJS lifetime — `.claude/rules/angular.md`; server-side
authorization — `.claude/rules/security.md`; the Angular stack and default
libraries — `docs/technology-stack.md`; generated clients —
`development-workflow` (generated output).

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

Empty or speculative folders: `.claude/rules/angular.md`. A feature owns the UI
and the frontend-specific data access it needs; do not move feature-specific code
into `shared` merely because two components inside the same feature use it.

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

Route-level/page components coordinate UI behavior. Reusable presentation
components receive data through explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state, and avoid unnecessary `effect()` when
`computed`, template binding, or explicit event handling expresses the
dependency more clearly.

## RxJS

RxJS provides real value for `HttpClient`, debounced search,
cancellation/switching, combining asynchronous sources, and event streams. For
subscriptions in components, `takeUntilDestroyed` and the `async` pipe are the
current lifecycle-aware facilities.

## HTTP

```ts
@Injectable({ providedIn: 'root' })
export class BooksApi {
  private readonly http = inject(HttpClient);

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('/api/books');
  }
}
```

Do not expose raw HTTP details throughout presentation components.

## HttpClient Configuration

Use provider-based configuration when configuration is required:

```ts
provideHttpClient(
  withInterceptors([
    authInterceptor,
    errorInterceptor,
  ]),
);
```

Class-based interceptors need a reason.

## Authentication in the UI

A frontend may attach an access token, display authenticated state, hide actions
the user cannot normally perform, and protect navigation with route guards —
all UI/UX concerns. Server-side semantics: `authentication` skill.

## HTTP Errors

When backend errors use `ProblemDetails`, parse and map them in one reusable
place (for example an error interceptor or a shared mapper). Backend HTTP
semantics: `http-api` skill.

## Forms

Keep transport/request mapping explicit. Do not duplicate complex Domain rules
in TypeScript unless the UI genuinely needs an equivalent user-facing rule.

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

For individual standalone route components, `loadComponent` is also appropriate.

## State Management

Start with component state, signals, a feature service/store, and RxJS
composition. Introduce a dedicated state-management library only when
application complexity demonstrates the need (a new library goes through
`add-dependency`).

## Shared Components

`shared` suits reusable UI primitives or behavior that genuinely crosses
features — a confirmation dialog, a generic loading indicator, a reusable table
primitive, a formatting pipe — not a dumping ground.

## Angular Material

When the project uses Angular Material, use its components consistently for
common UI primitives where they satisfy the requirement. Do not add Angular
Material automatically to an existing project that has not chosen it, and do not
wrap every Material component in a custom abstraction without a concrete reason.

## API Client Generation

When OpenAPI client generation is adopted, treat generated code as generated,
keep it separate from handwritten feature logic, and regenerate it when the API
contract changes. Backend contract documentation: `swagger` skill.

## Testing

Test frontend behavior at the appropriate level: meaningful component behavior,
validation, data-access request mapping, important route/auth behavior, complex
reactive state. Do not test Angular framework internals. E2E tests focus on a
small number of important user workflows unless the project requires broader
E2E coverage, and the same behavior is not duplicated at every test level. Use
the test runner configured in `package.json`.

## Performance

Do not prematurely optimize normal Angular code. Use route lazy loading and
sensible rendering and data access first; introduce memoization, virtual
scrolling, custom change-detection work, or other optimizations after
identifying a real need.

## Anti-Patterns

Avoid global service folders containing unrelated feature services, giant
`shared` directories, and choosing Signals or RxJS merely because one is newer
than the other.
