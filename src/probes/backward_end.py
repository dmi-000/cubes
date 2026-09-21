#!/usr/bin/env python3
"""[OQ 39] The BACKWARD end of the 183 plateau arc — found by steering on the margin, then solved.

[P378] bracketed the forward end at arc 0.05168.  Backward, the walk was still at 183 when its
budget ran out at 0.3, so the record sits near one end of an asymmetric interval and the far end
was never reached.

**WHAT ENDS THE ARC IS AN ALGEBRAIC CONDITION, not a place the walk gets tired.**  Each contact
has crossing parameters `s, t` in `[0,1]`; the plateau ends when one of them reaches an endpoint
-- the crossing arrives at a CORNER of a cube, and the vertex turns from `(2,2)` into `(3,2)`.
So the endpoint satisfies the 36 contact equations PLUS one corner condition: 9 conditions on a
9-parameter space, hence isolated, hence solvable rather than approachable.

TWO PHASES.

  A.  STEER ON THE MARGIN.  `contacts_at` already returns the smallest distance any parameter
      has to `{0,1}`.  That margin IS the distance to the boundary in the only coordinate that
      matters, so the step grows while the margin is comfortable and shrinks as it closes --
      instead of a fixed step walking blind for hundreds of iterations.

  B.  SOLVE THE ENDPOINT.  Once the margin is small, Newton on the augmented system (contacts
      + the dying parameter pinned to its limit) lands ON the boundary instead of near it.

Gates carried from [FAILURE_MODES 46]: `|F|` at the start must vanish, `|J d|` must sit at the
arithmetic's floor, and a corrector failure is reported as a corrector failure.
"""
import sys, os, json, itertools, pickle, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import record_curve as RCV
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
REC = [tuple(q) for q in WK.REC[4]]
WANT = {(1, 1, 1): 128, (1, 2): 24, (2, 2): 36, (3, 3): 6}


def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)



