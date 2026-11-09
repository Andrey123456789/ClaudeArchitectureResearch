---
name: angular
description: >
  Use when writing or reviewing Angular code: standalone components, feature
  folders, routes and lazy loading, signals and RxJS, HttpClient data-access
  services, interceptors, reactive forms, ProblemDetails handling, guards,
  Material, tests.
---

> Owner: Angular implementation technique and examples (normative policy lives in rules) | Scope: frontend | Loads: on demand — knowledge | Enforced: none

# Angular

Policy: `.claude/rules/angular.md` (structure, components, HTTP boundary,
reactive state, routing, forms) and `.claude/rules/security.md`
§ Authentication and Authorization (server-side authorization). Stack:
`docs/technology-stack.md` § Frontend.

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

Create a directory only when it contains meaningful code.

## Standalone Components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Use NgModules only when an integration or legacy dependency genuinely requires
them.

## Feature Organization

A feature owns the UI and the frontend-specific data access it needs. Code used by
two components of the same feature stays in that feature rather than moving to
`shared`.

## Pages and Components

Route-level (page) components coordinate UI behavior. Reusable presentation
components receive data through explicit inputs and emit meaningful UI events:

```ts
export class BookCardComponent {
  readonly book = input.required<Book>();
  readonly selected = output<string>();
}
```

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state, and avoid `effect()` when `computed`, a template
binding, or explicit event handling expresses the dependency more clearly.

## RxJS

RxJS earns its place for `HttpClient`, debounced search, cancellation and
switching, combining asynchronous sources, and event streams:

```ts
readonly results = toSignal(
  this.query.valueChanges.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.booksApi.search(term)),
  ),
  { initialValue: [] },
);
```

For manual subscriptions in components or services, tie the lifetime to the
owner, for example with `takeUntilDestroyed()`:

```ts
private readonly destroyRef = inject(DestroyRef);

ngOnInit(): void {
  this.events$
    .pipe(takeUntilDestroyed(this.destroyRef))
    .subscribe(event => this.handle(event));
}
```

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

Frontend API models mirror the published HTTP contract and keep raw HTTP details
out of presentation components.

## HttpClient Configuration

```ts
provideHttpClient(
  withInterceptors([
    authInterceptor,
    errorInterceptor,
  ]),
);
```

```ts
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).accessToken();
  return next(token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req);
};
```

Class-based interceptors need a reason in new code.

## Authentication in the Frontend

A frontend may attach an access token, show authenticated state, hide actions the
user cannot normally perform, and protect navigation with route guards — all
UI/UX concerns. Server-side semantics: `authentication` skill.

## HTTP Errors

When the backend returns `ProblemDetails`, centralize reusable parsing, for
example in an error interceptor or a small mapping helper:

```ts
export interface ProblemDetails {
  type?: string;
  title?: string;
  status?: number;
  detail?: string;
  errors?: Record<string, string[]>;
}
```

Map stable fields (`status`, `errors`, an error code) to UI behavior. Backend
status semantics: `http-api` skill.

## Forms

Reactive forms suit non-trivial forms where explicit state, validation, and
testability help:

```ts
readonly form = inject(NonNullableFormBuilder).group({
  title: ['', [Validators.required, Validators.maxLength(TITLE_MAX_LENGTH)]],
});
```

Keep transport/request mapping explicit. Limits such as `TITLE_MAX_LENGTH` mirror
backend constraints from `CUSTOM_SETTINGS.md`; complex Domain rules stay out of
TypeScript unless the UI genuinely needs an equivalent user-facing rule.

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

Start with component state, signals, a feature service or store, and RxJS
composition. A dedicated state-management library becomes worth it only when
application complexity demonstrates the need (adding one goes through
`add-dependency`; NgRx is not part of the default stack).

## Shared Components

`shared` holds reusable UI primitives or behavior that genuinely crosses
features — a confirmation dialog, a generic loading indicator, a reusable table
primitive, a formatting pipe — not a dumping ground.

## Angular Material

When the project uses Angular Material (the default stack), use its components
consistently for common UI primitives where they meet the requirement, and do not
wrap every Material component in a custom abstraction without a concrete reason.

## API Client Generation

When OpenAPI client generation is adopted: keep generated code separate from
handwritten feature logic, regenerate it when the API contract changes, and fix
the source contract rather than patching generated files
(`build-fix` workflow § Generated Code; `swagger` skill for the backend contract).

## Testing

Test frontend behavior at the appropriate level — meaningful component behavior,
validation, data-access request mapping, important route/auth behavior, complex
reactive state — not Angular framework internals. Vitest is the baseline runner
for new projects; use the runner the workspace configures:

```ts
it('requests books from the API', () => {
  const http = TestBed.inject(HttpTestingController);
  TestBed.inject(BooksApi).getBooks().subscribe();
  http.expectOne('/api/books').flush([]);
  http.verify();
});
```

End-to-end tests (Playwright when adopted) focus on a small number of important
user workflows unless the project requires broader coverage. Avoid duplicating
the same behavior at every test level.

## Performance

Start with route lazy loading and sensible rendering and data access; introduce
memoization, virtual scrolling, or custom change-detection work after identifying
a real need.

## Common Mistakes

- giant `shared` directories;
- global service folders mixing unrelated feature services;
- converting every Observable to a Signal, or choosing either merely because it
  is newer;
- parsing human-readable backend error strings.
