#!/usr/bin/env python3
"""Replace a chamber witness with the SIMPLEST point in the same chamber.

WHY.  Evaluating region counts on 727's chambers left 47% unevaluable: the exact
engine refused witnesses produced by the LP.  The failures separated by input
HEIGHT -- median 3.1e9 unevaluable against 1.1e7 evaluable -- which is
FAILURE_MODES 16's signature: the refusal is about the representative, not the
question.  A chamber is defined only up to which point of it you name, so the
cost of that point is a free choice.

WHAT DOES NOT WORK, measured before this was written (FAILURE_MODES 16b): a
chamber is a cone, so scaling a witness to integers is valid -- and it made things
WORSE, 50% evaluable down to 18%, because clearing denominators multiplies by the
LCM over coordinates whose denominators are unrelated.  "Make it an integer" and
"make it simple" point in opposite directions on a vector of unrelated rationals.

WHAT WORKS.  Coordinate descent with the continued-fraction choice.  Holding the
other coordinates fixed, the constraints restrict y_i to an open interval; replace
y_i by the SIMPLEST rational strictly inside it (`isolation67._pick`, the same
routine that fixed the midpoint problem in mode 16).  Simplifying one coordinate
moves the others' intervals, so iterate; each pass is exact and can only stay
inside the chamber.

Every step is verified by exact sign tests, and the function returns the ORIGINAL
witness unchanged if anything fails to verify -- a simplification that leaves the
chamber would be a wrong answer, not a slow one.
"""
from fractions import Fraction as F
from isolation67 import _pick


def _inside(rows, y, nc):
    return all(sum(r[t] * y[t] for t in range(nc)) > 0 for r in rows)


def height(y):
    return max(max(abs(F(v).numerator), abs(F(v).denominator)) for v in y)


def simplify(rows, y, nc, passes=4):
    """Simplest point found in the same open cone. Exact; never leaves it."""
    y = [F(v) for v in y]
    if not _inside(rows, y, nc):
        return y                                  # caller's point already bad
    for _ in range(passes):
        改 = False
        for i in range(nc):
            lo = hi = None
            ok = True
            for r in rows:
                a = F(r[i])
                b = sum(F(r[t]) * y[t] for t in range(nc) if t != i)
                if a == 0:
                    if b <= 0:
                        ok = False
                        break
                    continue
                bound = -b / a
                if a > 0:
                    lo = bound if lo is None or bound > lo else lo
                else:
                    hi = bound if hi is None or bound < hi else hi
            if not ok or (lo is not None and hi is not None and lo >= hi):
                continue
            cand = F(_pick(lo, hi))
            if cand == y[i]:
                continue
            old = y[i]
            y[i] = cand
            if _inside(rows, y, nc):
                改 = True
            else:
                y[i] = old                        # reject: exactness over progress
        if not 改:
            break
    return y
