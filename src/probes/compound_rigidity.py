#!/usr/bin/env python3
"""[OQ 39] How many `EE` contacts can 9 parameters support?  Compound-level Jacobian rank.

[P376] measured the codimension of each `EE` stratum exactly: `EE = 4` is codimension 1 and
`EE = 6, 8, 10` are all codimension **2** -- curves in `SO(3)`.  A 4-compound has 9 parameters
(three cube rotations, the fourth fixed as gauge) and six pairs, so the naive budget is

    sum over pairs of codim(EE_i)  <=  9

which caps `EE` at `3*10 + 3*4 = 42` -- **exactly the largest `EE` this session has produced.**

But the n = 4 RECORD has all six pairs at `EE = 6`, six codimension-2 conditions, 12 > 9.  It
exists, so its conditions must be DEPENDENT.  The naive budget is therefore not a bound, and the
question becomes how much dependency a configuration can arrange.

THIS MEASURES IT DIRECTLY.  For a compound, collect every active edge-edge contact across all
six pairs as one polynomial system in the 9 parameters, and compute the exact rank of its
Jacobian.  `rank` is the true number of independent conditions; `9 - rank` is the dimension of
the family the compound sits in.  Exact rational arithmetic throughout.
"""
import sys, os, json, itertools, collections
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_determinantal as D
import ee_bound_refute as EB
from euler3 import rowsT, frames
from c_level import shares_plane
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))

NAMED = {
    'n=4 RECORD': [tuple(q) for q in WK.REC[4]],
    'refuter [P373] EE=38': [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, -3, 2), (-4, -2, -5, -6)],
    'EE=42 climb': [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, 3, 2), (-4, 0, -5, -6)],
    'refuter-region best (173)': [(1, 0, 0, 0), (0, 2, -3, -2), (1, -5, -2, 2), (-2, -8, 0, 9)],
    'face-diagonal EE=40': [(1, 0, 0, 0), (3, 2, 2, 0), (5, 3, 3, 0), (7, 2, 2, 0)],
}



def in_range_labels(qi, qj):
    """labels (a,b,s,t,p,r) whose two EDGE SEGMENTS actually meet, in exact arithmetic.

    Mirrors `ee_determinantal.ee_exact`: the crossing must lie on both closed segments and be a
    (2,2) vertex -- on exactly two facets of each cube, so corners are excluded ([P329])."""
    Ms = [rowsT(R) for R in frames([qi, qj])]
    out = set()
    for a in range(3):
        for s, t in itertools.product((-1, 1), repeat=2):
            c1 = [F(0), F(0), F(0)]; c1[(a + 1) % 3] = F(s); c1[(a + 2) % 3] = F(t)
            A1 = [c1[k] - (F(1) if k == a else F(0)) for k in range(3)]
            B1 = [c1[k] + (F(1) if k == a else F(0)) for k in range(3)]
            P1 = [[sum(Ms[0][rr][k] * v[k] for k in range(3)) for rr in range(3)]
                  for v in (A1, B1)]
            # endpoints in world coordinates: cube i's frame columns
            E1 = [_world(Ms[0], v) for v in (A1, B1)]
            for b in range(3):
                for p, r in itertools.product((-1, 1), repeat=2):
                    c2 = [F(0), F(0), F(0)]; c2[(b + 1) % 3] = F(p); c2[(b + 2) % 3] = F(r)
                    A2 = [c2[k] - (F(1) if k == b else F(0)) for k in range(3)]
                    B2 = [c2[k] + (F(1) if k == b else F(0)) for k in range(3)]
                    E2 = [_world(Ms[1], v) for v in (A2, B2)]
                    pt = D.seg_int(E1[0], E1[1], E2[0], E2[1])
                    if pt is None:
                        continue
                    if D.nfacets(Ms[0], pt) != 2 or D.nfacets(Ms[1], pt) != 2:
                        continue
                    out.add((a, b, s, t, p, r))
    return out


def _world(M, v):
    """cube-frame coordinates -> world, where M's ROWS are the face normals (so M is the
    inverse of the frame): world = M^T v, because the normals are orthonormal."""
    return tuple(sum(F(M[rr][k]) * v[rr] for rr in range(3)) for k in range(3))


