"""V3-Q10 patches: every checker reads a PackageVersion version as MSBuild does (attribute or child element) and reports a missing or empty one (M1, K0, M). See DECLARATION.md."""
REASON = 'Q-10 resolved within approved semantics (DEP-006 and DEP-003, frozen oracle MUST; PV2-03 invalid package metadata; each candidate own NuGet text): a PackageVersion with no version is an error in all six, and a version given as a Version child element is read as MSBuild reads it.'
POLICIES = ['DEP-006', 'DEP-003']
EVIDENCE = '_investigation/cpm_residual_probe_before.json: <PackageVersion Include="A.B" /> evaluates to an empty Version and NuGet warns NU1604, yet M1 and K0 accept it; K0 accepts an empty <Version></Version> child; M rejects a valid <Version>1.2.3</Version> child that MSBuild, NuGet and the other five accept.'
PATCHES = [
    ('M1', '.claude/scripts/check-manifests.js',
     r"""    const version = versionOf(item);
    if (version !== null) {""",
     r"""    const version = versionOf(item);
    if (version === null) {
      findings.push(finding('ERROR', file, `${id}: PackageVersion has no Version; select the latest stable compatible version (${OWNER_WORKFLOW}).`));
    } else {"""),
    ('K0', '.claude/scripts/check-dependencies.cjs',
     r"""    const include = element.attributes.get('Include');
    const version = element.attributes.get('Version');
    if (!include || version === undefined) continue;""",
     r"""    const include = element.attributes.get('Include');
    // Version metadata as MSBuild reads it: a child <Version> element wins over the attribute.
    const child = /<Version\s*(?:\/>|>([\s\S]*?)<\/Version\s*>)/.exec(element.content);
    const version = child ? (child[1] || '').trim() : element.attributes.get('Version');
    if (!include) continue;
    if (version === undefined) {
      result.errors.push(`${rel}: ${include} has no Version; pin the verified stable version (add-dependency § 2).`);
      checkNugetName(rel, include, result);
      continue;
    }"""),
    ('M', '.claude/scripts/check-manifests.mjs',
     r"""  for (const { attrs } of elements(xml, 'PackageVersion')) {
    const id = attrs.include ?? '(missing Include)';
    checkNuGetId(id, rel, result);
    checkNuGetVersion(id, attrs.version, rel, result);""",
     r"""  for (const { attrs, body } of elements(xml, 'PackageVersion')) {
    const id = attrs.include ?? '(missing Include)';
    checkNuGetId(id, rel, result);
    // Version metadata as MSBuild reads it: a child <Version> element wins over the attribute.
    const child = body !== null ? elements(body, 'Version')[0] : undefined;
    checkNuGetVersion(id, child ? decodeReferences(child.body ?? '') : attrs.version, rel, result);"""),
]
