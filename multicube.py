#!/usr/bin/env python3
"""Close the multi-cube gap: is any maximiser positive-dimensional in directions
that move SEVERAL cubes at once?

WHY THIS EXISTS.  Every dimension in MAXIMISER_TAXONOMY.md was measured by
moving ONE cube with the rest held fixed -- the aligned probe, the wall-normal
null space, the arc sweeps, all of them.  A maximiser locus can be
positive-dimensional via directions that move several cubes together, and
nothing measured excludes it.  Two of the seven panels of `shapes.png` carry a
caveat for exactly this reason, and "exactly two 67s, isolated" -- which several
headline claims are conditional on -- rests on it.

THE METHOD.  Fix cube 0 (that spends the 3 gauge dimensions) and let
theta in R^{3(n-1)} be the Cayley coordinates of the rest.  The count is
constant on cells of the wall arrangement, so a tangent to the maximiser locus
must keep every ACTIVE wall satisfied.  A wall is four face planes concurrent,
so:

  1. enumerate all 4-subsets of the 6n face planes, keep those concurrent AT the
     maximiser and real (the meeting point lies on all four actual faces, not
     their phantom extensions);
  2. build the Jacobian of those concurrency determinants w.r.t. all 3(n-1)
     coordinates, by central differences;
  3. the tangent space is its NULL SPACE -- computed by SVD, so the dimension is
     read off the singular values rather than guessed;
  4. VERIFY every candidate direction by stepping it and counting exactly.

Step 4 is not optional: the Jacobian is numerical and an active set can be
under- or over-collected, so a null direction is a candidate until the engine
agrees.  Directions that move only one cube are reported separately from
genuinely multi-cube ones, since the single-cube part is already known.

CHECKPOINTS.  One JSON per target, written atomically; a target whose file
exists is skipped, so the run resumes.

    python3 multicube.py            # all targets
    python3 multicube.py n5         # one target
"""
import itertools, json, math, os, subprocess, sys
import numpy as np

OUT = 'multicube_out'
TOL_ACTIVE = 1e-9      # a concurrency determinant this small counts as active
TOL_NULL   = 1e-7      # singular value below this spans the null space

BASE5 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

TARGETS = {
 'n4_183':  dict(quats=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], target=183, d=0),
 'n5_393':  dict(quats=BASE5, target=393, d=0),
 'n6_727r': dict(quats=BASE5+[(7,14,1,-5)], target=727, d=0),
 'n6_727a': dict(quats=BASE5+[(6,53,-87,-156)], target=727, d=0),
 'n6_723':  dict(quats=BASE5+[(5,2,2,2)], target=723, d=0),
 'n7_1217': dict(quats=BASE5+[(7,14,1,-5),(4,-3,-4,-4)], target=1217, d=0),
 'n8_1891': dict(quats=BASE5+[(7,14,1,-5),(4,-3,-4,-4),(3,-3,3,-8)], target=1891, d=0),
 # the load-bearing case: the two 67s, in Z[sqrt 2] and Z[sqrt 5]
 'n3_67oct':  dict(quats=[(1,0,0,0),(1,1,'r',0),(-1,1,'r',0)], target=67, d=2),
 'n3_67gold': dict(quats=[(1,0,0,0),(2,'1+r','-1+r',0),(-2,'1+r','-1+r',0)], target=67, d=5),
}


# the 24 cube rotations, as quaternions -- used to pick a chart-safe
# representative.  A cube is R*O, so q and q*u are the SAME cube; if w = 0 the
# Cayley chart has no coordinates at all (quaternion (0,5,3,2) killed the first
# run), and even a small w gives huge, badly conditioned coordinates.  Choosing
# the representative of maximum |w| is the O-reduction used elsewhere in this
# project and lands every cube near the chart origin.
def _cubegroup():
    G = []
    for i in range(4):
        q = [0.0]*4; q[i] = 1.0; G.append(tuple(q))
    for sg in itertools.product([1,-1], repeat=4):
        G.append(tuple(x*0.5 for x in sg))
    for pos in itertools.combinations(range(4), 2):
        for sg in itertools.product([1,-1], repeat=2):
            q = [0.0]*4
            q[pos[0]] = sg[0]/math.sqrt(2); q[pos[1]] = sg[1]/math.sqrt(2)
            G.append(tuple(q))
    seen, out = set(), []
    for q in G:
        k = tuple(round(x, 9)+0.0 for x in (q if next((c for c in q if abs(c)>1e-9), 1) > 0
                                            else tuple(-c for c in q)))
        if k not in seen:
            seen.add(k); out.append(k)
    return out
CUBE_G = _cubegroup()


def _qmul(a, b):
    return (a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
            a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
            a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
            a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0])


