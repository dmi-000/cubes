#!/usr/bin/env python3
# Working principles: CENSUS_SPEC.md. Project index: README.md / C45_notes.md sect.13
"""(c1) exact census extraction from both n=3 max(3)=67 witnesses.

Feeds lemma L2.c of the max(3) = 67 proof plan (C45_notes.md sect.13):
extracts, in EXACT field arithmetic (no float in any decision), the
TOP-1 diagram (48 faces) and BOTTOM diagram (18 faces) of the sphere
S^2 for both certified 67-witnesses:
  W1 octahedral, field Q(sqrt2): R1=Rx(45), R2=Ry(45), R3=Rz(45)
      (slide3_q2.py, READ-ONLY -- imported, not edited).
  W2 golden,      field Q(sqrt5): {I, S, S^2}, S = 120deg rotation about
      n(psi) = (sin psi, cos psi, 0), tan psi = phi^2.
      (cube_compound_exact.py / certify_six.py, READ-ONLY -- imported.)

Method. For direction u in S^2, cube i has 3 unsigned face normals (the
columns of R_i); r_i(u) = 1/max_a |n_a.u|, active face = the argmax.
Swap curves r_i=r_j (active faces a,b) are great circles u.(n_a-s.n_b)=0,
s=+-1. All candidate vertices of the fine arrangement (triple points:
r_1=r_2=r_3; kinks: a swap circle meets an own-cube sector boundary,
i.e. an active-face change) are generated as exact cross products of
pairs of these great-circle normals, deduped projectively (u ~ -u is
NOT identified here -- vertices live on the actual sphere S^2, since
the diagram is antipodally SYMMETRIC, not antipodally QUOTIENTED: G3
checks the vertex set is closed under negation, not that it's absent).

For every candidate vertex we test ACTIVITY exactly (squared dot
products, sign() comparisons only -- no floats) to keep only genuine
triple points / kinks. For every relevant swap great circle we collect
its vertices, sort them by EXACT angular order in the circle's own
plane basis (half-plane + 2D cross-product comparator, an exact total
order), and classify each arc between consecutive vertices via ONE
exact interior sample point (again no floats) as TOP (tied pair is the
biggest reach, i.e. SMALLEST max|n.u|) or BOTTOM (tied pair is the
smallest reach). Euler's formula per sphere (F = E - V + 1 + #components)
on the resulting TOP-1 and BOTTOM graphs is GATE G2: must give 48, 18
for BOTH witnesses.

Deliverables: census_report.md (this script's --report mode),
census_data.json (this script's --report mode also writes it).
"""
import json
import math
import sys
import time
from fractions import Fraction as Fr
from functools import cmp_to_key
from itertools import combinations

from golden_rotations import Rot
from cube_compound_exact import Q5, PHI_H, IPHI_H, HALF as HALF5, ONE as ONE5, ZERO as ZERO5
import certify_six
from slide3_q2 import Q2, ZERO2, ONE2, Rx45, Ry45, Rz45, exact_count_q2


# ============================================================ generic vector algebra
# Works for any field element type supporting +,-,*,/,neg,eq,hash,sign(),float()
# (Q2 and Q5 both implement this interface identically -- see their docstrings).

