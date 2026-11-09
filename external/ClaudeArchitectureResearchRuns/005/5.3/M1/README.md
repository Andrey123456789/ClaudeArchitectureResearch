# Iteration 005 / 5.3 / M1 controlled refinement

This workspace refines one selected raw M1 implementation from iteration 5.2.

- **Selected baseline:** M1 / Run-02.
- **Run-01 is evidence only.** Its generated template is intentionally not copied into this workspace, to avoid accidental file-by-file merging.
- `baseline/` is immutable evidence.
- `source/` is the frozen source corpus.
- `audit/` contains the independent comparison, defect dossier, Run-03 decision, and external Claude Code hook-mechanics notes.
- `output/` starts empty. The refinement agent must copy `baseline/template/` to `output/template/` and edit only the output copy.

Run a fresh Claude Desktop Code session with this `M1` directory as the workspace root and invoke `/goal` with the complete contents of `GOAL_PROMPT.txt`.

A refined template is promoted only if `REFINEMENT_REPORT.md` proves it is **STRICTLY_BETTER** than the immutable baseline. A tie or regression is not a promotion.
