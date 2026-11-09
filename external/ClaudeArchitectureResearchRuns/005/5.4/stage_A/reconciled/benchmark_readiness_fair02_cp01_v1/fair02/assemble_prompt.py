"""Appends the shared FAIR-02 reporting instruction to a benchmark task prompt, identically for every candidate.

Usage:
  python -B assemble_prompt.py --task TASK_PROMPT.txt --out-dir DIR [--candidates M M1 L0 L1 K0 K1]

Writes DIR/<candidate>.prompt.txt and DIR/PROMPT_ASSEMBLY_MANIFEST.json. Refuses to run if the instruction
file no longer matches its recorded SHA-256, or if the assembled prompts are not byte-identical.
The task prompt itself must already be identical for all candidates; this tool does not edit it.
Composition: <task prompt with trailing whitespace removed> + "\n\n" + <instruction file bytes>.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INSTRUCTION = os.path.join(HERE, "RUN_REPORT_INSTRUCTION.txt")
PROVENANCE = os.path.join(HERE, "RUN_REPORT_INSTRUCTION.provenance.json")
CANDIDATES = ["M", "M1", "L0", "L1", "K0", "K1"]
SEPARATOR = "\n\n"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def assemble(task_text):
    instruction = open(INSTRUCTION, "rb").read()
    expected = json.load(open(PROVENANCE, encoding="utf-8"))["instruction_sha256"]
    if sha(instruction) != expected:
        raise SystemExit("RUN_REPORT_INSTRUCTION.txt does not match its recorded SHA-256; refusing to assemble.")
    return (task_text.rstrip() + SEPARATOR).encode("utf-8") + instruction


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--task", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--candidates", nargs="+", default=CANDIDATES)
    a = ap.parse_args(argv)
    task_bytes = open(a.task, "rb").read()
    prompt = assemble(task_bytes.decode("utf-8"))
    os.makedirs(a.out_dir, exist_ok=True)
    rows = []
    for c in a.candidates:
        p = os.path.join(a.out_dir, f"{c}.prompt.txt")
        with open(p, "wb") as f:
            f.write(prompt)
        rows.append({"candidate": c, "file": os.path.basename(p), "sha256": sha(open(p, "rb").read())})
    identical = len({r["sha256"] for r in rows}) == 1
    manifest = {
        "task_prompt_sha256": sha(task_bytes),
        "instruction_sha256": sha(open(INSTRUCTION, "rb").read()),
        "composition": "task.rstrip() + '\\n\\n' + instruction",
        "position": "end of the first user message of the run (same turn, same priority, same timing for every candidate)",
        "prompts": rows,
        "byte_identical_across_candidates": identical,
    }
    with open(os.path.join(a.out_dir, "PROMPT_ASSEMBLY_MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps(manifest, indent=2))
    if not identical:
        sys.exit(1)


if __name__ == "__main__":
    main()
