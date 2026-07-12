#!/usr/bin/env python3
# Working principles: README.md, ALGEBRAIC_SEARCH.md, six_cube_search_results.md
# Postscripts 9/11/12, slide3_q2.py, SLIDE3_SPEC_V2.md. Project index: README.md
"""Edge-concurrence-rich 6-cube search (task: substitute EDGE concurrences
for CORNER concurrences and test competitiveness against the 723 record).

Context this file assumes (see README.md / ALGEBRAIC_SEARCH.md / Postscript
9 for the proofs): the octahedral 3-compound {Rx45,Ry45,Rz45} (n=3, count
67) sits on an EDGE-crossing wall (2 planes of one cube + 2 planes of
another = an edge of cube A crossing an edge of cube B, a 4-fold point),
while the golden/dodecahedral 3-compound (also count 67) sits on a
CORNER-coincidence wall (3+3 planes = a corner of A coincides with a corner
of B). Every n=6 record so far (699/705/717/723) is CORNER-dominated (its
top concurrence is a 9-fold 3+3+3 shared-axis point). This file asks
whether an EDGE-dominated 6-cube config can compete.

This is a NEW file (per the task's hard rule: do not modify validated
files). It copies the Q(sqrt2) field class + exact_count_q2 kernel from
slide3_q2.py verbatim (that file is read-only ground truth) so it can be
extended here (a generic incidence analyzer) without touching the
original. It also imports (read-only, unmodified) golden_rotations.Rot /
rot_from_quat, and slide3_search's rational Farey/quat helpers.

Incidence analyzer
-------------------
`plane_list(rots)` turns a list of Rot objects (any field: Fraction-valued
Q5 with b=0, or Q2) into the 36 face planes (6 per cube: n.x = +-1, n =
column j of the rotation matrix -- exact unit vectors since every Rot here
is validated orthonormal). `find_concurrences` brute-forces ALL C(36,3)
triples of planes, solves the exact 3x3 linear system (Cramer's rule, pure
field arithmetic, no floats), and unions the plane-index sets that solve to
the identical exact point -- so a point where m>=4 planes meet is detected
automatically (it is found by C(m,3) >= 4 different triples, all resolving
to the SAME exact coordinate, and their plane-index sets get unioned by the
dict key). This is fully general: it does not assume the concurrence is an
"edge" or "corner" a priori, it just tallies. Classification (edge vs
corner) is a post-hoc read of the per-cube plane-count signature at each
found point: signature (2,2) = an edge of one cube crossing an edge of
another; signature (3,3[,3...]) = k cube-corners coinciding.

Cost: C(36,3) = 7140 triples/config -- exact but O(few seconds) per config
in Q2, O(sub-second) in plain Fraction. Fine for verifying/classifying a
handful of best candidates; too slow to screen thousands. For screening
(front 2's rational hill-climb) `fast_edge_corner_scan` uses the cheaper
structured method: cube edges are always intersections of 2 NON-opposite
faces (12 edges/cube) and cube corners are always intersections of 3
faces one per axis (8 corners/cube) -- these are the ONLY ways a cube can
contribute exactly 2 or exactly 3 planes to a point (opposite faces are
parallel and never meet), so pairwise edge-line/edge-line and
corner-point/corner-point coincidence tests over all 15 cube-pairs capture
every (2,2)-edge and (3,3[,...])-corner concurrence without the full
C(36,3) cost. Validated against find_concurrences on the known cases below.

Do NOT modify: slide3_q2.py, cube_compound_exact.py, certify_six.py,
exact_search.py, symmetry_search*.py, cube_regions[.cpp], golden_rotations.py,
six_cube_search_results.md. exact_search_results.jsonl is read-only.
"""
import itertools
import json
import math
import random
import subprocess
import sys
import time
from fractions import Fraction as Fr

from golden_rotations import Rot, rot_from_quat
from cube_compound_exact import Q5, ZERO as ZERO5, ONE as ONE5

ENGINE = '/Users/dmi/carroll/cube_regions'
MAXC = 512

