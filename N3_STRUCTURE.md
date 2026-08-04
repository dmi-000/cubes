# The n = 3 structure graph

Written 2026-08-03. Every number here is an exact count; see
[`six_cube_search_results.md`](six_cube_search_results.md) Postscripts 69–72
for the runs, and [`GLOSSARY.md`](GLOSSARY.md) for the vocabulary.

This is the n = 3 configuration space described through the n = 2 map of
[Postscript 70](six_cube_search_results.md). It is complete at the level of
**cells** (proved), partial at the level of **dimensions** and **edges**
(measured at representatives).

---

## 1. The construction

A 3-cube compound {I, R₁, R₂} contains three pairs, with relative rotations
R₁, R₂ and R₁⁻¹R₂. Each is a point of the n = 2 configuration space, whose
region count is one of **1, 4, 5, 9, 13**. So every 3-cube configuration
carries a label:

> **label = the multiset of its three pair counts.**

This is the project's "pair signature" given its proper home: the label is the
*image* of an n = 3 configuration in three copies of the n = 2 map. What the
label discards is the *fibre* — how the three pairs are glued to each other.
Section 5 is about that.

## 2. The nodes — complete, and proved

Of the 35 multisets of size 3 from {1, 4, 5, 9, 13}, exactly **25 are
realisable**, and the other 10 are impossible.

**Proof of the exclusion.** A pair counts 1 exactly when its two cubes are the
same solid. If cubes 1 and 2 coincide, then the pair (1,3) and the pair (2,3)
*are the same pair*, so their counts are equal. Hence any label containing 1
has the form **(1, x, x)**. The 10 excluded labels are precisely those
containing 1 with unequal partners:

    (1,1,4) (1,1,5) (1,1,9) (1,1,13) (1,4,5)
    (1,4,9) (1,4,13) (1,5,9) (1,5,13) (1,9,13)

So the node set is: the **20** multisets from {4, 5, 9, 13}, plus the **5**
degenerate nodes (1,1,1), (1,4,4), (1,5,5), (1,9,9), (1,13,13). All 25 were
also observed directly in ~2080 random rational triples.

**The degenerate nodes collapse to n = 2.** Measured, and forced: a compound
with a coincident pair is really two cubes, so its total is that pair's count.

    (1,1,1) → 1     (1,4,4) → 4     (1,5,5) → 5
    (1,9,9) → 9     (1,13,13) → 13

## 3. The nodes with their ceilings

Observed range over the random census, ordered by ceiling. These are
**observed maxima, not proved bounds** — except where section 5 supplies a
component argument.

| label | ceiling | range observed | note |
|---|---|---|---|
| (13,13,13) | **67** | 55 on the 2-dim component; **67** at isolated points | contains both n = 3 maxima |
| (9,9,13) | 59 | 39, 41, 49, 53, 59 | |
| (5,13,13) | 59 | 53, 59 | |
| (9,13,13) | 57 | 57 only | |
| (4,13,13) | 57 | 57 only | |
| (5,9,13) | 55 | 35 … 55 | |
| (9,9,9) | 55 | 25 … 55, nine values | |
| (4,9,13) | 53 | 39 … 53 | |
| (5,9,9) | 51 | 33 … 47 (+) | |
| (5,5,13) | 51 | 43 … 51 | |
| (4,9,9) | 49 | 29 … 49 | |
| (4,5,13) | 49 | 37 … 49 | |
| (5,5,9) | 47 | 31 … 47 | |
| (4,4,13) | 47 | 36 … 47 | |
| (4,5,9) | 45 | 23 … 45 | most populous non-generic cell |
| (4,4,9) | 44 | 20 … 44 | |
| (5,5,5) | 43 | 31 … 43 | |
| (4,5,5) | 41 | 21 … 41 | |
| (4,4,5) | 40 | 19 … 40 | |
| (4,4,4) | 38 | 22 … 38 | the generic cell |

The label bounds the total and does not determine it: (9,9,9) alone admits
nine distinct totals.

## 4. Dimensions

Measured by lattice cardinality — probe a radius-1 lattice in the 6 Cayley
coordinates (3⁶ − 1 = 728 points) and count how many neighbours keep the
label. A d-dimensional component contributes 3ᵈ − 1.

