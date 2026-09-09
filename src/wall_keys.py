#!/usr/bin/env python3
"""Record what is needed to RECONSTRUCT every wall polynomial, exactly.

The gap this closes.  data/record_walls.json records wall GRADIENTS -- the
linearisation of each wall at the record point.  A gradient cannot be solved for
a locus, so the bracket -> wall -> polynomial -> root chain had no second link.
The polynomials themselves were never recorded and are expensive to expand in
3(n-1) variables, so recording them is the wrong deliverable anyway.

What IS recorded here is the KEY.  A wall is completely determined by

    (frame i, group ((j,k,sgn),...), sig, c0)

and the configuration it sits at.  Nothing else -- no gradient, no expression --
enters dimension.branch_numerator, which returns the exact polynomial P with

    f = 1  <=>  P = 0            (P = D * lead * (f - 1),  D = N_i N_j)

So the key plus the record point IS the polynomial, in the same sense that a
matrix's entries are its determinant.  These keys were already being computed and
cached (dimension_cache, 587 entries) but the cache is content-keyed by
configuration hash: nothing tied an entry to a NAMED record, so no reader could
find the wall of a record they cared about.  This writes that index down.

INVARIANT for anyone editing this file: KEY_FIELDS is the complete argument list
of branch_numerator.  If a field is dropped from the export the polynomial stops
being reconstructible, and the loss is silent -- the gradients still export fine
and every gate below still passes on whatever remains.  Add fields; never remove.

on_line() is the chain link the n=9 bracket needs: it restricts a wall to the
line q(t) = A + t*D and returns the exact univariate coefficients, so a bracket
can be turned into a root instead of narrowed forever by bisection.
"""
import json, sys, os, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE

def relpath(p):
    """Report paths relative to the repository, never as resolved absolutes.

    Logs and run records are quoted in documents that get published, and a
    resolved path carries the account layout of whatever machine produced it.
    The value is also just less useful to a reader: `data/x.json` locates the
    file in the repo, an absolute path locates it on one host.
    """
    try:
        return os.path.relpath(p, ROOT)
    except ValueError:
        return os.path.basename(p)

import sympy as sp
import dimension as D

KEY_FIELDS = ('frame', 'group', 'sig', 'c0')

B5 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
REC = {4: [B5[i] for i in (0, 1, 2, 4)], 5: B5, 6: B5 + [(7, 14, 1, -5)],
       7: B5 + [(7, 14, 1, -5), (4, -3, -4, -4)],
       8: B5 + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61)]}
# 183 is deliberately present and deliberately expected to FAIL: cube 1 is a
# half-turn, so the record is at Cayley infinity and has no point in this chart.
# That is P287's artefact.  Unevaluable is reported as unevaluable, not skipped.
FIELD = {'oct67': 2, 'golden67': 5}     # DFIELD per named record; 0 elsewhere
Q67 = {2: [((1, 0), (0, 0), (0, 0), (0, 0)), ((1, 0), (1, 0), (0, 1), (0, 0)),
           ((-1, 0), (1, 0), (0, 1), (0, 0))],
       5: [((2, 0), (0, 0), (0, 0), (0, 0)), ((2, 0), (1, 1), (-1, 1), (0, 0)),
           ((-2, 0), (1, 1), (-1, 1), (0, 0))]}
NAMED = {'n4_183': [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
         'arcA': B5 + [(6, 53, -87, -156)]}


def _sp3(c):
    """Field element -> sympy, via dimension's OWN converter.

    NOT sp.Rational and NOT str(): over Q(sqrt d) the coordinates are QF objects
    whose str is "1/2+1/2\u221a5", which sympify cannot parse -- that error was
    the whole reason the two 67s were absent from this index.  `D._sp` is
    `qf_to_sp` and handles both Fractions and QF, so one converter covers every
    field the project uses.
    """
    return None if c is None else [D._sp(x) for x in c]


def cvecs_of(quats, tvars=None):
    """Cayley vectors for branch_numerator: cube 0 frozen, cubes 1.. as given."""
    out = [_sp3(D.cayley_of(quats[0]))]
    for j, q in enumerate(quats[1:]):
        out.append(tvars[j] if tvars is not None else _sp3(D.cayley_of(q)))
    return out


def numerator(key, cvecs):
    """The wall's exact polynomial.  P == 0 is the wall; P != 0 is off it."""
    return D.branch_numerator({k: key[k] for k in KEY_FIELDS}, cvecs)


def on_line(key, q0, pt, dirn):
    """Wall restricted to q(t) = pt + t*dirn -- exact coefficients, low degree
    first.  This is what a bracket gets solved against."""
    t = sp.Symbol('t')
    n = len(pt) // 3 + 1
    tv = [[sp.Rational(pt[3 * j + c]) + t * sp.Rational(dirn[3 * j + c])
           for c in range(3)] for j in range(n - 1)]
    P = sp.expand(numerator(key, [_sp3(D.cayley_of(q0))] + tv))
    if P == 0:
        return [F(0)]
    return [F(str(c)) for c in reversed(sp.Poly(P, t).all_coeffs())]


def walls_of(quats, use_cache=True, dfield=0):
    """Distinct walls at a configuration: full keys, deduped by gradient ray."""
    q0 = quats[0]
    D.set_field(dfield); D.QZERO[:] = [q0]
    pt = D.point_of(quats)
    if pt is None:
        return None, None
    ncols = 3 * (len(quats) - 1)
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, q0)
    get = D.cached_conditions if use_cache else D.conditions
    tight, loose = (get(Rs, len(quats), vars_, pt, D.quats_of(pt, q0), q0)
                    if use_cache else get(Rs, len(quats), vars_, pt,
                                          D.quats_of(pt, q0)))
    good = [t for t in tight if not t['degenerate']]
    seen, walls = set(), []
    for t in good:
        g = t['grad']
        piv = next((x for x in g if x != 0), None)
        if piv is None:
            continue
        k = tuple(str(x / piv) for x in g)
        if k in seen:
            continue
        seen.add(k)
        walls.append(t)
    return pt, walls


