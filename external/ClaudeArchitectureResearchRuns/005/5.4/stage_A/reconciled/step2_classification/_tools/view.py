"""Render a compact review view of one frozen batch (reading aid only; writes nothing).

  python -B view.py <C> <B###> [--nosrc] [--maxsrc N]
  python -B view.py <C> --keys KEY1,KEY2,...      (ad-hoc view of selected keys, e.g. calibration)

For each file touched by the batch: loading context, frontmatter, then the merged source regions of the
records' primary anchors (from the immutable inputs), then the records with index numbers used by the
decision file. Reported labels/modalities/triggers are attributed provenance, not classification truth.
"""
import json
import os
import sys

from common import (OUT, union_view, source_key, record_anchor, record_claim_text, occurrences,
                    clauses_by_group, facets, proposals, merge_queue_by_group, file_lines, frontmatter,
                    loading_context, group_primary_clause)

LAB = {'ORACLE_LINKED': 'OL', 'EXTRA': 'EX', 'POTENTIAL_EXTRA': 'PX', 'AMBIGUOUS': 'AMB',
       'POTENTIAL_DIFFERENT_STRENGTH': 'PDS', 'LINK_UNCERTAIN': 'LU'}
RUN = {'PRIMARY': 'P', 'REPLICA': 'R', 'CODEX': 'X'}
FLAG_TYPES = {'APPARENT_CONFLICT', 'UNRESOLVED'}
FLAG_SUB = set()  # trimmed 2026-11-02: only APPARENT_CONFLICT/UNRESOLVED relations shown


def short(s, n):
    s = ' '.join(str(s).split())
    return s if len(s) <= n else s[:n - 3] + '...'


def by_key():
    return {source_key(r): r for r in union_view()}


def merge_ranges(rs, gap=3):
    rs = sorted(rs)
    out = []
    for s, e in rs:
        if out and s <= out[-1][1] + gap:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def render_group(i, r, out):
    g = r['original_group']
    cand = r['candidate']
    occ = occurrences()
    p, s, e = record_anchor(r)
    others = []
    for oid in g['occurrence_ids']:
        o = occ[oid]
        if (o['path'], o['start_line'], o['end_line']) != (p, s, e):
            pp = o['path'].replace('output/template/', '')
            others.append('%s:%d-%d' % (pp, o['start_line'], o['end_line']))
    labs = []
    for l in g['original_labels']:
        mod = l.get('reported_modality')
        lab = LAB.get(l['reported_label'], l['reported_label'])
        pol = ','.join(l.get('reported_policy_ids') or [])
        labs.append('%s:%s%s%s' % (RUN[l['run']], lab, ('/' + short(mod, 60)) if mod else '',
                                   ('[' + pol + ']') if pol else ''))
    out.append('[%d] %s L%d-%d %s%s' % (i, g['group_id'], s, e, g['merge_type'],
                                         (' +occ: ' + '; '.join(others[:3]) + (' ...(%d)' % len(others) if len(others) > 3 else '')) if others else ''))
    out.append('  C: ' + g['neutral_claim_text'])
    out.append('  R: ' + ' '.join(labs))
    c = group_primary_clause(g)
    if c:
        t = c.get('reported_trigger_scope')
        x = c.get('reported_exceptions')
        if t and str(t).startswith('path-scoped'):
            t = 'path-scoped (see fm)'
        if t or x:
            out.append('  T: %s | E: %s' % (short(t or '-', 110), short(x or '-', 110)))
    flags = []
    for q in merge_queue_by_group().get(g['group_id'], []):
        if q['item_type'] in FLAG_TYPES or q.get('subtype') in FLAG_SUB:
            other = [x for x in (q.get('group_ids_a') or []) + (q.get('group_ids_b') or []) if x != g['group_id']]
            flags.append('%s/%s %s: %s' % (q['item_type'][:4], q.get('subtype') or '-', ','.join(other)[:40],
                                           short(q.get('open_question') or '', 110)))
    for f in flags[:4]:
        out.append('  Q: ' + f)
    if len(flags) > 4:
        out.append('  Q: ... %d more queue relations' % (len(flags) - 4))
    if r.get('facet_overlay_ids'):
        out.append('  F: facets ' + ','.join(r['facet_overlay_ids']))


