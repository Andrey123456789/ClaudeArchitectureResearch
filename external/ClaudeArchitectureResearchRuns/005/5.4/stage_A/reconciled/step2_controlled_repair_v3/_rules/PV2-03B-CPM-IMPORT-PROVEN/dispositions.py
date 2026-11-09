"""PV2-03B evidence dispositions. Read with the records citing each range."""


def d(c, path, a, b, quote, note):
    return {'candidate': c, 'path': path, 'start_line': a, 'end_line': b, 'disposition': 'REWORDED', 'new_quote': quote, 'note': note}


DISPOSITIONS = [
    d('M', '.claude/scripts/check-manifests.mjs', 262, 271, "'package references exist but no Directory.Packages.props was found above this project (.claude/rules/dependencies.md, NuGet)' });",
      'PV2-03B: the static finding now stands only when MSBuild did not prove a central file imported for the project (DirectoryPackagesPropsPath may name one outside the ancestor folders). FG-M-7f012a0fe2 is reworded to the conditional form.'),
]
