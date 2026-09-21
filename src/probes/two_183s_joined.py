#!/usr/bin/env python3
"""[OQ 39] Are the two 183 classes two points on ONE arc?  [P136]'s prediction, tested.

[P136] found the two 183 classes share 88 wall conditions cutting a 1-dimensional locus at both,
and predicted a curve through the pair.  [P379] measured the arc: 0.0517 forward, 0.6356
backward.  The symmetry-minimal distance between the two classes -- minimised over the residual
global octahedral rotation, the per-cube cosets, and the labelling -- is **0.06504**, inside the
backward reach and outside the forward one.

So the prediction is now falsifiable in one walk: go backward and watch that distance.  If it
falls to zero at some arc length, the two "isolated, non-congruent" maximisers of [P133] are two
points on a single constant-count arc.  If it bottoms out well above zero, they are not joined
by THIS curve and [P136]'s locus is a different object.

The distance is gauge-free by construction: each cube is compared as a COSET `q*O`, minimised
over the 24 right multiplications, and the whole configuration over the 24 global rotations
fixing cube 0's cube and the 6 relabellings.
"""
import sys, os, json, itertools, math, pickle, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import record_curve as RCV
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
REC = [tuple(q) for q in WK.REC[4]]
SECOND = [tuple(q) for q in WK.NAMED['n4_183']]
WANT = {(1, 1, 1): 128, (1, 2): 24, (2, 2): 36, (3, 3): 6}


def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)


def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])


def unit(q):
    n = math.sqrt(sum(t * t for t in q))
    return tuple(t / n for t in q)


def octahedral():
    out = [tuple(1.0 * s if i == k else 0.0 for i in range(4))
           for k in range(4) for s in (1, -1)]
    for k, l in itertools.combinations(range(4), 2):
        for s1 in (1, -1):
            for s2 in (1, -1):
                v = [0.0] * 4; v[k] = s1 / math.sqrt(2); v[l] = s2 / math.sqrt(2)
                out.append(tuple(v))
    for s in itertools.product((1, -1), repeat=4):
        out.append(tuple(x / 2.0 for x in s))
    uniq = []
    for q in out:
        if not any(all(abs(q[i] - r[i]) < 1e-9 for i in range(4)) or
                   all(abs(q[i] + r[i]) < 1e-9 for i in range(4)) for r in uniq):
            uniq.append(q)
    return uniq


OCT = octahedral()


def dq(a, b):
    return min(math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(4))),
               math.sqrt(sum((a[i] + b[i]) ** 2 for i in range(4))))


def sym_distance(cfg, target):
    """minimal distance over global rotation, per-cube cosets and relabelling"""
    best = 1e9
    for g in OCT:
        Ag = [unit(qmul(g, q)) for q in cfg]
        for perm in itertools.permutations([1, 2, 3]):
            tot = 0.0
            for idx, k in enumerate(perm, start=1):
                m = min(dq(unit(qmul(Ag[idx], u)), target[k]) for u in OCT)
                tot += m * m
            best = min(best, math.sqrt(tot))
    return best


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 50

    qs = [qmul(qconj(REC[0]), q) for q in REC]
    tgt = [unit(q) for q in (qmul(qconj(SECOND[0]), q) for q in SECOND)]
    d0 = sym_distance([unit(tuple(float(t) for t in q)) for q in qs], tgt)
    print('symmetry-minimal distance, record -> second class: %.8f' % d0, flush=True)

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
    print('GATE |F| at the record: %s  %s'
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

    # BOTH DIRECTIONS.  The backward walk moved monotonically AWAY (0.065 -> 0.301 over arc
    # 0.244, slope ~1), so the second class lies forward -- which is the SHORT end, 0.0517.
    print('\nWATCHING THE DISTANCE IN BOTH DIRECTIONS', flush=True)
    results = {}
    for DIRN, dname in ((-1, 'backward'), (1, 'forward')):
      print('   --- %s ---' % dname, flush=True)
      x = list(x0); prev = None; arc = mp.mpf(0); H = mp.mpf('0.004')
      rows = []; best = (d0, mp.mpf(0))
      for step in range(140):
        d = tangent(x, prev)
        if d is None:
            print('     no tangent at step %d' % step, flush=True)
            break
        if prev is None:
            d = [DIRN * t for t in d]
        elif sum(d[i] * prev[i] for i in range(12)) < 0:
            d = [-t for t in d]
        xn = correct([x[i] + H * d[i] for i in range(12)])
        if xn is None:
            H = H / 2
            if H < mp.mpf('1e-9'):
                print('     corrector failed at step %d' % step, flush=True)
                break
            continue
        nin, mar = RCV.contacts_at(mp, qs[0], xn, LAB)
        # The census along THIS curve was verified at every step in [P379]; re-verifying it
        # here would cost ~2 000 plane triples per step for a question about DISTANCE.  So it
        # is a periodic spot-check plus the contact count, not dropped.
        if step % 8 == 0 or nin != len(LAB):
            cen, _, _ = RCV.full_census(mp, qs[0], xn)
            if cen != WANT:
                print('     census changed at arc %s -- the arc ends before the target'
                      % mp.nstr(arc, 8), flush=True)
                break
        prev = d; arc += H; x = xn
        # margin-steered step, as in [P379]: the margin is the distance to the arc's end
        if mar > mp.mpf('0.02'):
            H = min(H * 2, mp.mpf('0.06'))
        else:
            H = max(min(mar * mp.mpf('0.7'), mp.mpf('0.06')), mp.mpf('1e-20'))
        cfg = [unit(tuple(float(t) for t in qs[0]))] + \
              [unit((float(x[4 * k]), float(x[4 * k + 1]),
                     float(x[4 * k + 2]), float(x[4 * k + 3]))) for k in range(3)]
        dist = sym_distance(cfg, tgt)
        if dist < best[0]:
            best = (dist, arc)
        if step % 5 == 0 or dist < 0.02:
            print('     arc %-10s  margin %-10s  distance %.8f'
                  % (mp.nstr(arc, 6), mp.nstr(mar, 5), dist), flush=True)
        rows.append({'arc': mp.nstr(arc, 10), 'distance': '%.10f' % dist,
                     'margin': mp.nstr(mar, 8)})
        if dist < 1e-6:
            print('     *** REACHED the second class at arc %s ***'
                  % mp.nstr(arc, 8), flush=True)
            break
        if mar < mp.mpf('1e-12'):
            print('     reached the arc end at %s' % mp.nstr(arc, 8), flush=True)
            break
      print('     closest approach %.8f at arc %s   (started at %.8f)'
            % (best[0], mp.nstr(best[1], 6), d0), flush=True)
      results[dname] = {'closest': '%.10f' % best[0], 'at_arc': mp.nstr(best[1], 10),
                        'final_arc': mp.nstr(arc, 10), 'trajectory': rows}

    out = {'what': 'are the two 183 classes on one arc?', 'supports': 'OQ 39; tests P136',
           'initial_distance': '%.10f' % d0, 'directions': results,
           'joined': any(float(r['closest']) < 1e-6 for r in results.values())}
    out['reproduce'] = PROV.stamp(parameters={'dps': 50, 'step': '0.004', 'max_arc': '0.25'},
                                  note='distance minimised over global rotation, per-cube '
                                       'cosets and relabelling')
    json.dump(out, open(os.path.join(ROOT, 'data', 'two_183s_joined.json'), 'w'), indent=1)
    print('\nwrote data/two_183s_joined.json', flush=True)


if __name__ == '__main__':
    main()
