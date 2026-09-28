#!/usr/bin/env python3
"""The two sheets of the 1217 plateau near the record, mapped in the same (t, u) plane.  [P393]

THE QUESTION.  [P393] found that adding the record's seventh cube `4,-3,-4,-4` to points of BOTH
727 branches, D1 and D2, gives 1217 along a segment of each, and that the seventh cube can slide
along the fibre direction e15 over D2 points too.  So near the record the plateau is two sheets,
fibre x D1 (the pentagon of [P301]) and fibre x D2, sharing the fibre line over the record.  The
D1 sheet's outline is known; the D2 sheet's is not.

COORDINATES.  p(t, u) = record + t * (branch direction on the sixth cube) + u * e15, where e15 is
the first Cayley coordinate of the seventh cube (world frame, cube 0 frozen, `dimension.point_of`).
    D1: (-1, -1/7, 3/14)      D2: (-1, -4/21, 2/7)       t as in the TOWER node inset.

METHOD.  Lines in both directions of the plane, each started at a point KNOWN to count 1217 and
walked OUTWARD, so a bracket is the first departure from 1217 along that ray, never a far cell
that happens to count 1217 again:
    vertical lines   at fixed t, up and down the fibre   -> u_lo(t), u_hi(t)
    horizontal lines at fixed u, both ways along the branch -> t_lo(u), t_hi(u)
Horizontal lines catch what vertical ones cannot: a sheet that reaches beyond its u = 0 segment
at other heights, or a corner cut transverse to both directions (the failure [P301] records).
Outward walk: u = 2^-k for k = 22 down to 0 until the count leaves 1217; then simplest-rational
refinement ([METHODS 15]).  Every count is engine-exact; unevaluable counts are reported and
counted, never scored as a departure.  A bracket contains the boundary; it is not the locus.

WHAT THIS DOES NOT COVER.  Between the dyadic steps of the outward walk a departure thinner than
the step could be stepped over, so each bracket is the first departure SEEN.  The outline between
measured lines is not measured.  Only the plane spanned by e15 and the branch is examined.

GATE, the D1 sheet must reproduce what is on file:  u = 0 extent (-2/19, ~0.0497) [P303];
fibre at t = 0 up in (1/512, 1/266) and down in (4/89, 1/22) [P299]; and the cut corner, fibre
negative with base positive, whose third wall meets the base's upper end near normalised
a = -0.049 [P301].
"""
import sys, os, json
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import dimension as D, wall_keys as W, fibre_boundary as FB

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'data', 'n7_two_sheets.json')
TARGET = 1217
BRANCH = {'D1': (F(-1), F(-1, 7), F(3, 14)), 'D2': (F(-1), F(-4, 21), F(2, 7))}
# vertical lines: t values spread over each branch's u = 0 segment, D1 (-2/19, 0.0497),
# D2 (-0.135781, 0.0702) [P393]
T_LINES = {'D1': [F(-1, 10), F(-1, 12), F(-1, 16), F(-1, 25), F(-1, 50), F(0), F(1, 100),
                  F(1, 50), F(1, 30), F(1, 25), F(1, 21),
                  # second pass: the bottom-left corner, and the short 1215 wall near t = 1/50
                  F(-21, 200), F(-13, 125), F(1, 70), F(1, 60), F(1, 55), F(1, 45), F(1, 40), F(1, 35)],
           'D2': [F(-2, 15), F(-1, 8), F(-1, 10), F(-3, 31), F(-1, 15), F(-1, 30), F(0),
                  F(1, 50), F(1, 30), F(1, 20), F(1, 16), F(2, 29),
                  # second pass: the bottom-left corner, either side of the -3/31 slit
                  F(-27, 200), F(-67, 500), F(-97, 1000), F(-24, 250)]}
# horizontal lines: u values spread over the fibre extent at t = 0, (-0.045, 0.0025) [P299]
U_LINES = [F(-1, 23), F(-1, 25), F(-1, 33), F(-1, 50), F(-1, 100), F(-1, 200), F(0),
           F(1, 1000), F(1, 500),
           # second pass: below the P301 grid's bottom row (fibre -1 = -1/23)
           F(-1, 20), F(-1, 15), F(-1, 12), F(-1, 11), F(-1, 10), F(-2, 19)]


