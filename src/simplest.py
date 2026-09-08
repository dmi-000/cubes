#!/usr/bin/env python3
"""The simplest rational strictly inside an interval, and its self-test.

Extracted from solve_more_ends.py so that climb.py can use it without importing that
module's whole endpoint-solver chain (catcache -> solve_ends -> the C9 catalogue).
solve_more_ends.py imports it from here, so there is one implementation and one
self-test, not two.
"""
from fractions import Fraction as F


def simplest_between(a, b):
    """Simplest rational strictly inside (a, b) — METHODS 15.

    A first version was a Stern-Brocot descent valid only for 0 < a < b. On the
    NEGATIVE side of the record it returned rationals OUTSIDE the interval, so the
    probes sampled the wrong cell and the walk sailed past the true endpoint,
    reporting -0.0606 where ground truth and `n78_ends.py` both say -0.04526. Self-
    tested below against known values before use.
    """
    import math
    if a > b:
        a, b = b, a
    if a == b:
        raise ValueError('empty interval')
    n = math.floor(a) + 1
    if a < n < b:
        return F(n)
    ia = math.floor(a)
    fa, fb = a - ia, b - ia
    if fa == 0:
        return ia + F(1, math.floor(1 / fb) + 1)
    return ia + 1 / simplest_between(1 / fb, 1 / fa)


def _selftest_simplest():
    cases = [(F(1, 3), F(1, 2), F(2, 5)), (F(-46, 1000), F(-452, 10000), None),
             (F(-1), F(1), F(0)), (F(1, 1000), F(26, 10000), None),
             (F(0), F(1, 7), None), (F(-2), F(-19, 10), None)]
    for a, b, want in cases:
        g = simplest_between(a, b)
        if not (min(a, b) < g < max(a, b)) or (want is not None and g != want):
            raise SystemExit('simplest_between self-test FAILED on (%s,%s) -> %s' % (a, b, g))


_selftest_simplest()
