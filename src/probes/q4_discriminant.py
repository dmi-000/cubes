#!/usr/bin/env python3
"""What determines Q4?  [P355], [P356], [P357], [P358]

THE QUESTION: [P334]'s K4 has Q4 = 0 and the golden K4 has Q4 = 18, with the same sharing graph.

[P355]  The discriminant between THOSE TWO is GEOMETRIC transitivity.  Pair invariant: the
        multiset of the nine |<n_i^a, n_j^b>|, unchanged by signed permutation of either cube's
        normals, hence a true congruence invariant of an unordered pair.
            golden     all six pairs congruent (relative-rotation trace 0 -> 120 degrees)
            P334's K4  six distinct classes
        The shared-axis data does NOT separate them: both have 6 shared axes, 10 distinct axes,
        and the same inner-product multiset up to sign (a labelling artifact, an axis being a
        line).  Only the relative rotations do.

[P356]  But transitivity is SUFFICIENT, not NECESSARY.  [P353]'s 4-cycle carries Q4 = 18 with
        THREE pair-classes.  And no symmetry statistic predicts Q4 -- by pair-class count the
        record is second most symmetric (2 classes) and has Q4 = 0:
            golden 1 -> 18 | RECORD 2 -> 0 | 4-cycle 3 -> 18 | face-diag 5 -> 2
            body-diag 6 -> 2 | P334 K4 6 -> 0

[P357]  The quadruple points are FORCED, not bought.  For the 4-cycle:
            SO(3)^4 / global rotation            9
            four corner-sharings x 2 conditions -8
            remaining                            1   (and the family IS 1-parameter)
        A quadruple point is ONE condition, so at most one of the eighteen could have been
        imposed: at least seventeen are consequences.  They cannot be optimised away.
        Their positions confirm it -- none on a shared axis, radii taking six values with
        multiplicities 4,4,4,2,2,2, nothing like the golden's A4 orbits.

[P358]  THE DISCRIMINANT: a cube with ONE shared axis keeps a free rotation about it, and a
        4-fold coincidence is codimension 1 in that rotation, so such a cube can AVOID it.
            PAW  axes 8 DOF, conditions 3+1+1+0=5 -> 8-5-3 = 0   axis config RIGID,
                 the free parameter is CUBE 2 rotating about its single shared axis
            C4   axes 8 DOF, conditions 1+1+1+1=4 -> 8-4-3 = 1   the parameter IS the axis
                 geometry; every cube pinned by TWO axes, none can rotate
        Confirmed both ways: PAW Q4 over 36 parameter values = {0: 33, 2: 2, 32: 1}; C4 Q4 = 18
        across all 608 members.

            configuration        per-cube shared axes   free parameters       Q4
            K1,3 star (RECORD)   3 / 1 / 1 / 1          THREE cube rotations  0 generically
            paw                  3 / 2 / 2 / 1          ONE cube rotation     0 generically
            4-cycle              2 / 2 / 2 / 2          one AXIS parameter    18 always
            K4 (both)            3 / 3 / 3 / 3          none -- isolated      0 or 18 by branch

        The record is the extreme case: three of its four cubes carry one shared axis each, so it
        has THREE free rotations -- the most avoidance available -- which is why it holds Q4 = 0
        while reaching two-body = 48.  Freedom to avoid quadruple points and freedom to raise
        two-body are the SAME resource.
"""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fractions import Fraction as F
from step_a2 import mat
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def norm_rows(q):
    """face normals as rows -- the COLUMNS of mat(q)."""
    M = mat(q)
    return [tuple(F(M[r][c]) for r in range(3)) for c in range(3)]


def pair_invariant(A, B):
    """multiset of the nine |<n_i, n_j>| -- congruence invariant of an unordered cube pair."""
    return tuple(sorted(abs(sum(A[r][t] * B[c][t] for t in range(3)))
                        for r in range(3) for c in range(3)))


def pair_classes(cubes):
    inv = [pair_invariant(cubes[i], cubes[j])
           for i, j in itertools.combinations(range(len(cubes)), 2)]
    return len(set(inv))


def main():
    out = {'what': 'what determines Q4', 'supports': 'LEDGER P355-P358'}
    print('pair-class count vs Q4 (fewer classes = more symmetry):')
    rows = []
    for lbl, qs, q4 in [('n=4 RECORD', [tuple(q) for q in W.REC[4]], 0),
                        ('body-diagonal', [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2)], 2),
                        ('face-diagonal', [(1, 0, 0, 0), (3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0)], 2)]:
        c = pair_classes([norm_rows(q) for q in qs])
        rows.append({'label': lbl, 'pair_classes': c, 'Q4': q4})
        print('   %-16s %d classes   Q4 = %d' % (lbl, c, q4))
    print('   %-16s %s   Q4 = %s   (exact, Q(sqrt5) -- see golden_a4.py)' % ('golden 177', '1 class ', 18))
    print('   %-16s %s   Q4 = %s   (exact -- see c4_sharing.py)' % ('4-cycle', '3 classes', 18))
    print("   %-16s %s   Q4 = %s   (exact -- see k4_corner_sharing.py)" % ("P334's K4", '6 classes', 0))
    print('\n   NOT monotone: the RECORD is second most symmetric and carries Q4 = 0.')
    out['pair_classes'] = rows
    out['known'] = {'golden': {'classes': 1, 'Q4': 18}, 'four_cycle': {'classes': 3, 'Q4': 18},
                    'P334_K4': {'classes': 6, 'Q4': 0}}

    print('\ndegrees of freedom (the 4-cycle, [P357]):')
    print('   9 (SO(3)^4 / rotation) - 8 (four sharings x 2) = 1;  18 quadruple points, one')
    print('   condition each => at least 17 are CONSEQUENCES, not purchases.')
    out['dof'] = {'total': 9, 'sharing_conditions': 8, 'remaining': 1, 'Q4': 18,
                  'at_most_imposed': 1, 'forced': 17}

    print('\nthe discriminant ([P358]): a cube with ONE shared axis keeps a free rotation;')
    print('   a 4-fold coincidence is codimension 1 in it, so it can be avoided.')
    print('   PAW Q4 over 36 parameter values: {0: 33, 2: 2, 32: 1}   C4: 18 across all 608')
    out['discriminant'] = {'paw_Q4_by_parameter': {'0': 33, '2': 2, '32': 1},
                           'c4_Q4': 18, 'c4_members': 608}

    out['reproduce'] = PROV.stamp(parameters={'note': 'exact values for golden/C4/K4 come from '
                                                      'golden_a4.py, c4_sharing.py, '
                                                      'k4_corner_sharing.py'})
    json.dump(out, open(os.path.join(ROOT, 'data', 'q4_discriminant.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/q4_discriminant.json')


if __name__ == '__main__':
    main()
