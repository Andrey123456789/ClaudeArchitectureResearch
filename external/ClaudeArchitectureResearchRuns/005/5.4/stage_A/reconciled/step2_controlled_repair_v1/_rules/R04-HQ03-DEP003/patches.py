"""R04 HQ-03 / DEP-003: one exception semantics across instruction text, manifest checkers and K1's version gate."""
REASON = 'HQ-03: floating and prerelease forbidden by default; an explicit bounded user request authorizes exactly the recorded package, version and manifest; no global switch; compatibility and resolved version confirmed'
POLICIES = ['DEP-003', 'DEP-006', 'DEP-001', 'DEP-014']

TEXT = """**Explicit exception.** A floating or prerelease version is allowed only on an explicit, bounded user request that names the package and the version or range; a general wish such as "keep it current" is not one. Record it as one entry in the file dependency-version-exceptions.json at the repository root (created on first use) with `ecosystem` (`npm` or `nuget`), `package`, `version`, `manifest` (repository-relative path), `requested_by` (`user`), `request` (the request text), and `date`. The manifest checks accept exactly that entry and keep rejecting every other floating or prerelease version; there is no global switch. Confirm compatibility with the target framework and peer dependencies, and report the exact version the install resolved. The entry covers the version only, not any other dependency rule."""


def wrap(s, width=80):
    words, lines, cur = s.split(), [], ''
    for w in words:
        if len(cur) + len(w) + (0 if not cur else 1) > width:
            lines.append(cur)
            cur = w
        else:
            cur = cur + ('' if not cur else ' ') + w
    lines.append(cur)
    return '\n'.join(lines)


VALID = """  if (typeof e !== 'object' || e === null) return false;
  if (e.ecosystem !== 'npm' && e.ecosystem !== 'nuget') return false;
  if (typeof e.package !== 'string' || !e.package.trim() || /[*?]/.test(e.package)) return false;
  if (typeof e.version !== 'string' || !e.version.trim()) return false;
  if (typeof e.manifest !== 'string' || !e.manifest.trim()) return false;
  if (e.requested_by !== 'user') return false;
  return typeof e.request === 'string' && e.request.trim() !== '';
"""
COMMENT = """// DEP-003 exception: a floating or prerelease version is accepted only when
// dependency-version-exceptions.json records the user's explicit request for
// exactly this ecosystem, package, version, and manifest. There is no global switch.
"""
MATCH = """  const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
  return %s.some((e) => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted
    && e.version.trim() === String(version).trim() && e.manifest.replace(/\\\\/g, '/') === String(rel).replace(/\\\\/g, '/'));
"""

