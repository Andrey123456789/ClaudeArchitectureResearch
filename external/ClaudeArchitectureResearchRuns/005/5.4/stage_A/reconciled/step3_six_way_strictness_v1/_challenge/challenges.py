# Gate C challenge content (Step 3 analyst; same model family as the judge: a self-challenge, not independent confirmation).
# ROOT(id, questions, for_, against, exceptions, verdict, limit)

ROOT("RC-ENF-REFERENCE-CMD-GATE",
     questions=["Is each stronger-side gate registered for the shell tool?", "Does M have any pre-execution reference gate elsewhere?", "Can the gate be bypassed so the difference disappears?"],
     for_="PreToolUse is registered for Bash|PowerShell with onFailure block in all six (settings.json read). PROBE-HOOK-01 P5/P6: K1 and L0 block, L1 asks, M1 and K0 deny until a marker, M allows (both runs).",
     against="M's dependency-guard reminds after the command (:282-285); searched M hooks and scripts for a pre-execution reference deny: none. All six can change the graph by editing a .csproj, which no PreToolUse gate covers; edits get post-change feedback that differs only non-materially (RC-ENF-RESERVED-GRAPH).",
     exceptions="K1 opens for an edge recorded as an accepted decision; M1/K0 open with a self-written marker; L1 opens on the user's answer.",
     verdict="HOLDS", limit="Material for the command route only; agents that edit project files directly see no pre-execution difference. Live display of ask/deny NOT_RUN.")
ROOT("RC-ENF-DEP-INSTALL-GATE",
     questions=["Does a self-written marker make the gate meaningless?", "Is the K1 'exact version' block the same mechanism?"],
     for_="PROBE-HOOK-01 P1–P4: M1/K0 refuse until the marker, L1 refuses once, K1 blocks only without an exact version, M/L0 allow and remind afterwards. The refusal text routes the agent to add-dependency before the install runs.",
     against="Markers are self-attested; nothing verifies that deprecation, vulnerability and license checks were done. The difference is an enforced extra step, not a guarantee.",
     exceptions="Restore-only installs are not gated (M1). Peer-dependency bypass is refused in all six regardless (PROBE-HOOK-02 Q1–Q10).",
     verdict="HOLDS", limit="The first-attempt outcome differs (refused vs executed); whether a live agent then performs the checks is NOT_RUN.")
ROOT("RC-ENF-INNER-LAYER",
     questions=["Do M, L0 or K0 have an inner-layer check anywhere?", "Are M1's namespace check and L1/K1's package check equivalent?"],
     for_="M1 check-architecture.js reads forbiddenNamespaces for the inner layers from its capability module; L1 check-architecture.mjs and K1 facets/architecture-style.cjs flag ASP.NET Core / EF Core packages and framework references in Application/Domain; all run from post-change hooks.",
     against="Searched M check-manifests.mjs, L0 manifest-checks.mjs and K0 check-dependencies.cjs for inner-layer framework or EF Core rules: none (K0 checks reference direction, not packages).",
     exceptions="M1 detects code namespaces, L1/K1 detect packages: a namespace without a package reference (or the reverse) is caught by only one side; both are stronger than no check.",
     verdict="HOLDS", limit="Source-read; not executed on a fixture.")
ROOT("RC-ENF-MEDIATOR-PKG",
     questions=["Is the mediator ban weaker in K1's text?"],
     for_="M1, L0, L1 flag MediatR and Kommand; M and K0 flag MediatR only; K1 has no mediator package flag (searched check-manifests.cjs and facets).",
     against="Mediator/CQRS adoption is Reserved in all six root files, so the text is the same; the difference is mechanical only.",
     exceptions="", verdict="HOLDS", limit="Source-read.")
ROOT("RC-ENF-TEST-REFS",
     questions=["Does L0 check test-project references anywhere?"],
     for_="M, M1, L1, K1 report an atypical test reference as a finding; K0 adds a notice (check-dependencies.cjs:151-157).",
     against="Searched L0 hooks and manifest checks: no test-reference rule.", exceptions="", verdict="HOLDS", limit="Source-read.")
