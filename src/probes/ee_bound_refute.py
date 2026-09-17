#!/usr/bin/env python3
"""[OQ 35] `sum EE <= 6*C(n,2)` is FALSE, and [P329]'s witness for the per-pair version was
counting the wrong object.

TWO DEFINITIONS OF "EE" WERE IN PLAY AND THEY ARE NOT THE SAME NUMBER.

  * `ee_per_pair.contacts(q)` counts PAIRS OF EDGES that meet -- an incidence count.
  * [P328]'s identity uses the number of ARRANGEMENT VERTICES of signature (2,2) -- a vertex
    count.  That is the term `EE` in
        TOTAL = [ 1 + L + sum holes + T3 ] + [ EE + 2*SC2 + 3*Q4 + 4*EE3 + 7*SC3 ].

They differ exactly where three edges of one cube meet three of the other at a SHARED CORNER:
that is ONE vertex, of signature (3,3), and it contributes NINE edge-pair incidences.  At
q = (0,1,1,1) -- a 180-degree rotation about a body diagonal, which fixes two opposite corners --
there are two such corners, so the incidence count exceeds the vertex count by 2*9 = 18.
[P329] read 24 incidences as 24 edge-edge contacts and reported `EE <= 6 per pair` refuted by a
factor of four.  **The (2,2) vertex count at (0,1,1,1) is 6 -- exactly what the codimension
derivation predicts, so that configuration is not a counterexample at all.**

THE PER-PAIR BOUND IS STILL FALSE, but the true witness is elsewhere and is half the size: 10,
at 72 of the 1856 admissible coprime quaternions with entries 0..6, e.g. q = (3,2,2,0) -- a
rotation about a FACE DIAGONAL.

AND THE TOTAL BOUND FALLS WITH IT.  [P329] tested `sum EE <= 6*C(n,2)` at n = 4 over 400
configurations seeded from the high-incidence quaternions -- and those seeds were selected by the
WRONG counter, so the search never looked where the (2,2) vertices actually are.  Rotating every
cube about ONE COMMON face diagonal keeps every pairwise rotation in the same family:

    n = 2   bound  6   found 10
    n = 3   bound 18   found 22
    n = 4   bound 36   found 42

Reported with the region counts, because the interesting part is that buying EE this way does not
buy regions: the identity still balances, and the gain is paid back in the generic term.
"""
import sys, os, json, itertools, collections
from math import gcd
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import shares_plane, level_graph, engine, strictly_inside
import wall_keys as W
import provenance as PROV

EXCESS = {(1, 2): 0, (2, 2): 2, (1, 1, 1): 2, (3, 3): 4, (1, 1, 1, 1): 6,
          (2, 2, 2): 8, (3, 3, 3): 14}


def vertices(qs):
    """every arrangement vertex: its signature, and its MEASURED excess.

    The excess is not read off the signature.  [P328] tabulated one excess per signature from the
    records, and those constants are GENERIC values: this probe measures `sum_levels (deg(v) - 2)`
    at each vertex and reports where the table disagrees, because on the degenerate family below
    it does.
    """
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    deg = collections.defaultdict(collections.Counter)      # level -> vertex -> degree
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                sd = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                for t in (a, b):
                    deg[sd + 1][tuple(p[z] + t * d[z] for z in range(3))] += 1
    # a vertex on b cube boundaries appears at b-1 LEVELS [P248]; its excess is the sum of
    # (deg - 2) over the levels it appears at, not (total degree - 2).
    exc = collections.Counter()
    for ell, dd in deg.items():
        for P, g in dd.items():
            exc[P] += g - 2
    sig = collections.Counter()
    meas = collections.defaultdict(collections.Counter)
    for P, dg in exc.items():
        on = []
        for M in Ms:
            h = [abs(sum(M[r][z] * P[z] for z in range(3))) for r in range(3)]
            if all(v <= 1 for v in h) and any(v == 1 for v in h):
                on.append(sum(1 for v in h if v == 1))
        k = tuple(sorted(on))
        sig[k] += 1
        meas[k][dg] += 1
    return sig, meas


