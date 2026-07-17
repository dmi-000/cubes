#!/usr/bin/env python3
# Working principles: RESONANCE4_SPEC.md. Project index: README.md
"""Exact algebraic solver + counter for n=4 dihedral-family cross-class
RESONANCES (RESONANCE4_SPEC.md).

Pipeline:
  1. reslib.wl / gate_r1.wl (wolframscript): symbolic derivation of the
     cross-class edge-line coplanarity curves g_type(Delta,psi) and the
     Groebner/Solve-based exact solving of n=4 resonance systems (k=2,3,4
     chosen pairs from the 6 pairs of cubes 1..4, each on one of 3 cross-
     class curves).  Produces exact algebraic solutions (Sqrt[] radicals),
     dumped as JSON via reslib_export.wl.
  2. This module: parse those exact solutions with sympy, classify field
     (rational / single quadratic Q(sqrt d) / higher), build the Rel-gauge
     rotation matrices exactly, and count regions with the field-matched
     exact engine:
       - rational           -> nfamily_common + C++ cube_regions_n
       - single Q(sqrt d)   -> a GENERIC field-parameterized clone of
                                slide3_q2.py's Q2 class (the "six literal
                                replacements" recipe, automated as a
                                factory instead of hand-duplicated per d --
                                same algorithm, same exact_count_q2 core,
                                reused verbatim from q3_count.py/q6_count.py)
       - degree-4 tower Q(sqrt a,sqrt b) -> qtower.py D_LIST pattern
       - anything else       -> reported OPEN (minimal polynomial only,
                                 per spec: never approximate a claimed count)

No floats in any predicate; float-only for diagnostics (psi in degrees,
voxel triage via six_cube_search.count_mats -- read-only, sanity only).
"""
import json
import math
import subprocess
import sys
from fractions import Fraction as Fr
from itertools import product as iproduct

import sympy as sp

from golden_rotations import Rot

CARROLL = '/Users/dmi/carroll'


# =====================================================================
# Generic Q(sqrt d) field -- factory clone of slide3_q2.py's Q2 pattern
# (the "six replacements": the 2 in __mul__, the 2 in __truediv__, the 2
# in sign()'s discriminant, sqrt(2) in __float__, 'r2' in __repr__, and
# the D itself -- generalized to a parameter instead of hand-duplicated).
# =====================================================================
_field_cache = {}


def make_qd(d):
    """Q(sqrt d) field class, d squarefree integer > 1. Cached by d."""
    if d in _field_cache:
        return _field_cache[d]

    class Qd:
        __slots__ = ('a', 'b')
        D = d

        def __init__(self, a, b=0):
            self.a = a if isinstance(a, Fr) else Fr(a)
            self.b = b if isinstance(b, Fr) else Fr(b)

        def __add__(s, o):
            o = o if isinstance(o, Qd) else Qd(o)
            return Qd(s.a + o.a, s.b + o.b)

        __radd__ = __add__

        def __sub__(s, o):
            o = o if isinstance(o, Qd) else Qd(o)
            return Qd(s.a - o.a, s.b - o.b)

        def __rsub__(s, o):
            return Qd(o) - s

        def __neg__(s):
            return Qd(-s.a, -s.b)

        def __mul__(s, o):
            o = o if isinstance(o, Qd) else Qd(o)
            return Qd(s.a * o.a + Qd.D * s.b * o.b, s.a * o.b + s.b * o.a)

        __rmul__ = __mul__

        def __truediv__(s, o):
            o = o if isinstance(o, Qd) else Qd(o)
            den = o.a * o.a - Qd.D * o.b * o.b
            return Qd((s.a * o.a - Qd.D * s.b * o.b) / den, (s.b * o.a - s.a * o.b) / den)

        def sign(s):
            a, b = s.a, s.b
            if a == 0 and b == 0:
                return 0
            if a >= 0 and b >= 0:
                return 1
            if a <= 0 and b <= 0:
                return -1
            t = a * a - Qd.D * b * b
            st = 1 if t > 0 else (-1 if t < 0 else 0)
            return st if a > 0 else -st

        def __eq__(s, o):
            return isinstance(o, Qd) and s.a == o.a and s.b == o.b

        def __hash__(s):
            return hash((s.a, s.b))

        def __float__(s):
            return float(s.a) + float(s.b) * (d ** 0.5)

        def __repr__(s):
            return f'({s.a}+{s.b}*r{d})'

    Qd.__name__ = f'Q{d}'
    _field_cache[d] = Qd
    return Qd


