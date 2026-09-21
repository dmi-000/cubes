#!/usr/bin/env python3
"""[OQ 39] Is the 183 plateau's ARC a feature of n = 4, or of the whole family?

[P378]-[P380] found the n = 4 record on a constant-count arc: 36 edge contacts, Jacobian rank 8
on 9 parameters, one genuine direction.  The obvious question is whether that is special to four
cubes.  [P307] already measured plateau dimensions **1, 2, 2 at n = 6, 7, 8**, so positive
dimension is not new above; and the GLOSSARY records n = 3 as ISOLATED -- a belief of exactly
the kind [P378] overturned at n = 4, and tested there only by straight-line probes.

So: run the same computation at every n where a maximiser is known.

    parameters after gauge-fixing cube 0:  3(n-1)
    rank r  =>  tangent dimension 3(n-1) - r

**n = 4 IS THE CONTROL and must return 8.**  A method that cannot reproduce the known answer
says nothing about the unknown ones.

The n = 3 maximisers are irrational -- `1/2 + sqrt2` and `3*phi/2` ([Theorem R]), so no integer
quaternion represents them -- and are taken from `wall_keys.Q67` in their quadratic fields.
Rank there is read from the SINGULAR VALUE GAP at 60 digits, and the gap is printed so a
borderline call cannot hide: a rank claimed across a ratio of 1e-3 would be a guess, one across
1e-40 is not.
"""
import sys, os, json, itertools, pickle, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 60

    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')
    path = os.path.join(ROOT, 'catalogue_cache', 'contact_forms_%s.pkl'
                        % hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12])
    FORMS = {k: sp.sympify(val) for k, val in pickle.load(open(path, 'rb')).items()}

    def field_quats(entries, d):
        """(a, b) -> a + b*sqrt(d), as exact sympy"""
        r = sp.sqrt(d)
        return [tuple(sp.Integer(a) + sp.Integer(b) * r for (a, b) in q) for q in entries]

    cases = [
        ('n=3  67, field Q(sqrt2)', field_quats(WK.Q67[2], 2)),
        ('n=3  67, field Q(sqrt5)', field_quats(WK.Q67[5], 5)),
        ('n=4  RECORD 183 (control)', [tuple(sp.Integer(t) for t in q) for q in WK.REC[4]]),
        ('n=5  RECORD 393', [tuple(sp.Integer(t) for t in q) for q in WK.REC[5]]),
        ('n=6  RECORD 727', [tuple(sp.Integer(t) for t in q) for q in WK.REC[6]]),
        # THE DIVERGENCE TEST.  [P307] measured plateau dimensions 1, 2, 2 at n = 6, 7, 8.
        # This method returns 1 at n = 6 -- agreement, and a second control.  If it also
        # returns 1 at n = 7 and 8, the two methods CONFLICT there, and either the contact
        # system is missing conditions that [P307]'s walls capture, or the two are measuring
        # different objects.  A uniform "rank = params - 1" at every n is the kind of result
        # that is either a theorem or an artefact, and this is where it must show which.
        ('n=7  RECORD 1217', [tuple(sp.Integer(t) for t in q) for q in WK.REC[7]]),
        ('n=8  RECORD 1895', [tuple(sp.Integer(t) for t in q) for q in WK.REC[8]]),
    ]

    out = {'what': 'contact-system rank at every n with a known maximiser',
           'supports': 'OQ 39; extends P378-P380', 'cases': {}}
    print('   %-26s %5s %8s %6s %6s %9s %s'
          % ('configuration', 'n', 'contacts', 'params', 'rank', 'tangent', 'sv gap'),
          flush=True)

    for name, qsym_vals in cases:
        n = len(qsym_vals)
        # numeric quaternions for the contact search
        qnum = [tuple(float(sp.N(t, 40)) for t in q) for q in qsym_vals]
        # contacts: found numerically at high precision (the exact in_range_labels needs
        # rationals, and these are not rational)
        LAB = []
        for i, j in itertools.combinations(range(n), 2):
            try:
                labs = CR.in_range_labels(_rationalise(qnum[i]), _rationalise(qnum[j]))
            except Exception:
                labs = set()
            for lab in labs:
                LAB.append(((i, j), lab))

        P = sp.symbols('P0:%d' % (4 * (n - 1)))
        qs2 = [list(qsym_vals[0])] + \
              [[P[4 * (k - 1) + c] for c in range(4)] for k in range(1, n)]
        eqs = []
        for (i, j), lab in LAB:
            sub = {}
            for c in range(4):
                sub[u[c]] = qs2[i][c]; sub[v[c]] = qs2[j][c]
            eqs.append(FORMS[lab].subs(sub))
        if not eqs:
            print('   %-26s %5d %8d   -- no contacts found --' % (name, n, 0), flush=True)
            out['cases'][name] = {'n': n, 'contacts': 0, 'note': 'no contacts located'}
            continue
        Jm = sp.Matrix([[sp.diff(e, p) for p in P] for e in eqs])
        subs0 = {}
        for k in range(1, n):
            for c in range(4):
                subs0[P[4 * (k - 1) + c]] = qsym_vals[k][c]
        Jv = Jm.subs(subs0)
        # scalings
        rows = [[mp.mpf(str(sp.N(Jv[r, c], 50))) for c in range(4 * (n - 1))]
                for r in range(Jv.rows)]
        for k in range(1, n):
            row = [mp.mpf(0)] * (4 * (n - 1))
            for c in range(4):
                row[4 * (k - 1) + c] = mp.mpf(str(sp.N(qsym_vals[k][c], 50)))
            rows.append(row)
        A = mp.matrix(rows)
        try:
            S = mp.svd_r(A, compute_uv=False)
        except Exception:
            print('   %-26s %5d  SVD refused (unevaluable, not rank 0)' % (name, n), flush=True)
            out['cases'][name] = {'n': n, 'contacts': len(LAB), 'note': 'SVD refused'}
            continue
        sv = sorted([abs(S[k]) for k in range(len(S))], reverse=True)
        smax = sv[0]
        rank = sum(1 for s in sv if s > smax * mp.mpf('1e-25'))
        gap = 'n/a'
        if rank < len(sv):
            gap = mp.nstr(sv[rank - 1] / max(sv[rank], mp.mpf('1e-300')), 4)
        params = 3 * (n - 1)
        tang = params - (rank - (n - 1))
        print('   %-26s %5d %8d %6d %6d %9d   %s'
              % (name, n, len(LAB), params, rank - (n - 1), tang, gap), flush=True)
        out['cases'][name] = {'n': n, 'contacts': len(LAB), 'params': params,
                              'rank': int(rank - (n - 1)), 'tangent_dim': int(tang),
                              'singular_value_gap': str(gap)}

    out['reproduce'] = PROV.stamp(parameters={'dps': 60, 'rank_threshold': '1e-25'},
                                  note='rank from the singular-value gap; n=4 is the control')
    json.dump(out, open(os.path.join(ROOT, 'data', 'rank_by_n.json'), 'w'), indent=1)
    print('\nwrote data/rank_by_n.json', flush=True)


def _rationalise(q, den=10**12):
    from fractions import Fraction as F
    vals = [F(int(round(t * den)), den) for t in q]
    g = 0
    from math import gcd
    ints = [v.numerator * (den // v.denominator) for v in vals]
    for t in ints:
        g = gcd(g, abs(t))
    if g == 0:
        return tuple(int(t) for t in ints)
    return tuple(int(t // g) for t in ints)


if __name__ == '__main__':
    main()
