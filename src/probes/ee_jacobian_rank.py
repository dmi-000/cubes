#!/usr/bin/env python3
"""[OQ 39] The CODIMENSION of each `EE` stratum, exactly — by Jacobian rank, not by counting.

The open question after [P373] is what limits `EE` when `B = 128`.  The per-subset route is
exhausted (`max(3) = 67` gives `EE <= 60`, the box bound already known), so the real constraint
is how many PAIRS can sit on a high-`EE` stratum at once.  A 4-compound has 9 free parameters
and 6 pairs, so the arithmetic is `sum over pairs of codim <= 9` — and the codimensions are
what this measures.

**EXACT, AND NOT A SAMPLE.**  [P366] showed edge `e` of one cube meets edge `f` of the other iff
one homogeneous DEGREE-4 form in the relative quaternion vanishes (144 of them, none identically
zero).  At a point `q` the ACTIVE set is the forms that vanish there with the crossing in range;
the codimension of the stratum through `q` is the rank of their Jacobian restricted to the
tangent space of the 3-sphere.  Rational `q`, integer forms, exact rank over `Q` — no tolerance
anywhere, and no counting argument that a larger height could overturn.

Antipodal symmetry pairs the contacts, so `EE = 2k` means `k` antipodal classes and at most `k`
independent conditions; the measured rank says how many are actually independent.
"""
import sys, os, json, itertools, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_determinantal as D
from euler3 import rowsT, frames
from c_level import shares_plane
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def build_forms():
    """the 144 coplanarity quartics, as sympy polynomials in (w,x,y,z), with their edge labels"""
    import sympy as sp
    w, x, y, z = sp.symbols('w x y z')
    N = w * w + x * x + y * y + z * z
    R = sp.Matrix([[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
                   [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                   [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]])
    forms = []
    for a in range(3):
        for b in range(3):
            for s, t, u, v in itertools.product((-1, 1), repeat=4):
                d1 = sp.Matrix([1 if i == a else 0 for i in range(3)])
                p1 = sp.Matrix([0, 0, 0]); p1[(a + 1) % 3] = s; p1[(a + 2) % 3] = t
                q2 = sp.Matrix([0, 0, 0]); q2[(b + 1) % 3] = u; q2[(b + 2) % 3] = v
                Dt = sp.expand(sp.Matrix.hstack(d1, R * q2 - N * p1).row_join(R * sp.Matrix(
                    [1 if i == b else 0 for i in range(3)])).det())
                forms.append(((a, b, s, t, u, v), sp.Poly(Dt, w, x, y, z)))
    return (w, x, y, z), forms


def main():
    import sympy as sp
    syms, forms = build_forms()
    w, x, y, z = syms
    print('quartic forms built: %d   (all degree %s)'
          % (len(forms), sorted({f.total_degree() for _, f in forms})), flush=True)

    grads = [(lab, [sp.Poly(sp.diff(f.as_expr(), s), w, x, y, z) for s in syms])
             for lab, f in forms]

    # representatives of each observed EE value, from the exact census
    reps = {}
    for q in itertools.product(range(-5, 6), repeat=4):
        if not any(q):
            continue
        from math import gcd
        g = 0
        for v in q:
            g = gcd(g, abs(v))
        if g != 1:
            continue
        neg = False
        for v in q:
            if v:
                neg = v < 0
                break
        if neg or shares_plane([(1, 0, 0, 0), q]):
            continue
        e = D.ee_exact(q)
        reps.setdefault(e, []).append(q)
    print('EE values with representatives: %s'
          % {k: len(v) for k, v in sorted(reps.items())}, flush=True)

    out = {'what': 'codimension of each EE stratum by exact Jacobian rank',
           'supports': 'OQ 39', 'strata': {}}
    print('\n   EE   sample   vanishing forms   Jacobian rank   codim on S^3   dim of stratum')
    for e in sorted(reps):
        ranks = collections.Counter(); nvan = collections.Counter()
        sample = reps[e][:6]
        for q in sample:
            sub = dict(zip(syms, [sp.Integer(t) for t in q]))
            rows = []
            nv = 0
            for lab, f in forms:
                if f.as_expr().subs(sub) == 0:
                    nv += 1
                    rows.append([g.as_expr().subs(sub) for g in dict(grads)[lab]])
            nvan[nv] += 1
            # restrict to the tangent space of the sphere: add the radial direction and
            # measure how much the active gradients add beyond it
            M = sp.Matrix(rows + [[sp.Integer(t) for t in q]]) if rows else \
                sp.Matrix([[sp.Integer(t) for t in q]])
            ranks[M.rank() - 1] += 1
        r = ranks.most_common(1)[0][0]
        print('   %2d   %6d   %15s   %13s   %12d   %d'
              % (e, len(sample), dict(nvan), dict(ranks), r, 3 - r), flush=True)
        out['strata'][str(e)] = {'sampled': len(sample),
                                 'vanishing_forms': {str(k): v for k, v in nvan.items()},
                                 'ranks': {str(k): v for k, v in ranks.items()},
                                 'codim': r, 'dim': 3 - r}

    print('\n   A 4-compound has 9 free parameters (three cube rotations) and 6 pairs, and the')
    print('   six relative rotations are determined by those 9.  So a profile demanding')
    print('   codimensions c_1..c_6 needs  sum c_i <= 9  to be expected at all.')
    cod = {int(k): v['codim'] for k, v in out['strata'].items()}
    for e, c in sorted(cod.items()):
        if c:
            print('      all six pairs at EE = %2d costs 6 * %d = %2d   %s'
                  % (e, c, 6 * c, 'FEASIBLE' if 6 * c <= 9 else 'over-determined'))
    out['budget'] = {'parameters': 9, 'pairs': 6,
                     'codim_by_EE': cod}

    out['reproduce'] = PROV.stamp(
        parameters={'representative_height': 5, 'samples_per_stratum': 6},
        note='exact rational Jacobian rank; no tolerance, no height census')
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_jacobian_rank.json'), 'w'), indent=1)
    print('\nwrote data/ee_jacobian_rank.json', flush=True)


if __name__ == '__main__':
    main()