def identity(qs):
    """TOTAL from the engine, TOTAL from [P328]'s identity, and the pieces.

    Two predictions are reported: `predicted_table` uses [P328]'s per-signature constants,
    `predicted_measured` uses the measured degrees.  The second is exact by construction; the
    first is the claim under test.
    """
    sig, meas = vertices(qs)
    exc_t = sum(EXCESS[k] * v for k, v in sig.items() if k in EXCESS)
    unknown = {str(k): v for k, v in sig.items() if k not in EXCESS}
    exc_m = sum(e * c for k in meas for e, c in meas[k].items())
    off = {str(k): {str(e): c for e, c in sorted(v.items())}
           for k, v in meas.items() if set(v) != {EXCESS.get(k)}}
    g = level_graph(qs)
    L = len(g)
    holes = sum(v['c'] for v in g.values())
    by = engine(qs).get('by_depth') or {}
    total = sum(v for k, v in by.items() if k != '0')
    # region-weighted edge-edge count: (2,2) vertices that actually carry excess
    ee_star = sum(c for e, c in meas.get((2, 2), {}).items() if e > 0)
    return {'sig': {str(k): v for k, v in sorted(sig.items())}, 'EE': sig.get((2, 2), 0),
            'EE_carrying_excess': ee_star,
            'levels': L, 'holes': holes,
            'half_excess_table': exc_t // 2, 'half_excess_measured': exc_m // 2,
            'predicted_table': 1 + L + holes + exc_t // 2,
            'predicted_measured': 1 + L + holes + exc_m // 2,
            'engine_total': total,
            'identity_holds': 1 + L + holes + exc_t // 2 == total,
            'measured_identity_holds': 1 + L + holes + exc_m // 2 == total,
            'signatures_off_table': off, 'unscored_signatures': unknown}


def corner_incidences(q):
    """the 9-per-shared-corner incidences that [P329]'s counter added to the (2,2) vertices."""
    sig, _ = vertices([(1, 0, 0, 0), q])
    return sig.get((3, 3), 0), sig.get((2, 2), 0), sig.get((2, 2), 0) + 9 * sig.get((3, 3), 0)


def per_pair_census(hi=6):
    cands = [(w, x, y, z) for w in range(hi + 1) for x in range(hi + 1)
             for y in range(hi + 1) for z in range(hi + 1)
             if (w, x, y, z) != (0, 0, 0, 0) and gcd(gcd(w, x), gcd(y, z)) == 1]
    hist = collections.Counter()
    best = (0, None)
    argmax = []
    tested = 0
    for q in cands:
        if shares_plane([(1, 0, 0, 0), q]):
            continue
        tested += 1
        ee = vertices([(1, 0, 0, 0), q])[0].get((2, 2), 0)
        hist[ee] += 1
        if ee > best[0]:
            best = (ee, q); argmax = [q]
        elif ee == best[0]:
            argmax.append(q)
    return tested, len(cands), hist, best, argmax


# every cube rotated about the SAME face diagonal (1,1,0): every pairwise rotation stays in the
# family, which is what makes the total add up instead of trading off.
COMMON_AXIS = [(3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0), (5, 3, 3, 0), (6, 5, 5, 0),
               (5, 2, 2, 0), (7, 5, 5, 0)]


def n2_census(hi=4):
    """(EE, regions) for every admissible pair -- because max(2) = 13 is PROVED, so at n = 2 the
    bound can be tested against configurations that are known maximisers rather than merely
    found ones."""
    tab = collections.Counter()
    for w in range(hi + 1):
        for x in range(hi + 1):
            for y in range(hi + 1):
                for z in range(hi + 1):
                    q = (w, x, y, z)
                    if q == (0, 0, 0, 0) or gcd(gcd(w, x), gcd(y, z)) != 1:
                        continue
                    qs = [(1, 0, 0, 0), q]
                    if shares_plane(qs):
                        continue
                    ee = vertices(qs)[0].get((2, 2), 0)
                    by = engine(qs).get('by_depth') or {}
                    tab[(ee, sum(v for k, v in by.items() if k != '0'))] += 1
    return tab


