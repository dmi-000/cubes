#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Q(sqrt5) golden engine). Project index: README.md
"""EXACT region count for sub-compounds of the compound of five cubes.

All geometry lives in the golden field Q(sqrt5): the 15 two-fold axes of the
icosahedron (= the face normals of the five cubes) are (1,0,0)-type and
(phi, 1/phi, 1)/2-type, and |(phi, 1/phi, 1)|^2 = 4, so the UNIT normals have
entries in Q(sqrt5).  Every predicate (side-of-plane, plane-triple vertex,
facet identity) is exact field arithmetic on pairs of rationals a + b*sqrt5.
No floating point, no epsilons, no voxel artifacts.

Method
------
1. The five cubes are the five orthogonal triples among the 15 unit axes
   (cube = {x : |n.x| <= 1 for its triple}); corners = +-n1 +-n2 +-n3 land on
   the 20 dodecahedron vertices.
2. Build the full arrangement of the 6N face planes (N = #cubes) inside a
   bounding box, by exact convex-cell clipping.  Arrangement cells are convex,
   hence connected, and each carries a definite N-bit membership label.
3. Every internal facet lies on exactly one face plane, and (because every
   cell face is refined by ALL planes) facets on the two sides of a plane
   coincide exactly as polygons -> facet identity = (plane id, vertex set).
4. A facet is REAL where it lies inside its cube's actual square face
   (|n'.w| < 1 and |n''.w| < 1 at the facet centroid for the cube's other two
   normals), else PHANTOM.  Merge cells across phantom facets (labels must
   agree - asserted); count union-find components per label.

Region count = number of same-label components; the outside must come out as
exactly one component (the compound is a union of concentric convex bodies,
hence star-shaped, hence no cavities) - asserted.

Usage:  python3 cube_compound_exact.py 1 2 3 4 5     # N cubes of the five
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations, product


# ---------------------------------------------------------------- Q(sqrt5)
class Q5:
    __slots__ = ('a', 'b')

    def __init__(self, a, b=0):
        self.a = a if isinstance(a, Fr) else Fr(a)
        self.b = b if isinstance(b, Fr) else Fr(b)

    def __add__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(s.a - o.a, s.b - o.b)

    def __neg__(s):
        return Q5(-s.a, -s.b)

    def __mul__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = o if isinstance(o, Q5) else Q5(o)
        d = o.a * o.a - 5 * o.b * o.b          # nonzero for o != 0
        return Q5((s.a * o.a - 5 * s.b * o.b) / d, (s.b * o.a - s.a * o.b) / d)

    def sign(s):
        a, b = s.a, s.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        t = a * a - 5 * b * b                   # never 0 in mixed case
        st = 1 if t > 0 else -1
        return st if a > 0 else -st

    def __eq__(s, o):
        return isinstance(o, Q5) and s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __float__(s):
        return float(s.a) + float(s.b) * 5 ** 0.5

    def __repr__(s):
        return f'({s.a}+{s.b}r5)'


ZERO, ONE = Q5(0), Q5(1)
HALF = Q5(Fr(1, 2))
PHI_H = Q5(Fr(1, 4), Fr(1, 4))      # phi/2
IPHI_H = Q5(Fr(-1, 4), Fr(1, 4))    # 1/(2 phi)


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def vadd(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def vsub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def vscale(u, t):
    return (u[0] * t, u[1] * t, u[2] * t)


# ------------------------------------------------- normals, cubes, planes
def build_axes():
    axes = [(ONE, ZERO, ZERO), (ZERO, ONE, ZERO), (ZERO, ZERO, ONE)]
    base = [PHI_H, IPHI_H, HALF]
    for cyc in range(3):
        p = base[-cyc:] + base[:-cyc]
        for s1, s2 in product((1, -1), repeat=2):
            v = (p[0] if s1 > 0 else -p[0],
                 p[1] if s2 > 0 else -p[1],
                 p[2])
            axes.append(v)
    assert len(axes) == 15
    for n in axes:
        assert (dot(n, n) - ONE).sign() == 0, 'normals must be unit'
    return axes


def find_cubes(axes):
    triples = [t for t in combinations(range(15), 3)
               if all(dot(axes[i], axes[j]).sign() == 0
                      for i, j in combinations(t, 2))]
    assert len(triples) == 5, f'expected 5 orthogonal triples, got {len(triples)}'
    return triples


# ------------------------------------------------------------ cell clipping
def clip(faces, f, cache):
    """Split convex cell (list of (pid, loop)) by plane function f.

    Returns (neg_half, pos_half); a half is None if empty.  Points with
    f = 0 belong to both halves.  cache: point -> sign of f.
    """
    def sgn(p):
        s = cache.get(p)
        if s is None:
            s = f(p).sign()
            cache[p] = s
        return s

    pts = {p for _, loop in faces for p in loop}
    signs = {p: sgn(p) for p in pts}
    if not any(s > 0 for s in signs.values()):
        return faces, None
    if not any(s < 0 for s in signs.values()):
        return None, faces

    inter = {}

    def cut(p, q):
        key = (p, q) if hash(p) <= hash(q) else (q, p)
        w = inter.get(key)
        if w is None:
            fp, fq = f(p), f(q)
            t = fp / (fp - fq)
            w = vadd(p, vscale(vsub(q, p), t))
            inter[key] = w
            cache[w] = 0
        return w

    halves = []
    for keep in (-1, 1):
        new_faces = []
        cap_edges = []
        for pid, loop in faces:
            out = []
            zeros = []
            m = len(loop)
            for i in range(m):
                p, q = loop[i], loop[(i + 1) % m]
                sp, sq = signs[p], signs[q]
                if sp * keep >= 0:
                    out.append(p)
                    if sp == 0:
                        zeros.append(p)
                if sp * sq < 0:
                    w = cut(p, q)
                    out.append(w)
                    zeros.append(w)
            ded = [p for i, p in enumerate(out) if p != out[i - 1]]
            if len(ded) >= 3:
                new_faces.append((pid, ded))
            zs = []
            for z in zeros:
                if z not in zs:
                    zs.append(z)
            if len(zs) == 2:
                cap_edges.append(tuple(zs))
        if cap_edges:
            nbr = {}
            for a, b in cap_edges:
                nbr.setdefault(a, []).append(b)
                nbr.setdefault(b, []).append(a)
            start = cap_edges[0][0]
            loop, prev, cur = [start], None, start
            while True:
                nxts = [x for x in nbr[cur] if x != prev]
                if not nxts:
                    break
                prev, cur = cur, nxts[0]
                if cur == start:
                    break
                loop.append(cur)
            if len(loop) >= 3 and cur == start:
                new_faces.append(('cap', loop))
        halves.append(new_faces if new_faces else None)
    return halves[0], halves[1]


# ------------------------------------------------------------------- main
def run(N):
    axes = build_axes()
    triples = find_cubes(axes)[:N]
    used = [i for t in triples for i in t]

    # dodecahedron-vertex sanity check for the full compound
    if N == 5:
        dod = {tuple(c * v for c, v in zip(s, (ONE, ONE, ONE)))
               for s in product((1, -1), repeat=3)}
        # golden-ratio vertices
        PHI, IPHI = Q5(Fr(1, 2), Fr(1, 2)), Q5(Fr(-1, 2), Fr(1, 2))
        for cyc in range(3):
            p = [ZERO, IPHI, PHI][-cyc:] + [ZERO, IPHI, PHI][:-cyc]
            nz = [i for i in range(3) if p[i] != ZERO]
            for s1, s2 in product((1, -1), repeat=2):
                q = list(p)
                q[nz[0]] = q[nz[0]] if s1 > 0 else -q[nz[0]]
                q[nz[1]] = q[nz[1]] if s2 > 0 else -q[nz[1]]
                dod.add(tuple(q))
        assert len(dod) == 20
        for t in triples:
            for s1, s2, s3 in product((1, -1), repeat=3):
                c = vadd(vadd(vscale(axes[t[0]], Q5(s1)),
                              vscale(axes[t[1]], Q5(s2))),
                         vscale(axes[t[2]], Q5(s3)))
                assert c in dod, 'cube corner off the dodecahedron'
        print('exact vertex check: all 40 corners on the dodecahedron  OK')

    # planes: (axis index, offset +-1); plane function n.x - c
    planes = [(ai, c) for ai in used for c in (1, -1)]

    B = Q5(4)
    corners = list(product((B, -B), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] == val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (float(p[a]), float(p[b])))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cell0 = [(('box', i, s), box_face(i, v))
             for i in range(3) for s, v in ((1, B), (-1, -B))]
    cells = [cell0]

    for pid, (ai, c) in enumerate(planes):
        n, cq = axes[ai], Q5(c)
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
    print(f'N={N}: arrangement cells: {len(cells)}')

    # labels from cell centroids
    def centroid(cell):
        pts = {p for _, loop in cell for p in loop}
        k = Q5(Fr(1, len(pts)))
        s = (ZERO, ZERO, ZERO)
        for p in pts:
            s = vadd(s, p)
        return vscale(s, k)

    def label(w):
        lab = 0
        for k, t in enumerate(triples):
            if all((dot(axes[ai], w) - ONE).sign() < 0 and
                   (dot(axes[ai], w) + ONE).sign() > 0 for ai in t):
                lab |= 1 << k
        return lab

    cents = [centroid(c) for c in cells]
    labs = [label(w) for w in cents]

    # facet identification: (plane id, frozenset of vertices)
    groups = {}
    for ci, cell in enumerate(cells):
        for pid, loop in cell:
            if isinstance(pid, tuple):      # box face
                continue
            groups.setdefault((pid, frozenset(loop)), []).append(ci)

    parent = list(range(len(cells)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    plane_cube = {}
    for pid, (ai, c) in enumerate(planes):
        (k, t) = next((k, t) for k, t in enumerate(triples) if ai in t)
        plane_cube[pid] = (k, [a for a in t if a != ai])

    for (pid, verts), cs in groups.items():
        assert len(cs) == 2, f'facet shared by {len(cs)} cells'
        a, b = cs
        k, others = plane_cube[pid]
        pl = list(verts)
        w = vscale(sum_pts(pl), Q5(Fr(1, len(pl))))
        real = all((dot(axes[ai], w) - ONE).sign() < 0 and
                   (dot(axes[ai], w) + ONE).sign() > 0 for ai in others)
        if real:
            assert labs[a] ^ labs[b] == 1 << k, 'real facet must flip its cube'
        else:
            assert labs[a] == labs[b], 'phantom facet with differing labels'
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    comps = {}
    for ci in range(len(cells)):
        comps.setdefault((labs[ci], find(ci)), None)
    per_label = {}
    for (lab, _r) in comps:
        per_label[lab] = per_label.get(lab, 0) + 1
    assert per_label.get(0, 0) == 1, 'outside must be a single region'
    by_depth = {}
    for lab, cnt in per_label.items():
        d = bin(lab).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
    total = sum(per_label.values())
    print(f'N={N}: bounded regions = {total - 1}   by depth: '
          f'{dict(sorted(by_depth.items()))}')
    print(f'      per label: {dict(sorted(per_label.items()))}')
    return total - 1


def sum_pts(pl):
    s = (ZERO, ZERO, ZERO)
    for p in pl:
        s = vadd(s, p)
    return s


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    for arg in sys.argv[1:]:
        run(int(arg))
