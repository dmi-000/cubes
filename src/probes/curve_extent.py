#!/usr/bin/env python3
"""[OQ 39] How far does the 183 curve go, and does the SECOND 183 class sit on the same kind?

[P378] showed the n = 4 record lies on a curve along which the full vertex census is preserved,
confirming the locus [P136] found from walls and refuting [P136]'s own reading of it (*"the
count is NOT constant along it"*) and [P287]'s isolation.

[P136] predicts the curve passes through the SECOND 183 class.  Testing that directly is harder
than it looks: the two classes are *"identical on every invariant"* ([P133]), so no invariant
can detect arrival, and the configurations live in different gauges.  What CAN be settled:

  A.  Does the second class have the same local structure -- 36 contacts, rank 8, a curve?
      If it is isolated while the record is not, [P136]'s shared-wall locus cannot be a
      constant-count curve through both.
  B.  How far does the record's curve extend with the census preserved?  Arc-length
      continuation, stepping and re-projecting, until the census changes or Newton fails.

This does NOT prove the two classes are joined.  It reports extent and structure, which is what
the method can support ([METHODS 1]).
"""
import sys, os, json, itertools, pickle, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import ee_bound_refute as EB
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))

REC = [tuple(q) for q in WK.REC[4]]
SECOND = [tuple(q) for q in WK.NAMED['n4_183']]


def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)


def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])