ROOT("RC-ENF-COMPETING-TEST-FW",
     questions=["Do M, L0, K0 flag xUnit/MSTest/TUnit anywhere?"],
     for_="M1 (MODULE.md competingFrameworkPackages), L1 (nunit/enforcement.json), K1 (facets/test-framework.cjs) flag a second framework after manifest edits.",
     against="Searched M, L0, K0 hooks and scripts for xunit/MSTest/TUnit: none. Text forbids a second framework in all six.",
     exceptions="", verdict="HOLDS", limit="Source-read.")
ROOT("RC-ENF-PKG-LISTS",
     questions=["Is AutoMapper approved anywhere, so the flag would be wrong?"],
     for_="AutoMapper is flagged by K0, L0, L1 only; Mapster is the approved mapper in all six (DEP-011).",
     against="The lists encode each candidate's own stack; direct Polly is flagged by all six and MediatR by all but K1, so the asymmetry is per package, not a uniform ordering.",
     exceptions="", verdict="HOLDS", limit="Coverage difference, not rule difference; source-read.")
ROOT("RC-ENF-MIGRATION-REMINDER",
     questions=["Are the two directions one root or two facts?", "Do Stop reminders actually block?"],
     for_="Model-without-migration reminder (PST-009): M1, L1, K1; changed-migration review reminder (PST-010): M, L0, K0, K1. All six Stop hooks block once per change state (settings and hook code read).",
     against="Reminders block finishing once and accept a stated reason; they never prevent a missing migration.",
     exceptions="", verdict="HOLDS", limit="Opposite directions per policy; only K1 has both. Host re-invocation after a Stop block NOT_RUN.")
ROOT("RC-ENF-IDE0005-BUILD",
     questions=["Is the claim that only L0's CLI build reports IDE0005 verified?", "Is M's configuration a defect?"],
     for_="L0 sets IDE0005 warning, EnforceCodeStyleInBuild and GenerateDocumentationFile (CS1591 suppressed). M sets the first two but not GenerateDocumentationFile, which M's own .editorconfig:32-33 says is also required.",
     against="No build was run in Step 3; the claim rests on the documented MSBuild requirement and M's own comment.",
     exceptions="", verdict="HOLDS_WITH_LIMIT", limit="Source-read; build NOT_RUN. M's configuration contradicts its own comment (change proposal CP-01).")
ROOT("RC-ENF-TOP-LEVEL-TESTS",
     questions=["Do M1 or K0 see a project under tests/?"],
     for_="L1 check.json forbiddenTopLevelDirectories ['tests'] reported after project-file edits; K1 checkAll warns in verify.",
     against="M1 check-architecture.js and K0 check-dependencies.cjs walk only backend/; M and L0 have no layout check.",
     exceptions="", verdict="HOLDS", limit="Source-read.")
ROOT("RC-ENF-NPMRC-BYPASS",
     questions=["Is an .npmrc bypass a realistic task outcome?", "Do the other five catch it some other way?"],
     for_="Only L0 treats .npmrc as a manifest (manifest-checks.mjs:71, :453-457). grep: no .npmrc handling in M, M1, L1, K0, K1.",
     against="It requires the agent to work around a refused command; all six refuse every shell form (PROBE-HOOK-02).",
     exceptions="", verdict="HOLDS_WITH_LIMIT", limit="Material only under AD-4; sensitivity S-EVASION makes DEP-025 FULL.")
ROOT("RC-ENF-DEP-REMOVAL-GATE",
     questions=["Is the removal text the same in all six?", "Is K1's block an omission or a design?"],
     for_="PROBE-HOOK-03: removal and bare-update commands — M/L0 allow, M1/K0 marker, L1 once, K1 block; K1 add-dependency :80 prescribes manifest edits and restore instead.",
     against="Same removal procedure text in all six add-dependency skills; not a canonical policy.",
     exceptions="", verdict="HOLDS", limit="Extras-level root; live host NOT_RUN.")

