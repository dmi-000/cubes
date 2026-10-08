#!/usr/bin/env python3
"""Which vertices of the level graphs carry E − V, at n = 5?  (For H1 of [P425].)

[P426] found `X1 − X2 + X3 − X4 = 6` on 193 of 600 generic n = 5 rows. That alternating sum would be
0 if three-cube tie points were the only vertices of degree above 2. So other vertex types
contribute. This classifies every vertex of every level graph.

For a vertex P (an exact point on cube surfaces), record:
- the cubes whose boundary contains P, and for each the number of active faces (1 face, 2 edge,
  3 corner);
- the number of other cubes strictly containing P;
- its degree on each level ℓ, and so its weight `deg/2 − 1` in `X_ℓ`.

The arcs are rebuilt exactly as `c_level.level_graph` builds them, and the per-level totals are
gated against it.

**`--slack`**: on the degenerate rows of data/band_n5_degenerate.json, H1's slack split by vertex
type. Each vertex's contribution to Σ_subsets X_S minus its contribution to the full X's. The split
must sum back to each row's slack. Output: data/vertex_types_n5_slack.json.

Output: data/vertex_types_n5.json.
"""
import os, sys, json, itertools, collections, multiprocessing as mp
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params

ROOT = os.path.dirname(os.path.dirname(HERE))


def graphs(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    deg = collections.defaultdict(collections.Counter)      # level -> point -> degree
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and CL.strictly_inside(mid, Ms[k]))
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    deg[s + 1][P] += 1
    return Ms, deg


def vtype(P, Ms):
    on, inside = [], 0
    for M in Ms:
        v = [abs(sum(M[r][k] * P[k] for k in range(3))) for r in range(3)]
        m = max(v)
        if m == 1:
            on.append(sum(1 for x in v if x == 1))
        elif m < 1:
            inside += 1
    return tuple(sorted(on, reverse=True)), inside


