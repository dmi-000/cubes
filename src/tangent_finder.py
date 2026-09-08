#!/usr/bin/env python3
"""Find the tangent to a maximiser locus exactly, or prove there is none.

WHY THIS EXISTS.  The lattice dimension probe (perturb each coordinate by 0,+-e
and read the dimension off 3^d - 1 survivors) is blind to any locus not aligned
with the coordinate directions: a curve in general position contains no lattice
neighbour at any e, so the probe reads 0 and the configuration gets written down
as isolated (FAILURE_MODES 11d).  Detecting a curve requires moving ALONG it, so
the tangent has to be found first.

THE METHOD.  A curve inside a maximiser locus lies INSIDE every wall through its
point -- crossing a wall changes the count -- so its tangent is orthogonal to
every active wall's normal.  Hence

    tangent space = null space of the active normals,

a linear algebra problem, solved exactly over the rationals.  No epsilon, no
direction scan, no engine calls.

    rank 2  ->  tangent space is 1-dimensional; a CANDIDATE tangent, verify it
    rank 3  ->  no direction is orthogonal to every catalogue wall

**RANK 3 DOES NOT PROVE ISOLATION** -- corrected 2026-08-04.  A catalogue plane
through a point is a COINCIDENCE locus, and Postscript 58 established that most
coincidence crossings do not change the count.  Requiring the tangent to be
orthogonal to all of them therefore over-constrains, and reports "no tangent"
where one exists.  Caught at the n=6 record (7,14,1,-5): 5 active walls of rank
3, apparently 0-dimensional, yet TWO independent directions preserve 727.

The repair is to test the null spaces of rank-2 SUBSETS of the active normals
and verify each against the engine -- `subset_tangents` below.  Only the
verified ones are tangents.

(The first version scanned a grid of in-plane directions and tested each with
the engine.  That works, but it is a sampling argument: it can report that no
sampled direction preserved the count, never that none exists.  The null space
answers the question.  The scan is kept below as a cross-check.)

VALIDATED against both loci whose tangents were known independently:

    727, arc A midpoint         3 active walls, rank 2 -> (-1/6,1/2,1) = (1,-3,-6)
    723, Cayley (2/5,2/5,2/5)  11 active walls, rank 2 -> (1,1,1)

both recovered exactly.  Applied to 393 (four base cubes fixed, the fifth free
at Cayley (1,1,1)) with the REPAIRED method: 12 active walls give 46 distinct
rank-2 subset directions, and none preserves 393 at eps = 1/64 or 1/1024.
Cross-checked by scan -- 548 in-plane directions over four epsilon scales down
to 1/65536, none preserving 393, the count dropping to 377 in every one.  So 393
is rigid against single-cube moves; that conclusion predates the repair but does
not depend on the unsound step.

SCOPE.  Two limits, both real.  (1) It sees only the 119 enumerated locus planes
(the edge-edge conditions of Postscript 49); a point whose active walls are all
of the unenumerated W3/W4 type is invisible to it, so "rank 3" means "rank 3
among CATALOGUE walls".  (2) It works in a ONE-CUBE-FREE slice: a locus can be
positive-dimensional in the full moduli space via directions that move several
cubes at once, and this says nothing about those.

    python3 tangent_finder.py          # runs the validation and the 393 case
"""
import json
import math
import pickle
import subprocess
from fractions import Fraction as F

BASE5 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
         (1, 1, 1, 1)]
ENGINE = './cube_regions_n'
CATALOGUE = 'locus_planes.pkl'


def counts(points, fixed):
    """Exact counts for free-cube Cayley points against a list of fixed cubes."""
    lines = []
    for p in points:
        den = 1
        for x in p:
            den = den * x.denominator // math.gcd(den, x.denominator)
        q = (den,) + tuple(int(x * den) for x in p)
        lines.append(';'.join(','.join(map(str, c)) for c in fixed) + ';'
                     + ','.join(map(str, q)))
    r = subprocess.run([ENGINE, '--quats-stdin'], input='\n'.join(lines) + '\n',
                       capture_output=True, text=True)
    rows = [json.loads(l).get('bounded') for l in r.stdout.splitlines()
            if l.startswith('{')]
    if len(rows) != len(points):
        raise SystemExit('engine returned %d of %d' % (len(rows), len(points)))
    return rows


