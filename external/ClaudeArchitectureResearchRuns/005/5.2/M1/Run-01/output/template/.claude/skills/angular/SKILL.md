---
name: angular
description: >
  Angular technique: standalone components, routes, Signals and RxJS, HttpClient
  services, functional interceptors, reactive forms, Material, Vitest, ng CLI
  scaffold/verify, Angular build errors.
---

> **Knowledge skill** · Capability: frontend/angular · Owns: Angular technique, examples, scaffold/verify commands, build-fix and security-review cues · Scope: frontend · Loading: on demand

# Angular

## Rules

Framework-independent frontend rules: `frontend.md`. Angular-specific rules:
`frontend-framework.md`. Stack decisions: `docs/frontend-stack.md`. Server-side
authorization and browser-credential rules: `security.md`. This skill shows how to
apply them.

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

Create directories only when they contain meaningful code.

Do not create empty architecture folders solely to satisfy the template.

## Standalone Components

Use standalone components for new Angular code.

```ts
@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.component.html',
})
export class BookListComponent {}
```

New code uses standalone components (`frontend-framework.md` → Angular APIs).

## Feature Organization

A feature owns the UI and frontend-specific data-access logic it requires; the
structure rules are in `frontend.md` → Structure.

## Pages and Components

Route-level/page components coordinate UI behavior.

Reusable presentation components should receive data through explicit inputs and
emit meaningful UI events.

Responsibility limits: `frontend.md` → Presentation and Data Access.

## Signals

Use Signals for state that is naturally synchronous and local to Angular UI:

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state.

Avoid unnecessary `effect()` when `computed`, template binding, or explicit
event handling expresses the dependency more clearly.

Choosing between Signals and RxJS: `frontend-framework.md` → Signals and RxJS.

## RxJS

Use RxJS when its stream model provides real value, for example:

- `HttpClient`;
- debounced search;
- cancellation/switching;
- combining asynchronous sources;
- event streams.

Compose instead of nesting subscriptions:

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

When a manual subscription is needed in framework-managed code, bind its lifetime:

```ts
this.events$
  .pipe(takeUntilDestroyed(this.destroyRef))
  .subscribe(event => this.handle(event));
```

## HTTP

Keep API communication in feature data-access services or another explicit HTTP
boundary.

```ts
@Injectable({ providedIn: 'root' })
export class BooksApi {
  private readonly http = inject(HttpClient);

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('/api/books');
  }
}
```

Frontend API models follow the published HTTP contract (`frontend.md`).

## HttpClient Configuration

Use modern provider-based configuration when configuration is required:

```ts
provideHttpClient(
  withInterceptors([
    authInterceptor,
    errorInterceptor,
  ]),
);
```

A functional interceptor:

```ts
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthTokenStore).token();
  return next(token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req);
};
```

## Authentication

A frontend may:

- attach an access token;
- display authenticated state;
- hide actions the user cannot normally perform;
- protect navigation with route guards.

These are UI/UX concerns; server-side authorization stays authoritative
(`security.md`). Server-side semantics: the `authentication` skill.

## HTTP Errors

Rules: `frontend.md` → API Errors. A central mapping helper:

```ts
export function toApiError(error: HttpErrorResponse): ApiError {
  const problem = error.error as ProblemDetails | null;
  return {
    status: error.status,
    code: problem?.['code'] ?? null,
    title: problem?.title ?? 'Request failed',
    fieldErrors: problem?.['errors'] ?? {},
  };
}
```

Backend HTTP semantics: the `http-api` skill.

## Forms

Rules: `frontend.md` → Forms and Validation. Keep transport/request mapping
explicit, and do not duplicate complex Domain rules in TypeScript unless the UI
genuinely needs an equivalent user-facing rule.

```ts
readonly form = inject(NonNullableFormBuilder).group({
  title: ['', [Validators.required, Validators.maxLength(this.settings.titleMaxLength)]],
});
```

## Routing

Route-level lazy loading (when to use it: `frontend.md` → Structure):

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

Start with:

```text
component state
signals
feature service/store
RxJS composition
```

State-library policy: `frontend.md` and `docs/frontend-stack.md`.

## Shared Components

`shared` is appropriate for reusable UI primitives or behavior that genuinely
crosses features.

Examples:

```text
confirmation dialog
generic loading indicator
reusable table primitive
formatting pipe
```

Do not use `shared` as a dumping ground.

## Angular Material

When the project has chosen Angular Material, use its components consistently
for common UI primitives where they satisfy the requirement.

Do not add Angular Material automatically to projects that have not chosen it.

Do not wrap every Material component in a custom abstraction without a concrete
reason.

## API Client Generation

When OpenAPI client generation is adopted, keep generated code separate from
handwritten feature logic and regenerate it when the API contract changes; repairs
to generated output go to its source (`build-fix` → Generated Code). Backend
contract documentation: the `swagger` skill.

## Scaffold and Verify Commands

```bash
npx @angular/cli@latest new MyApp.Web --directory frontend/MyApp.Web --routing --style=scss --strict
cd frontend/MyApp.Web
npx ng add @angular/material
npm run build
npm test
```

Check the CLI's current options (for example zoneless and the default test
runner) for the selected stable version, and confirm the scripts that actually
exist in `package.json` before running them.

## Build-Fix Specifics

Angular-specific failure categories: invalid standalone import, provider missing
from `app.config.ts` or a route, signal/RxJS typing issue, Angular/TypeScript
peer-version mismatch. Do not add NgModules merely to work around a standalone
configuration problem, convert code to `any`, or disable strict mode to make code
compile.

## Security Review Cues

Investigate deliberate sanitizer bypasses — `bypassSecurityTrustHtml`,
`bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`,
`bypassSecurityTrustUrl` — and direct DOM manipulation (`ElementRef`
`nativeElement.innerHTML`) with untrusted content. Ordinary template binding is
escaped/sanitized by Angular. `HttpClient` XSRF support
(`withXsrfConfiguration`) only helps when the backend issues and validates the
token.

## Testing

Test frontend behavior at the appropriate level.

Useful targets include:

- meaningful component behavior;
- validation;
- data-access request mapping;
- important route/auth behavior;
- complex reactive state.

Do not test Angular framework internals.

End-to-end tests should focus on a small number of important user workflows
unless the project explicitly requires broader E2E coverage.

Do not duplicate the same behavior unnecessarily at every test level.

## Performance

Do not prematurely optimize normal Angular code.

Use route lazy loading and sensible rendering/data access first.

Introduce specialized memoization, virtual scrolling, custom change-detection
work, or other optimizations after identifying a real need.

## Anti-Patterns

Avoid:

- new NgModules without a reason;
- global service folders containing unrelated feature services;
- manual subscriptions without lifecycle handling;
- giant `shared` directories;
- converting every Observable to a Signal;
- using Signals or RxJS merely because one is newer than the other.
