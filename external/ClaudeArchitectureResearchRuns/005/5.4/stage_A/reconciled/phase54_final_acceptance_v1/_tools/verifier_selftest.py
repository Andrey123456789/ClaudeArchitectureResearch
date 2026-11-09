"""Negative self-test of release/verify_release.py and release/make_working_copy.py.

Run from this task's output folder:  python -B _tools/verifier_selftest.py <scratch_dir>
Copies the release into <scratch_dir> (outside the release), applies one tampering per case,
and checks that the verifier returns FAIL for every tampering and PASS for the untouched control.
Also creates one working copy and checks it is writable, verified, and leaves the release unchanged.
Writes release_verification/VERIFIER_SELFTEST.json. Never writes inside release/.
"""
import json
import os
import shutil
import stat
import subprocess
import sys

OUT = os.getcwd()
REL = os.path.join(OUT, "release")
V3 = os.path.normpath(os.path.join(OUT, "..", "step2_controlled_repair_v3"))
SCR = os.path.abspath(sys.argv[1])


def run_verify(release_dir):
    p = subprocess.run([sys.executable, "-B", os.path.join(REL, "verify_release.py"), "--release-dir", release_dir,
                        "--v3-dir", V3, "--json"], capture_output=True, text=True)
    out = json.loads(p.stdout)
    return p.returncode, out["verdict"]


def fresh(name):
    d = os.path.join(SCR, name)
    if os.path.exists(d):
        raise SystemExit(f"{d} exists; use an empty scratch directory")
    shutil.copytree(REL, d, ignore=shutil.ignore_patterns("__pycache__"))
    for dp, dn, fn in os.walk(d):
        for n in fn:
            os.chmod(os.path.join(dp, n), stat.S_IREAD | stat.S_IWRITE)
    return d


def flip_byte(p):
    b = bytearray(open(p, "rb").read())
    b[len(b) // 2] ^= 0x01
    open(p, "wb").write(bytes(b))


def crlf_to_lf(p):
    b = open(p, "rb").read()
    if b"\r\n" in b:
        open(p, "wb").write(b.replace(b"\r\n", b"\n"))
        return True
    open(p, "wb").write(b.replace(b"\n", b"\r\n"))
    return False


cases = []
os.makedirs(SCR, exist_ok=True)

d = fresh("control")
rc, v = run_verify(d)
cases.append({"case": "C0 untouched copy", "expected": "PASS", "verdict": v, "exit": rc})

d = fresh("n1_flip_byte")
flip_byte(os.path.join(d, "candidates", "M", "template", "CLAUDE.md"))
rc, v = run_verify(d)
cases.append({"case": "N1 one bit flipped in M/CLAUDE.md", "expected": "FAIL", "verdict": v, "exit": rc})

d = fresh("n2_extra_file")
open(os.path.join(d, "candidates", "K1", "template", ".claude", "extra.md"), "w").write("x")
rc, v = run_verify(d)
cases.append({"case": "N2 unexpected file added to K1", "expected": "FAIL", "verdict": v, "exit": rc})

d = fresh("n3_missing_file")
os.remove(os.path.join(d, "candidates", "L0", "template", ".gitignore"))
rc, v = run_verify(d)
cases.append({"case": "N3 L0/.gitignore removed", "expected": "FAIL", "verdict": v, "exit": rc})

d = fresh("n4_manifest_edit")
mp = os.path.join(d, "CANDIDATE_FREEZE_MANIFEST.json")
open(mp, "a", encoding="utf-8").write(" ")
rc, v = run_verify(d)
cases.append({"case": "N4 manifest edited (sidecar mismatch)", "expected": "FAIL", "verdict": v, "exit": rc})

d = fresh("n5_line_endings")
was_crlf = crlf_to_lf(os.path.join(d, "candidates", "K0", "template", ".claude", "settings.json"))
rc, v = run_verify(d)
cases.append({"case": f"N5 K0 settings.json line endings converted ({'CRLF->LF' if was_crlf else 'LF->CRLF'})",
              "expected": "FAIL", "verdict": v, "exit": rc})

# working copy: created, writable, verified; release unchanged afterwards
wc = os.path.join(SCR, "working_copy_M")
p = subprocess.run([sys.executable, "-B", os.path.join(REL, "make_working_copy.py"), "M", wc], capture_output=True, text=True)
writable = all(os.stat(os.path.join(dp, n)).st_mode & stat.S_IWRITE for dp, _, fn in os.walk(wc) for n in fn)
inside = subprocess.run([sys.executable, "-B", os.path.join(REL, "make_working_copy.py"), "M", os.path.join(REL, "wc_inside")],
                        capture_output=True, text=True)
rc, v = run_verify(REL)
cases.append({"case": "W1 working copy of M created and verified", "expected": "exit 0, writable",
              "exit": p.returncode, "writable": writable, "verdict": "PASS" if p.returncode == 0 and writable else "FAIL"})
cases.append({"case": "W2 working copy inside release refused", "expected": "refused",
              "exit": inside.returncode, "verdict": "PASS" if inside.returncode != 0 and not os.path.exists(os.path.join(REL, "wc_inside")) else "FAIL"})
cases.append({"case": "W3 release still verifies after W1/W2", "expected": "PASS", "verdict": v, "exit": rc})

ok = all((c["verdict"] == c["expected"]) if c["expected"] in ("PASS", "FAIL") else c["verdict"] == "PASS" for c in cases)
res = {"tool": "_tools/verifier_selftest.py", "scratch": SCR, "cases": cases, "all_as_expected": ok}
os.makedirs(os.path.join(OUT, "release_verification"), exist_ok=True)
with open(os.path.join(OUT, "release_verification", "VERIFIER_SELFTEST.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(res, f, indent=1)
for c in cases:
    print(c["case"], "->", c["verdict"], "(expected", c["expected"] + ")")
print("ALL_AS_EXPECTED" if ok else "UNEXPECTED")
sys.exit(0 if ok else 1)
