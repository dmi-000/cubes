#!/usr/bin/env python3
"""Independent seed for the (0,10,0) dimension probe -- [P279]'s control gap.

[P279]'s two seeds were octahedrally equivalent two-sided, so realisation 2's
codimension rested on ONE pair.  Candidates here come from the OTHER (0,10,0)
configurations found in P277's axis survey, and each is CHECKED for
non-equivalence to (5,2,2,1) before it is used -- absolute-value multiset first
(cheap and decisive when it differs), then the full two-sided octahedral test.

Chosen for distance from the original rather than convenience: (4,7,-7,-18) has a
component of 18 against the seed's largest of 5, so it is the member of the
available set furthest from the easy case along the axis the probe could be wrong
about (lattice richness near small quaternions).
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from congruent import OCT, qmul, canon

ORIG = (5, 2, 2, 1)


def equivalent(a, b):
    ca = canon(b)
    return any(canon(qmul(qmul(g, a), h)) == ca for g in OCT for h in OCT)


CANDS = [(-2, 5, -3, 3), (4, 7, -7, -18), (0, 5, -4, -4)]
print(f"original seed {ORIG}, abs-multiset {sorted(map(abs, ORIG))}\n")
chosen = []
for q in CANDS:
    det = pair_detail([(1, 0, 0, 0), q])
    c = det.get((0, 1), collections.Counter())
    sig = (c[2], c[4], c[6])
    eq = equivalent(ORIG, q)
    print(f"  {str(q):18s} abs {str(sorted(map(abs, q))):16s} signature {sig} "
          f"weight {c[4] + 2 * c[6]:>3}   equivalent to seed: {eq}")
    if sig == (0, 10, 0) and not eq:
        chosen.append(q)
print(f"\nusable independent (0,10,0) seeds: {chosen}")

for q0 in chosen[:1]:
    hits = []
    tally = collections.Counter()
    for d in itertools.product(range(-3, 4), repeat=4):
        q = tuple(a + b for a, b in zip(q0, d))
        if not any(q):
            continue
        try:
            det = pair_detail([(1, 0, 0, 0), q])
        except Exception:
            continue
        c = det.get((0, 1), collections.Counter())
        sig = (c[2], c[4], c[6])
        tally[(c[4] + 2 * c[6], sig)] += 1
        if sig == (0, 10, 0):
            hits.append(q)
    print(f"\nseed {q0}: +-3 box, {sum(tally.values())} points")
    print(f"  (0,10,0) neighbours: {len(hits)}   [P279]'s seed gave 77]")
    for h in hits[:8]:
        print(f"     {h}")
    top = sorted(tally.items(), key=lambda kv: -kv[1])[:5]
    print(f"  most common (weight, signature): {top}")
    print("\n  DIFFERENT counts from 77 => genuinely independent measurement.")
    print("  IDENTICAL again => still the same pair, and the check above is wrong.")
