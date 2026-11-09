---
name: angular
description: Angular frontend technique. Use when creating, modifying, or reviewing Angular TypeScript, templates, routes, standalone components, signals, RxJS, HttpClient data-access services, functional interceptors, reactive forms, guards, ProblemDetails handling, lazy loading, Angular Material, or frontend tests.
---

> Level: 2-technology · Capability: frontend/angular · Facet: frontend.knowledge · Owns: Angular implementation technique, examples, security hotspots · Loading: on demand

# Angular

Rules: `.claude/rules/0-core/frontend.md` (neutral structure), `frontend.framework` (Angular rules), frontend stack (imported), security rules. Commands: `frontend.commands`. This skill adds technique only.

## Suggested structure

```text
src/app/
  core/        auth/  http/  layout/
  shared/      components/  directives/  pipes/
  features/
    books/     pages/  components/  data-access/  models/  books.routes.ts
    account/   pages/  data-access/  account.routes.ts
  app.config.ts
  app.routes.ts
```

Create directories only when they hold meaningful code. A feature owns its UI and frontend-specific data access; move code to `shared` only when it genuinely crosses features (confirmation dialog, loading indicator, reusable table primitive, formatting pipe), not because two components in one feature use it.

## Components

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

Do not introduce NgModules for ordinary feature work unless an integration or legacy dependency requires them. Route-level page components coordinate UI behavior; reusable presentation components take explicit inputs and emit meaningful events.

## Signals and RxJS

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);
readonly hasSelection = computed(() => this.selectedBookId() !== null);
```

Use `computed` for derived state and avoid `effect()` when `computed`, template binding, or explicit event handling expresses the dependency more clearly. RxJS fits `HttpClient`, debounced search, cancellation/switching (`switchMap`), combining async sources, and event streams. For manual subscriptions in components or services, `takeUntilDestroyed()` (or the `DestroyRef` it uses) ties lifetime to the owner.

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

Use frontend API models matching the published HTTP contract. Configure the client through providers:

```ts
provideHttpClient(withInterceptors([authInterceptor, errorInterceptor]));
```

Prefer functional interceptors; add a class-based one only with a reason. When backend errors use `ProblemDetails`, centralize parsing/mapping (for example in an error interceptor plus a small mapping helper).

## Authentication in the UI

The frontend may attach an access token, display authenticated state, hide actions the user normally cannot perform, and guard navigation — all UX. Server-side semantics: `authentication` skill.

## Forms

Reactive forms suit non-trivial forms needing explicit state, validation, and testability. Keep transport/request mapping explicit. Do not duplicate complex domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule.

## Routing and state

```ts
export const routes: Routes = [
  {
    path: 'books',
    loadChildren: () => import('./features/books/books.routes').then(m => m.BOOK_ROUTES),
  },
];
```

`loadComponent` suits single standalone route components. State escalation path: component state → signals → feature service/store → RxJS composition → a state library only when demonstrated complexity needs it (approval list: frontend stack).

## Angular Material

Use Material components consistently for common primitives when they satisfy the requirement; do not wrap every Material component in a custom abstraction without a reason.

## Generated API clients

When OpenAPI client generation is adopted, keep generated code separate from handwritten feature code and regenerate it when the contract changes (source-first fixes: `build-fix` § Generated code).

## Testing

Test meaningful component behavior, validation, data-access request mapping, important route/auth behavior, and complex reactive state with the configured runner; do not test framework internals. E2E covers a few important user workflows unless broader coverage is required; avoid duplicating the same behavior at every level.

## Security hotspots

Review deliberate sanitizer bypasses (`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted content; ordinary template binding is escaped/sanitized by the framework and is not automatically XSS.

## Performance

Do not prematurely optimize. Start with route lazy loading and sensible rendering and data access; add memoization, virtual scrolling, or custom change-detection work after identifying a real need.

## Anti-patterns

New NgModules without a reason; HTTP calls scattered through components; global service folders of unrelated feature services; state frameworks by default; unmanaged manual subscriptions; business logic in interceptors; frontend-only authorization; parsing human-readable backend error strings; giant `shared` directories; converting every Observable to a Signal; choosing Signals or RxJS because one is newer.