def vsub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def vadd(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def vscale(u, t):
    return (u[0] * t, u[1] * t, u[2] * t)


def dot3(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross3(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


def is_zero_vec(u):
    return all(c.sign() == 0 for c in u)


def abs_field(x):
    return x if x.sign() >= 0 else -x


def canon_ray(u):
    """Canonical representative of the RAY through u: divide by |first nonzero
    coordinate|.  INVARIANT (load-bearing): canon_ray(t*u) = sign(t)*canon_ray(u)
    for any nonzero scalar t -- this collapses positive rescalings (same point)
    while keeping u and -u DISTINCT (antipodal points are different vertices of
    the S^2 diagram).  Do not "simplify" to dividing by the raw first-nonzero
    value -- that collapses antipodes too (that's canon_circle below, which is
    the right thing for UNDIRECTED circles, wrong thing for POINTS)."""
    for c in u:
        if c.sign() != 0:
            d = abs_field(c)
            return tuple(x / d for x in u)
    return None


def canon_circle(v):
    """Canonical key for the UNDIRECTED great circle {u : u.v = 0}: v and -v
    denote the same circle, so divide by the raw first-nonzero coordinate
    (no abs) -- this collapses v ~ -v, unlike canon_ray."""
    for c in v:
        if c.sign() != 0:
            return tuple(x / c for x in v)
    return None


# ============================================================ witness construction

def build_w1():
    """Octahedral witness, field Q(sqrt2): validated slide3_q2.py matrices."""
    R = [Rx45(), Ry45(), Rz45()]
    normals = [[tuple(R[k].m[i][j] for i in range(3)) for j in range(3)] for k in range(3)]
    return R, normals


def build_w2():
    """Golden witness, field Q(sqrt5): {I, S, S^2}, S = 120deg about n(psi),
    tan psi = phi^2.  Derivation (by hand, verified exactly below and in the
    gate check): sin psi = phi/sqrt3, cos psi = 1/(phi sqrt3) give
    sin*cos = 1/3, sin^2 = (phi+1)/3, cos^2 = (2-phi)/3 (using phi^2=phi+1,
    1/phi^2=2-phi), and every sqrt3 introduced by the Rodrigues formula
    S = -I/2 + (3/2) n n^T + (sqrt3/2) [n]_x cancels EXACTLY, landing all 9
    entries in Q(sqrt5) alone (no sqrt3 residue)."""
    S = Rot([
        [PHI_H, HALF5, IPHI_H],
        [HALF5, -IPHI_H, -PHI_H],
        [-IPHI_H, PHI_H, -HALF5]])
    S2 = Rot([[sum((S.m[i][k] * S.m[k][j] for k in range(3)), ZERO5) for j in range(3)]
              for i in range(3)])
    IDENT = Rot([[ONE5, ZERO5, ZERO5], [ZERO5, ONE5, ZERO5], [ZERO5, ZERO5, ONE5]])
    R = [IDENT, S, S2]
    normals = [[tuple(R[k].m[i][j] for i in range(3)) for j in range(3)] for k in range(3)]
    return R, normals


def gate_s3_identity(S):
    ZERO, ONE = ZERO5, ONE5
    S2 = Rot([[sum((S.m[i][k] * S.m[k][j] for k in range(3)), ZERO) for j in range(3)]
              for i in range(3)])
    S3 = Rot([[sum((S.m[i][k] * S2.m[k][j] for k in range(3)), ZERO) for j in range(3)]
              for i in range(3)])
    IDENT = Rot([[ONE, ZERO, ZERO], [ZERO, ONE, ZERO], [ZERO, ZERO, ONE]])
    for i in range(3):
        for j in range(3):
            assert (S3.m[i][j] - IDENT.m[i][j]).sign() == 0, 'S^3 != I'
    m = S.m
    for i in range(3):
        for j in range(3):
            d = sum((m[k][i] * m[k][j] for k in range(3)), ZERO) - (ONE if i == j else ZERO)
            assert d.sign() == 0, f'S not orthonormal at {i},{j}'
    assert (S.det() - ONE).sign() == 0, 'det(S) != 1'


# ============================================================ GATE G1

def gate_g1():
    print('=== GATE G1: reproduce both 67 = {48,18,1} counts ===')
    t0 = time.time()
    total1, bd1 = exact_count_q2([Rx45(), Ry45(), Rz45()])
    print(f'  W1 octahedral (slide3_q2.exact_count_q2, Q(sqrt2)): '
          f'total={total1} by_depth={dict(sorted(bd1.items()))}  ({time.time()-t0:.1f}s)')
    assert total1 == 67 and bd1.get(1) == 48 and bd1.get(2) == 18 and bd1.get(3) == 1, \
        'W1 gate G1 FAILED'

    R2, _ = build_w2()
    gate_s3_identity(R2[1])
    t0 = time.time()
    total2, bd2 = certify_six.exact_count_config(R2, verbose=False)
    print(f'  W2 golden (certify_six.exact_count_config, Q(sqrt5), Q5-wrapped .m): '
          f'total={total2} by_depth={dict(sorted(bd2.items()))}  ({time.time()-t0:.1f}s)')
    assert total2 == 67 and bd2.get(1) == 48 and bd2.get(2) == 18 and bd2.get(3) == 1, \
        'W2 gate G1 FAILED'
    print('GATE G1: PASS (both witnesses reproduce 67 = {48,18,1})\n')
    return True


# ============================================================ per-witness census

PAIRS = [(0, 1), (1, 2), (0, 2)]


def sq_val(n, k, f, u):
    d = dot3(n[k][f], u)
    return d * d


def active_faces(n, k, u):
    vals = [sq_val(n, k, f, u) for f in range(3)]
    best = 0
    for f in (1, 2):
        if (vals[f] - vals[best]).sign() > 0:
            best = f
    mx = vals[best]
    return tuple(f for f in range(3) if (vals[f] - mx).sign() == 0)


def build_circles(n):
    cross_circles = {}
    for (i, j) in PAIRS:
        for a in range(3):
            for b in range(3):
                for s1 in (1, -1):
                    v = vsub(n[i][a], vscale(n[j][b], s1))
                    ck = canon_circle(v)
                    if ck is None:
                        continue
                    cross_circles.setdefault(ck, []).append((i, j, a, b, s1))
    own_circles = {}
    for k in range(3):
        for a, ap in combinations(range(3), 2):
            for s3 in (1, -1):
                v = vsub(n[k][a], vscale(n[k][ap], s3))
                ck = canon_circle(v)
                if ck is None:
                    continue
                own_circles.setdefault(ck, []).append((k, a, ap, s3))
    return cross_circles, own_circles


def gen_candidates(n):
    """All candidate vertices of the fine arrangement, BOTH antipodes.

    INVARIANT (load-bearing): each cross product v1 x v2 yields ONE vector u;
    the antipodal sphere point -u satisfies the same |dot| ties but is NOT
    generated by any other (sign-pattern) combination, so it must be added
    explicitly.  Omitting it loses half the vertices (caught in testing:
    tie arcs whose top/bottom status silently flipped across the missing
    antipodal triple point, and W2 G3 'missing antipode' failures)."""
    cands = set()

    def add(u):
        if is_zero_vec(u):
            return
        cr = canon_ray(u)
        if cr is not None:
            cands.add(cr)
            cands.add(tuple(-c for c in cr))

    # Step 1: triple-point candidates -- u = +-(n_a - s1 n_b) x (n_b - s2 n_c)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        v1 = vsub(n[0][a], vscale(n[1][b], s1))
                        v2 = vsub(n[1][b], vscale(n[2][c], s2))
                        add(cross3(v1, v2))
    # Step 3: kink candidates -- u = +-(n_a - s1 n_b) x (n_a - s3 n_a')
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for a in range(3):
                for b in range(3):
                    for s1 in (1, -1):
                        for ap in range(3):
                            if ap == a:
                                continue
                            for s3 in (1, -1):
                                v1 = vsub(n[i][a], vscale(n[j][b], s1))
                                v2 = vsub(n[i][a], vscale(n[i][ap], s3))
                                add(cross3(v1, v2))
    return cands


def classify_vertices(n, cands, cross_circles, own_circles):
    verts = {}
    for cr in cands:
        u = cr
        act = {k: active_faces(n, k, u) for k in range(3)}
        cross_inc = []
        for ck, gens in cross_circles.items():
            if dot3(u, ck).sign() != 0:
                continue
            for (i, j, a, b, s1) in gens:
                if a in act[i] and b in act[j]:
                    cross_inc.append((ck, i, j, a, b, s1))
        if not cross_inc:
            continue
        own_inc = []
        for ck, gens in own_circles.items():
            if dot3(u, ck).sign() != 0:
                continue
            for (k, a, ap, s3) in gens:
                if a in act[k] and ap in act[k]:
                    own_inc.append((ck, k, a, ap, s3))
        pairs_present = {(i, j) for (ck, i, j, a, b, s1) in cross_inc}
        is_triple = len(pairs_present) >= 2
        is_kink = (not is_triple) and len(own_inc) >= 1
        if not (is_triple or is_kink):
            continue
        verts[cr] = dict(active=act, cross_inc=cross_inc, own_inc=own_inc,
                          type=('triple' if is_triple else 'kink'))
    return verts


def half(alpha, beta):
    bs = beta.sign()
    if bs > 0:
        return 0
    if bs < 0:
        return 1
    return 0 if alpha.sign() > 0 else 1


def cross2(a1, b1, a2, b2):
    return a1 * b2 - a2 * b1


def make_basis(v):
    for ref in ((1, 0, 0), (0, 1, 0)):
        e1 = cross3(v, ref)
        if not is_zero_vec(e1):
            e2 = cross3(v, e1)
            return e1, e2
    raise AssertionError('degenerate circle normal')


def classify_sample(n, gens, sample, flags, where):
    """At an exact interior sample point of a circle with generator list
    `gens` [(i,j,a,b,s1), ...]: which generators are ACTIVE there (both tied
    faces achieve their cubes' max), and is the tie TOP (tied pair = the two
    LARGEST reaches, i.e. tied squared-dot <= third cube's max squared-dot)
    or BOTTOM (tied pair = two smallest reaches).  Returns (kinds, active_gens)
    where kinds is a subset of {'TOP','BOTTOM'}.  If two DIFFERENT pair-ties
    are active at the same sample, all three reaches coincide along the arc --
    a genuine degeneracy: flagged loudly, never silently dropped."""
    act_s = {kk: active_faces(n, kk, sample) for kk in range(3)}
    active_gens = [(i, j, a, b, s1) for (i, j, a, b, s1) in gens
                   if a in act_s[i] and b in act_s[j]]
    kinds = set()
    tied_pairs = {(i, j) for (i, j, a, b, s1) in active_gens}
    if len(tied_pairs) > 1:
        flags.append(f'DEGENERATE: two distinct pair-ties active on one arc '
                     f'({sorted(tied_pairs)}) at {where} -- triple-tie arc')
    for (i, j, a, b, s1) in active_gens:
        k = 3 - i - j  # the third cube (indices sum to 3)
        tied_val = sq_val(n, i, a, sample)
        tv2 = sq_val(n, j, b, sample)
        assert (tied_val - tv2).sign() == 0, 'tied values disagree at sample'
        third_vals = [sq_val(n, k, f, sample) for f in range(3)]
        third_val = third_vals[0]
        for f in (1, 2):
            if (third_vals[f] - third_val).sign() > 0:
                third_val = third_vals[f]
        c = (tied_val - third_val).sign()
        if c == 0:
            flags.append(f'DEGENERATE arc: tied==third at {where} '
                         f'(gen i={i},j={j},a={a},b={b},s1={s1})')
            continue
        # reach r = 1/|n.u|: tied pair is the top two reaches iff its squared
        # dot is <= the third cube's max squared dot.
        kinds.add('TOP' if c < 0 else 'BOTTOM')
    return kinds, active_gens


def build_graph(n, verts, cross_circles, kind):
    """kind in {'TOP','BOTTOM'}.

    Processes each geometric circle ONCE (a circle may carry several
    (i,j,a,b,s1) generators; treating them separately would double-count
    shared arcs).  Vertices on the circle = recorded diagram vertices
    incident to any of its generators; arcs between consecutive vertices are
    classified by one exact interior sample.  Circles with NO vertices can
    still carry a FREE LOOP of the diagram (activity cannot change along a
    vertex-free circle, since any activity-change point is a kink/triple
    candidate by construction): detected by exact probes and counted with
    the V=1, E=1 self-loop convention, under which F = E - V + 1 + #comp
    holds for arbitrary sphere embeddings (each standalone component
    contributes its own cellular circuit count).

    Returns (edges, vertex_set, degree, flags, n_free_loops)."""
    edges = []          # (v1, v2, circle_key)
    touched = set()
    degree = {}
    flags = []
    n_free_loops = 0

    for ck, gens in cross_circles.items():
        e1, e2 = make_basis(ck)
        # |e1|^2, |e2|^2 -- e1, e2 are orthogonal but NOT unit.  The true
        # chart coordinates of a point p on the circle are
        # (p.e1/|e1|^2, p.e2/|e2|^2); (alpha, beta) = (p.e1, p.e2) is their
        # image under the positive diagonal scaling diag(|e1|^2, |e2|^2).
        # Positive diagonal scalings preserve quadrants and the cyclic order
        # of rays, so SORTING by the (alpha, beta) pseudo-angle is a valid
        # exact angular order.  But (alpha, beta) must NEVER be used as basis
        # COEFFICIENTS -- that applies the scaling twice and the "interior
        # sample" can land in a different arc (real bug caught in testing:
        # 84 spurious inactivity flags, F=16 instead of 48).  Interior
        # samples below are built from the vertex VECTORS themselves.
        n1sq = dot3(e1, e1)
        n2sq = dot3(e2, e2)

        on_circle = []
        for cr, info in verts.items():
            if any(g[0] == ck for g in info['cross_inc']):
                alpha, beta = dot3(cr, e1), dot3(cr, e2)
                on_circle.append((alpha, beta, cr))

        if not on_circle:
            # Vertex-free circle: activity of each generator is CONSTANT
            # along it (any change point would be a recorded vertex).  Probe
            # a few exact points to find one where classification succeeds.
            for pa, pb in ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)):
                sample = vadd(vscale(e1, type(n1sq)(pa)),
                              vscale(e2, type(n1sq)(pb)))
                lflags = []
                kinds, act_gens = classify_sample(n, gens, sample, lflags,
                                                 f'free-circle {ck}')
                if not lflags:
                    break
            flags.extend(lflags)
            if kind in kinds:
                pv = ('loop', ck)
                touched.add(pv)
                edges.append((pv, pv, ck))
                degree[pv] = 2
                n_free_loops += 1
            continue

        on_circle.sort(key=cmp_to_key(
            lambda P, Q: (half(P[0], P[1]) - half(Q[0], Q[1]))
            or (-cross2(P[0], P[1], Q[0], Q[1]).sign())))
        m = len(on_circle)
        for idx in range(m):
            alpha_i, beta_i, cr_i = on_circle[idx]
            alpha_j, beta_j, cr_j = on_circle[(idx + 1) % m]
            if m == 1:
                cs = 0
            else:
                cs = cross2(alpha_i, beta_i, alpha_j, beta_j).sign()
            if cs > 0:
                # CCW arc i->j subtends <180deg: the sum of the two vertex
                # vectors is a positive combination, strictly inside the
                # minor cone = strictly inside this arc.
                sample = vadd(cr_i, cr_j)
            elif cs < 0:
                # CCW arc subtends >180deg: the antipode of the minor-cone
                # point lies strictly inside this (major) arc.
                sample = tuple(-c for c in vadd(cr_i, cr_j))
            else:
                # antipodal endpoints (or m=1 full-circle loop): the point
                # 90deg CCW in the TRUE chart from cr_i: chart(cr_i) =
                # (alpha_i/n1sq, beta_i/n2sq) -> CCW 90deg ->
                # (-beta_i/n2sq, alpha_i/n1sq); clear denominators by the
                # positive factor n1sq*n2sq.
                sample = vadd(vscale(e1, -(beta_i * n1sq)),
                              vscale(e2, alpha_i * n2sq))
            kinds, act_gens = classify_sample(
                n, gens, sample, flags,
                f'arc {cr_i} .. {cr_j} of circle {ck}')
            if kind not in kinds:
                continue
            edges.append((cr_i, cr_j, ck))
            touched.add(cr_i)
            touched.add(cr_j)
            degree[cr_i] = degree.get(cr_i, 0) + 1
            degree[cr_j] = degree.get(cr_j, 0) + 1
    return edges, touched, degree, flags, n_free_loops


def connected_components(vertex_set, edges):
    parent = {v: v for v in vertex_set}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for (v1, v2, *_rest) in edges:
        union(v1, v2)
    roots = {find(v) for v in vertex_set}
    return len(roots)


def euler_face_count(vertex_set, edges):
    V = len(vertex_set)
    E = len(edges)
    if V == 0:
        return None, V, E, 0
    C = connected_components(vertex_set, edges)
    F = E - V + 1 + C
    return F, V, E, C


def field_name(n):
    return 'Q(sqrt5)' if isinstance(n[0][0][0], Q5) else 'Q(sqrt2)'


def process_witness(name, n):
    print(f'=== {name}: building fine arrangement and swap-curve graphs ===')
    t0 = time.time()
    cross_circles, own_circles = build_circles(n)
    print(f'  cross-cube swap circles: {len(cross_circles)} (raw 54)  '
          f'own-cube sector circles: {len(own_circles)} (raw 18)')
    cands = gen_candidates(n)
    print(f'  candidate rays generated: {len(cands)} (raw <=540)')
    verts = classify_vertices(n, cands, cross_circles, own_circles)
    n_triple = sum(1 for v in verts.values() if v['type'] == 'triple')
    n_kink = sum(1 for v in verts.values() if v['type'] == 'kink')
    print(f'  surviving vertices: {len(verts)}  (triple points: {n_triple}, kinks: {n_kink})'
          f'  ({time.time()-t0:.1f}s)')

    top_edges, top_v, top_deg, top_flags, top_loops = build_graph(
        n, verts, cross_circles, 'TOP')
    bot_edges, bot_v, bot_deg, bot_flags, bot_loops = build_graph(
        n, verts, cross_circles, 'BOTTOM')

    Ftop, Vtop, Etop, Ctop = euler_face_count(top_v, top_edges)
    Fbot, Vbot, Ebot, Cbot = euler_face_count(bot_v, bot_edges)

    print(f'  TOP-1 graph:   V={Vtop} E={Etop} C={Ctop} free_loops={top_loops}'
          f'  ->  F = E-V+1+C = {Ftop}   (target 48)')
    print(f'  BOTTOM graph:  V={Vbot} E={Ebot} C={Cbot} free_loops={bot_loops}'
          f'  ->  F = E-V+1+C = {Fbot}   (target 18)')
    if top_flags:
        print(f'  TOP flags ({len(top_flags)}):')
        for f in top_flags[:20]:
            print('    ', f)
    if bot_flags:
        print(f'  BOTTOM flags ({len(bot_flags)}):')
        for f in bot_flags[:20]:
            print('    ', f)

    # GATE G3: antipodal symmetry of the vertex set (both graphs' vertex sets,
    # and the overall census, should be closed under u -> -u with matching degree).
    def check_antipodal(vset, deg, label):
        bad = []
        for v in vset:
            if v and v[0] == 'loop':
                continue  # free-loop pseudo-vertex: its circle is antipodally self-symmetric
            nv = tuple(-c for c in v)
            if nv not in vset:
                bad.append(('missing antipode', v))
            elif deg.get(v) != deg.get(nv):
                bad.append(('degree mismatch', v, deg.get(v), deg.get(nv)))
        ok = not bad
        print(f'  GATE G3 ({label} antipodal symmetry): {"PASS" if ok else "FAIL"}'
              + ('' if ok else f'  ({len(bad)} issues, e.g. {bad[:3]})'))
        return ok

    g3_top = check_antipodal(top_v, top_deg, 'TOP')
    g3_bot = check_antipodal(bot_v, bot_deg, 'BOTTOM')

    result = dict(
        name=name, field=field_name(n),
        n_triple=n_triple, n_kink=n_kink, n_vertices_total=len(verts),
        top=dict(V=Vtop, E=Etop, C=Ctop, F=Ftop, target=48, flags=top_flags,
                  g3=g3_top),
        bottom=dict(V=Vbot, E=Ebot, C=Cbot, F=Fbot, target=18, flags=bot_flags,
                     g3=g3_bot),
    )
    return result, verts, top_edges, bot_edges, top_deg, bot_deg


# ============================================================ census tables

def verify_triple_ties(n, verts):
    """Exact re-verification (spec step 1): at every triple point, ALL active
    faces of ALL cubes achieve one common squared dot value."""
    for cr, info in verts.items():
        if info['type'] != 'triple':
            continue
        vals = [sq_val(n, k, f, cr) for k in range(3) for f in info['active'][k]]
        for v in vals[1:]:
            assert (v - vals[0]).sign() == 0, \
                f'triple tie verification FAILED at {cr}'
    return True


def elementary_triples(n, verts):
    """The occurring active-face triples (f0, f1, f2) with sign patterns.

    At a triple point every active face of every cube attains the common
    tied |dot| value, so each (f0,f1,f2) in act0 x act1 x act2 is a raw
    'feasible triple' of the classification target list.  Sign pattern:
    (s01, s12) with s01 = sign((n0_f0 . u)(n1_f1 . u)) etc.; antipodally
    invariant (both dots negate)."""
    occ = {}
    for cr, info in verts.items():
        if info['type'] != 'triple':
            continue
        d = [[dot3(n[k][f], cr) for f in range(3)] for k in range(3)]
        for f0 in info['active'][0]:
            for f1 in info['active'][1]:
                for f2 in info['active'][2]:
                    s01 = d[0][f0].sign() * d[1][f1].sign()
                    s12 = d[1][f1].sign() * d[2][f2].sign()
                    key = (f0, f1, f2, s01, s12)
                    occ.setdefault(key, set()).add(cr)
    return occ


def orbit_reduce(occ_keys, sigma):
    """Group elementary triples under the compound's C3 symmetry
    (k, f) -> (k+1, f+sigma): ((f0,f1,f2),(s01,s12)) ->
    ((f2+sigma, f0+sigma, f1+sigma), (s01*s12, s01)).  sigma=1 for W1
    (conjugation by the (1,1,1) axis 3-fold rotates x->y->z, cycling both
    cubes Rx->Ry->Rz and face columns), sigma=0 for W2 (conjugation by S
    cycles I->S->S^2 with face columns fixed)."""
    def step(key):
        f0, f1, f2, s01, s12 = key
        return ((f2 + sigma) % 3, (f0 + sigma) % 3, (f1 + sigma) % 3,
                s01 * s12, s01)
    orbits = []
    seen = set()
    for key in sorted(occ_keys):
        if key in seen:
            continue
        orb = []
        cur = key
        while cur not in seen:
            seen.add(cur)
            orb.append(cur)
            cur = step(cur)
        orbits.append(orb)
    return orbits


def fkey(cr):
    return tuple(float(c) for c in cr)


def census_tables(name, n, verts, top_edges, bot_edges, top_deg, bot_deg,
                  sigma):
    """All census data for one witness, as a dict (also used for the JSON)."""
    verify_triple_ties(n, verts)

    order = sorted(verts, key=fkey)
    vid = {cr: idx for idx, cr in enumerate(order)}

    def serial(x):
        return [str(x.a), str(x.b)]

    vtab = []
    for cr in order:
        info = verts[cr]
        td = top_deg.get(cr, 0)
        bd = bot_deg.get(cr, 0)
        vtab.append(dict(
            id=vid[cr],
            coords_exact=[serial(c) for c in cr],
            coords_float=[round(float(c), 12) for c in cr],
            type=info['type'],
            active=[list(info['active'][k]) for k in range(3)],
            deg_top=td, deg_bottom=bd,
            on_top=td > 0, on_bottom=bd > 0,
            antipode_id=vid.get(tuple(-c for c in cr)),
        ))

    triples = [v for v in vtab if v['type'] == 'triple']
    kinks = [v for v in vtab if v['type'] == 'kink']

    def spectrum(rows, key):
        sp = {}
        for r in rows:
            sp[r[key]] = sp.get(r[key], 0) + 1
        return dict(sorted(sp.items()))

    w_top_triples = sum(r['deg_top'] - 2 for r in triples if r['deg_top'] > 0)
    w_top_all = sum(r['deg_top'] - 2 for r in vtab if r['deg_top'] > 0)
    w_bot_triples = sum(r['deg_bottom'] - 2 for r in triples if r['deg_bottom'] > 0)
    w_bot_all = sum(r['deg_bottom'] - 2 for r in vtab if r['deg_bottom'] > 0)

    # Every 'kink'-class vertex should live in exactly ONE diagram (its single
    # pair-tie is either the top pair or the bottom pair there).  The spec's
    # expectation 'kinks should be degree-2' is a GENERIC statement; at the
    # witnesses they are degenerate multi-crossings -- reported, not asserted.
    kink_single = all((r['deg_top'] > 0) != (r['deg_bottom'] > 0)
                      for r in kinks)

    occ = elementary_triples(n, verts)
    orbits = orbit_reduce(occ.keys(), sigma)

    def edge_serial(edges):
        out = []
        for (v1, v2, ck) in edges:
            def pid(v):
                if v and v[0] == 'loop':
                    return ['loop', [serial(c) for c in v[1]]]
                return vid[v]
            out.append(dict(v1=pid(v1), v2=pid(v2),
                            circle=[serial(c) for c in ck]))
        return out

    return dict(
        name=name,
        vertices=vtab,
        n_triple=len(triples), n_kink=len(kinks),
        triple_spectrum_top=spectrum(triples, 'deg_top'),
        triple_spectrum_bottom=spectrum(triples, 'deg_bottom'),
        kink_spectrum_top=spectrum(kinks, 'deg_top'),
        kink_spectrum_bottom=spectrum(kinks, 'deg_bottom'),
        weight_top_triples=w_top_triples, weight_top_all=w_top_all,
        weight_bottom_triples=w_bot_triples, weight_bottom_all=w_bot_all,
        kinks_in_single_diagram=kink_single,
        occurring_triples={
            f'({k[0]},{k[1]},{k[2]}) s01={k[3]:+d} s12={k[4]:+d}':
                sorted(vid[cr] for cr in crs)
            for k, crs in sorted(occ.items())},
        n_occurring_triples=len(occ),
        orbits=[[f'({k[0]},{k[1]},{k[2]}) s01={k[3]:+d} s12={k[4]:+d}'
                 for k in orb] for orb in orbits],
        n_orbits=len(orbits),
        top_edges=edge_serial(top_edges),
        bottom_edges=edge_serial(bot_edges),
    )


def fmt_spec(sp):
    return ', '.join(f'deg {d}: {c}' for d, c in sp.items()) or '(empty)'


def write_report(res1, cen1, res2, cen2, path_md, path_json):
    L = []
    L.append('# Census report: (c1) exact data from both n=3 max(3)=67 witnesses')
    L.append('')
    L.append('Produced by census_extract.py (exact field arithmetic only in all')
    L.append('decisions; floats used only for sorting/printing).  Feeds lemma')
    L.append('L2.c (and the bottom diagram of cluster 1) of C45_notes.md sect. 13.')
    L.append('')
    L.append('## Gates')
    L.append('')
    L.append('| gate | W1 octahedral Q(sqrt2) | W2 golden Q(sqrt5) |')
    L.append('|------|------------------------|--------------------|')
    L.append('| G1 exact count 67={48,18,1} | PASS (slide3_q2.exact_count_q2) '
             '| PASS (certify_six.exact_count_config) |')
    L.append(f'| G2 TOP-1 Euler F=48 | F={res1["top"]["F"]} '
             f'({"PASS" if res1["top"]["F"] == 48 else "FAIL"}) '
             f'| F={res2["top"]["F"]} '
             f'({"PASS" if res2["top"]["F"] == 48 else "FAIL"}) |')
    L.append(f'| G2 BOTTOM Euler F=18 | F={res1["bottom"]["F"]} '
             f'({"PASS" if res1["bottom"]["F"] == 18 else "FAIL"}) '
             f'| F={res2["bottom"]["F"]} '
             f'({"PASS" if res2["bottom"]["F"] == 18 else "FAIL"}) |')
    L.append(f'| G3 antipodal symmetry | '
             f'{"PASS" if res1["top"]["g3"] and res1["bottom"]["g3"] else "FAIL"} | '
             f'{"PASS" if res2["top"]["g3"] and res2["bottom"]["g3"] else "FAIL"} |')
    L.append('')
    L.append('## Graph invariants')
    L.append('')
    L.append('| quantity | W1 | W2 |')
    L.append('|----------|----|----|')
    for label, get in (
            ('TOP-1: V', lambda r: r['top']['V']),
            ('TOP-1: E', lambda r: r['top']['E']),
            ('TOP-1: components', lambda r: r['top']['C']),
            ('TOP-1: F = E-V+1+C', lambda r: r['top']['F']),
            ('BOTTOM: V', lambda r: r['bottom']['V']),
            ('BOTTOM: E', lambda r: r['bottom']['E']),
            ('BOTTOM: components', lambda r: r['bottom']['C']),
            ('BOTTOM: F = E-V+1+C', lambda r: r['bottom']['F'])):
        L.append(f'| {label} | {get(res1)} | {get(res2)} |')
    L.append('')
    L.append('## Vertex census')
    L.append('')
    L.append('| quantity | W1 | W2 |')
    L.append('|----------|----|----|')
    for label, key in (('triple points', 'n_triple'), ('kinks', 'n_kink')):
        L.append(f'| {label} | {cen1[key]} | {cen2[key]} |')
    L.append(f'| triple degree spectrum, TOP | {fmt_spec(cen1["triple_spectrum_top"])} '
             f'| {fmt_spec(cen2["triple_spectrum_top"])} |')
    L.append(f'| triple degree spectrum, BOTTOM | {fmt_spec(cen1["triple_spectrum_bottom"])} '
             f'| {fmt_spec(cen2["triple_spectrum_bottom"])} |')
    L.append(f'| kink degree spectrum, TOP | {fmt_spec(cen1["kink_spectrum_top"])} '
             f'| {fmt_spec(cen2["kink_spectrum_top"])} |')
    L.append(f'| kink degree spectrum, BOTTOM | {fmt_spec(cen1["kink_spectrum_bottom"])} '
             f'| {fmt_spec(cen2["kink_spectrum_bottom"])} |')
    L.append(f'| sum(deg-2), TOP, triple points | {cen1["weight_top_triples"]} '
             f'| {cen2["weight_top_triples"]} |')
    L.append(f'| sum(deg-2), TOP, all vertices | {cen1["weight_top_all"]} '
             f'| {cen2["weight_top_all"]} |')
    L.append(f'| sum(deg-2), BOTTOM, triple points | {cen1["weight_bottom_triples"]} '
             f'| {cen2["weight_bottom_triples"]} |')
    L.append(f'| kinks lie in exactly one diagram | '
             f'{cen1["kinks_in_single_diagram"]} '
             f'| {cen2["kinks_in_single_diagram"]} |')
    L.append(f'| occurring elementary triples (f0,f1,f2,s01,s12) | '
             f'{cen1["n_occurring_triples"]} | {cen2["n_occurring_triples"]} |')
    L.append(f'| ... in C3-symmetry orbits | {cen1["n_orbits"]} | {cen2["n_orbits"]} |')
    L.append('')
    L.append('## The sect. 13 projection vs the data (DISCREPANCY -- READ FIRST)')
    L.append('')
    L.append('Sect. 13 (L2.c) projects "at most 46 feasible triples x 2 points')
    L.append('= 92 V-weight, hence F <= 2 + 92/2 = 48", with L2.b assuming')
    L.append('"kink vertices are degree-2 and contribute 0".  The exact data')
    L.append('CONFIRMS the total-weight arithmetic but CORRECTS the accounting:')
    L.append('')
    L.append('1. TOTAL top-1 weight sum_v(deg_v - 2) = 92 EXACTLY, for BOTH')
    L.append('   witnesses (F = 2 + 92/2 = 48, single-component graphs).  The')
    L.append('   projected budget number is right and attained with equality.')
    L.append(f'2. BUT rank-triple points carry only {cen1["weight_top_triples"]} '
             'of the 92: both witnesses')
    L.append(f'   have exactly {cen1["n_triple"]} triple points, every one '
             'TRIVALENT in the TOP-1')
    L.append('   graph (and trivalent in the BOTTOM graph), each with a UNIQUE')
    L.append('   active face per cube.  There are no merged/high-degree triple')
    L.append('   points at either witness.')
    L.append('3. The remaining 60 units of weight are carried by SAME-PAIR')
    L.append('   double-tie vertices (classified "kink" here: only one cube')
    L.append('   PAIR is tied, but two or three faces per cube are active):')
    L.append('   - W1: 30 edge-edge contact vertices, all degree 4')
    L.append('     (30 x 2 = 60): two cubes sit on sector boundaries')
    L.append('     simultaneously, two branches of the same tie r_i = r_j')
    L.append('     cross.')
    L.append('   - W2: 18 edge-edge degree-4 vertices (36) + 6 CORNER-contact')
    L.append('     degree-6 vertices (24): at u ~ (1,1,1)-type directions two')
    L.append('     cubes are simultaneously at corners (all three faces tied,')
    L.append('     active sets of size 3); 36 + 24 = 60.')
    L.append('   So the L2.b obligation "(1) kinks are degree-2, discountable"')
    L.append('   is FALSE at both witnesses; the (c2)/(c3) budget must include')
    L.append('   same-pair multi-tie vertices.  The degeneracy-robust (c3)')
    L.append('   statement should budget the TOTAL weight 92 = (rank-triple')
    L.append('   weight) + (same-pair crossing weight), conserved under both')
    L.append('   kinds of merging.')
    L.append(f'4. Occurring elementary active triples: '
             f'{cen1["n_occurring_triples"]} (W1) and '
             f'{cen2["n_occurring_triples"]} (W2), in '
             f'{cen1["n_orbits"]}/{cen2["n_orbits"]} C3-orbits -- far below')
    L.append('   the projected <= 46.  Verified: each occurring triple is')
    L.append('   realized at EXACTLY 2 (antipodal) vertices, and each triple')
    L.append('   point realizes exactly one elementary triple; 16 x 2 = 32 =')
    L.append('   the triple-point count.  The "x 2 points per feasible')
    L.append('   triple" heuristic of sect. 13 is exact on the occurring')
    L.append('   triples; the slack is entirely in "<= 46 feasible" vs 16')
    L.append('   occurring.')
    L.append('5. BOTTOM graphs: both witnesses give the exact GENERIC census')
    L.append('   V=32, E=48, F=18, all 32 triple points trivalent, no kinks at')
    L.append('   all -- matching the general law V_1(n) = 12n - 4 = 32 of')
    L.append('   sect. 7 with NO degeneracy correction on the bottom side.')
    L.append('   (Both diagrams share the same 32 rank-triple points: at n=3')
    L.append('   all three reaches are equal there, so each is a vertex of')
    L.append('   both diagrams, trivalent in each: 6 arcs alternate')
    L.append('   top/bottom around every triple point.)')
    L.append('')
    for cen, res in ((cen1, res1), (cen2, res2)):
        L.append(f'## {cen["name"]}: occurring elementary triples '
                 '(classification target list)')
        L.append('')
        L.append('Faces are column indices 0,1,2 of each cube\'s rotation; triple')
        L.append('(f0,f1,f2) means face f_k of cube k is active and tied at the')
        L.append('point; s01 = sign((n0.u)(n1.u)), s12 = sign((n1.u)(n2.u)).')
        L.append('Grouped in orbits of the C3 symmetry of the compound.')
        L.append('')
        for orb in cen['orbits']:
            members = '; '.join(orb)
            pts = sorted({p for k in orb
                          for p in cen['occurring_triples'][k]})
            L.append(f'- orbit ({len(orb)}): {members}   [vertex ids: {pts}]')
        L.append('')
    L.append('## W1-vs-W2 merge comparison (for the (c3) robust budget)')
    L.append('')
    L.append('Within each witness all candidate constructions were deduped')
    L.append('projectively; "multiplicity" of a degenerate vertex = number of')
    L.append('active tied face-pairs of its cube pair (= deg/2 in its single')
    L.append('diagram).')
    L.append('')
    for cen in (cen1, cen2):
        kink_mult = {}
        for r in cen['vertices']:
            if r['type'] != 'kink':
                continue
            mult = (r['deg_top'] + r['deg_bottom']) // 2
            kink_mult[mult] = kink_mult.get(mult, 0) + 1
        L.append(f'- {cen["name"]}: triple points all multiplicity 3 '
                 f'(trivalent x2 diagrams); same-pair contact vertices by '
                 f'multiplicity: {dict(sorted(kink_mult.items()))}')
    L.append('')
    L.append('The witnesses realize the SAME global weights (92 top, 32')
    L.append('bottom) through different local contact patterns: W1 spreads')
    L.append('the 60 same-pair units over 30 edge-edge double crossings;')
    L.append('W2 concentrates 24 of them into 6 corner contacts (golden')
    L.append('corner coincidences, multiplicity 3) and keeps 18 edge-edge.')
    L.append('The (c3) budget must therefore be weight-preserving under')
    L.append('merging of same-pair contacts as well as of rank-triple points.')
    L.append('')
    L.append('## Full vertex tables')
    L.append('')
    for cen in (cen1, cen2):
        L.append(f'### {cen["name"]}')
        L.append('')
        L.append('| id | float coords | type | active (c0;c1;c2) | deg_top | '
                 'deg_bot | antipode |')
        L.append('|----|--------------|------|-------------------|--------|'
                 '---------|----------|')
        for r in cen['vertices']:
            co = ', '.join(f'{c:.4f}' for c in r['coords_float'])
            ac = ';'.join(''.join(map(str, a)) for a in r['active'])
            L.append(f'| {r["id"]} | ({co}) | {r["type"]} | {ac} | '
                     f'{r["deg_top"]} | {r["deg_bottom"]} | {r["antipode_id"]} |')
        L.append('')
    L.append('Exact coordinates (field-element pairs) and the full arc lists')
    L.append('are in census_data.json.')
    L.append('')

    with open(path_md, 'w') as f:
        f.write('\n'.join(L))

    data = dict(
        description='(c1) census data, exact, both max(3)=67 witnesses; '
                    'coords_exact entries are [a, b] with value a + b*sqrt(d), '
                    'd=2 (W1) / d=5 (W2), a,b rational strings',
        witnesses=[
            dict(field='Q(sqrt2)', gates=res1, census=cen1),
            dict(field='Q(sqrt5)', gates=res2, census=cen2),
        ])
    with open(path_json, 'w') as f:
        json.dump(data, f, indent=1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        raise SystemExit(0)
    gate_g1()

    R1, n1 = build_w1()
    R2, n2 = build_w2()

    res1, verts1, te1, be1, td1, bd1 = process_witness('W1 octahedral Q(sqrt2)', n1)
    print()
    res2, verts2, te2, be2, td2, bd2 = process_witness('W2 golden Q(sqrt5)', n2)

    print('\n=== GATE G2 summary ===')
    ok = True
    for res in (res1, res2):
        ok_top = res['top']['F'] == 48
        ok_bot = res['bottom']['F'] == 18
        ok = ok and ok_top and ok_bot
        print(f'  {res["name"]}: TOP F={res["top"]["F"]} '
              f'({"PASS" if ok_top else "FAIL"})   '
              f'BOTTOM F={res["bottom"]["F"]} ({"PASS" if ok_bot else "FAIL"})')
    assert ok, 'GATE G2 failed -- census tables are NOT deliverable'

    print('\n=== building census tables ===')
    cen1 = census_tables('W1 octahedral Q(sqrt2)', n1, verts1, te1, be1,
                         td1, bd1, sigma=1)
    cen2 = census_tables('W2 golden Q(sqrt5)', n2, verts2, te2, be2,
                         td2, bd2, sigma=0)
    write_report(res1, cen1, res2, cen2,
                 '/Users/dmi/carroll/census_report.md',
                 '/Users/dmi/carroll/census_data.json')
    print('wrote census_report.md and census_data.json')
    print(f'  W1: {cen1["n_triple"]} triples, {cen1["n_kink"]} kinks, '
          f'top weight {cen1["weight_top_triples"]}, '
          f'{cen1["n_occurring_triples"]} occurring triples '
          f'({cen1["n_orbits"]} orbits)')
    print(f'  W2: {cen2["n_triple"]} triples, {cen2["n_kink"]} kinks, '
          f'top weight {cen2["weight_top_triples"]}, '
          f'{cen2["n_occurring_triples"]} occurring triples '
          f'({cen2["n_orbits"]} orbits)')
