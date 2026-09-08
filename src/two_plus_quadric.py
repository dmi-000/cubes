#!/usr/bin/env python3
"""Two rational planes + one quadric: hunting IRRATIONAL records.

The n=3 record 67 is irrational.  Three independent walls against a rational
base cannot produce an irrational point (irrational_probe.py: 0/2451), because
every wall is a pair of rational planes (locus_linear.py) -- a 3-plane system
is always rational.  Two planes leave a rational LINE; a genuinely irreducible
QUADRIC (corner-on-face incidence) along that line gives a quadratic in one
parameter whose roots can be irrational.  That is the only remaining route to
an irrational record, and this script builds it exhaustively for two bases:

  n=4, target 183: base = the 183 record's first three cubes (drop the 4th).
  n=5, target 393: base = the 393 record's first four cubes (drop the 5th).

For the free (last) cube's Cayley coordinates (a,b,c) in Q^3:
  PLANES   -- edge-edge coplanarity conditions against each fixed cube.  Every
              one factors into two rational linear forms (locus_probe.py /
              locus_linear.py); we keep the distinct linear factors.
  QUADRICS -- corner-on-face-plane conditions (corner_probe.py TYPE A/B), one
              irreducible quadric per (cube, normal axis, sign, corner/vertex).

Every pair of independent planes gives a rational line P0 + t*D.  Substituting
into a quadric gives alpha*t^2 + beta*t + gamma = 0 with rational coefficients.
Delta = beta^2 - 4*alpha*gamma classifies the roots: a perfect-square rational
Delta gives rational t (already reachable by 3-plane solving); a non-square
Delta gives t in Q(sqrt d), d = squarefree part of Delta -- THESE are the
targets.  Each such root builds a free cube over Z[sqrt d] (qfield.py exact
arithmetic, qfield.clear_denoms to integers), counted by the widened field
engine cube_regions_q2w at that d.

INVARIANT: every wall extraction is exact (sympy Rational / Fraction, never
float); the squarefree part of Delta is computed by exact integer
factorisation, never by float sqrt.  Engine refusals (budget exceeded, zero
quaternion) are counted separately from low counts -- never folded into "no
region growth", per the standing rule that unevaluated is not a negative
result.
"""
import itertools
import json
import math
import subprocess
import sys
import time
from fractions import Fraction as F

import sympy as sp

import qfield as QF

a, b, c = sp.symbols('a b c', real=True)
CAP = 512
NBIN = './cube_regions_n'
WBIN = './cube_regions_q2w'

BASE4 = [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1)]   # 183's cubes 1-3
KNOWN4 = (1, -1, -4)                                    # (a,b,c) of cube 4 -> 183
TARGET4 = 183

BASE5 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1)]  # 393's cubes 1-4
KNOWN5 = (1, 1, 1)                                      # (a,b,c) of cube 5 -> 393
TARGET5 = 393

LOG = open('two_plus_quadric.log', 'a')


def log(msg):
    line = '[%6.1fs] %s' % (time.time() - T0, msg)
    print(line, flush=True)
    LOG.write(line + '\n')
    LOG.flush()


# --------------------------------------------------------------- gates
def gate(cmd, expect_key='bounded', expect=None, label=''):
    p = subprocess.run(cmd, capture_output=True, text=True)
    line = p.stdout.strip().splitlines()[-1]
    d = json.loads(line)
    got = d.get(expect_key)
    ok = (got == expect)
    log('GATE %s: %s -> %s (expect %s) %s'
        % (label, cmd, got, expect, 'PASS' if ok else '*** FAIL ***'))
    if not ok:
        log('GATE FAILED, output: %s' % line)
        sys.exit(1)
    return d


# --------------------------------------------------------------- geometry
def rot_sym(q):
    w, x, y, z = q
    n = w * w + x * x + y * y + z * z
    return sp.Matrix([
        [w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]
    ]) / n


def edge_list(M):
    out = []
    for ax in range(3):
        o1, o2 = [t for t in range(3) if t != ax]
        for s in (-1, 1):
            for t in (-1, 1):
                out.append((s * M[:, o1] + t * M[:, o2], M[:, ax]))
    return out


