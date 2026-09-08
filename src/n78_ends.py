#!/usr/bin/env python3
"""Are the n = 7 and n = 8 continuum ends IN their level sets?  Closed or open?

Every other family in the table has been settled by evaluating the count AT the
endpoint.  These two could not be, because their bounds are irrational: the count
there needs a configuration with irrational Cayley coordinates, which the integer
engine cannot express.  A W4 bound is the root of a QUADRATIC in the line
parameter, so it lives in some Q(sqrt d) -- exactly what `cube_regions_q2w --d D`
takes.  (A W3 bound is a quartic root and stays out of reach; n = 8's lower end
is one of those.)

Recover the quadratic, extract d, build the endpoint exactly in Z[sqrt d], count.
"""
import json, os, subprocess, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solve_ends import catalogue
from wall_params import line_polys, padd, pscale

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

def squarefree(n):
    """n = m^2 * d with d squarefree; return (m, d)"""
    m, d, i = 1, n, 2
    while i*i <= d:
        while d % (i*i) == 0:
            d //= i*i; m *= i
        i += 1
    return m, d

def w4_polys(a0, dv, pts):
    """every W4 quadratic on the line, as coefficient lists [c, b, a]"""
    M, N = line_polys(a0, dv)
    out = []
    for s_pt, npl, ncub in pts:
        for i in range(3):
            col = padd(*[pscale(M[k][i], F(s_pt[k])) for k in range(3)])
            for sign in (1, -1):
                p = padd(col, pscale(N, -sign))
                while p and p[-1] == 0: p = p[:-1]
                if len(p) == 3: out.append(p)
    return out

def roots_of(p):
    c, b, a = p
    disc = b*b - 4*a*c
    if disc < 0: return []
    return [((-b - disc**F(1,2) if False else None), None)]

def exact_root(p, target, tol=1e-9):
    """the (num_p, num_q, den, d) with root = (num_p + num_q*sqrt d)/den matching target"""
    c, b, a = p
    disc = b*b - 4*a*c
    if disc <= 0: return None
    num, den = disc.numerator, disc.denominator
    m1, d1 = squarefree(num * den)          # sqrt(disc) = sqrt(num*den)/den
    for sgn in (1, -1):
        val = (float(-b) + sgn*float(m1)*(d1**0.5)/float(den)) / (2*float(a))
        if abs(val - target) < tol:
            return (-b/(2*a), F(sgn*m1, den)/(2*a), d1)
    return None

def qstr(vals):
    """[(p,q)] over Z[sqrt d] -> engine 'p:q' string, cleared of denominators"""
    L = 1
    for p, q in vals:
        for x in (p, q):
            L = L*x.denominator//__import__('math').gcd(L, x.denominator)
    out = [(int(p*L), int(q*L)) for p, q in vals]
    g = 0
    for p, q in out: g = __import__('math').gcd(g, __import__('math').gcd(abs(p), abs(q)))
    if g > 1: out = [(p//g, q//g) for p, q in out]
    return ",".join("%d:%d" % t for t in out), max(max(abs(p), abs(q)) for p, q in out)

def run(cubes_str, d):
    p = subprocess.run(["./cube_regions_q2w", "--d", str(d), "--quats", cubes_str],
                       capture_output=True, text=True,
                       cwd=os.path.dirname(os.path.abspath(__file__)))
    try: return json.loads(p.stdout)["bounded"]
    except Exception: return p.stdout.strip()[:70] or "REJ"

def do(base, a0, dv, ends, label):
    pts, lines = catalogue(base)
    polys = w4_polys(a0, dv, pts)
    print("%s: %d triple points, %d W4 quadratics on the line" % (label, len(pts), len(polys)), flush=True)
    for target, name in ends:
        hit = None
        for p in polys:
            r = exact_root(p, target)
            if r: hit = r; break
        if not hit:
            print("   %-8s no quadratic matched %.12f" % (name, target)); continue
        rp, rq, d = hit
        cay = [(F(a0[i]) + rp*F(dv[i]), rq*F(dv[i])) for i in range(3)]
        vals = [(F(1), F(0))] + cay
        qs, mag = qstr(vals)
        base_s = ";".join(",".join("%d:0" % v for v in q) for q in base)
        c = run(base_s + ";" + qs, d)
        print("   %-8s s = (%s) + (%s)sqrt(%d) = %.12f   max component %d"
              % (name, rp, rq, d, target, mag), flush=True)
        print("            count AT the endpoint: %s" % c, flush=True)

if __name__ == '__main__':
    do(BASE+[(7,14,1,-5)], [F(-3,4), F(-1), F(-1)], [F(1), F(0), F(0)],
       [(-0.045258752093, 'lower'), (0.002550224044, 'upper')], "n=7 1217")
    do(BASE+[(7,14,1,-5),(4,-3,-4,-4)], [F(-1), F(1), F(-61,24)], [F(0), F(0), F(1)],
       [(0.101360157756, 'upper')], "n=8 1895 (lower end is a W3 quartic, out of reach)")
