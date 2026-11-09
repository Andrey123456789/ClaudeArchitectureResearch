---
name: angular
description: >
  Use when writing or reviewing Angular code: components, signals/RxJS,
  HttpClient data access, interceptors, ProblemDetails errors, reactive forms,
  routes and guards, state, Material, frontend tests.
---

> Level: 2 Technology · Owns: Angular implementation technique · Scope: frontend · Loads: on demand (knowledge skill)

# Angular

Policy owners: `.claude/rules/1-architecture/frontend-structure.md` (features, presentation, data access, error contract, validation role, lazy loading, state), `.claude/rules/2-technology/angular.md` (standalone, signals/RxJS, forms, interceptors, subscriptions, npm), `.claude/rules/0-core/security-principles.md` (server authorization, CSRF, token storage).

## Suggested structure

```text
src/app/
  core/            auth/, http/, layout/  — app-wide singletons, kept small
  shared/          components/, directives/, pipes/ — genuinely cross-feature UI only
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

Create directories only when they hold real code. Feature-specific code shared by two components of the same feature stays in that feature.

## Standalone components

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

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);
readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

`toSignal`/`toObservable` bridge the models where a boundary genuinely needs it.

## RxJS

Good fits: `HttpClient`, debounced search, cancellation/switching (`switchMap`), combining asynchronous sources, event streams. Compose instead of nesting:

```ts
readonly results = toSignal(
  this.query$.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(q => this.booksApi.search(q)),
  ),
  { initialValue: [] },
);

// manual subscription tied to the lifecycle
this.events$.pipe(takeUntilDestroyed(this.destroyRef)).subscribe(e => this.handle(e));
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

Frontend models mirror the published HTTP contract, hand-written or generated (`frontend-structure.md`).

## HttpClient configuration and interceptors

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(withInterceptors([authInterceptor, errorInterceptor])),
    provideRouter(routes),
  ],
};

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).accessToken();
  return next(token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req);
};
```

Interceptors handle cross-cutting concerns (auth headers, correlation, generic error mapping); class-based interceptors only with a reason.

## Authentication in the UI

The frontend may attach tokens, display authenticated state, hide actions the user cannot normally perform and guard navigation — all user experience. Server-side semantics: `authentication` skill.

```ts
export const authGuard: CanActivateFn = () =>
  inject(AuthService).isAuthenticated() || inject(Router).createUrlTree(['/login']);
```

## Error handling

Centralize problem-details parsing:

```ts
export function toApiError(error: HttpErrorResponse): ApiError {
  const problem = error.error as ProblemDetails | null;
  return {
    status: error.status,
    code: problem?.['code'] as string | undefined,
    title: problem?.title ?? 'Unexpected error',
    fieldErrors: problem?.errors ?? {},
  };
}
```

Components branch on `status` and `code` (`frontend-structure.md`); `http-api` describes the backend semantics.

## Forms

```ts
readonly form = inject(NonNullableFormBuilder).group({
  title: ['', [Validators.required, Validators.maxLength(TITLE_MAX_LENGTH)]],
});
```

Keep request mapping explicit; mirror approved limits from `CUSTOM_SETTINGS.md` for user feedback; do not duplicate complex Domain rules in TypeScript unless the UI needs an equivalent user-facing rule.

## Routing

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () => import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` suits a single standalone route component.

## State

Start with component state, signals, a feature service/store and RxJS composition; introduce a state-management library only when complexity demonstrates the need (and through `add-dependency`).

## Angular Material

Use Material components consistently for common primitives when they satisfy the requirement; do not wrap every component in a custom abstraction without a reason.

## Generated API clients

When OpenAPI client generation is adopted: keep generated code separate from handwritten feature logic, regenerate when the API contract changes, review the diff, and fix the generator input rather than hand-patching output (`swagger` skill for the backend side).

## Testing

Test meaningful component behavior, validation, data-access request mapping (`provideHttpClientTesting` + `HttpTestingController`), important route/auth behavior and complex reactive state with the workspace's runner (Vitest for new workspaces). Do not test framework internals; E2E (Playwright, when adopted) covers a few important workflows; avoid duplicating the same behavior at every level.

## Performance

Lazy routes and sensible rendering and data access first; memoization, virtual scrolling (`cdk-virtual-scroll-viewport`) or custom change-detection work only after identifying a real need.

## Review cues

New NgModules without a reason, HTTP calls in many components, global service folders of unrelated feature services, NgRx by default, unmanaged subscriptions, business logic in interceptors, frontend-only authorization, parsing error strings, giant `shared` folders, mechanical Observable↔Signal conversion.
