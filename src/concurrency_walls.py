#!/usr/bin/env python3
"""A wall family this project has never enumerated: FOUR FACE PLANES THROUGH A POINT.

HOW IT WAS FOUND.  The wall census ([OPEN_QUESTIONS 33]) counts regions in each cell
between consecutive solved walls, and its constancy gate G2 reported a cell on ray
e0 from the 727 record whose two ends disagreed: 693 at t = -5/24, 691 at t = -2/9.
Every neighbour of -2/9 gives 693 and -2/9 itself gives 691 -- an isolated drop of
two regions.  Both engines agree there, and the count is unchanged by rescaling the
quaternion, so it is geometry and not arithmetic.

AND NO COINCIDENCE CONDITION IS TIGHT THERE.  The tight set at t = -2/9 is the same
144 conditions as at its neighbours, with nothing gained and nothing lost.  The
project's entire wall machinery -- `conditions_on`, `wall_keys`, the polynomials in
`data/wall_polynomials.json` -- enumerates coincidences of face NORMALS, and this
degeneracy is not one.

WHAT IT IS.  At t = -2/9 six quadruples of face planes become concurrent, all of them
spanning cubes 1, 2, 3, 4 -- for instance

    (cube 1, axis 0, -)   (cube 2, axis 0, +)   (cube 3, axis 0, -)   (cube 4, axis 0, -)

with the antipodal image of each.  The same thing happens at t = -4/27, where eight
quadruples arrive across cubes {0,1,2,4} and {0,1,3,4}, and the count drops 705 -> 703.
Both are solved, not sampled: each quadruple's determinant restricted to the ray is an
exact polynomial and the parameter is one of its roots.

WHY IT IS A WALL OF THE COUNT.  A region is a component of constant cube-containment,
bounded by pieces of real faces.  Its vertices are triple points of face planes; when
a fourth plane passes through one, two vertices merge and a cell can close.  That is
codimension one in the configuration, exactly like a normal coincidence, and it is
invisible to every condition this project enumerates.

THE METHOD HERE is interpolation, not symbolic determinants: the determinant of the
4x4 is evaluated in exact rational arithmetic at DEG+1 parameters and interpolated,
which is exact for a polynomial of degree <= DEG.  DEG is then CHECKED rather than
assumed -- the interpolant is verified at extra parameters it did not see, and a
disagreement means the degree bound was too low and is reported, never absorbed.
"""
import sys, os, json, time, argparse
from fractions import Fraction as F
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import sympy as sp
import dimension as D
import wall_keys as W

T = sp.Symbol('t')
DEG = 8           # degree bound for the determinant along a ray; VERIFIED, not assumed
CHECK = 3         # extra parameters the interpolant must also reproduce


def mat_unnormalised(q):
    """(numerator rows of the rotation, the common denominator) for a quaternion.

    UNNORMALISED ON PURPOSE.  The face plane of a cube is `row . x = n`, with `row`
    and `n` both POLYNOMIAL in the ray parameter once the quaternion is written
    (1, c0, c1, c2) with c linear in t.  Dividing through by n first is what broke
    the first version of this file: the concurrency determinant then became a
    RATIONAL function, the polynomial interpolation was invalid, and the degree
    check -- correctly -- refused every quadruple, including the one already known
    to be there.  The check caught it; the gate is what made the check matter.
    """
    w, x, y, z = [F(v) for v in q]
    n = w * w + x * x + y * y + z * z
    return [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]], n


def planes_at(pt, dirn, q0, s):
    """The 6n face planes at parameter s, as (normal, offset) with both unnormalised.

    THE NORMALS ARE THE COLUMNS OF THE ROTATION, NOT THE ROWS.  `dimension.normals_sym`
    says so ("face normals of cube j in cube i's frame: COLUMNS of R_i^T R_j"), and
    `euler3`/`cellcomplex` use `rowsT`, the transpose.  The first version of this file
    used the rows, which is the plane set of a DIFFERENT configuration -- every cube
    rotated by its inverse -- and it silently produced a whole wrong table
    ([FAILURE_MODES 39], and the correction dated inside [P304]).  The convention is
    settled by the only independent count in the project: `cellcomplex.complexus`
    reproduces the engine exactly in this convention.
    """
    c = [pt[k] + s * dirn[k] for k in range(len(pt))]
    quats = [q0] + [(1, c[k], c[k + 1], c[k + 2]) for k in range(0, len(c), 3)]
    out = []
    for i, q in enumerate(quats):
        M, n = mat_unnormalised(q)
        for k in range(3):
            for sg in (1, -1):
                out.append(((i, k, sg), [sg * M[cc][k] for cc in range(3)] + [n]))
    return out


