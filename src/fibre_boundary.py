#!/usr/bin/env python3
"""Where does the 1217 count plateau END, inside the fibre over 727?

THE MISTAKE THIS EXISTS TO CORRECT.  I reported the plateau at 1217 as a single
point because the count fell to 1213 at t = 1/64 along the surviving direction.
That step is 14x COARSER than the minimum feature at n = 7 (1.08e-3, P292), and
the claim was an artefact of it: at 1/1024 and below the count is 1217 again.
The plateau is real and the boundary sits between.  Exactly the failure mode the
project already records as "an infinitesimal is exact; a small number is a sample".

METHOD.  Bracket by SIMPLEST-RATIONAL bisection (METHODS 15), not by halving:
the quaternion height along a ray grows like 1/t, so midpoints of unrelated
denominators compound out of the engine's budget, while the simplest rational in
an interval keeps the representative cheap.  Every count is engine-exact.

WHAT A BRACKET IS AND IS NOT.  The boundary is where a wall is crossed, so it is
an algebraic number.  This returns a rational interval containing it, never the
locus.  Turning a bracket into a root needs the wall polynomial restricted to the
ray -- which `wall_keys.on_line` now provides, and which this file does not do.

HEIGHT GUARD.  Counts are taken with the narrow engine and re-taken with the wide
one whenever the height passes 512, the narrow engine's stated budget.  A
disagreement is reported, never averaged or ignored.
"""
import sys, os, json, subprocess
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import dimension as D
import wall_keys as W

NARROW = os.path.join(HERE, 'cube_regions_n')
WIDE = os.path.join(HERE, 'cube_regions_q2w')
BUDGET = 512


def _run(engine, qs):
    spec = ";".join(",".join(str(v) for v in c) for c in qs)
    o = subprocess.run([engine, "--quats", spec], capture_output=True, text=True).stdout
    i = o.find('"bounded":')
    return int(o[i + 10:o.find(",", i)]) if i >= 0 else None


def count_at(pt, dv, t, q0, n):
    p = [pt[i] + t * dv[i] for i in range(len(pt))]
    qs = D.quats_of(p, q0)
    h = max(abs(x) for c in qs for x in c)
    a = _run(NARROW, qs)
    if h > BUDGET:
        b = _run(WIDE, qs)
        if a is not None and b is not None and a != b:
            return ('DISAGREE %s/%s' % (a, b), h)
        return (b if a is None else a, h)
    return (a, h)


def simplest_between(lo, hi):
    """simplest rational strictly inside (lo, hi), by Stern-Brocot descent"""
    assert lo < hi
    for k in range(int(lo) + 1, int(hi) + 2):
        if lo < k < hi:
            return F(k)
    fl = lo.numerator // lo.denominator
    return fl + 1 / simplest_between(1 / (hi - fl), 1 / (lo - fl)) \
        if lo - fl != 0 else fl + 1 / simplest_between(1 / (hi - fl), F(10) ** 9)


def bracket(pt, dv, q0, n, target, kmax=22, refine=10):
    """(inside, outside) bracketing the boundary along dv.

    TWO STAGES, and the first is why the earlier version was void.  The plateau's
    scale was unknown across three orders of magnitude, and simplest-rational
    descent from (0, 1/4) walks `hi` down one UNIT FRACTION per step -- 1/5, 1/6,
    ... -- so fourteen steps reached 1/18 while the boundary sat near 1/1024, and
    every direction returned the same meaningless interval.  Identical answers
    across twelve different directions is a bug, not a measurement.

      stage 1  GEOMETRIC: halve from 1 until the count returns to target. This
               finds the SCALE, which linear descent cannot.
      stage 2  simplest-rational refinement inside that one octave, where the
               representatives stay cheap.
    """
    trail = []
    inside = None
    outside = F(1)
    for k in range(0, kmax + 1):
        t = F(1, 2 ** k)
        c, h = count_at(pt, dv, t, q0, n)
        trail.append({'t': '1/%d' % 2 ** k, 'count': str(c), 'height': h})
        if isinstance(c, str) or c is None:
            continue                    # unevaluated: never scored as a change
        if c == target:
            inside = t
            break
        outside = t
    if inside is None:
        return None, outside, trail
    lo, hi = inside, outside
    for _ in range(refine):
        try:
            m = simplest_between(lo, hi)
        except Exception:
            break
        if not (lo < m < hi):
            break
        c, h = count_at(pt, dv, m, q0, n)
        trail.append({'t': str(m), 'count': str(c), 'height': h})
        if isinstance(c, str) or c is None:
            break
        if c == target:
            lo = m
        else:
            hi = m
    return lo, hi, trail


def main():
    q7 = W.REC[7]
    D.set_field(0); D.QZERO[:] = [q7[0]]
    pt = D.point_of(q7)
    nc = len(pt)
    base, _ = count_at(pt, [F(0)] * nc, F(0), q7[0], 7)
    print('record count %s, ambient %d, fibre = coords %d,%d,%d'
          % (base, nc, nc - 3, nc - 2, nc - 1), flush=True)
    # Directions inside the fibre. e15 is the surviving direction; the diagonals
    # are included because an axis-only probe is the failure FAILURE_MODES 11d
    # records -- a plateau that is not axis-aligned reads as zero extent.
    dirs = {'+e15': (1, 0, 0), '-e15': (-1, 0, 0), '+e16': (0, 1, 0), '-e16': (0, -1, 0),
            '+e17': (0, 0, 1), '-e17': (0, 0, -1),
            '+d(1,1,1)': (1, 1, 1), '-d(1,1,1)': (-1, -1, -1),
            '+d(1,-1,0)': (1, -1, 0), '+d(0,1,-1)': (0, 1, -1),
            '+d(2,1,-3)': (2, 1, -3), '+d(1,-3,2)': (1, -3, 2)}
    out = {'what': 'boundary of the 1217 COUNT PLATEAU inside the fibre over 727',
           'corrects': ('an earlier claim that the plateau is a single point, which '
                        'came from a step of 1/64 -- 14x coarser than the n=7 minimum '
                        'feature of 1.08e-3 (P292)'),
           'IMPORTANT': ('every entry is a BRACKET containing an algebraic boundary, '
                         'never the boundary itself'),
           'record_count': str(base), 'directions': {}}
    for name, (a, b, c) in dirs.items():
        dv = [F(0)] * nc
        dv[nc - 3], dv[nc - 2], dv[nc - 1] = F(a), F(b), F(c)
        lo, hi, trail = bracket(pt, dv, q7[0], 7, base)
        if lo is None:
            out['directions'][name] = {'status': 'NO INSIDE POINT FOUND down to 1/2^22',
                                       'trail': trail}
            print('  %-11s no point of the plateau found down to 1/2^22' % name, flush=True)
            continue
        out['directions'][name] = {'inside_at': str(lo), 'outside_at': str(hi),
                                   'ratio': float(hi / lo), 'trail': trail}
        print('  %-11s inside at t=%-14s outside at t=%-14s (ratio %.2f)'
              % (name, lo, hi, float(hi / lo)), flush=True)
        json.dump(out, open(os.path.join(ROOT, 'data', 'fibre_boundary.json'), 'w'), indent=1)
    json.dump(out, open(os.path.join(ROOT, 'data', 'fibre_boundary.json'), 'w'), indent=1)
    print('written data/fibre_boundary.json')


if __name__ == '__main__':
    main()
