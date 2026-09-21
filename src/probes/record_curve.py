#!/usr/bin/env python3
"""[OQ 39] Does the n = 4 RECORD lie on a CURVE that straight-line probes cannot see?

[P377] measured the record's edge-contact system: 36 active contacts, 18 corner-sharing
conditions **entirely implied by them**, and total rank **8** on 9 parameters — a 1-dimensional
tangent space.  [P287] concluded the 183 plateau is 0-dimensional, but its evidence is 19 682
straight-line Cayley probes and straight walks between the two 183 classes.  **A curved family
is invisible to every straight-line probe**, so the two results need not conflict.

THE TEST.  Take the kernel direction of the Jacobian at the record, step along it, and Newton-
correct back onto the contact variety.  If the corrected point satisfies all 36 contact
equations to high precision while remaining a genuine compound — contacts still IN RANGE, not
merely coplanar — the curve is real and the plateau is 1-dimensional in a sense no previous
probe could detect.  If Newton returns to the record or fails, the tangent direction is
obstructed at higher order and [P287] stands.

50-digit arithmetic, because the question is whether a displacement SURVIVES correction; a
tolerance set above the arithmetic's noise floor would answer a different question ([P334]'s
lesson, in the opposite direction).
"""
import sys, os, json, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import compound_rigidity as CR
import ee_determinantal as D
import ee_bound_refute as EB
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))




def full_census(mp, q0, x):
    """the complete signature census at a high-precision point.

    Robust where the first attempt was not: the 3x3 solve is done by explicit Cramer with a
    determinant guard instead of `mp.lu_solve` (which raised inside mpmath on a singular
    triple), and every skipped triple is COUNTED rather than silently dropped.
    Returns (census, skipped, margin)."""
    import itertools as it
    qs = [[mp.mpf(int(t)) for t in q0]] + \
         [[x[4 * k + c] for c in range(4)] for k in range(3)]

    def frame(q):
        w, xx, y, z = q
        n = w * w + xx * xx + y * y + z * z
        M = [[w*w+xx*xx-y*y-z*z, 2*(xx*y-w*z),      2*(xx*z+w*y)],
             [2*(xx*y+w*z),      w*w-xx*xx+y*y-z*z, 2*(y*z-w*xx)],
             [2*(xx*z-w*y),      2*(y*z+w*xx),      w*w-xx*xx-y*y+z*z]]
        return [[M[r][c] / n for r in range(3)] for c in range(3)]   # rows = FACE NORMALS

    F = [frame(q) for q in qs]
    planes = []
    for ci, M in enumerate(F):
        for r in range(3):
            for sg in (1, -1):
                planes.append((ci, [sg * M[r][c] for c in range(3)]))

    def det3(A):
        return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
                - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
                + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))

    TOL = mp.mpf('1e-18')
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

    sig = {}; seen = []; margin = mp.mpf(1)
    for p in pts:
        if any(max(abs(p[k] - o[k]) for k in range(3)) < TOL for o in seen):
            continue
        seen.append(p)
        # THE CONTAINMENT TRAP, and this is its fifth occurrence in the project and my first.
        # A vertex lies on the facets of its OWN cubes and may be OUTSIDE every other one --
        # a shared corner sits at distance sqrt3.  Being outside cube k means cube k
        # contributes NOTHING to the signature; it does NOT discard the vertex.  Discarding
        # them returned {(1,1,1): 44} for a compound whose T3 is 128, and the gate caught it.
        s = []
        for M in F:
            hs = [sum(M[r][c] * p[c] for c in range(3)) for r in range(3)]
            on = 0; outside = False
            for h in hs:
                m = abs(abs(h) - 1)
                if m < TOL:
                    on += 1
                else:
                    margin = min(margin, m)
                    if abs(h) > 1:
                        outside = True
                        break
            if outside:
                continue                       # this cube abstains; the vertex survives
            if on:
                s.append(on)
        if len(s) >= 2 and sum(s) >= 3:
            k = tuple(sorted(s))
            sig[k] = sig.get(k, 0) + 1
    return sig, skipped, margin


