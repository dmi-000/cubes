import time, itertools
import two_plus_quadric as T

T.T0 = time.time()


def build(base, name):
    edge = T.build_edge_conditions(base)
    corner = T.build_corner_conditions(base)
    planes = T.extract_planes(edge)
    quadrics = T.extract_quadrics(corner, planes)
    return planes, quadrics


def classify(base, planes, quadrics, name):
    all_planes = sorted(set(pl for pls in planes.values() for pl in pls))
    all_quads = [(j, qi, cd) for j, qs in quadrics.items() for qi, cd in enumerate(qs)]
    rat_cands = {}
    field_cands = {}
    stats = dict(par=0, deg=0, norr=0, rat_roots=0, irr_roots=0, overcap=0)
    t0 = time.time()
    npairs = len(all_planes) * (len(all_planes) - 1) // 2
    for i, (p1, p2) in enumerate(itertools.combinations(all_planes, 2)):
        line = T.line_from_planes(p1, p2)
        if line is None:
            stats['par'] += 1
            continue
        P0, Dv = line
        for j, qi, cd in all_quads:
            alpha, beta, gamma = T.quad_on_line(cd, P0, Dv)
            kind, d, roots = T.classify_roots(alpha, beta, gamma)
            if kind == 'degenerate':
                stats['deg'] += 1
                continue
            if kind == 'no-real-root':
                stats['norr'] += 1
                continue
            for rkind, rd, t in roots:
                pt = T.eval_point(P0, Dv, t)
                pairs = T.build_free_quat(pt, rd)
                if pairs is None:
                    stats['overcap'] += 1
                    continue
                key = T.sym_key(pairs)
                if rd == 0:
                    stats['rat_roots'] += 1
                    if key not in rat_cands:
                        rat_cands[key] = pairs
                else:
                    stats['irr_roots'] += 1
                    bucket = field_cands.setdefault(rd, {})
                    if key not in bucket:
                        bucket[key] = pairs
        if (i + 1) % 500 == 0:
            print(name, 'pairs', i + 1, '/', npairs, 'elapsed', round(time.time() - t0, 1),
                  'rat', len(rat_cands), 'irr', sum(len(v) for v in field_cands.values()),
                  flush=True)
    el = time.time() - t0
    print(name, 'classify time', el, 'stats', stats, flush=True)
    print(name, 'SYM-DEDUPED distinct rational candidates', len(rat_cands), flush=True)
    print(name, 'SYM-DEDUPED distinct irrational candidates',
          sum(len(v) for v in field_cands.values()), 'across', len(field_cands),
          'd values', flush=True)
    return rat_cands, field_cands


p4, q4 = build(T.BASE4, 'BASE4')
rat4, field4 = classify(T.BASE4, p4, q4, 'BASE4')
p5, q5 = build(T.BASE5, 'BASE5')
rat5, field5 = classify(T.BASE5, p5, q5, 'BASE5')
print('ALL DONE', flush=True)
