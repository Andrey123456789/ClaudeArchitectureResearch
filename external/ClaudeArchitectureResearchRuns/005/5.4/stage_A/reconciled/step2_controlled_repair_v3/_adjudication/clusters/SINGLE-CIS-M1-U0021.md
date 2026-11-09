# SINGLE-CIS-M1-U0021 (1 records)

## CIS-M1-U0021 (pass 2) M1 .claude/scripts/check-instructions.js:209-218  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The section-reference check accepts a nonempty leading word prefix matching an existing normalized heading, even when the complete captured section text does not match.
TRIGGER: Checking a recognized backticked target followed by a section-sign reference in an instruction artifact; target resolves. | EXC: Other checker errors still apply. Trailing words may intentionally be prose after the heading; does not establish that every longer string is an invalid reference or that the complete checker passes. | POL: ['WF-001']
CODEX WHY: Source-grounded effective acceptance boundary plausibly differs from complete section resolution. Independent existing slot/import exactness BF0055 concerns different targets, not this predicate. Normative significance remains uncertain because shortening may simply parse prose after a valid heading.
```
 206      for (const m of flat.matchAll(/`([a-z][a-z0-9-]*)`\s+(workflow|skill|agent)\b/g)) {
 207        if (!skillTarget(m[1])) add('ERROR', f, `${m[2]} reference does not resolve: ${m[1]}`);
 208      }
 209>     for (const m of flat.matchAll(/`([^`\n]+)`(?:\s+(?:workflow|skill|rule))?\s+§\s+([^.;:,)`§]+)/g)) {
 210>       const target = names.includes(m[1]) ? `.claude/skills/${m[1]}/SKILL.md` : resolveRef(m[1], f);
 211>       if (!target) {
 212>         if (!isInactive(m[1])) add('ERROR', f, `section reference target does not resolve: ${m[1]}`);
 213>         continue;
 214>       }
 215>       const words = m[2].trim().split(/\s+/);
 216>       let ok = false;
 217>       for (let n = words.length; n > 0 && !ok; n--) ok = hasHeading(target, words.slice(0, n).join(' '));
 218>       if (!ok) add('ERROR', f, `section reference does not resolve: ${m[1]} § ${m[2].trim()}`);
 219      }
 220    }
 221    const routing = /## Workflow Routing([\s\S]*?)(\n## |$)/.exec(common.readText('CLAUDE.md'));
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-3cbc656bc8 [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Required workflow skills (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance, development-workflow) and embedded knowledge s
- V2 FG-M1-3cbc656bc8 [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Required workflow skills (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance, development-workflow) and embedded knowledge s
- V2 FG-M1-3fead00a3e [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: template-maintenance must set disable-model-invocation: true.
- V2 FG-M1-3fead00a3e [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: template-maintenance must set disable-model-invocation: true.
- V2 FG-M1-e9dfb16975 [212, 212] INTERNAL_ARCHITECTURE/SHOULD pol=[] rel=[]: Warn when the always-loaded surface exceeds about 6500 tokens.
- V2 FG-M1-e9dfb16975 [218, 218] INTERNAL_ARCHITECTURE/SHOULD pol=[] rel=[]: Warn when the always-loaded surface exceeds about 6500 tokens.
- V2 FG-M1-ab58889322 [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Every instruction file's first content line must be a '> ' classification/ownership header.
- V2 FG-M1-ab58889322 [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Every instruction file's first content line must be a '> ' classification/ownership header.
- V2 FG-M1-ed62b948a3 [212, 212] INTERNAL_ARCHITECTURE/MUST_NOT pol=[] rel=[]: No Level:/Kind: classification may appear in instruction files.
- V2 FG-M1-ed62b948a3 [218, 218] INTERNAL_ARCHITECTURE/MUST_NOT pol=[] rel=[]: No Level:/Kind: classification may appear in instruction files.
- V2 FG-M1-a9b15db22c [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: CLAUDE.md keeps a Workflow Routing section whose targets exist.
- V2 FG-M1-a9b15db22c [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: CLAUDE.md keeps a Workflow Routing section whose targets exist.
- V2 FG-M1-229f8b91f5 [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: .claude/rules/ stays flat and every rule declares a non-empty paths list.
- V2 FG-M1-229f8b91f5 [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: .claude/rules/ stays flat and every rule declares a non-empty paths list.
- V2 FG-M1-aaf3401ee3 [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Skill front-matter name equals its directory and has a concrete description (≥20 characters).
- V2 FG-M1-aaf3401ee3 [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Skill front-matter name equals its directory and has a concrete description (≥20 characters).
- V2 FG-M1-333e8b6f6e [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Skill-private files live only in the skill's references/ directory.
- V2 FG-M1-333e8b6f6e [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Skill-private files live only in the skill's references/ directory.
- V2 FG-M1-debd1c101f [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: CLAUDE.md imports must resolve and no other instruction file may contain an @-import (always-loaded files are imported directly from CLAUDE.md).
- V2 FG-M1-debd1c101f [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: CLAUDE.md imports must resolve and no other instruction file may contain an @-import (always-loaded files are imported directly from CLAUDE.md).
- V2 FG-M1-ea34763ee6 [195, 229] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Backticked instruction references, workflow/skill/agent references, § section references, routing targets and manifest anchors must resolve (inactive facets of disabled slots exempt).
- V2 FG-M1-ea34763ee6 [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Backticked instruction references, workflow/skill/agent references, § section references, routing targets and manifest anchors must resolve (inactive facets of disabled slots exempt).
- V2 FG-M1-ea34763ee6 [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: Backticked instruction references, workflow/skill/agent references, § section references, routing targets and manifest anchors must resolve (inactive facets of disabled slots exempt).
- V2 FG-M1-6c87e2eeb9 [212, 212] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: MAP.md must list every instruction file, enforcement script/JSON, root config file, SPECIFICATION.md and CUSTOM_SETTINGS.md.
- V2 FG-M1-6c87e2eeb9 [218, 218] INTERNAL_ARCHITECTURE/MUST pol=[] rel=[]: MAP.md must list every instruction file, enforcement script/JSON, root config file, SPECIFICATION.md and CUSTOM_SETTINGS.md.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0062 -> FG-M1-ea34763ee6 [INTERNAL_ARCHITECTURE] Backticked instruction references, workflow/skill/agent references, § section references, routing targets and manifest anchors must resolve (inactive facets of disabled slots exemp
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0014 -> FG-M1-6c87e2eeb9 [INTERNAL_ARCHITECTURE] MAP.md must list every instruction file, enforcement script/JSON, root config file, SPECIFICATION.md and CUSTOM_SETTINGS.md.