def setup():
    q = W.REC[7]
    D.set_field(0); D.QZERO[:] = [q[0]]
    return q[0], D.point_of(q)


def vec(nc, branch=None, fibre=0):
    v = [F(0)] * nc
    if branch:
        v[12:15] = list(BRANCH[branch])
    if fibre:
        v[15] = F(fibre)
    return v


def at(pt, t, u, branch):
    d = vec(len(pt), branch)
    return [pt[i] + t * d[i] + (u if i == 15 else 0) for i in range(len(pt))]


def middle(lo, hi):
    """simplest rational in the MIDDLE HALF of (lo, hi).

    Plain simplest-rational descent from (1/512, 1/256) returns 1/257, 1/258, ... and walks hi
    down one unit fraction per step: fourteen steps left every bracket at (1/512, 1/270) whatever
    the boundary, and identical brackets on unrelated lines were the tell.  Restricting to the
    middle half shrinks the bracket by at least 3/4 per step and keeps representatives cheap."""
    q = (hi - lo) / 4
    return FB.simplest_between(lo + q, hi - q)


def outward(q0, p0, d, refine=24):
    """first departure from TARGET along p0 + s d, s > 0, p0 known inside.

    Returns (inside, outside, unevaluated, trail)."""
    c0, _ = FB.count_at(p0, d, F(0), q0, 7)
    if c0 != TARGET:
        return None, None, 0, [{'s': '0', 'count': str(c0)}]
    trail, unev, inside, outside = [], 0, F(0), None
    for k in range(22, -1, -1):
        s = F(1, 2 ** k)
        c, h = FB.count_at(p0, d, s, q0, 7)
        trail.append({'s': str(s), 'count': str(c), 'height': h})
        if not isinstance(c, int):
            unev += 1
            continue
        if c == TARGET:
            inside = s
        else:
            outside, ocount = s, c
            break
    if outside is None:
        return inside, None, unev, trail            # held to s = 1: no departure in range
    lo, hi = inside, outside
    for _ in range(refine):
        m = middle(lo, hi)
        c, h = FB.count_at(p0, d, m, q0, 7)
        trail.append({'s': str(m), 'count': str(c), 'height': h})
        if not isinstance(c, int):
            unev += 1
            break                                   # stop honestly rather than guess a side
        if c == TARGET:
            lo = m
        else:
            hi, ocount = m, c
    trail.append({'outside_count': ocount})
    return lo, hi, unev, trail


def main():
    q0, pt = setup()
    nc = len(pt)
    cache = json.load(open(OUT)) if os.path.exists(OUT) else {}
    lines = cache.setdefault('lines', {})
    rec, _ = FB.count_at(pt, vec(nc), F(0), q0, 7)
    print('record count %s (must be %d)' % (rec, TARGET), flush=True)
    assert rec == TARGET
    jobs = []
    for b in BRANCH:
        for t in T_LINES[b]:
            for sg in (1, -1):
                jobs.append(('%s|t=%s|%s' % (b, t, 'u+' if sg > 0 else 'u-'), at(pt, t, 0, b), vec(nc, fibre=sg)))
        for u in U_LINES:
            for sg in (1, -1):
                d = [sg * x for x in vec(nc, b)]
                jobs.append(('%s|u=%s|%s' % (b, u, 't+' if sg > 0 else 't-'), at(pt, 0, u, b), d))
    for key, p0, d in jobs:
        if key in lines:
            continue
        lo, hi, unev, trail = outward(q0, p0, d)
        lines[key] = {'inside': str(lo) if lo is not None else None,
                      'outside': str(hi) if hi is not None else None,
                      'unevaluated': unev, 'outside_count': trail[-1].get('outside_count') if trail else None,
                      'trail': trail}
        json.dump(cache, open(OUT, 'w'), indent=1)
        print('%-24s  (%s, %s)  unevaluated %d' % (
            key, float(lo) if lo is not None else None, float(hi) if hi is not None else None, unev),
            flush=True)
    print('wrote data/n7_two_sheets.json')


if __name__ == '__main__':
    main()
