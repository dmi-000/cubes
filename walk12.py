#!/usr/bin/env python3
"""Stratum walk at rank 13 — the faces adjacent to the record's own stratum.

WHY HERE.  [P165] The lattice collapses at the top: 87 157 flats at rank 11,
21 894 at 12, 2 044 at 13, and exactly 1 at rank 14 -- the record's own stratum,
the point every wall contains. Records sit at high coincidence, so the strata that
matter are the CHEAP ones. Chambers (P163) cost days and by P160 cannot reach 727
at all, because chamber interiors are where coincidences have been broken. These
faces CAN, because they are where walls meet.

GEOMETRY.  A rank-12 flat is 2-dimensional (ambient 15, and the arrangement's rank
is 14 because of the deficit-1 plateau, P162). The walls NOT containing it restrict
to a rank-1 arrangement on that 2-plane, so each flat carries exactly 2 open faces
-- about 4 100 evaluations in total.

WITNESSES.  Solved inside the flat's own 2-dimensional coordinates, so the
equalities hold by construction and only strict inequalities are decided. The point
is then simplified there (P160/FAILURE_MODES 16: unsimplified witnesses were 47%
unevaluable) and mapped back to R^15.

Unevaluable faces are COUNTED, never scored. Progress and checkpoints every 100
flats, so this is readable while it runs.
"""
import json, os, subprocess, sys, time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from exactlp import feasible_strict
from witness import simplify
from dimension import q_of

ENG = os.path.join(HERE, 'cube_regions_n')
ENGW = os.path.join(HERE, 'cube_regions_q2w')
OUT = os.path.join(HERE, 'walk12_report.json')


def nullspace(rows, n):
    A = [[F(x) for x in r] for r in rows]
    piv, where, r = [], {}, 0
    for c in range(n):
        pr = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        where[c] = r; piv.append(c); r += 1
    out = []
    for fc in [c for c in range(n) if c not in where]:
        v = [F(0)] * n
        v[fc] = F(1)
        for c in piv:
            v[c] = -A[where[c]][fc]
        out.append(v)
    return out


