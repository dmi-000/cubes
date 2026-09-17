#!/usr/bin/env python3
"""The checks behind [P330], as a runnable gate: does the (2,2) counter agree with an INDEPENDENT
enumerator, and did [P329]'s search pool actually exclude the counterexample?

WHY THIS FILE DOES NOT IMPORT `ee_per_pair`.  That module runs its census at MODULE LEVEL, so
importing it re-runs the census and REWRITES `data/ee_per_pair.json` -- which is how the
provenance block backfilled into that file was destroyed while auditing it ([INTERVENTIONS A15]).
The forty lines it needs are duplicated below instead. A probe whose work happens on import
cannot be audited without being run.

THREE GATES.

  A. DECOMPOSE, don't infer.  [P329] counted 24 "contacts" at q = (0,1,1,1) and [P330] claims
     18 of those are the nine-per-corner incidences at two shared corners. `6 + 9*2 = 24` is
     arithmetic that could be coincidence, so this resolves the 24 BY LOCATION.

  B. AN INDEPENDENT PATH.  `vertices()` finds (2,2) points through `segments()` and the
     arrangement. This builds them the other way -- all 12x12 edge pairs, line-line intersection,
     both parameters in range -- and requires agreement on every admissible pair. The first
     version of this oracle disagreed on 1506 of 1856 because it built edges from the COLUMNS of
     `mat(q)` and tested signatures against the ROWS ([FAILURE_MODES 38], third occurrence).

  C. THE POOL, not the seeds.  [P330] first asserted that [P329]'s search "never looked where the
     (2,2) vertices are". This measures [P329]'s actual candidate pool instead, and refutes that:
     the pool CONTAINS configurations above the bound, and the search missed them by sampling.
"""
import sys, os, json, itertools, collections
from math import gcd, comb
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from step_a2 import mat
from c_level import shares_plane
import ee_bound_refute as B
import provenance as PROV

# [P329]'s candidate pool, transcribed from `ee_total.py` -- not imported, see the docstring.
P329_HI = [(0, 1, 1, 1), (1, 1, 1, 1), (0, 1, 1, 0), (1, 1, 0, 0), (0, 0, 1, 1), (1, 0, 1, 1),
           (2, 1, 1, 1), (1, 2, 1, 1)]
P329_SMALL = [(w, x, y, z) for w in range(0, 4) for x in range(0, 4) for y in range(0, 4)
              for z in range(0, 4) if (w, x, y, z) != (0, 0, 0, 0)]
P329_DRAWS = 400


def edges(M):
    """the 12 edges as (point, direction); the face normals are the COLUMNS of M."""
    out = []
    cols = [[M[r][c] for r in range(3)] for c in range(3)]
    for k in range(3):
        o = [j for j in range(3) if j != k]
        for s0 in (1, -1):
            for s1 in (1, -1):
                out.append(([s0 * cols[o[0]][z] + s1 * cols[o[1]][z] for z in range(3)],
                            [cols[k][z] for z in range(3)]))
    return out


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def contact_points(q):
    """every edge-edge meeting point, with the NUMBER OF EDGE PAIRS meeting there."""
    M0 = [[F(1) if r == c else F(0) for c in range(3)] for r in range(3)]
    M1 = [[F(x) for x in row] for row in mat(q)]
    pts = collections.Counter()
    for (a, u) in edges(M0):
        for (b, v) in edges(M1):
            d = [b[z] - a[z] for z in range(3)]
            if det3(u, v, d) != 0:
                continue
            hit = None
            for (i, j) in ((0, 1), (0, 2), (1, 2)):
                den = u[i] * (-v[j]) - u[j] * (-v[i])
                if den == 0:
                    continue
                hit = ((d[i] * (-v[j]) - d[j] * (-v[i])) / den,
                       (u[i] * d[j] - u[j] * d[i]) / den)
                break
            if hit is None:
                continue
            s, t = hit
            if abs(s) <= 1 and abs(t) <= 1:
                pts[tuple(a[z] + s * u[z] for z in range(3))] += 1
    return pts, M0, M1


def direct_22(q):
    """(2,2) points via edge intersection -- the path `vertices()` does NOT take."""
    pts, M0, M1 = contact_points(q)
    # edges() read the COLUMNS of mat(q); the signature test must read them too.
    Ms = [M0, [[M1[r][c] for r in range(3)] for c in range(3)]]
    out = 0
    for P in pts:
        sig = []
        for M in Ms:
            h = [abs(sum(M[r][z] * P[z] for z in range(3))) for r in range(3)]
            sig.append(sum(1 for x in h if x == 1))
        if tuple(sig) == (2, 2):
            out += 1
    return out


