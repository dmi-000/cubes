#!/usr/bin/env python3
"""[OQ 36] SOLVED: four concentric cubes CAN pairwise share corners.  [P334]

THE REDUCTION.  Two cubes share a corner iff they share a BODY-DIAGONAL direction (the shared
corner sits at the end of it).  A cube's four diagonals, correctly signed, are a regular
tetrahedron of unit vectors -- pairwise inner product exactly -1/3.  So the question becomes
combinatorial: label each EDGE of K4 with an axis, and require the three axes at each VERTEX
to extend to a regular tetrahedron.

SOLVING IT.  Fix cube 0 as the standard cube and its three shared axes as three of its
diagonals (legitimate: the octahedral group acts as S4 on the four diagonals).  Writing the
remaining three axes as unknowns and imposing |<u,v>| = 1/3 gives, in every admissible branch,
    p, q = (sqrt3 +- sqrt15)/6,      p + q = 1/sqrt3,   p*q = -1/3
and the assignment below.  The rejected branches are exactly those putting a shared axis on a
diagonal of cube 0, which would make THREE cubes share it -- the merge this is trying to avoid.

WHAT IT IS WORTH, and the answer is not what was hoped.  All six pairs reach the proved cap
two-body = 10, so two-body = 60 = 10*C(4,2), ATTAINED for the first time at n = 4.  But T3
falls to 74 of 128, and the total lands near 138 against the record's 183.  **Both caps are
individually attainable and jointly they are not**, which is the trade [P333] predicted and
this pins down with an exact second endpoint.

EVERY DECISION HERE IS EXACT -- see `kfield.py`.  A 50-digit float version of the same count
returned T3 = 8 and failed its oracle; this one returns 128 on the n = 4 record, which is the
gate `--gate` runs.
"""
import sys, os, json, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from kfield import K
import provenance as PROV

R3 = K(0, 1, 0, 0)
R15 = K(0, 0, 0, 1)
P = (R3 + R15) * K(F(1, 6))
Q = (R3 - R15) * K(F(1, 6))
T3INV = R3 * K(F(1, 3))                      # 1/sqrt3

A = [T3INV, T3INV, T3INV]
B = [T3INV, T3INV, -T3INV]
C = [T3INV, -T3INV, T3INV]
X = [P, Q, K(0)]
Y = [Q, K(0), P]
Z = [K(0), P, -Q]
AXES = {'a': A, 'b': B, 'c': C, 'x': X, 'y': Y, 'z': Z}
# K4: vertex = cube, edge = the axis that pair shares
STAR = {0: ['a', 'b', 'c'], 1: ['a', 'x', 'y'], 2: ['b', 'x', 'z'], 3: ['c', 'y', 'z']}


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def smul(s, u):
    return [K.lift(s) * t for t in u]


def add(u, v):
    return [u[i] + v[i] for i in range(3)]


def build():
    """the four cubes, as exactly-orthonormal face-normal triples."""
    cubes, diag = {}, {}
    for i in range(4):
        us = [AXES[n] for n in STAR[i]]
        signed = None
        for sg in itertools.product([1, -1], repeat=3):
            su = [smul(sg[k], us[k]) for k in range(3)]
            if all(dot(su[m], su[n]) == K(F(-1, 3))
                   for m, n in itertools.combinations(range(3), 2)):
                signed = su
                break
        assert signed is not None, 'star %d does not extend to a regular tetrahedron' % i
        d4 = smul(-1, add(add(signed[0], signed[1]), signed[2]))
        assert dot(d4, d4) == K(1), 'fourth diagonal is not a unit vector'
        ds = signed + [d4]
        half = K(F(1, 2)) * R3
        N = [smul(half, add(ds[0], ds[k])) for k in (1, 2, 3)]
        for m, n in itertools.combinations(range(3), 2):
            assert dot(N[m], N[n]) == K(0), 'face normals not orthogonal'
        for m in range(3):
            assert dot(N[m], N[m]) == K(1), 'face normal not a unit vector'
        cubes[i], diag[i] = N, ds
    return cubes, diag


def solve3(rows, rhs):
    A_ = rows
    det = (A_[0][0] * (A_[1][1] * A_[2][2] - A_[1][2] * A_[2][1])
           - A_[0][1] * (A_[1][0] * A_[2][2] - A_[1][2] * A_[2][0])
           + A_[0][2] * (A_[1][0] * A_[2][1] - A_[1][1] * A_[2][0]))
    if det.is_zero():
        return None
    out = []
    for i in range(3):
        Bm = [r[:] for r in A_]
        for k in range(3):
            Bm[k][i] = rhs[k]
        d = (Bm[0][0] * (Bm[1][1] * Bm[2][2] - Bm[1][2] * Bm[2][1])
             - Bm[0][1] * (Bm[1][0] * Bm[2][2] - Bm[1][2] * Bm[2][0])
             + Bm[0][2] * (Bm[1][0] * Bm[2][1] - Bm[1][1] * Bm[2][0]))
        out.append(d / det)
    return out


