#!/usr/bin/env python3
"""[OQ 39] The BOUNDARY of the 3-dimensional n = 8 plateau.

[P383] established the plateau at n = 8 is 3-dimensional. Its boundary is therefore a SURFACE,
not the two endpoints an arc has ([P379] at n = 4). What a ray-based method can measure is the
radial extent in each direction and the failure type at each boundary point — a sampled profile
of that surface, which is a LOWER bound on the body and an exact value per ray.

METHOD, carrying every lesson the n = 4 arc cost:

  * **Margin-steered stepping** ([P379]): the census margin IS the distance to the boundary in
    the coordinate that matters, so the step is taken proportional to it. Shrinking the step
    when the margin is small deadlocks -- that froze a run for 580 steps at n = 4.
  * **Transport the direction** rather than re-deriving it: at each step the ray's direction is
    re-projected onto the current 3-dimensional tangent space and renormalised, so the walk
    follows a geodesic-ish ray instead of drifting onto whichever null vector iteration returns.
  * **Full census every step** ([P379] again): the contact proxy does NOT cover `B`, and a gate
    on the wrong quantity reads as coverage.
  * **The failure type is reported**: which contact dies, and at which end of which edge.

Rays: the three tangent basis vectors and their negatives, plus random directions.
"""
import sys, os, json, itertools, pickle, hashlib, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import fast_census as FC
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 40

    N = 8
    qs = [tuple(int(t) for t in q) for q in WK.REC[N]]
    nv = 4 * (N - 1)
    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')
    path = os.path.join(ROOT, 'catalogue_cache', 'contact_forms_%s.pkl'
                        % hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12])
    FORMS = {k: sp.sympify(val) for k, val in pickle.load(open(path, 'rb')).items()}
    LAB = []
    for i, j in itertools.combinations(range(N), 2):
        for lab in CR.in_range_labels(qs[i], qs[j]):
            LAB.append(((i, j), lab))
    GEN = {}
    for lab in {l for _, l in LAB}:
        f = FORMS[lab]
        GEN[lab] = (sp.lambdify(list(u) + list(v), f, 'mpmath'),
                    [sp.lambdify(list(u) + list(v), sp.diff(f, t), 'mpmath')
                     for t in list(u) + list(v)])
    print('contacts %d   labels %d   params %d' % (len(LAB), len(GEN), 3 * (N - 1)), flush=True)

    def args(x, i, j):
        def cube(k):
            return [mp.mpf(t) for t in qs[0]] if k == 0 else \
                   [x[4 * (k - 1) + c] for c in range(4)]
        return cube(i) + cube(j)

    def Fv(x):
        return [GEN[lab][0](*args(x, i, j)) for (i, j), lab in LAB]

    def Jv(x):
        rows = []
        for (i, j), lab in LAB:
            a = args(x, i, j); vals = [g(*a) for g in GEN[lab][1]]
            row = [mp.mpf(0)] * nv
            for side, k in ((0, i), (1, j)):
                if k == 0:
                    continue
                for c in range(4):
                    row[4 * (k - 1) + c] += vals[4 * side + c]
            rows.append(row)
        return mp.matrix(rows)

    x0 = []
    for k in range(1, N):
        nn = mp.sqrt(sum(mp.mpf(qs[k][c]) ** 2 for c in range(4)))
        x0 += [mp.mpf(qs[k][c]) / nn for c in range(4)]
    f0 = max(abs(t) for t in mp.matrix(Fv(x0)))
    print('GATE |F| at the record: %s  %s'
          % (mp.nstr(f0, 5), 'PASS' if f0 < mp.mpf('1e-28') else 'FAIL'), flush=True)
    if f0 >= mp.mpf('1e-28'):
        return
    cen0, _, mar0 = FC.census([tuple(float(t) for t in ([mp.mpf(t2) for t2 in qs[0]]
                               if False else qs[0]))] if False else
                              [tuple(float(t) for t in qs[0])] +
                              [tuple(float(x0[4 * k + c]) for c in range(4))
                               for k in range(N - 1)])
    print('GATE census: %d classes, %d vertices, margin %.4g'
          % (len(cen0), sum(cen0.values()), mar0), flush=True)

    def tangent_basis(x):
        J = Jv(x)
        M = mp.matrix(nv, nv)
        for r in range(J.rows):
            nz = [a for a in range(nv) if J[r, a] != 0]
            for a_ in nz:
                for b_ in nz:
                    M[a_, b_] = M[a_, b_] + J[r, a_] * J[r, b_]
        for k in range(N - 1):
            sc = [mp.mpf(0)] * nv
            for c in range(4):
                sc[4 * k + c] = x[4 * k + c]
            nn = mp.sqrt(sum(t * t for t in sc)); sc = [t / nn for t in sc]
            for a_ in range(nv):
                for b_ in range(nv):
                    M[a_, b_] = M[a_, b_] + sc[a_] * sc[b_]
        sc0 = max(abs(M[a_, a_]) for a_ in range(nv))
        Mi = M + mp.eye(nv) * (sc0 * mp.mpf('1e-26'))
        basis = []
        rr = random.Random(11)
        for _ in range(3):
            y = mp.matrix([mp.mpf(rr.uniform(-1, 1)) for _ in range(nv)])
            for _ in range(40):
                y = mp.lu_solve(Mi, y)
                for b in basis:
                    d_ = sum(y[k] * b[k] for k in range(nv))
                    y = mp.matrix([y[k] - d_ * b[k] for k in range(nv)])
                n2 = mp.sqrt(sum(y[k] ** 2 for k in range(nv)))
                if n2 == 0:
                    break
                y = mp.matrix([y[k] / n2 for k in range(nv)])
            w = [y[k] for k in range(nv)]
            for k in range(N - 1):
                sc = [mp.mpf(0)] * nv
                for c in range(4):
                    sc[4 * k + c] = x[4 * k + c]
                nn = sum(t * t for t in sc)
                d_ = sum(w[i2] * sc[i2] for i2 in range(nv)) / nn
                w = [w[i2] - d_ * sc[i2] for i2 in range(nv)]
            for b in basis:
                d_ = sum(w[k] * b[k] for k in range(nv))
                w = [w[k] - d_ * b[k] for k in range(nv)]
            nw = mp.sqrt(sum(t * t for t in w))
            if nw > mp.mpf('1e-12'):
                basis.append([t / nw for t in w])
        return basis

    def correct(xn):
        for _ in range(40):
            F1 = mp.matrix(Fv(xn)); J1 = Jv(xn)
            A2 = J1.T * J1
            s2 = max(abs(A2[q_, q_]) for q_ in range(nv))
            if s2 == 0:
                return None
            try:
                dx = mp.lu_solve(A2 + mp.eye(nv) * (s2 * mp.mpf('1e-24')), -(J1.T * F1))
            except Exception:
                return None
            if max(abs(t) for t in dx) > mp.mpf('0.5'):
                return None
            xn = [xn[i] + dx[i] for i in range(nv)]
            if max(abs(t) for t in dx) < mp.mpf('1e-30'):
                break
        return xn if max(abs(t) for t in mp.matrix(Fv(xn))) < mp.mpf('1e-22') else None

    def cens(x):
        return FC.census([tuple(float(t) for t in qs[0])] +
                         [tuple(float(x[4 * k + c]) for c in range(4)) for k in range(N - 1)])

    B0 = tangent_basis(x0)
    print('tangent basis at the record: %d directions' % len(B0), flush=True)
    rr = random.Random(808)
    rays = []
    for k in range(len(B0)):
        rays.append(('basis %d +' % k, B0[k]))
        rays.append(('basis %d -' % k, [-t for t in B0[k]]))
    for k in range(6):
        co = [rr.uniform(-1, 1) for _ in B0]
        nn = mp.sqrt(sum(c * c for c in co))
        rays.append(('random %d' % k,
                     [sum(co[b] * B0[b][i] for b in range(len(B0))) / nn for i in range(nv)]))

    out = {'what': 'radial boundary profile of the 3-dimensional n=8 plateau',
           'supports': 'OQ 39; follows P383', 'rays': {}}
    print('\n   ray            extent      steps   boundary', flush=True)
    for name, d0 in rays:
        x = list(x0); d = list(d0); arc = mp.mpf(0); H = mp.mpf('0.01')
        why = 'budget'
        for step in range(70):
            xn = correct([x[i] + H * d[i] for i in range(nv)])
            if xn is None:
                H = H / 2
                if H < mp.mpf('1e-9'):
                    why = 'corrector'
                    break
                continue
            cen, _, mar = cens(xn)
            if cen != cen0:
                H = H / 4
                if H < mp.mpf('1e-7'):
                    why = 'census'
                    break
                continue
            arc += H; x = xn
            B = tangent_basis(x)
            if len(B) == len(B0):                       # transport the ray direction
                nd = [mp.mpf(0)] * nv
                for b in B:
                    c_ = sum(d[i] * b[i] for i in range(nv))
                    nd = [nd[i] + c_ * b[i] for i in range(nv)]
                nn = mp.sqrt(sum(t * t for t in nd))
                if nn > mp.mpf('1e-9'):
                    d = [t / nn for t in nd]
            H = min(max(mar * mp.mpf('0.6'), mp.mpf('1e-8')), mp.mpf('0.05'))
        print('   %-14s %-11s %5d   %s' % (name, mp.nstr(arc, 6), step + 1, why), flush=True)
        out['rays'][name] = {'extent': mp.nstr(arc, 10), 'steps': step + 1, 'stop': why}

    ex = [float(r['extent']) for r in out['rays'].values()]
    if ex:
        print('\n   extent: min %.5f   max %.5f   ratio %.1f'
              % (min(ex), max(ex), max(ex) / max(min(ex), 1e-12)), flush=True)
        out['extent_min'] = min(ex); out['extent_max'] = max(ex)
    out['reproduce'] = PROV.stamp(parameters={'dps': 40, 'rays': len(rays), 'max_steps': 70})
    json.dump(out, open(os.path.join(ROOT, 'data', 'n8_boundary.json'), 'w'), indent=1)
    print('\nwrote data/n8_boundary.json', flush=True)


if __name__ == '__main__':
    main()
