#!/usr/bin/env python3
"""Local chambers around the 727 record's sixth cube, in its own R^3 Cayley space.

The 727 record is the 393 five-cube base (FIVE, see base_points.py) plus a sixth
cube FREE = (7,14,1,-5).  Extending a fixed base by one cube is a 3-DIMENSIONAL
problem -- the base's own walls do not constrain the new cube -- and against the
fixed base only 12 of the free cube's 6864-wall catalogue are INCIDENT at the
727 point (size_local.py: 4 W4 + 8 W3).  Twelve surfaces through a point in R^3
bound the local chambers at a few hundred, which is enumerable exactly.

METHOD
  1. Re-derive the 12 incident walls (mirroring size_local.py's incidence test,
     but keeping WHICH wall matched, not just the count).
  2. For each, build its condition SYMBOLICALLY in the free cube's 3 Cayley
     coordinates (dimension.cayley_matrix), differentiate, and evaluate the
     gradient exactly at the free cube's own Cayley point.  GATE: the condition
     itself must be exactly 0 there -- that is what "incident" means -- or the
     wall is wrong and the run stops.
  3. Enumerate the realizable sign vectors (faces) of the 12 gradients in R^3
     exactly, via isolation67.faces() (Fourier-Motzkin over Q, exact).
  4. For each face, embed its witness direction into the FULL 15-dim ambient
     configuration (cube 0 of FIVE frozen; cubes 1-4 of FIVE + the free cube
     are the 5*3 = 15 Cayley coordinates), as a direction moving ONLY the free
     cube, normalise, and count with the infinitesimal engine
     epscount.count_eps -- no step size, no sampling.

Exact arithmetic throughout: fractions.Fraction and sympy Rational only.  A
count_eps None is UNEVALUABLE (engine overflow-budget refusal), never scored as
"no improvement".  Chambers are not ranked by how many walls they touch -- this
project has refuted "more coincidences implies a higher count"; the engine
decides, always.
"""
import json, os, sys, time
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from base_points import FIVE, solve3
from size_local import base_arrangement, free_faces_edges, FREE
import dimension as D
import provenance
from epscount import count_eps
from isolation67 import faces as fm_faces


# --------------------------------------------------------- incidence lookup
# free_faces_edges(FREE) builds its 6 faces and 12 edges in a fixed, known
# order (size_local.py):
#   faces[fi]:  fi = 2*a + (0 if s==+1 else 1),  a in {0,1,2}, s in {+1,-1}
#   edges[ei]:  ei = 4*a + 2*(0 if sb==+1 else 1) + (0 if sc==+1 else 1)
# Decoding fi/ei back to (axis, sign(s)) lets the SAME face/edge be rebuilt
# symbolically from dimension.cayley_matrix, instead of only counted.

def face_axis_sign(fi):
    return fi // 2, (1 if fi % 2 == 0 else -1)


def edge_axis_signs(ei):
    a = ei // 4
    rem = ei % 4
    sb = 1 if rem < 2 else -1
    sc = 1 if rem % 2 == 0 else -1
    b, c = [t for t in range(3) if t != a]
    return a, b, c, sb, sc


def find_incident():
    """Re-run size_local's exact incidence test, keeping the hits (not just counting)."""
    real, lines, P = base_arrangement()
    faces_num, edges_num = free_faces_edges(FREE)

    w4_hits = []                       # (base triple point, face index)
    for pt in real:
        for fi, f in enumerate(faces_num):
            if sum(f[i] * pt[i] for i in range(3)) == 1:
                w4_hits.append((pt, fi))

    w3_hits = []                       # (line index, edge index, direction, base point)
    for li, (a, b, d) in enumerate(lines):
        n1, n2 = P[a][0], P[b][0]
        base_pt = None
        for k in range(3):
            e = [1 if t == k else 0 for t in range(3)]
            s = solve3((n1, P[a][1], 0), (n2, P[b][1], 0), (e, F(0), 0))
            if s is not None:
                base_pt = s
                break
        if base_pt is None:
            continue
        for ei, (Ppt, Dv) in enumerate(edges_num):
            W = [base_pt[i] - Ppt[i] for i in range(3)]
            det = (Dv[0] * (d[1] * W[2] - d[2] * W[1])
                   - Dv[1] * (d[0] * W[2] - d[2] * W[0])
                   + Dv[2] * (d[0] * W[1] - d[1] * W[0]))
            if det == 0:
                w3_hits.append((li, ei, d, base_pt))
    return w4_hits, w3_hits


# ------------------------------------------------- symbolic gradients at FREE
X, Y, Z = sp.symbols('x y z')
MC = D.cayley_matrix((X, Y, Z))          # free cube's rotation matrix as f(c)