def normalise(qs):
    """gauge-fix by rotating so cube 0 becomes the identity cube"""
    return [qmul(qconj(qs[0]), q) for q in qs]


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 50

    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')
    CACHE = os.path.join(ROOT, 'catalogue_cache')
    path = os.path.join(CACHE, 'contact_forms_%s.pkl'
                        % hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12])
    FORMS = {k: sp.sympify(val) for k, val in pickle.load(open(path, 'rb')).items()}
    print('forms from cache: %d' % len(FORMS), flush=True)

    out = {'what': 'extent of the 183 curve; structure at the second 183 class',
           'supports': 'OQ 39; follows P378, P136', 'classes': {}}

    print('\nA. THE TWO 183 CLASSES, each gauge-fixed so cube 0 is the identity')
    for name, qs0 in (('record', REC), ('second class [P133]', SECOND)):
        qs = normalise(qs0)
        sig, _ = EB.vertices(qs)
        P = sp.symbols('P0:12')
        qsym = [[sp.Integer(qs[0][c]) for c in range(4)]] + \
               [[P[4 * (k - 1) + c] for c in range(4)] for k in (1, 2, 3)]
        eqs = []
        for i, j in itertools.combinations(range(4), 2):
            for lab in CR.in_range_labels(qs[i], qs[j]):
                sub = {}
                for c in range(4):
                    sub[u[c]] = qsym[i][c]; sub[v[c]] = qsym[j][c]
                eqs.append(FORMS[lab].subs(sub))
        x0 = [sp.Integer(qs[k][c]) for k in (1, 2, 3) for c in range(4)]
        J = sp.Matrix([[sp.diff(e, p) for p in P] for e in eqs]).subs(dict(zip(P, x0)))
        rank = J.rank()
        ns = 12 - rank
        print('   %-20s census %s' % (name, dict(sorted(sig.items()))), flush=True)
        print('   %-20s contacts %d   Jacobian rank %d   null %d   genuine %d'
              % ('', len(eqs), rank, ns, ns - 3), flush=True)
        out['classes'][name] = {'quats': [list(q) for q in qs],
                                'census': {str(k): val for k, val in sorted(sig.items())},
                                'contacts': len(eqs), 'rank': int(rank),
                                'nullspace': int(ns), 'genuine_directions': int(ns - 3)}

    print('\nB. ARC-LENGTH CONTINUATION from the record, census checked at every step')
    qs = normalise(REC)
    P = sp.symbols('P0:12')
    qsym = [[sp.Integer(qs[0][c]) for c in range(4)]] + \
           [[P[4 * (k - 1) + c] for c in range(4)] for k in (1, 2, 3)]
    LAB = []
    eqs = []
    for i, j in itertools.combinations(range(4), 2):
        for lab in CR.in_range_labels(qs[i], qs[j]):
            LAB.append(((i, j), lab))
            sub = {}
            for c in range(4):
                sub[u[c]] = qsym[i][c]; sub[v[c]] = qsym[j][c]
            eqs.append(FORMS[lab].subs(sub))
    J = sp.Matrix([[sp.diff(e, p) for p in P] for e in eqs])
    Ff = sp.lambdify(P, eqs, 'mpmath')
    Jf = sp.lambdify(P, J.tolist(), 'mpmath')

    import record_curve as RCV
    WANT = {(1, 1, 1): 128, (1, 2): 24, (2, 2): 36, (3, 3): 6}
    gate, gskip, _ = RCV.full_census(mp, qs[0], [mp.mpf(int(qs[k][c]))
                                                 for k in (1, 2, 3) for c in range(4)])
    print('   GATE, census at the gauge-fixed record: %s   %s'
          % (gate, 'PASS' if gate == WANT else 'FAIL'), flush=True)
    out['gate'] = {'census': {str(k): val for k, val in gate.items()},
                   'pass': bool(gate == WANT)}
    if gate != WANT:
        print('   refusing to continue', flush=True)
        json.dump(out, open(os.path.join(ROOT, 'data', 'curve_extent.json'), 'w'), indent=1)
        return

    # NORMALISE THE REPRESENTATIVE.  Gauge-fixing by q -> conj(q0)*q multiplies every height
    # by |q0|^2, and the forms are degree 4, so J's entries grow like height^4 and the normal
    # equations become hopeless.  The height is a free choice ([METHODS]: a refusal may be
    # about your representative), so use unit quaternions and keep everything O(1).
    x = []
    for k in (1, 2, 3):
        n = mp.sqrt(sum(mp.mpf(int(qs[k][c])) ** 2 for c in range(4)))
        x += [mp.mpf(int(qs[k][c])) / n for c in range(4)]
    # GATE: the system must actually vanish at the starting point
    f0 = max(abs(t) for t in mp.matrix(Ff(*x)))
    print('   GATE, |F| at the gauge-fixed record: %s   %s'
          % (mp.nstr(f0, 5), 'PASS' if f0 < mp.mpf('1e-30') else 'FAIL'), flush=True)
    out['start_residual'] = mp.nstr(f0, 8)
    if f0 >= mp.mpf('1e-30'):
        print('   refusing to continue: the contact system does not vanish at the start',
              flush=True)
        json.dump(out, open(os.path.join(ROOT, 'data', 'curve_extent.json'), 'w'), indent=1)
        return
    H = mp.mpf('0.01')
    good = 0
    rows = []
    total = mp.mpf(0)
    prev_dir = None
    for stepn in range(140):
        Jv = mp.matrix(Jf(*x))
        # TANGENT by inverse iteration on a 12x12, not by SVD of a 36x12.
        # mpmath's svd_r at 50 digits dominated the runtime and was called every step; the
        # tangent is the null vector of  M = J^T J + sum_k s_k s_k^T  (the scalings folded in
        # as penalties), which inverse iteration finds in a handful of 12x12 solves.
        M = mp.matrix(12, 12)
        for r in range(Jv.rows):
            for a_ in range(12):
                if Jv[r, a_] == 0:
                    continue
                for b_ in range(12):
                    M[a_, b_] = M[a_, b_] + Jv[r, a_] * Jv[r, b_]
        for k in range(3):
            sc = [mp.mpf(0)] * 12
            for c in range(4):
                sc[4 * k + c] = x[4 * k + c]
            nn = mp.sqrt(sum(t * t for t in sc))
            sc = [t / nn for t in sc]
            for a_ in range(12):
                for b_ in range(12):
                    M[a_, b_] = M[a_, b_] + sc[a_] * sc[b_]
        scale = max(abs(M[a_, a_]) for a_ in range(12))
        Mi = M + mp.eye(12) * (scale * mp.mpf('1e-30'))
        y = mp.matrix([mp.mpf(1) / (k + 3) for k in range(12)]) if prev_dir is None \
            else mp.matrix(prev_dir)
        cand = []
        try:
            for _ in range(40):
                y = mp.lu_solve(Mi, y)
                n2 = mp.sqrt(sum(y[k] ** 2 for k in range(12)))
                y = mp.matrix([y[k] / n2 for k in range(12)])
            w = [y[k] for k in range(12)]
            for k in range(3):
                sc = [mp.mpf(0)] * 12
                for c in range(4):
                    sc[4 * k + c] = x[4 * k + c]
                nn = sum(t * t for t in sc)
                d_ = sum(w[i2] * sc[i2] for i2 in range(12)) / nn
                w = [w[i2] - d_ * sc[i2] for i2 in range(12)]
            nw = mp.sqrt(sum(t * t for t in w))
            if nw > mp.mpf('1e-15'):
                cand = [[t / nw for t in w]]
        except Exception:
            print('   step %d: tangent solve failed (unevaluable, not an end)' % stepn,
                  flush=True)
            break
        print('      step %d: tangent found, |J d| = %s'
              % (stepn, mp.nstr(max(abs(t) for t in (Jv * mp.matrix(cand[0]))), 5))
              if cand else '      step %d: no tangent' % stepn, flush=True) \
            if stepn == 0 else None
        if not cand:
            print('   step %d: no genuine tangent -- curve ends here' % stepn, flush=True)
            break
        d = cand[0]
        if prev_dir is not None and sum(d[i2] * prev_dir[i2] for i2 in range(12)) < 0:
            d = [-t for t in d]
        prev_dir = d
        # ADAPTIVE STEP.  A fixed step of 0.02 failed Newton at the very first step: the
        # predictor leaves the curve far enough that the corrector cannot return within
        # tolerance.  Halve until it converges, and grow again after two clean steps --
        # otherwise a continuation reports "the curve ends here" when what ended was the
        # step size ([METHODS]: a refusal may be about the representative, not the object).
        ok = False
        for _ in range(14):
            xn = [x[i] + H * d[i] for i in range(12)]
            for _ in range(60):
                Fv = mp.matrix(Ff(*xn)); Jv2 = mp.matrix(Jf(*xn))
                try:
                    A2 = Jv2.T * Jv2
                    sc2 = max(abs(A2[q_, q_]) for q_ in range(12))
                    if sc2 == 0:
                        break
                    dx = mp.lu_solve(A2 + mp.eye(12) * (sc2 * mp.mpf('1e-28')),
                                     -(Jv2.T * Fv))
                    if max(abs(t) for t in dx) > mp.mpf('0.5'):
                        break                      # reject a runaway correction
                except Exception:
                    break
                xn = [xn[i] + dx[i] for i in range(12)]
                if max(abs(t) for t in dx) < mp.mpf('1e-40'):
                    break
            resid = max(abs(t) for t in mp.matrix(Ff(*xn)))
            if resid <= mp.mpf('1e-18'):
                ok = True
                break
            H = H / 2
        if not ok:
            print('   step %d: Newton fails even at H = %s (|F| = %s) -- stopping'
                  % (stepn, mp.nstr(H, 4), mp.nstr(resid, 5)), flush=True)
            break
        good = good + 1 if 'good' in dir() else 1
        cen, skip, cmar = RCV.full_census(mp, qs[0], xn)
        nin, _ = RCV.contacts_at(mp, qs[0], xn, LAB)
        total += H
        same = (cen == WANT)
        if stepn % 6 == 0 or not same:
            print('   step %2d   arc %s   |F| %s   %d/%d contacts   census %s'
                  % (stepn, mp.nstr(total, 5), mp.nstr(resid, 5), nin, len(LAB),
                     'SAME' if same else 'CHANGED: %s' % cen), flush=True)
        rows.append({'step': stepn, 'arc': mp.nstr(total, 8), 'residual': mp.nstr(resid, 6),
                     'contacts_in_range': nin, 'census_same': bool(same)})
        if not same:
            print('   census changed at arc length %s -- the constant-count stretch ends here'
                  % mp.nstr(total, 6), flush=True)
            break
        x = xn
        if good >= 2 and H < mp.mpf('0.05'):
            H = H * 2
            good = 0
    out['continuation'] = rows
    out['arc_reached'] = mp.nstr(total, 8)
    print('\n   arc length with the census preserved: %s over %d steps'
          % (mp.nstr(total, 6), len(rows)), flush=True)

    out['reproduce'] = PROV.stamp(parameters={'dps': 50, 'step': '0.02', 'max_steps': 60})
    json.dump(out, open(os.path.join(ROOT, 'data', 'curve_extent.json'), 'w'), indent=1)
    print('\nwrote data/curve_extent.json', flush=True)


if __name__ == '__main__':
    main()
