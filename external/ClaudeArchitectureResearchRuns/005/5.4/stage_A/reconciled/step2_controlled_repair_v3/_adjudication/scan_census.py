"""Census of security-scan investigation atoms across six candidates: source line in frozen bytes vs. v2 records that state the atom."""
import json, re, os, sys
sys.path.insert(0, '_tools')
from rcommon import CANDIDATES, input_path, read_lines, norm_ws
v2=[json.loads(l) for l in open(r'..\step2_controlled_repair_v2\REPAIRED_CLASSIFICATIONS.jsonl',encoding='utf-8')]
ATOMS = {
 'acct-hashing': (r'password hashing|\bhashing\b', r'password hash|hashing'),
 'acct-reset': (r'reset', r'\breset'),
 'acct-lockout': (r'lockout', r'lockout|brute'),
 'acct-enumeration': (r'enumeration', r'enumeration'),
 'acct-credential-storage': (r'credential storage', r'credential storage'),
 'cfg-debug-flags': (r'debug/development flags', r'debug'),
 'cfg-verbose-errors': (r'verbose (production )?error', r'verbose'),
 'cfg-env-files': (r'\.env`? files', r'\.env'),
 'cfg-cert-bypass': (r'certificate-validation bypass', r'certificate'),
 'cfg-cred-urls': (r'URLs carrying credentials', r'URL'),
 'upload-execution': (r'execution or public-serving|execution/public-serving', r'execut'),
 'upload-public-serving': (r'public-serving', r'public'),
 'ssrf-inspect': (r'influence(s)? (over )?(the )?scheme', r'scheme|host/URL|user-controlled host|SSRF via'),
 'raw-html-ssr': (r'raw HTML', r'raw HTML|server-rendered UI'),
 'log-dup-missing': (r'(duplicate|duplicated) or missing|missing or duplicated', r'duplicat'),
}
SCAN='.claude/skills/security-scan/references/scan-layers.md'
for atom,(src_rx,claim_rx) in ATOMS.items():
    print('=====', atom)
    for c in CANDIDATES:
        p=input_path(c, SCAN)
        lines=read_lines(p) if os.path.exists(p) else []
        hits=[n for n,l in enumerate(lines,1) if re.search(src_rx,l,re.I)]
        # join wrapped lines: also test windows of 3
        if not hits:
            hits=[n for n in range(1,len(lines)+1) if re.search(src_rx,norm_ws(' '.join(lines[n-1:n+2])),re.I)][:1]
        recs=[]
        for r in v2:
            if r['candidate']!=c or not r['repair']['active']: continue
            refs=[(e.get('start_line'),e.get('end_line')) for e in r['current_evidence_refs'] if e.get('start_line') and e['path'].endswith(SCAN)]
            if any(s<=h+2 and e>=h-2 for h in hits for s,e in refs) and re.search(claim_rx, r['claim_text'] or '', re.I):
                recs.append('%s[%s/%s]' % (r['source_key'], r['classification'][:8], r.get('modality')))
        print('  %-3s src=%s recs=%s' % (c, hits[:3], recs))
