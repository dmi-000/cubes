#!/usr/bin/env python3
"""The last unsolved end of the tower: n=8's 1895 LOWER end, a W3 quartic.

`n78_ends.py` (2026-08-08) solved both 1217 ends and 1895's UPPER end, all W4 roots
of quadratics, hence in Q(sqrt d) and countable exactly. It left 1895's lower end as
"a W3 quartic, out of reach": a quartic root is degree 4 and the engine takes only
Q(sqrt d).

Out of reach is not necessarily irreducible. This finds the quartic that produces the
end and FACTORS it over Q. If it splits into quadratics the root is in Q(sqrt d)
after all and the endpoint can be counted exactly; if it is irreducible the end is
still LOCATED exactly as an algebraic number, and the counts immediately inside and
outside are still decidable, which is what open/closed needs.

`w3_params` returns roots and discards the polynomial, so the quartic is rebuilt here
alongside its roots.
"""
import os, sys, json, subprocess
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from catcache import catalogue
from wall_params import line_polys, padd, psub, pscale, det3_poly, real_roots
from n78_ends import w4_polys
from solve_more_ends import exact_roots, approx, simplest_between

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C7 = BASE + [(7,14,1,-5),(4,-3,-4,-4)]
a0 = [F(-1), F(1), F(-61,24)]
dv = [F(0), F(0), F(1)]
TARGET = 1895


def q_of(s):
    c = [a0[i] + s*dv[i] for i in range(3)]
    L = 1
    for v in c: L = L*v.denominator//gcd(L, v.denominator)
    iq = [L] + [int(v*L) for v in c]; g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)


def cnt(s):
    cfg = C7 + [q_of(s)]
    st = ";".join(",".join(map(str, q)) for q in cfg)
    m = max(abs(v) for q in cfg for v in q)
    cmd = (['./cube_regions_n','--quats',st] if m <= 512
           else ['./cube_regions_q2w','--d','0','--quats',st])
    try: return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)['bounded']
    except Exception: return None


def w3_polys_and_roots(a0, dv, lines):
    """like wall_params.w3_params but KEEPS the quartic beside each root"""
    M, N = line_polys(a0, dv)
    edges = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                P = [padd(pscale(M[i][b], F(sb)), pscale(M[i][c], F(sc)),
                          pscale(M[i][a], F(-1))) for i in range(3)]
                Dd = [pscale(M[i][a], F(2)) for i in range(3)]
                edges.append((Dd, P))
    out = []
    for p0, d2, ca, cb in lines:
        d2p = [[F(x)] for x in d2]
        for Dd, P in edges:
            w = [psub(pscale(N, F(p0[i])), P[i]) for i in range(3)]
            poly = det3_poly(Dd, d2p, w)
            for r in real_roots(poly):
                out.append((r, poly))
    return out


print('gate: the record must be 1895 at s=0 ->', cnt(F(0)), flush=True)
assert cnt(F(0)) == TARGET

pts, lines = catalogue(C7)
w4 = []
for p in w4_polys(a0, dv, pts):
    for r in exact_roots(p):
        w4.append((approx(r), ('W4', r, p)))
w3 = [(F(r).limit_denominator(10**12) if not isinstance(r, F) else r, ('W3', None, poly))
      for r, poly in w3_polys_and_roots(a0, dv, lines)]
allr = sorted([x for x in w4 + w3 if x[0] < 0], key=lambda t: -t[0])
print('%d W4 + %d W3 crossings on the line; %d below the record'
      % (len(w4), len(w3), len(allr)), flush=True)

prev, prev_item = F(0), None
end = None
for v, item in allr:
    if v == prev: continue
    c = cnt(simplest_between(v, prev))
    if c is None:
        print('   UNEVALUATED probe — stopping, not scored as a change'); break
    if c != TARGET:
        end = prev_item; break
    prev, prev_item = v, (v, item)
    print('   still %d down to s = %.9f (%s)' % (TARGET, float(v), item[0]), flush=True)

if end is None:
    print('no transition found below the record within the enumerated crossings')
else:
    (v, (kind, r, poly)) = end
    print('\nLOWER END is a %s crossing at s = %.12f' % (kind, float(v)), flush=True)
    x = sp.Symbol('x')
    P = sp.Poly(sum(sp.Rational(c) * x**i for i, c in enumerate(poly)), x)
    fac = sp.factor_list(P.as_expr())
    print('   its polynomial has degree %d; factorisation over Q:' % P.degree(), flush=True)
    for f, m in fac[1]:
        print('      (%s)^%d' % (sp.expand(f), m), flush=True)
    degs = sorted(sp.Poly(f, x).degree() for f, m in fac[1] if sp.Poly(f, x).degree() > 0)
    print('   irreducible factor degrees: %s -> %s' % (degs,
          'reachable in Q(sqrt d)' if all(d <= 2 for d in degs)
          else 'genuinely degree >2: located exactly, but not countable AT the end'), flush=True)
