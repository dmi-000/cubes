#!/usr/bin/env python3
"""Pool generator for anchor_split.py's gate, weighted to the cases that are HARD
for the proof rather than the ones that are easy to produce.

The proof has three moving parts and each has a different hard case:
  * Theorem 1 (comp == blocks) is hardest on SHARED-NORMAL configurations --
    P33 records those as the locus where an anchor is removed by self-exclusion.
  * the matroid step (s(t) <= s(P)) is vacuous unless some s > 0, i.e. unless two
    face directions of one cube sit in the SAME component.  Low-height, nearly
    aligned cubes are where components merge.
  * the union step (m(t) <= sum m(P)) is vacuous unless anchors are LOST, which
    needs another cube to reach inside a face centre -- again low height.
The record and generic high-height samples have comp = k = blocks = 6 everywhere
and exercise none of the three, so a pool of those would be a pass that means
nothing (FAILURE_MODES 29).
"""
import random, sys

def rq(rnd, h):
    while True:
        q = tuple(rnd.randint(-h, h) for _ in range(4))
        if any(q):
            return q

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    rnd = random.Random(seed)
    out = []
    # (a) low height: anchors get eaten, components merge
    for h in (1, 2, 3, 5):
        for _ in range(N):
            out.append([(1, 0, 0, 0)] + [rq(rnd, h) for _ in range(3)])
    # (b) shared-normal locus: axis-aligned rotations about a coordinate axis
    for _ in range(N):
        cfg = [(1, 0, 0, 0)]
        for _ in range(3):
            ax = rnd.randrange(3)
            q = [rnd.randint(1, 6), 0, 0, 0]
            q[1 + ax] = rnd.randint(-6, 6)
            cfg.append(tuple(q))
        out.append(cfg)
    # (c) near-record perturbations: the tight end of the inequality
    rec = [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]
    for scale in (1, 4, 16, 64):
        for _ in range(N):
            cfg = [rec[0]] + [tuple(c * scale + rnd.randint(-2, 2) for c in q) for q in rec[1:]]
            out.append(cfg)
    # (d) generic high height: the control that should be all-6
    for _ in range(N):
        out.append([(1, 0, 0, 0)] + [rq(rnd, 60) for _ in range(3)])
    for cfg in out:
        print(";".join(",".join(str(v) for v in q) for q in cfg))

main()
