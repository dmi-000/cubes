#!/usr/bin/env python3
"""SOLVE the plateau ends, rather than bisecting for them.

An end of a constant-count interval is a root of a wall equation restricted to
the line the interval lives on, so it is found by one polynomial solve.  The
existing solver (wall_params) is hard-wired to the FIVE-cube 393 base through
incidence2.base_catalogue; the n=7 and n=8 plateaux sit on 6- and 7-cube bases,
so the catalogue is rebuilt here for an arbitrary base.
"""
import collections, itertools, json, subprocess, sys
from fractions import Fraction as F

sys.path.insert(0, "/Users/dmi/cube-compounds")
from base_points import mat, planes, solve3
import wall_params as W

def catalogue(cubes, bound=4):
    """(real triple points, crossing lines) for an arbitrary base."""
    P = planes(cubes)
    mats = [mat(q) for q in cubes]
    trans = [[[M[k][i] for k in range(3)] for i in range(3)] for M in mats]

    def in_cube(pt, Minv):
        v = [sum(Minv[i][k]*pt[k] for k in range(3)) for i in range(3)]
        return max(abs(x) for x in v) <= 1

    pts = collections.defaultdict(set)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None or max(abs(x) for x in s) > bound:
            continue
        pts[s] |= {i, j, k}
    real_pts = []
    for s in pts:
        on = [t for t in range(len(P))
              if sum(P[t][0][u]*s[u] for u in range(3)) == P[t][1]]
        cubes_on = {P[t][2] for t in on}
        if all(in_cube(s, trans[c]) for c in cubes_on):
            real_pts.append((s, len(on), len(cubes_on)))

    lines = []
    for i, j in itertools.combinations(range(len(P)), 2):
        if P[i][2] == P[j][2]:
            continue
        n1, n2 = P[i][0], P[j][0]
        d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2],
             n1[0]*n2[1]-n1[1]*n2[0])
        if not any(d):
            continue
        k = max(range(3), key=lambda u: abs(d[u]))
        u1, u2 = [t for t in range(3) if t != k]
        det = n1[u1]*n2[u2] - n1[u2]*n2[u1]
        if det == 0:
            continue
        p0 = [F(0)]*3
        p0[u1] = (P[i][1]*n2[u2] - P[j][1]*n1[u2]) / det
        p0[u2] = (n1[u1]*P[j][1] - n2[u1]*P[i][1]) / det
        lines.append((tuple(p0), d, P[i][2], P[j][2]))
    return real_pts, lines

def q_of(c):
    from math import gcd
    L = 1
    for v in c: L = L*v.denominator//gcd(L, v.denominator)
    iq = [L]+[int(v*L) for v in c]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def count(cfg):
    s = ";".join(",".join(map(str, q)) for q in cfg)
    m = max(abs(v) for q in cfg for v in q)
    cmd = (["/Users/dmi/cube-compounds/cube_regions_n", "--quats", s] if m <= 512
           else ["/Users/dmi/cube-compounds/cube_regions_q2w", "--d", "0", "--quats", s])
    try:
        return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)["bounded"]
    except Exception:
        return None

def solve_end(base, a0, d, lo, hi, target, label):
    """the end of the target-count interval bracketed by (lo,hi), as a wall root"""
    pts, lines = catalogue(base)
    w4 = W.w4_params(a0, d, pts)
    w3 = W.w3_params(a0, d, lines)
    cands = sorted(set([('W4', s) for s in w4 if lo < s < hi] +
                       [('W3', s) for s in w3 if lo < s < hi]), key=lambda t: t[1])
    print('%s: base has %d triple points, %d crossing lines; '
          '%d W4 + %d W3 crossings on the line, %d inside (%s, %s)'
          % (label, len(pts), len(lines), len(w4), len(w3), len(cands),
             float(lo), float(hi)), flush=True)
    for kind, s in cands:
        eps = F(1, 10**7)
        below = count([q_of([a0[i]+(s-eps)*d[i] for i in range(3)])] and
                      base+[q_of([a0[i]+(s-eps)*d[i] for i in range(3)])])
        at = count(base+[q_of([a0[i]+s*d[i] for i in range(3)])])
        above = count(base+[q_of([a0[i]+(s+eps)*d[i] for i in range(3)])])
        flag = '  <== END' if (below == target) != (above == target) else ''
        print('   %s s = %.12f   count below/at/above: %s / %s / %s%s'
              % (kind, float(s), below, at, above, flag), flush=True)
    return cands

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

if __name__ == '__main__':
    which = sys.argv[1]
    if which == '8':
        base = BASE+[(7,14,1,-5),(4,-3,-4,-4)]
        a0 = [F(-1), F(1), F(-61,24)]; d = [F(0), F(0), F(1)]
        solve_end(base, a0, d, F(-1,8), F(-13,512), 1895, 'n=8 1895 lower end')
        solve_end(base, a0, d, F(51,512), F(13,128), 1895, 'n=8 1895 upper end')
    elif which == '7':
        base = BASE+[(7,14,1,-5)]
        a0 = [F(-3,4), F(-1), F(-1)]; d = [F(1), F(0), F(0)]
        solve_end(base, a0, d, F(-3,32), F(-11,256), 1217, 'n=7 1217 lower end')
        solve_end(base, a0, d, F(-1,256), F(1,256), 1217, 'n=7 1217 upper end')
