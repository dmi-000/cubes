#!/usr/bin/env python3
# Working principles: MULTIWALL_SPEC.md + multiwall_report.md. Project index: README.md
"""Depth-2 tower arithmetic: Q(sqrt3, sqrt5), built as Q5(sqrt3).

Per MULTIWALL_SPEC.md section 1: "Element of K(sqrt d): pair (p, q) with
p, q in K; base case K = Q uses Fraction."  Here K = Q5 (cube_compound_exact's
ALREADY VALIDATED Q(sqrt5) field -- reused, not re-derived, per the spec's
"reuse the field-parameterized core" instruction) and d = 3, giving
Ext3 = Q5(sqrt3) = Q(sqrt3, sqrt5), basis {1, sqrt3, sqrt5, sqrt15} as a
Q-vector space.  Writing a fully generic recursive "list of d's" tower over
raw Fractions would just re-derive Q5's own arithmetic at the bottom level;
instead this specializes the general scheme to depth 2 by taking Q5 itself
as the base field K, satisfying "only gate and use depth <= 2 for now."

INVARIANT (multiplicative independence, asserted below): {3, 5, 15} contains
no perfect square, i.e. sqrt3 is not in Q(sqrt5) -- required for the sign
algorithm (sign(p + q*sqrt3) recurses on p^2 - 3*q^2 in Q5, which can vanish
for (p,q) != (0,0) iff sqrt3 in Q5).

Sign algorithm (exact, no floats in any predicate):
  sign(p + q*sqrt3) = sign(p)              if q == 0
                     = sign(q)              if p == 0
                     = sign(p)              if sign(p) == sign(q)
                     = sign(p)*sign(p^2 - 3*q^2)   otherwise (p^2-3q^2 in Q5,
                       recurses via Q5.sign(), itself exact rational compare)

Hash/eq via the canonical flattened coordinate tuple (a.a, a.b, b.a, b.b),
i.e. the exact rational coefficients of 1, sqrt5, sqrt3, sqrt15.  __float__
is for diagnostics only (vertex-ordering in box_face, print statements) --
NEVER used in a sign/predicate.

The counting core (exact_count_tower) is a direct generalization of
certify_six.exact_count_config: same algorithm (plane-triple arrangement,
coincident-plane classes, facet-identity merge, union-find), but operating
directly on Ext3 field elements (no CN interval-filter wrapper -- the spec
says a tower eval may cost minutes, which is acceptable for a VERIFIER, and
skipping the interval tiers removes a large source of implementation risk
for a program that must be exactly right).  clip/dot/vadd/vsub/vscale are
IMPORTED, unmodified, from cube_compound_exact.py -- they are already
generic over any field supporting +,-,*,/,sign(),hash,eq, so no
reimplementation is needed for those (this is the "one counting core"
directive: only the field changes, not the geometry).

certify_six.py, cube_compound_exact.py, exact_search.py, exact_search_results.jsonl
are all read-only ground truth; nothing here modifies them.
"""
import math
from fractions import Fraction as Fr
from itertools import product

from cube_compound_exact import Q5, ZERO, ONE, dot, vadd, vsub, vscale, clip
from golden_rotations import Rot

D_LIST = (5, 3)   # inner extension sqrt5 (= Q5's own field), outer sqrt3


def _is_square(n):
    r = math.isqrt(n)
    return r * r == n


# multiplicative-independence gate for the d-list {5, 3} (and their product
# 15): none of the nonempty subset-products may be a perfect square, else
# sqrt(that product) collapses into a smaller subfield and the sign
# algorithm's "recurse on p^2 - d*q^2" step could hit an honest zero for
# (p,q) != (0,0), silently breaking exactness.
for _n in (5, 3, 15):
    assert not _is_square(_n), f'{_n} is a perfect square -- tower ill-formed'