_cf = D.cayley_of(FREE)                  # free cube's own Cayley point (Fraction triple)
POINT = {X: sp.Rational(_cf[0].numerator, _cf[0].denominator),
         Y: sp.Rational(_cf[1].numerator, _cf[1].denominator),
         Z: sp.Rational(_cf[2].numerator, _cf[2].denominator)}


def _rat(fr):
    return sp.Rational(fr.numerator, fr.denominator)


def w4_condition(pt, fi):
    """m(c).p - 1 = 0: free face plane (axis a, sign s) through base point pt."""
    a, s = face_axis_sign(fi)
    m = [s * MC[i, a] for i in range(3)]
    return sum(m[i] * _rat(pt[i]) for i in range(3)) - 1


def w3_condition(ei, d, base_pt):
    """det[D(c), d, W(c)] = 0: free edge (axis a) coplanar with base line."""
    a, b, c, sb, sc = edge_axis_signs(ei)
    Dv = [2 * MC[i, a] for i in range(3)]
    Ppt = [MC[i, b] * sb + MC[i, c] * sc - MC[i, a] for i in range(3)]
    bp = [_rat(t) for t in base_pt]
    W = [bp[i] - Ppt[i] for i in range(3)]
    # d's components are Fraction, not necessarily integer -- sp.Integer(Fraction)
    # truncates via int() (e.g. Fraction(180,361) -> 0), which silently zeroed
    # every W3 gradient the first time this was written.  Use _rat, always.
    dd = [_rat(t) for t in d]
    return (Dv[0] * (dd[1] * W[2] - dd[2] * W[1])
            - Dv[1] * (dd[0] * W[2] - dd[2] * W[0])
            + Dv[2] * (dd[0] * W[1] - dd[1] * W[0]))


def _to_fraction(e):
    e = sp.nsimplify(sp.together(sp.simplify(e)))
    if not e.is_Rational:
        raise ValueError('gradient component is not exactly rational: %s' % e)
    return F(int(e.p), int(e.q))


def gradient_and_gate(cond):
    """(gate_ok, grad) -- gate_ok iff cond itself is EXACTLY 0 at the free point."""
    val = sp.nsimplify(sp.together(sp.simplify(cond.subs(POINT))))
    gate_ok = (val == 0)
    grad = [_to_fraction(sp.diff(cond, v).subs(POINT)) for v in (X, Y, Z)]
    return gate_ok, grad


