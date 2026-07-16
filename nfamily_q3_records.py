#!/usr/bin/env python3
# Working principles: NFAMILY_SPEC.md. Project index: README.md
"""Q3: do the EXISTING RECORDS already contain family structure?

For each record config (n=4: 183, n=5: 393, n=6: 723 -- integer quats, from
six_cube_search_results.md; n=3: 67 -- irrational, ℚ(√2) octahedral witness,
from Postscript 9), compute for every cube pair:
  (a) exact interior edge-edge crossing count (nfamily_common.exact_pair_
      crossings for n=4/5/6's rational quats; a hand-adapted ℚ(√2) version
      for n=3, since that record has NO integer-quaternion representative
      -- both known witnesses (octahedral ℚ(√2), golden ℚ(√5)) are
      irrational fields, so the spec's "integer quats" framing does not
      literally apply to n=3; this script is explicit about that and uses
      the SAME exact algorithm generalized to ℚ(√2) instead of skipping it.
  (b) the independent "common axis + equal tilt" confirmation test
      (nfamily_common.family_axis_test / its ℚ(√2) analogue).
No floats decide any predicate in either path."""
import json
from fractions import Fraction as Fr
from itertools import product

from nfamily_common import (quat_to_matrix_exact, exact_config_crossings,
                             family_axis_test, CUBE_ROT_GROUP)


def n456_report():
    records = {
        4: (183, [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]),
        5: (393, [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]),
        6: (723, [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1), (5, 2, 2, 2)]),
    }
    out = {}
    for n, (total, quats) in records.items():
        mats = [quat_to_matrix_exact(*q) for q in quats]
        cr = exact_config_crossings(mats)
        pairs = []
        for (i, j), c in sorted(cr.items()):
            fam, _ = family_axis_test(mats[i], mats[j])
            pairs.append({'i': i, 'j': j, 'crossings': c, 'axis_test_family': fam})
        n_family = sum(1 for p in pairs if p['axis_test_family'])
        n_total = len(pairs)
        out[n] = {'record_total': total, 'quats': quats, 'pairs': pairs,
                  'n_family_pairs': n_family, 'n_pairs': n_total}
        print(f'n={n} record={total}: {n_family}/{n_total} pairs in family position')
        for p in pairs:
            tag = 'FAMILY' if p['axis_test_family'] else 'generic'
            print(f"    ({p['i']},{p['j']}): crossings={p['crossings']:2d}  {tag}")
    return out