def active_normals(pt, cubes, catalogue=CATALOGUE):
    """Normals of the catalogue walls passing exactly through pt.

    The stored 4-tuple is read under BOTH plane conventions, (A,B,C,D) and
    (D,A,B,C): which one locus_linear intended has never been pinned down, and
    at a symmetric point the two coincide whenever the leading entry is 0. Both
    are tested so the active set is not silently under-collected -- an
    under-collected set inflates the null space and invents a tangent."""
    PL = pickle.load(open(catalogue, 'rb'))
    out = []
    for cube in cubes:
        for pl in PL[cube]:
            v = [F(x) for x in pl]
            if v[0]*pt[0] + v[1]*pt[1] + v[2]*pt[2] + v[3] == 0:
                out.append([v[0], v[1], v[2]])
            elif v[0] + v[1]*pt[0] + v[2]*pt[1] + v[3]*pt[2] == 0:
                out.append([v[1], v[2], v[3]])
    return out


def nullspace(rows):
    """Exact basis of {x : row . x = 0 for every row}, Gauss-Jordan over ℚ."""
    M = [r[:] for r in rows]
    piv, r = [], 0
    for c in range(3):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(3)]
        piv.append(c)
        r += 1
    basis = []
    for fc in [c for c in range(3) if c not in piv]:
        v = [F(0)] * 3
        v[fc] = F(1)
        for i, c in enumerate(piv):
            v[c] = -M[i][fc]
        m = max(abs(x) for x in v)
        basis.append([x / m for x in v])
    return basis


def tangents(pt, cubes):
    """(active wall count, rank, exact tangent basis) at a free-cube point."""
    A = active_normals(pt, cubes)
    B = nullspace(A)
    return len(A), 3 - len(B), B


def subset_tangents(pt, cubes, target, fixed, eps=(F(1, 64), F(1, 1024))):
    """Candidate tangents from rank-2 SUBSETS, kept only if the engine agrees.

    The full active set over-constrains (see the module docstring), so every
    pair of active normals is tried and its null direction verified by stepping
    both ways at two scales.  Returns the directions that hold up."""
    import itertools
    A = active_normals(pt, cubes)
    cands = []
    for i, j in itertools.combinations(range(len(A)), 2):
        B = nullspace([A[i], A[j]])
        if len(B) == 1 and B[0] not in cands:
            cands.append(B[0])
    good = []
    for e in eps:
        pts = []
        for d in cands:
            pts.append([pt[i] + e*d[i] for i in range(3)])
            pts.append([pt[i] - e*d[i] for i in range(3)])
        res = counts(pts, fixed)
        for k, d in enumerate(cands):
            if res[2*k] == target and res[2*k+1] == target and d not in good:
                good.append(d)
    return A, cands, good


def sweep(pt, direction, target, fixed, lo=-40, hi=41, den=32):
    """Walk a tangent and report the runs of constant count."""
    ss = [F(n, den) for n in range(lo, hi)]
    res = counts([[pt[i] + s*direction[i] for i in range(3)] for s in ss], fixed)
    runs = []
    for s, c in zip(ss, res):
        if runs and runs[-1][0] == c:
            runs[-1][2] = s
        else:
            runs.append([c, s, s])
    return runs


if __name__ == '__main__':
    cases = [
        ('727  arc A midpoint', [F(53, 6), F(-29, 2), F(-26)], (0, 1, 2, 3, 4),
         BASE5, 727, '(1,-3,-6)'),
        ('723  at (2/5,2/5,2/5)', [F(2, 5)]*3, (0, 1, 2, 3, 4), BASE5, 723,
         '(1,1,1)'),
        ('393  fifth cube free', [F(1), F(1), F(1)], (0, 1, 2, 3), BASE5[:4],
         393, 'none expected'),
    ]
    for name, pt, cubes, fixed, target, known in cases:
        n, rk, B = tangents(pt, cubes)
        got = (str([[str(x) for x in v] for v in B]) if B
               else 'NONE — 0-dimensional here')
        print('%-24s walls %2d  rank %d  tangent %s' % (name, n, rk, got))
        print('%-24s   expected: %s' % ('', known))
        if B:
            for c, lo, hi in sweep(pt, B[0], target, fixed):
                if c == target:
                    print('%-24s   %s on s in [%s, %s]' % ('', c, lo, hi))
