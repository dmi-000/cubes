#!/usr/bin/env python3
"""The circle lemma of [P405], tested outside the cube pipeline, with a control that must fail.

LEMMA.  Colour points on a circle (one colour per cube; all points of all colours on ONE circle,
which is what congruent concentric cubes give: every projected facet normal has length
sqrt(1 - 1/|p|^2)).  Let h_i(w) = max over i's points v of v.w.
  bottom: argmax_i h_i -- changes = colour changes around the circle
  top:    argmin_i h_i -- changes must be <= the bottom's
  four colours: at least 4 colour changes (so C12 >= 4 > 3 at a four-fold point)
NOT exact: angles are rational, but the envelope is SAMPLED at 63 points between consecutive
critical angles (the points and their antipodes), so two switches inside one interval could be
missed.  This is a sanity check of an analytic proof, with a control; it is not the proof.
CONTROL: the same test with each colour on its OWN radius (Step T's blades) must show violations.
"""
import random, math, sys
from fractions import Fraction as Fr


def switches(pts, which, radii=None):
    """pts: list of (angle in turns, colour).  which='top' (argmin h) or 'bottom' (argmax h)."""
    cols = sorted({c for _, c in pts})
    crit = sorted({a for a, _ in pts} | {(a + Fr(1, 2)) % 1 for a, _ in pts})
    # every pairwise equality h_i = h_j is also critical; sample densely between critical angles
    samples = []
    for k in range(len(crit)):
        a, b = crit[k], crit[(k + 1) % len(crit)] + (1 if k + 1 == len(crit) else 0)
        for m in range(1, 64):
            samples.append(a + (b - a) * Fr(m, 64))
    def h(c, t):
        return max((radii[c] if radii else 1) * math.cos(2 * math.pi * float(t - a)) for a, cc in pts if cc == c)
    seq = []
    for t in samples:
        vals = {c: h(c, t) for c in cols}
        pick = (min if which == 'top' else max)(vals, key=vals.get)
        if not seq or seq[-1] != pick:
            seq.append(pick)
    if len(seq) > 1 and seq[0] == seq[-1]:
        seq.pop()
    return len(seq) if len(seq) > 1 else 0


def colour_changes(pts):
    s = [c for _, c in sorted(pts)]
    return sum(1 for i in range(len(s)) if s[i] != s[i - 1])


def main():
    rnd = random.Random(20260930)
    viol = ctrl_viol = four_bad = 0
    N = 3000
    for _ in range(N):
        pts = [(Fr(rnd.randrange(360), 360), c) for c in range(3) for _ in range(rnd.randint(1, 3))]
        if len({a for a, _ in pts}) < len(pts):
            continue                                    # coincident points = shared face plane
        top, bot = switches(pts, 'top'), switches(pts, 'bottom')
        viol += top > bot
        radii = {c: rnd.choice([0.3, 1.0, 3.0]) for c in range(3)}
        ctrl_viol += switches(pts, 'top', radii) > switches(pts, 'bottom', radii)
        pts4 = pts + [(Fr(rnd.randrange(360), 360), 3)]
        if len({a for a, _ in pts4}) == len(pts4):
            four_bad += colour_changes(pts4) < 4
    print('common circle: top > bottom in %d of %d sets (must be 0)' % (viol, N))
    print('CONTROL, own radii (Step T blades): top > bottom in %d (must be > 0)' % ctrl_viol)
    print('four colours: fewer than 4 colour changes in %d (must be 0)' % four_bad)
    sys.exit(1 if viol or not ctrl_viol or four_bad else 0)


if __name__ == '__main__':
    main()
