#!/usr/bin/env python3
"""Do SIGNED real incidences order the counts, where raw ones do not?

Raw real-incidence counts differ in every same-signature pair but order them only 57% of
the time, because incidences both split and merge regions. Zaslavsky says how to sign
them: bounded regions are |chi(1)|, an alternating sum over the intersection lattice
weighted by the Moebius function.

For a point where m planes meet (otherwise generic), the local lattice gives
|mu| = (m-1)(m-2)/2. A generic configuration would instead have C(m,3) separate simple
vertices there, each with |mu| = 1. So the EXCESS carried by a degenerate point is

    w(m) = C(m,3) - (m-1)(m-2)/2        w(3)=0, w(4)=1, w(5)=4, w(9)=56

which is exactly zero for a generic vertex and grows with degeneracy. Three candidate
statistics are tested against the same pairs, cheapest first, so the simplest that works
wins rather than the most elaborate:

    A  real3 - realhigh        naive split-minus-merge
    B  -sum |mu| over real     total Moebius weight
    C  -sum w(m) over real     the excess over generic -- the principled one

Our regions are bounded by face SQUARES, so Zaslavsky does not apply to the whole
arrangement; the claim tested is only that the LOCAL contribution of a real incidence
follows it. That is why this is measured rather than asserted.
"""
import itertools, sys
from collections import defaultdict
from fractions import Fraction as F
sys.path.insert(0, '.')
from concurrence import planes, solve3
from realsig import cube_data, on_face

def real_mult_hist(cfg):
    """multiplicity histogram of the REAL (face-bounded) incidence points"""
    P = planes(cfg)
    cubes = cube_data(cfg)
    owner = [i // 6 for i in range(len(P))]
    pts = defaultdict(set)
    cnt = defaultdict(int)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None:
            continue
        pts[s].update((owner[i], owner[j], owner[k]))
        cnt[s] += 1
    hist = defaultdict(int)
    for p, owners in pts.items():
        if not all(on_face(p, cubes[o][0], cubes[o][1]) for o in owners):
            continue
        m = 3
        while m * (m - 1) * (m - 2) // 6 < cnt[p]:
            m += 1
        hist[m] += 1
    return dict(hist)

def C3(m):
    return m * (m - 1) * (m - 2) // 6

def stats(h):
    real3 = h.get(3, 0)
    high = sum(v for m, v in h.items() if m > 3)
    A = real3 - high
    B = -sum(v * ((m - 1) * (m - 2) // 2) for m, v in h.items())
    C = -sum(v * (C3(m) - (m - 1) * (m - 2) // 2) for m, v in h.items())
    return A, B, C

if __name__ == '__main__':
    import random
    from math import gcd
    from signature import signature, count
    from sharedaxis import q_axis
    from symmetrize import axes
    from haarsample import haar_config
    rng = random.Random(4); AX = axes(3)
    vals = [F(p, q) for q in (1,2,3,4,5,6) for p in range(-6,7) if p and gcd(abs(p), q) == 1]
    groups = defaultdict(list)
    for i in range(70):
        cfg = (haar_config(rng, 4, 64, chart=True) if i % 2 else
               [(1,0,0,0)] + [q_axis(rng.choice(AX), rng.choice(vals)) for _ in range(3)])
        c = count(cfg)
        if c:
            groups[signature(cfg)].append((c, cfg))
    ok = {'A': 0, 'B': 0, 'C': 0}; tie = {'A': 0, 'B': 0, 'C': 0}; n = 0
    shown = 0
    print('  count A/B     stat A        stat B          stat C (principled)')
    for sg, v in groups.items():
        if len(v) < 2:
            continue
        for (c1, f1), (c2, f2) in itertools.combinations(v, 2):
            if c1 == c2:
                continue
            s1 = stats(real_mult_hist(f1)); s2 = stats(real_mult_hist(f2))
            n += 1
            for idx, k in enumerate('ABC'):
                if s1[idx] == s2[idx]:
                    tie[k] += 1
                elif (s1[idx] > s2[idx]) == (c1 > c2):
                    ok[k] += 1
            if shown < 6:
                print('   %4d/%-4d  %5d/%-5d  %7d/%-7d  %8d/%-8d'
                      % (c1, c2, s1[0], s2[0], s1[1], s2[1], s1[2], s2[2]))
                shown += 1
            if n >= 30:
                break
        if n >= 30:
            break
    print()
    for k in 'ABC':
        eff = n - tie[k]
        print('  stat %s: orders %2d of %2d non-tied (%.0f%%)   [%d ties]'
              % (k, ok[k], eff, 100.0 * ok[k] / max(eff, 1), tie[k]))
    print('  baseline 50%; raw real-incidence count scored 57%')
