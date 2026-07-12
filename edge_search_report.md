# Edge-concurrence search: can an edge-dominated 6-cube config beat 723?

**Verdict up front: no.** Across 4,600+ exact evaluations on four search
fronts, the best edge-dominated 6-cube total is **691** (an exact ℚ(√2)
octahedral pair, edge-PURE — zero corner concurrences), **32 regions
short** of the corner-dominated record **723**. Edge-concurrence richness
does **not** buy region count — within every structured family it
**anti-correlates** with total (Spearman −0.57 to −0.59). The data argues
*against* the conjecture that a maximum could substitute edge for corner
concurrences, though 4,600 evals is evidence, not proof (see coverage).

Files: `edge_search.py` (analyzer + drivers), `edge_search.jsonl` (log,
~4.6k rows across fronts 1a/1b/2random/2climb), this report.

## Method recap

An "edge concurrence" is a **(2,2) 4-fold point**: 2 face-planes of cube A
+ 2 of cube B meet at one point = an edge of A crossing an edge of B (the
incidence mode of the octahedral 3-compound {Rx45,Ry45,Rz45}). A "corner
concurrence" is a **(3,3[,3…]) point**: 3+ planes per cube = coincident
cube corners = a shared axis (the mode behind 699/717/**723**, whose top
concurrence is a **9-fold (3,3,3)** point — three cubes sharing a corner).

`edge_search.py` builds an exact incidence analyzer over the 36 face
planes. `find_concurrences` brute-forces all C(36,3)=7140 plane triples,
solves each 3×3 system exactly (Cramer, pure field arithmetic — Q(√2) or
Q(√5), **no floats in any predicate**), unions triples that resolve to the
identical exact point, and tallies the per-cube plane signature at each
≥4-fold point. `fast_edge_corner_scan` is the O(candidates·36) rational
screen used for ranking; **both were validated to agree exactly** on the
two anchor cases:

- octahedral 3-compound → total 67, **66 edge (2,2) points, 0 corner
  points**, max multiplicity 4 (edge-pure, as ALGEBRAIC_SEARCH.md asserts);
- the 723 record → **2 nine-fold (3,3,3) corner points**, 6 six-fold
  (3,3), 180 edge (2,2), max multiplicity 9 (corner-dominated).

## (1) Best edge-dominated total = 691 (vs record 723)

The overall best edge-dominated config is from the **exact ℚ(√2)** front
(front 1a), re-verified by the exact `exact_count_q2` counter:

```
config  {Rx45,Ry45,Rz45} ∪ R·{Rx45,Ry45,Rz45},  R = quat (31,13,33,30)
total   691
by_depth {1:174, 2:214, 3:164, 4:102, 5:36, 6:1}
concurrence profile: max_mult 4, edge4=132, corner6=0, corner9+=0  (edge-PURE)
```

This is genuinely edge-dominated — its **maximum concurrence multiplicity
is 4 and every ≥4-fold point is a (2,2) edge crossing; there is not a
single corner concurrence.** It is two exact-45° octahedral 3-compounds
related by a generic rational rotation R. (The best *rational-engine*
config, verified directly by `./cube_regions`, is 663:
`12,5,0,0; 12,0,5,0; 12,0,0,5; 191,113,41,17; 191,17,113,41; 191,41,17,113`,
by_depth {1:150,2:210,3:164,4:102,5:36,6:1}, edge4=72 — a Pythagorean-45°
approximant; the exact wall at 691 sits above its rational neighbours.)

**The gap to 723 is a depth-1 deficit: d1=174 here vs d1=210 for 723.**
This is the crux — 723's record IS its d1=210 shallow shell (constant
across the whole 699→717→723 corner family), and the edge-dominated family
cannot generate that shallow count: its best d1 tops out at 174. The deep
layers are already pinned at ceiling here (d3=164, d4=102, d5=36), so
there is no deep-tail slack to trade either. Edge crossings buy d2 (214,
near the 216 record high) but leave d1 ~36 short, and that is the whole
32-region gap.

## (2) Octahedral ℚ(√2) family best (front 1a, EXACT, no approximation)

Two exact-45° octahedral 3-compounds {Rx45,Ry45,Rz45} and R·{…}, R a
rational relative rotation embedded in Q(√2), counted with the exact
`exact_count_q2` kernel (~180 R values swept, generic + special axes):

```
best  total 691   R=(31,13,33,30)   by_depth {1:174,2:214,3:164,4:102,5:36,6:1}
      edge4=132, corner6=0  (edge-PURE, max_mult 4)  <- family best, generic R
      total 677   R=(-4,-28,17,-39)  edge4=132  (generic R)
      total 661   R=(-9,-4,12,13)    edge4=130  (max_mult 5)
      total 657   R=(3,21,13,0)      edge4=168  (near-icosahedral R)
      total 655   R=(5,±3,±3,±3)     edge4=240  (MOST edge-rich — yet LOWER total)
```

The exact-45° octahedral family reaches **691** at *generic* relative
rotations R, still below 723 and below the rational records 699/705/717.
The special/high-symmetry R values (shared (1,1,1) axis, near-icosahedral)
that *maximise* edge richness sit **lower** (655–657) — the R=(5,3,3,3)
config has the family-maximum edge richness (edge4=240) but one of the
lowest totals (655). So even inside the pure octahedral edge family, more
edge concurrences means fewer regions.

## (3) KEY analysis: edge-richness ANTI-correlates with total

Corner-concurrence points essentially never occur off the shared-axis
construction — in this dataset they appear **only in 66 degenerate
collapsed configs** (near-coincident cubes, totals 55/123), so a raw
"total vs corner-count" correlation is a degeneracy artifact and not
meaningful. The load-bearing measurement is **total vs edge-richness**,
and it is clean and negative:

Front 1b (structured octahedral overlays, non-degenerate total>400,
n=2501), mean total binned by number of edge (2,2) points:

| edge (2,2) point count | n | mean total | max total |
|---|---|---|---|
| 72–95   | 2062 | 643 | **663** |
| 96–119  | 25   | 607 | 647 |
| 120–143 | 414  | 568 | 639 |
| (144, degenerate)      | — | 355 | 355 |

**More edge concurrences → lower total.** Within-1b Spearman(total,
edge4) = **−0.569**; the maximally edge-rich structured configs
(edge4=144) collapse to 355. The **exact octahedral family (front 1a)**
shows the same sign: Spearman(total, edge4) = **−0.593** — its top totals
(691/677/667/663) all sit at edge4=132, while edge4=168 and 240 drop to
657 and 655. Front 2random (unstructured rational, n=2056): correlation ≈
**+0.08** (no predictive power; edge richness is just noise there, best
total 621). Front 2climb (hill-climb that *maximizes* edge4 from 6
restarts): every run drove edge4 up (0→36–72) while the **best total seen
along the path always EXCEEDED the edge-maximized endpoint** (e.g. seed 1:
endpoint edge4=72/total=621, best en route 635; seed 4: endpoint 569, best
en route 617) — i.e. steering toward edge richness steers away from
region count.

So edge-concurrence richness is at best neutral (random configs) and at
worst actively harmful (structured configs); it never behaves like the
corner concurrences that drive the record.

## (4) Verdict on the conjecture

**The conjecture "a 6-cube maximum could substitute edge for corner
concurrences" is not supported — the evidence points the other way.**
The best edge-dominated route caps at **691** (edge-pure, exact ℚ(√2)), a
32-region deficit to 723, and the deficit is structural: it lives in
depth-1 (d1=174 vs 210), and edge-richness *anti-correlates* with total
in every structured family (Spearman −0.57 to −0.59). The record's power
comes from its shallow d1=210 shell, a property of the corner-sharing /
shared-axis construction; edge crossings buy d2 but cannot reproduce the
d1 shell. Corner (shared-axis) concurrence and high region count are
correlated in every record; edge concurrence and high region count are
anti-correlated here.

**Coverage / honesty caveat.** This is ~4,600 exact evaluations, not an
exhaustive proof. It covers: the exact Q(√2) octahedral-pair family
(front 1a, ~180 relative rotations), rational Pythagorean-45° overlays
(front 1b, ~2,600 configs over convergent levels 3–7 × 273 R values), and
unstructured + edge-maximizing-climb rational configs (fronts 2random /
2climb, ~2,000). It does **not** rule out an edge-dominated config in a
region of SO(3)⁶ we did not sample, nor an *irrational* edge wall in a
field beyond Q(√2). What it does establish, exactly and reproducibly, is
that no edge-dominated configuration found by four independent search
strategies comes within 32 regions of 723, and that pushing edge richness
up demonstrably pushes total down. On the balance of the evidence, an
edge-for-corner substitution at the 6-cube maximum looks unavailable.