def render_prov(i, r, out):
    t = r['view_record_type']
    p, s, e = record_anchor(r)
    if t == 'PROVISIONAL_NEW_CLAUSE':
        out.append('[%d] %s (PROVISIONAL_NEW_CLAUSE) L%d-%d src=%s' % (i, r['proposal_id'], s, e, r['source_claim_id']))
        out.append('  C: ' + r['proposed_clause_text'])
        out.append('  R: pass1 modality=%s; trigger=%s; compared=%s' % (r.get('modality'), short(r.get('trigger_scope'), 100),
                                                                   ','.join(r.get('same_candidate_groups_compared') or [])))
    else:
        f = facets()[r['facet_id']]
        out.append('[%d] %s (PROVISIONAL_FACET_OVERLAY on %s) L%d-%d kind=%s' % (i, r['facet_id'], f['target_group_id'], s, e, f['facet_kind']))
        out.append('  C: ' + f['facet_text'])
        out.append('  R: pass1 rationale: ' + short(f.get('rationale', ''), 400))
        if f.get('distinguishing_scenario'):
            out.append('  S: ' + short(f['distinguishing_scenario'], 200))


def render(cand, items, maxsrc=260, nosrc=False):
    bk = by_key()
    recs = [bk[k] for k in items]
    out = []
    files = []
    for r in recs:
        p = record_anchor(r)[0]
        if p not in files:
            files.append(p)
    idx = {source_key(r): i for i, r in enumerate(recs, 1)}
    for p in files:
        rel = p.replace('output/template/', '')
        out.append('=' * 8 + ' FILE %s  [%s]' % (rel, loading_context(cand, p)))
        fm, raw = frontmatter(cand, p)
        for ln, l in raw[:8]:
            out.append('   fm%d| %s' % (ln, short(l, 220)))
        mine = [r for r in recs if record_anchor(r)[0] == p]
        if not nosrc:
            lines = file_lines(cand, p)
            rs = merge_ranges([(record_anchor(r)[1], record_anchor(r)[2]) for r in mine])
            shown = 0
            for s, e in rs:
                if shown >= maxsrc:
                    out.append('   ... (source display capped; read file directly for L%d-%d)' % (s, e)); continue
                for ln in range(s, min(e, len(lines)) + 1):
                    if shown >= maxsrc:
                        out.append('   ... (capped at L%d of %d-%d)' % (ln, s, e)); break
                    out.append('%5d| %s' % (ln, lines[ln - 1][:230]))
                    shown += 1
                out.append('   ~')
        out.append('-- records in %s:' % rel)
        for r in mine:
            i = idx[source_key(r)]
            if r['view_record_type'] == 'ORIGINAL_GROUP':
                render_group(i, r, out)
            else:
                render_prov(i, r, out)
    return '\n'.join(out)


def main():
    cand = sys.argv[1]
    maxsrc = 260
    if '--maxsrc' in sys.argv:
        maxsrc = int(sys.argv[sys.argv.index('--maxsrc') + 1])
    if '--keys' in sys.argv:
        items = sys.argv[sys.argv.index('--keys') + 1].split(',')
    else:
        bid = sys.argv[2]
        plan = json.load(open(os.path.join(OUT, '_batches', cand + '.json'), encoding='utf-8'))
        b = [x for x in plan['batches'] if x['batch_id'] == bid][0]
        items = [x['source_key'] for x in b['records']]
        print('##### %s %s  n=%d' % (cand, bid, len(items)))
    sys.stdout.reconfigure(encoding='utf-8')
    print(render(cand, items, maxsrc=maxsrc, nosrc='--nosrc' in sys.argv))


if __name__ == '__main__':
    main()