def contacts_at(mp, q0, x, labels):
    """of the record's 36 contacts, how many are still GENUINE at this point?

    The plane-triple census this replaced was both slow and fragile (mpmath's `lu_solve` threw
    on a singular triple), and it answered a bigger question than the one that matters.  The
    question that matters is whether each contact's crossing is still INSIDE both edge
    segments: the Newton step keeps the coplanarity equations satisfied by construction, so a
    contact can only be lost by the crossing sliding off the end of an edge.

    Returns (in_range, margin).  `margin` is the smallest distance any parameter had to the
    ends of [0,1]: every decision is a sign test on an O(1) quantity, so a margin approaching
    the arithmetic's accuracy means the answer is refused, not guessed.
    """
    qs = [[mp.mpf(int(t)) for t in q0]] + \
         [[x[4 * k + c] for c in range(4)] for k in range(3)]

    def frame(q):
        """columns of the rotation matrix = the cube's axes; rows of this = face normals"""
        w, xx, y, z = q
        n = w * w + xx * xx + y * y + z * z
        M = [[w*w+xx*xx-y*y-z*z, 2*(xx*y-w*z),      2*(xx*z+w*y)],
             [2*(xx*y+w*z),      w*w-xx*xx+y*y-z*z, 2*(y*z-w*xx)],
             [2*(xx*z-w*y),      2*(y*z+w*xx),      w*w-xx*xx-y*y+z*z]]
        return [[M[r][c] / n for r in range(3)] for c in range(3)]

    F = [frame(q) for q in qs]

    def world(M, v):
        return [sum(M[r][k] * v[r] for r in range(3)) for k in range(3)]

    ok = 0
    margin = mp.mpf(1)
    for (i, j), lab in labels:
        a, b, s1, t1, p1, r1 = lab
        c1 = [mp.mpf(0)] * 3; c1[(a + 1) % 3] = mp.mpf(s1); c1[(a + 2) % 3] = mp.mpf(t1)
        A1 = world(F[i], [c1[k] - (1 if k == a else 0) for k in range(3)])
        B1 = world(F[i], [c1[k] + (1 if k == a else 0) for k in range(3)])
        c2 = [mp.mpf(0)] * 3; c2[(b + 1) % 3] = mp.mpf(p1); c2[(b + 2) % 3] = mp.mpf(r1)
        A2 = world(F[j], [c2[k] - (1 if k == b else 0) for k in range(3)])
        B2 = world(F[j], [c2[k] + (1 if k == b else 0) for k in range(3)])
        u = [B1[k] - A1[k] for k in range(3)]
        v = [B2[k] - A2[k] for k in range(3)]
        w = [A2[k] - A1[k] for k in range(3)]

        def cross(p, q):
            return [p[1]*q[2]-p[2]*q[1], p[2]*q[0]-p[0]*q[2], p[0]*q[1]-p[1]*q[0]]

        def dot(p, q):
            return sum(p[k] * q[k] for k in range(3))

        n = cross(u, v)
        nn = dot(n, n)
        if nn < mp.mpf('1e-30'):
            continue
        sp_ = dot(cross(w, v), n) / nn
        tp = dot(cross(w, u), n) / nn
        m = min(sp_, 1 - sp_, tp, 1 - tp)
        margin = min(margin, abs(m))
        if 0 <= sp_ <= 1 and 0 <= tp <= 1:
            ok += 1
    return ok, margin


