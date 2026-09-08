#!/usr/bin/env python3
"""What would be required to VIOLATE W0 <= 84?  Derived, then checked.

THE DERIVATION.  Three facts, two of them proved:

  (i)  W0 = budget - W1,  budget = sum over the four triples of V3(T).   [exact,
       for simple configurations; fails where four cube boundaries meet, P272]
  (ii) V3(T) = 2(d2(T) - c(T) - 1) <= 2(d2(T) - 2),  since c >= 1 always. PROVED.
  (iii) Theorem S: sum_T d2(T) <= 48 + d3.                               PROVED.

Chaining (ii) and (iii):   budget <= 2*sum_T d2(T) - 16 <= 2(48 + d3) - 16 = 80 + 2*d3.
Therefore                  W0 <= 80 + 2*d3 - W1,
and                        W0 <= 84   <=>   W1 >= 2(d3 - 2).

So EVERYTHING else is already proved, and a violation requires exactly one thing:
the deepest level must carry FEWER triple points than its Euler-generic count.
Quantitatively, W0 >= 85 forces W1 <= budget - 85 <= 2*d3 - 5; triple points come
in antipodal pairs so W1 and 2*d3 are both even, giving

    A VIOLATION REQUIRES  W1 <= 2(d3 - 3),

i.e. the depth-3 level short by at least one whole ANTIPODAL PAIR of triple
points -- while the four triples' own budgets stay high enough that
budget >= 85 + W1.  Those two pull against each other, and this measures by how
much on the configurations that come closest.

Corollary worth stating: the budget-maximal case is CLOSED. budget = 128 needs all
four d2(T) = 18, i.e. sum_T d2(T) = 72; Theorem S then gives d3 >= 72 - 48 = 24,
and d3 <= 24 is the l=1 ceiling law, so d3 = 24 exactly.  [P263]'s observation that
every budget-attaining configuration has d3 = 24 is therefore a THEOREM, not a
regularity -- it is the equality case of Theorem S.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import shares_plane, parse, engine
from w1_gate import w1_direct
from oq32_simple import is_simple


def probe(qs):
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        return None
    e = engine(qs)
    d3 = e["by_depth"].get("3", 0)
    W = w1_direct(qs)
    budget = sum(w1_direct([qs[i] for i in T])[0]
                 for T in itertools.combinations(range(4), 3))
    return {"W0": W[0], "W1": W[1], "d3": d3, "budget": budget,
            "need_W1": 2 * (d3 - 3), "step": W[1] - 2 * (d3 - 2),
            "gap_to_violation": 86 - W[0]}   # 86, not 85: W0 is EVEN (antipodal pairs)


print(__doc__.split("Corollary")[0].strip()[:0] or "", end="")
for label, spec in (("n=4 record", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
                    ("deep c=2 witness", "1,0,0,0;76,86,80,-95;113,-103,44,-53;98,-87,23,53")):
    r = probe(parse(spec))
    print(f"{label:18s} W0={r['W0']:>3} budget={r['budget']:>4} W1={r['W1']:>3} d3={r['d3']:>3}"
          f"   needs W1<={r['need_W1']:>3} for a violation: "
          f"{'satisfied' if r['W1'] <= r['need_W1'] else 'NOT satisfied'}"
          f"   |  W0 short of 86 by {r['gap_to_violation']}")

print()
rnd = random.Random(67)
near = []
cnt = collections.Counter()
for _ in range(320):
    h = rnd.choice((6, 12, 30, 60, 120))
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(3)]
    if any(not any(q) for q in qs):
        continue
    try:
        r = probe(qs)
        if not r:
            continue
        simple = is_simple(qs)
    except Exception:
        continue
    cnt[("simple" if simple else "coincident", r["W1"] <= r["need_W1"])] += 1
    if r["W1"] <= r["need_W1"]:
        near.append((r["gap_to_violation"], simple, r,
                     ";".join(",".join(str(v) for v in q) for q in qs)))
print("configurations meeting the NECESSARY condition  W1 <= 2(d3-3):")
for k in sorted(cnt):
    print(f"  {k[0]:11s} meets={str(k[1]):5s} : {cnt[k]}")
print()
near.sort(key=lambda t: (t[0], not t[1]))   # dicts are not orderable; key explicitly
print(f"of those, how close did W0 get to 86?  ({len(near)} found)")
for gap, simple, r, spec in near[:8]:
    print(f"  W0={r['W0']:>3} (short by {gap:>3})  budget={r['budget']:>4} W1={r['W1']:>3} "
          f"d3={r['d3']:>3}  {'simple' if simple else 'coincident'}")
    print(f"     {spec}")
