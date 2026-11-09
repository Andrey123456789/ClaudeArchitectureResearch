# Iteration 006 handoff - inputs from Phase 5.4

**Phase 5.4 status at handoff: CLOSED_VERIFIED**, within the scope stated in `FINAL_STATE.json`. This file lists what the next iteration receives and what it must assume. It contains no benchmark design and no code generation. Iteration 006 has not been started and needs a separate instruction.

All paths are relative to `stage_A/reconciled/`.

## 1. Frozen candidates

Release `phase54-final-v1`. Manifest `phase54_final_acceptance_v1/release/CANDIDATE_FREEZE_MANIFEST.json`, SHA-256 `4058f10d670ae1c2f2c02df5e5ab8dba06217d7e0181c02abb0c6a85a1c6537f`.

| Candidate | Template path | Files | Tree SHA-256 |
|---|---|---|---|
| M | `phase54_final_acceptance_v1/release/candidates/M/template/` | 61 | `e7a6ae1082df120786fcaf77d2bf5967fa31f4febcc69f3912481d2aecac3073` |
| M1 | `phase54_final_acceptance_v1/release/candidates/M1/template/` | 80 | `434d3096585c8fa300f1f632b3488048d4facc7577c441f048df5e32e03c6e60` |
| L0 | `phase54_final_acceptance_v1/release/candidates/L0/template/` | 71 | `24a5c1ba9c5631bf81a66058d7046aa32a24bd6fa7a21a885a04599c578c24a7` |
| L1 | `phase54_final_acceptance_v1/release/candidates/L1/template/` | 86 | `e31d5ab54cf74b94b1cc5f0ad02fb561b0283ff6993ed5ce26473221858fecfa` |
| K0 | `phase54_final_acceptance_v1/release/candidates/K0/template/` | 63 | `9764b0729c3f1fa5550ddaa011aa4cad3f9444008fe0451505641c7b9932600c` |
| K1 | `phase54_final_acceptance_v1/release/candidates/K1/template/` | 87 | `ef793e9cedbc231c64208b2e8380574afe744b90554fe37a53509c13b71ce76b` |

Total 448 files, read-only. Never run inside `release/`: create a copy with `release/make_working_copy.py`, and confirm `release/verify_release.py` passes before and after a batch.

## 2. Other immutable inputs

