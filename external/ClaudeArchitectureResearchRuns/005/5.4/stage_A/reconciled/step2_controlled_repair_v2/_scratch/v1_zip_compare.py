"""One-off, not a tool of the run: compares the v1 tree with the archive the user made of it, by CRC and size. Reads only. Result in this folder."""
import json
import os
import sys
import zipfile
import zlib

REC = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
V1 = os.path.join(REC, 'step2_controlled_repair_v1')
Z = os.path.join(REC, 'step2_controlled_repair_v1.zip')


def crc(p):
    c = 0
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            c = zlib.crc32(b, c)
    return c & 0xffffffff


z = zipfile.ZipFile(Z)
names = [i for i in z.infolist() if not i.is_dir()]
prefixes = {i.filename.split('/')[0] for i in names}
strip = 'step2_controlled_repair_v1/' if prefixes == {'step2_controlled_repair_v1'} else ''
seen, bad, missing = set(), [], []
for i in names:
    rel = i.filename[len(strip):]
    seen.add(rel.replace('\\', '/'))
    p = os.path.join(V1, rel.replace('/', os.sep))
    if not os.path.exists(p):
        missing.append(rel)
    elif os.path.getsize(p) != i.file_size or crc(p) != i.CRC:
        bad.append(rel)
tree = set()
for d, _, fs in os.walk(V1):
    for n in fs:
        tree.add(os.path.relpath(os.path.join(d, n), V1).replace(os.sep, '/'))
out = {'archive_entries': len(names), 'tree_files': len(tree), 'differ': bad, 'missing_in_tree': missing, 'only_in_tree': sorted(tree - seen)[:50], 'n_only_in_tree': len(tree - seen)}
with open(os.path.join(os.path.dirname(__file__), 'v1_zip_compare.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: (v if not isinstance(v, list) else v[:10]) for k, v in out.items()}, indent=0))
sys.exit(0)
