#!/usr/bin/env python3
"""What CAUSES c_ell = 2?

EXACT CHARACTERISATION (not a correlate).  The level graph G carries the free
involution -I, so G -> G/+- is a double cover, and

    c_ell = 2   <=>   no path in G joins any vertex p to its antipode -p
                <=>   the sheet-swap signing of the quotient graph is BALANCED
                      (every cycle crosses the swap an even number of times)
                <=>   [at ell=1, where G lives on the sphere d(union)] the
                      arrangement contains NO loop that is essential in the
                      quotient RP^2.

c_ell = 1 is the opposite: some cycle downstairs lifts to a path from p to -p.
Verified directly in c_freeaction.py -- 150/150 nodes joined to their antipode on
the c=1 record, 0/176 and 0/130 on the two c=2 cases, never a mixture, which is
the all-or-nothing a double cover forces.

That is what c=2 IS.  This file asks what it goes WITH, because the exact
characterisation does not by itself say whether c=2 can happen where it would
hurt: [OQ 30] needs c_ell <= 1 at MAXIMISERS, not everywhere, so the question that
matters is whether a c=2 configuration can carry a large count.
"""
import collections, json, os, random, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from c_level import level_graph, shares_plane, parse, engine

SEEDS = ["1,0,0,0;1,5,10,15;1,2,4,6;8,7,14,21",
         "1,0,0,0;-23,-90,43,22;72,-37,-17,-2;-4,4,-79,25",
         "1,0,0,0;1,14,-21,-7;8,10,-15,-5;1,16,-24,-8",
         "1,0,0,0;29,-106,-12,-9;-106,31,32,29;-6,32,-34,31"]


def measure(qs, ell=1):
    """(c, E, V, d_ell, total) with d from the ENGINE, or None if unusable"""
    if shares_plane(qs):
        return None
    if max(abs(v) for q in qs for v in q) > 512:
        return None
    lv = level_graph(qs)
    g = lv.get(ell)
    if g is None:
        return None
    e = engine(qs)
    d = e["by_depth"].get(str(ell), 0)
    if g["E"] - g["V"] + g["c"] + 1 != d:
        return None                      # identity fails -> not a measurement
    return g["c"], g["E"], g["V"], d, e["bounded"]


def main():
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 400

    print("=" * 76)
    print("1. WHAT c=2 GOES WITH: E, V, d1 and total, split by c   (ell = 1)")
    print("=" * 76)
    by = collections.defaultdict(list)
    for _ in range(N):
        n = rnd.choice((4, 4, 5))
        h = rnd.choice((3, 9, 30, 120))
        qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(n - 1)]
        if any(not any(q) for q in qs):
            continue
        try:
            m = measure(qs)
        except Exception:
            continue
        if m:
            by[m[0]].append(m[1:])
    for c in sorted(by):
        rows = by[c]
        k = len(rows)
        print(f"  c={c}  n={k:>4}   mean E={sum(r[0] for r in rows)/k:7.1f}"
              f"  mean V={sum(r[1] for r in rows)/k:7.1f}"
              f"  mean d1={sum(r[2] for r in rows)/k:6.1f}"
              f"  max d1={max(r[2] for r in rows):>4}"
              f"  max total={max(r[3] for r in rows):>4}")

    print()
    print("=" * 76)
    print("2. DIRECTED CLIMB: how HIGH can d1 go while c stays 2?")
    print("   (the record has d1 = 92, total 183, and c = 1)")
    print("=" * 76)
    best_overall = None
    for spec in SEEDS:
        qs = parse(spec)
        m = measure(qs)
        if not m or m[0] != 2:
            print(f"  seed unusable: {spec}")
            continue
        best = (m[3], qs, m)
        stall = 0
        while stall < 220:
            base = best[1]
            scale = rnd.choice((1, 1, 2, 4))
            cand = [base[0]] + [tuple(v * scale + rnd.randint(-2, 2) for v in q)
                                for q in base[1:]]
            if any(not any(q) for q in cand):
                stall += 1
                continue
            try:
                mm = measure(cand)
            except Exception:
                stall += 1
                continue
            if mm and mm[0] == 2 and mm[3] > best[0]:
                best = (mm[3], cand, mm)
                stall = 0
            else:
                stall += 1
        c, E, V, d1, tot = best[2]
        spec2 = ";".join(",".join(str(v) for v in q) for q in best[1])
        print(f"  from {spec[:34]:34s} -> best d1={d1:>3} total={tot:>4} c={c}")
        print(f"       {spec2}")
        if best_overall is None or d1 > best_overall[0]:
            best_overall = (d1, tot, spec2)
    if best_overall:
        print()
        print(f"  BEST c=2 FOUND: d1 = {best_overall[0]}, total = {best_overall[1]}")
        print(f"    {best_overall[2]}")
        print(f"  against the n=4 record d1 = 92, total = 183 (c = 1)")


if __name__ == "__main__":
    main()
