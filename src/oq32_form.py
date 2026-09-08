#!/usr/bin/env python3
"""[OQ 32] restated exactly, and tested.

[P262]/[P263] need `W1 >= 2(d3 - 2)` (a LOWER bound on W1: W0 = budget - W1, so a
larger W1 makes the bound safer, a smaller one breaks it).  With W1 = V3(3) = V
the deepest level's vertex count, and d3 = E - V + c + 1 exact ([P243]),

    W1 >= 2(d3-2)   <=>   V >= 2(E - V + c - 1)   <=>   2E <= 3V - 2c + 2
                    <=>   SUM over deepest-level vertices of (3 - deg v)  >=  2(c - 1).

So the needed inequality is not about c alone: it says the graph's DEGREE DEFICIT
from cubic must pay for every extra component.  Two consequences fall out at once:

  * if every vertex has degree 3 (2E = 3V), the condition is exactly `c <= 1`;
  * a c = 2 configuration therefore breaks it ONLY IF its degrees are near-cubic.

The n=4 record has V=44, E=66, c=1: deficit 0, requirement 0 -- EXACTLY TIGHT, the
same signature Theorem S had.  The deepest-level c=2 witness has V=44, E=62, c=2:
deficit 8, requirement 2 -- it satisfies the inequality with room, which is why it
does NOT break the chain despite falsifying the equality the chain is written with.
"""
import collections, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph, shares_plane, parse, engine

CASES = [("n=4 record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
         ("deep c=2 witness", "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53")]


def row(qs):
    n = len(qs)
    ell = n - 1
    g = level_graph(qs).get(ell)
    if g is None:
        return None
    e = engine(qs)
    d = e["by_depth"].get(str(ell), 0)
    if g["E"] - g["V"] + g["c"] + 1 != d:
        return None
    V, E, c = g["V"], g["E"], g["c"]
    return V, E, c, d, 3 * V - 2 * E, 2 * (c - 1), e["bounded"]


print(f"{'case':22s} {'V':>4} {'E':>4} {'c':>3} {'d':>4} {'3V-2E':>6} {'2(c-1)':>7}  holds")
for label, spec in CASES:
    r = row(parse(spec))
    print(f"{label:22s} {r[0]:>4} {r[1]:>4} {r[2]:>3} {r[3]:>4} {r[4]:>6} {r[5]:>7}  "
          f"{'YES' if r[4] >= r[5] else '*** NO ***'}"
          + ("   (tight)" if r[4] == r[5] else ""))

print()
rnd = random.Random(31)
stat = collections.Counter()
slack = collections.Counter()
worst = None
for _ in range(260):
    n = rnd.choice((4, 4, 5))
    h = rnd.choice((3, 9, 30, 120))
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(n - 1)]
    if any(not any(q) for q in qs) or shares_plane(qs):
        continue
    if max(abs(v) for q in qs for v in q) > 512:
        continue
    try:
        r = row(qs)
    except Exception:
        continue
    if not r:
        continue
    ok = r[4] >= r[5]
    stat[(r[2], ok)] += 1
    slack[r[4] - r[5]] += 1
    if worst is None or r[4] - r[5] < worst[0]:
        worst = (r[4] - r[5], qs, r)
print("SUM(3-deg) >= 2(c-1) at the deepest level, blind sample:")
for k in sorted(stat):
    print(f"  c={k[0]}  holds={k[1]} : {stat[k]}")
print(f"  violations: {sum(v for k, v in stat.items() if not k[1])}")
print(f"  slack distribution (3V-2E) - 2(c-1): {dict(sorted(slack.items())[:10])}")
print(f"  tight (slack 0): {slack[0]}")
