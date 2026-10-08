#!/usr/bin/env python3
"""Per-direction lemma for PROOF_SHARED's local inequality (L), by exhaustive enumeration.  [P419]

(L) is a sum over directions θ around a vertex v of the "end" indicators
`e_A(θ) = [θ ∈ A] · [A does not contain both sides of θ]`. Near θ, only the cubes tying AT θ
matter. With δ their common distance, each such cube's nearest point is:

    l  at θ − δ only        (distance falls going left, rises going right)
    r  at θ + δ only
    w  at both              (θ bisects two of its own points: a local maximum)
    m  at θ itself          (δ = 0: its own point, a minimum)
    M  at θ + 180° only     (δ = 180°: every point it owns is the antipode)

Cubes not tying at θ are strictly Above or Below there.
- Equal type means a shared point:
  - the `l ∪ w` cubes all own `θ − δ`;
  - the `r ∪ w` cubes all own `θ + δ`.
- So at most one `w`, or two `w` cubes would share two points and be one cube.
- With `δ = 0`, every tying cube is `m`; with `δ = 180°`, every one is `M`.

This enumerates EVERY type for 4 cubes, so it is exhaustive, not a sample. It checks:

    four-fold (all four tie at v):  W  = Σ_S e_{B_S} − e_μ − 2·e_C12  >= 0
    triple (three tie, one Above):  D  = Σ_pairs e_π − e_τ − e_β      >= 0

Notation: μ = level 2-3, C12 = level 3-4 (innermost); τ / β = the triple's top / bottom; π = pair
ties. Values are tabulated by the sharing the type implies (the owner sets of `θ ∓ δ`).

**Must-fail control.** Without sharing or with one shared pair, both are EQUALITIES
(PROOF_SHARED §4). The script asserts:
- W = D = 0 on every type implying at most one sharing pair;
- some type implying more sharing gives W > 0 or D > 0.
Output: data/direction_types.json.
"""
import os, sys, json, itertools, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CUBES = 'abcd'


def value(t, side):
    """distance of a cube of type t, on side L (just left), 0 (at θ), R (just right); larger =
    more OUTER.  The common δ is 0; the step is 1."""
    if t == 'A':
        return 10
    if t == 'B':
        return -10
    if side == '0':
        return 0
    if t == 'm':
        return 1                                  # a minimum: rises both ways
    if t in 'wM':
        return -1                                 # a maximum: falls both ways
    if side == 'L':
        return 1 if t == 'r' else -1              # l falls going left
    return 1 if t == 'l' else -1                  # r falls going right


def end(U, j, typ):
    def tie(side):
        v = sorted((value(typ[x], side) for x in U), reverse=True)
        return v[j - 1] == v[j]
    return int(tie('0') and not (tie('L') and tie('R')))


def implied_pairs(typ):
    """sharing pairs the type forces: owners of θ−δ and of θ+δ (or of θ, or of the antipode)."""
    groups = [[x for x in typ if typ[x] in 'lw'], [x for x in typ if typ[x] in 'rw'],
              [x for x in typ if typ[x] == 'm'], [x for x in typ if typ[x] == 'M']]
    return {p for g in groups for p in itertools.combinations(sorted(g), 2)}


def types():
    for assign in itertools.product('lrwmMAB', repeat=4):
        typ = dict(zip(CUBES, assign))
        X = [x for x in CUBES if typ[x] not in 'AB']
        if len(X) < 2 or assign.count('w') > 1:
            continue
        kinds = {typ[x] for x in X}
        if ('m' in kinds or 'M' in kinds) and len(kinds) > 1:
            continue                              # δ = 0 or 180° is shared by all tying cubes
        yield typ, X


def main():
    four, triple = collections.Counter(), collections.Counter()
    bad = []
    for typ, X in types():
        pairs = implied_pairs(typ)
        cls = 'pairs=%d' % len(pairs)
        # four-fold vertex: all four tie AT v, but at a direction θ any subset ties and the rest
        # are strictly Above or Below -- so every type counts.  (A first version required all
        # four to tie at θ itself, which is the wrong scope, and was fixed before any use.)
        if True:
            W = (sum(end(S, 2, typ) for S in itertools.combinations(CUBES, 3))
                 - end(CUBES, 2, typ) - 2 * end(CUBES, 3, typ))
            four[(cls, W)] += 1
            if W < 0 or (len(pairs) <= 1 and W != 0):
                bad.append(('four', typ, W))
        if typ['d'] == 'A':                       # triple vertex abc, d outer (at v, so everywhere near)
            T = 'abc'
            D = (sum(end(p, 1, typ) for p in itertools.combinations(T, 2))
                 - end(T, 1, typ) - end(T, 2, typ))
            triple[(cls, D)] += 1
            if D < 0 or (len(pairs) <= 1 and D != 0):
                bad.append(('triple', typ, D))
    for name, c in (('four-fold W', four), ('triple D', triple)):
        print(name + ':')
        for k in sorted({k for k, _ in c}):
            print('   %-8s %s' % (k, sorted((v, n) for (kk, v), n in c.items() if kk == k)))
    control = any(v > 0 for (k, v) in four if k != 'pairs=0' and k != 'pairs=1') and \
              any(v > 0 for (k, v) in triple if k not in ('pairs=0', 'pairs=1'))
    print('violations (negative, or nonzero with <= 1 pair): %d' % len(bad))
    print('control (some multi-sharing type has positive slack): %s' % control)
    assert not bad and control
    json.dump({'four': {'%s|%d' % k: n for k, n in four.items()},
               'triple': {'%s|%d' % k: n for k, n in triple.items()},
               'violations': len(bad), 'control': control},
              open(os.path.join(ROOT, 'data', 'direction_types.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
