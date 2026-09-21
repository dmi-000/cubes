#!/usr/bin/env python3
"""[OQ 39] THE LAST LIVE BRANCH, ENUMERATED: every six-sharing 4-compound, exactly.

[P368] reduced `max(4) = 183` to one escape from `EE + B <= 164`: six corner-sharings with
`Q4 = 0`, which would need `EE + B >= 152` where the known `K4` measures 110.  That row is not a
search problem.

**THE REDUCTION.**  Two cubes share a corner iff they share a body-diagonal DIRECTION ([P334]).
Fix cube 0 as the standard cube and let cubes 1, 2, 3 share its diagonals `d1, d2, d3`.  The
three remaining sharings are then three unknown directions `s12, s13, s23`, and every constraint
on them is an INNER PRODUCT taking one of four values:

    s12 is a diagonal of cube 1 and of cube 2   =>  <s12,d1>, <s12,d2>  in  {+-1/3, +-1}
    s13 ...                                     =>  <s13,d1>, <s13,d3>  in  {+-1/3, +-1}
    s23 ...                                     =>  <s23,d2>, <s23,d3>  in  {+-1/3, +-1}
    cube 1 holds d1, s12, s13 together          =>  <s12,s13>           in  {+-1/3, +-1}
    cube 2 holds d2, s12, s23 together          =>  <s12,s23>           in  {+-1/3, +-1}
    cube 3 holds d3, s13, s23 together          =>  <s13,s23>           in  {+-1/3, +-1}

Two linear conditions and one norm give at most TWO directions per `(alpha, beta)` pair, so each
`s` ranges over a finite explicit set -- and the whole variety is a finite list to filter, not a
region to sample.  The coordinates come out as `0, +-sqrt3/3` and `+-(sqrt3 +- sqrt15)/6` -- the
**fourth** independent appearance of [P334]'s `p, q`, so `Q(sqrt3, sqrt5)` is the right field and
`src/kfield.py` closes over it.

Three vectors with pairwise `|dot| = 1/3` are the diagonals of a cube only when they can be
SIGNED to make all three dots `-1/3`; that filter is applied, and the fourth diagonal is then
`-(u1+u2+u3)`.  Cases where two of the three directions coincide are three cubes on ONE axis and
are reported separately rather than dropped.

Every surviving compound is censused in exact arithmetic and scored against
`TOTAL = 7 + EE + 2*SC2 + B - Q4`.
"""
import sys, os, json, itertools, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from kfield import K
import mpmath as mp
import paw_construction as PAW          # reuse its exact census; prints at import
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
R3 = K(0, 1, 0, 0); R15 = K(0, 0, 0, 1)
T3 = R3 * K(F(1, 3))                    # 1/sqrt3
P = (R3 + R15) * K(F(1, 6))             # (sqrt3 + sqrt15)/6
Q = (R3 - R15) * K(F(1, 6))             # (sqrt3 - sqrt15)/6
M13 = K(F(-1, 3))

# every coordinate the candidate directions can take, with its numeric value for RECOGNITION.
# recognition is only a lookup; each vector built from it is then CERTIFIED by exact assertions.
ATOMS = {}
for name, v in (('0', K(0)), ('1', K(1)), ('t3', T3), ('p', P), ('q', Q)):
    for s in (1, -1):
        w = K.lift(v) * K(s)
        ATOMS[float(w.num())] = w


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def sm(s, u):
    return [K.lift(s) * t for t in u]


def add(*us):
    return [sum((u[i] for u in us[1:]), us[0][i]) for i in range(3)]


def recognise(x, tol=1e-12):
    best = None
    for f, w in ATOMS.items():
        if abs(f - x) < tol and (best is None or abs(f - x) < abs(best[0] - x)):
            best = (f, w)
    return best[1] if best else None


