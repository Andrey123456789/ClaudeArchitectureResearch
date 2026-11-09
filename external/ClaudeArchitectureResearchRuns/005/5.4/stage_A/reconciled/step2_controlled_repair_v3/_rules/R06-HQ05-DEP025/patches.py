"""R06 HQ-05 / DEP-025: confirmation, comment markers and approvals cannot open a peer-dependency bypass. Enforcement and text change together in each candidate."""
REASON = 'HQ-05: an ordinary ask confirmation or shell-comment marker must not override peer compatibility policy or permit --force / --legacy-peer-deps; resolve the actual conflict; safe installs preserved'
POLICIES = ['DEP-025', 'DEP-003', 'DEP-019']

NO_ROUTE = 'No confirmation, comment marker, or approval opens this route.'
ENV_RX = r"/\bnpm_config_(force|legacy_peer_deps)\s*=\s*['\"]?(true|1)\b/i"

PATCHES = [
    # ---------- M: enforcement already denies; text states it
    ('M', '.claude/hooks/dependency-guard.mjs', """  while (start < tokens.length && (tokens[start] === '&' || /^[A-Za-z_][A-Za-z0-9_]*=/.test(tokens[start]))) start += 1;
""", """  while (start < tokens.length && (tokens[start] === '&' || tokens[start] === 'env' || tokens[start] === 'cross-env' || /^[A-Za-z_][A-Za-z0-9_]*=/.test(tokens[start]))) start += 1;
"""),
    ('M', '.claude/skills/add-dependency/SKILL.md', """   peer dependencies; resolve the actual compatibility problem instead. The
   dependency hook blocks these flags.
""", """   peer dependencies; resolve the actual compatibility problem instead. The
   dependency hook blocks these flags. No confirmation, comment marker, or
   approval opens this route.
"""),
    # ---------- M1
    ('M1', '.claude/scripts/lib/dependency-commands.js', "const PEER_OVERRIDE = /#\\s*peer-override:\\s*approved-by-user\\b/i;\n", ''),
    ('M1', '.claude/scripts/lib/dependency-commands.js', "function analyzeCommand(command, shell) {\n  const ops = classifyCommand(command, shell);\n",
     "function analyzeCommand(command, shell) {\n  const ops = classifyCommand(command, shell);\n  const peerConfig = segmentsOf(command, shell).find((s) => /^(\\S*[\\\\/])?npm(\\.cmd)?\\s.*\\bconfig\\s+set\\s+(legacy-peer-deps|force)(=true|\\s+true)\\b/i.test(s.tokens.join(' ')));\n  if (peerConfig || (" + ENV_RX + ".test(String(command)) && /\\bnpm(\\.cmd)?\\s/i.test(String(command)))) {\n    return {\n      block: true,\n      message: 'npm peer-dependency bypass configured for this command.\\n'\n        + `Resolve the actual compatibility problem instead (${DEPENDENCY_WORKFLOW}, Install). " + NO_ROUTE + "\\n`,\n    };\n  }\n"),
    ('M1', '.claude/scripts/lib/dependency-commands.js', "    if (flag && !PEER_OVERRIDE.test(op.comment)) {\n", "    if (flag) {\n"),
    ('M1', '.claude/scripts/lib/dependency-commands.js', "          'Only when the user explicitly approved the override, re-run the same command with the trailing comment: # peer-override: approved-by-user\\n',\n", "          '" + NO_ROUTE + "\\n',\n"),
    ('M1', '.claude/hooks/pre-tool-use.js', "// been applied, and npm peer-dependency override flags without approval. Only the\n", "// been applied, and npm peer-dependency override flags in every case. Only the\n"),
    ('M1', '.claude/skills/add-dependency/SKILL.md', """`# add-dependency: checked`. A peer-dependency override additionally needs the
user's explicit approval and the trailing comment
`# peer-override: approved-by-user`.
""", """`# add-dependency: checked`. That comment never applies to `--force` or
`--legacy-peer-deps`: the hook denies them. No confirmation, comment marker, or
approval opens this route.
"""),
    # ---------- L0
    ('L0', '.claude/hooks/claude-hook.mjs', "  const role = sub === undefined ? (manager === 'yarn' ? 'restore' : null) : Object.hasOwn(roles, sub) ? roles[sub] : null;\n  if (!role) return null;\n",
     "  const role = sub === undefined ? (manager === 'yarn' ? 'restore' : null) : Object.hasOwn(roles, sub) ? roles[sub] : null;\n  if (manager === 'npm' && sub === 'config' && rest[0] === 'set' && /^(legacy-peer-deps|force)(=true)?$/.test(rest[1] ?? '') && ((rest[1] ?? '').includes('=') || rest[2] === 'true')) return { kind: null, bypass: true };\n  if (!role) return null;\n"),
    ('L0', '.claude/hooks/claude-hook.mjs', "    lines.push(`Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. If the user explicitly decides to override, the user runs the command.`);\n  }\n",
     "    lines.push(`Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. " + NO_ROUTE + "`);\n  }\n  if (found.every(entry => !entry.bypass) && " + ENV_RX + ".test(command) && /\\bnpm(\\.cmd)?\\s/i.test(command)) {\n    lines.push('Blocked: the command sets an npm_config_* peer-dependency bypass.');\n    lines.push(`Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. " + NO_ROUTE + "`);\n  }\n"),
    ('L0', '.claude/skills/add-dependency/SKILL.md', "resolve the actual compatibility problem (the project hook blocks these flags; if the user explicitly decides to override, the user runs the command).",
     "resolve the actual compatibility problem (the project hook blocks these flags). " + NO_ROUTE),
    # ---------- L1
    ('L1', '.claude/hooks/pre-shell-command.mjs', "// - peer-dependency bypass flags (--force, -f, --legacy-peer-deps) → ask the user (add-dependency);\n", "// - peer-dependency bypass flags (--force, -f, --legacy-peer-deps) and npm_config_* equivalents → denied (add-dependency);\n"),
    ('L1', '.claude/hooks/pre-shell-command.mjs', """  if (verdict.force) {
    decide('ask', 'Peer-dependency bypass flag (--force / -f / --legacy-peer-deps) detected. The add-dependency workflow requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.');
  }
""", """  if (verdict.force || (""" + ENV_RX + """.test(command) && /\\bnpm(\\.cmd)?\\s/i.test(command))) {
    decide('deny', 'Peer-dependency bypass (--force / -f / --legacy-peer-deps or an npm_config_* equivalent) detected. The add-dependency workflow requires resolving the actual compatibility problem. """ + NO_ROUTE + """');
  }
"""),
    ('L1', '.claude/INSTRUCTION_MAP.md', "peer-dependency bypass flags → ask. Deny-once state", "peer-dependency bypass flags → denied, with no approval route. Deny-once state"),
    ('L1', '.claude/skills/add-dependency/SKILL.md', "- npm: never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies — resolve the actual compatibility problem.\n",
     "- npm: never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies — resolve the actual compatibility problem. The hook denies these flags. " + NO_ROUTE + "\n"),
    # ---------- K0
    ('K0', '.claude/hooks/hook.cjs', """  const force = args.some((a) => FORCE_FLAG.test(a) || spec.force.includes(a));
  const positionals = positionalsOf(args, valueOptions);
  let [sub, ...rest] = positionals;
""", """  const force = args.some((a) => FORCE_FLAG.test(a) || spec.force.includes(a));
  const positionals = positionalsOf(args, valueOptions);
  let [sub, ...rest] = positionals;
  if (tool === 'npm' && String(sub).toLowerCase() === 'config' && rest[0] === 'set' && /^(legacy-peer-deps|force)(=true)?$/i.test(rest[1] ?? '') && ((rest[1] ?? '').includes('=') || rest[2] === 'true')) return { force: true };
"""),
    ('K0', '.claude/hooks/hook.cjs', """  if (found.dependency.length > 0 && !DEPENDENCY_MARKER.test(command)) {
""", """  if (found.dependency.some((d) => d.force) || (""" + ENV_RX + """.test(command) && /\\bnpm(\\.cmd)?\\s/i.test(command))) {
    deny.push('The command uses --force, --legacy-peer-deps or an npm_config_* equivalent: resolve the actual peer-dependency conflict instead (`add-dependency` § 5). """ + NO_ROUTE + """');
  }
  if (found.dependency.length > 0 && !DEPENDENCY_MARKER.test(command)) {
"""),
    ('K0', '.claude/hooks/hook.cjs', """    if (found.dependency.some((d) => d.force)) deny.push('The command uses --force or --legacy-peer-deps: resolve the actual peer-dependency conflict instead (`add-dependency` § 5).');
""", ''),
    ('K0', '.claude/skills/add-dependency/SKILL.md', """Never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem.
- The pre-command hook stops package-changing commands — additions, updates and removals, with or without global options such as `--prefix`, and any `--force` or `--legacy-peer-deps` install — until this workflow has run. After steps 1–4, run the command with the trailing marker comment `# add-dependency: reviewed`, for example:""",
     """Never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem.
- The pre-command hook denies any `--force` or `--legacy-peer-deps` install. """ + NO_ROUTE + """
- The pre-command hook stops other package-changing commands — additions, updates and removals, with or without global options such as `--prefix` — until this workflow has run. After steps 1–4, run the command with the trailing marker comment `# add-dependency: reviewed`, for example:"""),
    ('K0', '.claude/MAP.md', "npm/pnpm/yarn/ng/dotnet/NuGet package additions, updates and removals (global options and `--force`/`--legacy-peer-deps` included) are denied without `# add-dependency: reviewed`;",
     "`--force`/`--legacy-peer-deps` installs are always denied; other npm/pnpm/yarn/ng/dotnet/NuGet package additions, updates and removals (global options included) are denied without `# add-dependency: reviewed`;"),
    # ---------- K1
    ('K1', '.claude/scripts/classify-command.cjs', """  if (!category) return [];
  const findings = [];
  if (options.some(o => PEER_BYPASS.test(o))) findings.push({ kind: 'peer-bypass', segment });
""", """  if (exe === 'npm' && verb === 'config' && positional[0] === 'set' && /^(legacy-peer-deps|force)(=true)?$/i.test(positional[1] || '') && ((positional[1] || '').includes('=') || positional[2] === 'true')) return [{ kind: 'peer-bypass', segment }];
  if (!category) return [];
  const findings = [];
  if (options.some(o => PEER_BYPASS.test(o))) findings.push({ kind: 'peer-bypass', segment });
"""),
    ('K1', '.claude/scripts/classify-command.cjs', """function classify(command, options = {}) {
  const findings = [];
""", """function classify(command, options = {}) {
  const findings = [];
  if (""" + ENV_RX + """.test(String(command)) && /\\bnpm(\\.cmd)?\\s/i.test(String(command))) findings.push({ kind: 'peer-bypass', segment: String(command).trim() });
"""),
    ('K1', '.claude/hooks/dispatch.cjs', "--force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts)`;",
     "--force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts). " + NO_ROUTE + "`;"),
    ('K1', '.claude/skills/add-dependency/SKILL.md', "never use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies.\n",
     "never use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies. " + NO_ROUTE + "\n"),
]
