#!/usr/bin/env python3
"""[OQ 39] The FULL extent of the 183 plateau: both directions, endpoints bisected.

[P378] followed the curve one way from the record and found the census preserved to arc 0.04,
breaking before 0.06 where 12 of the 36 contacts leave their segments.  A curve has two
directions, and the plateau is the union of both, so half of it was never measured.

This walks both ways and bisects each boundary.  What bounds the arc is a CONTACT LEAVING ITS
SEGMENT -- an inequality, not an equation -- so the endpoint is where some crossing parameter
reaches 0 or 1, and bisection on that is exact in the limit.

Reported as: the arc length each way, the total, and which contacts die at each end.
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
    print('contacts: %d' % len(LAB), flush=True)

    x0 = []
    for k in (1, 2, 3):
        n = mp.sqrt(sum(mp.mpf(int(qs[k][c])) ** 2 for c in range(4)))
        x0 += [mp.mpf(int(qs[k][c])) / n for c in range(4)]

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

    def walk(sign, hstep, nsteps):
        """march until the census changes; return (last good arc, last good x, x after)"""
        x = list(x0); prev = None; arc = mp.mpf(0)
        lastgood = (mp.mpf(0), list(x0))
        for _ in range(nsteps):
            d = tangent(x, prev)
            if d is None:
                return lastgood, None, 'no tangent'
            if prev is not None and sum(d[i] * prev[i] for i in range(12)) < 0:
                d = [-t for t in d]
            elif prev is None:
                d = [sign * t for t in d]
            prev = d
            xn = correct([x[i] + hstep * d[i] for i in range(12)])
            if xn is None:
                return lastgood, None, 'corrector failed'
            arc += hstep
            # CHEAP PROXY, verified against the expensive check at every boundary.  What ends
            # the arc is contacts leaving their segments, and `contacts_at` tests exactly that
            # in 36 segment intersections instead of ~2 000 plane triples.  The full census is
            # run only when the proxy fires, so a boundary is never declared on the proxy
            # alone.
            nin, _ = RCV.contacts_at(mp, qs[0], xn, LAB)
            if nin != len(LAB):
                cen, _, _ = RCV.full_census(mp, qs[0], xn)
                if cen != WANT:
                    return lastgood, (arc, xn, cen), 'census changed'
            lastgood = (arc, xn)
            x = xn
        return lastgood, None, 'budget exhausted'

    out = {'what': 'full extent of the 183 plateau arc', 'supports': 'OQ 39; completes P378',
           'directions': {}}
    # is the walk closing into a loop, or drifting away?  distance back to the start, reported
    # alongside the arc, so "budget exhausted" can be told apart from "went round".
    def dist_to_start(x):
        return mp.sqrt(sum((x[i] - x0[i]) ** 2 for i in range(12)))
    out['dist_to_start_note'] = 'euclidean in the 12 unit-quaternion coordinates'
    H = mp.mpf('0.01')
    for sign, name in ((1, 'forward'), (-1, 'backward')):
        (agood, xgood), bad, why = walk(sign, H, 30 if sign > 0 else 900)
        dd = dist_to_start(xgood)
        print('   %-9s last good arc %s   (%s)   distance from start %s'
              % (name, mp.nstr(agood, 6), why, mp.nstr(dd, 6)), flush=True)
        rec = {'last_good_arc': mp.nstr(agood, 10), 'stop_reason': why,
               'distance_from_start': mp.nstr(dd, 10)}
        if bad:
            abad, xbad, cen = bad
            lo, hi = agood, abad
            # bisect on arc length, re-walking from the record each time
            for _ in range(8):
                mid = (lo + hi) / 2
                steps = int(mid / H) + 1
                hh = mid / steps
                (am, xm), bb, _w = walk(sign, hh, steps)
                if bb is None and am >= mid - hh / 2:
                    lo = mid
                else:
                    hi = mid
            print('     boundary bracketed in [%s, %s]   census beyond: %s'
                  % (mp.nstr(lo, 8), mp.nstr(hi, 8), cen), flush=True)
            rec.update({'boundary_lo': mp.nstr(lo, 10), 'boundary_hi': mp.nstr(hi, 10),
                        'census_beyond': {str(k): v for k, v in cen.items()}})
        out['directions'][name] = rec

    f = out['directions'].get('forward', {}); b = out['directions'].get('backward', {})
    if 'boundary_lo' in f and 'boundary_lo' in b:
        tot = mp.mpf(f['boundary_lo']) + mp.mpf(b['boundary_lo'])
        print('\n   TOTAL plateau arc length (lower bound): %s' % mp.nstr(tot, 8), flush=True)
        out['total_arc_lower_bound'] = mp.nstr(tot, 10)

    out['reproduce'] = PROV.stamp(parameters={'dps': 50, 'step': '0.01', 'bisections': 8})
    json.dump(out, open(os.path.join(ROOT, 'data', 'plateau_arc.json'), 'w'), indent=1)
    print('\nwrote data/plateau_arc.json', flush=True)


if __name__ == '__main__':
    main()
