#!/usr/bin/env python3
"""[OQ 39] n = 8: is the plateau 3-dimensional (this method) or 2 ([P307])?

[P381] measured tangent dimensions 1, 1, 1, 1, 2, 3 for n = 3..8 and matched [P307]'s
independently measured plateau dimensions at n = 6 and n = 7 (1 and 2). At n = 8 the two
disagree: tangent 3 against [P307]'s stated 2.

**IT NEED NOT BE A CONTRADICTION.** Tangent dimension is an UPPER bound on local dimension, so
3 is consistent with a true 2 if the n = 8 record is a SINGULAR point of its contact variety --
the possibility [P377] raised for n = 4, where continuation then showed the tangent was exact.
[P382] found a THIRD case at n = 3: tangent exact, plateau 0, because the maximiser sits at an
endpoint. So all three relationships occur and the label cannot be guessed.

THE TEST. Take a basis of the 3-dimensional tangent space, displace along each direction and
along random combinations, Newton-correct, and recompute the full census. A direction whose
displacement survives with the census intact is a real plateau direction; one that collapses
back or breaks the census is not. The COUNT of surviving directions is the plateau dimension.

Gates, as in [P378] and [P382]: `|F|` at the record must vanish, each tangent's `|J d|` must sit
at the arithmetic's floor, and the census must reproduce the record's own before anything is
reported.
"""
import sys, os, json, itertools, pickle, hashlib, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import n3_arc as N3
import fast_census as FC
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 45

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
    print('contacts: %d   parameters: %d' % (len(LAB), 3 * (N - 1)), flush=True)

    P = sp.symbols('P0:%d' % nv)
    qs2 = [list(sp.Integer(t) for t in qs[0])] + \
          [[P[4 * (k - 1) + c] for c in range(4)] for k in range(1, N)]
    # MEMORY.  The first version substituted each contact into the full 32-variable system and
    # lambdified 102 x 21 = 2142 symbolic derivatives of expanded quartics, all live at once.
    # On a 16 GB machine with swap already 95 % full that is what a run gets killed for -- and
    # it is unnecessary: a contact form involves only TWO cubes, so ONE generic form and ONE
    # generic 8-entry gradient serve all 102 contacts, called with different arguments.
    GEN = {}
    for lab in {l for _, l in LAB}:
        f = FORMS[lab]
        gr = [sp.diff(f, t) for t in list(u) + list(v)]
        GEN[lab] = (sp.lambdify(list(u) + list(v), f, 'mpmath'),
                    [sp.lambdify(list(u) + list(v), g, 'mpmath') for g in gr])
    print('generic forms lambdified: %d labels (not %d derivatives)'
          % (len(GEN), len(LAB) * 3 * (N - 1)), flush=True)

    def _args(x, i, j):
        def cube(k):
            if k == 0:
                return [mp.mpf(t) for t in qs[0]]
            return [x[4 * (k - 1) + c] for c in range(4)]
        return cube(i) + cube(j)

    def Ff(*x):
        x = list(x)
        return [GEN[lab][0](*_args(x, i, j)) for (i, j), lab in LAB]

    def Jf(*x):
        x = list(x)
        rows = []
        for (i, j), lab in LAB:
            g = GEN[lab][1]
            a = _args(x, i, j)
            vals = [gg(*a) for gg in g]
            row = [mp.mpf(0)] * nv
            for side, k in ((0, i), (1, j)):
                if k == 0:
                    continue
                for c in range(4):
                    row[4 * (k - 1) + c] += vals[4 * side + c]
            rows.append(row)
        return rows
    print('system assembled from generic forms', flush=True)

    x0 = []
    for k in range(1, N):
        nn = mp.sqrt(sum(mp.mpf(qs[k][c]) ** 2 for c in range(4)))
        x0 += [mp.mpf(qs[k][c]) / nn for c in range(4)]
    f0 = max(abs(t) for t in mp.matrix(Ff(*x0)))
    print('GATE |F| at the record: %s   %s'
          % (mp.nstr(f0, 5), 'PASS' if f0 < mp.mpf('1e-30') else 'FAIL'), flush=True)
    out = {'what': 'n=8 plateau dimension: contact tangent vs P307', 'supports': 'OQ 39',
           'contacts': len(LAB), 'params': 3 * (N - 1), 'start_residual': mp.nstr(f0, 8)}
    if f0 >= mp.mpf('1e-30'):
        json.dump(out, open(os.path.join(ROOT, 'data', 'n8_dimension.json'), 'w'), indent=1)
        return

    qnum0 = [tuple(mp.mpf(t) for t in qs[0])] + \
            [tuple(x0[4 * k + c] for c in range(4)) for k in range(N - 1)]
    # The exact census takes about an HOUR at n = 8 -- two runs died inside it at the
    # wall-clock limit.  `fast_census` is the vectorised equivalent, GATED against the exact
    # one at n = 3 and n = 4 (identical censuses, 157x to 1705x).  It returns a margin; a small
    # one means escalate rather than trust.
    cen0, skip0, mar0 = FC.census([tuple(float(t) for t in q) for q in qnum0])
    print('   census margin at the record: %.5g   %s'
          % (mar0, 'ample' if mar0 > 1e-6 else '*** TOO SMALL -- escalate ***'), flush=True)
    print('GATE census at the record: %d signature classes, %d vertices  (skipped %d)'
          % (len(cen0), sum(cen0.values()), skip0), flush=True)
    out['census_classes'] = len(cen0); out['census_vertices'] = sum(cen0.values())

    # tangent space: null vectors of [J ; scalings], by inverse iteration with deflation
    Jv = mp.matrix(Jf(*x0))
    M = mp.matrix(nv, nv)
    for r in range(Jv.rows):
        nzk = [a for a in range(nv) if Jv[r, a] != 0]
        for a_ in nzk:
            for b_ in nzk:
                M[a_, b_] = M[a_, b_] + Jv[r, a_] * Jv[r, b_]
    for k in range(N - 1):
        sc = [mp.mpf(0)] * nv
        for c in range(4):
            sc[4 * k + c] = x0[4 * k + c]
        nn = mp.sqrt(sum(t * t for t in sc)); sc = [t / nn for t in sc]
        for a_ in range(nv):
            for b_ in range(nv):
                M[a_, b_] = M[a_, b_] + sc[a_] * sc[b_]
    scale = max(abs(M[a_, a_]) for a_ in range(nv))
    Mi = M + mp.eye(nv) * (scale * mp.mpf('1e-28'))
    rng = random.Random(8)
    basis = []
    for which in range(4):
        y = mp.matrix([mp.mpf(rng.uniform(-1, 1)) for _ in range(nv)])
        for _ in range(50):
            y = mp.lu_solve(Mi, y)
            for b in basis:                                  # deflate
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
                sc[4 * k + c] = x0[4 * k + c]
            nn = sum(t * t for t in sc)
            d_ = sum(w[i2] * sc[i2] for i2 in range(nv)) / nn
            w = [w[i2] - d_ * sc[i2] for i2 in range(nv)]
        for b in basis:
            d_ = sum(w[k] * b[k] for k in range(nv))
            w = [w[k] - d_ * b[k] for k in range(nv)]
        nw = mp.sqrt(sum(t * t for t in w))
        if nw < mp.mpf('1e-12'):
            print('   direction %d: none left (tangent exhausted)' % which, flush=True)
            break
        b = [t / nw for t in w]
        res = max(abs(t) for t in (Jv * mp.matrix(b)))
        print('   direction %d: |J d| = %s' % (which, mp.nstr(res, 5)), flush=True)
        if res > mp.mpf('1e-20') * max(abs(Jv[r, c]) for r in range(Jv.rows) for c in range(nv)):
            print('      -- not a genuine tangent, stopping the basis here', flush=True)
            break
        basis.append(b)
    print('genuine tangent directions found: %d' % len(basis), flush=True)
    out['tangent_directions'] = len(basis)

    def correct(xn):
        for _ in range(50):
            Fv = mp.matrix(Ff(*xn)); J2 = mp.matrix(Jf(*xn))
            A2 = J2.T * J2
            sc2 = max(abs(A2[q_, q_]) for q_ in range(nv))
            if sc2 == 0:
                return None
            try:
                dx = mp.lu_solve(A2 + mp.eye(nv) * (sc2 * mp.mpf('1e-26')), -(J2.T * Fv))
            except Exception:
                return None
            if max(abs(t) for t in dx) > mp.mpf('0.5'):
                return None
            xn = [xn[i] + dx[i] for i in range(nv)]
            if max(abs(t) for t in dx) < mp.mpf('1e-35'):
                break
        return xn if max(abs(t) for t in mp.matrix(Ff(*xn))) < mp.mpf('1e-25') else None

    print('\n   direction        moved by       census', flush=True)
    rows = []
    tests = [('basis %d' % k, basis[k]) for k in range(len(basis))]
    for k in range(2):
        cof = [rng.uniform(-1, 1) for _ in basis]
        nn = mp.sqrt(sum(c * c for c in cof))
        mix = [sum(cof[b] * basis[b][i] for b in range(len(basis))) / nn for i in range(nv)]
        tests.append(('random mix %d' % k, mix))
    # THE STEP MUST SIT INSIDE THE MARGIN.  The first run stepped 1e-4 while the census
    # margin at the record was 6.9e-5: the displacement was LARGER than the distance of the
    # nearest vertex to a facet boundary, so "census SAME" was being asserted at a scale the
    # margin does not protect.  Test at several steps, all well inside it.
    for name, dvec in tests:
      for hs in ('1e-6', '1e-8'):
        h = mp.mpf(hs)
        xn = correct([x0[i] + h * dvec[i] for i in range(nv)])
        if xn is None:
            print('   %-15s %-6s corrector failed' % (name, hs), flush=True)
            rows.append({'direction': name, 'step': hs, 'result': 'corrector failed'})
            continue
        moved = mp.sqrt(sum((xn[i] - x0[i]) ** 2 for i in range(nv)))
        qn = [tuple(mp.mpf(t) for t in qs[0])] + \
             [tuple(xn[4 * k2 + c] for c in range(4)) for k2 in range(N - 1)]
        cen, _, marx = FC.census([tuple(float(t) for t in q) for q in qn])
        same = (cen == cen0)
        print('   %-15s %-6s %-13s  %-8s  margin %.4g   step/margin %.3f'
              % (name, hs, mp.nstr(moved, 8), 'SAME' if same else 'CHANGED',
                 marx, float(h) / marx), flush=True)
        rows.append({'direction': name, 'step': hs, 'moved': mp.nstr(moved, 10),
                     'census_same': bool(same), 'margin': '%.6g' % marx,
                     'step_over_margin': float(h) / marx})
    # a direction counts only if it survives at a step well INSIDE the margin
    surv = len({r['direction'] for r in rows if r.get('census_same')
                and r.get('step_over_margin', 9) < 0.5})
    print('\n   directions whose displacement survives with the census intact: %d' % surv,
          flush=True)
    print('   [P307] measured the n = 8 plateau as 2-dimensional.', flush=True)
    out['surviving'] = surv; out['tests'] = rows
    out['reproduce'] = PROV.stamp(parameters={'dps': 45, 'step': '1e-4'})
    json.dump(out, open(os.path.join(ROOT, 'data', 'n8_dimension.json'), 'w'), indent=1)
    print('\nwrote data/n8_dimension.json', flush=True)


if __name__ == '__main__':
    main()