def row(qs):
    qs = [tuple(q) for q in qs]
    Ms, deg = graphs(qs)
    ref = CL.level_graph(qs)
    gate = all(sum(dg.values()) // 2 - len(dg) == ref[l]['E'] - ref[l]['V'] for l, dg in deg.items())
    contrib = collections.defaultdict(lambda: collections.Counter())   # type -> level -> weight
    count = collections.Counter()
    pts = set(P for dg in deg.values() for P in dg)
    for P in pts:
        t = vtype(P, Ms)
        degs = tuple(deg[l].get(P, 0) for l in range(1, len(qs)))
        key = (t[0], t[1], degs)
        count[key] += 1
        for l in range(1, len(qs)):
            dd = deg[l].get(P, 0)
            if dd:
                contrib[key][l] += F(dd, 2) - 1
    X = {l: sum(contrib[k][l] for k in contrib) for l in range(1, len(qs))}
    return {'gate': gate, 'X': {l: str(v) for l, v in X.items()},
            'types': [[list(k[0]), k[1], list(k[2]), c,
                       {l: str(contrib[k][l]) for l in contrib[k] if contrib[k][l]}]
                      for k, c in count.items()]}


def main():
    d = json.load(open(os.path.join(ROOT, 'data', 'band_n5.json')))
    rows = [r for r in d['rows'] if r['slack2'] + r['slack3'] == 0]
    alt = lambda r: r['X']['1'] - r['X']['2'] + r['X']['3'] - r['X']['4'] if isinstance(r['X'], dict) and '1' in r['X'] else \
        r['X'][1] - r['X'][2] + r['X'][3] - r['X'][4]
    six = [r for r in rows if alt(r) == 6][:20]
    zero = [r for r in rows if alt(r) == 0][:20]
    with mp.Pool(8) as p:
        res = p.map(row, [r['qs'] for r in six + zero])
    print('gate (E − V per level equals c_level): %d of %d' % (sum(r['gate'] for r in res), len(res)))
    for label, rs in (('alt = 6', res[:len(six)]), ('alt = 0', res[len(six):])):
        agg = collections.Counter()
        w = collections.defaultdict(collections.Counter)
        for r in rs:
            for on, inside, degs, c, con in r['types']:
                key = (tuple(on), inside, tuple(degs))
                if any(x not in (0, 2) for x in degs):
                    agg[key] += c
                    for l, v in con.items():
                        w[key][l] += F(v)
        print('%s (%d rows): vertex types with some degree other than 2' % (label, len(rs)))
        for key, c in sorted(agg.items(), key=lambda x: -x[1]):
            print('   cubes on (active faces) %-10s inside %d  degrees by level %-14s count %5d  X weight %s'
                  % (key[0], key[1], key[2], c, {l: str(v) for l, v in sorted(w[key].items())}))
    json.dump({'rows': res}, open(os.path.join(ROOT, 'data', 'vertex_types_n5.json'), 'w'), indent=1, default=str)


if __name__ == '__main__' and '--slack' not in sys.argv:
    main()


def slack_row(qs):
    """per vertex type, its contribution to slack2 = Σ_tri X_S(2) − X2 − X4 and
    slack3 = Σ_4 X_S(3) − X3 − X4"""
    qs = [tuple(q) for q in qs]
    Ms, deg = graphs(qs)
    sub = {}
    for k, l in ((3, 2), (4, 3)):
        for S in itertools.combinations(range(5), k):
            _, dg = graphs([qs[i] for i in S])
            for P, dd in dg.get(l, {}).items():
                sub.setdefault((l, P), 0)
                sub[(l, P)] += F(dd, 2) - 1
    w = lambda l, P: (F(deg[l][P], 2) - 1) if P in deg.get(l, {}) else 0
    pts = set(P for dg in deg.values() for P in dg) | set(P for _, P in sub)
    out = collections.defaultdict(lambda: [0, F(0), F(0)])
    for P in pts:
        t = vtype(P, Ms)
        degs = tuple(deg[l].get(P, 0) for l in range(1, 5))
        s2 = sub.get((2, P), 0) - w(2, P) - w(4, P)
        s3 = sub.get((3, P), 0) - w(3, P) - w(4, P)
        if s2 or s3 or any(x not in (0, 2) for x in degs):
            key = (t[0], t[1], degs)
            out[key][0] += 1
            out[key][1] += s2
            out[key][2] += s3
    return [[list(k[0]), k[1], list(k[2]), v[0], str(v[1]), str(v[2])] for k, v in out.items()]


def main_slack():
    d = json.load(open(os.path.join(ROOT, 'data', 'band_n5_degenerate.json')))
    rows = [r for r in d['rows'] if r['slack2'] + r['slack3'] > 0]
    with mp.Pool(8) as p:
        res = p.map(slack_row, [r['qs'] for r in rows])
    agg = collections.defaultdict(lambda: [0, F(0), F(0)])
    ok = 0
    for r, types in zip(rows, res):
        s2 = sum(F(t[4]) for t in types)
        s3 = sum(F(t[5]) for t in types)
        ok += (s2 == r['slack2'] and s3 == r['slack3'])
        for on, inside, degs, c, a2, a3 in types:
            key = (tuple(on), inside, tuple(degs))
            agg[key][0] += c
            agg[key][1] += F(a2)
            agg[key][2] += F(a3)
    print('degenerate rows %d; per-vertex slack sums reproduce the row slack: %d' % (len(rows), ok))
    for key, (c, a2, a3) in sorted(agg.items(), key=lambda x: -x[1][0]):
        if a2 or a3 or any(x not in (0, 2) for x in key[2]):
            print('   on %-12s inside %d  degrees %-14s count %5d  slack2 %6s  slack3 %6s'
                  % (key[0], key[1], key[2], c, a2, a3))
    neg = [(k, v) for k, v in agg.items() if v[1] < 0 or v[2] < 0]
    print('types with negative total slack: %d' % len(neg))
    rowneg = sum(1 for types in res for t in types if F(t[4]) < 0 or F(t[5]) < 0)
    print('(row, type) pairs with a negative contribution: %d' % rowneg)
    json.dump({'types': [[list(k[0]), k[1], list(k[2]), v[0], str(v[1]), str(v[2])] for k, v in agg.items()],
               'reproduced': ok, 'rows': len(rows)},
              open(os.path.join(ROOT, 'data', 'vertex_types_n5_slack.json'), 'w'), indent=1)


if __name__ == '__main__' and '--slack' in sys.argv:
    main_slack()
