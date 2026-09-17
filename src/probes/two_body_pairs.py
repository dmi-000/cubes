#!/usr/bin/env python3
"""Where the gap actually is: two-body PER PAIR, and why shared corners merge.  [P333].

`EE + 2*SC2` IS the two-body term of [P258], and `two-body <= 10*C(n,2)` is PROVED ([P237]).
So [OQ 35]'s premise -- that the degenerate terms are the ones nothing bounds -- is wrong for
the two-cube ones, and the edge-edge thread ([P329], [P330]) was re-bounding a bounded quantity
while capping only half of the sum.

A pair sits at `two-body = 10` exactly when it is a 2-cube maximiser (`max(2) = 13`, proved),
and there are two routes -- EE = 10 with no shared corner, or EE = 6 with one.  In the records
only a HUB cube reaches the cap, with every other cube, using a DISTINCT antipodal corner-pair
each time.  Concentrating the sharings on one axis merges them into a single n-fold vertex and
loses the rest, which is the frustration mechanism operating inside the two-body term.
"""
import sys, os, json, itertools, collections
from math import comb
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import shares_plane, engine
import ee_bound_refute as B
import wall_keys as W
import provenance as PROV

# every cube rotated about ONE common body diagonal: [P44] says every PAIR counts 13
BODY_DIAGONAL = [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2), (4, 1, 1, 1)]


def terms(qs):
    """T3, two-body, holes and the engine count, with the signature census behind them."""
    n = len(qs)
    sig, _ = B.vertices(qs)
    EE = sig.get((2, 2), 0)
    SC2 = sig.get((3, 3), 0)
    by = engine(qs).get('by_depth') or {}
    return {'sig': {str(k): v for k, v in sorted(sig.items())},
            'T3': sig.get((1, 1, 1), 0), 'T3_cap': 32 * comb(n, 3),
            'two_body': EE + 2 * SC2, 'two_body_cap': 10 * comb(n, 2),
            'EE': EE, 'SC2': SC2,
            'count': sum(v for k, v in by.items() if k != '0'),
            'bound': 1 + 32 * comb(n, 3) + 10 * comb(n, 2) + 3 * (n - 1)}


def per_pair(qs):
    """each pair IN ISOLATION: two-body and the pair's own region count (13 = max(2))."""
    out = []
    for i, j in itertools.combinations(range(len(qs)), 2):
        t = terms([qs[i], qs[j]])
        out.append({'pair': [i, j], 'EE': t['EE'], 'SC2': t['SC2'],
                    'two_body': t['two_body'], 'at_cap': t['two_body'] == 10,
                    'pair_count': t['count']})
    return out


def shared_corners(qs):
    """which cube PAIRS share which corner POINTS -- the (3,3) vertices, located."""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    pts = set()
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a < b:
                    for t in (a, b):
                        pts.add(tuple(p[z] + t * d[z] for z in range(3)))
    found = []
    for P in sorted(pts):
        on = []
        for idx, M in enumerate(Ms):
            h = [abs(sum(M[r][z] * P[z] for z in range(3))) for r in range(3)]
            if all(v <= 1 for v in h) and any(v == 1 for v in h):
                on.append((idx, sum(1 for v in h if v == 1)))
        if len(on) >= 2 and all(c == 3 for _, c in on):
            found.append({'cubes': [i for i, _ in on], 'corner': [str(v) for v in P]})
    return found


def main():
    out = {'what': 'the two-body term per pair, the hub, and why shared corners merge',
           'question': 'OPEN_QUESTIONS 35', 'supports': 'LEDGER P333', 'records': {},
           'body_diagonal_family': {}}

    print('=== the gap, term by term ===')
    for n in (4, 5):
        qs = [tuple(q) for q in W.REC[n]]
        t = terms(qs)
        pp = per_pair(qs)
        sc = shared_corners(qs)
        deg = collections.Counter()
        for s in sc:
            for c in s['cubes']:
                deg[c] += 1
        out['records'][n] = dict(t, per_pair=pp, shared_corners=sc,
                                 shared_corners_per_cube={str(k): v for k, v in sorted(deg.items())},
                                 antipodal_pairs_used={str(k): v // 2 for k, v in sorted(deg.items())})
        print('n=%d record  T3 %d/%d (%s)  two-body %d/%d (short %d)  count %d  bound %d'
              % (n, t['T3'], t['T3_cap'], 'AT CAP' if t['T3'] == t['T3_cap'] else 'below',
                 t['two_body'], t['two_body_cap'], t['two_body_cap'] - t['two_body'],
                 t['count'], t['bound']))
        atcap = [p['pair'] for p in pp if p['at_cap']]
        print('    pairs at the two-body cap: %d of %d   %s'
              % (len(atcap), len(pp), atcap))
        print('    shared CORNERS per cube: %s  -> antipodal pairs used: %s  (4 available)'
              % (dict(sorted(deg.items())),
                 {k: v // 2 for k, v in sorted(deg.items())}))

    print('\n=== why one common axis does NOT work: the sharings merge ===')
    for n in (4,):
        qs = BODY_DIAGONAL[:n]
        if shares_plane(qs):
            continue
        t = terms(qs)
        out['body_diagonal_family'][n] = t
        print('body-diagonal n=%d  T3 %d/%d  two-body %d/%d  count %d'
              % (n, t['T3'], t['T3_cap'], t['two_body'], t['two_body_cap'], t['count']))
        print('    signatures %s' % t['sig'])
        print('    -> all %d cubes share the SAME two corners (the axis endpoints), so the'
              % n)
        print('       pairwise sharings collapse into ONE %d-fold vertex.' % n)

    print('\n=== the combinatorial cap on corner sharing ===')
    print('    a cube has 4 antipodal corner-pairs, and two partners cannot use the same one,')
    print('    so the corner-sharing graph has max degree 4: at most 2n of C(n,2) pairs.')
    print('      n        4     5     6     7')
    print('      C(n,2)   6    10    15    21')
    print('      2n       8    10    12    14     complete only for n <= 5')
    out['corner_cap'] = {str(n): {'pairs': comb(n, 2), 'max_sharing_pairs': 2 * n,
                                  'complete_possible': 2 * n >= comb(n, 2)}
                         for n in (4, 5, 6, 7)}

    out['reproduce'] = PROV.stamp(parameters={'records': [4, 5],
                                              'body_diagonal': [list(q) for q in BODY_DIAGONAL]})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'two_body_pairs.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/two_body_pairs.json')


if __name__ == '__main__':
    main()