| File | Role | SHA-256 |
|---|---|---|
| `phase54_final_acceptance_v1/release/CANDIDATE_FREEZE_MANIFEST.json` | Authoritative list of the 448 frozen files | `4058f10d670ae1c2f2c02df5e5ab8dba06217d7e0181c02abb0c6a85a1c6537f` |
| `phase54_final_acceptance_v1/release/CANDIDATE_FREEZE_MANIFEST.json.sha256` | Manifest hash sidecar | `cc2c1155c9e460aa1172cc2d2238a80d24f8d6649885baba8ef6d69391708c15` |
| `phase54_final_acceptance_v1/release/RELEASE_PROVENANCE.md` | Source and decisions of the release | `8c9a5ed514d4b73c1973b4017b16d2a94f436423cac9e13373e05fad145128ef` |
| `phase54_final_acceptance_v1/release/verify_release.py` | Read-only release verifier | `6fd875440aced485287bf18504084866980c16987e4d8e46163d279d1818d643` |
| `phase54_final_acceptance_v1/release/make_working_copy.py` | Creates a verified writable copy | `56badb894ee625293e3803d7cd456ccf28779cc0a9179f0f559213043f067b41` |
| `phase54_final_acceptance_v1/FINAL_PHASE54_CLOSURE_REPORT.md` | Original closure, CLOSED_CONDITIONAL, on CLI 2.1.293 | `12055bbef0dafa992986daf9f3430934dd34ec9a7971414e527e093e8194f5a0` |
| `phase54_final_acceptance_v1/BENCHMARK_HANDOFF_CONTRACT.md` | Original handoff contract and gates | `bed852d7e2ca93762d8982d60416a3ce938dd38a3f828c9eef246247a173b6d7` |
| `phase54_final_acceptance_v1/ARCHITECTURE_DIFFERENCES_AND_LIMITS.md` | Differences to measure | `c785e4a9d49a9ec895bee8aef06eb23b029698e3de461a71bca0a7764c3482bd` |
| `phase54_final_acceptance_v1/PHASE54_METRIC_LINEAGE.md` | Metric lineage | `876cd4bc24b1344a93682e94391bb9928868b0626af56aacae8f11be4e516177` |
| `phase54_final_acceptance_v1/LIVE_HOST_PILOT_MATRIX.jsonl` | CLI 2.1.293 pilot rows | `36f5cbae3662eac7b0328dea91e33b4b8c8cf74303fa4a3b9606db692d11b696` |
| `phase54_final_acceptance_v1/LIVE_HOST_PILOT_REPORT.md` | CLI 2.1.293 pilot report and manual procedure | `142472641dd141b02cc2f53fba2d1accaea3592e2d91309b02ea2dfae3bfd5e4` |
| `phase54_cli317_host_recheck_v1/CLI317_RECHECK_REPORT.md` | CLI 2.1.317 recheck report | `cfdfc9b016a8b27e4d8f127cf4221e746d1176f743a839036bdf96938d82f118` |
| `phase54_cli317_host_recheck_v1/PHASE54_CLOSURE_ADDENDUM.md` | First closure addendum | `ff145b78e93edde35a985610f6bfdb718d3f0fa7d02588d55eb4439fd436ebe0` |
| `phase54_cli317_host_recheck_v1/CLI_VERSION_AND_HASH.md` | Executable identity | `34db5a3d51b0908504ce9ec430bac553be997afb7e1dabf454ced76f1a826177` |
| `phase54_cli317_host_recheck_v1/CLI317_RECHECK_MATRIX.jsonl` | CLI 2.1.317 rows | `491bd5115dd2fb6d8dc99d6d49ca98aadf30e41cb0e0004f1e8db660992e55f1` |
| `benchmark_readiness_fair02_cp01_v1/FAIR01_APPROVED_DISPOSITION.md` | FAIR-01 decision and measures | `e46820de9b7d0120292856ea698bc1b14027ae840c6b6dde9020e778230641ff` |
| `benchmark_readiness_fair02_cp01_v1/FINAL_BENCHMARK_READINESS_DECISIONS.md` | FAIR-01, FAIR-02 and CP-01 states | `9cf3a4584862e2b6ad21257cfbad7c8df5c50bb29b56b56af3ea48b55ee79407` |
| `benchmark_readiness_fair02_cp01_v1/CP01_IDE0005_REPRODUCTION_REPORT.md` | CP-01 experiment | `d2bd9b50191e1eff6f37d2daa86c467f39eb8d3e81a350bfa875f4e5ae62d7ee` |
| `benchmark_readiness_fair02_cp01_v1/fair02/RUN_REPORT_INSTRUCTION.txt` | FAIR-02 instruction, appended identically to each task prompt | `bb17a883e947b6d259afa683d26a5cbd23343e6a02e26bf93fd239918ffe6710` |
| `benchmark_readiness_fair02_cp01_v1/fair02/BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md` | FAIR-02 protocol addendum | `fbdf196a411476afe87aaa139fcaa2b7b0e742db60b4531158cda8728a2ec869` |
| `benchmark_readiness_fair02_cp01_v1/fair02/INTEGRATION_CONTRACT.md` | Runner dependencies R1-R9 | `cc769d983405fab8d7b350ea0327f4088759451c0c211c14700bccdc9df083c7` |
| `benchmark_readiness_fair02_cp01_v1/fair02/REPORT_COMPLETENESS_RUBRIC.md` | Secondary score rubric | `62fcbc66679fa3496dbde97227d8cbd96164ad05140ef9d49717cbf2fe932dfb` |
| `benchmark_readiness_fair02_cp01_v1/fair02/RUN_EVIDENCE_SCHEMA.md` | Per-run evidence schema | `dcb026859c2258bbfa1f270ded9dd54f7427f4cdb1f3a8772c5627c49689aaf9` |
| `benchmark_readiness_fair02_cp01_v1/fair02/assemble_prompt.py` | Prompt assembly tool | `dd58e49e94777c56e2ba2ff78a71cdcc6f4f025271a1f030dc5b791a9175ffd5` |
| `benchmark_readiness_fair02_cp01_v1/fair02/score_report.py` | Report scorer | `29a845d53472d161b71b2bb79340e045935118641de5a1431f0876b62edb828c` |
| `step3_six_way_strictness_v1/FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md` | Six-way strictness analysis | `d116189a33a75096cd81057d7ea47d0b294080af9fd25f878d0b15298157a7ea` |
| `step3_six_way_strictness_v1/METRICS.json` | Step 3 metrics | `504cef889a67ccc4a75fdd9b79f274563afbbaf2fd9a4f4932ac11ac7c1a2655` |
| `step3_six_way_strictness_v1/POLICY_SIX_WAY_MATRIX.jsonl` | Step 3 policy matrix | `74b8bfedb0dbd71ca4ec587c5fc070f149dcfbcc985c17ada3af015f91c16796` |
| `step3_six_way_strictness_v1/OPEN_DECISIONS_AND_SENSITIVITY.md` | Step 3 open decisions | `17bdb59ec3148f499479537a293ad01442269d088fd067b4f7f35f86c48f0132` |

