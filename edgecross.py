#!/usr/bin/env python3
"""Tangent directions that preserve the EDGE-EDGE CROSSINGS, solved exactly.

Two edges from different cubes generically do NOT meet -- two lines in space
miss.  So every edge-edge crossing a configuration carries is a codimension-1
coincidence, and a 13-pair carries 24 of them at once.  Preserving them is
therefore a strong, purely geometric condition on a perturbation, and unlike the
Step-A tightness of `tight_set.py` it is a condition about incidences that
actually exist in the arrangement rather than about slabs that might bound a
region.

Preserving crossings is NOT the same as preserving the region count -- a count
can survive a crossing being destroyed, and can change while all crossings hold.
It is a hint about where the count is likely to be rigid, and every direction it
proposes is verified against the engine before being believed.

The crossing condition for edges (P1, D1) and (P2, D2) is coplanarity,
det[D1, D2, P2 - P1] = 0, tested for REAL crossings only: the common point must
lie inside both segments.  Detection is exact over Q; the Jacobian is central
differences on the same determinants.
"""
import itertools, json, subprocess, sys
from fractions import Fraction as F
from math import gcd
import numpy as np

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"

# ---------- rotations ----------

def rotF(q):
    """exact rotation matrix (Fractions) from an integer quaternion"""
    w, x, y, z = [F(v) for v in q]
    n = w*w + x*x + y*y + z*z
    return [[(w*w+x*x-y*y-z*z)/n, 2*(x*y-w*z)/n, 2*(x*z+w*y)/n],
            [2*(x*y+w*z)/n, (w*w-x*x+y*y-z*z)/n, 2*(y*z-w*x)/n],
            [2*(x*z-w*y)/n, 2*(y*z+w*x)/n, (w*w-x*x-y*y+z*z)/n]]

def rotN(q):
    return np.array([[float(v) for v in row] for row in rotF(q)])

def edges(R, F_=F):
    """the 12 edges of R([-1,1]^3) as (basepoint, direction)"""
    out = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                P = [R[i][b]*sb + R[i][c]*sc - R[i][a] for i in range(3)]
                D = [2*R[i][a] for i in range(3)]
                out.append((P, D))
    return out

def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))

def real_crossing(P1, D1, P2, D2):
    """exact: do the two SEGMENTS meet? returns True only for a real crossing"""
    W = [P2[i]-P1[i] for i in range(3)]
    if det3(D1, D2, W) != 0:
        return False
    # solve P1 + s D1 = P2 + t D2 on the two best-conditioned rows
    for i, j in ((0,1), (0,2), (1,2)):
        den = D1[i]*(-D2[j]) - (-D2[i])*D1[j]
        if den == 0:
            continue
        s = (W[i]*(-D2[j]) - (-D2[i])*W[j]) / den
        t = (D1[i]*W[j] - W[i]*D1[j]) / den
        return 0 <= s <= 1 and 0 <= t <= 1
    return False

# ---------- the crossing set and its Jacobian ----------

def crossing_set(quats):
    """list of (i, ei, j, ej) edge pairs that really cross, exact over Q"""
    Rs = [rotF(q) for q in quats]
    Es = [edges(R) for R in Rs]
    out = []
    for i, j in itertools.combinations(range(len(quats)), 2):
        for ei, (P1, D1) in enumerate(Es[i]):
            for ej, (P2, D2) in enumerate(Es[j]):
                if real_crossing(P1, D1, P2, D2):
                    out.append((i, ei, j, ej))
    return out

def dets_at(quats, p):
    """the crossing determinants under perturbation p (3 per free cube)"""
    Rs = []
    for k, q in enumerate(quats):
        R = rotN(q)
        if k > 0:
            d = p[3*(k-1):3*k]
            K = np.array([[0, -d[2], d[1]], [d[2], 0, -d[0]], [-d[1], d[0], 0]])
            R = R @ (np.eye(3) + K)
        Rs.append(R)
    Es = [edges(R, float) for R in Rs]
    return Es

def jacobian(quats, cset, h=1e-5):
    npar = 3*(len(quats)-1)
    def vals(p):
        Es = dets_at(quats, p)
        out = []
        for (i, ei, j, ej) in cset:
            P1, D1 = Es[i][ei]; P2, D2 = Es[j][ej]
            W = [P2[k]-P1[k] for k in range(3)]
            out.append(det3(D1, D2, W))
        return np.array(out)
    J = np.zeros((len(cset), npar))
    for k in range(npar):
        e = np.zeros(npar); e[k] = h
        J[:, k] = (vals(e) - vals(-e))/(2*h)
    # scale rows so no crossing dominates by accident of edge length
    for r in range(J.shape[0]):
        nr = np.linalg.norm(J[r])
        if nr > 1e-12:
            J[r] /= nr
    return J

def nullspace(J, npar):
    if J.shape[0] == 0:
        return np.eye(npar), npar
    U, S, Vt = np.linalg.svd(J)
    tol = 1e-7*max(S[0], 1e-30)
    rank = int((S > tol).sum())
    null = np.array([Vt[i] for i in range(npar) if i >= len(S) or S[i] <= tol])
    return null, rank

# ---------- engine verification ----------

