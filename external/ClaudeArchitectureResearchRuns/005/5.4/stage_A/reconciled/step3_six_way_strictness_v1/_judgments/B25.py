from jdsl import C, D, P  # noqa: F401

_FR = "frontend path rule (paths: frontend/**)"

P("FE-001",
  dims=["D1 modern standalone Angular APIs for new code, organized primarily by feature; NgModules only when an integration or legacy dependency requires them"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each " + _FR + ": M rules/angular.md:17-20, M1 rules/frontend-framework.md:12-14, L0 rules/2-technology/angular.md:12, L1 rules/2-technology/frontend/framework.md:10, K0 rules/frontend/angular.md:19, K1 rules/frontend/frontend-framework.md:10. The explicit NgModule exception sits in the rule for five candidates and in L1's angular skill :38 (plus capabilities/frontend/angular/commands.md:35 'adding NgModules to work around a standalone configuration problem' is an invalid shortcut); L1's rule already requires standalone APIs for new code, so the sentence restates it. Stored modality MUST_NOT (M, M1) vs DEFAULT is the same default with its exception.")

P("FE-002",
  dims=["D1 pages/components focus on presentation and UI orchestration; trivial presentation logic is not moved into services merely to shrink components"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _FR + ": M angular.md:28-30, M1 rules/frontend.md:26-28, L0 rules/1-architecture/frontend-structure.md:19, L1 rules/0-core/frontend.md:10, K0 angular.md:24, K1 rules/frontend/frontend.md:15. code-review skills in M, M1, L0 and L1 repeat it as a review item.")

P("FE-003",
  dims=["D1 backend communication in explicit feature data-access services/HTTP boundary; no HttpClient calls scattered through presentation components; no backend Domain types imported into Angular"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each " + _FR + ": M angular.md:39-43, M1 frontend.md:32-35, L0 frontend-structure.md:20, L1 0-core/frontend.md:11 (also names persistence types), K0 angular.md:25, K1 frontend.md:21. 'Use frontend API models that match the published HTTP contract' is in the rule for five and in L1's angular skill :63; the canonical ban on importing backend Domain types is in L1's rule. build-fix skills in all six list the matching invalid shortcuts.")

P("FE-004",
  dims=["D1 Signals for synchronous local UI state, RxJS for async streams/HTTP composition/cancellation/event pipelines; no mechanical conversions"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each " + _FR + ": M angular.md:31-33, M1 frontend-framework.md:15-17, L0 2-technology/angular.md:13, L1 framework.md:11, K0 angular.md:30, K1 frontend-framework.md:11.")

P("FE-005",
  dims=["D1 route-level lazy loading for meaningful features; not every tiny component"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each " + _FR + ": M angular.md:53-54, M1 frontend.md:47-48, L0 frontend-structure.md:15, L1 0-core/frontend.md:13, K0 angular.md:37, K1 frontend.md:16; angular skills in all six add the same loadComponent/loadChildren technique.")

P("FE-006",
  dims=["D1 simple component/signal/feature-service state before a state-management library"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each " + _FR + ": M angular.md:34-35, M1 frontend.md:45-46, L0 frontend-structure.md:21, L1 0-core/frontend.md:14, K0 angular.md:31, K1 frontend.md:17; angular skills in all six give the same escalation path (component state, signals, feature service/store, RxJS, then a library only for demonstrated complexity). The library itself is a dependency decision (DEP-015).")
