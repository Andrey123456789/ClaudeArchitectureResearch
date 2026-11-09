"""PV2-03 claim updates: K0 records that stated the repository-root requirement or quoted the old D-17 text now state the placement MSBuild
uses. Labels, DEP-006/DEP-023 links and modality are unchanged: the CPM obligation per project is the same; only the location mandate went."""
RULE = 'PV2-03-K0-CPM-ROOT'
NOTE = 'PV2-03: the root-only mandate is removed (approved); a nested Directory.Packages.props that MSBuild imports for each project is valid. Effective CPM per project is still required.'
UPDATES = {
    'FG-K0-36395ffe06': dict(rule=RULE, status='REWORDED', claim='Each project must have a Directory.Packages.props in its own directory or a parent inside the repository, where MSBuild finds it (checker error); the repository root is the typical place, not a requirement.', note=NOTE, set={}, sub={}),
    'FG-K0-73dd5d1170': dict(rule=RULE, status='REWORDED', claim='A project with no Directory.Packages.props in its directory or any parent up to the repository root is an error.', note=NOTE, set={}, sub={}),
    'FG-K0-934611ccd5': dict(rule=RULE, status='REWORDED', claim='Repository-level Directory.Build.props for genuinely shared build settings and Directory.Packages.props for CPM (typically at the repository root; any location MSBuild imports for each project is valid); project-specific settings stay in their projects.', note=NOTE, set={}, sub={}),
}
ADDED = []
