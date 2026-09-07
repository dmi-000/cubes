#!/usr/bin/env python3
"""The plane-incidence signature computed just OUTSIDE a configuration, exactly.

Replaces the finite-step measurement in TAXONOMY 12a. A displacement of 2^-20 answers a
question about 2^-20; this answers the question 12a meant to ask -- what the signature is
immediately off the stratum, in a given direction -- with the step size removed by
construction rather than driven small.

The answer is DIRECTIONAL, and that is the point rather than a limitation: "is the signature
preserved under perturbation" has no scalar answer, only a set of directions along which it
survives. A percentage was always a lossy summary of a cone.

Everything is exact: coordinates live in Z[e] ordered by the sign of the lowest nonzero
coefficient (`epsfield`), so "these three planes meet in a point", "these two points are the
same point" and "this point lies within this face" are polynomial identities and sign tests,
not comparisons at a chosen scale.
"""
import itertools, random, sys
from collections import Counter, defaultdict
sys.path.insert(0, '.')
from epsfield import (ZERO, const, padd, psub, pmul, pneg, psign, canon_point)


def qmul_e(p, r):
    w, x, y, z = p; e, f, g, h = r
    return (psub(psub(psub(pmul(w, e), pmul(x, f)), pmul(y, g)), pmul(z, h)),
            padd(padd(padd(pmul(w, f), pmul(x, e)), pmul(y, h)), pneg(pmul(z, g))),
            padd(padd(psub(pmul(w, g), pmul(x, h)), pmul(y, e)), pmul(z, f)),
            padd(padd(psub(pmul(w, h), pmul(y, f)), pmul(x, g)), pmul(z, e)))


def lift(q):
    return tuple(const(c) for c in q)


def planes_e(cfg):
    """the six face planes of each cube: COLUMNS of the rotation matrix ([P227])"""
    out = []
    for (w, x, y, z) in cfg:
        ww, xx, yy, zz = pmul(w, w), pmul(x, x), pmul(y, y), pmul(z, z)
        n = padd(padd(padd(ww, xx), yy), zz)
        two = const(2)
        M = [[padd(psub(psub(ww, yy), zz), xx),
              pmul(two, psub(pmul(x, y), pmul(w, z))),
              pmul(two, padd(pmul(x, z), pmul(w, y)))],
             [pmul(two, padd(pmul(x, y), pmul(w, z))),
              padd(psub(psub(ww, xx), zz), yy),
              pmul(two, psub(pmul(y, z), pmul(w, x)))],
             [pmul(two, psub(pmul(x, z), pmul(w, y))),
              pmul(two, padd(pmul(y, z), pmul(w, x))),
              padd(psub(psub(ww, xx), yy), zz)]]
        for c in range(3):
            v = (M[0][c], M[1][c], M[2][c])
            out.append((v[0], v[1], v[2], n, M, n))
            out.append((v[0], v[1], v[2], pneg(n), M, n))
    return out


def det3(a, b, c):
    return psub(padd(pmul(a[0], psub(pmul(b[1], c[2]), pmul(b[2], c[1]))),
                     pmul(a[2], psub(pmul(b[0], c[1]), pmul(b[1], c[0])))),
                pmul(a[1], psub(pmul(b[0], c[2]), pmul(b[2], c[0]))))


def solve3_e(p, q, r):
    A = (p[:3], q[:3], r[:3]); B = (p[3], q[3], r[3])
    det = det3((A[0][0], A[1][0], A[2][0]), (A[0][1], A[1][1], A[2][1]), (A[0][2], A[1][2], A[2][2]))
    if not det:
        return None
    cols = [[A[0][0], A[1][0], A[2][0]], [A[0][1], A[1][1], A[2][1]], [A[0][2], A[1][2], A[2][2]]]
    nums = []
    for i in range(3):
        c = [list(x) for x in cols]
        c[i] = [B[0], B[1], B[2]]
        nums.append(det3(tuple(c[0]), tuple(c[1]), tuple(c[2])))
    return canon_point((nums[0], nums[1], nums[2], det))


def signature_e(cfg, cap=12):
    """(histogram of multiplicities >= 4, max multiplicity) just outside, exactly"""
    P = planes_e(cfg)
    cnt = defaultdict(int)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3_e(P[i], P[j], P[k])
        if s is not None:
            cnt[s] += 1
    h = Counter(); mx = 0
    for _, c in cnt.items():
        m = 3
        while m * (m - 1) * (m - 2) // 6 < c:
            m += 1
        mx = max(mx, m)
        if m >= 4:
            h[min(m, cap)] += 1
    return tuple(sorted(h.items())), mx


def perturb_generic(cfg, rng, bound=5):
    """q -> q + e*v with v a random integer direction; cube 0 is the gauge and is held"""
    out = [lift(cfg[0])]
    for q in cfg[1:]:
        v = [rng.randint(-bound, bound) for _ in range(4)]
        while not any(v):
            v = [rng.randint(-bound, bound) for _ in range(4)]
        out.append(tuple(trimpair(c, d) for c, d in zip(q, v)))
    return out


def trimpair(c, d):
    from epsfield import trim
    return trim((int(c), int(d)))


def perturb_about(cfg, axis):
    """q -> q * (1, e*axis): an infinitesimal extra rotation about `axis`.

    If every moving cube already shares that axis, this stays inside the shared-axis family,
    so any coincidence that exists BECAUSE they share it must survive. That makes it the
    'must be preserved' side of a two-sided gate.
    """
    d = (const(1), (0, axis[0]), (0, axis[1]), (0, axis[2]))
    return [lift(cfg[0])] + [qmul_e(lift(q), d) for q in cfg[1:]]


if __name__ == '__main__':
    from sharedaxis import q_axis
    from fractions import Fraction as F
    # THREE CUBES ON THE (1,1,1) CORNER AXIS: they share that corner, so nine face planes
    # pass through it. A two-sided gate -- a control that can fail in BOTH directions, which
    # is what a control chosen for convenience never does.
    cfg = [(1, 0, 0, 0), q_axis((1, 1, 1), F(1, 3)), q_axis((1, 1, 1), F(2, 5))]
    base, bmax = signature_e([lift(q) for q in cfg])
    print('base (exact, unperturbed)          : %s   max %d' % (base, bmax))
    assert bmax == 9, 'setup wrong: the corner triple should carry a 9-fold'

    tang, tmax = signature_e(perturb_about(cfg, (1, 1, 1)))
    print('+ e * (rotation about the shared axis): %s   max %d' % (tang, tmax))

    rng = random.Random(11)
    gen, gmax = signature_e(perturb_generic(cfg, rng))
    print('+ e * (generic direction)             : %s   max %d' % (gen, gmax))

    ok_t = (tmax == 9)
    ok_g = (gmax < 9)
    print()
    print('GATE, both sides required:')
    print('  tangent direction PRESERVES the 9-fold : %s' % ('PASS' if ok_t else 'FAIL'))
    print('  generic direction BREAKS   the 9-fold  : %s' % ('PASS' if ok_g else 'FAIL'))
    sys.exit(0 if (ok_t and ok_g) else 1)
