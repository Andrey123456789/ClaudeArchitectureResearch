---
name: angular
description: >
  Use when writing or reviewing Angular code: standalone components, routes and
  lazy loading, Signals, RxJS, HttpClient services, interceptors, reactive
  forms, guards, ProblemDetails handling, Material, Vitest tests.
---

> Kind: KNW | Scope: frontend | Capability: frontend/angular | Loading: on-demand knowledge

# Angular

Policy: `.claude/rules/frontend/frontend.md`, `.claude/rules/frontend/frontend-framework.md`, `.claude/rules/frontend/security.md`, `.claude/rules/frontend/dependencies.md`. Stack: decision register (frontend row).

## Suggested structure

```text
src/app/
  core/            auth/, http/, layout/
  shared/          components/, directives/, pipes/
  features/
    books/         pages/, components/, data-access/, models/, books.routes.ts
    account/       pages/, data-access/, account.routes.ts
  app.config.ts
  app.routes.ts
```

Create directories only when they contain meaningful code. A feature owns its UI and frontend-specific data-access logic; do not move feature code into `shared` merely because two components of the same feature use it. `shared` holds genuinely cross-feature primitives (confirmation dialog, loading indicator, reusable table primitive, formatting pipe) and must not become a dumping ground.

## Standalone components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Introduce NgModules only when an integration or legacy dependency genuinely requires them. Route-level page components coordinate UI behavior; reusable presentation components receive data through explicit inputs and emit meaningful events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);
readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state. Avoid `effect()` when `computed`, template binding, or explicit event handling expresses the dependency more clearly. Do not convert every Observable into a Signal, and do not pick Signals or RxJS merely because one is newer.

## RxJS

RxJS fits `HttpClient`, debounced search, cancellation/switching (`switchMap`), combining asynchronous sources, and event streams. Compose with operators instead of nesting subscriptions. For manual subscriptions in components or services, tie the lifetime to the framework lifecycle:

```ts
private readonly destroyRef = inject(DestroyRef);

ngOnInit(): void {
  this.search.valueChanges
    .pipe(debounceTime(300), switchMap(term => this.api.search(term)), takeUntilDestroyed(this.destroyRef))
    .subscribe(results => this.results.set(results));
}
```

Prefer the `async` pipe or `toSignal` when they remove the manual subscription entirely.

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

Use frontend API models that match the published HTTP contract. Configure the client with providers:

```ts
provideHttpClient(withInterceptors([authInterceptor, errorInterceptor]));
```

Do not introduce class-based interceptors without a reason.

## Authentication in the UI

The frontend may attach an access token, display authenticated state, hide actions the user cannot normally perform, and protect navigation with route guards — all UX. Server-side semantics: `authentication`.

## HTTP errors

When backend errors use `ProblemDetails`, centralize reusable parsing/mapping (for example in an error interceptor or a shared error mapper) and branch on stable fields such as `status`, `type`, or an error code. HTTP semantics: `http-api`.

## Forms

Reactive forms (rule: `frontend-framework.md`): `FormBuilder` with typed `FormGroup`/`FormControl`, built-in and custom validators, and explicit mapping from form value to request model. Do not duplicate complex Domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule.

## Routing

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () => import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` also fits individual standalone route components.

## State management

Start with component state, Signals, a feature service/store, and RxJS composition; introduce a dedicated state library only when application complexity demonstrates the need.

## Angular Material

When the project has chosen Angular Material, use its components consistently for common UI primitives where they satisfy the requirement; do not add it to projects that have not chosen it, and do not wrap every Material component in a custom abstraction without a concrete reason.

## API client generation

When OpenAPI client generation is adopted, keep generated code separate from handwritten feature logic, regenerate it when the API contract changes, and do not patch generated files unless the generation workflow requires it. Contract documentation: `swagger`.

## Security notes

Template binding is escaped/sanitized by Angular. Investigate deliberate bypasses — `DomSanitizer.bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`, `bypassSecurityTrustUrl`, `innerHTML` with untrusted content, direct DOM manipulation through `ElementRef.nativeElement`. Angular's `HttpClient` XSRF support (`withXsrfConfiguration`) only helps when the backend issues and validates the matching token.

## Testing

Use the workspace's configured runner (Vitest for new projects). Test meaningful component behavior, validation, data-access request mapping (`provideHttpClientTesting`, `HttpTestingController`), important route/auth behavior, and complex reactive state; do not test framework internals or duplicate the same behavior at every level. E2E tests (Playwright, when adopted) cover a small number of important user workflows unless broader coverage is required.

## Performance

Do not prematurely optimize: route lazy loading and sensible rendering/data access first; memoization, virtual scrolling (`@angular/cdk/scrolling`), custom change-detection work, and similar optimizations after identifying a real need.

## Build-fix patterns

Typical Angular failures: template compilation errors, invalid standalone `imports`, missing providers, route configuration errors, Signal/RxJS typing issues, Angular/TypeScript peer-version mismatches. Fix the missing standalone import or provider instead of adding an NgModule to work around a standalone configuration problem.

## Anti-patterns

Avoid NgModules without a reason, global service folders containing unrelated feature services, state frameworks by default, complex business logic in interceptors, giant `shared` directories, and converting every Observable to a Signal.
