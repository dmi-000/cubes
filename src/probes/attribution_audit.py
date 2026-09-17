#!/usr/bin/env python3
"""Were the recorded plateau boundaries attributed to the right wall?

[P304] found a second wall family. Every boundary this project located as "the nearest wall
root at which the count changes" searched the COINCIDENCE family only -- [P296]'s arc D extent,
[P301]/[P302]/[P303]'s three walls of the 1217 plateau. The measured EXTENTS stand: they were
counted, not inferred. What is unaudited is the ATTRIBUTION, because a concurrency wall at the
same parameter would be an equally good cause and no search would have seen it.

This restricts BOTH families to the ray and reports, for each claimed boundary, whether a
concurrency wall vanishes there too.
"""
import sys, os, json
from fractions import Fraction as F
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import sympy as sp
import dimension as D, wall_keys as W, wall_solve as WS
import wall_census as C, concurrency_walls as CW, map_arcs as M, provenance as PROV
import plateau_solve as PS

T = sp.Symbol('t')
# boundary parameters as recorded, with the condition each was attributed to
CLAIMS = {8: {'t': '-0.0236342201', 'attributed': 'frame 7, group ((2,1,1),(5,1,1))',
              'source': 'P303'}}


def audit(n, window=F(1, 10)):
    quats = list(W.REC[n]); q0 = quats[0]
    D.set_field(0); D.QZERO[:] = [q0]
    pt = D.point_of(quats); nc = len(pt)
    a0, v, lo, hi = M.ARCS['D']
    d = [F(0)] * nc                      # the base direction: arc D lifted to cube 5
    for k in range(3):
        d[3 * 5 - 3 + k] = v[k]
    claim = CLAIMS[n]
    tgt = float(claim['t'])
    out = {'n': n, 'record': D.count_at(pt, len(quats)), 'claim': claim,
           'direction': 'arc D lift on cube 5', 'window': str(window),
           'coincidence_roots_near': [], 'concurrency_roots_near': []}
    tol = 1e-7

    keys = [{k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
            for c in WS.conditions_on(quats)]
    for key in keys:
        try:
            co = W.on_line(key, q0, pt, d)
        except Exception:
            continue
        if len(co) < 2:
            continue
        P = sp.Poly([sp.Rational(x) for x in reversed(co)], T)
        for a, b in C.root_intervals(P, -float(window), float(window)):
            mid = (float(a) + float(b)) / 2
            if abs(mid - tgt) < tol:
                out['coincidence_roots_near'].append(
                    {'frame': key['frame'], 'group': [list(g) for g in key['group']],
                     'root': [str(a), str(b)]})
    print('coincidence walls at the claimed boundary: %d'
          % len(out['coincidence_roots_near']), flush=True)

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
        for a, b in C.root_intervals(P, -float(window), float(window)):
            mid = (float(a) + float(b)) / 2
            if abs(mid - tgt) < tol:
                rows = [snap[0][i] for i in c]
                # GENUINE means a common point exists: rank(normals) = rank(augmented) = 3.
                # The first version counted distinct normals instead, which is not the test,
                # and it called this boundary AMBIGUOUS on two quadruples that have no common
                # point at all (rank 3 normals, rank 4 augmented -- an inconsistent system).
                rn = PS.rank([x[:3] for x in rows]); ra = PS.rank(rows)
                out['concurrency_roots_near'].append(
                    {'planes': [list(lab[i]) for i in c], 'rank_normals': rn,
                     'rank_augmented': ra, 'genuine': bool(rn == ra == 3),
                     'root': [str(a), str(b)]})
    print('concurrency walls at the claimed boundary: %d'
          % len(out['concurrency_roots_near']), flush=True)
    gen = [w for w in out['concurrency_roots_near'] if w['genuine']]
    out['genuine_concurrency_at_boundary'] = len(gen)
    out['attribution'] = (
        'AMBIGUOUS: a genuine concurrency wall vanishes there too' if gen and out['coincidence_roots_near']
        else 'CONFIRMED: the coincidence condition is the only wall with a common point there'
        if out['coincidence_roots_near'] else 'NOT REPRODUCED')
    out['note'] = ('The rank-degenerate quadruples found here carry the coincidence\'s OWN '
                   'normals plus two planes of the added cube: their determinant vanishes '
                   'BECAUSE the coincidence does. A consequence, not an independent wall.')
    print(out['attribution'], flush=True)
    return out


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    r = audit(n)
    r['reproduce'] = PROV.stamp(parameters={'n': n})
    p = os.path.join(HERE, '..', '..', 'data', 'attribution_audit_n%d.json' % n)
    json.dump(r, open(p, 'w'), indent=1, default=str)
    print('written data/attribution_audit_n%d.json' % n)
