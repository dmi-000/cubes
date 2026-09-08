"""Q(sqrt3) exact region counter -- field-constant clone of slide3_q2.py
(D: 2 -> 3), same pattern as q6_count.py. Verifier for the dihedral-family
sweep at Pythagorean psi: S(psi) = -I/2 + (3/2)nn^T + (sqrt3/2)[n]_x,
n=(sin psi, cos psi, 0), has entries in Q(sqrt3) when sin,cos rational.
Created 2026-07-16 (DIHEDRAL_FAMILY_NEXT.md Task 1).
"""
import math
from fractions import Fraction as Fr
from itertools import product

from golden_rotations import Rot


class Q2:
    __slots__ = ('a', 'b')

    def __init__(self, a, b=0):
        self.a = a if isinstance(a, Fr) else Fr(a)
        self.b = b if isinstance(b, Fr) else Fr(b)

    def __add__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(s.a + o.a, s.b + o.b)

    def __radd__(s, o):
        return s.__add__(o)

    def __sub__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(s.a - o.a, s.b - o.b)

    def __neg__(s):
        return Q2(-s.a, -s.b)

    def __mul__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        d = o.a * o.a - 3 * o.b * o.b
        return Q2((s.a * o.a - 3 * s.b * o.b) / d, (s.b * o.a - s.a * o.b) / d)

    def sign(s):
        a, b = s.a, s.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        t = a * a - 3 * b * b
        st = 1 if t > 0 else -1
        return st if a > 0 else -st

    def __eq__(s, o):
        return isinstance(o, Q2) and s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __float__(s):
        return float(s.a) + float(s.b) * 3 ** 0.5

    def __repr__(s):
        return f'({s.a}+{s.b}r3)'


ZERO2, ONE2 = Q2(0), Q2(1)
HALF2 = Q2(Fr(1, 2))
R2_2 = Q2(0, Fr(1, 2))    # sqrt(2)/2 = 1/sqrt2 = cos45 = sin45


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def vadd(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def vsub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def vscale(u, t):
    return (u[0] * t, u[1] * t, u[2] * t)


def clip(faces, f, cache):
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


def exact_count_q2(rots, verbose=False, with_labels=False):
    """Direct clone of qtower.exact_count_tower / certify_six.exact_count_config,
    specialized to Q2 field elements directly (no CN wrapper -- see qtower.py's
    docstring rationale, same applies here: a verifier, not a search engine)."""
    one = ONE2
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
        return (tuple((x.a, x.b) for x in comps), c)

    classes = {}
    for k, j, c in planes:
        classes.setdefault(plane_key(k, j, c), []).append((k, j))
    owners_of = [classes[plane_key(k, j, c)] for (k, j, c) in planes]

    B, nB = Q2(4), Q2(-4)
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
        print(f'exact(Q2): arrangement cells = {len(cells)}')

    def centroid_pts(pts):
        kk = Q2(Fr(1, len(pts)))
        s = (ZERO2,) * 3
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


def Rx45():
    return Rot([[ONE2, ZERO2, ZERO2], [ZERO2, R2_2, -R2_2], [ZERO2, R2_2, R2_2]])


def Ry45():
    return Rot([[R2_2, ZERO2, R2_2], [ZERO2, ONE2, ZERO2], [-R2_2, ZERO2, R2_2]])


def Rz45():
    return Rot([[R2_2, -R2_2, ZERO2], [R2_2, R2_2, ZERO2], [ZERO2, ZERO2, ONE2]])


def assert_orthonormal(R):
    m = R.m
    for i in range(3):
        for j in range(3):
            d = sum((m[k][i] * m[k][j] for k in range(3)), ZERO2) \
                - (ONE2 if i == j else ZERO2)
            assert d.sign() == 0, f'orthonormality fail at ({i},{j}): {d!r}'



def S_of(p, q, r):
    """S(psi) over Q(sqrt3) for sin=p/r, cos=q/r (p^2+q^2=r^2)."""
    from fractions import Fraction as Fr
    s, c = Fr(p, r), Fr(q, r)
    Q = lambda a=0, b=0: Q2(a, b)
    H = Fr(1, 2)
    return Rot([
        [Q(-H + 3*s*s/2), Q(3*s*c/2),      Q(0,  c/2)],
        [Q(3*s*c/2),      Q(-H + 3*c*c/2), Q(0, -s/2)],
        [Q(0, -c/2),      Q(0,  s/2),      Q(-H)]])

def count_triple(p, q, r):
    S = S_of(p, q, r); assert_orthonormal(S)
    S2 = Rot([[sum((S.m[i][k]*S.m[k][j] for k in range(3)), ZERO2)
               for j in range(3)] for i in range(3)])
    for i in range(3):
        for j in range(3):
            d = sum((S.m[i][k]*S2.m[k][j] for k in range(3)), ZERO2) - (ONE2 if i==j else ZERO2)
            assert d.sign() == 0, 'S^3 != I'
    IDENT = Rot([[ONE2, ZERO2, ZERO2],[ZERO2, ONE2, ZERO2],[ZERO2, ZERO2, ONE2]])
    return exact_count_q2([IDENT, S, S2])

if __name__ == '__main__':
    import math, time, sys
    total, bd = exact_count_q2([Rot([[ONE2,ZERO2,ZERO2],[ZERO2,ONE2,ZERO2],[ZERO2,ZERO2,ONE2]])]*2)
    assert total == 1 and bd.get(2) == 1, 'self-test failed'
    print('self-test ok (identity pair -> 1 region)')
    TRIPLES=[(0,1,1),(13,84,85),(11,60,61),(9,40,41),(16,63,65),(7,24,25),(12,35,37),
             (5,12,13),(36,77,85),(39,80,89),(8,15,17),(33,56,65),(28,45,53),(3,4,5),
             (48,55,73),(65,72,97),(20,21,29),(21,20,29),(72,65,97),(55,48,73),(4,3,5),
             (45,28,53),(56,33,65),(15,8,17),(80,39,89),(77,36,85),(12,5,13),(35,12,37),
             (24,7,25),(63,16,65),(40,9,41),(60,11,61),(84,13,85),(1,0,1)]
    print(' psi(deg)  (p,q,r)        total  d1  d2  d3')
    for p,q,r in TRIPLES:
        psi=math.degrees(math.asin(p/r))
        t0=time.time(); total,bd=count_triple(p,q,r)
        print(f' {psi:7.3f}  ({p},{q},{r})'.ljust(26)+
              f'{total:5d}  {bd.get(1,0):3d} {bd.get(2,0):3d} {bd.get(3,0):3d}   ({time.time()-t0:.1f}s)',flush=True)
