#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (certified-interval kernel). Project index: README.md
"""CERTIFIED-INTERVAL region count for sub-compounds of the five-cube compound.

The middle option between floating voxels and full exact arithmetic:
filtered/certified numerics in the style of the exact-geometric-computation
paradigm (Yap; CGAL's lazy-exact kernels).  Every number is an interval
enclosure of its true value in Q(sqrt5), carried together with its expression
DAG.  A sign query is answered by the cheapest tier that can CERTIFY it:

  tier 1: double-precision intervals with outward rounding (fast filter)
  tier 2: 200-bit mpmath intervals, DAG re-evaluated (if mpmath installed)
  tier 3: exact Q(sqrt5) arithmetic (imported from cube_compound_exact)

An interval that excludes 0 certifies a sign.  An interval can NEVER certify
a zero, and this configuration is full of structural zeros (vertices exactly
on planes, orthogonal normals), so those escalate to tier 3.  A pure-interval
alternative would replace tier 3 with a separation bound (for x = a + b*sqrt5
of bounded height, |x| below the bound implies x = 0); we use the exact
kernel since we have it.

The arrangement algorithm is the same as cube_compound_exact.py; only the
number type changes.  Point identity (dict/set keys) is routed through the
exact value (computed once per number), so topology is exact by construction;
the interval tiers accelerate the O(points x planes) sign predicates.

Note on honesty: with data this shallow (bounded-height golden-field numbers)
the exact kernel is already cheap, so the filter's speedup is modest; the
technique earns its keep when coordinates come from long derivations where
exact numbers blow up.  Statistics of which tier decided each sign are
printed so the division of labour is visible.

Usage:  python3 cube_compound_interval.py 1 2 3 4 5
"""
import math
import sys
import time
from fractions import Fraction as Fr
from itertools import product

from cube_compound_exact import Q5, ZERO, ONE, build_axes, find_cubes

try:
    from mpmath import iv as _iv
    HAVE_MPMATH = True
except ImportError:
    HAVE_MPMATH = False

STATS = {'tier1': 0, 'tier2': 0, 'tier3': 0, 'zero': 0, 'exact_evals': 0}

_INF = float('inf')


def _up(x):
    return math.nextafter(x, _INF)


def _dn(x):
    return math.nextafter(x, -_INF)


def _int_iv(i):
    f = float(i)
    if abs(i) <= 2 ** 53:
        return (f, f)
    return (_dn(f), _up(f))


_SQRT5 = (_dn(math.sqrt(5.0)), _up(math.sqrt(5.0)))


def _fr_iv(fr):
    nlo, nhi = _int_iv(fr.numerator)
    dlo, dhi = _int_iv(fr.denominator)     # denominator > 0
    return (_dn(min(nlo / dlo, nlo / dhi)), _up(max(nhi / dlo, nhi / dhi)))


def _q5_iv(q):
    alo, ahi = _fr_iv(q.a)
    blo, bhi = _fr_iv(q.b)
    c = [blo * _SQRT5[0], blo * _SQRT5[1], bhi * _SQRT5[0], bhi * _SQRT5[1]]
    return (_dn(alo + min(c)), _up(ahi + max(c)))


def _bad(*vs):
    return any(not math.isfinite(v) for v in vs)


def _add(x, y):
    if _bad(*x, *y):
        return (-_INF, _INF)
    return (_dn(x[0] + y[0]), _up(x[1] + y[1]))


def _sub(x, y):
    if _bad(*x, *y):
        return (-_INF, _INF)
    return (_dn(x[0] - y[1]), _up(x[1] - y[0]))


def _mul(x, y):
    if _bad(*x, *y):
        return (-_INF, _INF)
    c = [x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1]]
    return (_dn(min(c)), _up(max(c)))


def _div(x, y):
    if _bad(*x, *y) or y[0] <= 0.0 <= y[1]:
        return (-_INF, _INF)
    c = [x[0] / y[0], x[0] / y[1], x[1] / y[0], x[1] / y[1]]
    return (_dn(min(c)), _up(max(c)))


