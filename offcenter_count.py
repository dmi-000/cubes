#!/usr/bin/env python3
# Working principles: PROJECT.md + certify_six.py::exact_count_config (the
# concentric ancestor of this file). Project index: README.md.
"""Exact bounded-region counter for compounds of n congruent cubes that may
be TRANSLATED as well as rotated -- i.e. cube k = R_k([-1,1]^3) + t_k for an
integer-quaternion rotation R_k and a rational translation t_k, instead of
the concentric R_k([-1,1]^3) that certify_six.py::exact_count_config counts.

THE MATH (see PROJECT.md and the task brief this file was built from)
-----------------------------------------------------------------------
Local cube coordinates y in [-1,1]^3 map to world coordinates via
x = R_k y + t_k.  Because R_k is orthogonal, y = R_k^T (x - t_k), and the
j-th local coordinate is y_j = n_j . (x - t_k) where n_j is the j-th COLUMN
of R_k (columns of R = rows of R^T).  Face j of the local cube is y_j = +-1,
so in world coordinates:

    face plane:      n_j . x = +-1 + n_j . t_k          (offset shifts)
    inside cube k:   |n_j . (x - t_k)| < 1  for all three columns n_j
    on-face-square:  for a point already on face j, it is a REAL point of
                      the physical square face (not a phantom continuation
                      of the plane) iff the OTHER two local coordinates
                      satisfy |n_a . (x - t_k)| < 1, |n_b . (x - t_k)| < 1.

So relative to the concentric counter, exactly three things change: (a) the
plane offset per (cube, axis, sign) becomes 1 + n.t_k instead of a bare 1
(and correspondingly for -1); (b) the face-square and (c) the containment
tests are relative to the cube's own centre t_k, not the origin. Everything
else -- convex-cell clipping against the plane arrangement, phantom-facet
identification and merging, depth labelling -- is the same algorithm as
certify_six.py, adapted here to use plain Fraction arithmetic directly
(points are tuples of Fraction, which are already hashable/orderable/exact,
so no interval-number wrapper class is needed the way certify_six.py needed
CN for its Q(sqrt5) leaves).

HARD GATE: with all t_k = 0 this must reproduce the concentric counts from
cube_regions / certify_six.py EXACTLY (see selftest() below, run by default
with no arguments). Do not trust anything from --experiment before the gate
prints ALL PASS.

Usage
-----
  python3 offcenter_count.py                 # run the t=0 gate, print PASS/FAIL
  python3 offcenter_count.py --experiment     # run the off-centering experiment
                                               # on the 723 record, write report
"""
import itertools
import json
import sys
import time
from fractions import Fraction as Fr


# --------------------------------------------------------------- rotations
def rot_from_quat(w, x, y, z):
    """Integer quaternion -> exact rational 3x3 rotation matrix (list of
    3 rows, each a list of 3 Fractions). Same formula as
    golden_rotations.rot_from_quat, but landing in plain Fraction instead
    of the Q(sqrt5) field Q5 (unnecessary here: no golden/dodecahedral
    axes are used by this file, only integer-quaternion rotations, which
    are already rational)."""
    n = w * w + x * x + y * y + z * z
    if n == 0:
        raise ValueError('zero quaternion')

    def q(v):
        return Fr(v, n)

    return [[q(w * w + x * x - y * y - z * z), q(2 * (x * y - w * z)),
              q(2 * (x * z + w * y))],
             [q(2 * (x * y + w * z)), q(w * w - x * x + y * y - z * z),
              q(2 * (y * z - w * x))],
             [q(2 * (x * z - w * y)), q(2 * (y * z + w * x)),
              q(w * w - x * x - y * y + z * z)]]


def cols_of(m):
    """Columns of a 3x3 matrix (list of rows) as 3 tuples of Fraction."""
    return [tuple(m[i][j] for i in range(3)) for j in range(3)]


def as_frac(v):
    if isinstance(v, Fr):
        return v
    if isinstance(v, tuple) and len(v) == 2:
        return Fr(v[0], v[1])
    return Fr(v)