def main():
    import sympy as sp
    import mpmath as mp
    mp.mp.dps = 50

    REC = [tuple(q) for q in WK.REC[4]]
    U, V = CR.__dict__.get('U'), CR.__dict__.get('V')

    # rebuild the symbolic contact forms (CR builds them inside main, so redo here)
    u = sp.symbols('u0:4'); v = sp.symbols('v0:4')

    def rot(q):
        w, x, y, z = q
        return sp.Matrix([[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
                          [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                          [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]])

    RU, RV = rot(u), rot(v)
    NU = sum(t * t for t in u); NV = sum(t * t for t in v)

    # THE ONE EXPENSIVE STEP, and it had been recomputed in four consecutive runs before this
    # cache existed ([METHODS 2]: cache the expensive step BEFORE the first run).  The forms
    # depend on nothing but the cube geometry, so the key is the code that makes them.
    import pickle, hashlib
    CACHE = os.path.join(ROOT, 'catalogue_cache')
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(b'contact-forms-v1-bideg22').hexdigest()[:12]
    path = os.path.join(CACHE, 'contact_forms_%s.pkl' % key)
    if os.path.exists(path):
        FORMS = {k: sp.sympify(v) for k, v in pickle.load(open(path, 'rb')).items()}
        print('forms loaded from cache: %d' % len(FORMS), flush=True)
    else:
        FORMS = {}
        for a in range(3):
            for b in range(3):
                for s, t, p, r in itertools.product((-1, 1), repeat=4):
                    d1 = RU * sp.Matrix([1 if i == a else 0 for i in range(3)])
                    c1 = sp.Matrix([0, 0, 0]); c1[(a + 1) % 3] = s; c1[(a + 2) % 3] = t
                    d2 = RV * sp.Matrix([1 if i == b else 0 for i in range(3)])
                    c2 = sp.Matrix([0, 0, 0]); c2[(b + 1) % 3] = p; c2[(b + 2) % 3] = r
                    FORMS[(a, b, s, t, p, r)] = sp.expand(
                        sp.Matrix.hstack(d1, d2, NU * RV * c2 - NV * RU * c1).det())
        pickle.dump({k: sp.srepr(v) for k, v in FORMS.items()}, open(path, 'wb'))
        print('forms built and cached: %d' % len(FORMS), flush=True)

    # the 12 unknowns: cubes 1,2,3 (cube 0 is gauge-fixed at the record's first quaternion)
    P = sp.symbols('P0:12')
    qsym = [[sp.Integer(REC[0][c]) for c in range(4)]] + \
           [[P[4 * (k - 1) + c] for c in range(4)] for k in (1, 2, 3)]

    eqs = []
    for i, j in itertools.combinations(range(4), 2):
        live = CR.in_range_labels(REC[i], REC[j])
        for lab in live:
            f = FORMS[lab]
            sub = {}
            for c in range(4):
                sub[u[c]] = qsym[i][c]; sub[v[c]] = qsym[j][c]
            eqs.append(f.subs(sub))
    print('active contact equations: %d' % len(eqs), flush=True)

    J = sp.Matrix([[sp.diff(e, p) for p in P] for e in eqs])
    x0 = [sp.Integer(REC[k][c]) for k in (1, 2, 3) for c in range(4)]
    J0 = J.subs(dict(zip(P, x0)))
    print('Jacobian rank at the record: %d  (12 unknowns)' % J0.rank(), flush=True)

    ns = J0.nullspace()
    print('null space dimension: %d   (3 of these are the per-cube scalings)' % len(ns),
          flush=True)

    # strip the three scaling directions
    scal = []
    for k in range(3):
        col = [sp.Integer(0)] * 12
        for c in range(4):
            col[4 * k + c] = sp.Integer(REC[k + 1][c])
        scal.append(sp.Matrix(col))
    S = sp.Matrix.hstack(*scal)
    # the number of GENUINE directions is dim(null) - dim(null ^ scalings), NOT the count of
    # basis vectors that individually extend S: two such vectors can span the same 4-space.
    # (The first version printed 2 where the answer is 1.)
    NS = sp.Matrix.hstack(*ns) if ns else sp.zeros(12, 0)
    ngen = NS.rank() - sp.Matrix.hstack(S, NS).rank() + S.rank()
    ngen = NS.rank() - (sp.Matrix.hstack(S, NS).rank() - S.rank()) if False else \
        NS.rank() - S.rank() if sp.Matrix.hstack(S, NS).rank() == NS.rank() else None
    if ngen is None:
        ngen = sp.Matrix.hstack(S, NS).rank() - S.rank()
    genuine = []
    for w in ns:
        M = sp.Matrix.hstack(S, w)
        if M.rank() > S.rank():
            genuine.append(w)
    print('genuine (non-scaling) kernel dimension: %d   (basis vectors outside the scalings: %d)'
          % (ngen, len(genuine)), flush=True)

    out = {'what': 'is the n=4 record on a curve invisible to straight-line probes?',
           'supports': 'OQ 39', 'jacobian_rank': int(J0.rank()),
           'nullspace_dim': len(ns), 'genuine_directions': len(genuine)}

    if not genuine:
        print('\nNO genuine direction: the tangent space is spanned by the scalings alone,')
        print('so the record is RIGID and [P287] stands with a second, independent argument.')
        out['verdict'] = 'rigid: tangent space is scalings only'
    else:
        w = genuine[0]
        wn = [mp.mpf(str(sp.nsimplify(t))) if t.is_rational else mp.mpf(float(t))
              for t in w]
        nrm = mp.sqrt(sum(t * t for t in wn))
        wn = [t / nrm for t in wn]
        Ff = sp.lambdify(P, eqs, 'mpmath')
        Jf = sp.lambdify(P, J.tolist(), 'mpmath')
        base = [mp.mpf(int(t)) for t in x0]
        # GATE: the same census code at the RECORD ITSELF must return the record's census.
        # Skipping this is what let a rows/columns error read as 'the curve changes the
        # combinatorics'.
        LABELS = []
        for i, j in itertools.combinations(range(4), 2):
            for lab in CR.in_range_labels(REC[i], REC[j]):
                LABELS.append(((i, j), lab))
        g_n, g_guard = contacts_at(mp, REC[0], base, LABELS)
        want = len(LABELS)
        print('\n   GATE at the record itself: %d of %d contacts in range   %s'
              % (g_n, want, 'PASS' if g_n == want else 'FAIL -- the checker is wrong'),
              flush=True)
        gc, gskip, gmar = full_census(mp, REC[0], base)
        WANT0 = {(1, 1, 1): 128, (1, 2): 24, (2, 2): 36, (3, 3): 6}
        print('   GATE, full census at the record: %s   %s   (skipped %d)'
              % (gc, 'PASS' if gc == WANT0 else 'FAIL', gskip), flush=True)
        out['gate'] = {'in_range': g_n, 'expected': want, 'pass': bool(g_n == want),
                       'census': {str(k): v for k, v in gc.items()},
                       'census_pass': bool(gc == WANT0), 'census_skipped': gskip}
        if gc != WANT0:
            print('   refusing to report: the census gate failed', flush=True)
            json.dump(out, open(os.path.join(ROOT, 'data', 'record_curve.json'), 'w'), indent=1)
            return
        if g_n != want:
            print('   refusing to report the continuation until the census gate passes',
                  flush=True)
            json.dump(out, open(os.path.join(ROOT, 'data', 'record_curve.json'), 'w'), indent=1)
            return
        print('\n   step        |F| after Newton      moved by      contacts in range')
        rows = []
        for step in ('1e-3', '1e-4', '1e-6'):
            h = mp.mpf(step)
            x = [base[i] + h * wn[i] for i in range(12)]
            for _ in range(60):
                Fv = mp.matrix(Ff(*x))
                Jv = mp.matrix(Jf(*x))
                try:
                    dx = mp.lu_solve(Jv.T * Jv + mp.eye(12) * mp.mpf('1e-40'), -(Jv.T * Fv))
                except Exception:
                    break
                x = [x[i] + dx[i] for i in range(12)]
                if max(abs(t) for t in dx) < mp.mpf('1e-45'):
                    break
            resid = max(abs(t) for t in mp.matrix(Ff(*x)))
            moved = mp.sqrt(sum((x[i] - base[i]) ** 2 for i in range(12)))
            nin, guard = contacts_at(mp, REC[0], x, LABELS)
            print('   %-8s   %-20s  %-12s  %2d of %d in range%s'
                  % (step, mp.nstr(resid, 8), mp.nstr(moved, 8), nin, len(LABELS),
                     '   *** margin %s, REFUSED ***' % mp.nstr(guard, 5)
                     if guard < mp.mpf('1e-20') else '   margin %s' % mp.nstr(guard, 5)),
                  flush=True)
            cen, skip, cmar = full_census(mp, REC[0], x)
            WANT = {(1, 1, 1): 128, (1, 2): 24, (2, 2): 36, (3, 3): 6}
            print('              census %s  %s   (skipped %d, margin %s)'
                  % (cen, 'MATCHES the record' if cen == WANT else 'DIFFERS',
                     skip, mp.nstr(cmar, 5)), flush=True)
            rows.append({'step': step, 'residual': mp.nstr(resid, 12),
                         'moved': mp.nstr(moved, 12),
                         'contacts_in_range': nin, 'of': len(LABELS),
                         'margin': mp.nstr(guard, 8),
                         'census': {str(k): v for k, v in cen.items()},
                         'census_matches': bool(cen == WANT),
                         'census_skipped': skip})
        out['newton'] = rows
        out['verdict'] = ('a genuine tangent direction exists; whether it integrates to a real '
                          'curve is read from whether Newton keeps the displacement')

    out['reproduce'] = PROV.stamp(parameters={'dps': 50},
                                  note='exact Jacobian; Newton in 50-digit arithmetic')
    json.dump(out, open(os.path.join(ROOT, 'data', 'record_curve.json'), 'w'), indent=1)
    print('\nwrote data/record_curve.json', flush=True)


if __name__ == '__main__':
    main()
