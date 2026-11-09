"""V3-Q10 claim updates: K0 checker records that list the PackageVersion version errors now include a missing version, read from the
Version attribute or a Version child element. Labels, policy links and modality are unchanged."""
RULE = 'V3-Q10-PACKAGEVERSION-VERSION'
NOTE = 'V3-Q10 (Q-10 resolved within approved semantics: DEP-006, DEP-003, PV2-03 invalid package metadata): K0 reads a Version child element before the attribute and reports a PackageVersion with no version.'
UPDATES = {
    'FG-K0-6d818b0488': dict(rule=RULE, status='REWORDED', claim='A PackageVersion with a missing, empty, floating (*) or range version (Version attribute or Version child element) is an error and a prerelease gets a notice (allowed only when explicitly requested). A recorded explicit user exception for that package, version and manifest is accepted.', note=NOTE, set={}, sub={}),
    'FG-K0-27ff43d9ff': dict(rule=RULE, status='REWORDED', claim="Missing, empty, floating ('*') or range ([ ] ( )) PackageVersion values (Version attribute or Version child element) are errors; prerelease versions produce a notice that they are allowed only when explicitly requested.", note=NOTE, set={}, sub={}),
    'FG-K0-3213a45f06': dict(rule=RULE, status='REWORDED', claim='Missing, empty, floating or range PackageVersion values are errors and prerelease versions get a notice that they are allowed only when explicitly requested (reported: no explicit-request exception for floating/range versions).', note=NOTE, set={}, sub={}),
}
ADDED = []