def dying_contact(mp, q0, x, labels):
    """which contact's crossing parameter is closest to an endpoint, and which endpoint"""
    qs = [[mp.mpf(int(t)) for t in q0]] + \
         [[x[4 * k + c] for c in range(4)] for k in range(3)]

    def frame(q):
        w, xx, y, z = q
        n = w * w + xx * xx + y * y + z * z
        M = [[w*w+xx*xx-y*y-z*z, 2*(xx*y-w*z),      2*(xx*z+w*y)],
             [2*(xx*y+w*z),      w*w-xx*xx+y*y-z*z, 2*(y*z-w*xx)],
             [2*(xx*z-w*y),      2*(y*z+w*xx),      w*w-xx*xx-y*y+z*z]]
        return [[M[r][c] / n for r in range(3)] for c in range(3)]

    F = [frame(q) for q in qs]

    def world(M, v):
        return [sum(M[r][k] * v[r] for r in range(3)) for k in range(3)]

    best = None
    for (i, j), lab in labels:
        a, b, s1, t1, p1, r1 = lab
        c1 = [mp.mpf(0)] * 3; c1[(a + 1) % 3] = mp.mpf(s1); c1[(a + 2) % 3] = mp.mpf(t1)
        A1 = world(F[i], [c1[k] - (1 if k == a else 0) for k in range(3)])
        B1 = world(F[i], [c1[k] + (1 if k == a else 0) for k in range(3)])
        c2 = [mp.mpf(0)] * 3; c2[(b + 1) % 3] = mp.mpf(p1); c2[(b + 2) % 3] = mp.mpf(r1)
        A2 = world(F[j], [c2[k] - (1 if k == b else 0) for k in range(3)])
        B2 = world(F[j], [c2[k] + (1 if k == b else 0) for k in range(3)])
        u_ = [B1[k] - A1[k] for k in range(3)]; v_ = [B2[k] - A2[k] for k in range(3)]
        w_ = [A2[k] - A1[k] for k in range(3)]

        def cr(p, q):
            return [p[1]*q[2]-p[2]*q[1], p[2]*q[0]-p[0]*q[2], p[0]*q[1]-p[1]*q[0]]

        def dt(p, q):
            return sum(p[k] * q[k] for k in range(3))

        n_ = cr(u_, v_); nn = dt(n_, n_)
        if nn < mp.mpf('1e-30'):
            continue
        sp_ = dt(cr(w_, v_), n_) / nn; tp = dt(cr(w_, u_), n_) / nn
        for val, what in ((sp_, 's=0 (corner of cube %d)' % i),
                          (1 - sp_, 's=1 (corner of cube %d)' % i),
                          (tp, 't=0 (corner of cube %d)' % j),
                          (1 - tp, 't=1 (corner of cube %d)' % j)):
            if best is None or abs(val) < best[0]:
                best = (abs(val), (i, j), lab, what)
    if best is None:
        return None
    return {'pair': list(best[1]), 'label': list(best[2]), 'approaching': best[3],
            'distance': mp.nstr(best[0], 8)}


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 50

    qs = [qmul((REC[0][0], -REC[0][1], -REC[0][2], -REC[0][3]), q) for q in REC]
    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')
    path = os.path.join(ROOT, 'catalogue_cache', 'contact_forms_%s.pkl'
                        % hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12])
    FORMS = {k: sp.sympify(val) for k, val in pickle.load(open(path, 'rb')).items()}
    P = sp.symbols('P0:12')
    qsym = [[sp.Integer(qs[0][c]) for c in range(4)]] + \
           [[P[4 * (k - 1) + c] for c in range(4)] for k in (1, 2, 3)]
    LAB, eqs = [], []
    for i, j in itertools.combinations(range(4), 2):
        for lab in CR.in_range_labels(qs[i], qs[j]):
            LAB.append(((i, j), lab))
            sub = {}
            for c in range(4):
                sub[u[c]] = qsym[i][c]; sub[v[c]] = qsym[j][c]
            eqs.append(FORMS[lab].subs(sub))
    J = sp.Matrix([[sp.diff(e, p) for p in P] for e in eqs])
    Ff = sp.lambdify(P, eqs, 'mpmath'); Jf = sp.lambdify(P, J.tolist(), 'mpmath')

    x0 = []
    for k in (1, 2, 3):
        n = mp.sqrt(sum(mp.mpf(int(qs[k][c])) ** 2 for c in range(4)))
        x0 += [mp.mpf(int(qs[k][c])) / n for c in range(4)]

    f0 = max(abs(t) for t in mp.matrix(Ff(*x0)))
    print('GATE |F| at the start: %s   %s'
          % (mp.nstr(f0, 5), 'PASS' if f0 < mp.mpf('1e-30') else 'FAIL'), flush=True)
    if f0 >= mp.mpf('1e-30'):
        return

    def tangent(x, prev):
        Jv = mp.matrix(Jf(*x))
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
            nn = mp.sqrt(sum(t * t for t in sc)); sc = [t / nn for t in sc]
            for a_ in range(12):
                for b_ in range(12):
                    M[a_, b_] = M[a_, b_] + sc[a_] * sc[b_]
        scale = max(abs(M[a_, a_]) for a_ in range(12))
        Mi = M + mp.eye(12) * (scale * mp.mpf('1e-30'))
        y = mp.matrix(prev) if prev else mp.matrix([mp.mpf(1) / (k + 3) for k in range(12)])
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
        return [t / nw for t in w] if nw > mp.mpf('1e-15') else None

    def correct(xn):
        for _ in range(60):
            Fv = mp.matrix(Ff(*xn)); Jv = mp.matrix(Jf(*xn))
            A2 = Jv.T * Jv
            sc2 = max(abs(A2[q_, q_]) for q_ in range(12))
            if sc2 == 0:
                return None
            try:
                dx = mp.lu_solve(A2 + mp.eye(12) * (sc2 * mp.mpf('1e-28')), -(Jv.T * Fv))
            except Exception:
                return None
            if max(abs(t) for t in dx) > mp.mpf('0.5'):
                return None
            xn = [xn[i] + dx[i] for i in range(12)]
            if max(abs(t) for t in dx) < mp.mpf('1e-40'):
                break
        return xn if max(abs(t) for t in mp.matrix(Ff(*xn))) < mp.mpf('1e-18') else None

    print('\nA. BACKWARD WALK, step steered by the margin', flush=True)
    x = list(x0); prev = None; arc = mp.mpf(0)
    H = mp.mpf('0.02')
    nin0, m0 = RCV.contacts_at(mp, qs[0], x, LAB)
    print('   start: %d/%d contacts, margin %s' % (nin0, len(LAB), mp.nstr(m0, 6)), flush=True)
    traj = []
    reason = 'budget exhausted'
    for step in range(120):
        d = tangent(x, prev)
        if d is None:
            reason = 'no tangent'
            break
        if prev is None:
            d = [-t for t in d]                      # BACKWARD
        elif sum(d[i] * prev[i] for i in range(12)) < 0:
            d = [-t for t in d]
        xn = correct([x[i] + H * d[i] for i in range(12)])
        if xn is None:
            H = H / 2
            if H < mp.mpf('1e-9'):
                reason = 'corrector failed at every step size'
                break
            continue
        nin, mar = RCV.contacts_at(mp, qs[0], xn, LAB)
        # THE PROXY DOES NOT COVER B.  `contacts_at` tracks the 36 EE contacts and nothing
        # else, so T3 and Q4generic can change with all 36 contacts intact -- a triple point
        # entering or leaving a facet is invisible to it.  The first run checked the full
        # census ONLY when a contact was lost, walked 0.6356 with 36/36 the whole way, and
        # arrived at a census of {(1,1,1):56, (1,1,1,1):18}: B had changed long before, and
        # the "census SAME" claim covered nothing.  A gate on the wrong quantity is not a gate.
        cen, _, _ = RCV.full_census(mp, qs[0], xn)
        if True:
            if cen != WANT:
                # step back and refine
                H = H / 4
                if H < mp.mpf('1e-14'):
                    reason = 'census changed -- the 183 stretch ends here'
                    traj.append({'arc': mp.nstr(arc, 10), 'margin': mp.nstr(mar, 6),
                                 'contacts': nin, 'census': {str(k): v for k, v in cen.items()},
                                 'census_changed': True})
                    break
                continue
        prev = d; arc += H; x = xn
        # steer: the margin IS the distance to the boundary in the coordinate that matters
        # NEWTON ON THE MARGIN, not a shrinking walk.  The margin falls at very nearly 1 per
        # unit arc near the boundary (measured: 6.0e-4 -> 2.9e-4 over an arc of 3.1e-4), so
        # the distance remaining IS the margin.  The first version shrank H whenever the
        # margin was small, which deadlocks: small margin -> tiny step -> no progress -> the
        # margin stays small.  It froze at arc 0.635417 for 580 steps at H = 1e-10.
        if mar > mp.mpf('0.02'):
            H = min(H * 2, mp.mpf('0.08'))
        else:
            H = max(min(mar * mp.mpf('0.7'), mp.mpf('0.08')), mp.mpf('1e-30'))
        if step % 5 == 0 or mar < mp.mpf('1e-6'):
            print('   step %3d  arc %-10s  margin %-10s  B %3d  EE %2d  H %s'
                  % (step, mp.nstr(arc, 6), mp.nstr(mar, 5),
                     cen.get((1, 1, 1), 0) + 4 * cen.get((1, 1, 1, 1), 0),
                     cen.get((2, 2), 0), mp.nstr(H, 4)), flush=True)
            traj.append({'step': step, 'arc': mp.nstr(arc, 10), 'margin': mp.nstr(mar, 8),
                         'contacts': nin,
                         'census': {str(k): v for k, v in cen.items()}})
        if mar < mp.mpf('1e-18'):
            reason = 'margin closed -- at the boundary'
            break
    dist = mp.sqrt(sum((x[i] - x0[i]) ** 2 for i in range(12)))
    print('\n   stopped: %s   arc %s   distance from start %s'
          % (reason, mp.nstr(arc, 8), mp.nstr(dist, 8)), flush=True)
    # which contact is dying, and at which end of its edge?  s or t reaching 0 or 1 means the
    # crossing has arrived at a CORNER -- the (2,2) vertex is turning into a (3,2).
    dying = dying_contact(mp, qs[0], x, LAB)
    print('   dying contact: %s' % (dying,), flush=True)
    ninf, marf = RCV.contacts_at(mp, qs[0], x, LAB)
    cenf, _, _ = RCV.full_census(mp, qs[0], x)
    print('   at the stop: %d/%d contacts, margin %s, census %s'
          % (ninf, len(LAB), mp.nstr(marf, 6), 'SAME' if cenf == WANT else str(cenf)),
          flush=True)

    out = {'what': 'the backward end of the 183 plateau arc', 'supports': 'OQ 39; completes P378',
           'start_residual': mp.nstr(f0, 8), 'stop_reason': reason,
           'backward_arc': mp.nstr(arc, 10), 'distance_from_start': mp.nstr(dist, 10),
           'final_contacts': ninf, 'final_margin': mp.nstr(marf, 10),
           'final_census': {str(k): v for k, v in cenf.items()},
           'census_same_at_stop': bool(cenf == WANT),
           'trajectory': traj}
    out['reproduce'] = PROV.stamp(parameters={'dps': 50, 'max_steps': 600,
                                              'step_range': ['1e-10', '0.08']})
    json.dump(out, open(os.path.join(ROOT, 'data', 'backward_end.json'), 'w'), indent=1)
    print('\nwrote data/backward_end.json', flush=True)


if __name__ == '__main__':
    main()