ITEM("SAW-GOV-007-K1", kind="STRONGER_AND_WEAKER_CELL", target="GOV-007/K1",
     questions=["Is K1 weaker than its peers on GOV-007?"],
     for_="v3 'stronger' evidence: FG-K1-68a63438b7, development-workflow :48 MUST 'update the durable source of truth in the same change' (Step 3: K1 in the stricter 'same change' tier with L0, L1).",
     against="v3 'weaker' evidence: FG-K1-5e58bef88f / FG-K1-6175d8f714, actual-state.cjs :181/:183 SHOULD reminders when SPECIFICATION.md or CUSTOM_SETTINGS.md change. All six have an equivalent post-edit reminder (GOV-007 same-text: M file-change.mjs:40-45, M1 post-tool-use.js:72-74, L0 claude-hook.mjs:657-662, L1 post-change-checks.mjs:322-323, K0 hook.cjs:468).",
     exceptions="", verdict="HOLDS", limit="The mixed label is a MUST rule plus advisory reminders present in all six; GOV-007 stays PARTIAL for the 'same change' timing delta, not for a K1 weakness.")
ITEM("CP-01", kind="CHANGE_PROPOSAL", target="M Directory.Build.props",
     questions=["Should M's IDE0005 build setup be repaired?"],
     for_="M's .editorconfig:32-33 states that IDE0005 at build needs GenerateDocumentationFile; M's Directory.Build.props sets EnforceCodeStyleInBuild but not GenerateDocumentationFile.",
     against="Whether M intends build-time IDE0005 is a design choice; the comment may be the error.",
     exceptions="", verdict="OPEN",
     limit="Proposal, not applied: either add GenerateDocumentationFile=true with NoWarn CS1591 to M's Directory.Build.props, or correct the comment. Expected impact: RUN-010 D2 would place M with L0. Requires a separately approved repair with full regression.")
ITEM("RD-01", kind="RECORD_DISCREPANCY", target="FG-L1-5a6df8a726 (extras X0286)",
     questions=["Does L1 let the user confirm a peer-dependency bypass?"],
     for_="Stored claim: 'commands with these flags run only after the user confirms'.",
     against="Current line pre-shell-command.mjs:254: 'No confirmation, comment marker, or approval opens this route.' PROBE-HOOK-02 Q1–Q10: L1 denies on both runs, with and without markers.",
     exceptions="", verdict="REVISED", limit="Step 3 relies on the current line and the probe; the v3 claim text needs a data correction (not edited).")
ITEM("RD-02", kind="RECORD_DISCREPANCY", target="FG-M1-159a4ef4c3 (extras X0791)",
     questions=["Does M1's marker open the peer-dependency bypass?"],
     for_="Stored claim: 'the flags are denied whatever the purpose, unless the marker is present'.",
     against="PROBE-HOOK-02 Q9/Q10: M1 denies `--legacy-peer-deps` and `--force` carrying both markers on both runs; M1 add-dependency :115-118 says no marker opens the route.",
     exceptions="", verdict="REVISED", limit="Data correction proposed; DEP-025 D1 parity holds.")
ITEM("FAIR-01", kind="BENCHMARK_FAIRNESS", target="Enforcement asymmetry (11 material roots)",
     questions=["Could the asymmetry bias a later practical comparison?"],
     for_="M1, L1, K1 deliver more mechanical checks; M and L0 more reminders; M1/K0 add marker steps; K1 requires recorded edges before reference commands.",
     against="All of them implement the same normative text; they are architecture-specific enforcement choices that are part of what the experiment compares.",
     exceptions="", verdict="OPEN",
     limit="Not a Step 3 decision. A practical experiment should log hook interventions per candidate so outcome differences can be attributed (host behavior NOT_RUN).")
ITEM("FAIR-02", kind="BENCHMARK_FAIRNESS", target="Report-content extras (RC-TXT-REPORT-*) and force vocabulary",
     questions=["Would grading final reports favour some candidates?"],
     for_="Seven report/review-output items and the default-deviation reporting duty differ by candidate (EXTRA_GENUINE_ROOTS.json).",
     against="None changes the engineering outcome of a task.", exceptions="", verdict="OPEN",
     limit="Relevant only if reports are graded; listed for the user (OPEN_DECISIONS_AND_SENSITIVITY.md section 4).")
