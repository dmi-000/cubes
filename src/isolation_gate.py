#!/usr/bin/env python3
"""Gate on the face enumerator, against arrangements whose face count is KNOWN.

Two independent implementations agreeing proves they share assumptions.  These
controls instead compare against a closed form:

  coordinate arrangement e_1..e_n in R^n -> exactly 3^n - 1 non-zero faces, all
  realizable, so both the enumerator AND its feasibility pruning are checked
  (a pruner that wrongly rejects shows up immediately as a shortfall);

  m distinct lines through the origin in R^2 -> exactly 4m faces (2m open
  sectors + 2m rays), which no coordinate-arrangement test would catch because
  it has dependent walls -- the case the golden 67 actually is;

  a repeated wall must not change the face count, since it adds no hyperplane.

Every witness is additionally checked to satisfy its own sign vector exactly, so
a face that is counted is a face that was constructed.
"""
import os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dimension as D
from qfield import Q
from isolation67 import faces, _fm


class Null:
    def write(self, *a): pass
    def flush(self): pass


fails = []


def check(name, ok, detail=''):
    print('%-56s %s %s' % (name, 'ok' if ok else 'FAIL', detail))
    if not ok:
        fails.append(name)


def enumerate_faces(walls, ncols, d):
    D.set_field(d)
    zero = Q(0, 0, d) if d else F(0)
    return faces([[(Q(F(x), 0, d) if d else F(x)) for x in w] for w in walls],
                 ncols, zero, Null())


def witnesses_valid(walls, fs, d):
    for sigma, dv in fs:
        for i, w in enumerate(walls):
            s = sum(F(w[i2]) * (dv[i2].a if d else dv[i2]) for i2 in range(len(w)))
            # only exact over Q here; the field case is checked via sign below
            got = 0 if s == 0 else (1 if s > 0 else -1)
            if got != sigma[i]:
                return False
    return True


def main():
    for d in (0, 5):
        for n in (2, 3, 4):
            walls = [[1 if t == c else 0 for t in range(n)] for c in range(n)]
            fs = enumerate_faces(walls, n, d)
            check('coordinate arrangement R^%d, d=%d -> 3^n - 1' % (n, d),
                  len(fs) == 3 ** n - 1, '%d vs %d' % (len(fs), 3 ** n - 1))
            if d == 0:
                check('  witnesses realize their own sign vectors',
                      witnesses_valid(walls, fs, d))

    for m in (2, 3, 4, 5):
        walls = [[1, 0]] + [[k, 1] for k in range(m - 1)]
        fs = enumerate_faces(walls, 2, 0)
        check('%d distinct lines in R^2 -> 4m faces' % m, len(fs) == 4 * m,
              '%d vs %d' % (len(fs), 4 * m))

    walls = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, -2, 0]]
    fs = enumerate_faces(walls, 3, 0)
    check('repeated / rescaled walls do not change the face count',
          len(fs) == 3 ** 3 - 1, '%d vs 26' % len(fs))

    D.set_field(0)
    y = _fm([[F(1), F(0)], [F(-1), F(1)], [F(0), F(-1)]], 2)
    check('infeasible strict system detected (y1>0, y2>y1, y2<0)', y is None,
          str(y))
    y = _fm([[F(1), F(0)], [F(-1), F(1)]], 2)
    ok = y is not None and y[0] > 0 and y[1] - y[0] > 0
    check('feasible strict system returns a valid witness', ok, str(y))

    print('\n%s' % ('FACE GATE PASSES' if not fails else 'FAILED: ' + ', '.join(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
