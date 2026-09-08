#!/usr/bin/env python3
"""Chamber count of the next rung WITHOUT building its lattice.

Stanley's modular factorisation theorem, in the form that makes it computable:
if X is a modular flat of L(A), then

    chi_A(t) = chi_{A_X}(t) . sum over Y with Y ^ X = 0  of  mu(0,Y) t^(rA - rX - rank Y)

A_X here is the previous rung's arrangement, embedded exactly (verified: all 27
of 727's walls appear verbatim in 1217's).  So the whole quotient depends only on
the flats COMPLEMENTARY to X -- those whose closed wall-set contains no old wall.

WHY THIS IS CHEAP, and it is the entire point.  The full lattice grows ~35x per
rung: 988 flats at 12 walls, 33 158 at 18, 1 192 678 at 27.  At 51 walls it is
far out of reach.  But complementary flats have rank at most rA - rX = 3, so the
search is over subsets of the NEW walls of size <= 3 -- thousands, not millions.

MOEBIUS IS EXACT HERE, not an approximation of the full lattice's.  Every flat
below a complementary Y is itself complementary (it has fewer walls, so still no
old ones), so the interval [0, Y] lies wholly inside the enumerated set and the
recursion mu(Y) = -sum_{Z<Y} mu(Z) gives the true value in L(A).

GATED on the previous rung: run with `gate` and it must return
g(t) = t^3 - 9t^2 + 30t - 22 with |g(-1)| = 62 for 393 c 727, reproducing P155's
quotient by a completely different route than dividing two polynomials.
"""
import json, os, sys, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from zaslavsky import Flats


def quotient(W_outer, n_outer, W_inner, n_inner, label='', log=sys.stdout):
    L = Flats(W_outer)
    m = L.m
    old = [i for i, w in enumerate(W_outer) if all(x == 0 for x in w[n_inner:])]
    new = [i for i in range(m) if i not in old]
    old_mask = 0
    for i in old:
        old_mask |= 1 << i
    # ranks
    b = []
    for i in range(m):
        L._add(b, L.w[i])
    rA = len(b)
    b = []
    for i in old:
        L._add(b, L.w[i])
    rX = len(b)
    Xb = [(pp, list(rr)) for pp, rr in b]
    deg = rA - rX
    print('%s outer %d walls rank %d | inner %d walls rank %d | quotient degree %d'
          % (label, m, rA, len(old), rX, deg), file=log, flush=True)

    # complementary flats: closures of subsets of `new` whose closure avoids all old walls
    comp = {}                       # mask -> rank
    bot, _ = L.closure_of_basis([]), 0
    comp[bot] = 0
    frontier = {bot: []}
    for depth in range(1, deg + 1):
        nxt = {}
        for Fm, basis in frontier.items():
            for j in new:
                if Fm >> j & 1:
                    continue
                bb = [(p, list(r)) for p, r in basis]
                L._add(bb, L.w[j])
                G = L.closure_of_basis(bb)
                if G & old_mask:            # pulls in an old wall: not complementary
                    continue
                if G not in comp:
                    comp[G] = depth
                    nxt[G] = bb
        frontier = nxt
        print('   rank %d: %d complementary flats (%d total)'
              % (depth, len(nxt), len(comp)), file=log, flush=True)

    # PRECONDITION GATE.  Stanley's identity holds only when X is MODULAR, and
    # nothing above checks that -- the sum below is a well-defined polynomial for
    # ANY X, it simply has no relation to chi_A/chi_{A_X} when the hypothesis
    # fails.  That is how this program reported 1 289 462 112 chambers for n=7 on
    # 2026-08-24 (LEDGER P158, retracted): correct arithmetic, inapplicable
    # theorem, and a number with a plausible shape.
    #
    # Modularity requires rank(X)+rank(Y) = rank(X v Y)+rank(X ^ Y) for every flat
    # Y.  On COMPLEMENTARY Y (X ^ Y = 0) that reduces to rank additivity, and the
    # complementary flats are already enumerated here -- so a necessary condition
    # costs seconds instead of the full lattice sweep that proved modularity at
    # the previous rung (1 192 678 flats, P156).  Measured: 0 violations for
    # 393 c 727, where modularity is proved; 11 of 263 for 727 c 1217, where the
    # direct LP measurement independently gives 666 leaves against a predicted 279.
    #
    # This gate REFUSES rather than warns.  A number that is wrong only under an
    # unstated hypothesis is more dangerous than no number.
    viol = 0
    for Ym, r in comp.items():
        if r == 0:
            continue
        jb = [(pp, list(rr)) for pp, rr in Xb]
        for k in range(m):
            if Ym >> k & 1:
                L._add(jb, L.w[k])
        if rX + r != len(jb):
            viol += 1
    if viol:
        raise SystemExit(
            '%s MODULARITY REFUTED: %d of %d complementary flats violate rank '
            'additivity rank(X)+rank(Y)=rank(X v Y). Stanley\'s factorisation does '
            'not apply, so no quotient is reported. chi_{A_X} need not divide '
            'chi_A here.' % (label, viol, len(comp) - 1))
    print('%s modularity precondition: 0 violations over %d complementary flats'
          % (label, len(comp) - 1), file=log, flush=True)

    # Moebius within the complementary sub-poset (exact: it is an order ideal)
    order = sorted(comp, key=lambda f: (comp[f], bin(f).count('1')))
    mu = {}
    for i, Fm in enumerate(order):
        mu[Fm] = 1 if i == 0 else -sum(mu[G] for G in order[:i] if G & Fm == G)
    coeffs = [0] * (deg + 1)
    for Fm, r in comp.items():
        coeffs[r] += mu[Fm]
    # g(t) = sum_r coeffs[r] t^(deg - r)
    g_at_minus1 = sum(c * (-1) ** (deg - r) for r, c in enumerate(coeffs))
    poly = ' + '.join('%d t^%d' % (c, deg - r) for r, c in enumerate(coeffs) if c)
    print('%s g(t) = %s   g(-1) = %d   |g(-1)| = %d'
          % (label, poly, g_at_minus1, abs(g_at_minus1)), file=log, flush=True)
    return coeffs, abs(g_at_minus1), len(comp)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'gate'
    C6 = BASE + [(7, 14, 1, -5)]
    C7 = C6 + [(4, -3, -4, -4)]
    if which == 'gate':
        W6, n6 = walls_of(C6); W3, n3 = walls_of(BASE)
        c, g, nf = quotient(W6, n6, W3, n3, label='393 c 727:')
        ok = (c == [1, -9, 30, -22] and g == 62)
        print('  expected [1,-9,30,-22], |g(-1)|=62 -> %s' % ('PASS' if ok else 'FAIL'))
        return 0 if ok else 1
    W7, n7 = walls_of(C7); W6, n6 = walls_of(C6)
    t0 = time.time()
    c, g, nf = quotient(W7, n7, W6, n6, label='727 c 1217:')
    pred = 4621728 * g
    print('\nPREDICTED chambers(1217) = 4,621,728 x %d = %s' % (g, '{:,}'.format(pred)))
    json.dump({'quotient_coeffs': c, 'abs_g_at_-1': g, 'n_complementary_flats': nf,
               'chambers_727': 4621728, 'predicted_chambers_1217': pred,
               'secs': time.time() - t0},
              open(os.path.join(HERE, 'quotient_1217.json'), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