def _dirs(ncols, howmany=3):
    """Deterministic probe directions, NOT axis-aligned: an axis-only probe is
    the failure that made map_shapes2 read 0-dimensional everywhere."""
    out = []
    for s in range(howmany):
        out.append([F((7 * (i + 1) + 13 * s) % 11 - 5, 1 + (i + s) % 3)
                    for i in range(ncols)])
    return out


def gate(quats, label, walls, pt, verbose=True, dfield=0):
    """Anchors OUTSIDE the reconstruction, so agreement is not self-agreement.

    G1  P(record) == 0            -- absolute; the wall must contain its point.
    G2  dP/dt|0 == s * (grad.d)   -- ONE scale s across independent directions;
                                     grad came from sympy diff of f, P from the
                                     cancelled-numerator formula.  Two routes.
    G3  negative control: corrupt the key (flip one sign in sig) and G1 must
        FAIL.  Without this, a gate that reconstructs nothing passes silently.
    """
    q0 = quats[0]
    ncols = len(pt)
    ds = _dirs(ncols)
    res = {'label': label, 'walls': len(walls), 'g1_zero': 0, 'g1_fail': [],
           'g2_ok': 0, 'g2_fail': [], 'g3_control_caught': 0, 'g3_missed': []}
    if dfield:
        res['g2_fail'] = ['NOT APPLICABLE over Q(sqrt %d): the probe line is '
                          'rational and on_line takes sp.Rational coordinates. '
                          'Reported as unevaluated, not as a pass.' % dfield]
    for idx, w in enumerate(walls):
        cv = cvecs_of(D.quats_of(pt, q0))
        P0 = numerator(w, cv)
        if sp.simplify(P0) == 0:
            res['g1_zero'] += 1
        else:
            res['g1_fail'].append([idx, str(P0)[:60]])
            continue
        scales = []
        for d in ([] if dfield else ds):
            co = on_line(w, q0, pt, d)
            lin = co[1] if len(co) > 1 else F(0)
            gd = sum(F(a) * b for a, b in zip(w['grad'], d))
            if gd == 0:
                if lin != 0:
                    scales.append(None)
                continue
            scales.append(F(lin) / gd)
        s = [x for x in scales if x is not None]
        if dfield:
            pass                       # G2 unevaluated over a field, see above
        elif scales and all(x is not None for x in scales) and s and len(set(s)) == 1:
            res['g2_ok'] += 1
        else:
            res['g2_fail'].append([idx, [str(x) for x in scales]])
        bad = dict(w)
        bad['sig'] = [(-v if c == 0 else v) for c, v in enumerate(w['sig'])]
        if bad['sig'] == w['sig']:
            bad['sig'] = [-v for v in w['sig']]
        if sp.simplify(numerator(bad, cv)) != 0:
            res['g3_control_caught'] += 1
        else:
            res['g3_missed'].append(idx)
    if verbose:
        print('%-9s walls %3d | G1 %3d/%3d | G2 %3d | G3 caught %3d/%3d'
              % (label, res['walls'], res['g1_zero'], res['walls'],
                 res['g2_ok'], res['g3_control_caught'], res['g1_zero']),
              flush=True)
    return res


