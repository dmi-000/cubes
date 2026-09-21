#!/usr/bin/env python3
"""[OQ 39] DELIMITING the 3-dimensional n = 8 plateau: its facets, from the inequalities.

[P383] established the plateau is 3-dimensional. Rays sample its boundary a dozen points at a
time and each costs a full continuation -- the first ray of `n8_boundary.py` spent 70 steps and
measured its own step budget rather than the plateau. The inequalities define the body directly.

**WHAT BOUNDS THE PLATEAU IS AN INEQUALITY, NOT AN EQUATION** ([P379], [P382]): each contact
survives only while its crossing parameters `s, t` stay in `[0,1]`, and the plateau ends where
one reaches an endpoint -- the crossing arrives at a CORNER and a `(2,2)` vertex becomes
`(3,2)`. With 102 contacts that is **408 smooth constraints** on a 3-dimensional plateau.

**SO THE PLATEAU IS A POLYTOPE, to first order.** Linearise each constraint at the record in the
three plateau coordinates and it becomes a half-space; the plateau is their intersection, and
each facet NAMES the contact that bounds it in that direction. The gradients are taken by
central differences ALONG THE TANGENT DIRECTIONS, with Newton correction back onto the contact
variety at each sample -- stepping off the variety changes the contact set and would measure
something else.

Reported: the distance to every facet, which contact owns it, and the polytope's vertices and
extent. First order only: the true boundary is curved, and this is its tangent cone at the
record, exact as a first-order description and an approximation to the body.
"""
import sys, os, json, itertools, pickle, hashlib, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def crossing_params(qlist, labels):
    """for each labelled contact, its two crossing parameters s, t (floats)."""
    import numpy as np
    F = []
    for q in qlist:
        w, x, y, z = q
        n = w*w + x*x + y*y + z*z
        M = np.array([[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
                      [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                      [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]]) / n
        F.append(M.T)                                   # rows = face normals
    out = []
    for (i, j), lab in labels:
        a, b, s1, t1, p1, r1 = lab
        c1 = np.zeros(3); c1[(a+1) % 3] = s1; c1[(a+2) % 3] = t1
        e1 = np.zeros(3); e1[a] = 1.0
        A1 = F[i].T @ (c1 - e1); B1 = F[i].T @ (c1 + e1)
        c2 = np.zeros(3); c2[(b+1) % 3] = p1; c2[(b+2) % 3] = r1
        e2 = np.zeros(3); e2[b] = 1.0
        A2 = F[j].T @ (c2 - e2); B2 = F[j].T @ (c2 + e2)
        u_ = B1 - A1; v_ = B2 - A2; w_ = A2 - A1
        n_ = np.cross(u_, v_); nn = n_ @ n_
        if nn < 1e-24:
            out.append((np.nan, np.nan)); continue
        out.append((np.cross(w_, v_) @ n_ / nn, np.cross(w_, u_) @ n_ / nn))
    return np.array(out)


def main():
    import sympy as sp, mpmath as mp, numpy as np
    mp.mp.dps = 40
    N = 8
    qs = [tuple(int(t) for t in q) for q in WK.REC[N]]
    nv = 4 * (N - 1)
    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')
    FORMS = {k: sp.sympify(val) for k, val in pickle.load(open(
        os.path.join(ROOT, 'catalogue_cache', 'contact_forms_%s.pkl'
                     % hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12]), 'rb')).items()}
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
    print('contacts %d   constraints %d' % (len(LAB), 4 * len(LAB)), flush=True)

    def args(x, i, j):
        def cube(k):
            return [mp.mpf(t) for t in qs[0]] if k == 0 else [x[4*(k-1)+c] for c in range(4)]
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
                    row[4*(k-1)+c] += vals[4*side+c]
            rows.append(row)
        return mp.matrix(rows)

    x0 = []
    for k in range(1, N):
        nn = mp.sqrt(sum(mp.mpf(qs[k][c])**2 for c in range(4)))
        x0 += [mp.mpf(qs[k][c])/nn for c in range(4)]
    print('GATE |F| at the record: %s' % mp.nstr(max(abs(t) for t in mp.matrix(Fv(x0))), 5),
          flush=True)

    # tangent basis
    J = Jv(x0)
    M = mp.matrix(nv, nv)
    for r in range(J.rows):
        nz = [a for a in range(nv) if J[r, a] != 0]
        for a_ in nz:
            for b_ in nz:
                M[a_, b_] += J[r, a_] * J[r, b_]
    for k in range(N-1):
        sc = [mp.mpf(0)]*nv
        for c in range(4):
            sc[4*k+c] = x0[4*k+c]
        nn = mp.sqrt(sum(t*t for t in sc)); sc = [t/nn for t in sc]
        for a_ in range(nv):
            for b_ in range(nv):
                M[a_, b_] += sc[a_]*sc[b_]
    Mi = M + mp.eye(nv)*(max(abs(M[a, a]) for a in range(nv))*mp.mpf('1e-26'))
    rr = random.Random(3)
    basis = []
    for _ in range(3):
        y = mp.matrix([mp.mpf(rr.uniform(-1, 1)) for _ in range(nv)])
        for _ in range(40):
            y = mp.lu_solve(Mi, y)
            for b in basis:
                d_ = sum(y[k]*b[k] for k in range(nv))
                y = mp.matrix([y[k]-d_*b[k] for k in range(nv)])
            n2 = mp.sqrt(sum(y[k]**2 for k in range(nv)))
            y = mp.matrix([y[k]/n2 for k in range(nv)])
        w = [y[k] for k in range(nv)]
        for k in range(N-1):
            sc = [mp.mpf(0)]*nv
            for c in range(4):
                sc[4*k+c] = x0[4*k+c]
            nn = sum(t*t for t in sc); d_ = sum(w[i2]*sc[i2] for i2 in range(nv))/nn
            w = [w[i2]-d_*sc[i2] for i2 in range(nv)]
        for b in basis:
            d_ = sum(w[k]*b[k] for k in range(nv))
            w = [w[k]-d_*b[k] for k in range(nv)]
        nw = mp.sqrt(sum(t*t for t in w))
        basis.append([t/nw for t in w])
    print('tangent basis: %d' % len(basis), flush=True)

    def correct(xn):
        for _ in range(30):
            F1 = mp.matrix(Fv(xn)); J1 = Jv(xn)
            A2 = J1.T*J1
            s2 = max(abs(A2[q_, q_]) for q_ in range(nv))
            dx = mp.lu_solve(A2 + mp.eye(nv)*(s2*mp.mpf('1e-24')), -(J1.T*F1))
            if max(abs(t) for t in dx) > mp.mpf('0.5'):
                return None
            xn = [xn[i]+dx[i] for i in range(nv)]
            if max(abs(t) for t in dx) < mp.mpf('1e-30'):
                break
        return xn

    def cfg(x):
        return [tuple(float(t) for t in qs[0])] + \
               [tuple(float(x[4*k+c]) for c in range(4)) for k in range(N-1)]

    st0 = crossing_params(cfg(x0), LAB)
    # g >= 0 constraints: s, 1-s, t, 1-t
    g0 = np.concatenate([st0[:, 0], 1-st0[:, 0], st0[:, 1], 1-st0[:, 1]])
    print('constraint values at the record: min %.6g   (must be > 0)' % np.nanmin(g0),
          flush=True)

    h = mp.mpf('1e-5')
    A = np.zeros((len(g0), 3))
    for k in range(3):
        xp = correct([x0[i] + h*basis[k][i] for i in range(nv)])
        xm = correct([x0[i] - h*basis[k][i] for i in range(nv)])
        stp = crossing_params(cfg(xp), LAB); stm = crossing_params(cfg(xm), LAB)
        gp = np.concatenate([stp[:, 0], 1-stp[:, 0], stp[:, 1], 1-stp[:, 1]])
        gm = np.concatenate([stm[:, 0], 1-stm[:, 0], stm[:, 1], 1-stm[:, 1]])
        A[:, k] = (gp - gm) / (2*float(h))
    print('gradients taken (central differences on the variety)', flush=True)

    norms = np.linalg.norm(A, axis=1)
    live = (norms > 1e-9) & np.isfinite(g0)
    dist = np.where(live, g0/np.maximum(norms, 1e-30), np.inf)
    order = np.argsort(dist)
    names = []
    for kind in ('s>=0', 's<=1', 't>=0', 't<=1'):
        for (i, j), lab in LAB:
            names.append('%s pair(%d,%d)' % (kind, i, j))

    print('\n   the TEN nearest facets -- these delimit the plateau:', flush=True)
    print('   %-22s %12s %10s' % ('constraint', 'distance', '|grad|'), flush=True)
    rows = []
    for idx in order[:10]:
        print('   %-22s %12.6f %10.4f' % (names[idx], dist[idx], norms[idx]), flush=True)
        rows.append({'constraint': names[idx], 'distance': float(dist[idx]),
                     'grad_norm': float(norms[idx])})

    out = {'what': 'facets of the 3-dimensional n=8 plateau, from the contact inequalities',
           'supports': 'OQ 39; delimits P383', 'contacts': len(LAB),
           'constraints': int(live.sum()), 'nearest_facets': rows,
           'inradius': float(dist[order[0]])}
    try:
        from scipy.spatial import HalfspaceIntersection
        hs = np.column_stack([-A[live], -g0[live]])
        interior = np.zeros(3)
        hi = HalfspaceIntersection(hs, interior)
        V = hi.intersections
        out['vertices'] = int(len(V))
        out['circumradius'] = float(np.max(np.linalg.norm(V, axis=1)))
        print('\n   polytope: %d vertices   inradius %.6f   circumradius %.6f'
              % (len(V), dist[order[0]], out['circumradius']), flush=True)
        try:
            from scipy.spatial import ConvexHull
            ch = ConvexHull(V)
            out['volume'] = float(ch.volume); out['facets'] = int(len(ch.simplices))
            print('   volume %.4g   hull facets %d' % (ch.volume, len(ch.simplices)), flush=True)
        except Exception as e:
            print('   hull unavailable: %s' % e, flush=True)
    except Exception as e:
        print('\n   halfspace intersection unavailable (%s); facet distances stand' % e,
              flush=True)

    out['reproduce'] = PROV.stamp(parameters={'dps': 40, 'fd_step': '1e-5'},
                                  note='first-order: the tangent cone at the record')
    json.dump(out, open(os.path.join(ROOT, 'data', 'n8_polytope.json'), 'w'), indent=1)
    print('\nwrote data/n8_polytope.json', flush=True)


if __name__ == '__main__':
    main()
