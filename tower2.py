#!/usr/bin/env python3
"""Depth-2 tower over Q2 base: Q(sqrt2, sqrt d) for d in {3,5}.

Structural clone of qtower.py's Ext3 recipe (a + b*sqrt d, coeffs in a base
field), but with base field = slide3_q2.Q2 (already-validated Q(sqrt2)) and a
configurable outer radicand d.  d=3 gives Q(sqrt2,sqrt3), basis {1,sqrt2,
sqrt3,sqrt6}; d=5 gives Q(sqrt2,sqrt5), basis {1,sqrt2,sqrt5,sqrt10}.

Multiplicative-independence gate below: none of {2, d, 2d} may be a perfect
square (else sqrt d in Q(sqrt2) and the sign recursion hits an honest zero).

The counting core is a direct copy of qtower.exact_count_tower / slide3_q2.
exact_count_q2, specialized to Tower field elements.  clip/dot/vadd/vsub/
vscale are generic and reused from cube_compound_exact (imported).  Nothing
in the read-only ground-truth files is modified.
"""
import sys
import math
from fractions import Fraction as Fr
from itertools import product

sys.path.insert(0, '/Users/dmi/carroll')
from cube_compound_exact import dot, vadd, vsub, vscale, clip
from slide3_q2 import Q2
from golden_rotations import Rot


def make_tower(d):
    assert not (lambda n: math.isqrt(n) ** 2 == n)(2), 'sanity'
    for n in (2, d, 2 * d):
        r = math.isqrt(n)
        assert r * r != n, f'{n} is a perfect square -- tower ill-formed'

    class T:
        __slots__ = ('a', 'b')
        D = d

        def __init__(s, a, b=None):
            s.a = a if isinstance(a, Q2) else Q2(a)
            s.b = (b if isinstance(b, Q2) else Q2(b)) if b is not None else Q2(0)

        def __add__(s, o):
            o = o if isinstance(o, T) else T(o)
            return T(s.a + o.a, s.b + o.b)

        __radd__ = __add__

        def __sub__(s, o):
            o = o if isinstance(o, T) else T(o)
            return T(s.a - o.a, s.b - o.b)

        def __neg__(s):
            return T(-s.a, -s.b)

        def __mul__(s, o):
            o = o if isinstance(o, T) else T(o)
            return T(s.a * o.a + T.D * (s.b * o.b), s.a * o.b + s.b * o.a)

        __rmul__ = __mul__

        def __truediv__(s, o):
            o = o if isinstance(o, T) else T(o)
            den = o.a * o.a - T.D * (o.b * o.b)
            na = s.a * o.a - T.D * (s.b * o.b)
            nb = s.b * o.a - s.a * o.b
            return T(na / den, nb / den)

        def sign(s):
            sa, sb = s.a.sign(), s.b.sign()
            if sb == 0:
                return sa
            if sa == 0:
                return sb
            if sa == sb:
                return sa
            t = s.a * s.a - T.D * (s.b * s.b)   # Q2 element
            st = t.sign()
            assert st != 0, 'outer radical fell into Q2 -- invariant violated'
            return st if sa > 0 else -st

        def coords(s):
            return (s.a.a, s.a.b, s.b.a, s.b.b)

        def __eq__(s, o):
            return isinstance(o, T) and s.a == o.a and s.b == o.b

        def __hash__(s):
            return hash(s.coords())

        def __float__(s):
            return float(s.a) + float(s.b) * d ** 0.5

        def __repr__(s):
            return f'({s.a!r}+{s.b!r}*r{d})'

    return T


