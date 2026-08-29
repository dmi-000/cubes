#!/usr/bin/env python3
"""Exact chamber counts by MEMOISED NBC recursion — no chamber is ever built.

THEORY.  For a real central arrangement, Zaslavsky's theorem plus Whitney's
gives  chambers = number of NBC subsets  (independent sets containing no broken
circuit, a circuit minus its least element).  Scanning elements from the LAST
index downward, an element f may be either taken or skipped exactly when
f is NOT in the closure of the already-taken set T (all of whose elements exceed
f); if f IS in that closure, both branches die -- skipping f makes a broken
circuit, and taking it makes a dependent set.  So:

    N(i, F) = 0                          if wall i lies in flat F
    N(i, F) = N(i-1, F) + N(i-1, cl(F + i))   otherwise
    N(-1, F) = 1

MEMOISATION IS THE WHOLE POINT.  The recursion depends on the taken set only
through its CLOSURE, so states are (index, flat) pairs and there are at most
m x |L(A)| of them.  Without it this enumerates one node per NBC set -- 4.7M for
727, the chamber count itself, which is no better than the enumeration already
running.  With it the cost is the size of the intersection lattice, and these
arrangements are degenerate, so that is far smaller.

WHY NOT THE MOEBIUS ROUTE.  Built first, and abandoned on measurement: the flat
enumeration is fine (183: 988 flats, 4.4s, correct 1 712) but recovering mu needs
sum over G < F for every flat F, which is O(|L|^2) subset tests -- 393 reached
23 699 flats, so ~5.6x10^8 tests, and 727 would be far worse.  This recursion
computes the same number in O(m x |L|) without ever forming mu.

GATES.  183 = 1 712 and 393 = 74 544, both from independent enumeration
(P146, P148), must pass before this is believed on 727.
"""
import json, os, sys, time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


class Flats:
    """Closure operator on wall index sets, with caching. Exact rational."""

    def __init__(self, walls):
        self.w = [[F(x) for x in row] for row in walls]
        self.m = len(walls)
        self.n = len(walls[0])
        self._cl = {}
        self._basis = {}
        self.empty = self.closure_of_basis([])

    @staticmethod
    def _reduce(basis, v):
        v = list(v)
        for p, row in basis:
            if v[p]:
                f = v[p]
                v = [a - f * b for a, b in zip(v, row)]
        return v

    @classmethod
    def _add(cls, basis, v):
        r = cls._reduce(basis, v)
        for i, x in enumerate(r):
            if x:
                basis.append((i, [a / x for a in r]))
                basis.sort()
                return True
        return False

    def closure_of_basis(self, basis):
        mask = 0
        for j in range(self.m):
            if not any(self._reduce(basis, self.w[j])):
                mask |= 1 << j
        self._basis.setdefault(mask, [list(b) for b in basis])
        return mask

    def extend(self, mask, j):
        """closure(flat mask + wall j)"""
        key = (mask, j)
        hit = self._cl.get(key)
        if hit is not None:
            return hit
        basis = [tuple(b) for b in self._basis[mask]]
        basis = [(p, list(r)) for p, r in basis]
        self._add(basis, self.w[j])
        out = self.closure_of_basis(basis)
        self._cl[key] = out
        return out


def chambers(walls, log=sys.stdout, label=''):
    t0 = time.time()
    L = Flats(walls)
    m = L.m
    memo = {}
    sys.setrecursionlimit(10000)

    def N(i, flat):
        if i < 0:
            return 1
        key = (i, flat)
        got = memo.get(key)
        if got is not None:
            return got
        if flat >> i & 1:
            memo[key] = 0
            return 0
        r = N(i - 1, flat) + N(i - 1, L.extend(flat, i))
        memo[key] = r
        return r

    total = N(m - 1, L.empty)
    print('%s chambers = %s   (%d states, %d flats, %.1fs)'
          % (label, '{:,}'.format(total), len(memo), len(L._basis),
             time.time() - t0), file=log, flush=True)
    return total, len(memo), len(L._basis), time.time() - t0


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'gate'
    import arrangement as A
    from growth727 import walls_of, BASE
    if which == 'gate':
        ok = True
        W, nc = A._record183_walls(sys.stderr)
        n, _, _, _ = chambers(W, label='183:')
        ok &= n == 1712
        print('  183 %s (expect 1,712)' % ('PASS' if n == 1712 else 'FAIL'))
        W, nc = walls_of(BASE)
        n, _, _, _ = chambers(W, label='393:')
        ok &= n == 74544
        print('  393 %s (expect 74,544)' % ('PASS' if n == 74544 else 'FAIL'))
        print('GATE %s' % ('PASS' if ok else 'FAIL'))
        return 0 if ok else 1
    cfg = BASE if which == '393' else BASE + [(7, 14, 1, -5)]
    W, nc = walls_of(cfg)
    n, st, fl, secs = chambers(W, label='%s:' % which)
    json.dump({'label': which, 'chambers': n, 'states': st, 'flats': fl,
               'secs': secs, 'method': 'memoised NBC recursion (Zaslavsky/Whitney)'},
              open(os.path.join(HERE, 'zaslavsky_%s.json' % which), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())


def charpoly(walls, log=sys.stdout, label=''):
    """The characteristic polynomial, not just chambers = |chi(-1)|.

    Same recursion as `chambers`, tracking NBC sets BY SIZE:
        chi(t) = sum over NBC sets S of (-1)^|S| t^(n-|S|)
    The Whitney numbers are what carry the structure; chi(-1) collapses them to
    one integer, which is why two arrangements can share a chamber count factor
    (393 and 727 both carry 1553) with no increment showing that factor.

    Returns (w, chambers) where w[k] = number of NBC sets of size k.
    """
    t0 = time.time()
    L = Flats(walls)
    m = L.m
    memo = {}
    sys.setrecursionlimit(10000)

    def N(i, flat):
        if i < 0:
            return (1,)
        key = (i, flat)
        got = memo.get(key)
        if got is not None:
            return got
        if flat >> i & 1:
            memo[key] = ()
            return ()
        a = N(i - 1, flat)
        b = N(i - 1, L.extend(flat, i))
        out = [0] * max(len(a), len(b) + 1)
        for k, v in enumerate(a):
            out[k] += v
        for k, v in enumerate(b):
            out[k + 1] += v
        out = tuple(out)
        memo[key] = out
        return out

    w = N(m - 1, L.empty)
    tot = sum(w)
    print('%s Whitney numbers %s  -> chambers %s  (%.1fs)'
          % (label, list(w), '{:,}'.format(tot), time.time() - t0),
          file=log, flush=True)
    return w, tot
