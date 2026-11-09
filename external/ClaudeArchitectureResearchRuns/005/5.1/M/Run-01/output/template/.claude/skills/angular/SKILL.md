---
name: angular
description: >
  Use when creating, modifying, reviewing, or testing Angular code: standalone
  components, feature folders, routes and lazy loading, signals and RxJS,
  HttpClient data-access services, functional interceptors, reactive forms,
  ProblemDetails handling, guards, Angular Material, generated API clients, or
  frontend tests.
---

> Owns: Angular implementation technique and examples | Scope: frontend | Loads: on demand (knowledge skill)

# Angular

Policy owners: structure, components, HTTP boundary, state/reactivity, routing,
forms → `.claude/rules/angular.md`; frontend stack and library limits →
`docs/technology-stack.md`; server-side authorization, CSRF, token storage →
`.claude/rules/security.md`.

## Suggested Structure

```text
src/app/
  core/            auth/, http/, layout/
  shared/          components/, directives/, pipes/
  features/
    books/
      pages/  components/  data-access/  models/
      books.routes.ts
    account/
      pages/  data-access/
      account.routes.ts
  app.config.ts
  app.routes.ts
```

Create directories only when they contain meaningful code. `shared` fits
genuinely cross-feature UI primitives (confirmation dialog, loading indicator,
table primitive, formatting pipe).

## Standalone Components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {
  readonly books = input.required<Book[]>();
  readonly selected = output<string>();
}
```

Route-level/page components coordinate UI behavior; reusable presentation
components take explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);
readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state; avoid `effect()` when `computed`, template
binding, or explicit event handling expresses the dependency more clearly.

## RxJS

Good fits: `HttpClient`, debounced search, cancellation/switching
(`switchMap`), combining asynchronous sources, event streams.

```ts
private readonly destroyRef = inject(DestroyRef);

ngOnInit(): void {
  this.searchTerms.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.booksApi.search(term)),
    takeUntilDestroyed(this.destroyRef),
  ).subscribe(results => this.results.set(results));
}
```

`toSignal()` bridges an Observable into template state without a manual
subscription.

## Data-Access Services

```ts
@Injectable({ providedIn: 'root' })
export class BooksApi {
  private readonly http = inject(HttpClient);

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('/api/books');
  }
}
```

## HttpClient Configuration

```ts
provideHttpClient(
  withInterceptors([authInterceptor, errorInterceptor]),
);

export const errorInterceptor: HttpInterceptorFn = (req, next) =>
  next(req).pipe(
    catchError((error: HttpErrorResponse) => throwError(() => toApiError(error))),
  );
```

`toApiError` is a central `ProblemDetails` parser (status, `title`, stable
`code`/`errors` fields) that features consume instead of message text.

## Authentication in the Frontend

A frontend may attach access tokens (functional interceptor), display
authenticated state, hide actions, and guard navigation with functional
`CanActivateFn` guards; their security role is defined in `security.md`.
Server-side technique: `authentication`.

## Forms

```ts
readonly form = inject(NonNullableFormBuilder).group({
  title: ['', [Validators.required, Validators.maxLength(TITLE_MAX_LENGTH)]],
});
```

Keep transport/request mapping explicit. Mirror a backend limit only when the UI
needs it, sourcing the value from the approved setting (`CUSTOM_SETTINGS.md`)
and keeping it synchronized (`custom-settings`). Do not duplicate complex Domain
rules in TypeScript without a user-facing need.

## Routing

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () => import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` also suits individual standalone route components.

## State Management Progression

component state → signals → feature service/store → RxJS composition → a
state-management library only when complexity demonstrably requires it (a new
library goes through `add-dependency` and may be Reserved).

## Angular Material

Use Material components consistently for common UI primitives where they meet
the requirement; do not wrap every Material component in a custom abstraction
without a concrete reason.

## Generated API Clients

When OpenAPI client generation is adopted, keep generated code separate from
handwritten feature logic, regenerate it when the contract changes, and fix the
source rather than patching generated files (`build-fix`).

## Testing

Use the configured runner (Vitest for new projects). Useful targets: meaningful
component behavior, validation, data-access request mapping
(`provideHttpClientTesting()` + `HttpTestingController`), important route/auth
behavior, complex reactive state. Do not test framework internals. Keep E2E
(Playwright, when adopted) to a few important user workflows under
`frontend/<Name>.Web/e2e/`, and avoid duplicating the same behavior at every
level.

## Performance

Start with lazy routes and sensible rendering/data access. Add memoization,
virtual scrolling (`@angular/cdk/scrolling`), or custom change-detection work
only after identifying a real need.