def main():
    only = sys.argv[1:] or None
    out = {'what': 'reconstruction keys for every wall at every named record',
           'why': ('gradients (data/record_walls.json) are linearisations and '
                   'cannot be solved for a locus; these keys ARE the polynomials, '
                   'via dimension.branch_numerator'),
           'reconstruct': ('import wall_keys as W; '
                           'W.numerator(key, W.cvecs_of(quats))  -> exact P, '
                           'wall is P == 0; '
                           'W.on_line(key, q0, pt, dir) -> univariate in t'),
           'key_fields': list(KEY_FIELDS),
           'IMPORTANT': ('the key is complete ONLY together with the record '
                         'quaternions stored beside it: the same key at another '
                         'configuration is a different polynomial'),
           'records': {}}
    p = os.path.join(ROOT, 'data', 'wall_keys.json')
    # MERGE, never replace.  A run restricted to one record used to rebuild `out`
    # from scratch and dump it, silently DELETING every record it had not been
    # asked to recompute -- `wall_keys.py 4` reduced a six-record index to one,
    # and nothing said so.  An export that drops what it did not measure is a
    # deletion wearing a write's clothes.  INVARIANT: this file only ever grows
    # or updates in place; removing a record must be a deliberate, separate act.
    if os.path.exists(p):
        try:
            prev = json.load(open(p))
            if isinstance(prev.get('records'), dict):
                out['records'].update(prev['records'])
        except Exception:
            pass
    from fractions import Fraction as _F
    try:
        from qfield import Q as _Q
        F67 = {lab: [tuple(_Q(_F(a), _F(b), FIELD[lab]) for a, b in quat)
                     for quat in Q67[FIELD[lab]]] for lab in FIELD}
    except Exception:
        F67 = {}
    todo = ([(str(n), q) for n, q in sorted(REC.items())] + sorted(NAMED.items())
            + sorted(F67.items()))
    for label, quats in todo:
        if only and label not in only:
            continue
        df = FIELD.get(label, 0)
        try:
            pt, walls = walls_of(quats, dfield=df)
        except Exception as e:
            out['records'][label] = {'error': type(e).__name__ + ': ' + str(e)[:90],
                                     'quats': [list(q) for q in quats]}
            print('%-9s FAILED %s' % (label, type(e).__name__), flush=True)
            json.dump(out, open(p, 'w'), indent=1)
            continue
        if pt is None:
            out['records'][label] = {
                'quats': [list(q) for q in quats],
                'unevaluable': 'at Cayley infinity (a cube has w == 0); this '
                               'chart has no point for it -- see P287',
                'walls': None}
            print('%-9s UNEVALUABLE (Cayley infinity)' % label, flush=True)
            json.dump(out, open(p, 'w'), indent=1)
            continue
        g = gate(quats, label, walls, pt, dfield=df)
        out['records'][label] = {
            'quats': [[str(x) for x in q] for q in quats],
            'field': ('Q(sqrt %d)' % df) if df else 'Q',
            'point': [str(x) for x in pt],
            'ambient': len(pt),
            'distinct_walls': len(walls),
            'gate': g,
            'keys': [{'frame': w['frame'],
                      'group': [list(x) for x in w['group']],
                      'sig': list(w['sig']), 'c0': w['c0'],
                      'grad': [str(x) for x in w['grad']]} for w in walls]}
        json.dump(out, open(p, 'w'), indent=1)
    print('written', relpath(p))


if __name__ == '__main__':
    main()


# ---------------------------------------------------------------------------
# Quaternion-linear families.
#
# on_line() above takes a line in CAYLEY coordinates.  The families this project
# actually brackets are linear in QUATERNIONS -- solve_wall.py moves the tenth
# cube along q(t) = (12-t)A + tB -- and a quaternion line is a Moebius curve in
# Cayley coordinates, not a line.  Restricting a wall to it therefore needs the
# condition rebuilt over (M, N) pairs rather than over Cayley triples.
#
# The formula is dimension.branch_numerator's, unchanged; only the source of
# (M, N) differs.  M/N is the rotation in both cases, which is the whole content
# of the cancellation that formula relies on.  gate_mn() checks the two routes
# against each other on a record where both apply -- they must be PROPORTIONAL,
# not equal: Cayley uses N = 1 + |c|^2 and quaternions use N = |q|^2, and those
# differ by w^2 per cube.  A wall is a hypersurface, so proportional is identical.
# ---------------------------------------------------------------------------

def MN_of_quat(q):
    """Unnormalised rotation matrix and its scale: M/N is the rotation."""
    w, x, y, z = q
    N = w * w + x * x + y * y + z * z
    M = sp.Matrix([[w*w + x*x - y*y - z*z, 2*(x*y - w*z), 2*(x*z + w*y)],
                   [2*(x*y + w*z), w*w - x*x + y*y - z*z, 2*(y*z - w*x)],
                   [2*(x*z - w*y), 2*(y*z + w*x), w*w - x*x - y*y + z*z]])
    return M, N