# --------------------------------------------------------------------- main
def main():
    log = open(os.path.join(HERE, 'extension_chambers.log'), 'a')
    def LOG(*a):
        print(*a)
        print(*a, file=log, flush=True)

    LOG('\n===== %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    t0 = time.time()

    # ---- full 15-dim ambient configuration: base FIVE's cubes 1..4 + FREE
    R6 = list(FIVE) + [FREE]
    D.set_field(0)
    D.QZERO[:] = [R6[0]]
    pt = D.point_of(R6)
    if pt is None:
        LOG('ABORT: point_of(R6) is None (Cayley infinity)'); return

    # ---- SANITY CHECK: the base configuration itself must count 727
    base_count = D.count_at(pt, len(R6))
    base_count_eps = count_eps(pt, None, 0, R6[0])
    LOG('sanity: D.count_at(727 point) = %s ; count_eps(zero direction) = %s'
        % (base_count, base_count_eps))
    if base_count != 727 or base_count_eps != 727:
        LOG('ABORT: base configuration does not count 727 -- stopping, not enumerating.')
        json.dump({'ABORT': 'base count != 727',
                   'count_at': base_count, 'count_eps_zero': base_count_eps},
                  open(os.path.join(HERE, 'extension_chambers.json'), 'w'), indent=1)
        return

    # ---- step 1: incident walls
    w4_hits, w3_hits = find_incident()
    LOG('incident walls found: %d W4 + %d W3 = %d' % (len(w4_hits), len(w3_hits),
                                                       len(w4_hits) + len(w3_hits)))

    # ---- step 1b/GATE + step-1-continued: symbolic gradients
    wall_info, walls = [], []
    gate_failures = []
    for pt4, fi in w4_hits:
        cond = w4_condition(pt4, fi)
        ok, grad = gradient_and_gate(cond)
        wall_info.append({'type': 'W4', 'face_index': fi,
                          'base_point': [str(v) for v in pt4],
                          'gate_ok': ok, 'grad': [str(v) for v in grad]})
        if not ok:
            gate_failures.append(wall_info[-1])
        else:
            walls.append(grad)
    for li, ei, d, base_pt in w3_hits:
        cond = w3_condition(ei, d, base_pt)
        ok, grad = gradient_and_gate(cond)
        wall_info.append({'type': 'W3', 'line_index': li, 'edge_index': ei,
                          'line_dir': [str(v) for v in d],
                          'base_point': [str(v) for v in base_pt],
                          'gate_ok': ok, 'grad': [str(v) for v in grad]})
        if not ok:
            gate_failures.append(wall_info[-1])
        else:
            walls.append(grad)

    if gate_failures:
        LOG('GATE FAILURE: %d of %d walls did NOT evaluate to exactly 0 at the '
            'free point -- wrong wall(s), stopping.' % (len(gate_failures), len(wall_info)))
        for g in gate_failures:
            LOG('   %s' % g)
        json.dump({'ABORT': 'GATE failure', 'gate_failures': gate_failures,
                   'wall_info': wall_info},
                  open(os.path.join(HERE, 'extension_chambers.json'), 'w'), indent=1)
        return
    LOG('GATE: all %d incident-wall conditions evaluate to exactly 0 at the free '
        'point. all gradients nonzero: %s'
        % (len(walls), all(any(g != 0 for g in w) for w in walls)))

    zero_walls = [i for i, w in enumerate(walls) if all(g == 0 for g in w)]
    if zero_walls:
        LOG('WARNING: %d wall gradient(s) are exactly zero (degenerate at this '
            'point): %s' % (len(zero_walls), zero_walls))

    # ---- step 2: enumerate faces of the 12-wall arrangement in R^3, exactly
    fs = fm_faces(walls, 3, F(0), log)
    LOG('realizable non-zero faces: %d' % len(fs))
    if len(fs) > 5000:
        LOG('ABORT: %d faces > ~5000 -- something is wrong with the gradients, '
            'not grinding through it.' % len(fs))
        json.dump({'ABORT': 'too many faces', 'n_faces': len(fs),
                   'wall_info': wall_info},
                  open(os.path.join(HERE, 'extension_chambers.json'), 'w'), indent=1)
        return

    # ---- step 3: count each face via the infinitesimal engine
    results = []
    hist = {}
    uneval = 0
    best = None
    best_entry = None
    for idx, (sigma, dvec) in enumerate(fs):
        full_dir = [F(0)] * 12 + list(dvec)
        dv_full = D.normalize_dir(full_dir)
        c = count_eps(pt, dv_full, 0, R6[0])
        entry = {'sigma': list(sigma), 'dir3': [str(v) for v in dvec],
                 'dir_full': [str(v) for v in dv_full], 'count': c}
        results.append(entry)
        if c is None:
            uneval += 1
        else:
            hist[c] = hist.get(c, 0) + 1
            if best is None or c > best:
                best = c
                best_entry = entry
        if (idx + 1) % 50 == 0 or idx + 1 == len(fs):
            LOG('   ... %d/%d faces counted (%d unevaluable so far)'
                % (idx + 1, len(fs), uneval))

    exceeds_727 = (best is not None and best > 727)
    hist_sorted = dict(sorted(hist.items(), reverse=True))

    LOG('\n===== RESULTS =====')
    LOG('incident walls: %d (%d W4 + %d W3)' % (len(walls), len(w4_hits), len(w3_hits)))
    LOG('realizable faces: %d' % len(fs))
    LOG('histogram (count -> #faces): %s' % hist_sorted)
    LOG('best count found: %s' % best)
    LOG('exceeds 727: %s' % exceeds_727)
    LOG('unevaluable faces (engine None): %d of %d' % (uneval, len(fs)))
    if best_entry is not None:
        LOG('best face: sigma=%s dir3=%s' % (best_entry['sigma'], best_entry['dir3']))
    LOG('elapsed: %.1fs' % (time.time() - t0))

    out = {
        'base_count': base_count,
        'incident_walls': len(walls),
        'incident_w4': len(w4_hits),
        'incident_w3': len(w3_hits),
        'gate_all_ok': True,
        'wall_info': wall_info,
        'n_faces': len(fs),
        'histogram': {str(k): v for k, v in hist_sorted.items()},
        'best_count': best,
        'exceeds_727': exceeds_727,
        'best_face': best_entry,
        'unevaluable': uneval,
        'faces': results,
        'secs': round(time.time() - t0, 1),
    }
    outpath = os.path.join(HERE, 'extension_chambers.json')
    json.dump(out, open(outpath, 'w'), indent=1)
    provenance.stamp(outpath,
                     note='local chambers of the 727 sixth cube in its own R^3 '
                          'Cayley space; exact incidence, exact gradients, '
                          'Fourier-Motzkin face enumeration, infinitesimal '
                          'count_eps -- no sampling, no step size')


if __name__ == '__main__':
    main()