def main():
    out = {'what': 'EE means two different things, and sum EE <= 6*C(n,2) is false',
           'question': 'OPEN_QUESTIONS 35', 'corrects': 'LEDGER P329'}

    print('G0 ORACLE -- [P328] identity on the records')
    out['oracle'] = []
    for n in (4, 5, 6):
        r = identity([tuple(q) for q in W.REC[n]])
        out['oracle'].append(dict(r, n=n))
        print('   n=%d  EE=%3d  1+L+holes=%2d  half-excess %4d/%4d (table/measured)'
              '  predicted=%4d  engine=%4d  %s'
              % (n, r['EE'], 1 + r['levels'] + r['holes'], r['half_excess_table'],
                 r['half_excess_measured'], r['predicted_table'], r['engine_total'],
                 'OK' if r['identity_holds'] else 'FAIL'), flush=True)
        if r['unscored_signatures']:
            print('      unscored signatures:', r['unscored_signatures'])
        if r['signatures_off_table']:
            print('      signatures whose measured excess is not the tabulated constant:',
                  r['signatures_off_table'])

    print('\nG1 -- what [P329] actually counted at q=(0,1,1,1)')
    sc, ee, inc = corner_incidences((0, 1, 1, 1))
    out['p329_witness'] = {'q': [0, 1, 1, 1], 'shared_corner_vertices': sc,
                           'ee_vertices': ee, 'edge_pair_incidences': ee + 9 * sc,
                           'p329_reported': 24, 'explains': ee + 9 * sc == 24}
    print('   (3,3) shared-corner vertices: %d   (2,2) edge-edge vertices: %d'
          '   -> %d + 9*%d = %d incidences, [P329] reported 24  %s'
          % (sc, ee, ee, sc, ee + 9 * sc, 'EXPLAINED' if ee + 9 * sc == 24 else 'UNEXPLAINED'))

    print('\nG2 -- per-pair (2,2) census, coprime integer quaternions with entries 0..6')
    tested, allc, hist, best, argmax = per_pair_census()
    out['per_pair'] = {'tested': tested, 'candidates': allc,
                       'distribution': {str(k): v for k, v in sorted(hist.items())},
                       'max': best[0], 'argmax_count': len(argmax),
                       'argmax_examples': [list(q) for q in argmax[:8]]}
    print('   tested %d of %d   distribution %s' % (tested, allc, dict(sorted(hist.items()))))
    print('   MAX per-pair EE = %d, attained by %d quaternions, e.g. %s'
          % (best[0], len(argmax), best[1]))

    print('\nG3 -- the total bound, on the common-face-diagonal family')
    out['total_bound'] = []
    for k in (2, 3, 4, 5, 6):
        bound = 6 * k * (k - 1) // 2
        bst = None
        for combo in itertools.combinations(COMMON_AXIS, k - 1):
            qs = [(1, 0, 0, 0)] + list(combo)
            if shares_plane(qs):
                continue
            r = identity(qs)
            if bst is None or r['EE'] > bst[0]['EE']:
                bst = (r, qs)
        r, qs = bst
        row = dict(r, n=k, bound=bound, exceeds=r['EE'] > bound,
                   quats=[list(q) for q in qs])
        out['total_bound'].append(row)
        print('   n=%d  bound 6*C(n,2)=%2d   total EE %2d %s   EE carrying excess %2d %s'
              % (k, bound, r['EE'], 'EXCEEDS' if r['EE'] > bound else 'within',
                 r['EE_carrying_excess'],
                 'EXCEEDS' if r['EE_carrying_excess'] > bound else 'within'))
        print('        %s   count %s   identity: table %s, measured %s'
              % (';'.join(','.join(map(str, q)) for q in qs), r['engine_total'],
                 'OK' if r['identity_holds'] else 'FAIL',
                 'OK' if r['measured_identity_holds'] else 'FAIL'))
        if r['signatures_off_table'] or r['unscored_signatures']:
            print('        off-table: %s   unscored: %s'
                  % (r['signatures_off_table'], r['unscored_signatures']))

    print('\nG4 -- n = 2, where the maximum 13 is PROVED: does the bound fail at MAXIMISERS?')
    tab = n2_census()
    out['n2_census'] = {'%d,%d' % k: v for k, v in sorted(tab.items())}
    for (ee, tot), c in sorted(tab.items()):
        print('   EE=%2d  regions=%2d   %d configurations%s'
              % (ee, tot, c, '   <- exceeds the bound 6, and is a MAXIMISER' if ee > 6 and tot == 13 else ''))

    out['reproduce'] = PROV.stamp(parameters={'quaternion_entry_range': '0..6', 'n2_census_range': '0..4',
                                              'common_axis_family': [list(q) for q in COMMON_AXIS]})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'ee_bound_refute.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/ee_bound_refute.json')


if __name__ == '__main__':
    main()
