# suite_post.jsonl restored (2026-11-06)

During PV2-03B, `suite_run.py PV2-03-K0-CPM-ROOT post` was run as an extra check of this suite on PV2-03B bytes. It overwrote this folder's
`suite_post.jsonl`, the post-change run recorded for PV2-03 on 2026-11-05. No gate tool reads that file.

- The accidental re-run (PV2-03B state, 85 PASS, 1 NOT_RUN) is kept as `suite_rerun_at_PV2-03B.jsonl`.
- `suite_post.jsonl` was rebuilt from the PV2-03 gate's own results (`TEST_RESULTS/PV2-03-K0-CPM-ROOT.jsonl`, rows of suite
  PV2-03-K0-CPM-ROOT, in order). That is the same suite on the same bytes at the PV2-03 checkpoint, run by the gate rather than
  by `suite_run.py` just before it. Fixture paths in details may differ from the lost file; outcomes are the gate's.