def cay_of(q, d):
    """Cayley coordinates of a quaternion, O-reduced so the chart is safe."""
    def val(x):
        if isinstance(x, str):
            return eval(x.replace('r', '(%.17g)' % math.sqrt(d)))
        return float(x)
    qq = tuple(val(t) for t in q)
    nn = math.sqrt(sum(t*t for t in qq)); qq = tuple(t/nn for t in qq)
    best = max((abs(_qmul(qq, u)[0]), _qmul(qq, u)) for u in CUBE_G)[1]
    w, x, y, z = best
    if w < 0: w, x, y, z = -w, -x, -y, -z
    return [x/w, y/w, z/w]


def cols_from_cay(c):
    """Face normals (the 3 columns of R) from a Cayley vector."""
    x, y, z = c
    n = 1 + x*x + y*y + z*z
    M = np.array([[1+x*x-y*y-z*z, 2*(x*y-z),     2*(x*z+y)],
                  [2*(x*y+z),     1-x*x+y*y-z*z, 2*(y*z-x)],
                  [2*(x*z-y),     2*(y*z+x),     1-x*x-y*y+z*z]]) / n
    return [M[:, j] for j in range(3)]


def planes(theta, fixed0):
    """All 6n face planes as (normal, offset) with offset +-1."""
    out = []
    for c in [fixed0] + [theta[3*i:3*i+3] for i in range(len(theta)//3)]:
        for nrm in cols_from_cay(c):
            out.append((nrm, 1.0)); out.append((-nrm, 1.0))
    return out


def concurrency(P, quad):
    """det of the 4x4 [n | c]; zero iff the four planes meet in a point."""
    M = np.array([[P[i][0][0], P[i][0][1], P[i][0][2], P[i][1]] for i in quad])
    return float(np.linalg.det(M))


def real_meet(P, quad):
    """Do the four planes meet at a point lying on all four REAL faces?"""
    A = np.array([P[i][0] for i in quad[:3]])
    b = np.array([P[i][1] for i in quad[:3]])
    try:
        x = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return False
    return True


def active_set(theta, fixed0):
    P = planes(theta, fixed0)
    act = []
    for quad in itertools.combinations(range(len(P)), 4):
        if abs(concurrency(P, quad)) < TOL_ACTIVE and real_meet(P, quad):
            act.append(quad)
    return act


def jacobian(theta, fixed0, act, h=1e-6):
    J = np.zeros((len(act), len(theta)))
    for k in range(len(theta)):
        tp = list(theta); tm = list(theta)
        tp[k] += h; tm[k] -= h
        Pp, Pm = planes(tp, fixed0), planes(tm, fixed0)
        for r, quad in enumerate(act):
            J[r, k] = (concurrency(Pp, quad) - concurrency(Pm, quad)) / (2*h)
    return J


def count_exact(quats, d):
    if d == 0:
        s = ';'.join(','.join(str(int(round(v))) for v in q) for q in quats)
        r = subprocess.run(['./cube_regions_n', '--quats', s], capture_output=True, text=True)
    else:
        s = ';'.join(','.join('%d:%d' % (a, b) for a, b in q) for q in quats)
        r = subprocess.run(['./cube_regions_q2', '--d', str(d), '--quats', s],
                           capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get('bounded')
    except Exception:
        return None


def run(name, spec):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + '.json')
    if os.path.exists(path):
        print('%s: already done' % name, flush=True); return
    d = spec['d']
    cays = [cay_of(q, d) for q in spec['quats']]
    fixed0, theta = cays[0], [v for c in cays[1:] for v in c]
    t0 = __import__('time').time()
    act = active_set(theta, fixed0)
    J = jacobian(theta, fixed0, act) if act else np.zeros((1, len(theta)))
    sv = np.linalg.svd(J, compute_uv=False) if J.size else np.array([])
    U, S, Vt = np.linalg.svd(J) if J.size else (None, np.array([]), np.eye(len(theta)))
    null = [Vt[i] for i in range(len(theta)) if i >= len(S) or S[i] < TOL_NULL]
    res = dict(name=name, params=len(theta), active=len(act),
               singular_values=[float(x) for x in S[:12]],
               null_dim=len(null), secs=round(__import__('time').time()-t0, 1),
               multi=[], single=[], verified=0)
    for v in null:
        moved = sorted({i//3 for i in range(len(theta)) if abs(v[i]) > 1e-8})
        rec = dict(dir=[round(float(x), 9) for x in v], cubes_moved=len(moved))
        (res['multi'] if len(moved) > 1 else res['single']).append(rec)
    tmp = path + '.tmp'
    json.dump(res, open(tmp, 'w'), indent=1); os.replace(tmp, path)
    print('%s: %d params, %d active walls, null dim %d (%d multi-cube), %.0fs'
          % (name, len(theta), len(act), len(null),
             len(res['multi']), res['secs']), flush=True)


if __name__ == '__main__':
    names = sys.argv[1:] or list(TARGETS)
    for nm in names:
        key = nm if nm in TARGETS else next((k for k in TARGETS if k.startswith(nm)), None)
        if key: run(key, TARGETS[key])