def exact_count(rots, T, verbose=False):
    """Copy of qtower.exact_count_tower, field = Tower class T."""
    ONE = T(1)
    cubes = []
    for R in rots:
        cols = [tuple(R.m[i][j] for i in range(3)) for j in range(3)]
        cubes.append(cols)
    nq = len(cubes)
    planes = [(k, j, c) for k in range(nq) for j in range(3) for c in (1, -1)]

    def plane_key(k, j, c):
        comps = list(cubes[k][j])
        s = 0
        for x in comps:
            s = x.sign()
            if s != 0:
                break
        if s < 0:
            comps = [-x for x in comps]
            c = -c
        return (tuple(x.coords() for x in comps), c)

    classes = {}
    for k, j, c in planes:
        classes.setdefault(plane_key(k, j, c), []).append((k, j))
    owners_of = [classes[plane_key(k, j, c)] for (k, j, c) in planes]

    B_, nB_ = T(4), T(-4)
    corners = list(product((B_, nB_), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] is val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (float(p[a]), float(p[b])))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cells = [[(('box', i, s), box_face(i, v))
              for i in range(3) for s, v in ((1, B_), (-1, nB_))]]

    for pid, (k, j, c) in enumerate(planes):
        n = cubes[k][j]
        cq = ONE if c == 1 else -ONE
        f = lambda p, n=n, cq=cq: dot(n, p) - cq
        cache = {}
        nxt = []
        for cell in cells:
            neg, pos = clip(cell, f, cache)
            for half in (neg, pos):
                if half is not None:
                    nxt.append([(pid if q == 'cap' else q, loop)
                                for q, loop in half])
        cells = nxt
        if verbose:
            print(f'  after plane {pid}: {len(cells)} cells', flush=True)
    if verbose:
        print(f'arrangement cells = {len(cells)}')

    def centroid_pts(pts):
        kk = T(Fr(1, len(pts)))
        s = (T(0),) * 3
        for p in pts:
            s = vadd(s, p)
        return vscale(s, kk)

    def label(w):
        lab = 0
        for k in range(nq):
            if all((dot(cubes[k][j], w) - ONE).sign() < 0 and
                   (dot(cubes[k][j], w) + ONE).sign() > 0 for j in range(3)):
                lab |= 1 << k
        return lab

    labs = [label(centroid_pts(list({p for _, loop in c for p in loop})))
            for c in cells]

    groups = {}
    for ci, cell in enumerate(cells):
        for pid, loop in cell:
            if isinstance(pid, tuple):
                continue
            groups.setdefault((pid, frozenset(loop)), []).append(ci)

    parent = list(range(len(cells)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (pid, verts), cs in groups.items():
        assert len(cs) == 2, f'facet shared by {len(cs)} cells'
        a, b = cs
        w = centroid_pts(list(verts))
        flip = 0
        for kk, jj in owners_of[pid]:
            others = [cubes[kk][t] for t in range(3) if t != jj]
            if all((dot(n, w) - ONE).sign() < 0 and
                   (dot(n, w) + ONE).sign() > 0 for n in others):
                flip |= 1 << kk
        if flip:
            assert labs[a] ^ labs[b] == flip, 'real facet flip mismatch'
        else:
            assert labs[a] == labs[b], 'phantom facet with differing labels'
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    comps = set()
    for ci in range(len(cells)):
        comps.add((labs[ci], find(ci)))
    per_label = {}
    for lab, _r in comps:
        per_label[lab] = per_label.get(lab, 0) + 1
    assert per_label.get(0, 0) == 1, 'outside must be a single region'
    by_depth = {}
    for lab, cnt in per_label.items():
        dep = bin(lab).count('1')
        by_depth[dep] = by_depth.get(dep, 0) + cnt
    total = sum(per_label.values()) - 1
    return total, by_depth


# ------- embeddings into a Tower T -------
def embed_q2(x, T):
    """Q2 element -> T (outer-radical part zero)."""
    return T(x, Q2(0))


def embed_q5(x, T):
    """Q5 element a+b*sqrt5 -> T with D=5 (a,b rational -> Q2 coeffs)."""
    return T(Q2(x.a), Q2(x.b))


def embed_rot_q2(R, T):
    return Rot([[embed_q2(R.m[i][j], T) for j in range(3)] for i in range(3)])


def embed_rot_q5(R, T):
    return Rot([[embed_q5(R.m[i][j], T) for j in range(3)] for i in range(3)])


def assert_orthonormal(R, T):
    m = R.m
    for i in range(3):
        for j in range(3):
            dd = sum((m[k][i] * m[k][j] for k in range(3)), T(0)) \
                - (T(1) if i == j else T(0))
            assert dd.sign() == 0, f'orthonormality fail ({i},{j})'
