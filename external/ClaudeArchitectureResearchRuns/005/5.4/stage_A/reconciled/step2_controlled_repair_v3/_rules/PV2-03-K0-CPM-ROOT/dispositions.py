"""PV2-03 evidence dispositions. Read with the records citing each range."""


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


DISPOSITIONS = [
    d('K0', '.claude/scripts/check-dependencies.cjs', 247, 249, 'no Directory.Packages.props in its directory or any parent up to the repository root, so Central Package Management cannot apply (D-17).',
      'PV2-03: the root-only error is replaced by the per-project nearest-ancestor check (where MSBuild looks). FG-K0-73dd5d1170 is reworded to the new check.'),
    d('K0', 'docs/architecture/decision-register.md', 42, 42, '`Directory.Packages.props` for Central Package Management (typically at the repository root; any location MSBuild imports for each project is valid)',
      'PV2-03: D-17 keeps the shared build configuration; the central file location is typical, not mandated. FG-K0-934611ccd5 is reworded to match.'),
]
