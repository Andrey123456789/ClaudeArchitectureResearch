# External mechanics note — Claude Code hooks

These mechanics were independently checked against the current official Claude Code Hooks documentation before preparing this refinement package.

Reference: https://code.claude.com/docs/en/hooks

Relevant constraints encoded into the defect dossier and task:

- command hooks support an exec form with an executable plus `args`, avoiding a shell;
- project path placeholders such as `${CLAUDE_PROJECT_DIR}` are substituted by Claude Code and can be passed as plain arguments;
- hook input includes `cwd` for the current working directory;
- the stable project-directory location used to locate installed project hooks is not a safe substitute for the active repository/worktree root when the session operates in a worktree or changes directory.

The refinement run itself should not browse the network. Treat these mechanics as supplied research evidence.
