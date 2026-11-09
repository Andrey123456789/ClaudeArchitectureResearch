"""R27: runs the final cold audit inside the gate. FINDING rows stay in FINAL_AUDIT_RESULTS.jsonl and go to the final report; they never become PASS rows here."""
from final_audit import run_audit


def run(ctx):
    for r in run_audit():
        name = '[%s] %s' % (r['section'], r['test'])
        if r['status'] == 'FAIL':
            ctx.add(name, 'FAIL', r['detail'], r['candidate'], 'AUDIT')
        elif r['status'] == 'NOT_RUN':
            ctx.add(name, 'NOT_RUN', r['detail'], r['candidate'], 'AUDIT')
        elif r['status'] == 'PASS':
            ctx.add(name, 'PASS', r['detail'], r['candidate'], 'AUDIT')
