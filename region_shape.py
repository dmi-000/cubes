#!/usr/bin/env python3
"""Characterise the uniform 55 region that contains the two n=3 maxima.

Zero signal means a uniform region, and a region has boundaries and a shape.
The count is 55 at every rational approach to the octahedral 67 (twelve orders
of magnitude, climb_limit.py), so 67 is a PUNCTURE in a uniform region rather
than a peak on a slope.  This locates the region's edges in the dihedral
family and measures where each maximum sits inside it.
"""
import math
from q3_count import count_triple

def tri(rmax):
    out = set()
    for m in range(2, 300):
        for n in range(1, m):
            if (m-n) % 2 == 1 and math.gcd(m, n) == 1:
                a, b, c = m*m-n*n, 2*m*n, m*m+n*n
                for k in range(1, rmax//c + 1):
                    out.add((a*k, b*k, c*k)); out.add((b*k, a*k, c*k))
    return out
T = tri(4000)
def near(target, lo, hi, k):
    cand = sorted(T, key=lambda t: abs(math.degrees(math.asin(t[0]/t[2])) - target))
    sel = []
    for p, q, r in cand:
        psi = math.degrees(math.asin(p/r))
        if lo < psi < hi and all(abs(psi - math.degrees(math.asin(s[0]/s[2]))) > 1e-3
                                 for s in sel):
            sel.append((p, q, r))
        if len(sel) >= k: break
    return sorted(sel, key=lambda t: math.asin(t[0]/t[2]))

OCT, GOLD = 35.26438968, 69.09484255
print('the 55 region of the dihedral family, and where the two 67s sit in it\n')
for name, lo, hi in (('LOWER edge', 21.0, 24.5), ('UPPER edge', 67.5, 71.5)):
    print('%s:' % name)
    for p, q, r in near((lo+hi)/2, lo, hi, 9):
        psi = math.degrees(math.asin(p/r))
        t, _ = count_triple(p, q, r)
        mark = ''
        if abs(psi-OCT) < .2: mark = '   <- octahedral 67 is at 35.264'
        if abs(psi-GOLD) < .2: mark = '   <- GOLDEN 67 is at 69.095'
        print('   psi=%9.5f  (%d,%d,%d)  count %d%s' % (psi, p, q, r, t, mark))
    print()
print('octahedral 67 at %.5f, golden 67 at %.5f' % (OCT, GOLD))