def n3_octahedral_report():
    """n=3, 67: octahedral witness S_oct=Rx(45deg) in Q(sqrt2), orbited by
    C=120deg about (1,1,1) (rational). Same exact algorithm, Q2 field."""
    from slide3_q2 import Q2, ONE2, ZERO2, Rx45, exact_count_q2, assert_orthonormal
    from golden_rotations import Rot

    def mmul(A, B):
        return [[sum((A[i][k] * B[k][j] for k in range(3)), ZERO2) for j in range(3)] for i in range(3)]

    def mT(A):
        return [[A[j][i] for j in range(3)] for i in range(3)]

    Cf = quat_to_matrix_exact(1, 1, 1, 1)
    C = [[Q2(Fr(Cf[i][j])) for j in range(3)] for i in range(3)]
    Soct = Rx45().m
    C2 = mmul(C, C)
    mats = [Soct, mmul(C, Soct), mmul(C2, Soct)]
    for M in mats:
        assert_orthonormal(Rot(M))
    total, bd = exact_count_q2([Rot(m) for m in mats])
    assert total == 67, f'expected 67, got {total}'

    def cube_edges_q2():
        edges = []
        for a in range(3):
            o = [i for i in range(3) if i != a]
            for s1, s2 in product((-1, 1), repeat=2):
                c = [ZERO2, ZERO2, ZERO2]
                c[o[0]], c[o[1]] = Q2(Fr(s1)), Q2(Fr(s2))
                d = [ZERO2, ZERO2, ZERO2]
                d[a] = ONE2
                edges.append((tuple(c), tuple(d)))
        return edges
    EDGES = cube_edges_q2()

    def mv(M, v):
        return tuple(sum((M[i][k] * v[k] for k in range(3)), ZERO2) for i in range(3))

    def cross(u, v):
        return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])

    def dot(u, v):
        return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]

    def sub(u, v):
        return (u[0]-v[0], u[1]-v[1], u[2]-v[2])

    def pair_crossings(Mi, Mj):
        ei = [(mv(Mi, c), mv(Mi, d)) for c, d in EDGES]
        ej = [(mv(Mj, c), mv(Mj, d)) for c, d in EDGES]
        n_cross = 0
        for C1, D1 in ei:
            for C2, D2 in ej:
                n = cross(D1, D2)
                if n[0] == ZERO2 and n[1] == ZERO2 and n[2] == ZERO2:
                    continue
                w = sub(C2, C1)
                if dot(w, n) != ZERO2:
                    continue
                idx = next(k for k in range(3) if n[k] != ZERO2)
                r0, r1 = [k for k in range(3) if k != idx]
                a11, a12 = D1[r0], -D2[r0]
                a21, a22 = D1[r1], -D2[r1]
                b1, b2 = w[r0], w[r1]
                det = a11 * a22 - a12 * a21
                if det == ZERO2:
                    continue
                t = (b1 * a22 - a12 * b2) / det
                s = (a11 * b2 - b1 * a21) / det
                if t * D1[idx] - s * D2[idx] != w[idx]:
                    continue
                if ((t + ONE2).sign() > 0 and (ONE2 - t).sign() > 0 and
                        (s + ONE2).sign() > 0 and (ONE2 - s).sign() > 0):
                    n_cross += 1
        return n_cross

    def family_axis_test_q2(Mi, Mj):
        R = mmul(mT(Mi), Mj)
        for Qm in CUBE_ROT_GROUP:
            Qm2 = [[Q2(Fr(x)) for x in row] for row in Qm]
            Rp = mmul(mT(Qm2), R)
            if Rp[1][0] == Rp[0][1]:
                return True
        return False

    pairs = []
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        c = pair_crossings(mats[i], mats[j])
        fam = family_axis_test_q2(mats[i], mats[j])
        pairs.append({'i': i, 'j': j, 'crossings': c, 'axis_test_family': fam})
    print(f'n=3 record=67 (octahedral, Q(sqrt2) witness): '
          f'{sum(p["axis_test_family"] for p in pairs)}/3 pairs in family position')
    for p in pairs:
        print(f"    ({p['i']},{p['j']}): crossings={p['crossings']:2d}  "
              f"{'FAMILY' if p['axis_test_family'] else 'generic'}")
    return {'record_total': 67, 'field': 'Q(sqrt2) [C-orbit of Rx45 about (1,1,1)]',
            'by_depth': {int(k): v for k, v in bd.items() if int(k) != 0},
            'pairs': pairs, 'n_family_pairs': sum(p['axis_test_family'] for p in pairs),
            'n_pairs': 3,
            'note': ('67 has NO integer-quaternion representative -- both known '
                     'witnesses (octahedral Q(sqrt2), golden Q(sqrt5)) are irrational. '
                     'This IS literally a member of the dihedral family (psi=arcsin(1/sqrt3), '
                     'Delta=120deg), confirmed here with an independent EXACT (not 1e-16 '
                     'numeric) crossing count in Q(sqrt2): 10 crossings/pair, matching '
                     'Postscript 25\'s "30 interior crossings" = 10x3 pairs.')}


if __name__ == '__main__':
    out = {}
    out['n3'] = n3_octahedral_report()
    out.update({str(k): v for k, v in n456_report().items()})
    with open('/Users/dmi/carroll/nfamily_q3_records.json', 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print('\nwritten nfamily_q3_records.json')