# ----------------------------------------------------------- Q2 field, copied
# verbatim from slide3_q2.py (that file is read-only ground truth; copied
# here so this file can extend it -- e.g. genericized incidence code --
# without touching the original, per the hard rule).


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
        return Q2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        d = o.a * o.a - 2 * o.b * o.b
        return Q2((s.a * o.a - 2 * s.b * o.b) / d, (s.b * o.a - s.a * o.b) / d)

    def sign(s):
        a, b = s.a, s.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        t = a * a - 2 * b * b
        st = 1 if t > 0 else -1
        return st if a > 0 else -st

    def __eq__(s, o):
        return isinstance(o, Q2) and s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __float__(s):
        return float(s.a) + float(s.b) * 2 ** 0.5

    def __repr__(s):
        return f'({s.a}+{s.b}r2)'


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
    specialized to Q2 field elements directly (no CN wrapper)."""
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
    corners = list(itertools.product((B, nB), repeat=3))

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


def rot_from_quat_q2(a, b, c, d):
    """Rational rotation matrix (b-part=0) embedded in Q2, built the same
    way as golden_rotations.rot_from_quat but wrapped in Q2 instead of Q5
    so it composes (Rot.__mul__ is field-generic) with Rx45/Ry45/Rz45."""
    n = a * a + b * b + c * c + d * d
    q = lambda x: Q2(Fr(x, n))
    r = Rot([[q(a * a + b * b - c * c - d * d), q(2 * (b * c - a * d)),
              q(2 * (b * d + a * c))],
             [q(2 * (b * c + a * d)), q(a * a - b * b + c * c - d * d),
              q(2 * (c * d - a * b))],
             [q(2 * (b * d - a * c)), q(2 * (c * d + a * b)),
              q(a * a - b * b - c * c + d * d)]])
    return r


# ------------------------------------------------------- generic incidence analyzer

def plane_list(rots):
    """36 face planes n.x = c, n = a column of R.m (field-generic: works for
    Q5-with-b=0 (rational, from golden_rotations.rot_from_quat) or Q2)."""
    planes = []
    for k, R in enumerate(rots):
        cols = [tuple(R.m[i][j] for i in range(3)) for j in range(3)]
        one = None
        for j in range(3):
            for c in (1, -1):
                planes.append((k, j, c, cols[j]))
    return planes


def _det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def _solve3(rows, rhs, one):
    D = _det3(rows)
    if D.sign() == 0:
        return None
    xs = []
    for col in range(3):
        M2 = [list(r) for r in rows]
        for r in range(3):
            M2[r][col] = rhs[r]
        xs.append(_det3(M2) / D)
    return tuple(xs)


def find_concurrences(rots, one, min_mult=4):
    """Exact brute-force: all C(36,3) plane triples, solved exactly; points
    that arise from >=2 distinct triples have multiplicity >=4 (a generic
    triple of planes meets at ONE point and no other plane passes through
    it; extra triples resolving to the identical point mean extra planes
    are concurrent there). Returns list of dicts: point, mult, signature
    (per-cube plane counts sorted desc), by_cube."""
    planes = plane_list(rots)
    n = len(planes)
    pointmap = {}
    for i, j, k in itertools.combinations(range(n), 3):
        ni, nj, nk = planes[i][3], planes[j][3], planes[k][3]
        ci, cj, ck = planes[i][2] * one, planes[j][2] * one, planes[k][2] * one
        pt = _solve3((ni, nj, nk), (ci, cj, ck), one)
        if pt is None:
            continue
        pointmap.setdefault(pt, set()).update((i, j, k))
    results = []
    for pt, idxset in pointmap.items():
        if len(idxset) < min_mult:
            continue
        by_cube = {}
        for idx in idxset:
            kc = planes[idx][0]
            by_cube[kc] = by_cube.get(kc, 0) + 1
        sig = tuple(sorted(by_cube.values(), reverse=True))
        results.append({'point': pt, 'mult': len(idxset), 'sig': sig,
                         'by_cube': by_cube})
    results.sort(key=lambda r: -r['mult'])
    return results


def summarize_concurrences(results):
    max_mult = max((r['mult'] for r in results), default=3)
    edge4 = sum(1 for r in results if r['sig'] == (2, 2))
    corner_types = [r for r in results if all(v == 3 for v in r['sig'])
                     and len(r['sig']) >= 2]
    corner6 = sum(1 for r in corner_types if r['sig'] == (3, 3))
    corner9plus = sum(1 for r in corner_types if len(r['sig']) >= 3)
    other = [r for r in results if r['sig'] != (2, 2) and r not in corner_types]
    return {'max_mult': max_mult, 'edge4_count': edge4,
            'corner6_count': corner6, 'corner9plus_count': corner9plus,
            'other_count': len(other),
            'top_sigs': sorted({r['sig'] for r in results}, reverse=True)[:8]}


# ---------------------------------------------------- fast rational-only screen

def _rat_planes(quats):
    """quats: list of 6 (w,x,y,z) integer tuples. Returns per-cube: 6 planes
    as (normal 3-tuple of Fraction, const +-1) plus the 8 corner points and
    12 edge-lines (as (point_on_line, direction, the 2 defining plane idx))
    -- all EXACT via golden_rotations.rot_from_quat (Q5, b=0 for rational
    quats, so .a is the plain Fraction and .b==0 always)."""
    cubes = []
    for (w, x, y, z) in quats:
        R = rot_from_quat(w, x, y, z)
        cols = [tuple(R.m[i][j].a for i in range(3)) for j in range(3)]
        assert all(R.m[i][j].b == 0 for i in range(3) for j in range(3))
        planes = []  # (axis, sign, normal, const)
        for ax in range(3):
            for s in (1, -1):
                planes.append((ax, s, cols[ax], Fr(s)))
        cubes.append({'cols': cols, 'planes': planes})
    return cubes


def _corner_points(cube):
    cols = cube['cols']
    pts = {}
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1):
                p = tuple(sx * cols[0][i] + sy * cols[1][i] + sz * cols[2][i]
                           for i in range(3))
                pts[(sx, sy, sz)] = p
    return pts


def _edge_lines(cube):
    """12 edges: fix 2 of the 3 axes (adjacent, non-opposite faces), the
    free axis varies -> a line. Returns list of (point0, direction,
    free_axis) using the two FIXED-axis signs to get a point on the line."""
    cols = cube['cols']
    lines = []
    for fixed in itertools.combinations(range(3), 2):
        free = [a for a in range(3) if a not in fixed][0]
        for s0 in (1, -1):
            for s1 in (1, -1):
                p0 = tuple(s0 * cols[fixed[0]][i] + s1 * cols[fixed[1]][i]
                            for i in range(3))
                d = cols[free]
                lines.append({'p0': p0, 'd': d, 'free': free,
                              'fixed': fixed, 'signs': (s0, s1)})
    return lines


def _line_intersect(l1, l2):
    """Exact intersection of two 3D lines (Fraction arithmetic), or None if
    skew/parallel. p1 + t*d1 = p2 + u*d2 solved via least-2-of-3 coords
    then verified on the 3rd."""
    p1, d1 = l1['p0'], l1['d']
    p2, d2 = l2['p0'], l2['d']
    # solve t*d1 - u*d2 = p2 - p1 using two coordinate rows with nonzero det
    rhs = tuple(p2[i] - p1[i] for i in range(3))
    rows = [(0, 1), (0, 2), (1, 2)]
    for a, b in rows:
        det = d1[a] * (-d2[b]) - (-d2[a]) * d1[b]
        if det == 0:
            continue
        t = (rhs[a] * (-d2[b]) - (-d2[a]) * rhs[b]) / det
        u = (d1[a] * rhs[b] - rhs[a] * d1[b]) / det
        c = [-1, -1, -1]
        pt1 = tuple(p1[i] + t * d1[i] for i in range(3))
        pt2 = tuple(p2[i] + u * d2[i] for i in range(3))
        if pt1 == pt2:
            return pt1
        else:
            return None
    return None


def _full_signature_at(point, cubes):
    """Exact per-cube plane-membership tally of `point` against ALL 6
    planes of every cube (not just the 2/3 that generated the candidate) --
    this is what makes the fast scan's classification EXACTLY agree with
    the brute-force find_concurrences: a point discovered via a structural
    edge- or corner-coincidence may have MORE planes through it than the
    2 or 3 that discovered it (e.g. a third cube's face happens to pass
    through the same point), and the true signature must count all of
    them, not just the discovering pair."""
    by_cube = {}
    for k, cube in enumerate(cubes):
        cnt = 0
        for ax, s, normal, const in cube['planes']:
            if sum(normal[i] * point[i] for i in range(3)) == const:
                cnt += 1
        if cnt:
            by_cube[k] = cnt
    return by_cube


def fast_edge_corner_scan(quats):
    """Cheap structured scan: pairwise cube corners (8x8 per pair) and
    pairwise cube edge-lines (12x12 per pair) over all C(6,2)=15 cube
    pairs locate every candidate concurrence point (a point where SOME
    cube contributes >=2 planes -- the only way a cube can contribute an
    edge (2) or corner (3) -- opposite faces are parallel and never meet,
    so this is complete for edge/corner-type points). Each unique
    candidate point is then classified EXACTLY via `_full_signature_at`
    (checked against all 36 planes, not just the discovering ones), so
    the edge4_count / corner6_count / corner9plus_count here agree
    exactly with `summarize_concurrences(find_concurrences(...))` while
    costing O(candidates * 36) instead of O(C(36,3))."""
    n = len(quats)
    cubes = _rat_planes(quats)
    corner_pts = [_corner_points(c) for c in cubes]
    edge_lns = [_edge_lines(c) for c in cubes]

    candidates = set()
    for k in range(n):
        for p in corner_pts[k].values():
            candidates.add(p)
    for k1, k2 in itertools.combinations(range(n), 2):
        for l1 in edge_lns[k1]:
            for l2 in edge_lns[k2]:
                pt = _line_intersect(l1, l2)
                if pt is not None:
                    candidates.add(pt)

    results = []
    for pt in candidates:
        by_cube = _full_signature_at(pt, cubes)
        if sum(by_cube.values()) < 4:
            continue
        sig = tuple(sorted(by_cube.values(), reverse=True))
        results.append({'point': pt, 'mult': sum(by_cube.values()),
                         'sig': sig, 'by_cube': by_cube})

    summ = summarize_concurrences(results) if results else {
        'max_mult': 3, 'edge4_count': 0, 'corner6_count': 0,
        'corner9plus_count': 0, 'other_count': 0, 'top_sigs': []}
    summ['edge_richness'] = summ['edge4_count']
    summ['results'] = results
    return summ


# --------------------------------------------------------------- ./cube_regions

def gcd_reduce(ints):
    g = math.gcd(*[abs(i) for i in ints])
    if g > 1:
        ints = [i // g for i in ints]
    if not any(ints):
        ints = [1, 0, 0, 0]
    return ints


def hamilton(r, q):
    w1, x1, y1, z1 = r
    w2, x2, y2, z2 = q
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return gcd_reduce([w, x, y, z])


def fits_cap(quats, cap=MAXC):
    return all(abs(c) <= cap for grp in quats for c in grp)


def count_quats(quats):
    """One eval via the fast validated C++ engine. quats: list of 6
    (w,x,y,z) int tuples."""
    s = ';'.join(','.join(map(str, g)) for g in quats)
    proc = subprocess.run([ENGINE, '--quats', s], capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    rec = json.loads(proc.stdout.strip().split('\n')[-1])
    if 'error' in rec:
        return None
    return rec


def count_quats_batch(quat_list):
    inp = '\n'.join(';'.join(','.join(map(str, g)) for g in q)
                     for q in quat_list) + '\n'
    proc = subprocess.run([ENGINE, '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
    out = proc.stdout.strip().split('\n') if proc.stdout.strip() else []
    recs = []
    for line in out:
        try:
            recs.append(json.loads(line))
        except Exception:
            recs.append({'error': 'parse'})
    return recs


LOG_PATH = '/Users/dmi/carroll/edge_search.jsonl'


def log_record(rec):
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')


# ============================================================ search front 1a
# EXACT Q(sqrt2): two octahedral 3-compounds {Rx45,Ry45,Rz45} and R.{...},
# R a RATIONAL relative rotation (embedded in Q2). Counted with exact_count_q2
# (no floats anywhere); classified with the full find_concurrences.

def run_front1a(qmax_axis=3, n_random=12, best_n=8):
    from slide3_search import r_candidates
    Rx, Ry, Rz = Rx45(), Ry45(), Rz45()
    cands = r_candidates(qmax_axis=qmax_axis, n_random=n_random)
    print(f'front1a: {len(cands)} R candidates (exact Q(sqrt2), slow path)')
    results = []
    for i, (tag, Rq) in enumerate(cands):
        Rrel = rot_from_quat_q2(*Rq)
        rots = [Rx, Ry, Rz, Rrel * Rx, Rrel * Ry, Rrel * Rz]
        t0 = time.time()
        try:
            total, bd = exact_count_q2(rots)
        except Exception as e:
            print(f'  [{i}] {tag} R={Rq}: FAILED ({e})')
            continue
        conc = find_concurrences(rots, ONE2)
        summ = summarize_concurrences(conc)
        dt = time.time() - t0
        rec = {'front': '1a', 'tag': tag, 'R': list(Rq), 'total': total,
               'by_depth': {str(k): v for k, v in bd.items()}, 'summary': summ,
               'dt': round(dt, 2)}
        rec['summary'] = {k: v for k, v in summ.items()}
        log_record(rec)
        results.append(rec)
        flag = ' <<< BEATS 723' if total > 723 else ''
        print(f'  [{i}/{len(cands)}] {tag:28s} R={Rq}  total={total:4d}  '
              f'max_mult={summ["max_mult"]}  edge4={summ["edge4_count"]:3d}  '
              f'corner6={summ["corner6_count"]}  corner9+={summ["corner9plus_count"]}  '
              f'({dt:.1f}s){flag}')
        if total > 723:
            print('  *** FLAG: total exceeds 723 record, verify independently ***')
    results.sort(key=lambda r: -r['total'])
    print('\nfront1a top results:')
    for r in results[:best_n]:
        print(f'  total={r["total"]:4d}  tag={r["tag"]:28s}  R={r["R"]}  '
              f'summary={r["summary"]}')
    return results


# ============================================================ search front 1b
# RATIONAL Pythagorean-angle approximants to 45deg (tan(theta/2)=p/q close to
# sqrt2-1) combined with a rational R grid; counted by the fast C++ engine,
# ranked by fast_edge_corner_scan richness. Much bigger grid than 1a.

def _pell_convergents(levels=8):
    """Convergents of tan(22.5deg)=sqrt2-1=[0;2,2,2,...]: (q,p) with
    p/q -> sqrt2-1."""
    p0, q0, p1, q1 = 0, 1, 1, 2
    out = [(q0, p0), (q1, p1)]
    for _ in range(levels):
        p2, q2 = 2 * p1 + p0, 2 * q1 + q0
        out.append((q2, p2))
        p0, q0, p1, q1 = p1, q1, p2, q2
    return out


def run_front1b(levels=(4, 5, 6, 7), qmax_axis=6, n_random=40, best_n=15):
    from slide3_search import triple_quats, overlay_quats, r_candidates, fits_cap
    convs = _pell_convergents(8)
    cands = r_candidates(qmax_axis=qmax_axis, n_random=n_random)
    print(f'front1b: {len(convs)} convergent levels available, using levels '
          f'{levels}, {len(cands)} R candidates -> up to '
          f'{len(levels) * len(levels) * len(cands)} configs')
    results = []
    n_done = 0
    t_start = time.time()
    for lvl1 in levels:
        q1, p1 = convs[lvl1]
        for lvl2 in levels:
            q2, p2 = convs[lvl2]
            batch_meta = []
            batch_quats = []
            for tag, Rq in cands:
                quats = overlay_quats(q1, p1, q2, p2, Rq)
                if not fits_cap(quats):
                    continue
                batch_meta.append((lvl1, lvl2, tag, Rq))
                batch_quats.append(quats)
            if not batch_quats:
                continue
            recs = count_quats_batch(batch_quats)
            for (l1, l2, tag, Rq), quats, rec in zip(batch_meta, batch_quats, recs):
                n_done += 1
                if 'error' in rec or 'bounded' not in rec:
                    continue
                total = rec['bounded']
                rich = fast_edge_corner_scan(quats)
                out = {'front': '1b', 'lvl1': l1, 'lvl2': l2, 'tag': tag,
                       'R': list(Rq), 'q1p1': [q1, p1], 'q2p2': [q2, p2],
                       'total': total, 'by_depth': rec.get('by_depth'),
                       'edge4_count': rich['edge4_count'],
                       'corner6_count': rich['corner6_count'],
                       'corner9plus_count': rich['corner9plus_count'],
                       'max_mult': rich['max_mult']}
                log_record(out)
                results.append(out)
                if total > 723:
                    print(f'  *** FLAG total={total} > 723 *** {out}')
    dt = time.time() - t_start
    print(f'front1b: {n_done} configs evaluated in {dt:.1f}s')
    results.sort(key=lambda r: -r['total'])
    print('\nfront1b top by total:')
    for r in results[:best_n]:
        print(f'  total={r["total"]:4d}  lvl=({r["lvl1"]},{r["lvl2"]})  '
              f'tag={r["tag"]:24s} R={r["R"]}  edge4={r["edge4_count"]:3d}  '
              f'corner6={r["corner6_count"]} corner9+={r["corner9plus_count"]}')
    results_by_edge = sorted(results, key=lambda r: -r['edge4_count'])
    print('\nfront1b top by edge-richness (edge4_count):')
    for r in results_by_edge[:best_n]:
        print(f'  edge4={r["edge4_count"]:3d}  total={r["total"]:4d}  '
              f'lvl=({r["lvl1"]},{r["lvl2"]}) tag={r["tag"]:24s} R={r["R"]}')
    return results


# ============================================================ search front 2
# Rational random + hill-climb, ranked by EDGE-richness (not total), to test
# whether edge-rich configs are competitive / whether richness predicts total.

def random_quats(rng, cap=24, n=6):
    out = []
    for _ in range(n):
        while True:
            q = [rng.randint(-cap, cap) for _ in range(4)]
            if any(q):
                break
        out.append(tuple(gcd_reduce(q)))
    return out


def perturb_quats(quats, rng, step=3, cap=MAXC):
    out = []
    for g in quats:
        g2 = list(g)
        i = rng.randrange(4)
        g2[i] += rng.choice([-step, -1, 1, step])
        g2 = gcd_reduce(g2)
        if any(abs(c) > cap for c in g2):
            g2 = list(g)
        out.append(tuple(g2))
    return out


def run_front2_random(n_samples=500, cap=24, seed=2026):
    rng = random.Random(seed)
    results = []
    t0 = time.time()
    for i in range(n_samples):
        quats = random_quats(rng, cap=cap)
        rec = count_quats(quats)
        if rec is None or 'bounded' not in rec:
            continue
        total = rec['bounded']
        rich = fast_edge_corner_scan(quats)
        out = {'front': '2random', 'i': i, 'quats': [list(q) for q in quats],
               'total': total, 'edge4_count': rich['edge4_count'],
               'corner6_count': rich['corner6_count'],
               'corner9plus_count': rich['corner9plus_count'],
               'max_mult': rich['max_mult']}
        log_record(out)
        results.append(out)
        if total > 723:
            print(f'  *** FLAG total={total} > 723 *** {out}')
    dt = time.time() - t0
    print(f'front2random: {len(results)} configs in {dt:.1f}s')
    totals = [r['total'] for r in results]
    edges = [r['edge4_count'] for r in results]
    if len(results) > 3:
        try:
            from scipy.stats import pearsonr
            r_val, p_val = pearsonr(totals, edges)
            print(f'  Pearson r(total, edge4_count) = {r_val:.4f} (p={p_val:.2e})')
        except ImportError:
            pass
    best_total = max(results, key=lambda r: r['total'])
    best_edge = max(results, key=lambda r: r['edge4_count'])
    print(f'  best total: {best_total["total"]} (edge4={best_total["edge4_count"]})')
    print(f'  best edge4: {best_edge["edge4_count"]} (total={best_edge["total"]})')
    return results


def run_front2_hillclimb(n_seeds=6, n_steps=120, cap=24, seed=3000):
    """Greedy hill-climb maximizing edge4_count (NOT total) from several
    random restarts, tracking total at every step so we can see what total
    an edge-maximizing search lands on."""
    rng = random.Random(seed)
    all_results = []
    for s in range(n_seeds):
        cur = random_quats(rng, cap=cap)
        cur_rec = count_quats(cur)
        cur_total = cur_rec['bounded'] if cur_rec else 0
        cur_rich = fast_edge_corner_scan(cur)
        cur_edge = cur_rich['edge4_count']
        best_total_seen = cur_total
        print(f'  seed {s}: start edge4={cur_edge} total={cur_total}')
        for step in range(n_steps):
            cand = perturb_quats(cur, rng, step=rng.choice([1, 2, 3]))
            rec = count_quats(cand)
            if rec is None or 'bounded' not in rec:
                continue
            rich = fast_edge_corner_scan(cand)
            edge = rich['edge4_count']
            total = rec['bounded']
            out = {'front': '2climb', 'seed': s, 'step': step,
                   'quats': [list(q) for q in cand], 'total': total,
                   'edge4_count': edge, 'corner6_count': rich['corner6_count'],
                   'corner9plus_count': rich['corner9plus_count']}
            log_record(out)
            all_results.append(out)
            if total > 723:
                print(f'  *** FLAG total={total} > 723 *** {out}')
            # accept if edge-richer, or equal-richness but higher total (tie-break)
            if edge > cur_edge or (edge == cur_edge and total > cur_total):
                cur, cur_edge, cur_total = cand, edge, total
            best_total_seen = max(best_total_seen, total)
        print(f'  seed {s}: end edge4={cur_edge} total={cur_total}  '
              f'(best total seen along path: {best_total_seen})')
        all_results.append({'front': '2climb_final', 'seed': s,
                             'quats': [list(q) for q in cur], 'total': cur_total,
                             'edge4_count': cur_edge})
    return all_results


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'front1a':
        run_front1a()
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'front1b':
        run_front1b()
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'front2random':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 500
        run_front2_random(n_samples=n)
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'front2climb':
        run_front2_hillclimb()
        raise SystemExit(0)

    print('edge_search.py self-test')

    # --- known case 1: octahedral 3-compound (n=3) must show EDGE (2,2)
    # concurrences and total 67, per README/ALGEBRAIC_SEARCH.md/Postscript 9.
    Rx, Ry, Rz = Rx45(), Ry45(), Rz45()
    total, bd = exact_count_q2([Rx, Ry, Rz])
    print(f'octahedral 3-compound: total={total} bd={bd}')
    assert total == 67
    res = find_concurrences([Rx, Ry, Rz], ONE2)
    summ = summarize_concurrences(res)
    print('  concurrences:', summ)
    assert summ['edge4_count'] > 0, 'expected edge (2,2) concurrences'
    assert summ['corner6_count'] == 0 and summ['corner9plus_count'] == 0, \
        'octahedral compound should have NO corner-type concurrences'

    # --- known case 2: the 723 record (6 cubes) must show CORNER (3,3,3)
    # 9-fold concurrences (two of them), per Postscript 12.
    quats723 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5),
                (2, 1, 1, 1), (1, 1, 1, 1), (5, 2, 2, 2)]
    rots723 = [rot_from_quat(*q) for q in quats723]
    res723 = find_concurrences(rots723, ONE5)
    summ723 = summarize_concurrences(res723)
    print('723 record concurrences (full C(36,3) scan):', summ723)
    assert summ723['corner9plus_count'] >= 2, 'expected >=2 9-fold points'

    # cross-check the fast scanner against the full scanner on 723 -- must
    # agree EXACTLY (same edge4/corner6/corner9plus counts), since the fast
    # scanner now re-derives the full signature at every candidate point.
    fast723 = fast_edge_corner_scan(quats723)
    print('723 record fast scan:', {k: v for k, v in fast723.items()
                                       if k != 'results'})
    assert fast723['corner9plus_count'] == summ723['corner9plus_count'] == 2
    assert fast723['edge4_count'] == summ723['edge4_count']
    assert fast723['corner6_count'] == summ723['corner6_count']
    assert fast723['max_mult'] == summ723['max_mult'] == 9

    # also cross-check the fast scanner on the octahedral n=3 case (rational
    # control: a Pythagorean-angle approximant to 45deg should show edge
    # concurrences too, though not necessarily identical count to the exact
    # wall since it is off the wall by construction)
    print('self-tests pass: fast scanner agrees with full C(36,3) scanner')
