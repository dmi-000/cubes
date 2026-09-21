#!/usr/bin/env python3
"""[OQ 39] What `EE` and `B` ARE — their relation to subsets, depth, symmetry and the walls.

Asked directly.  `EE` and `B` have carried the `max(4)` argument for three days as two numbers
that go up and down; this measures what they are made of.

FIVE QUESTIONS, four measured here and one derived.

  A. SUBSETS.  Is `EE` of a compound the SUM of its pairs' isolated `EE`?  A `(2,2)` vertex
     belongs to one pair, but only while no third cube's boundary passes through it -- then the
     signature lengthens and the vertex leaves `EE` entirely.  So `EE <= sum of pair EE` with
     a DEFICIT measuring exactly that interference.  Same question for `B` against `E_S`,
     where [P346]'s budget law says the relation is an identity.

  B. DEPTH.  Every `(2,2)` and `(1,1,1)` vertex sits at a containment count.  Where in the
     depth profile do they live?

  C. SYMMETRY.  A compound's symmetry group permutes its pairs and triples, and `EE` and `B`
     are sums over the orbits -- so the ORBIT SIZES force the multiplicities.  Measured as the
     multiset of per-pair `EE` and per-triple `E_S`.

  D. THE VERTEX BUDGET.  `EE`, `SC2`, `T3`, `Q4` are the signature census; this prints it whole
     so the two named numbers can be seen against everything they compete with.

  E. WALLS (derived, stated in the output).  `EE > 0` is codimension 1 in the 144 quartics of
     [P366].  `B` is different in kind: three planes ALWAYS meet in a point, so `T3` does not
     change when a concurrence appears -- it changes when an existing triple point crosses the
     edge of a facet, i.e. when it lands on a FOURTH plane.  That is [P304]'s concurrency wall,
     whose mechanism was refuted for count drops but which is the right object here.
"""
import sys, os, json, itertools, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames
import ee_bound_refute as EB
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))

NAMED = {
    'n=4 RECORD': [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (1, 1, 1, 1)],
    'EE=26 triple +1': [(1, 0, 0, 0), (3, 2, 2, 0), (3, -4, 0, -3), (1, 1, 0, 3)],
    'face-diagonal': [(1, 0, 0, 0), (3, 2, 2, 0), (5, 3, 3, 0), (7, 2, 2, 0)],
    'n=5 RECORD': [tuple(q) for q in WK.REC[5]],
}


def census(qs):
    return EB.vertices(qs)[0]


def contain_count(Ms, p):
    """how many cubes contain p (closed)"""
    n = 0
    for M in Ms:
        if all(abs(sum(M[r][z] * p[z] for z in range(3))) <= 1 for r in range(3)):
            n += 1
    return n


def depth_by_sig(qs):
    """containment count of every arrangement vertex, bucketed by signature"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    from cellcomplex import on_bdry_params
    from c_level import strictly_inside
    from euler3 import segments
    pts = set()
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for t in cuts:
                pts.add(tuple(p[z] + t * d[z] for z in range(3)))
    out = collections.defaultdict(collections.Counter)
    for P in pts:
        sig = []
        for M in Ms:
            h = [abs(sum(M[r][z] * P[z] for z in range(3))) for r in range(3)]
            if all(x <= 1 for x in h):
                c = sum(1 for x in h if x == 1)
                if c:
                    sig.append(c)
        if len(sig) >= 2:
            out[tuple(sorted(sig))][contain_count(Ms, P)] += 1
    return out


def main():
    out = {'what': 'what EE and B are made of', 'supports': 'OQ 39', 'compounds': {}}
    for name, qs in NAMED.items():
        n = len(qs)
        sig = census(qs)
        EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
        T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
        Q4 = sum(v for k, v in sig.items() if len(k) >= 4)
        B = T3 + 4 * Qg
        pair_EE = {}
        for i, j in itertools.combinations(range(n), 2):
            pair_EE[(i, j)] = census([qs[i], qs[j]]).get((2, 2), 0)
        tri_ES = {}
        for S in itertools.combinations(range(n), 3):
            s3 = census([qs[i] for i in S])
            tri_ES[S] = s3.get((1, 1, 1), 0) + 4 * s3.get((1, 1, 1, 1), 0)
        sum_pair = sum(pair_EE.values()); sum_tri = sum(tri_ES.values())
        dep = depth_by_sig(qs)

        print('=== %s   (n = %d)' % (name, n))
        print('   signature census: %s' % dict(sorted(sig.items())))
        print('   A. SUBSETS   EE %3d  vs sum of pair EE %3d   deficit %d'
              % (EE, sum_pair, sum_pair - EE))
        print('                B  %3d  vs sum of triple E_S %3d   deficit %d   (budget law)'
              % (B, sum_tri, sum_tri - B))
        print('   C. ORBITS    per-pair EE  %s' % sorted(pair_EE.values(), reverse=True))
        print('                per-triple E_S %s' % sorted(tri_ES.values(), reverse=True))
        for s in ((2, 2), (1, 1, 1)):
            if s in dep:
                print('   B. DEPTH     %-9s by containment count: %s'
                      % (str(s), dict(sorted(dep[s].items()))))
        out['compounds'][name] = {
            'n': n, 'sig': {str(k): v for k, v in sorted(sig.items())},
            'EE': EE, 'SC2': SC, 'T3': T3, 'Q4generic': Qg, 'Q4': Q4, 'B': B,
            'sum_pair_EE': sum_pair, 'EE_deficit': sum_pair - EE,
            'sum_tri_ES': sum_tri, 'B_deficit': sum_tri - B,
            'pair_EE': sorted(pair_EE.values(), reverse=True),
            'tri_ES': sorted(tri_ES.values(), reverse=True),
            'depth': {str(k): {str(a): b for a, b in sorted(v.items())}
                      for k, v in dep.items()}}
        print()

    out['reproduce'] = PROV.stamp(parameters={'compounds': list(NAMED)})
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_b_structure.json'), 'w'), indent=1)
    print('wrote data/ee_b_structure.json')


if __name__ == '__main__':
    main()