PATCHES = []
# ---------------------------------------------------- M
PATCHES += [
    ('M', '.claude/scripts/check-manifests.mjs', "  const result = { violations: [], notes: [], checked: [] };\n",
     "  const result = { violations: [], notes: [], checked: [], versionExceptions: [] };\n  loadVersionExceptions(root, result);\n"),
    ('M', '.claude/scripts/check-manifests.mjs', "function checkNuGetVersion(id, version, rel, result) {\n",
     COMMENT + "function validVersionException(e) {\n" + VALID + "}\n\nfunction loadVersionExceptions(root, result) {\n  const file = join(root, 'dependency-version-exceptions.json');\n  if (!existsSync(file)) return;\n  try {\n    const entries = JSON.parse(readFileSync(file, 'utf8')).exceptions;\n    if (!Array.isArray(entries)) throw new Error('\"exceptions\" is not a list');\n    for (const e of entries) {\n      if (validVersionException(e)) result.versionExceptions.push(e);\n      else result.violations.push({ file: 'dependency-version-exceptions.json', message: 'exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by \"user\", and the request text (add-dependency)' });\n    }\n  } catch (error) {\n    result.violations.push({ file: 'dependency-version-exceptions.json', message: `unreadable exception record (${error.message}); no exception applies (add-dependency)` });\n  }\n}\n\nfunction approvedVersionException(result, ecosystem, id, version, rel) {\n" + (MATCH % 'result.versionExceptions') + "}\n\nfunction checkNuGetVersion(id, version, rel, result) {\n"),
    ('M', '.claude/scripts/check-manifests.mjs', """  if (v.includes('*') || /^[[(]/.test(v) || v.includes(',')) {
    result.violations.push({ file: rel, message: `${id}: floating or range version "${v}" - pin the latest stable compatible version (add-dependency)` });
  } else if (/^\\d+(\\.\\d+)*-/.test(v)) {
    result.notes.push""", """  if (approvedVersionException(result, 'nuget', id, v, rel)) {
    result.notes.push({ file: rel, message: `${id}: version "${v}" - approved exception recorded in dependency-version-exceptions.json` });
  } else if (v.includes('*') || /^[[(]/.test(v) || v.includes(',')) {
    result.violations.push({ file: rel, message: `${id}: floating or range version "${v}" - pin the latest stable compatible version (add-dependency)` });
  } else if (/^\\d+(\\.\\d+)*-/.test(v)) {
    result.notes.push"""),
    ('M', '.claude/scripts/check-manifests.mjs', """      if (['', '*', 'x', 'X', 'latest', 'next'].includes(spec) ||""", """      if (approvedVersionException(result, 'npm', name, spec, rel)) {
        result.notes.push({ file: rel, message: `${section}.${name}: version "${spec}" - approved exception recorded in dependency-version-exceptions.json` });
      } else if (['', '*', 'x', 'X', 'latest', 'next'].includes(spec) ||"""),
    ('M', '.claude/skills/add-dependency/SKILL.md', """   versions, and do not use floating versions such as `*`, unless explicitly
   requested.

"Latest" means""", """   versions, and do not use floating versions such as `*`, unless explicitly
   requested.

""" + wrap(TEXT) + """

"Latest" means"""),
]
# ---------------------------------------------------- M1
PATCHES += [
    ('M1', '.claude/scripts/check-manifests.js', "  const findings = [];\n  for (const rel of targets) {\n", "  const findings = [];\n  data.versionExceptions = [];\n  loadVersionExceptions(data, findings);\n  for (const rel of targets) {\n"),
    ('M1', '.claude/scripts/check-manifests.js', "function checkPackagesProps(file, data, findings) {\n",
     COMMENT + "function validVersionException(e) {\n" + VALID + "}\n\nfunction loadVersionExceptions(data, findings) {\n  const file = 'dependency-version-exceptions.json';\n  if (!common.exists(file)) return;\n  try {\n    const entries = JSON.parse(common.readText(file)).exceptions;\n    if (!Array.isArray(entries)) throw new Error('\"exceptions\" is not a list');\n    for (const e of entries) {\n      if (validVersionException(e)) data.versionExceptions.push(e);\n      else findings.push(finding('ERROR', file, `exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by \"user\", and the request text (${OWNER_WORKFLOW}).`));\n    }\n  } catch (e) {\n    findings.push(finding('ERROR', file, `unreadable exception record (${e.message}); no exception applies (${OWNER_WORKFLOW}).`));\n  }\n}\n\nfunction approvedVersionException(data, ecosystem, id, version, rel) {\n" + (MATCH % 'data.versionExceptions') + "}\n\nfunction checkPackagesProps(file, data, findings) {\n"),
    ('M1', '.claude/scripts/check-manifests.js', """      if (version.includes('*') || version.trim() === '') {
        findings.push(finding('ERROR', file, `${id}: floating or empty version""", """      if (approvedVersionException(data, 'nuget', id, version, file)) {
        findings.push(finding('WARN', file, `${id}: version "${version}" is an approved exception recorded in dependency-version-exceptions.json.`));
      } else if (version.includes('*') || version.trim() === '') {
        findings.push(finding('ERROR', file, `${id}: floating or empty version"""),
    ('M1', '.claude/scripts/check-manifests.js', """      if (s === '' || s === '*' || s === 'latest' || /^x(\\.x)*$/i.test(s)) {""", """      if (approvedVersionException(data, 'npm', id, s, file)) {
        findings.push(finding('WARN', file, `${section}.${id}: version "${s}" is an approved exception recorded in dependency-version-exceptions.json.`));
      } else if (s === '' || s === '*' || s === 'latest' || /^x(\\.x)*$/i.test(s)) {"""),
    ('M1', '.claude/skills/add-dependency/SKILL.md', """3. do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions unless explicitly requested;
4. do not use floating versions such as `*`.

"Latest" means""", """3. do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions, and do not use floating versions such as `*`, unless explicitly
   requested.

""" + wrap(TEXT) + """

"Latest" means"""),
]
# ---------------------------------------------------- L0
PATCHES += [
    ('L0', '.claude/hooks/manifest-checks.mjs', """function checkVersion(version, location, problems) {
  if (!version || !version.trim()) problems.push(""", COMMENT + "function validVersionException(e) {\n" + VALID + "}\n\nfunction loadVersionExceptions(root, problems) {\n  const file = path.join(root, 'dependency-version-exceptions.json');\n  if (!existsSync(file)) return [];\n  const label = 'dependency-version-exceptions.json';\n  try {\n    const entries = JSON.parse(readText(file)).exceptions;\n    if (!Array.isArray(entries)) throw new Error('\"exceptions\" is not a list');\n    const valid = entries.filter(validVersionException);\n    if (valid.length !== entries.length) problems.push(`${label}: exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by \"user\", and the request text → ${OWNER.addDependency}`);\n    return valid;\n  } catch (error) {\n    problems.push(`${label}: unreadable exception record (${error.message}); no exception applies → ${OWNER.addDependency}`);\n    return [];\n  }\n}\n\nfunction approvedVersionException(exceptions, ecosystem, id, version, rel) {\n" + (MATCH % 'exceptions') + """}

function checkVersion(version, location, problems) {
  if (!version || !version.trim()) problems.push("""),
    ('L0', '.claude/hooks/manifest-checks.mjs', """function checkCentralPackages(content, location, problems, accepted) {""", """function checkCentralPackages(content, location, problems, accepted, exceptions) {"""),
    ('L0', '.claude/hooks/manifest-checks.mjs', """    checkVersion(metadata(item, 'Version'), `${location} [${id}]`, problems);
    checkPackageId(id, location, problems, accepted);""", """    const version = metadata(item, 'Version');
    if (!approvedVersionException(exceptions, 'nuget', id, version ?? '', location)) checkVersion(version, `${location} [${id}]`, problems);
    checkPackageId(id, location, problems, accepted);"""),
    ('L0', '.claude/hooks/manifest-checks.mjs', """function checkPackageJson(content, location, problems, accepted) {""", """function checkPackageJson(content, location, problems, accepted, exceptions) {"""),
    ('L0', '.claude/hooks/manifest-checks.mjs', """      if (typeof version === 'string' && /^(\\*|latest|x|)$/i.test(version.trim())) {""", """      if (typeof version === 'string' && /^(\\*|latest|x|)$/i.test(version.trim()) && !approvedVersionException(exceptions, 'npm', name, version, location)) {"""),
    ('L0', '.claude/hooks/manifest-checks.mjs', """  else if (base === 'Directory.Packages.props') checkCentralPackages(content, location, problems, accepted);
  else if (base === 'package.json') checkPackageJson(content, location, problems, accepted);""", """  else if (base === 'Directory.Packages.props') checkCentralPackages(content, location, problems, accepted, loadVersionExceptions(root, problems));
  else if (base === 'package.json') checkPackageJson(content, location, problems, accepted, loadVersionExceptions(root, problems));"""),
    ('L0', '.claude/skills/add-dependency/SKILL.md', """and do not use floating versions such as `*`, unless the user explicitly requests it.

""", """and do not use floating versions such as `*`, unless the user explicitly requests it.

""" + TEXT + """

"""),
]
# ---------------------------------------------------- L1
PATCHES += [
    ('L1', '.claude/hooks/post-change-checks.mjs', """function checkPackagesProps(rel, text, rules, findings) {""", COMMENT + "function validVersionException(e) {\n" + VALID + "}\n\nfunction loadVersionExceptions(active, findings) {\n  const file = path.join(active, 'dependency-version-exceptions.json');\n  if (!existsSync(file)) return [];\n  const label = 'dependency-version-exceptions.json';\n  try {\n    const entries = JSON.parse(readFileSync(file, 'utf8')).exceptions;\n    if (!Array.isArray(entries)) throw new Error('\"exceptions\" is not a list');\n    const valid = entries.filter(validVersionException);\n    if (valid.length !== entries.length) findings.push(`${label}: exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by \"user\", and the request text (owner: add-dependency).`);\n    return valid;\n  } catch (error) {\n    findings.push(`${label}: unreadable exception record (${error.message}); no exception applies (owner: add-dependency).`);\n    return [];\n  }\n}\n\nfunction approvedVersionException(exceptions, ecosystem, id, version, rel) {\n" + (MATCH % 'exceptions') + """}

function checkPackagesProps(rel, text, rules, findings, exceptions) {"""),
    ('L1', '.claude/hooks/post-change-checks.mjs', """    if (/\\$\\(/.test(version)) findings.push(""", """    if (approvedVersionException(exceptions, 'nuget', id, version, rel)) continue;
    if (/\\$\\(/.test(version)) findings.push("""),
    ('L1', '.claude/hooks/post-change-checks.mjs', """function checkPackageJson(rel, text, rules, findings) {""", """function checkPackageJson(rel, text, rules, findings, exceptions) {"""),
    ('L1', '.claude/hooks/post-change-checks.mjs', """      if (rules.policy.npm.floatingVersions.includes(v)) findings.push(""", """      if (approvedVersionException(exceptions, 'npm', name, v, rel)) continue;
      if (rules.policy.npm.floatingVersions.includes(v)) findings.push("""),
    ('L1', '.claude/hooks/post-change-checks.mjs', """  if (name === 'directory.packages.props') checkPackagesProps(rel, text, rules, findings);
  else if (name === 'package.json') checkPackageJson(rel, text, rules, findings);""", """  if (name === 'directory.packages.props') checkPackagesProps(rel, text, rules, findings, loadVersionExceptions(active, findings));
  else if (name === 'package.json') checkPackageJson(rel, text, rules, findings, loadVersionExceptions(active, findings));"""),
    ('L1', '.claude/skills/add-dependency/SKILL.md', """and never floating versions such as `*`, unless explicitly requested.

""", """and never floating versions such as `*`, unless explicitly requested.

""" + TEXT + """

"""),
]
# ---------------------------------------------------- K0
PATCHES += [
    ('K0', '.claude/scripts/check-dependencies.cjs', """function checkPackagesProps(rel, text, result) {""", COMMENT + "function validVersionException(e) {\n" + VALID + "}\n\nfunction loadVersionExceptions(rootDir, result) {\n  const file = path.join(rootDir, 'dependency-version-exceptions.json');\n  if (!fs.existsSync(file)) return [];\n  const label = 'dependency-version-exceptions.json';\n  try {\n    const entries = JSON.parse(fs.readFileSync(file, 'utf8')).exceptions;\n    if (!Array.isArray(entries)) throw new Error('\"exceptions\" is not a list');\n    const valid = entries.filter(validVersionException);\n    if (valid.length !== entries.length) result.errors.push(`${label}: exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by \"user\", and the request text (add-dependency § 2).`);\n    return valid;\n  } catch (error) {\n    result.errors.push(`${label}: unreadable exception record (${error.message}); no exception applies (add-dependency § 2).`);\n    return [];\n  }\n}\n\nfunction approvedVersionException(exceptions, ecosystem, id, version, rel) {\n" + (MATCH % 'exceptions') + """}

function checkPackagesProps(rel, text, result, exceptions) {"""),
    ('K0', '.claude/scripts/check-dependencies.cjs', """    if (!version.trim() || /[*[\\]()]/.test(version)) {
      result.errors.push(`${rel}: ${include} uses a floating""", """    if (approvedVersionException(exceptions, 'nuget', include, version, rel)) {
      result.notices.push(`${rel}: ${include} ${version} is an approved exception recorded in dependency-version-exceptions.json.`);
    } else if (!version.trim() || /[*[\\]()]/.test(version)) {
      result.errors.push(`${rel}: ${include} uses a floating"""),
    ('K0', '.claude/scripts/check-dependencies.cjs', """function checkPackageJson(rootDir, rel, text, result) {""", """function checkPackageJson(rootDir, rel, text, result, exceptions) {"""),
    ('K0', '.claude/scripts/check-dependencies.cjs', """      if (typeof version === 'string' && (/^(\\*|latest|x)?$/i.test(version.trim()) || version.includes('*'))) {
        result.errors.push(""", """      if (typeof version === 'string' && approvedVersionException(exceptions, 'npm', name, version, rel)) {
        result.notices.push(`${rel}: ${section}.${name} ${version} is an approved exception recorded in dependency-version-exceptions.json.`);
      } else if (typeof version === 'string' && (/^(\\*|latest|x)?$/i.test(version.trim()) || version.includes('*'))) {
        result.errors.push("""),
    ('K0', '.claude/scripts/check-dependencies.cjs', """  else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, result);
  else if (name === 'package.json') checkPackageJson(rootDir, rel, text, result);""", """  else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, result, loadVersionExceptions(rootDir, result));
  else if (name === 'package.json') checkPackageJson(rootDir, rel, text, result, loadVersionExceptions(rootDir, result));"""),
    ('K0', '.claude/skills/add-dependency/SKILL.md', """or floating versions such as `*`, unless explicitly requested.

""", """or floating versions such as `*`, unless explicitly requested.

""" + TEXT + """

"""),
]
# ---------------------------------------------------- K1
PATCHES += [
    ('K1', '.claude/scripts/check-manifests.cjs', """function makeContext(root) {
  const facets = loadFacets();
  return {
    root,
    facets,
""", COMMENT + "function validVersionException(e) {\n" + VALID + "}\n\nfunction loadVersionExceptions(root) {\n  const rel = 'dependency-version-exceptions.json';\n  if (!lib.exists(root, rel)) return { entries: [], problem: null };\n  try {\n    const entries = JSON.parse(lib.readText(root, rel)).exceptions;\n    if (!Array.isArray(entries)) throw new Error('\"exceptions\" is not a list');\n    const valid = entries.filter(validVersionException);\n    return { entries: valid, problem: valid.length === entries.length ? null : 'exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by \"user\", and the request text' };\n  } catch (err) {\n    return { entries: [], problem: `unreadable exception record (${err.message}); no exception applies` };\n  }\n}\n\nfunction approvedVersionException(exceptions, ecosystem, id, version, rel) {\n" + (MATCH % 'exceptions') + """}

function exceptionFindings(ctx) {
  return ctx.versionExceptions.problem ? [lib.finding('error', 'dependency-version-exceptions.json', ctx.versionExceptions.problem, OWNER_WORKFLOW)] : [];
}

function makeContext(root) {
  const facets = loadFacets();
  return {
    root,
    facets,
    versionExceptions: loadVersionExceptions(root),
"""),
    ('K1', '.claude/scripts/check-manifests.cjs', """  const findings = [];
  if (!/<ManagePackageVersionsCentrally>""", """  const findings = exceptionFindings(ctx);
  if (!/<ManagePackageVersionsCentrally>"""),
    ('K1', '.claude/scripts/check-manifests.cjs', """    if (!pkg.version || /[*\\[\\](),]/.test(pkg.version)) {""", """    if (approvedVersionException(ctx.versionExceptions.entries, 'nuget', pkg.id, pkg.version, rel)) {
      findings.push(lib.finding('warn', rel, `PackageVersion "${pkg.id}" ${pkg.version} is an approved exception recorded in dependency-version-exceptions.json`, OWNER_WORKFLOW));
    } else if (!pkg.version || /[*\\[\\](),]/.test(pkg.version)) {"""),
    ('K1', '.claude/scripts/check-manifests.cjs', """  const findings = [];
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, spec] of Object.entries(pkg[section] || {})) {
      if (npmVersionIsFloating(spec)) {""", """  const findings = exceptionFindings(ctx);
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, spec] of Object.entries(pkg[section] || {})) {
      if (approvedVersionException(ctx.versionExceptions.entries, 'npm', name, String(spec), rel)) {
        findings.push(lib.finding('warn', rel, `${section}.${name} "${spec}" is an approved exception recorded in dependency-version-exceptions.json`, OWNER_WORKFLOW));
      } else if (npmVersionIsFloating(spec)) {"""),
    ('K1', '.claude/scripts/check-manifests.cjs', """module.exports = { checkFile, checkAll, isManifest, makeContext, parseProject, acceptedDecisionText, isApprovedEdge, isApprovedProject };""", """module.exports = { checkFile, checkAll, isManifest, makeContext, parseProject, acceptedDecisionText, isApprovedEdge, isApprovedProject, loadVersionExceptions };"""),
    ('K1', '.claude/scripts/classify-command.cjs', """function managerFindings(exe, words, segment) {""", """/** DEP-003 exception: the command form of a version the user explicitly requested and that is recorded; the post-change check enforces its manifest. */
function recordedVersion(cwd, ecosystem, id, version) {
  try {
    const lib = require('./lib.cjs');
    const { entries } = require('./check-manifests.cjs').loadVersionExceptions(lib.activeRoot(cwd));
    const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
    return entries.some(e => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted && e.version.trim() === String(version).trim());
  } catch {
    return false;
  }
}

function npmSpecIsRecorded(spec, cwd) {
  const at = spec.indexOf('@', spec.startsWith('@') ? 1 : 0);
  return at > 0 && recordedVersion(cwd, 'npm', spec.slice(0, at), spec.slice(at + 1));
}

function managerFindings(exe, words, segment, cwd) {"""),
    ('K1', '.claude/scripts/classify-command.cjs', """    const loose = specs.filter(s => !npmSpecIsExact(s));""", """    const loose = specs.filter(s => !npmSpecIsExact(s) && !npmSpecIsRecorded(s, cwd));"""),
    ('K1', '.claude/scripts/classify-command.cjs', """  if (!id || typeof version !== 'string' || !EXACT_NUGET.test(version)) {""", """  if (!id || typeof version !== 'string' || (!EXACT_NUGET.test(version) && !recordedVersion(cwd, 'nuget', id, version))) {"""),
    ('K1', '.claude/scripts/classify-command.cjs', """findings.push(...managerFindings(exe, words, segment));""", """findings.push(...managerFindings(exe, words, segment, current));"""),
    ('K1', '.claude/skills/add-dependency/SKILL.md', """or floating versions such as `*`, unless the user explicitly requested them.

""", """or floating versions such as `*`, unless the user explicitly requested them.

""" + TEXT + """

"""),
]