def admissible(hi=6):
    return [q for q in ((w, x, y, z) for w in range(hi + 1) for x in range(hi + 1)
                        for y in range(hi + 1) for z in range(hi + 1))
            if q != (0, 0, 0, 0) and gcd(gcd(q[0], q[1]), gcd(q[2], q[3])) == 1
            and not shares_plane([(1, 0, 0, 0), q])]


def main():
    out = {'what': 'the gates behind [P330]: decomposition, an independent counter, and the pool',
           'question': 'OPEN_QUESTIONS 35', 'supports': 'LEDGER P330'}

    print('GATE A -- resolve [P329]\'s 24 at q=(0,1,1,1) BY LOCATION')
    pts, _, _ = contact_points((0, 1, 1, 1))
    hist = collections.Counter(pts.values())
    nine = {str(tuple(str(v) for v in P)): c for P, c in pts.items() if c == 9}
    out['gate_a'] = {'total_incidences': sum(pts.values()), 'distinct_points': len(pts),
                     'incidences_per_point': {str(k): v for k, v in sorted(hist.items())},
                     'nine_incidence_points': nine,
                     'reconstructs_24': sum(pts.values()) == 24}
    print('   incidences %d over %d distinct points; per-point histogram %s'
          % (sum(pts.values()), len(pts), dict(sorted(hist.items()))))
    for P, c in sorted(pts.items(), key=lambda kv: -kv[1])[:2]:
        print('      %s  ->  %d edge pairs   (a SHARED CORNER)' % (tuple(str(v) for v in P), c))
    print('   so 24 = 6 single contacts + 2 corners x 9   %s'
          % ('CONFIRMED' if sorted(hist.items()) == [(1, 6), (9, 2)] else 'NOT CONFIRMED'))

    print('\nGATE B -- arrangement path vs direct enumeration, every admissible pair')
    cands = admissible()
    bad = [(q, a, b) for q in cands
           for a, b in [(B.vertices([(1, 0, 0, 0), q])[0].get((2, 2), 0), direct_22(q))] if a != b]
    out['gate_b'] = {'pairs_compared': len(cands), 'disagreements': len(bad),
                     'examples': [[list(q), a, b] for q, a, b in bad[:5]]}
    print('   compared %d pairs;  DISAGREEMENTS: %d   %s'
          % (len(cands), len(bad), 'PASS' if not bad else 'FAIL'))

    print('\nGATE C -- did [P329]\'s pool exclude the counterexample?')
    pool = list(dict.fromkeys(P329_HI + P329_SMALL))
    axis = [q for q in pool if q[3] == 0 and q[1] == q[2] and q[1] != 0
            and not shares_plane([(1, 0, 0, 0), q])]
    best = (0, None)
    for combo in itertools.combinations(axis, 3):
        qs = [(1, 0, 0, 0)] + list(combo)
        if shares_plane(qs):
            continue
        ee = B.vertices(qs)[0].get((2, 2), 0)
        if ee > best[0]:
            best = (ee, qs)
    p = comb(len(axis), 3) / comb(len(pool), 3)
    out['gate_c'] = {'pool_size': len(pool), 'common_axis_members': [list(q) for q in axis],
                     'best_in_pool_EE': best[0], 'bound_at_n4': 36,
                     'best_in_pool_quats': [list(q) for q in best[1]],
                     'p_single_draw': p, 'draws': P329_DRAWS,
                     'expected_hits': P329_DRAWS * p,
                     'pool_contained_a_violation': best[0] > 36}
    print('   pool %d, of which %d are rotations about (1,1,0)' % (len(pool), len(axis)))
    print('   best n=4 total EE available INSIDE the pool: %d   (bound 36)  -> %s'
          % (best[0], 'THE POOL CONTAINED A VIOLATION' if best[0] > 36 else 'pool was clean'))
    print('        %s' % ';'.join(','.join(map(str, q)) for q in best[1]))
    print('   P(one draw of 3 lands in the family) = %.2e;  expected hits in %d draws = %.4f'
          % (p, P329_DRAWS, P329_DRAWS * p))

    out['reproduce'] = PROV.stamp(parameters={'quaternion_entry_range': '0..6',
                                              'p329_draws': P329_DRAWS})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'ee_audit.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/ee_audit.json')


if __name__ == '__main__':
    main()
