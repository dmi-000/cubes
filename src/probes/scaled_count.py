#!/usr/bin/env python3
"""Region counts of a compound in which ONE cube is scaled by s (faces at distance s).  [P414]

For plan item 2 (shared face planes): shrinking or growing one cube of a shared pair by a tiny
factor breaks the 2-dimensional tie patches.  This asks whether some such tie-break never lowers
the count; if it doesn't, the shared-plane case would reduce to a compound with no shared plane
(though that compound is no longer congruent).  Built on sphere_count's exact D-set counter (DEPTH +
PIECES), which stays valid with shared planes: M_x(u) = max_f f.u / s_x.
"""
import os, sys, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import sphere_count as SC


class Scaled(SC.Compound):
    def __init__(self, quats, scales):
        super().__init__(quats, 'Q')
        self.s = [F(x) for x in scales]

    def beat_pieces(self, A, B):
        out = []
        for ts in itertools.product(range(6), repeat=len(B)):
            cons = []
            for b, t in zip(B, ts):
                tv = self.fc[b][t]
                cons += [(SC.sub(tv, f), False) for f in self.fc[b]]
                for a in A:
                    # M_a < M_b:  f.u / s_a < t.u / s_b  for every face f of a
                    cons += [([tv[k] / self.s[b] - f[k] / self.s[a] for k in range(3)], True)
                             for f in self.fc[a]]
            out.append((cons, self.frame(B[0], ts[0])))
        return out


def count(quats, scales=None):
    C = Scaled(quats, scales or [1] * len(quats))
    return C.count()


if __name__ == '__main__':
    import time
    qs = [(1, 0, 0, 0), (-13, 0, 0, -5), (6, -7, 7, 12), (1, 1, 7, -1)]
    for sc in ([1, 1, 1, 1], [1, F(999999, 1000000), 1, 1], [1, F(1000001, 1000000), 1, 1]):
        t = time.time(); print(sc, count(qs, sc), '%.1fs' % (time.time() - t))
