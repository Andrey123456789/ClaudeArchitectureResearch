"""PV2-03B claim updates: records that stated the static ancestor check as an unconditional error now state the condition (MSBuild did not
prove another central file imported). Labels, DEP-006/DEP-023 links and modality are unchanged: the per-project CPM obligation is the same."""
RULE = 'PV2-03B-CPM-IMPORT-PROVEN'
NOTE = 'PV2-03B (completes approved PV2-03): a central file MSBuild imports for the project from outside its ancestor folders (DirectoryPackagesPropsPath) is valid; the static ancestor check stands only when the MSBuild proof is missing.'
UPDATES = {
    'FG-K0-36395ffe06': dict(rule=RULE, status='REWORDED', claim='Each project needs a Directory.Packages.props that MSBuild imports for it: one in its own directory or a parent inside the repository, or another file MSBuild imports (DirectoryPackagesPropsPath). The checker errors when there is none above the project and MSBuild does not prove an import; the repository root is the typical place, not a requirement.', note=NOTE, set={}, sub={}),
    'FG-K0-73dd5d1170': dict(rule=RULE, status='REWORDED', claim='A project with no Directory.Packages.props in its directory or any parent up to the repository root is an error, unless MSBuild proves another central file imported for it with Central Package Management on.', note=NOTE, set={}, sub={}),
    'FG-M-7f012a0fe2': dict(rule=RULE, status='REWORDED', claim='Violations when the effective ManagePackageVersionsCentrally MSBuild evaluates for a project is not true, when no central manifest is imported, when package references exist with no Directory.Packages.props above the project and MSBuild does not prove another central file imported, when a PackageVersion lacks Version, or when a project declares or evaluates to a version; an evaluated reference with no PackageVersion is a violation. When the proof cannot run the outcome is NOT_RUN, never a pass.', note=NOTE, set={}, sub={}),
}
ADDED = []
