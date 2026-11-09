"""Applied together with PV2-04 (not before): v2 C07 asserted M has no frontend-test ban; PV2-04 removes that difference."""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(BASE, '_tools', 'suites', 'C07_PARITY_CLOSE.py')
s = open(p, encoding='utf-8').read()
old_line = [l for l in s.split('\n') if l.startswith("    ctx.check('M has no such ban: a real text difference, left as it is'")]
assert len(old_line) == 1
s = s.replace(old_line[0], "    # v3 PV2-04 (approved) adds the M ban; M is now in BAN above and checked like the other five. v2 asserted its absence here.\n    ctx.check('M states the ban in its placement owner (v3 PV2-04)', has('M', '.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`') and by.get('V3A-M-030', {}).get('modality') == 'MUST_NOT', candidate='M', kind='SOURCE')")
a = "BAN = {'M1': (LAYOUT,"
assert s.count(a) == 1
s = s.replace(a, "BAN = {'M': ('.claude/skills/project-structure/SKILL.md', 'Never place frontend tests under `backend/`', 'V3A-M-030'), 'M1': (LAYOUT,")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
p = os.path.join(BASE, '_tools', 'adaptations.py')
s = open(p, encoding='utf-8').read()
a = "    {'file': 'bootstrap_v2.py', 'kind': 'REMOVED',"
b = """    {'file': 'suites/C07_PARITY_CLOSE.py', 'kind': 'TEST_UPDATED', 'change': 'PV2-04-M-FRONTEND-TESTS', 'why': 'C07 asserted "M has no such ban: a real text difference, left as it is". The approved PV2-04 decision removes exactly that difference. M joins the six-candidate BAN table (its placement owner, project-structure step 7, and its added record V3A-M-030 at MUST_NOT), and the absence assertion becomes a presence assertion. Stricter; nothing loosened.', 'negative': 'PV2_04 mutation "the M sentence removed is caught (the placement is no longer forbidden)".'},
    {'file': 'bootstrap_v2.py', 'kind': 'REMOVED',"""
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('applied')
