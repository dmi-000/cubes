#!/usr/bin/env python3
"""Rebuild the n=9 and n=10 records correctly, then re-measure.

Two errors in k4_explore.py, both mine:
  * RESULTS says n=9 is "1895's SEVEN + two more" -- seven of the eight cubes of
    the n=8 record, plus two -- so 9 cubes.  I appended two to all EIGHT, giving a
    10-cube configuration counting 3869, not the record 2787.
  * the pair loop used the dictionary label n, not len(qs), so the histogram
    covered only the first n cubes of whatever was passed.

Which seven is not stated, so it is SOLVED here rather than guessed: try each of
the eight ways to drop one cube, and keep the one that reproduces 2787.  n=10 is
then that nine plus 6555,6555,6497,6555.  Everything is keyed off len(qs).
"""
import collections, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twobody_solve import pair_detail
from c_level import parse, engine

BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
R8 = parse(BASE + ";7,14,1,-5;4,-3,-4,-4;24,-24,24,-61")
ADD9 = [tuple(int(v) for v in s.split(",")) for s in ("168,-168,168,-415", "109,-11,91,140")]
ADD10 = (6555, 6555, 6497, 6555)

print("solving for which seven of the n=8 record's eight cubes the n=9 record uses")
R9 = None
for drop in range(8):
    cfg = [q for i, q in enumerate(R8) if i != drop] + ADD9
    try:
        c = engine(cfg)["bounded"]
    except Exception as e:
        print(f"  drop cube {drop}: engine error"); continue
    print(f"  drop cube {drop}: {len(cfg)} cubes -> {c}" + ("   <-- 2787, the record" if c == 2787 else ""))
    if c == 2787:
        R9 = cfg
if R9 is None:
    print("\nno single-drop reconstruction gives 2787 -- the recorded provenance needs re-reading")
    sys.exit(1)

R10 = R9 + [ADD10]
print(f"\nn=10 check: {len(R10)} cubes -> {engine(R10)['bounded']}  (record 3925)")

print()
print(f"{'n':>3} {'total':>6} {'d1':>6} {'W0':>6} {'T':>5} {'k':>3} {'nz':>4} {'C(n,2)':>7} "
      f"{'8n+40':>6}  histogram")
for cfg in (R9, R10):
    n = len(cfg)
    e = engine(cfg)
    det = pair_detail(cfg)
    w = {p: c[4] + 2 * c[6] for p, c in det.items()}
    allw = [w.get(p, 0) for p in itertools.combinations(range(n), 2)]
    T, k = sum(allw), sum(1 for v in allw if v == 10)
    nz = sum(1 for v in allw if v > 0)
    d1 = e["by_depth"].get("1", 0)
    print(f"{n:>3} {e['bounded']:>6} {d1:>6} {2*(d1-T-2):>6} {T:>5} {k:>3} {nz:>4} "
          f"{n*(n-1)//2:>7} {8*n+40:>6}  {dict(sorted(collections.Counter(allw).items(), reverse=True))}")
    assert len(allw) == n * (n - 1) // 2
print("\nT = 8n+40 predicts 112 at n=9 and 120 at n=10.")
