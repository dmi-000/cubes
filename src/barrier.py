#!/usr/bin/env python3
"""How DEEP are the valleys between local maxima? — the number that decides annealing.

Separation says how far apart two maxima are; the barrier says how far DOWN you must go
to get from one to the other, and that is what a downhill step budget actually has to
pay. A walk that allows k non-improving moves can only cross a valley that costs fewer
than k of them.

METHOD, and its direction of error. Both configurations are put in a common gauge (cube 0
= identity), each of B's cubes is replaced by the octahedral image nearest A's
corresponding cube (a cube is invariant under those 24 rotations, so this changes nothing
about the compound and everything about the interpolation), and the straight Cayley
segment between them is counted at exact rational points.

  * A particular path gives an UPPER bound on the true barrier: some other path may be
    shallower.
  * Sampling a path gives a LOWER bound on that path's depth: the segment could dip
    between samples.

So the number reported is neither bound in isolation, and is labelled as what it is: the
deepest dip SEEN on the straight path. If it is already large, annealing across that
valley is hopeless; if it is small, annealing is worth trying and the true barrier could
be smaller still.
"""
import json, glob, math, sys
from fractions import Fraction as F
sys.path.insert(0, '.')
import dimension as D
import climb as C
from maxima_spacing import qmul, qconj, canon, OCT, gauge

def align(A, B):
    """B in A's gauge, each cube replaced by its octahedral image nearest A's"""
    A, B = gauge(A), gauge(B)
    out = [A[0]]
    for a, b in zip(A[1:], B[1:]):
        na = math.sqrt(sum(v * v for v in a))
        best, bq = -1, None
        for s in OCT:
            r = canon(qmul(b, s))
            nr = math.sqrt(sum(v * v for v in r))
            c = abs(sum(x * y for x, y in zip(a, r))) / (na * nr)
            if c > best:
                best, bq = c, r
        out.append(bq)
    return A, out

def profile(A, B, steps=48):
    A, B = align(A, B)
    D.set_field(0); D.QZERO[:] = [A[0]]
    pa, pb = D.point_of(A), D.point_of(B)
    if pa is None or pb is None:
        return None
    out = []
    for k in range(steps + 1):
        t = F(k, steps)
        p = [pa[i] + t * (pb[i] - pa[i]) for i in range(len(pa))]
        cf = C.cfg_at(p, A[0])
        out.append(C.cnt(cf))
    return out

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    npair = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    seen, cfgs = set(), []
    for f in glob.glob('basin_n*_d*_s*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            if len(d['cfg0']) != n:
                continue
            c = d.get('end') if d.get('end') is not None else d.get('best_evaluable')
            key = tuple(map(tuple, d['cfg1']))
            if c is None or key in seen:
                continue
            seen.add(key); cfgs.append((c, [tuple(q) for q in d['cfg1']]))
    cfgs.sort(key=lambda t: -t[0])
    print('n=%d: %d local maxima; pairing the highest ones' % (n, len(cfgs)), flush=True)
    print('%6s %6s %8s %8s %8s   %s' % ('A', 'B', 'min seen', 'drop A', 'drop B', 'unevaluable'))
    drops = []
    for i in range(min(npair, len(cfgs))):
        for j in range(i + 1, min(i + 3, len(cfgs))):
            pr = profile(cfgs[i][1], cfgs[j][1])
            if pr is None:
                continue
            ok = [v for v in pr if v is not None]
            if not ok:
                continue
            lo = min(ok)
            print('%6d %6d %8d %8d %8d   %d of %d'
                  % (cfgs[i][0], cfgs[j][0], lo, cfgs[i][0] - lo, cfgs[j][0] - lo,
                     len(pr) - len(ok), len(pr)), flush=True)
            drops.append(min(cfgs[i][0], cfgs[j][0]) - lo)
    if drops:
        drops.sort()
        print('\nbarrier depth seen on the straight path, in REGIONS:')
        print('   min %d   median %d   max %d   (over %d pairs)'
              % (drops[0], drops[len(drops)//2], drops[-1], len(drops)))
        print('   a walk allowing k downhill MOVES crosses a valley only if the dip costs')
        print('   fewer than k of them; each move here changes the count by a multiple of 4.')
