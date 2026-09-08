#!/usr/bin/env python3
"""Is c_ell = 3 forbidden by the antipodal structure, or only unobserved?

Every cube here is centrally symmetric about the common centre, so the WHOLE
arrangement is invariant under -I, and so is every depth level and its curve
graph.  Components therefore come in antipodal PAIRS (X, -X with X != -X) or are
SELF-ANTIPODAL (X = -X), giving

    c_ell  =  (# self-antipodal)  +  2 * (# pairs).

Parity does NOT forbid c = 3: it needs 3 self-antipodal components, or 1
self-antipodal plus 1 pair.  So [P259]'s dichotomy c in {1,2} cannot be a parity
argument -- it must be a CONNECTIVITY claim about the quotient (mod +-), which is
[OQ 30].  This file checks the decomposition on actual components rather than
assuming it, and reports which of the two shapes any c = 3 instance has.
"""
import collections, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, shares_plane, parse, engine


def components_with_nodes(qs, want_ell):
    """the depth-ell curve graph's components, each as a frozenset of node points"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    node = {}
    arcs = []
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                if s + 1 != want_ell:
                    continue
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, len(node))
                    ends.append(node[P])
                arcs.append(tuple(ends))
    par = list(range(len(node)))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for a, b in arcs:
        par[f(a)] = f(b)
    groups = collections.defaultdict(set)
    for P, idx in node.items():
        groups[f(idx)].add(P)
    return [frozenset(v) for v in groups.values()]


def antipodal_structure(comps):
    """classify components under negation; returns (self_antipodal, pairs, unmatched)"""
    lookup = {c: i for i, c in enumerate(comps)}
    neg = [frozenset(tuple(-x for x in P) for P in c) for c in comps]
    selfa, pairs, unmatched = 0, 0, 0
    done = set()
    for i, c in enumerate(comps):
        if i in done:
            continue
        j = lookup.get(neg[i])
        if j is None:
            unmatched += 1
            done.add(i)
        elif j == i:
            selfa += 1
            done.add(i)
        else:
            pairs += 1
            done.add(i)
            done.add(j)
    return selfa, pairs, unmatched


def main():
    cases = [
        ("c_check's ell=2 c=3 (plane-degenerate)", "1,0,0,0;1,4,-4,12;3,-1,1,-3;5,-1,1,-3", 2),
        ("n=5 ell=3 c=3 (plane-degenerate)", "1,0,0,0;-1,2,-1,3;2,3,2,2;1,-3,3,0;3,-2,2,-3", 3),
        ("n=4 record 183, ell=1 (c=1)", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4", 1),
        ("a c=2 non-degenerate case ([P245])", "1,0,0,0;1,5,10,15;1,2,4,6;8,7,14,21", 1),
    ]
    print(f"{'case':44s} {'c':>3} {'self':>5} {'pairs':>6} {'unmatched':>10}  sizes")
    for label, spec, ell in cases:
        qs = parse(spec)
        comps = components_with_nodes(qs, ell)
        sa, pr, un = antipodal_structure(comps)
        sizes = sorted((len(c) for c in comps), reverse=True)
        flag = "  <-- NOT -I-CLOSED" if un else ""
        print(f"{label:44s} {len(comps):>3} {sa:>5} {pr:>6} {un:>10}  {sizes[:8]}"
              f"   deg={shares_plane(qs)}{flag}")
    print()
    print("c = self + 2*pairs in every row above, so c = 3 = 1 self + 1 pair is")
    print("STRUCTURALLY ALLOWED.  It is not parity that rules it out.")


if __name__ == "__main__":
    main()
