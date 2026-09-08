#!/usr/bin/env python3
"""Chamber counts by DERIVATION: Zaslavsky's theorem on the intersection lattice.

WHY.  Three days of this project have been spent ENUMERATING chambers -- 4.7M of
them for 727, at two exact LP calls apiece, over days of wall-clock.  Zaslavsky's
theorem gives the same number from the intersection lattice of the wall normals:

    number of chambers of a real central arrangement  =  sum |mu(0, x)|
                                                        x in L(A)

L(A) is the lattice of FLATS -- subspaces obtained by intersecting walls -- ordered
by reverse inclusion, and mu is its Moebius function.  No chamber is ever
constructed.  Search yields lower bounds forever; only derivation gives an answer
that cannot be improved by running longer.

WHY IT SHOULD BE CHEAP HERE, and this is the part measured rather than assumed:
these arrangements are extremely DEGENERATE.  Their realised fractions of the
Zaslavsky/Buck bound are 47% (183), 34% (393), ~6% (727) -- P151.  Degeneracy means
many subsets of walls collapse to the same flat, so the lattice is far smaller than
the generic sum-of-binomials.  The property that made enumeration expensive is the
property that should make this cheap.

GATES, NOT OPTIONAL.  183 must return 1 712 and 393 must return 74 544 -- both
established by independent enumeration (P146, P148) -- before this is pointed at
727, whose answer is not yet known.  A method validated only on the case it was
built for is not validated (FAILURE_MODES 18).

REPRESENTATION.  A flat is stored as the frozenset of wall indices whose
hyperplanes contain it -- its CLOSURE.  This makes flats canonical (two subsets
spanning the same subspace give the same key) and containment a set test.  All
arithmetic is exact rational; no floating point decides anything.
"""
import json, os, sys, time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _reduce(basis, v):
    """Reduce v against a list of (pivot, row); return the residual."""
    v = list(v)
    for p, row in basis:
        if v[p]:
            f = v[p]
            v = [a - f * b for a, b in zip(v, row)]
    return v


def _add(basis, v):
    """Add v to the basis if independent. True if the rank grew."""
    r = _reduce(basis, v)
    for i, x in enumerate(r):
        if x:
            row = [a / x for a in r]
            basis.append((i, row))
            return True
    return False


def _span_basis(walls, idxs):
    b = []
    for i in idxs:
        _add(b, walls[i])
    return b


def closure(walls, idxs):
    """(closed wall set, rank) -- every wall whose hyperplane contains the flat."""
    b = _span_basis(walls, idxs)
    cl = [j for j in range(len(walls)) if not any(_reduce(b, walls[j]))]
    return frozenset(cl), len(b)


def lattice(walls, log=sys.stdout):
    """All flats, by rank. Returns {flat: rank}."""
    m = len(walls)
    zero, r0 = closure(walls, [])          # walls containing the whole space
    flats = {zero: r0}
    level = [zero]
    t0 = time.time()
    while level:
        nxt = []
        for Fset in level:
            for j in range(m):
                if j in Fset:
                    continue
                G, rk = closure(walls, list(Fset) + [j])
                if G not in flats:
                    flats[G] = rk
                    nxt.append(G)
        if nxt:
            print('   rank %2d: %8d new flats (%6d total, %.0fs)'
                  % (flats[nxt[0]], len(nxt), len(flats), time.time() - t0),
                  file=log, flush=True)
        level = nxt
    return flats


def chambers_from_lattice(flats, log=sys.stdout):
    """Zaslavsky: chambers = sum |mu(0,x)|.  mu by the defining recursion."""
    order = sorted(flats, key=lambda f: (flats[f], len(f)))
    mu = {}
    total = 0
    for i, Fset in enumerate(order):
        s = 0
        for G in order[:i]:
            if G < Fset:
                s += mu[G]
        mu[Fset] = 1 if not mu else -s
        total += abs(mu[Fset])
    return total, mu


def run(label, walls, ncols, log=sys.stdout):
    t0 = time.time()
    print('%s: %d walls, ambient %d' % (label, len(walls), ncols), file=log, flush=True)
    fl = lattice(walls, log)
    print('   %d flats, building Moebius...' % len(fl), file=log, flush=True)
    n, mu = chambers_from_lattice(fl, log)
    print('%s: CHAMBERS = %s   (%d flats, %.1fs)'
          % (label, '{:,}'.format(n), len(fl), time.time() - t0), file=log, flush=True)
    return n, len(fl), time.time() - t0


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'gate'
    import arrangement as A
    from growth727 import walls_of, BASE
    KNOWN = {'183': 1712, '393': 74544}
    if which == 'gate':
        ok = True
        W, nc = A._record183_walls(sys.stderr)
        n, nf, _ = run('183', [[F(x) for x in w] for w in W], nc)
        ok &= (n == KNOWN['183'])
        print('  183 %s (expect %d)' % ('PASS' if n == KNOWN['183'] else 'FAIL', KNOWN['183']))
        W, nc = walls_of(BASE)
        n, nf, _ = run('393', [[F(x) for x in w] for w in W], nc)
        ok &= (n == KNOWN['393'])
        print('  393 %s (expect %d)' % ('PASS' if n == KNOWN['393'] else 'FAIL', KNOWN['393']))
        print('GATE %s' % ('PASS' if ok else 'FAIL'))
        return 0 if ok else 1
    cfg = BASE if which == '393' else BASE + [(7, 14, 1, -5)]
    W, nc = walls_of(cfg)
    n, nf, secs = run(which, [[F(x) for x in w] for w in W], nc)
    json.dump({'label': which, 'chambers': n, 'n_flats': nf, 'secs': secs},
              open(os.path.join(HERE, 'charpoly_%s.json' % which), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