def qmulF(p, q):
    w,x,y,z = p; e,f,g,h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g,
            w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)

def redq(q):
    L = 1
    for v in q: L = L*v.denominator//gcd(L, v.denominator)
    iq = [int(v*L) for v in q]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def count(cfg):
    s = ";".join(",".join(map(str, q)) for q in cfg)
    m = max(abs(v) for q in cfg for v in q)
    cmd = [ENG, "--quats", s] if m <= 512 else [ENGW, "--d", "0", "--quats", s]
    try:
        return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)["bounded"]
    except Exception:
        return None

def walk(quats, u, epss=(F(1,64), F(1,256), F(1,1024))):
    base = count(list(quats))
    for e in epss:
        for sg in (1, -1):
            cfg = [tuple(F(v) for v in quats[0])]
            for i in range(1, len(quats)):
                d = [F(u[3*(i-1)+k])*e*sg for k in range(3)]
                cfg.append(qmulF(tuple(F(v) for v in quats[i]), (F(1), d[0], d[1], d[2])))
            if count([redq(c) for c in cfg]) != base:
                return False
    return True

def sparse_dirs(null, npar, ncube):
    """directions in the null space supported on one or two cubes"""
    out = []
    for r in (1, 2, 3):
        for S in itertools.combinations(range(1, ncube+1), r):
            keep = [3*(i-1)+j for i in S for j in range(3)]
            drop = [i for i in range(npar) if i not in keep]
            if not drop:
                out += [('all', v) for v in null]
                continue
            M = null[:, drop].T
            if M.size == 0:
                continue
            U, S2, V2t = np.linalg.svd(M, full_matrices=True)
            tol = 1e-8*max(S2[0] if len(S2) else 1.0, 1e-30)
            for i in range(null.shape[0]):
                if i >= len(S2) or S2[i] <= tol:
                    out.append(('cubes'+str(S), V2t[i] @ null))
    return out

def report(quats, label, known=()):
    n = len(quats); npar = 3*(n-1)
    cset = crossing_set(quats)
    J = jacobian(quats, cset)
    null, rank = nullspace(J, npar)
    base = count(list(quats))
    print('%-24s count=%-5s %3d edge-edge crossings, rank %2d of %2d -> null dim %d'
          % (label, base, len(cset), rank, npar, len(null)), flush=True)
    for name, ci, d in known:
        q = np.array([float(v) for v in quats[ci]])
        A = np.zeros((4, 4))
        for k in range(3):
            u = [0.0]*3; u[k] = 1.0
            A[:, k] = qmulF(tuple(q), (0.0, u[0], u[1], u[2]))
        A[:, 3] = -q
        sol, *_ = np.linalg.lstsq(A, np.array([0.0, d[0], d[1], d[2]])*q[0], rcond=None)
        full = np.zeros(npar); full[3*(ci-1):3*ci] = sol[:3]
        full /= np.linalg.norm(full)
        proj = np.linalg.norm(null.T @ (null @ full)) if len(null) else 0.0
        print('    known %-20s in the crossing null space: %.4f' % (name, proj), flush=True)
    hits = []
    seen = []
    for name, v in sparse_dirs(null, npar, n-1):
        if np.max(np.abs(v)) < 1e-9:
            continue
        v = v/np.linalg.norm(v)
        if any(abs(abs(v @ s)-1) < 1e-6 for s in seen):
            continue
        seen.append(v)
        u = [F(float(x)).limit_denominator(10**6) for x in v/np.max(np.abs(v))]
        if walk(quats, u):
            hits.append(v)
            print('    HOLDS %-12s %s' % (name, np.array2string(
                v/np.max(np.abs(v)), precision=3, suppress_small=True,
                max_line_width=220)), flush=True)
    if hits:
        s = np.linalg.svd(np.array(hits), compute_uv=False)
        print('    -> %d verified, spanning dimension %d'
              % (len(hits), int((s > 1e-6*s[0]).sum())), flush=True)
    elif len(null):
        print('    -> null space non-trivial but nothing in it holds the count', flush=True)
    return len(cset), rank, len(null)

I = (1,0,0,0)
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

if __name__ == '__main__':
    print('=== CONTROLS: five configurations with verified tangents ===')
    report([I, (1,-12,-11,0)], 'n=2 mirror 13', [('(1,1,0)', 1, [1,1,0])])
    report([I, (10,3,3,3)], 'n=2 diagonal 13', [('(1,1,1)', 1, [1,1,1])])
    report(BASE+[(10,9,9,9)], 'n=6 723', [('(1,1,1)', 5, [1,1,1])])
    report(BASE+[(6,53,-87,-156)], 'n=6 727 arc A', [('(1,-3,-6)', 5, [1,-3,-6])])
    report(BASE+[(7,14,1,-5)], 'n=6 727 RECORD',
           [('D1 (-1,-1/7,3/14)', 5, [-1, -1/7, 3/14]),
            ('D2 (-1,-4/21,2/7)', 5, [-1, -4/21, 2/7])])
    print()
    print('=== the open cells ===')
    report([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    report(BASE, 'n=5 393')
    report(BASE+[(7,14,1,-5),(4,-3,-4,-4)], 'n=7 1217')
    report(BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)], 'n=8 1895')