# --------------------------------------------------------------- geometry
def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def vadd(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def vsub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def vscale(u, t):
    return (u[0] * t, u[1] * t, u[2] * t)


def sign(v):
    return 1 if v > 0 else (-1 if v < 0 else 0)


def clip(faces, f, cache):
    """Split a convex cell (list of (pid, loop-of-points)) by the plane
    f(p) == 0.  Returns (neg_half, pos_half); a half is None if empty.
    Identical algorithm to cube_compound_interval.clip / cube_compound_exact
    .clip, just against plain-Fraction f() instead of a Q5/CN plane
    function -- points are tuples of Fraction, so no wrapper class,
    dict/set identity, or leaf() call is needed."""
    def sgn(p):
        s = cache.get(p)
        if s is None:
            s = sign(f(p))
            cache[p] = s
        return s

    pts = {p for _, loop in faces for p in loop}
    signs = {p: sgn(p) for p in pts}
    if not any(s > 0 for s in signs.values()):
        return faces, None
    if not any(s < 0 for s in signs.values()):
        return None, faces

    inter = {}

    def cut(p, q):
        key = frozenset((p, q))
        w = inter.get(key)
        if w is None:
            fp, fq = f(p), f(q)
            t = fp / (fp - fq)
            w = vadd(p, vscale(vsub(q, p), t))
            inter[key] = w
            cache[w] = 0
        return w

    halves = []
    for keep in (-1, 1):
        new_faces = []
        cap_edges = []
        for pid, loop in faces:
            out = []
            zeros = []
            m = len(loop)
            for i in range(m):
                p, q = loop[i], loop[(i + 1) % m]
                sp, sq = signs[p], signs[q]
                if sp * keep >= 0:
                    out.append(p)
                    if sp == 0:
                        zeros.append(p)
                if sp * sq < 0:
                    w = cut(p, q)
                    out.append(w)
                    zeros.append(w)
            ded = [p for i, p in enumerate(out) if p != out[i - 1]]
            if len(ded) >= 3:
                new_faces.append((pid, ded))
            zs = []
            for z in zeros:
                if z not in zs:
                    zs.append(z)
            if len(zs) == 2:
                cap_edges.append(tuple(zs))
        if cap_edges:
            nbr = {}
            for a, b in cap_edges:
                nbr.setdefault(a, []).append(b)
                nbr.setdefault(b, []).append(a)
            start = cap_edges[0][0]
            loop, prev, cur = [start], None, start
            while True:
                nxts = [x for x in nbr[cur] if x != prev]
                if not nxts:
                    break
                prev, cur = cur, nxts[0]
                if cur == start:
                    break
                loop.append(cur)
            if len(loop) >= 3 and cur == start:
                new_faces.append(('cap', loop))
        halves.append(new_faces if new_faces else None)
    return halves[0], halves[1]


# ---------------------------------------------------------------- counter
def offcenter_count(configs, verbose=False, with_labels=False):
    """Exact bounded-region count for cubes R_k([-1,1]^3) + t_k.

    configs: list of (quat, translation) pairs.
      quat = (w, x, y, z) integers (or rationals), any nonzero quaternion.
      translation = (tx, ty, tz), each an int, Fraction, or (num, den) pair.
    t_k = (0,0,0) for every k reproduces the concentric counter exactly
    (this is the hard gate in selftest() below).
    """
    nq = len(configs)
    cols = []
    trans = []
    sizes = []
    for cfg in configs:
        # cfg = (quat, translation) or (quat, translation, size). size is the
        # cube's half-width (default 1 = the concentric unit cube). A cube of
        # size s_k has faces n.(x - t_k) = +-s_k and interior |n.(x-t_k)| < s_k,
        # so s_k enters exactly three predicates: the plane offset, the
        # real-facet extent, and the containment/label test -- all below.
        quat, t = cfg[0], cfg[1]
        s = cfg[2] if len(cfg) > 2 else 1
        m = rot_from_quat(*quat)
        cols.append(cols_of(m))
        trans.append(tuple(as_frac(c) for c in t))
        sizes.append(as_frac(s))

    # proj[k][j] = n_{k,j} . t_k -- the amount face j of cube k is pushed
    # out along its own normal by the translation. Precomputed once so the
    # plane-offset, coincidence-key, real-facet and label predicates below
    # all derive from the same number (no risk of the offset and the
    # containment test silently using different translations).
    proj = [[dot(cols[k][j], trans[k]) for j in range(3)] for k in range(nq)]

    planes = [(k, j, c) for k in range(nq) for j in range(3) for c in (1, -1)]

    # INVARIANT (generalizes the concentric coincidence-class comment in
    # certify_six.py): two planes from different cubes are the SAME plane
    # iff they have the same normal direction AND the same effective
    # offset n.x = c_eff.  In the concentric counter c_eff in {+1,-1}
    # always, so equality of the (canonicalized) normal direction was
    # enough; with translation c_eff = c + n.t_k varies continuously, so
    # the offset must be compared too, or translated cubes whose faces are
    # merely PARALLEL (not coincident) would be wrongly merged into one
    # coincidence class -- silently dropping real facets. A coincidence
    # class still gets the "first plane cuts, later ones find no strict
    # crossing" treatment; every cube owning that exact plane must still be
    # tested for real-vs-phantom independently (same reasoning as the
    # concentric file: do not simplify to single-owner testing).
    def plane_key(k, j, c):
        n = cols[k][j]
        c_eff = c * sizes[k] + proj[k][j]
        s = 0
        for x in n:
            s = sign(x)
            if s != 0:
                break
        if s < 0:
            n = tuple(-x for x in n)
            c_eff = -c_eff
        return (n, c_eff)

    classes = {}
    for k, j, c in planes:
        classes.setdefault(plane_key(k, j, c), []).append((k, j))
    owners_of = [classes[plane_key(k, j, c)] for (k, j, c) in planes]

    # bounding box: must contain every translated cube. Cube k's farthest
    # point from the origin is at most sqrt(3) + |t_k| (sup-norm-safe bound
    # using L1: sqrt(3) + |t_k,x|+|t_k,y|+|t_k,z|), so any axis-aligned box
    # of half-width > 2 + max_k sum(|t_k,i|) safely contains all cubes;
    # take a generous margin on top (matches the concentric file's B=4 for
    # unit cubes of half-diagonal sqrt(3) ~ 1.73, margin factor > 2x).
    max_t = Fr(0)
    for t in trans:
        s = sum(abs(c) for c in t)
        if s > max_t:
            max_t = s
    B = Fr(4) + 4 * max_t
    nB = -B
    corners = list(itertools.product((B, nB), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] == val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (p[a], p[b]))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cells = [[(('box', i, s), box_face(i, v))
              for i in range(3) for s, v in ((1, B), (-1, nB))]]

    for pid, (k, j, c) in enumerate(planes):
        n = cols[k][j]
        c_eff = c + proj[k][j]
        f = lambda p, n=n, c_eff=c_eff: dot(n, p) - c_eff
        cache = {}
        nxt = []
        for cell in cells:
            neg, pos = clip(cell, f, cache)
            for half in (neg, pos):
                if half is not None:
                    nxt.append([(pid if q == 'cap' else q, loop)
                                for q, loop in half])
        cells = nxt
    if verbose:
        print(f'offcenter: arrangement cells = {len(cells)}')

    def centroid_pts(pts):
        k = Fr(1, len(pts))
        s = (Fr(0), Fr(0), Fr(0))
        for p in pts:
            s = vadd(s, p)
        return vscale(s, k)

    def label(w):
        lab = 0
        for k in range(nq):
            if all(-sizes[k] < dot(cols[k][j], w) - proj[k][j] < sizes[k]
                   for j in range(3)):
                lab |= 1 << k
        return lab

    labs = [label(centroid_pts(list({p for _, loop in c for p in loop})))
            for c in cells]

    groups = {}
    for ci, cell in enumerate(cells):
        for pid, loop in cell:
            if isinstance(pid, tuple):
                continue
            groups.setdefault((pid, frozenset(loop)), []).append(ci)

    parent = list(range(len(cells)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (pid, verts), cs in groups.items():
        assert len(cs) == 2, f'facet shared by {len(cs)} cells'
        a, b = cs
        w = centroid_pts(list(verts))
        flip = 0
        for kk, jj in owners_of[pid]:
            others = [t for t in range(3) if t != jj]
            if all(-sizes[kk] < dot(cols[kk][t], w) - proj[kk][t] < sizes[kk]
                   for t in others):
                flip |= 1 << kk
        if flip:
            assert labs[a] ^ labs[b] == flip, 'real facet flip mismatch'
        else:
            assert labs[a] == labs[b], 'phantom facet with differing labels'
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    comps = set()
    for ci in range(len(cells)):
        comps.add((labs[ci], find(ci)))
    per_label = {}
    for lab, _r in comps:
        per_label[lab] = per_label.get(lab, 0) + 1
    assert per_label.get(0, 0) == 1, 'outside must be a single region'
    by_depth = {}
    for lab, cnt in per_label.items():
        d = bin(lab).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
    total = sum(per_label.values()) - 1
    if with_labels:
        return total, by_depth, per_label
    return total, by_depth


# --------------------------------------------------------------------- gate
RECORD_723 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5),
              (2, 1, 1, 1), (1, 1, 1, 1), (5, 2, 2, 2)]
RECORD_723_DEPTH = {1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1}
RECORD_723_TOTAL = 723

# Three random-seed configs, taken from ./cube_regions --seed S (ground
# truth from the validated C++ engine), used as extra t=0 gate cases.
SEED_CASES = {
    2228: ([[143, 11, 232, 433], [356, 266, -168, -191], [100, 274, -7, 421],
            [-30, -49, -221, 458], [261, 22, 198, 393], [200, -122, 391, -232]],
           623, {1: 112, 2: 208, 3: 164, 4: 102, 5: 36, 6: 1}),
    42: ([[450, 147, -41, 191], [220, -67, -67, 453], [-245, -247, 286, -244],
          [109, -47, 370, 334], [364, 261, -81, 234], [-355, 365, -56, 17]],
         531, {1: 74, 2: 164, 3: 156, 4: 100, 5: 36, 6: 1}),
    777: ([[308, 202, 355, 28], [346, -237, -200, -216], [344, -318, 182, 99],
           [158, 218, 397, 179], [-84, 390, 139, -289], [141, 423, -210, -139]],
          575, {1: 92, 2: 184, 3: 160, 4: 102, 5: 36, 6: 1}),
}


def zero_t(quats):
    return [(tuple(q), (0, 0, 0)) for q in quats]


def _drop_depth0(by_depth):
    # by_depth (like certify_six.exact_count_config's) tallies EVERY label
    # including the outside region (label 0, depth 0, count always 1); the
    # canonical depth profiles quoted in PROJECT.md / README.md omit that
    # depth-0 entry, so strip it before comparing against them.
    return {k: v for k, v in by_depth.items() if k != 0}


def selftest():
    print('=== t=0 gate: offcenter_count must reproduce concentric counts ===')
    ok = True

    t0 = time.time()
    total, by_depth = offcenter_count(zero_t(RECORD_723))
    dt = time.time() - t0
    cmp_depth = _drop_depth0(by_depth)
    passed = (total == RECORD_723_TOTAL and cmp_depth == RECORD_723_DEPTH)
    ok &= passed
    print(f'  723 record: total={total} by_depth={dict(sorted(cmp_depth.items()))} '
          f'({dt:.1f}s)  {"PASS" if passed else "FAIL (expected 723, " + str(RECORD_723_DEPTH) + ")"}')

    for seed, (quats, exp_total, exp_depth) in SEED_CASES.items():
        t0 = time.time()
        total, by_depth = offcenter_count(zero_t(quats))
        dt = time.time() - t0
        cmp_depth = _drop_depth0(by_depth)
        passed = (total == exp_total and cmp_depth == exp_depth)
        ok &= passed
        print(f'  seed {seed}: total={total} by_depth={dict(sorted(cmp_depth.items()))} '
              f'({dt:.1f}s)  {"PASS" if passed else "FAIL (expected " + str(exp_total) + ")"}')

    print('=== GATE RESULT:', 'ALL PASS' if ok else 'FAIL -- do not trust --experiment', '===')
    return ok


# ------------------------------------------------------------ experiment
def fmt_t(t):
    return '(' + ','.join(str(c) for c in t) + ')'


def run_config(name, translations, log):
    """translations: list of n 3-tuples (Fraction-able). Returns (total, by_depth)."""
    cfg = [(RECORD_723[k], translations[k]) for k in range(6)]
    t0 = time.time()
    total, by_depth = offcenter_count(cfg)
    dt = time.time() - t0
    line = (f'{name}: total={total}  by_depth={dict(sorted(by_depth.items()))}  '
            f'translations={[fmt_t(t) for t in translations]}  ({dt:.1f}s)')
    print(line)
    log.append({'name': name, 'total': total, 'by_depth': by_depth,
                 'translations': [[str(c) for c in t] for t in translations]})
    return total, by_depth


def experiment():
    import random
    ZERO6 = [(0, 0, 0)] * 6
    steps = [Fr(-1, 2), Fr(-1, 4), Fr(-1, 8), Fr(0), Fr(1, 8), Fr(1, 4), Fr(1, 2)]
    log = []
    best = (RECORD_723_TOTAL, 'baseline (t=0)', ZERO6, RECORD_723_DEPTH)

    print('=== baseline ===')
    base_total, base_depth = run_config('baseline t=0', ZERO6, log)
    assert base_total == RECORD_723_TOTAL

    print('\n=== (i) one cube at a time, along each axis ===')
    for k in range(6):
        for axis in range(3):
            for s in steps:
                if s == 0:
                    continue
                tr = list(ZERO6)
                v = [Fr(0), Fr(0), Fr(0)]
                v[axis] = s
                tr[k] = tuple(v)
                name = f'cube{k} axis{axis} t={s}'
                total, by_depth = run_config(name, tr, log)
                if total > best[0]:
                    best = (total, name, tr, by_depth)

    print('\n=== (iii) shared (1,1,1) axis: translate cubes along (1,1,1)/sqrt3 ===')
    # use rational direction (1,1,1) unnormalized -- direction only matters,
    # magnitude is carried by the step itself (a rational translation along
    # (1,1,1) by amount s means each component = s).
    for s in steps:
        if s == 0:
            continue
        for subset_name, subset in [
            ('all6', range(6)),
            ('first3', range(3)),
            ('last3', range(3, 6)),
        ]:
            tr = list(ZERO6)
            for k in subset:
                tr[k] = (s, s, s)
            name = f'(1,1,1)-axis {subset_name} t={s}'
            total, by_depth = run_config(name, tr, log)
            if total > best[0]:
                best = (total, name, tr, by_depth)

    print('\n=== (ii) random small translation sets ===')
    random.seed(20260712)
    for trial in range(40):
        tr = [tuple(random.choice(steps) for _ in range(3)) for _ in range(6)]
        name = f'random#{trial}'
        total, by_depth = run_config(name, tr, log)
        if total > best[0]:
            best = (total, name, tr, by_depth)

    return base_total, base_depth, best, log


def write_report(base_total, base_depth, best, log, gate_ok):
    best_total, best_name, best_tr, best_depth = best
    increased = best_total > RECORD_723_TOTAL
    lines = []
    lines.append('# Off-center 723 experiment report\n')
    lines.append(f'Generated by offcenter_count.py.\n')
    lines.append(f'\n## t=0 gate\n')
    lines.append(f'Gate result: {"ALL PASS" if gate_ok else "FAIL"} '
                 f'(723 record and 3 random seeds reproduced exactly at t=0; '
                 f'see selftest() output above / offcenter_count.py --gate).\n')
    lines.append(f'\n## Baseline\n')
    lines.append(f'723 record at t=0: total={base_total}, '
                 f'by_depth={dict(sorted(base_depth.items()))}\n')
    lines.append(f'\n## Best off-center result found\n')
    lines.append(f'`{best_name}`: total={best_total}, '
                 f'by_depth={dict(sorted(best_depth.items()))}\n')
    lines.append(f'translations={[fmt_t(t) for t in best_tr]}\n')
    lines.append(f'\n**Off-centering {"DID" if increased else "did NOT"} '
                 f'increase the total above 723.**\n')
    lines.append(f'\n## Top 15 configs by total\n')
    top = sorted(log, key=lambda r: -r['total'])[:15]
    lines.append('| total | by_depth | config |\n|---|---|---|\n')
    for r in top:
        lines.append(f"| {r['total']} | {dict(sorted({int(k): v for k, v in r['by_depth'].items()}.items()))} | {r['name']} |\n")
    lines.append(f'\n## Depth-profile trend under translation\n')
    lines.append('Comparing every perturbed config against the baseline '
                 f'{{1:{base_depth.get(1,0)}, 2:{base_depth.get(2,0)}, '
                 f'3:{base_depth.get(3,0)}, 4:{base_depth.get(4,0)}, '
                 f'5:{base_depth.get(5,0)}, 6:{base_depth.get(6,0)}}}:\n\n')
    deltas = {d: [] for d in range(1, 7)}
    for r in log:
        for d in range(1, 7):
            deltas[d].append(r['by_depth'].get(d, r['by_depth'].get(str(d), 0)) - base_depth.get(d, 0))
    for d in range(1, 7):
        vals = deltas[d]
        lines.append(f'- depth {d}: min delta {min(vals)}, max delta {max(vals)}, '
                     f'mean delta {sum(vals)/len(vals):.2f}\n')
    lines.append(f'\n## All {len(log)} configs tried\n')
    lines.append('See offcenter_experiment_log.jsonl for the full machine-readable log.\n')
    with open('offcenter_report.md', 'w') as fh:
        fh.write(''.join(lines))
    with open('offcenter_experiment_log.jsonl', 'w') as fh:
        for r in log:
            fh.write(json.dumps(r) + '\n')
    print(f'\nwrote offcenter_report.md and offcenter_experiment_log.jsonl')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__)
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '--experiment':
        gate_ok = selftest()
        if not gate_ok:
            print('GATE FAILED -- refusing to run the experiment.')
            raise SystemExit(1)
        print()
        base_total, base_depth, best, log = experiment()
        write_report(base_total, base_depth, best, log, gate_ok)
        print(f'\nFINAL: t=0 gate PASS; best off-center total = {best[0]} '
              f'({"beats" if best[0] > RECORD_723_TOTAL else "does not beat"} 723)')
    else:
        ok = selftest()
        raise SystemExit(0 if ok else 1)
