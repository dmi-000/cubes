#!/usr/bin/env python3
"""The charging argument for d2 <= 65 + c2 + W4 + X at n = 4, checked vertex by vertex.  [P404]

THE ARGUMENT.  Gamma = the level-2 boundary of the 4-compound (2nd = 3rd largest M).  B_S = the
bottom diagram of the triple S (its level-2 boundary: arcs of dA n dB inside the third cube of S).
Every vertex of Gamma is charged to a vertex of some B_S:
  two-body v of pair {a,b}: S = {a, b, the cube that strictly contains v};  claim deg_Gamma = deg_B
  triple point p of S, 4th cube NOT containing p: claim deg_Gamma = deg_B
  triple point p of S, 4th cube containing p: Gamma follows S's TOP diagram; the excess over deg_B
      is X (the Step T phenomenon)
  four-fold points: tested for charging to their four B_S occurrences (the advisor's refinement)
and E_S - V_S = d2(S) - 1 - c_S <= 16 per triple (ANCHOR, c_S >= 1).  Hence
      E_Gamma - V_Gamma  <=  sum_S (E_S - V_S) + X + W4'  <=  64 + X + W4'.

CHECKS, per configuration (the rows of depth2_tradeoff.py, shared face planes excluded):
  G1  each triple: E_S - V_S + c_S + 1 equals the engine's d2(S)
  G2  every two-body and every 4th-outside triple point of Gamma has deg_Gamma == deg_B exactly
  G3  E_Gamma - V_Gamma <= sum_S (E_S - V_S) + X + W4
  G4  the SHARP prediction: in the margin-0 rows (d2 = 66, c2 = 1) the triple budget is exactly 64
"""
import os, sys, itertools, collections, json
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


def level_s1(Ms, idx):
    """level-2 graph of the sub-compound idx: arcs of dA_i n dA_j with exactly one OTHER cube of
    idx strictly containing them.  Returns (node -> degree, E, c)."""
    node, arcs = {}, []
    for i, j in itertools.combinations(idx, 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in idx if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in idx if k not in (i, j) and CL.strictly_inside(mid, Ms[k]))
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
    c = len({f(x) for x in range(len(node))})
    return {P: deg[i] for P, i in node.items()}, len(arcs), c


def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2, w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2)


def engine_d2(qs):
    """the engine's d2, retried under global rotations when its guard refuses: the count cannot
    depend on orientation, and rotating clears the clipping-sliver defect ([P180] Addendum 5)."""
    for r in [(1, 0, 0, 0), (3, 1, 1, 1), (5, 1, 2, 3), (7, 2, -3, 1)]:
        e = CL.engine([qmul(r, q) for q in qs])
        if 'by_depth' in e:
            return e['by_depth'].get('2', 0)
    raise RuntimeError('engine refused under 4 rotations')


def check(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    G, EG, cG = level_s1(Ms, [0, 1, 2, 3])
    VG = len(G)
    triples = list(itertools.combinations(range(4), 3))
    B, budget, g1 = {}, 0, []
    for S in triples:
        dS, ES, cS = level_s1(Ms, list(S))
        B[S] = dS
        budget += ES - len(dS)
        eng = engine_d2([qs[k] for k in S])
        g1.append(ES - len(dS) + cS + 1 == eng)
    X, W4, W4_uncharged, g2_bad, W2 = F(0), F(0), F(0), [], F(0)
    for P, dg in G.items():
        on = [k for k in range(4) if on_boundary(P, Ms[k])]
        inside = [k for k in range(4) if CL.strictly_inside(P, Ms[k])]
        if len(on) == 2:
            W2 += F(dg, 2) - 1
            S = tuple(sorted(on + inside))
            if len(inside) != 1 or S not in B:
                g2_bad.append(('two-body, not exactly one containing cube', P))
                continue
            if B[S].get(P, 2) != dg:
                g2_bad.append(('two-body degree', dg, B[S].get(P, 2)))
        elif len(on) == 3:
            S = tuple(sorted(on))
            dB = B[S].get(P, 2)
            if inside:                             # the 4th cube contains p: Gamma follows TOP
                X += F(max(dg - dB, 0), 2)
            elif dB != dg:
                g2_bad.append(('triple, 4th outside, degree', dg, dB))
        elif len(on) == 4:
            excess = F(dg, 2) - 1
            W4 += excess
            charged = sum(F(B[S].get(P, 2), 2) - 1 for S in triples)
            W4_uncharged += max(excess - charged, 0)
    # every node of Gamma and of each B_S must have degree >= 2: an arc separates two differently
    # labelled cells, so it cannot end.  The charging inequality needs it (uncharged nodes >= 0).
    mindeg = min(list(G.values()) + [d for S in B for d in B[S].values()] or [2])
    eg_minus_vg = EG - VG
    return {'EG-VG': eg_minus_vg, 'c2': cG, 'budget': budget, 'X': X, 'W4': W4,
            'W4_uncharged': W4_uncharged, 'W2': W2, 'g1_all': all(g1), 'g2_bad': g2_bad,
            'g3': eg_minus_vg <= budget + X + W4_uncharged, 'd2': eg_minus_vg + cG + 1,
            'mindeg': mindeg}


def main():
    rows = json.load(open(os.path.join(ROOT, 'data', 'depth2_tradeoff.json')))['rows']
    out, bad = [], 0
    for r in rows:
        qs = [tuple(q) for q in r['qs']]
        c = check(qs)
        margin0 = (r['d2'] == 66 and r['c2'] == 1)
        g4 = (not margin0) or c['budget'] == 64
        ok = c['g1_all'] and not c['g2_bad'] and c['g3'] and g4 and c['d2'] == r['d2'] and c['mindeg'] >= 2
        bad += not ok
        if not ok or margin0 or c['X'] or c['W4']:
            print('%-8s d2 %2d c2 %d | EG-VG %3s budget %3s X %-4s W4 %-4s (uncharged %s) W2 %-3s | G1 %s G2 %s G3 %s G4 %s'
                  % (r['name'][:8], c['d2'], c['c2'], c['EG-VG'], c['budget'], c['X'], c['W4'],
                     c['W4_uncharged'], c['W2'], c['g1_all'], 'ok' if not c['g2_bad'] else c['g2_bad'][:2],
                     c['g3'], g4), flush=True)
        out.append({k: str(v) for k, v in c.items() if k != 'g2_bad'} | {'g2_bad': len(c['g2_bad']),
                                                                        'qs': r['qs'], 'margin0': margin0})
    json.dump(out, open(os.path.join(ROOT, 'data', 'depth2_charging.json'), 'w'), indent=1)
    xs = sum(1 for o in out if o['X'] != '0')
    w4 = sum(1 for o in out if o['W4'] != '0')
    w4u = sum(1 for o in out if o['W4_uncharged'] != '0')
    print('\n%d rows; %d FAIL a gate; X > 0 in %d; W4 > 0 in %d, of which uncharged in %d'
          % (len(out), bad, xs, w4, w4u))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