class CN:
    """Certified number: float interval + expression DAG + lazy exact value."""
    __slots__ = ('iv', 'node', '_exact', '_hash')

    def __init__(self, iv_, node, exact=None):
        self.iv = iv_
        self.node = node
        self._exact = exact
        self._hash = None

    @staticmethod
    def leaf(q):
        return CN(_q5_iv(q), ('q', q), q)

    def exact(self):
        if self._exact is None:
            op, a, b = self.node
            STATS['exact_evals'] += 1
            ea, eb = a.exact(), b.exact()
            self._exact = (ea + eb if op == '+' else
                           ea - eb if op == '-' else
                           ea * eb if op == '*' else
                           ea / eb)
        return self._exact

    def __add__(s, o):
        return CN(_add(s.iv, o.iv), ('+', s, o))

    def __sub__(s, o):
        return CN(_sub(s.iv, o.iv), ('-', s, o))

    def __mul__(s, o):
        return CN(_mul(s.iv, o.iv), ('*', s, o))

    def __truediv__(s, o):
        return CN(_div(s.iv, o.iv), ('/', s, o))

    def __neg__(s):
        return CN((-s.iv[1], -s.iv[0]), ('-', CN.leaf(ZERO), s))

    def sign(self):
        lo, hi = self.iv
        if lo > 0.0:
            STATS['tier1'] += 1
            return 1
        if hi < 0.0:
            STATS['tier1'] += 1
            return -1
        if HAVE_MPMATH:
            v = self._reeval_iv()
            if v is not None:
                if v.a > 0:
                    STATS['tier2'] += 1
                    return 1
                if v.b < 0:
                    STATS['tier2'] += 1
                    return -1
        s = self.exact().sign()
        STATS['tier3'] += 1
        if s == 0:
            STATS['zero'] += 1
        return s

    def _reeval_iv(self, prec=200):
        old = _iv.prec
        _iv.prec = prec
        memo = {}

        def ev(n):
            key = id(n)
            if key in memo:
                return memo[key]
            op = n.node[0]
            if op == 'q':
                q = n.node[1]
                r = (_iv.mpf(q.a.numerator) / q.a.denominator +
                     _iv.mpf(q.b.numerator) / q.b.denominator * _iv.sqrt(5))
            else:
                a, b = ev(n.node[1]), ev(n.node[2])
                try:
                    r = (a + b if op == '+' else a - b if op == '-' else
                         a * b if op == '*' else a / b)
                except ZeroDivisionError:
                    r = None
                if r is None or (op == '/' and (b.a <= 0 <= b.b)):
                    r = None
            memo[key] = r
            return r

        try:
            return ev(self)
        finally:
            _iv.prec = old

    # identity via the exact value: topology is exact by construction
    def __eq__(s, o):
        return isinstance(o, CN) and s.exact() == o.exact()

    def __hash__(s):
        if s._hash is None:
            s._hash = hash(s.exact())
        return s._hash


# ---------------------------------------------------------------- geometry
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
        key = frozenset((p, q))
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


EXPECT = {1: 1, 2: 13, 3: 67, 4: 177, 5: 351}


def run(N):
    t0 = time.time()
    for k in STATS:
        STATS[k] = 0
    axes_q = build_axes()
    triples = find_cubes(axes_q)[:N]
    used = [i for t in triples for i in t]
    axes = {i: tuple(CN.leaf(c) for c in axes_q[i]) for i in used}
    one = CN.leaf(ONE)

    planes = [(ai, c) for ai in used for c in (1, -1)]
    B = CN.leaf(Q5(4))
    nB = CN.leaf(Q5(-4))
    corners = list(product((B, nB), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] is val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (p[a].iv[0], p[b].iv[0]))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cells = [[(('box', i, s), box_face(i, v))
              for i in range(3) for s, v in ((1, B), (-1, nB))]]

    for pid, (ai, c) in enumerate(planes):
        n = axes[ai]
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

    def centroid(cell):
        pts = {p for _, loop in cell for p in loop}
        k = CN.leaf(Q5(Fr(1, len(pts))))
        s = (CN.leaf(ZERO),) * 3
        for p in pts:
            s = vadd(s, p)
        return vscale(s, k)

    def label(w):
        lab = 0
        for k, t in enumerate(triples):
            if all((dot(axes[ai], w) - one).sign() < 0 and
                   (dot(axes[ai], w) + one).sign() > 0 for ai in t):
                lab |= 1 << k
        return lab

    labs = [label(centroid(c)) for c in cells]

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

    plane_cube = {}
    for pid, (ai, c) in enumerate(planes):
        (k, t) = next((k, t) for k, t in enumerate(triples) if ai in t)
        plane_cube[pid] = (k, [a for a in t if a != ai])

    for (pid, verts), cs in groups.items():
        assert len(cs) == 2, f'facet shared by {len(cs)} cells'
        a, b = cs
        k, others = plane_cube[pid]
        pl = list(verts)
        s = (CN.leaf(ZERO),) * 3
        for p in pl:
            s = vadd(s, p)
        w = vscale(s, CN.leaf(Q5(Fr(1, len(pl)))))
        real = all((dot(axes[ai], w) - one).sign() < 0 and
                   (dot(axes[ai], w) + one).sign() > 0 for ai in others)
        if real:
            assert labs[a] ^ labs[b] == 1 << k
        else:
            assert labs[a] == labs[b]
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    comps = set()
    for ci in range(len(cells)):
        comps.add((labs[ci], find(ci)))
    per_label = {}
    for lab, _r in comps:
        per_label[lab] = per_label.get(lab, 0) + 1
    assert per_label.get(0, 0) == 1
    total = sum(per_label.values()) - 1
    ok = 'PASS' if total == EXPECT.get(N) else f'FAIL (expected {EXPECT.get(N)})'
    dt = time.time() - t0
    nsign = STATS['tier1'] + STATS['tier2'] + STATS['tier3']
    print(f'N={N}: bounded regions = {total}   [{ok}]  cells={len(cells)}  '
          f'{dt:.1f}s')
    print(f'      signs: {nsign} total | tier1 (float iv): {STATS["tier1"]} '
          f'| tier2 (200-bit iv): {STATS["tier2"]} '
          f'| tier3 (exact): {STATS["tier3"]} (of which true zeros: '
          f'{STATS["zero"]}) | exact node evals: {STATS["exact_evals"]}')
    return total


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    for arg in sys.argv[1:]:
        run(int(arg))