def numerator_MN(key, MNs):
    """dimension.branch_numerator's formula over explicit (M, N) pairs."""
    i = key['frame']
    Ms = [m for m, _ in MNs]; Ns = [n for _, n in MNs]
    m = {}
    for (j, k, sgn) in key['group']:
        A = Ms[i].T * Ms[j]
        m[(j, k, sgn)] = ([sgn * A[r, k] for r in range(3)], Ns[i] * Ns[j])
    g, sig, c0 = key['group'], key['sig'], key['c0']
    if len(g) == 1:
        mm, den = m[g[0]]
        return sp.expand(sum(sig[c] * mm[c] for c in range(3) if c != c0) - den)
    (m1, d1), (m2, d2) = m[g[0]], m[g[1]]
    # see dimension.branch_numerator: d1 != d2 whenever the group's two normals
    # come from different cubes, and then lambda*'s denominators do not cancel.
    return sp.expand(sum(sig[c] * (m2[c0]*m1[c] - m1[c0]*m2[c])
                         for c in range(3) if c != c0)
                     - (m2[c0] * d1 - m1[c0] * d2))


def on_quat_line(key, quats, moving, A, B, span=1):
    """Wall restricted to the family that moves cube `moving` along
    q(t) = (span - t)*A + t*B, every other cube held at its record quaternion.

    Returns exact coefficients in t, low degree first -- the univariate whose
    root IS the wall, which is what a bracket is for.
    """
    t = sp.Symbol('t')
    qt = [sp.Rational(span) * sp.Integer(a) - t * sp.Integer(a) + t * sp.Integer(b)
          for a, b in zip(A, B)]
    MNs = [MN_of_quat([sp.Integer(v) for v in q]) for q in quats]
    MNs[moving] = MN_of_quat(qt)
    P = sp.expand(numerator_MN(key, MNs))
    if P == 0:
        return [F(0)]
    return [F(str(c)) for c in reversed(sp.Poly(P, t).all_coeffs())]


def _proportional(u, v):
    """u and v are the same hypersurface iff their coefficient vectors are
    parallel.  Compared as vectors, not as strings: a string gate whose two
    sides are built the same way tests nothing."""
    nz = [(a, b) for a, b in zip(u, v) if a != 0 or b != 0]
    if not nz:
        return True
    r = None
    for a, b in nz:
        if a == 0 or b == 0:
            return False
        if r is None:
            r = F(b) / F(a)
        elif F(b) / F(a) != r:
            return False
    return r is not None


def gate_mn(label='4'):
    """Anchor the quaternion route against the Cayley route on one record."""
    quats = REC[int(label)] if label.isdigit() else NAMED[label]
    pt, walls = walls_of(quats)
    cv = cvecs_of(D.quats_of(pt, quats[0]))
    ok = bad = 0
    for w in walls:
        Pc = sp.expand(numerator(w, cv))
        Pq = sp.expand(numerator_MN(w, [MN_of_quat([sp.Integer(v) for v in q])
                                        for q in quats]))
        # both are numbers here (record point, no free variable): proportional
        # means both zero, since the wall contains the record.
        if Pc == 0 and Pq == 0:
            ok += 1
        else:
            bad += 1
    # a real proportionality test needs a VARYING point, so also compare the two
    # routes along a Cayley line, where both can be evaluated.
    d = _dirs(len(pt))[0]
    par = notpar = 0
    for w in walls:
        cay = on_line(w, quats[0], pt, d)
        t = sp.Symbol('t')
        MNs = []
        for j, q in enumerate(quats):
            if j == 0:
                MNs.append(MN_of_quat([sp.Integer(v) for v in q]))
            else:
                c = [sp.Rational(pt[3*(j-1)+k]) + t*sp.Rational(d[3*(j-1)+k])
                     for k in range(3)]
                x, y, z = c
                Nn = 1 + x*x + y*y + z*z
                Mm = sp.Matrix([[1+x*x-y*y-z*z, 2*(x*y-z), 2*(x*z+y)],
                                [2*(x*y+z), 1-x*x+y*y-z*z, 2*(y*z-x)],
                                [2*(x*z-y), 2*(y*z+x), 1-x*x-y*y+z*z]])
                MNs.append((Mm, Nn))
        P = sp.expand(numerator_MN(w, MNs))
        q_co = ([F(0)] if P == 0
                else [F(str(c)) for c in reversed(sp.Poly(P, t).all_coeffs())])
        n = max(len(cay), len(q_co))
        u = cay + [F(0)] * (n - len(cay)); v = q_co + [F(0)] * (n - len(q_co))
        if _proportional(u, v):
            par += 1
        else:
            notpar += 1
    print('gate_mn %s: vanish-at-record %d/%d, route-agreement %d/%d'
          % (label, ok, ok + bad, par, par + notpar), flush=True)
    return ok, bad, par, notpar
