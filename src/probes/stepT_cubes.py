#!/usr/bin/env python3
"""Can CUBES realise Step T's excess, deg_top > deg_bot at a triple point?  [P405]

X > 0 in [P404] needs a triple point p of a triple S where the triple's TOP diagram (level 1 of S)
has higher degree than its BOTTOM diagram (level 2 of S), with a fourth cube containing p.
PROOF_67 realised deg_top > deg_bot on general six-faced cells; for congruent concentric cubes it
was never tested.  Search: triples (I, b, c) with b, c small-height rational rotations (rich in
coincidences), shared face planes excluded (the level graphs are invalid there), every triple point
classified exactly by its degree in both diagrams.  Unevaluated triples are counted.
"""
import os, sys, itertools, collections, json, random, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import level_s1, on_boundary
from euler3 import rowsT, frames

ROOT = os.path.dirname(os.path.dirname(HERE))


def triple_points(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    top, _, _ = level0(Ms)
    bot, _, _ = level_s1(Ms, [0, 1, 2])
    out = []
    for P in set(top) | set(bot):
        if sum(1 for M in Ms if on_boundary(P, M)) == 3:
            out.append((P, top.get(P, 2), bot.get(P, 2)))
    return out


def level0(Ms):
    """the TOP diagram of the triple: arcs with NO other cube containing them"""
    import depth2_charging as DC
    from euler3 import segments
    from cellcomplex import on_bdry_params
    idx = [0, 1, 2]
    node, arcs = {}, []
    for i, j in itertools.combinations(idx, 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in idx if k not in (i, j) for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                if any(CL.strictly_inside(mid, Ms[k]) for k in idx if k not in (i, j)):
                    continue
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node[P] = node.get(P, 0) + 1
    return node, None, None


def main():
    H = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rnd = random.Random(20260930)
    pool = [q for q in itertools.product(range(-H, H + 1), repeat=4) if any(q) and q[0] >= 0]
    found, spectrum, degen, err, t0 = [], collections.Counter(), 0, 0, time.time()
    for it in range(N):
        b, c = rnd.sample(pool, 2)
        qs = [(1, 0, 0, 0), b, c]
        if CL.shares_plane(qs):
            degen += 1
            continue
        try:
            tp = triple_points(qs)
        except Exception:
            err += 1
            continue
        for P, dt, db in tp:
            spectrum[(dt, db)] += 1
            if dt > db:
                found.append({'qs': qs, 'p': [str(x) for x in P], 'deg_top': dt, 'deg_bot': db})
    print('H=%d: %d triples tried, %d share a face plane (excluded), %d unevaluated, %.0fs'
          % (H, N, degen, err, time.time() - t0))
    print('triple-point (deg_top, deg_bot) spectrum: %s' % dict(sorted(spectrum.items())))
    print('deg_top > deg_bot: %d triple points' % len(found))
    for f in found[:5]:
        print('   ', f)
    json.dump({'H': H, 'N': N, 'excluded': degen, 'unevaluated': err,
               'spectrum': {str(k): v for k, v in spectrum.items()}, 'found': found},
              open(os.path.join(ROOT, 'data', 'stepT_cubes_H%d.json' % H), 'w'), indent=1)


if __name__ == '__main__':
    main()