def concur_det(r1, r2, r3, r4):
    """det of the 4x4 [normal | offset]: zero exactly when the four planes concur.

    Written out by cofactors rather than eliminated, because it is evaluated a third
    of a million times per ray and the entries are exact Fractions.
    """
    m = (r1, r2, r3, r4)

    def d3(a, b, c, cols):
        (i, j, k) = cols
        return (a[i] * (b[j] * c[k] - b[k] * c[j])
                - a[j] * (b[i] * c[k] - b[k] * c[i])
                + a[k] * (b[i] * c[j] - b[j] * c[i]))
    tot = F(0)
    sgn = 1
    for col in range(4):
        cols = tuple(x for x in range(4) if x != col)
        rest = [m[r] for r in range(1, 4)]
        tot += sgn * m[0][col] * d3(rest[0], rest[1], rest[2], cols)
        sgn = -sgn
    return tot


def newton_poly(xs, ys):
    """Exact interpolating polynomial coefficients, highest degree first."""
    n = len(xs)
    coef = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    out = [F(0)] * n                       # Horner expansion into monomial form
    for k in range(n - 1, -1, -1):
        new = [F(0)] * n
        for d in range(n - 1):
            new[d + 1] += out[d]
        for d in range(n):
            new[d] -= xs[k] * out[d] if d < n else F(0)
        new[0] += coef[k]
        out = new
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out[::-1]


def _polyval(c, x):
    v = F(0)
    for a in c:
        v = v * x + a
    return v


def _divmod(a, b):
    """Polynomial division over the rationals, coefficients highest-first."""
    a = list(a)
    out = []
    while len(a) >= len(b) and any(a):
        if a[0] == 0:
            a.pop(0)
            continue
        f = a[0] / b[0]
        out.append(f)
        for i in range(len(b)):
            a[i] -= f * b[i]
        a.pop(0)
    while len(a) > 1 and a[0] == 0:
        a.pop(0)
    return out, a


def sturm_count(c, lo, hi):
    """Number of distinct real roots of c in (lo, hi], exactly, by Sturm's theorem.

    Used only as a FILTER: a quadruple whose determinant has no root on the ray is
    dropped before any symbolic work happens.  Exactness matters even for a filter --
    a numeric filter that drops a real wall would recreate the very gap this file
    exists to close.
    """
    if len(c) < 2:
        return 0
    seq = [list(c)]
    d = [c[i] * (len(c) - 1 - i) for i in range(len(c) - 1)]
    if not any(d):
        return 0
    seq.append(d)
    while len(seq[-1]) > 1:
        _, r = _divmod(seq[-2], seq[-1])
        r = [-x for x in r]
        while len(r) > 1 and r[0] == 0:
            r.pop(0)
        if not any(r):
            break
        seq.append(r)

    def signs(x):
        out = []
        for p in seq:
            v = _polyval(p, x)
            if v != 0:
                out.append(1 if v > 0 else -1)
        return sum(1 for i in range(len(out) - 1) if out[i] != out[i + 1])
    return signs(lo) - signs(hi)