def main():
    import sympy as sp
    U = sp.symbols('u0:4'); V = sp.symbols('v0:4')

    def rot(q):
        w, x, y, z = q
        return sp.Matrix([[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
                          [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                          [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]])

    RU, RV = rot(U), rot(V)
    NU = sum(t * t for t in U); NV = sum(t * t for t in V)

    # the contact condition for edge (a; s,t) of cube U against edge (b; p,r) of cube V:
    # the two edge lines are coplanar.  Homogeneous, bidegree (2,2).
    FORMS = {}
    for a in range(3):
        for b in range(3):
            for s, t, p, r in itertools.product((-1, 1), repeat=4):
                d1 = RU * sp.Matrix([1 if i == a else 0 for i in range(3)])
                c1 = sp.Matrix([0, 0, 0]); c1[(a + 1) % 3] = s; c1[(a + 2) % 3] = t
                d2 = RV * sp.Matrix([1 if i == b else 0 for i in range(3)])
                c2 = sp.Matrix([0, 0, 0]); c2[(b + 1) % 3] = p; c2[(b + 2) % 3] = r
                FORMS[(a, b, s, t, p, r)] = sp.expand(
                    sp.Matrix.hstack(d1, d2, NU * RV * c2 - NV * RU * c1).det())
    print('contact forms built: %d' % len(FORMS), flush=True)

    out = {'what': 'compound-level Jacobian rank of the EE contact system',
           'supports': 'OQ 39', 'compounds': {}}
    print('\n   %-26s EE   active   sharing   rank   TANGENT dim   naive budget'
          % 'compound', flush=True)
    print('   (TANGENT dim = 9 - rank is an UPPER bound on the local family dimension, and')
    print('    equals it only at a SMOOTH point -- at a singular point the variety is smaller)',
          flush=True)

    for name, qs in NAMED.items():
        sig, _ = EB.vertices(qs)
        EE = sig.get((2, 2), 0)
        # the 9 parameters: coordinates of q2, q3, q4 (q1 is the gauge-fixed identity)
        params = []
        for k in (1, 2, 3):
            params += [sp.Symbol('p%d_%d' % (k, i)) for i in range(4)]
        subsmap = {}
        for k in (1, 2, 3):
            for i in range(4):
                subsmap[sp.Symbol('p%d_%d' % (k, i))] = sp.Integer(qs[k][i])

        rows = []
        active = 0
        for i, j in itertools.combinations(range(4), 2):
            qi, qj = qs[i], qs[j]
            # which contacts are live for this pair
            sub = {}
            for c in range(4):
                sub[U[c]] = sp.Integer(qi[c]); sub[V[c]] = sp.Integer(qj[c])
            live = in_range_labels(qi, qj)
            for lab, f in FORMS.items():
                # ONLY the contacts that actually occur.  A form can vanish because the two
                # edge LINES are coplanar while the segments miss each other entirely; that
                # is a coincidence at this point and not a condition the family must keep.
                # Counting those inflates the rank and understates the family's dimension.
                if lab not in live:
                    continue
                if sp.expand(f.subs(sub)) != 0:
                    raise AssertionError('a live contact whose form does not vanish: %s' % (lab,))
                active += 1
                # gradient w.r.t. the 9 parameters, via the chain rule: f depends on q_i, q_j
                row = []
                for k in (1, 2, 3):
                    for c in range(4):
                        g = sp.Integer(0)
                        if i == k:
                            g += sp.diff(f, U[c]).subs(sub)
                        if j == k:
                            g += sp.diff(f, V[c]).subs(sub)
                        row.append(g)
                rows.append(row)
        # THE CORNER SHARINGS ARE CONDITIONS TOO, and omitting them was the first version's
        # error.  A (3,3) vertex is a shared body-diagonal DIRECTION: R_i d_a = +-R_j d_b, two
        # scalar conditions per sharing, and nothing about edge-edge contacts implies them.
        # [P287] proved the 183 plateau is 0-dimensional, so a system returning rank 8 on the
        # record is under-determined, not evidence that the record moves.
        sharing_rows = 0
        for i, j in itertools.combinations(range(4), 2):
            for da in itertools.product((1, -1), repeat=3):
                for db in itertools.product((1, -1), repeat=3):
                    va = rot(U) * sp.Matrix(list(da)) * NV
                    vb = rot(V) * sp.Matrix(list(db)) * NU
                    sub = {}
                    for c in range(4):
                        sub[U[c]] = sp.Integer(qs[i][c]); sub[V[c]] = sp.Integer(qs[j][c])
                    diff = [sp.expand((va - vb)[k].subs(sub)) for k in range(3)]
                    if any(d != 0 for d in diff):
                        continue
                    for k in range(3):                      # 3 components, rank 2 of them
                        row = []
                        for kk in (1, 2, 3):
                            for c in range(4):
                                g = sp.Integer(0)
                                if i == kk:
                                    g += sp.diff((va - vb)[k], U[c]).subs(sub)
                                if j == kk:
                                    g += sp.diff((va - vb)[k], V[c]).subs(sub)
                                row.append(g)
                        rows.append(row)
                        sharing_rows += 1

        # quotient out the three per-cube scalings q_k -> lambda q_k
        for k in (1, 2, 3):
            row = [sp.Integer(0)] * 12
            for c in range(4):
                row[4 * (k - 1) + c] = sp.Integer(qs[k][c])
            rows.append(row)
        M = sp.Matrix(rows)
        rank = M.rank() - 3            # subtract the three scaling directions
        naive = 0
        codim = {0: 0, 4: 1, 6: 2, 8: 2, 10: 2}
        for i, j in itertools.combinations(range(4), 2):
            e = EB.vertices([qs[i], qs[j]])[0].get((2, 2), 0)
            naive += codim.get(e, 2)
        print('   %-26s %2d   %6d   %7d   %4d   %11d   %d'
              % (name, EE, active, sharing_rows, rank, 9 - rank, naive), flush=True)
        out['compounds'][name] = {'EE': EE, 'active_contacts': active,
                                  'sharing_rows': sharing_rows, 'rank': rank,
                                  'tangent_dim': 9 - rank, 'naive_budget': naive,
                                  'quats': [list(q) for q in qs]}

    print('\n   `rank` counts INDEPENDENT conditions; the naive budget counts them as though')
    print('   they were independent.  Where naive > rank the configuration has arranged')
    print('   dependency -- which is how it beats the parameter count.')
    print('   GATE: [P287] proved the 183 plateau is 0-DIMENSIONAL, so the record must reach')
    print('   rank 9.  If it does not, the system is missing conditions.')
    out['reproduce'] = PROV.stamp(note='exact rational Jacobian rank, gauge = q1 fixed, '
                                       'three per-cube scalings quotiented')
    json.dump(out, open(os.path.join(ROOT, 'data', 'compound_rigidity.json'), 'w'), indent=1)
    print('\nwrote data/compound_rigidity.json', flush=True)


if __name__ == '__main__':
    main()