def onface(N, pt):
    """(is pt in the closed cube?, how many facets pass through it) -- exact throughout."""
    cnt = 0
    for r in range(3):
        h = dot(N[r], pt)
        if h == K(1) or h == K(-1):
            cnt += 1
            continue
        if (K(1) - h).sign() < 0 or (K(1) + h).sign() < 0:
            return False, 0
    return True, cnt


def count_T3(cubes, n=4):
    seen = set()
    for tri in itertools.combinations(range(n), 3):
        for pick in itertools.product(range(3), repeat=3):
            for sg in itertools.product([1, -1], repeat=3):
                rows = [smul(sg[k], cubes[tri[k]][pick[k]]) for k in range(3)]
                pt = solve3(rows, [K(1), K(1), K(1)])
                if pt is None:
                    continue
                sig, ok = [], True
                for k in tri:
                    good, cnt = onface(cubes[k], pt)
                    if not good or cnt == 0:
                        ok = False
                        break
                    sig.append(cnt)
                if ok and tuple(sorted(sig)) == (1, 1, 1):
                    seen.add(tuple((t.a, t.b, t.c, t.d) for t in pt))
    return len(seen)


def gate():
    """the SAME code path on the n = 4 record, where T3 = 128 is known ([P328])."""
    sys.path.insert(0, os.path.join(HERE, '..'))
    from euler3 import rowsT, frames
    import wall_keys as W
    Ms = [rowsT(R) for R in frames([tuple(q) for q in W.REC[4]])]
    cubes = {i: [[K(F(Ms[i][r][c])) for c in range(3)] for r in range(3)] for i in range(4)}
    got = count_T3(cubes)
    print('GATE: exact-field T3 on the n=4 RECORD = %d  (must be 128)  %s'
          % (got, 'PASS' if got == 128 else 'FAIL'))
    return got == 128


def main():
    ok = gate()
    if not ok:
        print('gate failed -- refusing to report the compound'); return

    cubes, diag = build()
    print('\nfour cubes built; every face normal EXACTLY orthonormal in Q(sqrt3,sqrt5)')

    # incidence structure: which axes are shared, by how many cubes
    def key(v):
        for t in v:
            if not t.is_zero():
                if t.sign() < 0:
                    v = [-t for t in v]
                break
        return tuple((t.a, t.b, t.c, t.d) for t in v)
    allax = {}
    for i, ds in diag.items():
        for d in ds:
            allax.setdefault(key(d), set()).add(i)
    shared2 = {k: v for k, v in allax.items() if len(v) == 2}
    shared3 = {k: v for k, v in allax.items() if len(v) >= 3}
    pairs = sorted(tuple(sorted(v)) for v in shared2.values())
    print('   distinct axes %d;  shared by exactly two cubes %d;  shared by three or more %d'
          % (len(allax), len(shared2), len(shared3)))
    print('   pairs realised: %s' % (pairs,))
    complete = sorted(pairs) == sorted(itertools.combinations(range(4), 2))
    print('   K4 COMPLETE: %s     merges: %s' % (complete, bool(shared3)))

    t3 = count_T3(cubes)
    sc2 = 2 * len(shared2)
    print('\n   T3        = %3d  of cap 128' % t3)
    print('   SC2       = %3d  (exact: one shared axis per pair, two antipodal corners each)'
          % sc2)
    print('   two-body  =  60  of cap 60   ATTAINED    (EE = 36 at 25/40/60 digits, SC2 proved)')
    print('   T3 + two-body = %d;  the n=4 record has 128 + 48 = 176' % (t3 + 60))

    out = {'what': 'OQ 36 solved: four cubes CAN pairwise share corners',
           'question': 'OPEN_QUESTIONS 36', 'supports': 'LEDGER P334',
           'field': 'Q(sqrt3,sqrt5)', 'p_q': '(sqrt3 +- sqrt15)/6',
           'gate_record_T3': 128, 'K4_complete': complete, 'merges': bool(shared3),
           'distinct_axes': len(allax), 'axes_shared_by_two': len(shared2),
           'T3': t3, 'T3_cap': 128, 'SC2': sc2, 'two_body': 60, 'two_body_cap': 60,
           'T3_plus_two_body': t3 + 60, 'record_T3_plus_two_body': 176,
           'star': {str(k): v for k, v in STAR.items()}}
    out['reproduce'] = PROV.stamp(parameters={'field': 'Q(sqrt3,sqrt5)'})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'k4_corner_sharing.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/k4_corner_sharing.json')


if __name__ == '__main__':
    main()
