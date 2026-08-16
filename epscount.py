#!/usr/bin/env python3
"""count(base + eps*direction) with eps a positive INFINITESIMAL, not a number.

This replaces the project's oldest sampled primitive.  Every displaced count so
far has been count(base + eps*d) for a finite eps chosen by hand or by halving,
and a finite eps measures the cell it happens to land in: at the golden 67, 333
of 2196 faces disagreed across three fixed step sizes purely because the coarsest
step left the face.  Here eps is an element of the ordered field Q(sqrt D)(eps)
-- smaller than every positive rational -- so the count returned IS the eps -> 0
limit, with no step size to choose and none to defend.

Cayley coordinate c_i(eps) = c_i + eps*d_i is degree 1 in eps, so after clearing
denominators the quaternion components are degree-1 polynomials over Z[sqrt D],
which is exactly what cube_regions_eps accepts ("p0:q0|p1:q1").
"""
import json, os, subprocess
from fractions import Fraction as F
from math import gcd

from qfield import Q

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'cube_regions_eps')


def _pair(x, d):
    x = x if isinstance(x, Q) else Q(F(x), 0, d)
    return x.a, x.b


def eps_quats(point, direction, d, q0=None):
    """quaternions of base + eps*direction, as engine component strings.

    The common denominator is cleared over the base AND direction parts together
    and the content divided out once over the whole quaternion: scaling a
    quaternion by a positive rational is a gauge freedom, but scaling one eps
    degree relative to another is NOT -- it would change the direction's length
    relative to the base point, which is the one thing eps must not depend on.
    """
    ncols = len(point)
    n = ncols // 3 + 1
    if direction is None:
        direction = [Q(0, 0, d)] * ncols
    L = 1
    vals = list(point) + list(direction)
    for v in vals:
        for part in _pair(v, d):
            L = L * part.denominator // gcd(L, part.denominator)
    groups = []
    q0 = q0 if q0 is not None else tuple(Q(F(t), 0, d) for t in (1, 0, 0, 0))
    L0 = 1
    for t in q0:
        for part in _pair(t, d):
            L0 = L0 * part.denominator // gcd(L0, part.denominator)
    groups.append([((int(_pair(t, d)[0] * L0), int(_pair(t, d)[1] * L0)), (0, 0))
                   for t in q0])
    for k in range(0, ncols, 3):
        comp = [((L, 0), (0, 0))]
        for r in range(3):
            b = _pair(point[k + r], d)
            g = _pair(direction[k + r], d)
            comp.append(((int(b[0] * L), int(b[1] * L)),
                         (int(g[0] * L), int(g[1] * L))))
        groups.append(comp)
    out = []
    for comp in groups:
        flat = [v for c in comp for pair in c for v in pair]
        g = 0
        for v in flat:
            g = gcd(g, abs(v))
        if g > 1:
            comp = [tuple(tuple(v // g for v in pair) for pair in c) for c in comp]
        out.append(','.join('%d:%d|%d:%d' % (c[0][0], c[0][1], c[1][0], c[1][1])
                            for c in comp))
    return ';'.join(out), n


def count_eps(point, direction, d, q0=None):
    """exact count at the infinitesimally displaced configuration, or None.

    None means the engine REFUSED (overflow budget or malformed input) and is
    returned as None so callers can count it as unevaluated.  It is never a
    stand-in for "the count did not change".
    """
    s, n = eps_quats(point, direction, d, q0)
    p = subprocess.run([ENG, '--d', str(d), '--quats', s],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])['bounded']
    except Exception:
        return None


def count_eps_err(point, direction, d, q0=None):
    """count plus the engine's stderr, for diagnosing a refusal"""
    s, n = eps_quats(point, direction, d, q0)
    p = subprocess.run([ENG, '--d', str(d), '--quats', s],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])['bounded'], ''
    except Exception:
        return None, (p.stderr or p.stdout)[:200]
