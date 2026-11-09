"""Evidence dispositions for C01. Each range was read in claimview.py with the records citing it. A later row supersedes a v1 row for the same range."""


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


CM = '.claude/scripts/check-manifests.mjs'
EVAL = 'effective ManagePackageVersionsCentrally is'
DISPOSITIONS = [
    d('M', '.claude/MAP.md', 114, 114, '`Directory.Build.props`, `Directory.Build.targets`, `package.json`', 'Hook row names the chain files.'),
    d('M', '.claude/hooks/file-change.mjs', 4, 6, 'Directory.Build.props, Directory.Build.targets,', 'Header names the chain files.'),
    d('M', '.claude/hooks/file-change.mjs', 46, 55, "name === 'Directory.Build.targets' || name === 'package.json';", 'Chain files reach the check; the rest of the block is unchanged.'),
    d('M', '.claude/rules/dependencies.md', 26, 30, 'effective `ManagePackageVersionsCentrally` must be true for each project', 'Owner text gains the effective reading; versionless and narrow-scope duties unchanged.'),
    d('M', CM, 203, 211, 'function checkCentralProps(root, file, result, checkedProps)', 'Literal test removed; version and id checks kept.'),
    d('M', CM, 209, 211, EVAL, 'Literal test replaced by the evaluated value.'),
    d('M', CM, 252, 261, 'function checkProject(root, file, result, checkedProps)', 'Literal opt-out test removed; evaluated value covers it.'),
    d('M', CM, 257, 278, 'version declared in the project file', 'Literal opt-out test removed; static version lint kept.'),
    d('M', CM, 257, 285, 'version declared in the project file', 'Literal opt-out test removed; static version lint kept.'),
    d('M1', '.claude/scripts/check-manifests.js', 115, 119, 'function checkPackagesProps(file, data, findings)', 'Literal test removed.'),
    d('M1', '.claude/scripts/check-manifests.js', 117, 119, EVAL, 'Literal test replaced by the evaluated value.'),
    d('M1', '.claude/skills/verify/SKILL.md', 103, 109, 'and the vulnerability commands of `add-dependency` § Verify.', 'NOT_RUN sentence added; the rest unchanged.'),
    d('L0', '.claude/hooks/claude-hook.mjs', 463, 466, 'const reported = new Set();', 'Shares the per-run report set; validation unchanged.'),
    d('L0', '.claude/hooks/manifest-checks.mjs', 252, 259, EVAL, 'Literal reader removed; the evaluated value replaces it.'),
    d('L0', '.claude/hooks/manifest-checks.mjs', 306, 308, EVAL, 'Literal test replaced by the evaluated value.'),
    d('L0', '.claude/skills/verify/SKILL.md', 50, 50, 'manifest-checks.mjs', 'Names the whole-repository command and the NOT_RUN reading.'),
    d('L1', '.claude/hooks/post-change-checks.mjs', 24, 26, 'Directory\\.Build\\.targets', 'Chain files are manifests now.'),
    d('L1', '.claude/hooks/post-change-checks.mjs', 68, 78, 'function checkPackagesProps(rel, text, rules, findings, exceptions)', 'Literal test removed; version and exception checks kept. Supersedes the R04 quote.'),
    d('L1', '.claude/hooks/post-change-checks.mjs', 70, 70, EVAL, 'Literal test replaced by the evaluated value.'),
    d('L1', '.claude/scripts/lib/project.mjs', 238, 263, 'return { versions };', 'Parser no longer reports a literal central flag.'),
    d('L1', '.claude/skills/verify/SKILL.md', 49, 49, 'post-change-checks.mjs', 'Names the whole-repository command and the NOT_RUN reading.'),
    d('K0', '.claude/hooks/hook.cjs', 372, 380, "'*Directory.Build.props', '*Directory.Build.targets'", 'Chain files are in the observed list.'),
    d('K0', '.claude/rules/common/dependencies.md', 22, 22, 'the effective `ManagePackageVersionsCentrally` must be true for each project', 'Owner text sharpened. Supersedes the R08 quote.'),
    d('K0', '.claude/scripts/check-dependencies.cjs', 166, 170, 'function effectiveCpm(root, project)', 'Evaluated by MSBuild. Supersedes the R08 quote.'),
    d('K0', '.claude/scripts/check-dependencies.cjs', 167, 170, 'function effectiveCpm(root, project)', 'Evaluated by MSBuild. Supersedes the R08 quote.'),
    d('K0', '.claude/scripts/check-dependencies.cjs', 244, 249, 'const total = { errors: [], notices: [], notRun: [], files: [] };', 'Carries NOT_RUN; root-manifest check kept.'),
    d('K0', '.claude/skills/verify/SKILL.md', 56, 56, 'then review against `rules/backend/architecture.md`.', 'NOT_RUN sentence added; the rest unchanged.'),
    d('K0', '.claude/skills/verify/SKILL.md', 56, 58, 'then review against `rules/backend/architecture.md`.', 'NOT_RUN sentence added; the rest unchanged.'),
    d('K1', '.claude/scripts/actual-state.cjs', 18, 39, ":(glob)**/Directory.Build.targets", 'Chain files are in the observed list.'),
    d('K1', '.claude/scripts/check-manifests.cjs', 99, 104, EVAL, 'Literal test replaced by the evaluated value. Supersedes the R04 quote.'),
    d('K1', '.claude/scripts/check-manifests.cjs', 102, 104, EVAL, 'Literal test replaced by the evaluated value.'),
    d('K1', '.claude/scripts/check-manifests.cjs', 158, 185, 'return rel.endsWith(\'.csproj\') || CPM_CHAIN_FILES.has(base) || base === \'package.json\';', 'Chain files are manifests now.'),
    d('K1', '.claude/scripts/check-manifests.cjs', 163, 172, "manifest could not be read", 'Read-failure reporting unchanged; chain files added.'),
    d('K1', '.claude/scripts/check-manifests.cjs', 243, 255, 'process.exitCode = errors ? 1 : notRun ? 3 : 0;', 'Exit code 3 added for NOT_RUN; argument handling unchanged.'),
    d('K1', '.claude/skills/verify/SKILL.md', 52, 52, 'then run `node "<root>/.claude/scripts/check-manifests.cjs"`.', 'NOT_RUN sentence added; the rest unchanged.'),
]
