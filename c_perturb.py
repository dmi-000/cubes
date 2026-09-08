#!/usr/bin/env python3
"""Is c_ell > 1 a DEGENERATE condition?  Decide it by perturbation, not by counting.

A degeneracy is a closed, measure-zero condition: it is destroyed by a generic
arbitrarily small move.  If c = 2 survives random perturbation at every scale,
then c = 2 holds on an OPEN set and is not a degeneracy, whatever else it is.

This is the right test and the counting was not, for a reason worth stating: the
c = 2 instances were found by sampling INTEGER quaternions, and integer sampling
hits rational measure-zero loci with positive probability.  So "0.4% of random
draws have c = 2" is NOT evidence that the c=2 set has positive measure.  Only
perturbation settles it.

Prediction, if the double-cover reading of [P269] is right: the Z/2 monodromy of a
free involution is LOCALLY CONSTANT -- it cannot change under a small move unless
the graph's topology changes -- so c = 2 must survive.  If instead c collapses to
1 under the first perturbation, the reading is wrong and c > 1 is degenerate.
"""
import collections, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph, shares_plane, parse, engine

SEEDS = [
    ("1,0,0,0;1,5,10,15;1,2,4,6;8,7,14,21", 1),
    ("1,0,0,0;-23,-90,43,22;72,-37,-17,-2;-4,4,-79,25", 1),
    ("1,0,0,0;1,14,-21,-7;8,10,-15,-5;1,16,-24,-8", 1),
]


def c_at(qs, ell, check=True):
    """c at level ell, and whether the Euler identity holds (None if not checked).

    c itself is computed in exact Fraction arithmetic in Python and has NO size
    limit.  Only the IDENTITY check calls the C++ engine, whose documented budget
    is |component| <= 512 after gcd reduction -- so at fine perturbation scales the
    engine refuses while c remains perfectly computable.  Skipping the engine there
    is not a weakening: it removes a limit of the REPRESENTATIVE (the integer
    quaternion's height) that says nothing about the object.  Reporting those draws
    as failures, as an earlier version of this file did, would have scored 26
    unevaluated draws as if they were evidence.
    """
    lv = level_graph(qs)
    g = lv.get(ell)
    if g is None:
        return None, None
    if not check or max(abs(v) for q in qs for v in q) > 512:
        return g["c"], None
    e = engine(qs)
    d = e["by_depth"].get(str(ell), 0)
    return g["c"], (g["E"] - g["V"] + g["c"] + 1 == d)


def main():
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    for spec, ell in SEEDS:
        base = parse(spec)
        c0, ok0 = c_at(base, ell)
        print("=" * 74)
        print(f"seed  {spec}")
        print(f"  ell={ell}  c={c0}  identity_ok={ok0}  shares_plane={shares_plane(base)}")
        for scale in (10, 100, 1000, 10000):
            tally = collections.Counter()
            for _ in range(N):
                qs = [base[0]] + [tuple(v * scale + rnd.randint(-1, 1) for v in q)
                                  for q in base[1:]]
                if any(not any(q) for q in qs):
                    continue
                try:
                    c, ok = c_at(qs, ell)
                except Exception:
                    tally["error"] += 1
                    continue
                tally[(c, ok, shares_plane(qs))] += 1
            tot = sum(tally.values())
            kept = sum(v for k, v in tally.items()
                       if isinstance(k, tuple) and k[0] == c0)
            print(f"  perturb 1/{scale:<6} ({tot} draws): kept c={c0} in {kept}/{tot}"
                  f"   -> {dict(sorted((str(k), v) for k, v in tally.items()))}")
    print()
    print("A condition that survives a generic perturbation at every scale is OPEN,")
    print("hence not a degeneracy.  A condition destroyed by the first perturbation is.")


if __name__ == "__main__":
    main()
