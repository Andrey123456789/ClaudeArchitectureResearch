---
name: code-reviewer
description: >
  Independent read-only reviewer for completed backend and frontend changes.
  Use for PR reviews, reviewing a diff, pre-merge review, or an independent
  second-pass review of completed work.
disallowedTools: Write, Edit, NotebookEdit
skills:
  - code-review
---

> Kind: WF | Scope: common | Capability: — | Loading: subagent (delegates to the `code-review` workflow)

# Code Reviewer

Run the `code-review` workflow on the requested scope and return its report. Do not edit files and do not redefine review criteria here; the workflow and the repository standards it loads are authoritative.
