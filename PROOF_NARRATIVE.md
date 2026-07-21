# How max(3) = 67 got proved — a narrative

*A readable account of the proof that three concentric unit cubes make at
most 67 bounded regions. It is a companion to the formal write-up
(`PROOF_FORMAL.md`); here the goal is the shape of the argument and how it
was found, including a couple of wrong turns, told briefly. Written by an
AI (Claude) under human direction; the human's questions supplied several
of the turning points.*

## The question

Three unit cubes share a centre and are rotated freely. Their faces cut
space into regions; the bounded ones number, at most (as far as any
search ever found), 67 — attained by two very different arrangements, the
"octahedral" one (cubes at 45° about the three axes) and the "golden" one
(a golden-ratio triple). The problem: prove 67 is really the maximum.

## The reduction that makes it tractable

A region is fixed by which cubes contain it, so counting regions splits
by depth: d₃ (in all three), d₂ (in exactly two), d₁ (in exactly one),
summing to the total. Because every cube is convex and contains the
centre, the whole problem projects onto the unit sphere of directions:
along each ray, you cross the cubes' boundaries in a fixed order, and the
depth steps down 3 → 2 → 1 → 0. The depth-m regions then correspond to the
faces of a partition of the sphere, and **Euler's formula V − E + F = 2**
governs those face counts. This is the backbone, and it is why the answer
turns out not to depend on the cubes being cubes.

The three layers, in increasing difficulty:

- **d₃ ≤ 1** is immediate: the triple intersection is convex, so
  connected.
- **d₂ ≤ 18** follows from a one-line "convex-cover" fact: the part of
  two cubes that lies outside the third is a union of at most six convex
  pieces (one per face of the third cube), so at most six components; times
  three ways to pick the outside cube gives 18.
- **d₁ ≤ 48** is the hard one, and it is where all the work lives.

## The heart: d₁ ≤ 48

Euler turns d₁ into a vertex count: d₁ = 2 + ½ W, where W is the total
"weight" Σ(degree − 2) of the sphere-diagram's vertices. So d₁ ≤ 48 means
**W ≤ 92**. The vertices come in two kinds — *triple points* (all three
cubes reach equally far) and *contacts* (two cubes' edges or corners
coincide) — and an exact census of both maximizers showed the budget
splits as 92 = 32 (triple points) + 60 (contacts), tight in both cases.

The triple-point half, **≤ 32**, was settled by noticing that triple
points are shared with the *other* extreme diagram (which cube reaches
*least*), and that diagram is controlled by the already-proved d₂ ≤ 18.
So 32 is another Euler bound.

That left one inequality — **contact weight ≤ 60** — standing between the
argument and a full proof. It resisted for a while; an appealing shortcut
(anchoring each region at a cube corner) turned out to give the wrong
count and was abandoned.

## A wrong turn, and what it taught

While probing whether *non-cube* cells might beat 67, the region counter
being used quietly counted the wrong thing — cells of the infinitely
extended face planes rather than regions bounded by the actual finite
faces. That inflated the counts and produced a string of exciting-but-false
claims that off-centred cubes and general hexahedra "beat the record." A
human noticing that some regions were being split by a face's invisible
extension exposed the error. Corrected — regions are components of constant
cube-containment — every one of those claims collapsed: nothing beats 67,
and cubes are in fact *extremal*.

The wrong turn paid a dividend, though. Redoing the bookkeeping correctly
made clear that the two settled layers (d₂ ≤ 18 and triple ≤ 32) never
used anything about cubes beyond "convex, six faces." So max(3) = 67 was
really a statement about *any* three convex six-faced cells — which raised
the obvious question: if the bound is shape-independent, there ought to be
a single topological reason for it.

## The Euler insight that closed it

Chasing exactly that intuition, the contacts turned out to have a clean
geometric meaning: a contact is a place where an *edge of one cube crosses
an edge of another* in space, and such a crossing is precisely a
degree-four vertex of the convex polytope where those two cubes *intersect*.
That reframes the last inequality entirely. For any convex polytope, the
total vertex weight Σ(degree − 2) equals 2F − 4, where F is its number of
faces — a pure Euler identity. Two six-faced cubes intersect in a polytope
with at most twelve faces, so its weight is at most 20; and the contacts
of a pair are among that polytope's vertices, with matching degree. Over
the three pairs:

    contact weight ≤ 3 × (2·12 − 4) = 60.

That is the missing bound, and it holds for the same shape-independent
reason as the others: it is Euler's formula, this time on the three
*pairwise intersection polytopes*.

So the whole theorem rests on three Euler arguments on three different
objects — the "reaches-least" diagram (triple ≤ 32), the convex-cover
(d₂ ≤ 18), and the pairwise intersection polytopes (contact ≤ 60) —
assembling to d₁ + d₂ + d₃ ≤ 48 + 18 + 1 = 67. Both maximizers saturate
every step simultaneously, which is exactly why 67 is the ceiling.

## Where it stands

The argument is complete and rigorous for all three concentric convex
six-faced cells whose boundaries meet pairwise transversally — an open
dense set of configurations that includes both maximizers. Getting there
required disarming one non-generic case that at first looked fatal: an
over-degenerate triple point, where three cells coincide at a point with
one at a corner and two at thin blades. The tempting shortcut — that the
"farthest-cell" diagram can be no more branched than the "nearest-cell"
diagram, which the already-proved d₂ ≤ 18 would then cap — is simply false:
such a point can have a degree-eight farthest-cell vertex against a
degree-four nearest-cell vertex, realizable by honest cells. The fix does
not repair that false inequality but sidesteps it. Each triple point is
charged to *two* budgets at once — the nearest-cell diagram and the three
pairwise intersection polytopes — and a short case analysis (on how many
cells are ever nearest at the point) shows a degree-eight vertex draws no
more than its fair share of the combined budget. The two pieces that made
it elementary: the farthest and nearest diagrams' total branching equals
the number of times the three cells' reach profiles cross, and each pair
crosses at most twice its smaller active-facet count. With that, the
degenerate triple points are fully handled — no restriction on them at all
— and max(3) = 67 is a theorem for all pairwise-transversal triples of
convex six-faced cells, cubes among them. (The full write-up is
[`PROOF_STEP_T.md`](PROOF_STEP_T.md).) A single milder caveat predates this and is unrelated
to triple points: two cells meeting tangentially rather than transversally,
a higher-codimension degeneracy the contact bound already set aside.

Two smaller results fell out along the way and are fully proved: the
two-cube maximum is 13 (the first complete maximum theorem in the
project), and the "second-deepest" ceiling d_{n−1} ≤ 6n holds for every n.

*Full details, with the marked intermediate steps, are in
`PROOF_FORMAL.md`; the dated blow-by-blow — including the retracted
claims — is in the ledger `six_cube_search_results.md`, Postscripts 33–41.*