def candidates(a, b, af, bf):
    """exact unit vectors s with <s,a> = af and <s,b> = bf, found numerically then certified."""
    import numpy as np
    an = np.array([float(t.num()) for t in a]); bn = np.array([float(t.num()) for t in b])
    M = np.array([an, bn]); rhs = np.array([float(af.num()), float(bf.num())])
    p, *_ = np.linalg.lstsq(M, rhs, rcond=None)
    if np.linalg.norm(M @ p - rhs) > 1e-12:
        return [], 0
    n = np.cross(an, bn)
    if n @ n < 1e-12:
        return [], 0
    n = n / np.sqrt(n @ n)
    r2 = 1 - p @ p
    if r2 < -1e-12:
        return [], 0
    r = np.sqrt(max(r2, 0.0))
    out = []; lost = 0
    for cand in ([p + r * n, p - r * n] if r > 1e-9 else [p]):
        ex = [recognise(float(c)) for c in cand]
        if any(e is None for e in ex):
            lost += 1                       # a coordinate outside the atom set: NOT dropped
            continue                        # silently -- counted and reported
        if dot(ex, a) != af or dot(ex, b) != bf or dot(ex, ex) != K(1):
            lost += 1
            continue
        out.append(ex)
    return out, lost


def dedup(vs):
    keep = []
    for s in vs:
        if not any(all((s[i] - t[i]).is_zero() for i in range(3)) or
                   all((s[i] + t[i]).is_zero() for i in range(3)) for t in keep):
            keep.append(s)
    return keep


def diag_ok(u, v):
    """|<u,v>| is 1/3 or 1 -- exactly"""
    d = dot(u, v)
    return any((d - K(x)).is_zero() for x in (F(1, 3), F(-1, 3), 1, -1))


def sign_to_cube(u1, u2, u3):
    """sign the three so every pairwise dot is -1/3; None if impossible (not a cube's diagonals)"""
    for s2 in (1, -1):
        for s3 in (1, -1):
            v2 = sm(s2, u2); v3 = sm(s3, u3)
            if (dot(u1, v2) - M13).is_zero() and (dot(u1, v3) - M13).is_zero() \
               and (dot(v2, v3) - M13).is_zero():
                return [u1, v2, v3, sm(-1, add(u1, v2, v3))]
    return None


def same_axis(u, v):
    return all((u[i] - v[i]).is_zero() for i in range(3)) or \
           all((u[i] + v[i]).is_zero() for i in range(3))


def cube_from(base, u, v):
    """the cube whose diagonals include base, u and v.

    THE CASE THAT WAS MISHANDLED: when u and v are the SAME axis, this cube shares one
    direction with BOTH its partners -- three cubes on one axis.  It then has only TWO pinned
    diagonals, and two diagonals already determine a cube ([P350]'s `tet2`).  The first version
    required three distinct ones, so all 52 such solutions failed the filter and were reported
    under 'not a cube's diagonals' -- silently, while the summary line claimed they had been
    censused."""
    ds = [base]
    for w in (u, v):
        if not any(same_axis(w, x) for x in ds):
            ds.append(w)
    if len(ds) >= 3:
        return sign_to_cube(ds[0], ds[1], ds[2]), 3
    if len(ds) == 2:
        return PAW.tet2(ds[0], ds[1]), 2
    return None, 1