def build_edge_conditions(base):
    """Raw edge-edge determinant polynomials, per fixed cube."""
    M6 = rot_sym((1, a, b, c))
    e6 = edge_list(M6)
    per = {}
    for j, q in enumerate(base):
        t0 = time.time()
        ef = edge_list(rot_sym(q))
        ps = []
        for (i1, x1), (i2, x2) in itertools.product(enumerate(e6), enumerate(ef)):
            d = sp.Matrix.hstack(x1[1], x2[1], x2[0] - x1[0]).det()
            P = sp.expand(sp.together(sp.simplify(d)).as_numer_denom()[0])
            if P != 0:
                ps.append(P)
        per[j] = ps
        log('  cube %d edge-edge: %d raw conditions (%.1fs)'
            % (j, len(ps), time.time() - t0))
    return per


def build_corner_conditions(base):
    """Raw corner-on-face-plane polynomials (TYPE A + TYPE B), per fixed cube."""
    M6 = rot_sym((1, a, b, c))
    corners6 = [M6 * sp.Matrix(s) for s in itertools.product((1, -1), repeat=3)]
    per = {}
    for j, q in enumerate(base):
        t0 = time.time()
        Rj = rot_sym(q)
        cj = [Rj * sp.Matrix(t) for t in itertools.product((1, -1), repeat=3)]
        conds = set()
        for k in range(3):
            for sign in (1, -1):
                for cor in corners6:                       # TYPE A
                    e = (Rj[:, k].T * cor)[0, 0] - sign
                    P = sp.expand(sp.together(sp.simplify(e)).as_numer_denom()[0])
                    if P != 0:
                        conds.add(sp.factor(P))
                for v in cj:                               # TYPE B
                    e = (M6[:, k].T * v)[0, 0] - sign
                    P = sp.expand(sp.together(sp.simplify(e)).as_numer_denom()[0])
                    if P != 0:
                        conds.add(sp.factor(P))
        per[j] = sorted(conds, key=sp.default_sort_key)
        log('  cube %d corner: %d raw conditions (%.1fs)'
            % (j, len(per[j]), time.time() - t0))
    return per


def canon_plane(co):
    g = 0
    for x in co:
        g = math.gcd(g, abs(x))
    co = tuple(x // g for x in co) if g > 1 else tuple(co)
    for x in co:
        if x:
            if x < 0:
                co = tuple(-y for y in co)
            break
    return co


def extract_planes(edge_conds):
    """{cube: sorted list of distinct (A,B,C,D)} with Aa+Bb+Cc+D=0."""
    out = {}
    for j, ps in edge_conds.items():
        S = set()
        for P in ps:
            for f, _m in sp.factor_list(P)[1]:
                p = sp.Poly(f, a, b, c)
                if p.total_degree() != 1:
                    continue
                co = [sp.Rational(p.coeff_monomial(m)) for m in (a, b, c, 1)]
                g = sp.ilcm(*[x.q for x in co]) if any(co) else 1
                co = [int(x * g) for x in co]
                if not any(co):
                    continue
                S.add(canon_plane(co))
        out[j] = sorted(S)
    return out


MONOMS = [(2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1),
          (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)]


def poly_coeffs(P):
    p = sp.Poly(P, a, b, c)
    if p.total_degree() > 2:
        return None
    out = {}
    for m in MONOMS:
        mono = a**m[0] * b**m[1] * c**m[2] if any(m) else sp.Integer(1)
        out[m] = F(sp.Rational(p.coeff_monomial(mono)))
    return out


def extract_quadrics(corner_conds, plane_sets):
    """{cube: list of coeff-dicts} for the IRREDUCIBLE degree-2 factors;
    any stray linear factor is folded into plane_sets[cube] (defensive --
    corner conditions are documented irreducible, but never assumed so
    silently)."""
    out = {}
    for j, ps in corner_conds.items():
        Sq, extra_planes = [], set()
        seen_q = set()
        for P in ps:
            for f, _m in sp.factor_list(P)[1]:
                p = sp.Poly(f, a, b, c)
                deg = p.total_degree()
                if deg == 1:
                    co = [sp.Rational(p.coeff_monomial(m)) for m in (a, b, c, 1)]
                    g = sp.ilcm(*[x.q for x in co]) if any(co) else 1
                    co = [int(x * g) for x in co]
                    if any(co):
                        extra_planes.add(canon_plane(co))
                elif deg == 2:
                    key = sp.factor(f)
                    if key in seen_q:
                        continue
                    seen_q.add(key)
                    cd = poly_coeffs(f)
                    if cd is not None:
                        Sq.append(cd)
        out[j] = Sq
        if extra_planes:
            plane_sets[j] = sorted(set(plane_sets[j]) | extra_planes)
            log('  cube %d: %d stray linear factors folded into planes'
                % (j, len(extra_planes)))
    return out


# --------------------------------------------------------------- symmetry dedup
# The free cube's OWN 24-element rotation symmetry group means 24 raw roots
# describe the same physical compound (locus_linear.py's sym_key).  Without
# folding that orbit, the raw root count (hundreds of thousands) makes the
# engine pass infeasible; with it, only distinct compounds are ever counted.
# The dedup KEY is the canonical orbit representative; the value SUBMITTED to
# the engine is the ORIGINAL point, never the rotated one -- rotating by a
# symmetry element can inflate component magnitude past CAP even when the
# original point was safely under it, and submitting the original is exactly
# as valid since region count is rotation-invariant on the orbit.
def _canon_int(q):
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x // g for x in q) if g > 1 else tuple(q)
    for x in q:
        if x:
            if x < 0:
                q = tuple(-y for y in q)
            break
    return q


SYMS = sorted(set(_canon_int(t) for t in
    [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1) for y in (-1, 0, 1)
     for z in (-1, 0, 1)
     if (w, x, y, z) != (0, 0, 0, 0) and w*w+x*x+y*y+z*z in (1, 2, 4)]))