## 3. Approved decisions (not to be redesigned)

| Decision | Content | Consequence |
|---|---|---|
| FAIR-01 | Approved as preserve: all hooks, checkers, loading and enforcement differences stay exactly as in v3 | Measure the differences; do not harmonize them without a separate explicit decision |
| FAIR-02 | One reporting instruction, SHA-256 `bb17a883e947b6d259afa683d26a5cbd23343e6a02e26bf93fd239918ffe6710`, appended identically to each task prompt with a secondary Report Completeness Score | Keep it external. It must never be added to a template |
| CP-01 | Option 0: M keeps IDE0005 through `dotnet format`; no `GenerateDocumentationFile` | M stays unchanged |

## 4. Critical environmental assumptions

| Assumption | Evidence | Consequence if it changes |
|---|---|---|
| Claude Code CLI 2.1.317, SHA-256 `26b01ec22df2c17ac7f5703aa547d36706e8d58412136ced0344a8ced4d86038` | 51 headless sessions; static hash at closure | Fail-closed `onFailure: "block"` is a property of the host version: 2.1.293 ignored it. Re-check on any version change |
| Identify the binary by hash, not path | It moved to `%LOCALAPPDATA%\Claude-Data\claude_pzs8sxrjxfjjc\claude-code\2.1.317\a33aa5518497\claude.exe`; both older paths are gone | Pinned paths from the recheck no longer resolve |
| Claude Desktop 4.23118.0.0, for Desktop runs | Package, manifest and process records | Desktop Auto results are bound to this version |
| `node` on PATH | Recheck D1 | With `node` missing, every Bash call is refused on 2.1.317: the run is unusable rather than unguarded. Keep a preflight |
| Windows 11 Pro 10.0.26200 | Environment probe | No other OS was tested |
| Blocks are read from the tool result | Hook events report `exit 1, outcome error` whether or not the host blocks | Do not infer a block from the hook event alone |
| `onFailure: "block"` only where declared | SYN-DX2: exit 1 without it still runs | In the candidates only PreToolUse declares it |
| Headless `--permission-prompts none` denies every `ask` immediately | S-C rows, SYN-ASKNONE | Steps needing `ask` approval cannot complete headless (all six: Git commits; L1: reference commands) |
| Output redirection needs host approval even with an exact allow rule | Attempt-1 harness defect | Use `touch` for markers |
| In Desktop Auto, a K0 hook `ask` reaches a person as a card | v1 operator statement and v2 screenshot; the hook's reason on the card is shown by the v2 screenshot only | Seen for K0 only |
| Hook records for denied attempts may be absent from the transcript | v1 attempt 1 and v2 | Do not rely on the transcript alone to attribute a denied request |
| Shell `cd` persists between tool calls | INC-01 | Use absolute paths near frozen folders |

## 5. Carried gates

| Gate | State at handoff |
|---|---|
| G1 hook health | Reduced: HOST-01 resolved on 2.1.317; `node` preflight and tool-result reading remain |
| G2 run mode | **Open user decision**, headless or interactive |
| G3 host pin | Pin CLI 2.1.317 |
| G4 runner R1-R8 | **Open**: no runner exists |
| G5 host pilot | Done headless on 2.1.317. Desktop Auto done for K0 only |
| G6 FAIR-02 addendum | Ready to adopt |
| G7 open items Q-01, Q-02, Q-03, Q-12, RD-01, RD-02, optional independent review | Open, non-blocking |
| G8 hook durations (M1 none, L1 15 s) | To be logged in real runs |

## 6. Explicitly deferred

- Interactive runs of M, M1, L0, L1 and K1. Needed only if interactive mode is chosen, and K0's result does not stand in for them.
- Interactive terminal sessions with a person answering `ask` (six `IA` rows, NOT_RUN).
- F1 reference gate on 2.1.317 (passed on 2.1.293 only).
- D2 malformed hook input live (static only), and M1 timeout.
- Benchmark protocol, task prompts, runner, approval policy and any measured run.
- Any candidate change, including the optional CP-01 comment clarification.

No ranking of the six candidates follows from Stage A. Static parity and hook smoke tests do not show how the architectures perform on real tasks.
