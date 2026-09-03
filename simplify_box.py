#!/usr/bin/env python3
"""A cheaper REPRESENTATIVE of the same chamber, per-coordinate.

`climb.simplify_point` searches dyadic roundings: every coordinate is forced onto the
same denominator 2^k, and k has to be large enough for the TIGHTEST coordinate. One
narrow direction therefore sets the height of all 3(n-1) of them, and the height is what
ends the climb -- the engines refuse above ~2^28.5 of probe height and no step-size
change avoids it (M = 4096, 256 and 16 all refuse identically).

The chamber is a product of intervals in no particular basis, but it is open, so each
coordinate has its own slack. Measuring that slack one coordinate at a time and taking
the simplest rational inside EACH interval separately gives every coordinate its own
denominator. Nothing here is new machinery: `simplest_between` is the same routine the
endpoint solver uses, and the anchor is the count itself, so a wrong guess is rejected
rather than trusted.

This is the "lower precision path" question asked at one point rather than along a path:
if the same chamber has a much cheaper representative, the climb never needed the
expensive one, and the engine ceiling was never the binding constraint there.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, '.')
import climb as C
from simplest import simplest_between

def _count_with(pt, i, val, q0):
    p = list(pt); p[i] = val
    return C.cnt(C.cfg_at(p, q0))

def slack(pt, i, c, q0, sign, start=F(1, 1024), cap=64):
    """how far coordinate i can move in `sign` before the count changes"""
    step = start
    good = F(0)
    while step <= cap:
        if _count_with(pt, i, pt[i] + sign * step, q0) == c:
            good = step; step *= 2
        else:
            break
    lo, hi = good, step
    for _ in range(24):                      # bisect the boundary
        mid = (lo + hi) / 2
        if _count_with(pt, i, pt[i] + sign * mid, q0) == c:
            lo = mid
        else:
            hi = mid
    return lo

def simplify_box(pt, c, q0, ncols, rounds=2, verbose=False):
    pt = list(pt)
    for r in range(rounds):
        for i in range(ncols):
            dn = slack(pt, i, c, q0, -1)
            up = slack(pt, i, c, q0, +1)
            if up == 0 and dn == 0:
                continue
            s = simplest_between(pt[i] - dn, pt[i] + up)
            if _count_with(pt, i, s, q0) == c:
                pt[i] = s
        if verbose:
            h = max(abs(x) for q in C.cfg_at(pt, q0) for x in q)
            print('   round %d: height %d' % (r + 1, h), flush=True)
    return pt

if __name__ == '__main__':
    import json, glob
    import dimension as D
    rows = []
    for f in glob.glob('basin_n*_d*_s*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            if d.get('end') is None:
                rows.append(d)
    print('%d configurations that ENDED a climb by engine refusal\n' % len(rows))
    for d in rows[:int(sys.argv[1]) if len(sys.argv) > 1 else 3]:
        cfg = [tuple(q) for q in d['cfg1']]
        n = len(cfg); ncols = 3 * (n - 1)
        D.set_field(0); D.QZERO[:] = [cfg[0]]
        pt = D.point_of(cfg)
        c = C.cnt(cfg) or C.cnt(cfg)
        h0 = max(abs(x) for q in cfg for x in q)
        print('n=%d  count %s  dyadic representative height %d' % (n, c, h0), flush=True)
        pt2 = simplify_box(pt, c, cfg[0], ncols, rounds=2, verbose=True)
        cf2 = C.cfg_at(pt2, cfg[0]); h1 = max(abs(x) for q in cf2 for x in q)
        ok = C.cnt(cf2)
        print('   -> per-coordinate height %d  (%.0fx smaller)  count %s %s'
              % (h1, h0 / max(h1, 1), ok, 'OK' if ok == c else 'COUNT CHANGED -- rejected'))
        print('   bits needed for a probe: %.0f -> %.0f  (engines have 112 / 240)\n'
              % (C.required_bits(h0 * h0 * C.M), C.required_bits(h1 * h1 * C.M)), flush=True)
