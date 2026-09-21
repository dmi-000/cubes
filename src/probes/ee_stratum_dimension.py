#!/usr/bin/env python3
"""[OQ 39] The DIMENSION of the high-`EE` locus — what really limits `EE` at `B = 128`.

Two ceilings on `EE` at `B = 128` have now been certified by directed searches and refuted
([P373]).  The per-subset route cannot help: `max(3) = 67` gives `sum E_i + E_S <= 62`, so at
`E_S = 32` a triple has `sum EE_i <= 30` PROVED, and summing over the four triples of an n = 4
compound (each pair in two of them) returns `EE <= 60` — exactly the box bound already known.

So the binding constraint is not per-subset.  It is how many PAIRS can sit on a high-`EE`
stratum at once, and that is a question about the stratum's DIMENSION: the six relative
rotations of a 4-compound are determined by three free rotations (9 parameters), so requiring
`k` pairs at `EE >= 8` imposes `k * codim` conditions on 9.

**Dimension is measurable without any sampling of maxima.**  `EE` is constant on strata cut out
by [P366]'s 144 quartics, all defined over `Q`.  Counting integer quaternions of height `<= H`
on a stratum grows like `H^(d+1)` for a `d`-dimensional stratum, so the growth exponent gives
the dimension.  Every count here is exact: `EE` comes from the exact edge oracle.

**RESULT: INCONCLUSIVE, and the reason is worth keeping.**  `EE = 0` is the generic value --
95 % of quaternions at height 400 -- yet it does not occur AT ALL for primitive quaternions of
height <= 4, and is 11 % at height 6.  The whole census sits inside a transient where low height
makes every rotation special, so no exponent here is asymptotic.  This is the representative-cost
trap of [METHODS] in the place it is hardest to see: the instrument is fine, the INPUTS were all
special, and a larger census would cost H^4.  The codimensions are obtained exactly instead, by
Jacobian rank, in `ee_jacobian_rank.py`.
"""
import sys, os, json, itertools, collections
from math import gcd, log

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_determinantal as D
from c_level import shares_plane
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def census(H):
    """exact EE for every primitive quaternion of height <= H, one per antipodal pair"""
    c = collections.Counter()
    deg = 0
    for q in itertools.product(range(-H, H + 1), repeat=4):
        if not any(q):
            continue
        g = 0
        for v in q:
            g = gcd(g, abs(v))
        if g != 1:
            continue
        neg = False
        for v in q:
            if v:
                neg = v < 0
                break
        if neg:
            continue
        if shares_plane([(1, 0, 0, 0), q]):
            deg += 1              # degenerate pairs are excluded project-wide, and COUNTED
            continue
        c[D.ee_exact(q)] += 1
    return c, deg


def main():
    out = {'what': 'dimension of the high-EE strata by point-count growth',
           'supports': 'OQ 39', 'by_height': {}}
    Hs = [2, 3, 4, 5, 6]
    rows = {}
    for H in Hs:
        c, deg = census(H)
        rows[H] = c
        tot = sum(c.values())
        print('   H = %d   primitive non-degenerate: %5d   degenerate skipped: %4d   %s'
              % (H, tot, deg, dict(sorted(c.items()))), flush=True)
        out['by_height'][str(H)] = {'total': tot, 'degenerate': deg,
                                    'dist': {str(k): v for k, v in sorted(c.items())}}

    print('\n   GROWTH EXPONENT between consecutive heights  (log ratio / log height ratio)')
    print('   EE value :  ' + '  '.join('%d->%d' % (Hs[i], Hs[i + 1]) for i in range(len(Hs) - 1)))
    vals = sorted({v for c in rows.values() for v in c})
    expo = {}
    for v in vals:
        cells = []
        for i in range(len(Hs) - 1):
            a, b = rows[Hs[i]].get(v, 0), rows[Hs[i + 1]].get(v, 0)
            cells.append('%5.2f' % (log(b / a) / log(Hs[i + 1] / Hs[i]))
                         if a and b else '    -')
        expo[v] = cells
        print('   EE = %2d  :  ' % v + '  '.join(cells))
    out['growth_exponents'] = {str(k): v for k, v in expo.items()}

    print('\n   READ IT AS: primitive integer quaternions of height <= H number ~H^4, so a')
    print('   stratum of DIMENSION d (in the 3-sphere) contributes ~H^(d+1): exponent 4 is the')
    print('   full sphere, 3 a surface, 2 a curve, 1 isolated points.')
    print('   *** AND THIS CENSUS DOES NOT REACH THE ASYMPTOTIC REGIME. ***  EE = 0 -- the')
    print('   generic value, 95% of quaternions at height 400 -- does not appear AT ALL below')
    print('   H = 5, and is still only 11% at H = 6.  Every exponent here is measured inside')
    print('   the transient where low height makes every rotation special, so they are')
    print('   reported and NOT interpreted.  The exact codimensions come from Jacobian rank')
    print('   instead: src/probes/ee_jacobian_rank.py.')

    out['reproduce'] = PROV.stamp(
        parameters={'heights': Hs},
        note='EE from the exact edge oracle; counts are of primitive quaternions, one per '
             'antipodal pair, degenerate (shared face plane) excluded and counted')
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_stratum_dimension.json'), 'w'), indent=1)
    print('\nwrote data/ee_stratum_dimension.json', flush=True)


if __name__ == '__main__':
    main()