class Ext3:
    """Element of Q5(sqrt3) = Q(sqrt3, sqrt5): a + b*sqrt3, a, b in Q5."""
    __slots__ = ('a', 'b')
    D = 3

    def __init__(self, a, b=None):
        self.a = a if isinstance(a, Q5) else Q5(a)
        self.b = (b if isinstance(b, Q5) else Q5(b)) if b is not None else Q5(0)

    def __add__(s, o):
        o = o if isinstance(o, Ext3) else Ext3(o)
        return Ext3(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        o = o if isinstance(o, Ext3) else Ext3(o)
        return Ext3(s.a - o.a, s.b - o.b)

    def __neg__(s):
        return Ext3(-s.a, -s.b)

    def __mul__(s, o):
        o = o if isinstance(o, Ext3) else Ext3(o)
        return Ext3(s.a * o.a + Ext3.D * (s.b * o.b), s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = o if isinstance(o, Ext3) else Ext3(o)
        d = o.a * o.a - Ext3.D * (o.b * o.b)
        num_a = s.a * o.a - Ext3.D * (s.b * o.b)
        num_b = s.b * o.a - s.a * o.b
        return Ext3(num_a / d, num_b / d)

    def sign(s):
        sa, sb = s.a.sign(), s.b.sign()
        if sb == 0:
            return sa
        if sa == 0:
            return sb
        if sa == sb:
            return sa
        t = s.a * s.a - Ext3.D * (s.b * s.b)     # Q5 element
        st = t.sign()
        assert st != 0, 'sqrt3 in Q5 -- tower invariant violated'
        return st if sa > 0 else -st

    def coords(s):
        """Canonical flattened tuple over basis {1, sqrt5, sqrt3, sqrt15}."""
        return (s.a.a, s.a.b, s.b.a, s.b.b)

    def __eq__(s, o):
        return isinstance(o, Ext3) and s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash(s.coords())

    def __float__(s):
        return float(s.a) + float(s.b) * 3 ** 0.5

    def __repr__(s):
        return f'({s.a!r}+{s.b!r}*r3)'


ZERO3, ONE3 = Ext3(0), Ext3(1)


def embed_q5(x):
    """Q5 -> Ext3 (sqrt3-part zero)."""
    return Ext3(x, Q5(0))


def embed_rot(R):
    """Rot with Q5 entries -> Rot with Ext3 entries (sqrt3-parts all zero)."""
    return Rot([[embed_q5(R.m[i][j]) for j in range(3)] for i in range(3)])


def det3(R):
    m = R.m
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def assert_orthonormal(R):
    m = R.m
    for i in range(3):
        for j in range(3):
            d = sum((m[k][i] * m[k][j] for k in range(3)), ZERO3) \
                - (ONE3 if i == j else ZERO3)
            assert d.sign() == 0, f'orthonormality fail at ({i},{j}): {d!r}'
    assert (det3(R) - ONE3).sign() == 0, f'det != 1: {det3(R)!r}'


def sixth_wall_R():
    """Exact rotation by 90 deg about (1,1,1)/sqrt3, via Rodrigues:
    R = u u^T + [u]_x  (cos90=0, sin90=1, so the I*cos term vanishes).
    u = (1,1,1)/sqrt3 -> u_i u_j = 1/3 for all i,j (RATIONAL: sqrt3*sqrt3=3);
    [u]_x entries are +-1/sqrt3 = +-sqrt3/3.  Entries 1/3 +- sqrt3/3, exactly
    as MULTIWALL_SPEC.md section 3 states."""
    third = Ext3(Q5(Fr(1, 3)))
    s3 = Ext3(Q5(0), Q5(Fr(1, 3)))    # sqrt3/3 = 1/sqrt3
    rows = [
        [third,      third - s3,  third + s3],
        [third + s3, third,       third - s3],
        [third - s3, third + s3,  third],
    ]
    R = Rot(rows)
    assert_orthonormal(R)
    return R


def z_rot_30():
    """Exact rotation by 30 deg about z: cos30=sqrt3/2, sin30=1/2."""
    c = Ext3(Q5(0), Q5(Fr(1, 2)))   # sqrt3/2
    s = Ext3(Q5(Fr(1, 2)))          # 1/2
    R = Rot([[c, -s, ZERO3], [s, c, ZERO3], [ZERO3, ZERO3, ONE3]])
    assert_orthonormal(R)
    return R


IDENT3 = Rot([[ONE3, ZERO3, ZERO3], [ZERO3, ONE3, ZERO3], [ZERO3, ZERO3, ONE3]])


# ------------------------------------------------------ counting core
def exact_count_tower(rots, verbose=False, with_labels=False):
    """Direct generalization of certify_six.exact_count_config to Ext3
    field elements (no CN wrapper).  See module docstring."""
    one = ONE3
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

    B, nB = Ext3(Q5(4)), Ext3(Q5(-4))
    corners = list(product((B, nB), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] is val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (float(p[a]), float(p[b])))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cells = [[(('box', i, s), box_face(i, v))
              for i in range(3) for s, v in ((1, B), (-1, nB))]]

    for pid, (k, j, c) in enumerate(planes):
        n = cubes[k][j]
        cq = one if c == 1 else -one
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
        print(f'exact(tower): arrangement cells = {len(cells)}')

    def centroid_pts(pts):
        kk = Ext3(Q5(Fr(1, len(pts))))
        s = (ZERO3,) * 3
        for p in pts:
            s = vadd(s, p)
        return vscale(s, kk)

    def label(w):
        lab = 0
        for k in range(nq):
            if all((dot(cubes[k][j], w) - one).sign() < 0 and
                   (dot(cubes[k][j], w) + one).sign() > 0 for j in range(3)):
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
            if all((dot(n, w) - one).sign() < 0 and
                   (dot(n, w) + one).sign() > 0 for n in others):
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
        d = bin(lab).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
    total = sum(per_label.values()) - 1
    if with_labels:
        return total, by_depth, per_label
    return total, by_depth


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    import time
    print('qtower self-test: identity pair (should be a single cube, 1 region)')
    t0 = time.time()
    total, bd = exact_count_tower([IDENT3, IDENT3])
    print(f'  total={total} by_depth={bd} ({time.time()-t0:.1f}s) '
          f'(dup-cube coincidence path)')