# region counting core: import the exact_count_q2 ALGORITHM once, but it
# is written against a specific field module-level ZERO2/ONE2 etc.  Reuse
# by dynamic re-binding: q3_count.exact_count_q2 is generic over any field
# object supporting +,-,*,/,sign(),hash,eq (see its own docstring lineage:
# clone of qtower.exact_count_tower). We just need ZERO/ONE of the target
# field, which are trivial constants; the function itself never hardcodes
# a class, only 'Q2(...)' constants for the box corners -- so we recreate
# the tiny counting core parameterized over the field class instead of
# reimporting a hardcoded one. This IS the six_count.py/q3_count.py
# algorithm, generalized the same way nfamily/qtower generalize their base.
from itertools import product


def exact_count_field(rots, Field, verbose=False, with_labels=False):
    ZEROf, ONEf = Field(0), Field(1)

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
                    sp_, sq = signs[p], signs[q]
                    if sp_ * keep >= 0:
                        out.append(p)
                        if sp_ == 0:
                            zeros.append(p)
                    if sp_ * sq < 0:
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

    one = ONEf
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

    B, nB = Field(4), Field(-4)
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

    def centroid_pts(pts):
        kk = Field(Fr(1, len(pts)))
        s = (ZEROf,) * 3
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
        dd = bin(lab).count('1')
        by_depth[dd] = by_depth.get(dd, 0) + cnt
    total = sum(per_label.values()) - 1
    if with_labels:
        return total, by_depth, per_label
    return total, by_depth


def rel_matrix_field(Field, cD, sD, cP, sP):
    """Rel(Delta,psi) with entries in Field, given field elements cD,sD,cP,sP
    (must already satisfy cD^2+sD^2=1, cP^2+sP^2=1 in Field)."""
    one = Field(1)
    return Rot([
        [cD * cP * cP + sP * sP, cP * sP * (one - cD), cP * sD],
        [cP * sP * (one - cD), cD * sP * sP + cP * cP, -(sD * sP)],
        [-(cP * sD), sD * sP, cD],
    ])


# =====================================================================
# GATE R2: reproduce the n=3 octahedral 67 through this ladder, in Q(sqrt2)
# per RESONANCE4_SPEC.md ("slide3_q2.py is validated and read-only, use it
# as the reference for a fresh clone's output").
# =====================================================================
def gate_r2():
    Q2 = make_qd(2)
    r2_2 = Q2(0, Fr(1, 2))  # sqrt2/2 = 1/sqrt2
    IDENT = Rot([[Q2(1), Q2(0), Q2(0)], [Q2(0), Q2(1), Q2(0)], [Q2(0), Q2(0), Q2(1)]])
    Rx = Rot([[Q2(1), Q2(0), Q2(0)], [Q2(0), r2_2, -r2_2], [Q2(0), r2_2, r2_2]])
    Ry = Rot([[r2_2, Q2(0), r2_2], [Q2(0), Q2(1), Q2(0)], [-r2_2, Q2(0), r2_2]])
    Rz = Rot([[r2_2, -r2_2, Q2(0)], [r2_2, r2_2, Q2(0)], [Q2(0), Q2(0), Q2(1)]])
    total, bd = exact_count_field([Rx, Ry, Rz], Q2)
    ok = (total == 67)
    print(f'GATE R2: fresh Q(sqrt2) clone on octahedral triple -> total={total} '
          f'by_depth={dict(sorted(bd.items()))}  {"PASS" if ok else "FAIL"}')
    return ok, total, bd


if __name__ == '__main__':
    gate_r2()