def moving_cubes(dirn):
    """Which cubes the direction actually moves.  Cube 0 is the gauge and fixed."""
    return {1 + k // 3 for k in range(len(dirn)) if dirn[k] != 0}


def concurrency_walls(quats, dirn, lo, hi, verbose=True):
    """Every four-plane-concurrency wall on the ray, solved.

    Only quadruples containing a plane of a MOVING cube can move; the rest are
    constant in t and contribute no wall.  That is not an approximation: a
    determinant with no t in it is either identically zero or nowhere zero.
    """
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    q0 = quats[0]
    mov = moving_cubes(dirn)
    ts = [F(i + 1, 7) - F(1, 3) for i in range(DEG + 1 + CHECK)]   # distinct, small
    snap = [planes_at(pt, dirn, q0, s) for s in ts]
    labels = [p[0] for p in snap[0]]
    idx = {lab: i for i, lab in enumerate(labels)}
    t0 = time.time()

    rows_out, n_quads, degree_fail = [], 0, 0
    for combo in combinations(labels, 4):
        if not any(lab[0] in mov for lab in combo):
            continue
        n_quads += 1
        ii = [idx[lab] for lab in combo]
        vals = [concur_det(*[snap[si][j][1] for j in ii]) for si in range(len(ts))]
        co = newton_poly(ts[:DEG + 1], vals[:DEG + 1])
        if not all(_polyval(co, ts[DEG + 1 + j]) == vals[DEG + 1 + j]
                   for j in range(CHECK)):
            degree_fail += 1          # the degree bound was too low: reported, never absorbed
            continue
        if len(co) < 2:
            continue
        if sturm_count(co, F(str(lo)), F(str(hi))) == 0:
            continue
        Pp = sp.Poly([sp.Rational(x) for x in co], T)
        roots = []
        for r in sp.real_roots(Pp.sqf_part(), radicals=False):
            fr = float(r)
            if lo <= fr <= hi:
                roots.append({'decimal': fr,
                              'rational': str(sp.Rational(r)) if r.is_Rational else None})
        if roots:
            rows_out.append({'planes': [list(l) for l in combo],
                             'cubes': sorted({l[0] for l in combo}),
                             'degree': len(co) - 1,
                             'polynomial': [str(x) for x in co],
                             'roots': roots})
    if verbose:
        print('   concurrency: %d quadruples touched by the ray | %d with a root in '
              '[%g, %g] | %d degree-bound failures  (%.0fs)'
              % (n_quads, len(rows_out), lo, hi, degree_fail, time.time() - t0),
              flush=True)
    return {'quadruples_examined': n_quads, 'walls_with_roots': len(rows_out),
            'degree_bound': DEG, 'degree_bound_failures': degree_fail,
            'walls': rows_out}


def gate(quats, dirn):
    """G4: the known -2/9 concurrency on ray e0 must come back, with its quadruple.

    An anchor outside the method: the wall was located by a count disagreement and
    confirmed by an independent symbolic determinant before this file existed.
    """
    r = concurrency_walls(quats, dirn, -0.3, -0.1, verbose=False)
    want = [(1, 0, -1), (2, 0, 1), (3, 0, -1), (4, 0, -1)]
    for w in r['walls']:
        if [tuple(p) for p in w['planes']] == want:
            hit = [x for x in w['roots'] if x['rational'] == '-2/9']
            return bool(hit), w
    return False, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', type=int, default=6)
    ap.add_argument('--window', type=float, default=0.25)
    ap.add_argument('--rays', default='e0')
    ap.add_argument('--gate', action='store_true')
    a = ap.parse_args()
    quats = W.REC[a.n]
    D.set_field(0); D.QZERO[:] = [quats[0]]
    nc = len(D.point_of(quats))

    def axis(k):
        d = [F(0)] * nc; d[k] = F(1); return d

    if a.gate:
        ok, w = gate(quats, axis(0))
        print('G4 %s' % ('ok: the -2/9 concurrency is returned with its quadruple'
                         if ok else 'FAILED: the known concurrency was not found'))
        if w:
            print('   ', json.dumps(w))
        raise SystemExit(0 if ok else 1)

    out = {'what': 'four-plane concurrency walls -- a codimension-1 wall family of the '
                   'COUNT that no coincidence condition sees',
           'found_by': 'G2 of the wall census, on ray e0 at t = -2/9 (P304)',
           'n': a.n, 'quats': [list(q) for q in quats], 'rays': {}}
    path = os.path.join(ROOT, 'data', 'concurrency_walls_n%d.json' % a.n)
    if os.path.exists(path):
        try:
            prev = json.load(open(path))
            if isinstance(prev.get('rays'), dict):
                out['rays'].update(prev['rays'])
        except Exception:
            pass
    for lab in a.rays.split(','):
        k = int(lab[1:])
        print(lab, flush=True)
        out['rays'][lab] = concurrency_walls(quats, axis(k), -a.window, a.window)
        json.dump(out, open(path, 'w'), indent=1)
    print('written %s' % os.path.relpath(path, ROOT))


if __name__ == '__main__':
    main()
