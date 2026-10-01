#!/usr/bin/env python3
"""How much room does the depth-2 trade-off have?  [P402]'s condition, measured at n = 4.

[P402]: on the level-2 boundary Gamma (2nd = 3rd largest M), with weights w(v) = deg/2 - 1,

    d2 = 1 + c2 + W3 + W2 + W4          (Euler: d2 = E - V + c2 + 1)

W3 = weight of vertices on exactly three cube boundaries (triple points, 1/2 each when simple),
W2 = two-body weight (vertices on exactly two boundaries: edge-edge 1, shared corner 2), W4 = four.
Since the triple points of the four triples number at most 128, a generic W3 <= 64, and

    d2 <= 66   <=>   (c2 - 1) + W2 + W4  <=  64 - W3        (the triple-point deficit)

This measures every term exactly (the level graph of `c_level.py`, Fractions), on the records and
on random rational configurations, and reports how tight the trade-off is: is two-body weight at
depth 2 ever present, and when it is, how much deficit pays for it?

GATE: E - V + c2 + 1 must equal the engine's d2 on EVERY configuration (the identity is exact with
the wall graph, [P243]); a failure voids that row. Configurations sharing a face plane are excluded
and counted: the pipeline is invalid there ([P246]).
"""
import os, sys, itertools, collections, json, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import c_level as CL
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params

ROOT = os.path.dirname(os.path.dirname(HERE))


def on_boundary(P, M):
    vals = [sum(M[r][k] * P[k] for k in range(3)) for r in range(3)]
    return all(-1 <= v <= 1 for v in vals) and any(v == 1 or v == -1 for v in vals)


def level2(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    node, arcs = {}, []
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and CL.strictly_inside(mid, Ms[k]))
                if s != 1:
                    continue
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, len(node))
                    ends.append(node[P])
                arcs.append(tuple(ends))
    deg = collections.Counter()
    for a, b in arcs:
        deg[a] += 1
        deg[b] += 1
    par = list(range(len(node)))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in arcs:
        par[f(a)] = f(b)
    c2 = len({f(x) for x in range(len(node))})
    W = collections.Counter()
    for P, idx in node.items():
        k = sum(1 for M in Ms if on_boundary(P, M))
        W[k] += F(deg[idx], 2) - 1
    return {'V': len(node), 'E': len(arcs), 'c2': c2, 'W2': W[2], 'W3': W[3], 'W4': W[4] + W[5],
            'Wother': sum(v for k, v in W.items() if k not in (2, 3, 4, 5))}


def main():
    named = [('RECORD 183', '1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4'),
             ('refuter 173 (P373)', '1,0,0,0;0,2,-3,-2;0,2,-3,2;-4,-2,-5,-6'),
             ('P374 climb, 177 by formula / 175', '1,0,0,0;0,2,-3,-2;0,2,3,2;-4,0,-5,-6')]
    rnd = random.Random(20260930)
    pop = [(nm, CL.parse(s)) for nm, s in named]
    while len(pop) < 3 + 250:
        qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-7, 7) for _ in range(4)) for _ in range(3)]
        if any(not any(q) for q in qs):
            continue
        pop.append(('random', qs))
    rows, voided, degen = [], 0, 0
    for nm, qs in pop:
        if CL.shares_plane(qs):
            degen += 1
            continue
        e = CL.engine(qs)
        d2 = e['by_depth'].get('2', 0)
        g = level2(qs)
        ident = g['E'] - g['V'] + g['c2'] + 1
        if ident != d2:
            voided += 1
            print('IDENTITY FAILS', nm, qs, ident, d2)
            continue
        slack = 66 - d2
        rows.append({'name': nm, 'qs': qs, 'total': e['bounded'], 'd2': d2, 'c2': g['c2'],
                     'W2': str(g['W2']), 'W3': str(g['W3']), 'W4': str(g['W4']),
                     'Wother': str(g['Wother']), 'deficit': str(64 - g['W3']), 'slack': slack})
        if nm != 'random':
            print('%-34s total %3d  d2 %2d  c2 %d  W2 %-4s W3 %-5s W4 %-4s deficit %-5s slack %d'
                  % (nm, e['bounded'], d2, g['c2'], g['W2'], g['W3'], g['W4'], 64 - g['W3'], slack), flush=True)
    R = [r for r in rows if r['name'] == 'random']
    w2pos = [r for r in R if F(r['W2']) > 0]
    print('\n%d random configurations evaluated, %d excluded (shared face plane), %d voided by the gate'
          % (len(R), degen, voided))
    print('d2 > 66 anywhere: %d' % sum(1 for r in rows if r['d2'] > 66))
    print('with two-body weight at depth 2: %d of %d' % (len(w2pos), len(R)))
    if w2pos:
        tight = sorted(w2pos, key=lambda r: r['slack'])[:8]
        print('  tightest (smallest slack 66 - d2) among them:')
        for r in tight:
            print('    d2 %2d  c2 %d  W2 %-4s W4 %-4s deficit %-5s -> slack %d   total %d'
                  % (r['d2'], r['c2'], r['W2'], r['W4'], r['deficit'], r['slack'], r['total']))
    print('c2 values: %s' % dict(collections.Counter(r['c2'] for r in rows)))
    print('min slack overall: %d (at d2 = %d)' % (min(r['slack'] for r in rows), max(r['d2'] for r in rows)))
    json.dump({'rows': rows, 'excluded_shared_plane': degen, 'voided': voided},
              open(os.path.join(ROOT, 'data', 'depth2_tradeoff.json'), 'w'), indent=1, default=str)
    print('wrote data/depth2_tradeoff.json')


if __name__ == '__main__':
    if not CL.gate():
        sys.exit('GATE FAILED')
    main()