def reduce_basis(B):
    """Lagrange-reduce a 2-dimensional RATIONAL basis. No denominator clearing.

    The witness is simplified inside the flat's own coordinates, then mapped back
    through B -- so B's height, not the witness's, sets the height the engine sees.
    Measured: evaluable faces had median basis height 3.5e4, unevaluable ones
    2.9e8, and the wide engine rejected the latter for quaternion magnitude.

    THE FIRST VERSION CLEARED DENOMINATORS FIRST and made every one of 40 test
    bases WORSE -- median 6.1e4 -> 2.4e6 -- because the LCM over 15 unrelated
    denominators compounds. That is FAILURE_MODES 16b, written four days earlier
    about this exact operation, and repeated here inside the fix for its own parent
    mode. Lagrange reduction needs an inner product and exact division, both of
    which Q provides; integers were never required.

    Only the SPAN matters, so any basis of it is as correct as any other.
    """
    if len(B) != 2:
        # Lagrange reduction as written is 2-dimensional. Measured at rank 13 it
        # left 39 of 40 bases unchanged -- the RREF nullspace basis is already
        # reduced -- so returning B untouched here loses nothing real. Stated
        # rather than silently generalised to a dimension it was not written for.
        return [[F(x) for x in b] for b in B]
    u, v = [[F(x) for x in b] for b in B]
    dot = lambda a, b: sum(x * y for x, y in zip(a, b))
    for _ in range(200):
        if dot(v, v) < dot(u, u):
            u, v = v, u
        d = dot(v, v)
        if d == 0:
            break
        q = round(dot(u, v) / d)
        if q == 0:
            break
        u = [a - q * b for a, b in zip(u, v)]
        if not any(u):
            return [[F(x) for x in b] for b in B]
    return [u, v]


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    import evalpoint as EP
    import dimension as D
    import epscount
    # WIDE eps engine (P167): the narrow one refused 20 of 20 rank-12 directions,
    # because a rank-12 flat is a 2-plane cut by 13 equations and contains no short
    # rational vector -- an instrument limit, not a bad representative.
    epscount.ENG = os.path.join(HERE, 'cube_regions_epsw')
    from epscount import count_eps
    W, nc, pt, n = EP.setup(BASE + [(7, 14, 1, -5)], 727)   # gates on 727 or exits
    q0 = D.QZERO[0]
    if count_eps(list(pt), None, 0, q0) != 727:
        raise SystemExit('eps engine gate failed at the record point')
    m = len(W)
    masks = [int(x) for x in open(os.path.join(HERE, 'flats_727_rank12.txt')) if x.strip()]
    # ORDER BY WALL MULTIPLICITY, DESCENDING (P168 Addendum 1). Within a stratum
    # the maximum is monotone in how many walls contain the flat: at rank 13 the
    # 14-18 band topped out at 679 and the 23-24 band reached 719. So the flats
    # most likely to carry a high count are evaluated FIRST, and a partial run is
    # informative rather than merely incomplete. This orders the search; it does
    # not predict a value (METHODS 6).
    masks.sort(key=lambda m: -bin(m).count('1'))
    if limit:
        masks = masks[:limit]
    print('rank-12 flats: %d | ambient %d | walls %d | adapter gated at 727'
          % (len(masks), nc, m), flush=True)

    # INFINITESIMAL, NOT FINITE.  The walls are gradients of the conditions tight
    # at the record, so the arrangement is the TANGENT structure: a face is a
    # direction out of pt, not a region at finite distance. Evaluating at pt + y
    # crosses conditions the linearisation does not model -- measured directly,
    # the count varied across three points of every one of 20 faces, and settled
    # only as the displacement shrank. METHODS 14: the fix is arithmetic, not a
    # smaller number. `count_eps` returns the eps -> 0 limit exactly, and its gate
    # includes the control that scaling a direction by 97 cannot change the count.
    counts, unev, nface = {}, 0, 0
    faces_out = open(os.path.join(HERE, 'walk12_faces.jsonl'), 'w')
    t0 = time.time()
    for idx, mask in enumerate(masks):
        inS = [j for j in range(m) if mask >> j & 1]
        B = nullspace([W[j] for j in inS], nc)
        if len(B) != 3:
            unev += 1
            continue
        B = reduce_basis(B)
        out = [j for j in range(m) if not (mask >> j & 1)]
        rows2 = [r for r in ([sum(F(W[j][t]) * b[t] for t in range(nc)) for b in B]
                             for j in out) if any(r)]
        frontier = [[]]
        for r in rows2:
            nxt = []
            for ext in frontier:
                sub = [[s * rows2[i][k] for k in range(3)] for i, s in enumerate(ext)]
                for sgn in (1, -1):
                    if feasible_strict(sub + [[sgn * r[0], sgn * r[1], sgn * r[2]]], 3) is not None:
                        nxt.append(ext + [sgn])
            frontier = nxt
        for ext in frontier:
            sub = [[s * rows2[i][k] for k in range(3)] for i, s in enumerate(ext)]
            y2 = feasible_strict(sub, 3)
            if y2 is None:
                unev += 1
                continue
            y2 = simplify(sub, list(y2), 3)
            y = [sum(F(y2[k]) * B[k][t] for k in range(3)) for t in range(nc)]
            c = count_eps(list(pt), y, 0, q0)
            nface += 1
            # PER-FACE RECORD, not just a histogram. The first run recorded counts
            # and discarded which flat produced them, so "which faces carry 715 and
            # 719?" needed the whole 42-minute walk again. Same mistake as the flat
            # census (P165). 4 088 lines is nothing; a re-run is not.
            faces_out.write(json.dumps({'mask': mask, 'ext': ext, 'count': c}) + '\n')
            if c is None:
                unev += 1
            else:
                counts[c] = counts.get(c, 0) + 1
        if (idx + 1) % 100 == 0:
            mx = max(counts) if counts else None
            print('   %d/%d flats, %d faces, max=%s, unevaluable %d (%.0fs)'
                  % (idx + 1, len(masks), nface, mx, unev, time.time() - t0), flush=True)
            json.dump({'flats_done': idx + 1, 'faces': nface, 'counts': counts,
                       'unevaluable': unev, 'secs': time.time() - t0},
                      open(OUT, 'w'), indent=1)
    faces_out.close()
    mx = max(counts) if counts else None
    print('\nrank-12 walk: %d faces, MAX = %s (record 727), unevaluable %d, %.0fs'
          % (nface, mx, unev, time.time() - t0), flush=True)
    print('top counts: %s' % sorted(counts)[-10:], flush=True)
    json.dump({'flats_done': len(masks), 'faces': nface, 'counts': counts,
               'unevaluable': unev, 'secs': time.time() - t0, 'complete': True},
              open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
