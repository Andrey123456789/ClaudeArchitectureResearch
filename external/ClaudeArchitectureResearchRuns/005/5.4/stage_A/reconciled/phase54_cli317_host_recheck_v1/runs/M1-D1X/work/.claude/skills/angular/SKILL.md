---
name: angular
description: >
  Use for Angular code or setup: standalone components, routes and lazy
  loading, Signals/RxJS, HttpClient data access, interceptors, Reactive Forms,
  Material, Vitest/Playwright tests, ng new scaffolding.
---

> Capability: frontend/angular · Knowledge skill · Technique only · Policy: `.claude/rules/frontend.md`, `.claude/rules/frontend-framework.md`, `.claude/rules/security.md`

# Angular

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

Route-level page components coordinate UI behavior. Reusable presentation
components receive data through explicit inputs and emit meaningful UI events.

## Signals

```ts
readonly loading = signal(false);
readonly selectedBookId = signal<string | null>(null);

readonly hasSelection = computed(
  () => this.selectedBookId() !== null
);
```

Use `computed` for derived state. Avoid unnecessary `effect()` when `computed`,
template binding, or explicit event handling expresses the dependency more
clearly.

## RxJS

RxJS provides real value for `HttpClient`, debounced search,
cancellation/switching, combining asynchronous sources, and event streams.
Compose with operators such as `switchMap`, `combineLatest`, and `debounceTime`
instead of nesting subscriptions.

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

Do not introduce class-based interceptors without a reason.

## Authentication in the UI

The frontend may attach an access token, display authenticated state, hide
actions the user is not permitted to perform, and protect navigation with route
guards. These are UX concerns; server-side authorization stays authoritative
(`.claude/rules/security.md`), and server-side authentication semantics follow
the `authentication` skill.

## HTTP Errors

When backend errors use `ProblemDetails`, map them in one reusable place — for
example an error interceptor plus a small parsing helper — and expose
UI-friendly error state to features. Backend status semantics: `http-api`
skill.

## Forms

Reactive Forms give explicit state, validation, and testability for
non-trivial forms. Keep transport/request mapping explicit, and do not
duplicate complex Domain rules in TypeScript unless the UI genuinely needs an
equivalent user-facing rule.

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

For an individual standalone route component, `loadComponent` is also
appropriate.

## State Management

Start with component state, Signals, a feature service/store, and RxJS
composition. Introduce a dedicated state-management library only when
application complexity demonstrates a need (not by default:
`docs/capabilities/frontend.md`).

## Shared Components

Good `shared` candidates: a confirmation dialog, a generic loading indicator, a
reusable table primitive, a formatting pipe.

## Angular Material

When the project has chosen Angular Material, use its components consistently
for common UI primitives where they satisfy the requirement. Do not add it
automatically to a project that has not chosen it, and do not wrap every
Material component in a custom abstraction without a concrete reason.

## API Client Generation

When OpenAPI client generation is adopted, treat generated code as generated:
keep it separate from handwritten feature logic and regenerate it when the API
contract changes (`build-fix` § Generated Code). Backend contract
documentation: `swagger` skill.

## Testing

Useful frontend test targets: meaningful component behavior, validation,
data-access request mapping, important route/auth behavior, and complex
reactive state. Do not test Angular framework internals. End-to-end tests focus
on a small number of important user workflows unless the project requires
broader E2E coverage; do not duplicate the same behavior at every test level.

## Performance

Do not prematurely optimize normal Angular code. Use route lazy loading and
sensible rendering and data access first; introduce memoization, virtual
scrolling, custom change-detection work, or other optimizations after
identifying a real need.

## Security Review Notes

Deliberate sanitizer bypasses deserve investigation during security review:
`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`,
`bypassSecurityTrustResourceUrl`, and direct DOM manipulation with untrusted
content. Ordinary Angular binding is escaped/sanitized by the framework.

## Review Checks

Check-by-reference against `frontend.md`, `frontend-framework.md`, and
`security.md`: new NgModules without a reason; HTTP calls scattered through
components; global service folders with unrelated feature services; state
frameworks by default; manual subscriptions without lifecycle handling;
business logic in interceptors; frontend-only authorization; parsing
human-readable backend error strings; giant `shared` directories; converting
every Observable to a Signal; choosing Signals or RxJS merely because one is
newer.

## Scaffolding

- Create the workspace under `frontend/<Name>.Web/` with the current Angular
  CLI (`ng new`), using the baseline in `docs/capabilities/frontend.md`:
  standalone APIs, strict mode, routing, SCSS, zoneless change detection when
  the selected stable version supports it, and the CLI's Vitest unit-test
  setup.
- Let the CLI select mutually compatible Angular, TypeScript, and RxJS
  versions; add Angular Material/CDK with `ng add @angular/material` through
  `add-dependency`.
- Unit and component tests stay colocated in the workspace; Playwright E2E
  tests, when required, live under `frontend/<Name>.Web/e2e/`.
- Build and test through the scripts the workspace defines (for example
  `npm run build`, `npm test`).
