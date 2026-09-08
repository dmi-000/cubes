#!/usr/bin/env python3
"""Can a rational climb approach the irrational maximum in VALUE, not just in
position?

Rationals are dense, so a climb can get arbitrarily close to the octahedral 67
in configuration space.  The question is whether the COUNT converges to 67 as
it does so.  Postscript 65 says no -- 67 is a SPIKE, with 55 on both sides at
a quarter of a degree -- but that was measured along one family.  This walks
the continued-fraction convergents of sqrt2 - 1, which are the best rational
approximations that exist at each denominator, straight at the point.

If the count stays flat while the distance falls by orders of magnitude, then
no refinement schedule, however clever, converts a rational climb into the
irrational optimum: the target is invisible until you land exactly on it.
"""
import json, math, subprocess
# convergents of sqrt2 - 1 = [0;2,2,2,...]
conv, p, q, pp, qq = [], 0, 1, 1, 0
for _ in range(14):
    a = 2 if conv else 2
    p, pp = a*p + pp, p
    q, qq = a*q + qq, q
    conv.append((pp if False else p, q))
seen = set(); rows = []
for p, q in conv:
    if q in seen: continue
    seen.add(q)
    cfg = [(q, p, 0, 0), (q, 0, p, 0), (q, 0, 0, p)]
    s = ';'.join(','.join(map(str, c)) for c in cfg)
    out = subprocess.run(['./cube_regions_n', '--quats', s],
                         capture_output=True, text=True).stdout
    tot = json.loads(out).get('bounded') if out.startswith('{') else None
    err = abs(p/q - (math.sqrt(2)-1))
    rows.append((p, q, err, tot))
print('the octahedral 67 sits at Cayley coordinate sqrt2-1 = %.12f on each axis'
      % (math.sqrt(2)-1))
print('walking its best rational approximations straight at it:\n')
print('%-22s %-14s %s' % ('approximation p/q', 'distance', 'region count'))
for p, q, err, tot in rows:
    print('%-22s %-14.2e %s' % ('%d/%d' % (p, q), err, tot))
print('\nexact point (in Q(sqrt2)): 67')