def main():
    d = {1: [T3, T3, T3], 2: [T3, T3, -T3], 3: [T3, -T3, T3]}
    VALS = [K(F(1, 3)), K(F(-1, 3)), K(1), K(-1)]
    lost_total = 0
    S = {}
    for i, j in ((1, 2), (1, 3), (2, 3)):
        got = []
        for af in VALS:
            for bf in VALS:
                c, lost = candidates(d[i], d[j], af, bf)
                got += c; lost_total += lost
        S[(i, j)] = dedup(got)
    print('candidate shared directions:  s12 %d   s13 %d   s23 %d   (unrecognised: %d)'
          % (len(S[(1, 2)]), len(S[(1, 3)]), len(S[(2, 3)]), lost_total), flush=True)

    triples = []
    for a in S[(1, 2)]:
        for b in S[(1, 3)]:
            if not diag_ok(a, b):
                continue
            for c in S[(2, 3)]:
                if diag_ok(a, c) and diag_ok(b, c):
                    triples.append((a, b, c))
    print('(s12, s13, s23) satisfying every inner-product condition: %d' % len(triples),
          flush=True)

    rows = []; collapsed = 0; notcube = 0; failed = 0; identical = 0
    seen = {}
    for a, b, c in triples:
        # NOTE, and this cost a run: two of s12/s13/s23 coinciding means THREE cubes on one
        # axis, which is a legitimate compound and must be censused, not filtered.  The first
        # version skipped these 52 cases and the enumeration came back without [P334]'s K4 --
        # a count the construction guarantees, missing.  [FAILURE_MODES 44].
        if any(same_axis(x, y) for x, y in ((a, b), (a, c), (b, c))):
            collapsed += 1
        cubes = []
        bad = False
        for base, u, v in ((d[1], a, b), (d[2], a, c), (d[3], b, c)):
            ds, npin = cube_from(base, u, v)
            if ds is None:
                bad = True
                break
            cubes.append(PAW.normals(ds))
        if bad:
            notcube += 1
            continue
        # reject only if two cubes are literally the SAME cube: same three face-normal AXES.
        # An earlier version compared frozensets of |components|, which collapses distinct
        # cubes onto one key and rejected every genuine solution -- 0 censused, a count the
        # construction guarantees coming back empty ([FAILURE_MODES 44]).
        allc = [PAW.C3] + cubes

        def axkey(M):
            rows = []
            for r in M:
                v = list(r)
                for t in v:                      # sign-normalise: a normal and its negative
                    if not t.is_zero():          # bound the same pair of facets
                        if t.sign() < 0:
                            v = [-x for x in v]
                        break
                rows.append(tuple((x.a, x.b, x.c, x.d) for x in v))
            return frozenset(rows)
        if len({axkey(M) for M in allc}) < 4:
            identical += 1
            continue
        try:
            sig, _ = PAW.census(allc)               # C3 is the STANDARD cube in paw_construction
        except Exception:
            failed += 1
            continue
        EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
        t3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
        Q4 = sum(v for k, v in sig.items() if len(k) == 4)
        B = t3 + 4 * Qg
        rows.append({'EE': EE, 'SC2': SC, 'B': B, 'Q4': Q4, 'EE_plus_B': EE + B,
                     'TOTAL': 7 + EE + 2 * SC + B - Q4,
                     'sig': {str(k): v for k, v in sorted(sig.items())}})
        seen[(EE, SC, B, Q4)] = seen.get((EE, SC, B, Q4), 0) + 1

    print('   of which three cubes share one axis:               %d' % collapsed, flush=True)
    print('   rejected as coincident cubes:                     %d' % identical, flush=True)
    print('   directions that are not a cube\'s diagonals:      %d' % notcube, flush=True)
    print('   census failures (unevaluable):                    %d' % failed, flush=True)
    print('   compounds censused: %d' % len(rows), flush=True)
    print('\n   EE  SC2    B   Q4   EE+B   TOTAL    multiplicity', flush=True)
    for k in sorted(seen, reverse=True):
        EE, SC, B, Q4 = k
        print('   %3d  %3d  %3d  %3d    %3d     %3d        %d'
              % (EE, SC, B, Q4, EE + B, 7 + EE + 2 * SC + B - Q4, seen[k]), flush=True)
    if rows:
        print('\n   MAX TOTAL over every six-sharing compound: %d   (record 183)'
              % max(r['TOTAL'] for r in rows), flush=True)
        print('   MAX EE + B: %d   (the branch needs 152 to beat 183)'
              % max(r['EE_plus_B'] for r in rows), flush=True)

    out = {'what': 'exact enumeration of six-sharing 4-compounds', 'supports': 'OQ 39',
           'candidates': {str(k): len(v) for k, v in S.items()},
           'unrecognised_coordinates': lost_total,
           'inner_product_solutions': len(triples), 'three_cubes_one_axis': collapsed,
           'coincident_cubes_rejected': identical,
           'not_cube_diagonals': notcube, 'unevaluable': failed,
           'censused': len(rows),
           'spectrum': {'%d,%d,%d,%d' % k: v for k, v in sorted(seen.items())},
           'max_TOTAL': max((r['TOTAL'] for r in rows), default=None),
           'max_EE_plus_B': max((r['EE_plus_B'] for r in rows), default=None)}
    out['reproduce'] = PROV.stamp(
        parameters={'field': 'Q(sqrt3,sqrt5)', 'inner_products': ['+-1/3', '+-1']},
        note='enumeration, not search: every constraint is an inner product with four '
             'possible values, so the variety is a finite explicit list')
    json.dump(out, open(os.path.join(ROOT, 'data', 'six_sharing.json'), 'w'), indent=1)
    print('\nwrote data/six_sharing.json', flush=True)


if __name__ == '__main__':
    main()
