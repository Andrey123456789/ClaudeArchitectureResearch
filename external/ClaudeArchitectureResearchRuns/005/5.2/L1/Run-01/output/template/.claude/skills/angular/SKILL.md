---
name: angular
description: >
  Use for Angular code: standalone components, routes, lazy loading, signals,
  RxJS, HttpClient data access, functional interceptors, reactive forms,
  Material, tests.
---
> Level: 2-technology | Capability: frontend/angular (frontend.knowledge) | Owns: Angular technique, examples, testing and security notes | Scope: frontend | Loads: on demand (skill)

# Angular

Policy: `frontend-structure.md` (framework-neutral) and `frontend-framework.md`
(Angular). Commands: `frontend.commands`.

## Suggested structure

```text
src/app/
  core/          auth/, http/, layout/
  shared/        components/, directives/, pipes/
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

Create directories only when they contain meaningful code. A feature owns its UI
and its frontend data access.

## Standalone components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Route/page components coordinate UI behavior; reusable presentation components
take explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state; avoid `effect()` when `computed`, template
binding, or explicit event handling expresses the dependency more clearly.

## RxJS

RxJS fits `HttpClient`, debounced search, cancellation/switching
(`switchMap`), combining asynchronous sources, and event streams. Compose with
operators instead of nesting subscriptions; tie manual subscriptions to the
lifecycle:

```ts
private readonly destroyRef = inject(DestroyRef);

ngOnInit(): void {
  this.search.valueChanges
    .pipe(debounceTime(300), switchMap(q => this.api.search(q)),
          takeUntilDestroyed(this.destroyRef))
    .subscribe(results => this.results.set(results));
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

Frontend API models mirror the published HTTP contract.

## HttpClient configuration

```ts
provideHttpClient(
  withInterceptors([authInterceptor, errorInterceptor]),
);
```

Typical cross-cutting interceptor work: attaching tokens, correlation headers,
mapping `ProblemDetails` into a shared error model.

## Authentication in the UI

The frontend may attach an access token, display authenticated state, hide
actions the user cannot normally perform, and guard navigation — all UX. Server
semantics: `authentication`.

## HTTP errors

Centralize `ProblemDetails` parsing (status, `type`, `title`, `errors` for
validation problems, stable error codes) in one place, for example an error
interceptor plus a mapper used by data-access services.

## Forms

Reactive forms give explicit state, validation, and testability for non-trivial
forms. Keep transport/request mapping explicit; do not duplicate complex domain
rules in TypeScript unless the UI needs an equivalent user-facing rule.

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

`loadComponent` fits individual standalone route components.

## State management

Start with component state, signals, a feature service/store, and RxJS
composition; introduce a state library only when application complexity
demonstrates the need (frontend stack decision).

## Shared components and Angular Material

`shared` is for reusable UI primitives that genuinely cross features
(confirmation dialog, loading indicator, table primitive, formatting pipe), not
a dumping ground. Use Material components consistently for common primitives;
do not wrap every Material component in a custom abstraction without a reason.

## API client generation

When OpenAPI client generation is adopted, keep generated code separate from
handwritten feature code, regenerate it when the contract changes, and patch it
manually only when the generation workflow requires that.

## Testing

Test meaningful component behavior, validation, data-access request mapping
(`provideHttpClientTesting()` with `HttpTestingController`), important
route/auth behavior, and complex reactive state — not framework internals. Keep
E2E tests to a few important user workflows unless broader coverage is
required, and do not duplicate the same behavior at every level.

## Security notes

Angular escapes and sanitizes ordinary template bindings. Review deliberate
sanitizer bypasses — `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`,
`bypassSecurityTrustStyle`, `bypassSecurityTrustUrl`,
`bypassSecurityTrustResourceUrl` — and direct DOM manipulation (`innerHTML` via
`ElementRef`, `Renderer2` with untrusted content) during security reviews.

## Performance

Start with route lazy loading and sensible rendering/data access; add
memoization, virtual scrolling, or custom change-detection work only for an
identified need.

## Anti-patterns

New NgModules without a reason; HTTP calls scattered through components; global
service folders of unrelated feature services; state frameworks by default;
manual subscriptions without lifecycle handling; business logic in
interceptors; frontend authorization as the only authorization; parsing
human-readable backend error strings; giant `shared` directories; converting
every Observable to a Signal; choosing Signals or RxJS merely because one is
newer.