| cell | neighbours keeping the label | 3ᵈ − 1 | dimension |
|---|---|---|---|
| (4,4,4) generic | **728** of 728 | 3⁶ − 1 | **6** — open, full measure |
| (13,13,13) shared axis | **8** of 728 | 3² − 1 | **2** |
| (13,13,13) distinct axes | — | — | **0** — isolated points |
| (1,1,1) | — | — | 0, and 18 distinct labels adjacent |

## 5. The fibre: what the label does not see

**The (13,13,13) cell is reducible.** A 13-pair is a pair whose relative
rotation lies on the n = 2 maximum graph — the four body-diagonal circles and
six edge arcs. Then:

- **All three axes the same body diagonal.** If R₁ and R₂ are rotations about
  one diagonal, so is R₁⁻¹R₂, so the third condition is *free*: two parameters
  survive. Measured: 418 of 420 sampled pairs are 13-pairs, dimension 2, and
  the total is **55** in all 1512 non-degenerate cases.
- **Axes on distinct diagonals.** The third condition is a genuine
  codimension-2 constraint on a 2-parameter family, leaving isolated points.
  Measured: 40 of 441, and every *rational* one is degenerate. **The two 67s
  live here**, and are irrational.

So one extra bit — same diagonal or distinct — determines the total on the
whole 2-dimensional component. **The axis relation is the first piece of fibre
data**, and the label plus that bit is strictly stronger than the label alone.

## 6. Edges — the closure order

Which labels occur arbitrarily close to which, measured at representatives
(728-point lattice at spacing 1/64):

**From (4,4,4) generic:** only (4,4,4). It is an open cell; nothing else is
adjacent. Consistent with 98.8% of n = 2 pairs being 4 at large height.

**From (13,13,13) shared-axis**, 13 labels are adjacent:

    (4,5,9) ×216   (4,9,9) ×135   (4,4,9) ×78   (4,9,13) ×75
    (4,5,5)  ×75   (4,5,13) ×57   (4,4,5) ×54   (4,4,13) ×12
    (13,13,13) ×8  (5,9,9)   ×6   (5,5,9)  ×6   (5,5,5)   ×3
    (9,9,9)    ×3

**From (1,1,1)**, the most degenerate node, 18 labels are adjacent, including
(13,13,13) — everything is near the point where all three cubes coincide.

The pattern is the product of the n = 2 closure order, in which 4 is generic,
5 and 9 are more special and mutually non-adjacent, 13 is more special still,
and 1 is the most special of all. Perturbing an n = 3 configuration relaxes its
three pairs toward the generic simultaneously, so a cell's neighbours are the
labels obtained by relaxing entries — which is what the counts above show.

## 7. What this says about the maxima

max(3) = 67 is attained at **isolated points of the distinct-axis part of a
single cell, (13,13,13)** — the cell in which all three pairs sit on the n = 2
maximum locus. Both non-congruent maximisers are there: the octahedral one
(three 45° turns, Cayley point (√2−1)·axis, verified in ℚ(√2) to have three
13-pairs and total 67 with profile {48,18,1}) and the golden one (pairs 13 from
its subcompound chain 1, 13, 67, 177).

So the three-cube maximum is built from three copies of the two-cube maximum,
assembled on distinct axes. And the irrationality has a location: it is not a
property of the cell — the cell's 2-dimensional component is rational and
totals 55 — but of the isolated component within it.

## 8. What is not established

- Ceilings in section 3 are **observed**, from a random rational census. Cells
  whose maximum needs irrational or high-height configurations will read low —
  (13,13,13) itself read 55 until the two 67s were checked in their own fields.
- Dimensions are measured at **one representative each**; a cell may have
  components of several dimensions, as (13,13,13) does.
- Edges are measured at **three representatives**. The closure order is
  conjectured to be the componentwise n = 2 order; that is consistent with the
  data and not proved.
- The 13-locus of n = 2 includes six **edge arcs** as well as the four
  body-diagonal circles. Section 5 scanned only the diagonals; the arcs may
  contribute further components to (13,13,13).
