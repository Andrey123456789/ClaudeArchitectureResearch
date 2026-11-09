"""R14: item 8.7 C# language version. No template edit. All six carry the check and the change gate."""
from suitelib2 import anchors


def run(ctx):
    f = '.claude/skills/modern-csharp/SKILL.md'
    anchors(ctx, 'confirm configured language version', {'M': (f, ["confirm that the project's configured language version supports it"]), 'M1': (f, ["Confirm that the project's configured language version supports a feature"]), 'L0': (f, ['Confirm the configured language version supports a feature']),
                                                         'L1': (f, ['Confirm the configured language version supports a feature']), 'K0': (f, ['Confirm the configured language version supports a feature']), 'K1': (f, ['Confirm the configured language version supports a feature'])})
    anchors(ctx, 'changing LangVersion is gated', {'M': (f, ['do not change `LangVersion` or the target framework']), 'M1': (f, ['Changing `LangVersion` or the target framework is a stack']), 'L0': (f, ['changing `LangVersion` or the target framework → Reserved']),
                                                   'L1': (f, ['changing `LangVersion` or the target framework requires approval']), 'K0': (f, ['changing `LangVersion` or the target framework to use newer syntax is a decision']), 'K1': (f, ['never silently change `LangVersion`'])})
