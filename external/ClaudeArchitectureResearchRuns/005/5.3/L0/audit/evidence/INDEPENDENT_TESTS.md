# Independent audit evidence

The independent audit did not accept either `GENERATION_REPORT.md` as ground truth.

## Static checks

- Both shipped instruction checkers exit PASS on their own templates.
- All shipped `.js` / `.cjs` / `.mjs` files pass Node syntax checking.
- Run-02 independent Level 0/1 scan found no concrete-technology terms from the audit deny set.
- Run-01 independent Level-1 scan found:
  - `ProblemDetails` in `1-architecture/frontend-structure.md`;
  - an Angular-named `2-technology/angular.md` routing pointer in the same Level-1 rule.
- No `Kind:`, capability contract/module/slot machinery, or K/L1 leakage was found in either runtime template.

## Runtime size/topology

- Run-01: 78 files, 269,166 bytes; 66 Markdown files, 219,933 Markdown bytes; 27 rules; 28 skill directories.
- Run-02: 71 files, 305,547 bytes; 63 Markdown files, 257,463 Markdown bytes; 24 rules; 29 skill directories.
- Whole-template path Jaccard: 0.656.
- Rule-path Jaccard: 0.500.
- Skill-directory Jaccard: 0.900.

## Behavioral hook tests

### Nested cwd launcher

Exact configured launchers were executed from `backend/Demo.Api`:

- Run-01 PreToolUse launcher: exit 0.
- Run-02 PreToolUse launcher: exit 1 with Node module-not-found before hook code ran.

### BOM-prefixed input

A valid hook payload prefixed with UTF-8 BOM was supplied:

- Run-01 dependency guard: exit 1, JSON parse failure.
- Run-02 pre-bash: exit 0, correctly parsed.

### Simulated active worktree product-input edit

With `CLAUDE_PROJECT_DIR` pointing at a main checkout and the edit path/cwd pointing at a separate worktree:

- Run-01 post-edit: exit 0, no `SPECIFICATION.md` reminder (worktree file resolves outside the main-root model).
- Run-02, when launched from the worktree root copy: exit 2 with the expected product-input reminder.

This is why refinement must separate stable launcher location from active repository/worktree root instead of copying either raw strategy unchanged.

### Run-02 command classification

Observed results:

| Command | pre-bash | post-bash |
|---|---:|---:|
| `npm install x --force` | blocked | routed |
| `npm --prefix frontend install x --force` | silent | silent |
| `pnpm --dir frontend add x --force` | silent | silent |
| `yarn --cwd frontend add x --force` | silent | silent |
| `dotnet add Foo.Api.csproj reference Foo.Domain.csproj` | silent | silent |
| `npm install x` | silent | routed |

### Stop fingerprint

In a temporary Git repository:

1. production file modified without test changes -> Stop exit 2 and reminder;
2. same file edited again, same status/file set -> Stop exit 0.

The state fingerprint does not include changed content/diff identity.

### Checker vs modern exec form

A temporary copy of Run-02 settings was changed from shell-form `node <script> <event>` to exec-form `command: node`, `args: [script,event]`. The shipped checker returned FAIL solely because it hardcodes the old serialization. This is a checker defect, not evidence that exec-form is invalid.
