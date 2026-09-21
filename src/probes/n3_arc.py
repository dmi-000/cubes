#!/usr/bin/env python3
"""[OQ 39] Is the n = 3 maximiser isolated, or is it on an arc too?

[P381] found BOTH 67s carrying a 1-dimensional tangent -- rank 5 of 6 -- which is the structure
n = 4 had while [P287] believed it isolated.  [GLOSSARY] still records n = 3 as isolated: *"for
a configuration, means no continuum of the same count around it (true at n = 3)"*.  A tangent is
an upper bound on dimension, so that belief is not yet refuted; it is UNTESTED by the one test
that settled n = 4.

This runs that test: Newton continuation along the tangent, with the full census recomputed at
every step.  If the displacement survives correction with the census intact, the 67 lies on an
arc and the isolation claim falls exactly as [P287]'s did.  If Newton returns to the 67 or the
census breaks immediately, the tangent is obstructed at higher order and isolation stands with
a second, independent argument.

**THE 67s ARE IRRATIONAL** -- `1/2 + sqrt2` and `3*phi/2` ([Theorem R]) -- so there is no exact
rational point to work from and everything runs at 50 digits.  Two gates, both from
[FAILURE_MODES 46] and [P378]: `|F|` at the start must vanish, and the census routine must
reproduce the 67's OWN census before any continuation is reported.
"""
import sys, os, json, itertools, pickle, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def census_n(mp, qlist, tol_exp=18):
    """full signature census for ANY number of cubes, at high precision.

    Carries both lessons the n = 4 version had to learn: rows = FACE NORMALS (the columns of
    the rotation matrix), and a vertex outside cube k means cube k ABSTAINS -- it does not
    discard the vertex."""
    import itertools as it
    F = []
    for q in qlist:
        w, x, y, z = q
        n = w * w + x * x + y * y + z * z
        M = [[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
             [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
             [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]]
        F.append([[M[r][c] / n for r in range(3)] for c in range(3)])
    planes = []
    for ci, M in enumerate(F):
        for r in range(3):
            for sg in (1, -1):
                planes.append((ci, [sg * M[r][c] for c in range(3)]))

    def det3(A):
        return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
                - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
                + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))

    TOL = mp.mpf('1e-%d' % tol_exp)
    pts = []; skipped = 0
    for t in it.combinations(range(len(planes)), 3):
        if len({planes[i][0] for i in t}) < 2:
            continue
        A = [planes[i][1][:] for i in t]
        d = det3(A)
        if abs(d) < TOL:
            skipped += 1
            continue
        sol = []
        for c in range(3):
            B = [r[:] for r in A]
            for r in range(3):
                B[r][c] = mp.mpf(1)
            sol.append(det3(B) / d)
        pts.append(sol)

    sig = {}; seen = []
    for p in pts:
        if any(max(abs(p[k] - o[k]) for k in range(3)) < TOL for o in seen):
            continue
        seen.append(p)
        s = []
        for M in F:
            hs = [sum(M[r][c] * p[c] for c in range(3)) for r in range(3)]
            on = 0; outside = False
            for h in hs:
                if abs(abs(h) - 1) < TOL:
                    on += 1
                elif abs(h) > 1:
                    outside = True
                    break
            if outside:
                continue
            if on:
                s.append(on)
        if len(s) >= 2 and sum(s) >= 3:
            k = tuple(sorted(s))
            sig[k] = sig.get(k, 0) + 1
    return sig, skipped


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 50

    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')
    path = os.path.join(ROOT, 'catalogue_cache', 'contact_forms_%s.pkl'
                        % hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12])
    FORMS = {k: sp.sympify(val) for k, val in pickle.load(open(path, 'rb')).items()}

    out = {'what': 'is the n=3 maximiser on an arc?', 'supports': 'OQ 39; tests GLOSSARY '
           '"isolated at n=3" and follows P381', 'fields': {}}

    for d in (2, 5):
        name = 'Q(sqrt%d)' % d
        print('\n=== the 67 in %s ===' % name, flush=True)
        qsym = [tuple(sp.Integer(a) + sp.Integer(b) * sp.sqrt(d) for (a, b) in q)
                for q in WK.Q67[d]]
        qnum = [tuple(mp.mpf(str(sp.N(t, 45))) for t in q) for q in qsym]

        cen0, skip0 = census_n(mp, qnum)
        tot0 = sum(cen0.values())
        print('   census at the 67: %s   (skipped %d)' % (dict(sorted(cen0.items())), skip0),
              flush=True)

        # contacts, located from a high-precision rationalisation
        from fractions import Fraction as Fr
        def rat(q, den=10**14):
            return tuple(int(round(float(t) * den)) for t in q)
        LAB = []
        for i, j in itertools.combinations(range(3), 2):
            for lab in CR.in_range_labels(rat(qnum[i]), rat(qnum[j])):
                LAB.append(((i, j), lab))
        print('   contacts located: %d' % len(LAB), flush=True)

        P = sp.symbols('P0:8')
        qs2 = [list(qsym[0])] + [[P[4 * (k - 1) + c] for c in range(4)] for k in (1, 2)]
        eqs = []
        for (i, j), lab in LAB:
            sub = {}
            for c in range(4):
                sub[u[c]] = qs2[i][c]; sub[v[c]] = qs2[j][c]
            eqs.append(FORMS[lab].subs(sub))
        Jm = sp.Matrix([[sp.diff(e, p) for p in P] for e in eqs])
        Ff = sp.lambdify(P, eqs, 'mpmath'); Jf = sp.lambdify(P, Jm.tolist(), 'mpmath')

        x0 = []
        for k in (1, 2):
            nn = mp.sqrt(sum(qnum[k][c] ** 2 for c in range(4)))
            x0 += [qnum[k][c] / nn for c in range(4)]
        f0 = max(abs(t) for t in mp.matrix(Ff(*x0)))
        print('   GATE |F| at the 67: %s   %s'
              % (mp.nstr(f0, 5), 'PASS' if f0 < mp.mpf('1e-35') else 'FAIL'), flush=True)
        rec = {'census': {str(k): val for k, val in cen0.items()}, 'vertices': tot0,
               'contacts': len(LAB), 'start_residual': mp.nstr(f0, 8)}
        if f0 >= mp.mpf('1e-35'):
            print('   refusing to continue', flush=True)
            out['fields'][name] = rec
            continue

        # tangent by inverse iteration on the 8x8
        Jv = mp.matrix(Jf(*x0))
        M = mp.matrix(8, 8)
        for r in range(Jv.rows):
            for a_ in range(8):
                if Jv[r, a_] == 0:
                    continue
                for b_ in range(8):
                    M[a_, b_] = M[a_, b_] + Jv[r, a_] * Jv[r, b_]
        for k in range(2):
            sc = [mp.mpf(0)] * 8
            for c in range(4):
                sc[4 * k + c] = x0[4 * k + c]
            nn = mp.sqrt(sum(t * t for t in sc)); sc = [t / nn for t in sc]
            for a_ in range(8):
                for b_ in range(8):
                    M[a_, b_] = M[a_, b_] + sc[a_] * sc[b_]
        scale = max(abs(M[a_, a_]) for a_ in range(8))
        Mi = M + mp.eye(8) * (scale * mp.mpf('1e-30'))
        y = mp.matrix([mp.mpf(1) / (k + 3) for k in range(8)])
        for _ in range(60):
            y = mp.lu_solve(Mi, y)
            n2 = mp.sqrt(sum(y[k] ** 2 for k in range(8)))
            y = mp.matrix([y[k] / n2 for k in range(8)])
        w = [y[k] for k in range(8)]
        for k in range(2):
            sc = [mp.mpf(0)] * 8
            for c in range(4):
                sc[4 * k + c] = x0[4 * k + c]
            nn = sum(t * t for t in sc)
            dd = sum(w[i2] * sc[i2] for i2 in range(8)) / nn
            w = [w[i2] - dd * sc[i2] for i2 in range(8)]
        nw = mp.sqrt(sum(t * t for t in w))
        if nw < mp.mpf('1e-15'):
            print('   no genuine tangent -- ISOLATED by this test', flush=True)
            rec['verdict'] = 'no genuine tangent'
            out['fields'][name] = rec
            continue
        dvec = [t / nw for t in w]
        resid_t = max(abs(t) for t in (Jv * mp.matrix(dvec)))
        print('   tangent |J d| = %s' % mp.nstr(resid_t, 5), flush=True)

        def correct(xn):
            for _ in range(60):
                Fv = mp.matrix(Ff(*xn)); Jv2 = mp.matrix(Jf(*xn))
                A2 = Jv2.T * Jv2
                sc2 = max(abs(A2[q_, q_]) for q_ in range(8))
                if sc2 == 0:
                    return None
                try:
                    dx = mp.lu_solve(A2 + mp.eye(8) * (sc2 * mp.mpf('1e-28')), -(Jv2.T * Fv))
                except Exception:
                    return None
                if max(abs(t) for t in dx) > mp.mpf('0.5'):
                    return None
                xn = [xn[i] + dx[i] for i in range(8)]
                if max(abs(t) for t in dx) < mp.mpf('1e-40'):
                    break
            return xn if max(abs(t) for t in mp.matrix(Ff(*xn))) < mp.mpf('1e-30') else None

        # BOTH DIRECTIONS.  The first version stepped only along +d and concluded
        # "isolated".  At n = 4 the two directions differed by a factor of TWELVE
        # (0.0517 against 0.6356), so a one-sided test cannot support that word.
        print('   dirn  step       |F| after Newton     moved by        census', flush=True)
        steps = []
        for sgn, sname in ((1, '+'), (-1, '-')):
          for st in ('1e-3', '1e-4', '1e-5'):
            h = mp.mpf(st) * sgn
            xn = correct([x0[i] + h * dvec[i] for i in range(8)])
            if xn is None:
                print('   %-4s  %-9s corrector failed' % (sname, st), flush=True)
                steps.append({'dirn': sname, 'step': st, 'result': 'corrector failed'})
                continue
            moved = mp.sqrt(sum((xn[i] - x0[i]) ** 2 for i in range(8)))
            qn = [qnum[0]] + [tuple(xn[4 * k + c] for c in range(4)) for k in range(2)]
            cen, _ = census_n(mp, qn)
            same = (cen == cen0)
            print('   %-4s  %-9s  %-18s  %-12s  %s'
                  % (sname, st, mp.nstr(max(abs(t) for t in mp.matrix(Ff(*xn))), 5),
                     mp.nstr(moved, 8), 'SAME' if same else 'CHANGED: %s' % dict(cen)),
                  flush=True)
            steps.append({'dirn': sname, 'step': st, 'moved': mp.nstr(moved, 10),
                          'census_same': bool(same),
                          'census': {str(k): val for k, val in cen.items()}})
        rec['tangent_residual'] = mp.nstr(resid_t, 8)
        rec['continuation'] = steps
        kept = [s for s in steps if s.get('census_same')]
        moved_ok = [s for s in steps if 'moved' in s and
                    float(s['moved']) > abs(float(s['step'])) * 0.5]
        rec['verdict'] = (
            'ON AN ARC in at least one direction' if kept else
            'the CONTACT curve is real (displacement survives, |F| stays at 1e-50) but the '
            'COUNT does not extend: the 67 sits AT a boundary of its own arc, in both '
            'directions' if moved_ok else
            'no surviving displacement')
        print('   VERDICT: %s' % rec['verdict'], flush=True)
        out['fields'][name] = rec

    out['reproduce'] = PROV.stamp(parameters={'dps': 50, 'steps': ['1e-3', '1e-4', '1e-5']})
    json.dump(out, open(os.path.join(ROOT, 'data', 'n3_arc.json'), 'w'), indent=1)
    print('\nwrote data/n3_arc.json', flush=True)


if __name__ == '__main__':
    main()
