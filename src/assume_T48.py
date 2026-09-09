#!/usr/bin/env python3
"""Assume T <= 48 and follow it.  Two places it can lead: to max(4) = 183, or to
a contradiction at higher n.

THE DERIVATION.  The level-1 anatomy ([P272]) is exact:

    d1  =  W0/2 + T + c1 + 1

With W0 <= 84 ([P273]/[P275], open), T <= 48 (ASSUMED), c1 = 1:

    d1 <= 42 + 48 + 1 + 1 = 92        -- exactly the record's d1
    max(4) <= d1 + d2 + d3 + d4 <= 92 + 66 + 24 + 1 = 183   -- exactly the record

So **T <= 48 is the last brick**: with the other three caps it closes max(4) = 183,
the whole conjecture.  That is worth knowing whichever way it turns out.

TWO STRESS TESTS, run here.

(a) THE c1 = 2 ESCAPE.  c1 = 2 does occur ([P269]), and it would give
    d1 <= 42 + 48 + 2 + 1 = 93, hence max(4) <= 184, not 183.  So the assumption
    alone is not enough -- unless c1 = 2 configurations cannot also carry W0 = 84
    and T = 48.  Measured below on every known c1 = 2 configuration.

(b) HIGHER n.  T <= 48 at n = 4 is 8 per pair against [P237]'s cap of 10.  If that
    per-pair figure is real rather than an n=4 accident, the records at n = 5..8
    should respect T <= 8*C(n,2).  If one EXCEEDS it, the assumption is either
    n-specific or wrong, and the excess is a counterexample worth having.
"""
import collections, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import parse, engine, level_graph
from w1_gate import w1_direct

BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
RECORDS = {4: "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4",
           5: BASE,
           6: BASE + ";7,14,1,-5",
           7: BASE + ";7,14,1,-5;4,-3,-4,-4",
           8: BASE + ";7,14,1,-5;4,-3,-4,-4;24,-24,24,-61"}


def T_of(qs):
    det = pair_detail(qs)
    return sum(c[4] + 2 * c[6] for c in det.values()), \
           {p: c[4] + 2 * c[6] for p, c in det.items()}


print("(b) HIGHER n: does T <= 8*C(n,2) hold at the records?")
print(f"{'n':>2} {'total':>6} {'d1':>5} {'T':>5} {'8*C(n,2)':>9} {'10*C(n,2)':>10}  verdict")
for n in sorted(RECORDS):
    qs = parse(RECORDS[n])
    e = engine(qs)
    T, per = T_of(qs)
    npair = n * (n - 1) // 2
    ok = T <= 8 * npair
    print(f"{n:>2} {e['bounded']:>6} {e['by_depth'].get('1',0):>5} {T:>5} {8*npair:>9} "
          f"{10*npair:>10}  {'ok' if ok else '*** EXCEEDS 8/pair ***'}   per-pair "
          f"{sorted(per.values(), reverse=True)[:8]}")

print()
print("(a) THE c1 = 2 ESCAPE: can a c1=2 configuration carry W0 = 84 and T = 48?")
print(f"{'W0':>4} {'T':>4} {'c1':>3} {'d1':>4} {'W0/2+T+c1+1':>12}  configuration")
worst = None
for spec in [l.strip() for l in open("c2_configs.txt") if l.strip()]:
    qs = parse(spec)
    if max(abs(v) for q in qs for v in q) > 512 or len(qs) != 4:
        continue
    try:
        g = level_graph(qs)[1]
        e = engine(qs)
        W = w1_direct(qs)
        T, _ = T_of(qs)
    except Exception:
        continue
    if g["c"] != 2:
        continue
    d1 = e["by_depth"].get("1", 0)
    print(f"{W[0]:>4} {T:>4} {g['c']:>3} {d1:>4} {W[0]//2 + T + g['c'] + 1:>12}  {spec[:44]}")
    if worst is None or W[0] + T > worst[0]:
        worst = (W[0] + T, W[0], T, d1)
if worst:
    print(f"\n  best W0+T among c1=2: W0={worst[1]} T={worst[2]} (d1={worst[3]})")
    print(f"  the 184 escape needs W0=84 AND T=48 with c1=2, i.e. W0+T = 132.")
