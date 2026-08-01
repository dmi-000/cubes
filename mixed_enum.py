#!/usr/bin/env python3
# Working principles: locus_linear.py (planes) + corner_probe.py (quadrics).
"""Mixed strata: two edge-edge PLANES and one corner QUADRIC.

The two condition types on the 393 base behave differently:
  * edge-edge coplanarity factors into rational PLANES -> all-rational strata,
    which is why the edge-edge enumeration found no irrational point (an
    artifact of the type, Postscript 49);
  * corner-on-face incidence is an IRREDUCIBLE QUADRIC -> can be irrational.

Their mixture is the tractable and interesting case.  Two planes cut a rational
line; restricting a quadric to that line gives a QUADRATIC IN ONE PARAMETER,
so every solution is rational or degree-2 irrational -- exactly Q(sqrt d),
the field of the n=3 maximizers (sqrt 2 and sqrt 5).  Pure quadric triples
reach degree 8 and produced almost no real points (corner_probe).

No Groebner is needed: intersect two planes exactly, evaluate the quadric at
three parameter values to recover the restricted quadratic by interpolation,
then solve it.  Rational roots are counted by the integer engine; irrational
roots are recorded with their field Q(sqrt d) for the algebraic counters.

INVARIANT: exact rational arithmetic (Fraction) throughout; a discriminant is
called a perfect square only when its exact rational square root is verified,
never by floating point.
"""
import itertools
import json
import math
import pickle
import sys
from fractions import Fraction as F

import sympy as sp

import record_hunt as R

a, b, c = sp.symbols('a b c', real=True)
FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]
CAP = 512


def load_planes():
    import locus_linear as L
    return L.extract_planes()


def quad_coeffs(P):
    """Quadric as {(i,j,k): rational coeff} over monomials a^i b^j c^k."""
    p = sp.Poly(sp.expand(P), a, b, c)
    return {m: F(int(sp.Rational(co).p), int(sp.Rational(co).q))
            for m, co in zip(p.monoms(), p.coeffs())}


def qeval(co, pt):
    v = F(0)
    for (i, j, k), cf in co.items():
        v += cf * pt[0] ** i * pt[1] ** j * pt[2] ** k
    return v


def line_of(p, q):
    """Intersection line of two planes: (point, direction), exact, or None."""
    n1, n2 = p[:3], q[:3]
    d = (n1[1] * n2[2] - n1[2] * n2[1], n1[2] * n2[0] - n1[0] * n2[2],
         n1[0] * n2[1] - n1[1] * n2[0])
    if not any(d):
        return None
    # fix the coordinate with the largest |d| component and solve the 2x2
    k = max(range(3), key=lambda i: abs(d[i]))
    i, j = [t for t in range(3) if t != k]
    det = n1[i] * n2[j] - n1[j] * n2[i]
    if det == 0:
        return None
    rhs1, rhs2 = -p[3], -q[3]
    pt = [F(0), F(0), F(0)]
    pt[i] = F(rhs1 * n2[j] - rhs2 * n1[j], det)
    pt[j] = F(n1[i] * rhs2 - n2[i] * rhs1, det)
    return (tuple(pt), tuple(F(x) for x in d))


def isqrt_exact(fr):
    """Exact rational square root of a non-negative Fraction, or None."""
    if fr < 0:
        return None
    n, dd = fr.numerator, fr.denominator
    rn, rd = math.isqrt(n), math.isqrt(dd)
    return F(rn, rd) if rn * rn == n and rd * rd == dd else None


def to_quat(pt):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0] * den), int(pt[1] * den), int(pt[2] * den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x // g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= CAP else None


def qmul(p, q):
    w, x, y, z = p
    e, f, g, h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


SYMS = list(dict.fromkeys(
    R.canon([t])[0] for t in
    [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1) for y in (-1, 0, 1)
     for z in (-1, 0, 1)
     if (w, x, y, z) != (0, 0, 0, 0) and w*w+x*x+y*y+z*z in (1, 2, 4)]))


def sym_key(q):
    return min(R.canon([qmul(tuple(q), h)])[0] for h in SYMS)


def main():
    planes = load_planes()
    quads = {j: [quad_coeffs(P) for P in Q]
             for j, Q in pickle.load(open('corner_conds.pkl', 'rb')).items()}
    print('planes/cube %s ; quadrics/cube %s'
          % ([len(planes[j]) for j in range(5)],
             [len(quads[j]) for j in range(5)]), flush=True)

    seen, cands, irr = set(), [], {}
    nsys = 0
    for tri in itertools.combinations(range(5), 3):
        for qi in tri:                       # which cube supplies the quadric
            pi, pj = [t for t in tri if t != qi]
            for P1 in planes[pi]:
                for P2 in planes[pj]:
                    L = line_of(P1, P2)
                    if L is None:
                        continue
                    p0, d = L
                    s1 = tuple(p0[t] + d[t] for t in range(3))
                    s2 = tuple(p0[t] - d[t] for t in range(3))
                    for co in quads[qi]:
                        nsys += 1
                        # q(t) = A t^2 + B t + C from three exact samples
                        C0 = qeval(co, p0)
                        Cp = qeval(co, s1)
                        Cm = qeval(co, s2)
                        A = (Cp + Cm - 2 * C0) / 2
                        B = (Cp - Cm) / 2
                        if A == 0:
                            if B == 0:
                                continue
                            ts = [-C0 / B]
                        else:
                            disc = B * B - 4 * A * C0
                            r = isqrt_exact(disc)
                            if r is None:
                                if disc > 0:
                                    key = disc.numerator * disc.denominator
                                    irr[key] = irr.get(key, 0) + 1
                                continue
                            ts = [(-B + r) / (2 * A), (-B - r) / (2 * A)]
                        for t in ts:
                            pt = tuple(p0[u] + t * d[u] for u in range(3))
                            qt = to_quat(pt)
                            if qt is None:
                                continue
                            k = sym_key(qt)
                            if k in seen:
                                continue
                            seen.add(k)
                            cands.append(qt)
    print('systems %d -> %d distinct rational candidates; %d irrational '
          '(degree-2) solution pairs by squarefree class'
          % (nsys, len(cands), sum(irr.values())), flush=True)

    eng = R.Engine(6, int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    out = open('mixed_enum.jsonl', 'a')
    best, hist = (0, None), {}
    B = 500
    for s in range(0, len(cands), B):
        chunk = cands[s:s + B]
        res = eng.count([[list(x) for x in FIVE] + [list(q)] for q in chunk])
        for q, (tot, bd) in zip(chunk, res):
            hist[tot] = hist.get(tot, 0) + 1
            if tot > best[0]:
                best = (tot, q)
            if tot >= 723:
                out.write(json.dumps({'total': tot, 'sixth': q,
                                      'by_depth': bd}) + '\n')
                out.flush()
                if tot > 727:
                    print('*** ABOVE 727: %d %s' % (tot, q), flush=True)
        print('  counted %d/%d best %s' % (min(s+B, len(cands)), len(cands),
                                           best), flush=True)
    print('\nDONE best=%s' % (best,), flush=True)
    print('top:', {t: hist[t] for t in sorted(hist)[-12:]}, flush=True)
    json.dump({'hist': {str(k): v for k, v in hist.items()},
               'best': [best[0], list(best[1])],
               'irrational_classes': len(irr),
               'irrational_solutions': sum(irr.values())},
              open('mixed_enum_summary.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