assert len(SYMS) == 24, 'expected the 24-element rotation group, got %d' % len(SYMS)


def qmul_field(P, S):
    """P: quaternion of (p,q) field pairs.  S: plain-int quaternion.  -> P*S,
    same field."""
    w, x, y, z = P
    e, f, g, h = S
    def s(pq, k):
        return (pq[0] * k, pq[1] * k)
    def c(*terms):
        return (sum(t[0] for t in terms), sum(t[1] for t in terms))
    return (c(s(w, e), s(x, -f), s(y, -g), s(z, -h)),
            c(s(w, f), s(x, e), s(y, h), s(z, -g)),
            c(s(w, g), s(x, -h), s(y, e), s(z, f)),
            c(s(w, h), s(x, g), s(y, -f), s(z, e)))


def canon_pairs(pairs):
    g = 0
    for p, q in pairs:
        g = math.gcd(g, abs(p))
        g = math.gcd(g, abs(q))
    if g > 1:
        pairs = [(p // g, q // g) for p, q in pairs]
    for p, q in pairs:
        if p or q:
            if p < 0 or (p == 0 and q < 0):
                pairs = [(-p, -q) for p, q in pairs]
            break
    return tuple(pairs)


def sym_key(pairs):
    return min(canon_pairs(qmul_field(pairs, s)) for s in SYMS)


# --------------------------------------------------------------- line algebra
def cross(u, v):
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def det3(r0, r1, r2):
    return (r0[0]*(r1[1]*r2[2]-r1[2]*r2[1]) - r0[1]*(r1[0]*r2[2]-r1[2]*r2[0])
            + r0[2]*(r1[0]*r2[1]-r1[1]*r2[0]))


def solve3(rows, rhs):
    d = det3(*rows)
    if d == 0:
        return None
    def cof(col):
        N = [list(r) for r in rows]
        for i in range(3):
            N[i][col] = rhs[i]
        return det3(*[tuple(r) for r in N])
    return (F(cof(0), d), F(cof(1), d), F(cof(2), d))


def line_from_planes(p, q):
    """p,q: (A,B,C,D) with Aa+Bb+Cc+D=0.  -> (P0, D) rational, or None if
    parallel/identical planes (no line)."""
    n1, n2 = p[:3], q[:3]
    Dv = cross(n1, n2)
    if not any(Dv):
        return None
    P0 = solve3([n1, n2, Dv], [F(-p[3]), F(-q[3]), F(0)])
    if P0 is None:
        return None
    return P0, Dv


def quad_on_line(coef, P0, Dv):
    Pa, Pb, Pc = P0
    Da, Db, Dc = (F(x) for x in Dv)
    caa, cbb, ccc = coef[(2,0,0)], coef[(0,2,0)], coef[(0,0,2)]
    cab, cac, cbc = coef[(1,1,0)], coef[(1,0,1)], coef[(0,1,1)]
    ca, cb, cc, c0 = coef[(1,0,0)], coef[(0,1,0)], coef[(0,0,1)], coef[(0,0,0)]
    alpha = caa*Da*Da + cbb*Db*Db + ccc*Dc*Dc + cab*Da*Db + cac*Da*Dc + cbc*Db*Dc
    beta = (2*caa*Pa*Da + 2*cbb*Pb*Db + 2*ccc*Pc*Dc
            + cab*(Pa*Db+Pb*Da) + cac*(Pa*Dc+Pc*Da) + cbc*(Pb*Dc+Pc*Db)
            + ca*Da + cb*Db + cc*Dc)
    gamma = (caa*Pa*Pa + cbb*Pb*Pb + ccc*Pc*Pc + cab*Pa*Pb + cac*Pa*Pc + cbc*Pb*Pc
             + ca*Pa + cb*Pb + cc*Pc + c0)
    return alpha, beta, gamma


def squarefree_part(n):
    """largest squarefree d>0 with n = k^2*d, for integer n>0.  Exact
    (sympy's `core`, not a bounded trial division) -- Delta's numerator*
    denominator can run to tens of digits, where naive trial division would
    silently under-reduce a large square factor instead of raising."""
    return int(sp.ntheory.factor_.core(n))


def isqrt(n):
    x = math.isqrt(n)
    assert x * x == n
    return x


def classify_roots(alpha, beta, gamma):
    """-> list of (kind, d, t) roots; kind in {'rational','irrational'}.
    t is a Fraction (rational) or a qfield.Q (irrational, field d)."""
    if alpha == 0:
        return ('degenerate', None, None)
    Delta = beta * beta - 4 * alpha * gamma
    if Delta < 0:
        return ('no-real-root', None, None)
    p, q = Delta.numerator, Delta.denominator     # q > 0, p >= 0
    N = p * q
    if N == 0:
        t0 = -beta / (2 * alpha)
        return ('rational', 1, [('rational', 0, t0)])
    sf = squarefree_part(N)
    if sf == 1:
        sq = F(isqrt(N), q)
        ts = sorted({(-beta + sq) / (2*alpha), (-beta - sq) / (2*alpha)})
        return ('rational', 1, [('rational', 0, t) for t in ts])
    kfac = isqrt(N // sf)
    A = -beta / (2 * alpha)
    B = F(kfac, q * 2 * alpha)
    roots = [('irrational', sf, QF.Q(A, B, sf)), ('irrational', sf, QF.Q(A, -B, sf))]
    return ('irrational', sf, roots)


def eval_point(P0, Dv, t):
    return tuple(P0[i] + t * F(Dv[i]) for i in range(3))


def build_free_quat(pt, d):
    """pt = (a,b,c) each a Fraction (d must then be 0) or qfield.Q(field d).
    -> gcd-reduced integer (p,q) pairs [w,x,y,z], or None (zero / over CAP)."""
    one = F(1) if d == 0 else QF.Q(1, 0, d)
    vals = [one] + list(pt)
    L, pairs = QF.clear_denoms(vals)
    g = 0
    for p, q in pairs:
        g = math.gcd(g, abs(p))
        g = math.gcd(g, abs(q))
    if g > 1:
        pairs = [(p // g, q // g) for p, q in pairs]
    if all(p == 0 and q == 0 for p, q in pairs):
        return None
    if max(max(abs(p), abs(q)) for p, q in pairs) > CAP:
        return None
    return pairs


def fmt_rat_quat(pairs):
    return ','.join(str(p) for p, q in pairs)


def fmt_field_quat(pairs):
    return ','.join('%d:%d' % (p, q) for p, q in pairs)


# --------------------------------------------------------------- engines
def run_rational_batch(fixed, quats):
    """fixed: list of int quaternion tuples.  quats: list of (p,q) pair-lists
    (q parts must be all 0).  -> list of dicts (engine JSON) aligned."""
    lines = []
    fixed_str = ';'.join(','.join(str(c) for c in fc) for fc in fixed)
    for pairs in quats:
        free_str = fmt_rat_quat(pairs)
        lines.append(fixed_str + ';' + free_str)
    if not lines:
        return []
    p = subprocess.run([NBIN, '--quats-stdin'], input='\n'.join(lines) + '\n',
                        capture_output=True, text=True)
    out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith('{')]
    if len(out) != len(lines):
        raise RuntimeError('rational batch: got %d of %d, stderr=%s'
                            % (len(out), len(lines), p.stderr[:300]))
    return out


def run_field_batch(fixed, quats, d):
    fixed_str = ';'.join(','.join('%d:0' % c for c in fc) for fc in fixed)
    lines = [fixed_str + ';' + fmt_field_quat(pairs) for pairs in quats]
    if not lines:
        return []
    p = subprocess.run([WBIN, '--d', str(d), '--quats-stdin'],
                        input='\n'.join(lines) + '\n',
                        capture_output=True, text=True)
    out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith('{')]
    if len(out) != len(lines):
        raise RuntimeError('field batch d=%d: got %d of %d, stderr=%s'
                            % (d, len(out), len(lines), p.stderr[:300]))
    return out


# --------------------------------------------------------------- control gate
def find_control(base, planes, quadrics, known_pt, target, name):
    """Search the just-built catalogs for a (plane-pair, quadric) system whose
    root reproduces `known_pt` exactly, and verify its engine count == target.
    Returns True/False (found & verified)."""
    ka, kb, kc = (F(x) for x in known_pt)
    all_planes = [(j, pl) for j, pls in planes.items() for pl in pls]
    hit_planes = [(j, pl) for j, pl in all_planes
                  if pl[0]*ka + pl[1]*kb + pl[2]*kc + pl[3] == 0]
    # direct evaluation of the quadric form at the known point:
    def qval(cd, pt):
        pa, pb, pc = pt
        return (cd[(2,0,0)]*pa*pa + cd[(0,2,0)]*pb*pb + cd[(0,0,2)]*pc*pc
                + cd[(1,1,0)]*pa*pb + cd[(1,0,1)]*pa*pc + cd[(0,1,1)]*pb*pc
                + cd[(1,0,0)]*pa + cd[(0,1,0)]*pb + cd[(0,0,1)]*pc + cd[(0,0,0)])
    hit_quads = [(j, qi, cd) for j, qs in quadrics.items()
                 for qi, cd in enumerate(qs) if qval(cd, (ka, kb, kc)) == 0]
    log('  control %s: %d planes and %d quadrics vanish at the known point'
        % (name, len(hit_planes), len(hit_quads)))
    if len(hit_planes) < 2 or not hit_quads:
        log('  control %s: NOT FOUND (need >=2 planes and >=1 quadric through '
            'the known point)' % name)
        return False
    for (j1, p1), (j2, p2) in itertools.combinations(hit_planes, 2):
        line = line_from_planes(p1, p2)
        if line is None:
            continue
        P0, Dv = line
        for j, qi, cd in hit_quads:
            alpha, beta, gamma = quad_on_line(cd, P0, Dv)
            kind, d, roots = classify_roots(alpha, beta, gamma)
            if kind == 'degenerate' or kind == 'no-real-root':
                continue
            for rkind, rd, t in roots:
                pt = eval_point(P0, Dv, t)
                if pt == (ka, kb, kc):
                    pairs = build_free_quat(pt, rd)
                    if pairs is None:
                        continue
                    if rd == 0:
                        res = run_rational_batch(base, [pairs])[0]
                    else:
                        res = run_field_batch(base, [pairs], rd)[0]
                    tot = res.get('bounded')
                    ok = (tot == target)
                    log('  control %s: reproduced known point via planes '
                        '(cube %d,%d) + quadric (cube %d,#%d), root=%s(d=%s), '
                        'engine total=%s (expect %s) %s'
                        % (name, j1, j2, j, qi, rkind, rd, tot, target,
                           'PASS' if ok else '*** FAIL ***'))
                    return ok
    log('  control %s: planes/quadrics vanish at the point but no '
        '(pair,quadric) system reconstructed it exactly (numerical '
        'coincidence, not a shared root) -- NOT FOUND' % name)
    return False


# ------------------------------------------------- caching (restartability)
# The catalog build (~1-2 min/base, sympy) and the classify sweep (~1 min/base)
# are cheap next to engine evaluation (many thousands of subprocess calls,
# tens of minutes) -- but ALL of it is wasted on a restart without a cache.
# Both stages are pickled to the project directory (never scratch) keyed by
# base name, and engine evaluation is checkpointed to a JSONL results file so
# a killed-and-resumed run repeats no completed engine call.
import os
import pickle


def cache_path(kind, name):
    return 'tpq_%s_%s.pkl' % (kind, name)


def results_path(name):
    return 'tpq_results_%s.jsonl' % name


def rkey(kind, d, pairs):
    return '%s|%d|%s' % (kind, d, ','.join('%d:%d' % (p, q) for p, q in pairs))


def classify_systems(base, planes, quadrics, name):
    cp = cache_path('cands', name)
    if os.path.exists(cp):
        with open(cp, 'rb') as fh:
            stats, rat_cands, field_cands = pickle.load(fh)
        log('%s: loaded cached candidates (%d rational, %d irrational across '
            '%d d values)' % (name, len(rat_cands),
            sum(len(v) for v in field_cands.values()), len(field_cands)))
        return stats, rat_cands, field_cands

    all_planes = sorted(set(pl for pls in planes.values() for pl in pls))
    all_quads = [(j, qi, cd) for j, qs in quadrics.items()
                 for qi, cd in enumerate(qs)]
    nplanes, nquads = len(all_planes), len(all_quads)
    npairs = nplanes * (nplanes - 1) // 2
    nsystems = npairs * nquads
    log('%s: %d distinct planes, %d distinct quadrics -> %d plane-pairs x '
        '%d quadrics = %d (line, quadric) systems'
        % (name, nplanes, nquads, npairs, nquads, nsystems))

    stats = {'systems': nsystems, 'plane_pairs_total': npairs,
              'parallel_pairs': 0, 'degenerate_quadric': 0,
              'no_real_root': 0, 'rational_roots': 0, 'irrational_roots': 0,
              'zero_or_overcap': 0, 'd_distribution': {}}
    rat_cands = {}     # sym-orbit key -> pairs (original, cap-safe point)
    field_cands = {}   # d -> {sym-orbit key -> pairs}
    t0 = time.time()
    npair_done = 0
    for p1, p2 in itertools.combinations(all_planes, 2):
        line = line_from_planes(p1, p2)
        npair_done += 1
        if line is None:
            stats['parallel_pairs'] += 1
            continue
        P0, Dv = line
        for j, qi, cd in all_quads:
            alpha, beta, gamma = quad_on_line(cd, P0, Dv)
            kind, d, roots = classify_roots(alpha, beta, gamma)
            if kind == 'degenerate':
                stats['degenerate_quadric'] += 1
                continue
            if kind == 'no-real-root':
                stats['no_real_root'] += 1
                continue
            for rkind, rd, t in roots:
                pt = eval_point(P0, Dv, t)
                pairs = build_free_quat(pt, rd)
                if pairs is None:
                    stats['zero_or_overcap'] += 1
                    continue
                # orbit dedup under the free cube's own 24 rotations; the
                # point SUBMITTED stays the original (cap-safe) one, never
                # the rotated representative -- see notice above sym_key.
                key = sym_key(pairs)
                if rd == 0:
                    stats['rational_roots'] += 1
                    if key not in rat_cands:
                        rat_cands[key] = pairs
                else:
                    stats['irrational_roots'] += 1
                    stats['d_distribution'][rd] = stats['d_distribution'].get(rd, 0) + 1
                    bucket = field_cands.setdefault(rd, {})
                    if key not in bucket:
                        bucket[key] = pairs
        if npair_done % 2000 == 0:
            log('  %s: %d/%d plane-pairs done (%.0fs), rational cands %d, '
                'irrational cands %d' % (name, npair_done, npairs,
                time.time() - t0, len(rat_cands),
                sum(len(v) for v in field_cands.values())))

    log('%s: sweep done in %.0fs. stats=%s' % (name, time.time() - t0,
        {k: v for k, v in stats.items() if k != 'd_distribution'}))
    log('%s: d distribution (squarefree parts of irrational roots, RAW root '
        'instances before orbit dedup): %s' % (name, stats['d_distribution']))
    log('%s: distinct (orbit-deduped) rational candidates %d, distinct '
        'irrational candidates %d across %d distinct d values'
        % (name, len(rat_cands), sum(len(v) for v in field_cands.values()),
           len(field_cands)))

    with open(cp, 'wb') as fh:
        pickle.dump((stats, rat_cands, field_cands), fh)
    log('%s: cached candidates to %s' % (name, cp))
    return stats, rat_cands, field_cands


def evaluate_candidates(base, stats, rat_cands, field_cands, target, name):
    """Resumable engine evaluation: a JSONL checkpoint means a killed and
    restarted run repeats no completed engine call (never re-derive what a
    cache already answered)."""
    rp = results_path(name)
    done = {}
    if os.path.exists(rp):
        with open(rp) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                done[r['key']] = r
        log('%s: resuming from %d cached engine results in %s'
            % (name, len(done), rp))
    out = open(rp, 'a')

    def checkpoint(key, kind, d, pairs, tot, err):
        rec = {'key': key, 'kind': kind, 'd': d, 'pairs': pairs,
               'total': tot, 'error': err}
        out.write(json.dumps(rec) + '\n')
        out.flush()
        done[key] = rec

    B = 500

    # ---- rational candidates
    todo_keys = [k for k in rat_cands if rkey('rational', 0, rat_cands[k]) not in done]
    log('%s: rational candidates: %d total, %d already cached, %d to run'
        % (name, len(rat_cands), len(rat_cands) - len(todo_keys), len(todo_keys)))
    for s in range(0, len(todo_keys), B):
        chunk_keys = todo_keys[s:s+B]
        chunk = [rat_cands[k] for k in chunk_keys]
        res = run_rational_batch(base, chunk)
        for pairs, r in zip(chunk, res):
            key = rkey('rational', 0, pairs)
            tot = r.get('bounded')
            checkpoint(key, 'rational', 0, pairs, tot, r.get('error'))
        log('  %s: rational %d/%d evaluated' % (name, min(s+B, len(todo_keys)),
            len(todo_keys)))

    hist_rat, best_rat, refusals_rat = {}, (0, None), 0
    for k, pairs in rat_cands.items():
        r = done[rkey('rational', 0, pairs)]
        if r.get('error') is not None or r.get('total') is None:
            refusals_rat += 1
            continue
        tot = r['total']
        hist_rat[tot] = hist_rat.get(tot, 0) + 1
        if tot > best_rat[0]:
            best_rat = (tot, pairs)
    log('%s: rational candidates evaluated. refusals=%d, best=%s'
        % (name, refusals_rat, best_rat[0]))

    # ---- irrational candidates, grouped by d
    for d, cands in field_cands.items():
        todo_keys = [k for k in cands if rkey('irrational', d, cands[k]) not in done]
        if not todo_keys:
            continue
        for s in range(0, len(todo_keys), B):
            chunk_keys = todo_keys[s:s+B]
            chunk = [cands[k] for k in chunk_keys]
            try:
                res = run_field_batch(base, chunk, d)
            except Exception as e:
                log('  %s: field batch d=%d FAILED: %s' % (name, d, e))
                for pairs in chunk:
                    checkpoint(rkey('irrational', d, pairs), 'irrational', d,
                               pairs, None, str(e))
                continue
            for pairs, r in zip(chunk, res):
                key = rkey('irrational', d, pairs)
                checkpoint(key, 'irrational', d, pairs, r.get('bounded'),
                           r.get('error'))

    hist_irr, best_irr, refusals_irr = {}, (0, None, None), 0
    for d, cands in field_cands.items():
        for k, pairs in cands.items():
            r = done[rkey('irrational', d, pairs)]
            if r.get('error') is not None or r.get('total') is None:
                refusals_irr += 1
                continue
            tot = r['total']
            hist_irr[tot] = hist_irr.get(tot, 0) + 1
            if tot > best_irr[0]:
                best_irr = (tot, pairs, d)
    log('%s: irrational candidates evaluated. refusals=%d, best=%s (d=%s)'
        % (name, refusals_irr, best_irr[0], best_irr[2]))

    best_overall = max(best_rat, (best_irr[0], best_irr[1]), key=lambda x: x[0])
    best_d = 0 if best_overall[0] == best_rat[0] and best_rat[0] >= best_irr[0] \
        else best_irr[2]

    result = {
        'name': name, 'target': target, 'stats': stats,
        'rational': {'candidates': len(rat_cands), 'refusals': refusals_rat,
                     'hist': {str(k): v for k, v in hist_rat.items()},
                     'best': best_rat[0]},
        'irrational': {'candidates': sum(len(v) for v in field_cands.values()),
                        'distinct_d': len(field_cands), 'refusals': refusals_irr,
                        'hist': {str(k): v for k, v in hist_irr.items()},
                        'best': best_irr[0], 'best_d': best_irr[2]},
        'best_overall': best_overall[0],
        'reaches_or_exceeds_target': best_overall[0] >= target,
    }

    # ---- re-verify any candidate reaching/exceeding the target, independently
    reverified = []

    def reverify(pairs, d):
        if d == 0:
            r = run_rational_batch(base, [pairs])[0]
        else:
            r = run_field_batch(base, [pairs], d)[0]
        return r

    if best_rat[0] >= target and best_rat[1] is not None:
        r = reverify(best_rat[1], 0)
        log('%s: RE-VERIFY rational best %s -> %s' % (name, best_rat[0], r))
        reverified.append({'kind': 'rational', 'd': 0, 'quat': best_rat[1],
                            'reverify': r})
    if best_irr[0] >= target and best_irr[1] is not None:
        r = reverify(best_irr[1], best_irr[2])
        log('%s: RE-VERIFY irrational best %s (d=%s) -> %s'
            % (name, best_irr[0], best_irr[2], r))
        reverified.append({'kind': 'irrational', 'd': best_irr[2],
                            'quat': best_irr[1], 'reverify': r})
    result['reverified'] = reverified
    if reverified:
        log('%s: FULL QUATERNION LIST of record-reaching candidate(s):' % name)
        for rv in reverified:
            log('   base=%s free(d=%s)=%s -> %s'
                % (base, rv['d'], rv['quat'], rv['reverify']))
    return result


def main():
    global T0
    T0 = time.time()
    log('=== two_plus_quadric.py starting ===')

    # ---------------------------------------------------------- MANDATORY GATES
    gate([NBIN, '--quats',
          '1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4'], expect=183, label='n=4 183')
    gate([WBIN, '--d', '2', '--quats',
          '1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0'],
         expect=67, label='n=3 67 (Q(sqrt2))')

    report = {'gates': 'PASS'}

    for base, known, target, name in (
            (BASE4, KNOWN4, TARGET4, 'n=4_target183'),
            (BASE5, KNOWN5, TARGET5, 'n=5_target393')):
        log('\n--- building catalogs for %s (base=%s) ---' % (name, base))
        catp = cache_path('catalog', name)
        if os.path.exists(catp):
            with open(catp, 'rb') as fh:
                planes, quadrics = pickle.load(fh)
            log('%s: loaded cached plane/quadric catalog from %s' % (name, catp))
        else:
            edge = build_edge_conditions(base)
            corner = build_corner_conditions(base)
            planes = extract_planes(edge)
            quadrics = extract_quadrics(corner, planes)
            with open(catp, 'wb') as fh:
                pickle.dump((planes, quadrics), fh)
            log('%s: cached plane/quadric catalog to %s' % (name, catp))
        for j in range(len(base)):
            log('  cube %d: %d distinct planes, %d distinct quadrics'
                % (j, len(planes[j]), len(quadrics[j])))

        ctrl_ok = find_control(base, planes, quadrics, known, target, name)
        report.setdefault('controls', {})[name] = ctrl_ok

        stats, rat_cands, field_cands = classify_systems(base, planes, quadrics, name)
        res = evaluate_candidates(base, stats, rat_cands, field_cands, target, name)
        report[name] = res

    log('\n=== FINAL SUMMARY ===')
    for name in ('n=4_target183', 'n=5_target393'):
        r = report[name]
        log('%s: control=%s, rational best=%d (over %d candidates, %d '
            'refusals), irrational best=%d at d=%s (over %d candidates '
            'across %d distinct d, %d refusals), best overall=%d, '
            'reaches/exceeds target %d: %s'
            % (name, report['controls'][name], r['rational']['best'],
               r['rational']['candidates'], r['rational']['refusals'],
               r['irrational']['best'], r['irrational']['best_d'],
               r['irrational']['candidates'], r['irrational']['distinct_d'],
               r['irrational']['refusals'], r['best_overall'],
               r['target'], r['reaches_or_exceeds_target']))

    with open('two_plus_quadric.json', 'w') as fh:
        json.dump(report, fh, indent=1, default=str)
    log('wrote two_plus_quadric.json')


if __name__ == '__main__':
    main()
