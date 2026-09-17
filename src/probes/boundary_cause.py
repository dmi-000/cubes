#!/usr/bin/env python3
"""What actually bounds the 1217 plateau: first count change on a ray, both families ranked.

The attribution audit [P304] opened, done without relying on any recorded parameter. On a
given ray this takes the roots of BOTH wall families, sorts them, counts in every cell, and
reports the FIRST parameter at which the count leaves the record -- with everything that
vanishes there and whether it has a common point.

Why not just check the recorded boundary: because the recorded boundaries are brackets found
by searching coincidence roots only. Re-deriving the boundary from both families answers the
attribution question and re-measures the extent at the same time.

GENUINE means rank(normals) = rank(augmented) = 3. A quadruple built from a coincidence's own
normals plus planes of another cube has a determinant that vanishes BECAUSE the coincidence
does -- a consequence, not a rival cause. At n = 8 both such quadruples had rank 3 against
rank 4: inconsistent, no common point ([P307] audit).
"""
import sys, os, json
from fractions import Fraction as F
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import sympy as sp
import dimension as D, wall_keys as W, wall_solve as WS
import wall_census as C, concurrency_walls as CW, map_arcs as M
import plateau_solve as PS, provenance as PROV

T = sp.Symbol('t')


def rays_for(n, nc):
    a0, v, lo, hi = M.ARCS['D']
    f = [F(0)] * nc; f[nc - 3] = F(1)
    b = [F(0)] * nc
    for k in range(3):
        b[nc - 6 + k] = v[k]
    return {'fibre_e15': f, 'base_arcD_lift': b}


def walls_on(pt, q0, nc, d, keys, window):
    """(sorted roots, identity) from both families."""
    items = []
    for key in keys:
        try:
            co = W.on_line(key, q0, pt, d)
        except Exception:
            continue
        if len(co) < 2:
            continue
        P = sp.Poly([sp.Rational(x) for x in reversed(co)], T)
        for a, b in C.root_intervals(P, -float(window), float(window)):
            items.append((F(a), F(b), {'family': 'coincidence', 'frame': key['frame'],
                                       'group': [list(g) for g in key['group']]}))
    ts = [F(i + 1, 7) - F(1, 3) for i in range(CW.DEG + 1 + CW.CHECK)]
    snap = [[x[1] for x in CW.planes_at(pt, d, q0, t)] for t in ts]
    lab = [x[0] for x in CW.planes_at(pt, d, q0, F(0))]
    mov = CW.moving_cubes(d)
    for c in combinations(range(len(lab)), 4):
        if not any(lab[i][0] in mov for i in c):
            continue
        vals = [CW.concur_det(*[snap[si][i] for i in c]) for si in range(len(ts))]
        co = CW.newton_poly(ts[:CW.DEG + 1], vals[:CW.DEG + 1])
        if not all(CW._polyval(co, ts[CW.DEG + 1 + j]) == vals[CW.DEG + 1 + j]
                   for j in range(CW.CHECK)):
            continue
        if len(co) < 2 or CW.sturm_count(co, -window, window) == 0:
            continue
        P = sp.Poly([sp.Rational(x) for x in co], T)
        rows = [snap[0][i] for i in c]
        rn = PS.rank([x[:3] for x in rows]); ra = PS.rank(rows)
        for a, b in C.root_intervals(P, -float(window), float(window)):
            items.append((F(a), F(b), {'family': 'concurrency',
                                       'planes': [list(lab[i]) for i in c],
                                       'rank_normals': rn, 'rank_augmented': ra,
                                       'genuine': bool(rn == ra == 3)}))
    items.sort(key=lambda x: (x[0], x[1]))
    return items


def run(n, window=F(1, 8)):
    quats = list(W.REC[n]); q0 = quats[0]
    D.set_field(0); D.QZERO[:] = [q0]
    pt = D.point_of(quats); nc = len(pt)
    rec = D.count_at(pt, len(quats))
    keys = [{k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
            for c in WS.conditions_on(quats)]
    out = {'n': n, 'record': rec, 'window': str(window), 'rays': {}}
    for nm, d in rays_for(n, nc).items():
        items = walls_on(pt, q0, nc, d, keys, window)
        # cluster into distinct crossings
        cl = []
        for a, b, info in items:
            if cl and a <= cl[-1]['hi']:
                cl[-1]['hi'] = max(cl[-1]['hi'], b); cl[-1]['walls'].append(info)
            else:
                cl.append({'lo': a, 'hi': b, 'walls': [info]})
        edges = [-window] + [x for c in cl for x in (c['lo'], c['hi'])] + [window]
        cnt = []
        for i in range(0, len(edges) - 1, 2):
            a, b = edges[i], edges[i + 1]
            s = C.simplest_in(a, b) if a < b else None
            cnt.append(None if s is None else
                       D.count_at([pt[k] + s * d[k] for k in range(nc)], len(quats)))
        first = None
        for j, c in enumerate(cl):
            before = cnt[j] if j < len(cnt) else None
            after = cnt[j + 1] if j + 1 < len(cnt) else None
            if before == rec and after is not None and after != rec:
                gen = [w for w in c['walls']
                       if w['family'] == 'coincidence' or w.get('genuine')]
                first = {'side': 'positive' if c['lo'] > 0 else 'negative',
                         'bracket': [str(c['lo']), str(c['hi'])],
                         'count_before': before, 'count_after': after,
                         'walls_with_a_common_point': gen,
                         'n_walls_total': len(c['walls']),
                         'families': sorted({w['family'] for w in gen})}
                break
        out['rays'][nm] = {'crossings': len(cl), 'counts': cnt,
                           'first_departure_from_record': first}
        print('%-16s crossings %3d | first departure %s' % (
            nm, len(cl), (first['families'] if first else 'none in window')), flush=True)
        if first:
            print('    %s -> %s at %s, walls with a common point: %d of %d'
                  % (first['count_before'], first['count_after'], first['bracket'][0][:12],
                     len(first['walls_with_a_common_point']), first['n_walls_total']),
                  flush=True)
    out['reproduce'] = PROV.stamp(parameters={'n': n, 'window': str(window)})
    p = os.path.join(HERE, '..', '..', 'data', 'boundary_cause_n%d.json' % n)
    json.dump(out, open(p, 'w'), indent=1, default=str)
    print('written data/boundary_cause_n%d.json' % n)


if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
