# Glossary

Grouped rather than alphabetised, because most of these terms are only
meaningful next to each other. Terms coined inside this project are marked
**(ours)**; the rest are standard usage applied to this problem.

The last two sections matter most for reading old documents: §7 lists terms
whose meaning **changed**, and §8 lists terms that are **overloaded** and have
misled at least once.

---

## 1. The objects

**Compound** — *n* unit cubes [−1,1]³, all sharing the origin as centre, each
under its own rotation. The only free parameters are the rotations.

**Region** — a connected component of constant **cube-containment**. Two points
are in the same region iff you can **walk from one to the other without the set
of cubes containing you ever changing along the way**. Both halves matter: the
containment set must be constant, *and* the piece must be connected. Distinct
pieces sharing the same containment set are distinct regions.

  The two-cube maximum makes the distinction concrete: there are only **3**
  non-empty containment sets — {A}, {B}, {A,B} — but **13** regions, because
  {A} has six components (A's six lobes poking out of B), {B} has six, and
  {A,B} has one (it is convex, so it cannot have more). A definition phrased
  only as "the containment set doesn't change" would predict 3 and is wrong.

Getting this definition wrong — counting cells of the infinite plane
arrangement instead — was the project's founding error.

**Real facet / phantom facet** **(ours)** — a face plane, out where its own cube
isn't, does not separate anything: crossing it changes nothing, so the regions
on either side are the same region (*phantom*). Only the actual bounded face
square separates (*real*). Counting cells of the infinite plane arrangement
instead inflates every total.

**Depth** — how many cubes contain a region. Depth 1 is inside exactly one
cube; depth *n* is the core where all overlap. **Depth profile** = the region
count at each depth, e.g. 727 = {214, 220, 156, 100, 36, 1}.

**Base / free cube** **(ours)** — in most searches, five cubes are held fixed
(*the base*, usually the 393 configuration) and the sixth (*the free cube*)
varies over its 3 degrees of freedom.

**Cayley coordinates** — writing the free cube's quaternion as q = (1, a, b, c)
and using (a, b, c) as the 3 coordinates of configuration space. Omits
quaternions with w = 0, which costs no compounds (that omission is a chart
artifact, not a gap).

**Pair count / 13-pair, 9-pair, 4-pair** **(ours)** — the two-cube region count
of one pair within a compound. 13 is the two-cube maximum, so a *13-pair* is a
locally maximal, rigid pair; a *9-pair* is a tunable one.

## 2. Configuration space

**Wall** — a codimension-1 surface in configuration space where the region
count can change. Everywhere else the count is locally constant.

**Line** **(ours)** — the intersection of two walls, hence a 1-parameter family.
Because edge-edge conditions factor into *rational planes*, these lines are
rational, which is why rational points are dense on them.

**Chamber** **(ours)** — a maximal stretch of a line on which the whole
combinatorial type is constant. Bounded by wall crossings.

**Type** **(ours)** — the per-label vector (regions sorted by containment
bitmask). As discriminating as the full adjacency profile and ~50× cheaper. A
type *is* a chamber.

**Plateau** **(ours)** — the set of configurations attaining a record value. At
n = 6 the 727 plateau is at least 161 configurations in 54 types, forming a
union of 1-dimensional segments.

**Continuum** — a positive-length stretch on which the count holds. Note that
*any* continuum contains irrational points, with full measure — so finding an
irrational configuration in one is guaranteed and carries no information.

**Seam** **(ours, and now retired)** — was proposed for "irrational points
between rational continua". Postscript [61](LEDGER.md#p61) refuted the picture; see §7.

**C₃ quotient** **(ours)** — the 393 base is invariant under the 120° rotation
about (1,1,1), which 3-cycles three of its cubes. Configurations must be
quotiented by it or they triple-count (417 → 161). It acts on *lines* too, by a
projective map.

## 3. The wall taxonomy

Every wall is **four face planes concurrent at a real point**. The types are
named by how those four planes distribute over cubes:

| distribution | geometry | name |
|---|---|---|
| 3 + 1 | a **corner** of A touching a **face** of B | corner-on-face |
| 2 + 2 | an **edge** of A crossing an **edge** of B | edge-edge |
| 2 + 1 + 1 | an **edge** of A meeting the **line** where faces of B and C cross | **W3** **(ours)** |
| 1 + 1 + 1 + 1 | one face plane from each of **four** cubes, concurrent | **W4** **(ours)** |

The names count *cubes*, not planes. Against a fixed base these are finite:
**424 real triple points** of the base give 2544 W4 conditions (quadrics);
**360 crossing lines** give 4320 W3 conditions (**quartics** — so a W3 crossing
can have degree 4 and lie in no ℚ(√d)).

Corner-meeting-corner and edge-lying-in-a-face are codimension **2** — not
walls, despite sounding like they belong.

## 4. Counting laws and named results

**Ceiling law** — C(l, n) = (12l − 6)n − 2(l² − 1) bounds the depth-*l* count
for l ≥ 2. Never exceeded in ~1M configurations; proved only for l = 1.

**Anchor lemma** — the proved l = 1 case, d_{n−1} ≤ 6n, via the radial
envelope having local minima only at the 6n face centres.

**Cap-sum** — 1 + Σ C(l, n), the total if every layer hit its ceiling at once.

**Frustration** **(ours)** — from n = 4 up, the depth layers cannot all be
maxed simultaneously; they must be traded. This is why the problem changes
character at four cubes, and why n = 3's maximum is forced to be irrational
(rigid demands land on isolated points; trades live on open sets).

**Frustration deficit** — the observed gap, conjecturally 6(n−3)(n−2), between
the cap-sum and the true maximum.

**Increment identity** — T = count(S_j) + Δ_j, where S_j is the compound minus
cube j. Δ_j equals |V(G)| − #components(G_j) exactly, with G the region
adjacency graph including the outside region and G_j its bit-j subgraph.

**B_j** **(ours)** — the derived bound Δ_j ≤ B_j = 1 + c + Σ_v (deg(v)/2 − 1),
an Euler cell count of the arrangement the other cubes' planes trace on ∂C_j.

**E1 / E2** — measured envelopes. E1: a six-cube total never exceeds its best
five-cube subset by more than 336. E2: if any five-cube subset misses its deep
caps, the total is capped ~150 below the record. E1's *increment* is now
derived (B_j); its flat constant is still empirical.

**Theorem R** — rational configurations have rational O-reduced pair
invariants; the two n = 3 maximisers have ½+√2 and 3φ/2, so neither is
congruent to any rational configuration.

**Configuration vs class** — a CONFIGURATION is an actual placement in space, so
two rotated copies are different configurations. A CLASS is a configuration up
to rotation, and is what gets counted. Rotated copies are already identified in
any statement about classes; the 3-dimensional fibre of rotations inside a class
is bookkeeping about the unquotiented space and normally never needs mentioning.
Pinning a base (as the 727 work does) spends those 3 degrees of freedom exactly
so that every remaining move changes the class. Keep the words apart: sliding
between them makes it sound as though rotated copies were being counted
separately.

**Congruence class** — an equivalence class of configurations under "some
isometry fixing the origin carries one onto the other as a set". Restricting to
O(3) rather than the full isometry group E(3) = R^3 x| O(3) costs nothing: a
compound of origin-centred cubes has its centroid at the origin, so any isometry
between two of them carries centroid to centroid and therefore fixes the origin.
The translations are excluded by the geometry, not by assumption. Nor does the
O(3)-vs-SO(3) choice matter: Q = [-1,1]^3 is centrally symmetric, so -I fixes
every centred cube, and every improper isometry g = (-I)·r acts on these
compounds exactly as the rotation r does. The two groups give IDENTICAL orbits,
there is no handedness bit to gain, and -I sits in the stabiliser of every
configuration (so a stabiliser computed among rotations alone is the one that
measures the orbit). A congruence class here is one copy of SO(3) = RP^3. Note also that
an isometry is an ELEMENT of O(3); the 48 isometries carrying one cube onto a
DIFFERENT cube form a coset, not a subgroup (no identity), which is why they can
be counted but not composed. Three
redundancies are quotiented at once, and conflating them causes errors: a
GLOBAL g acting on the left (same g for every cube); a PER-CUBE ambiguity, since
Rᵢ and Rᵢ·u give the identical cube for any u in the octahedral group, so a cube
is a coset Rᵢ·O and not a rotation; and LABELLING, since the cubes are
unordered. Formally a point of O(3) \ (SO(3)/O)ⁿ / Sₙ.

Beware which space you are counting in. As a subset of all compounds, a single
class is an O(3) ORBIT — 3-dimensional, uncountably many members, one per rotated
copy in space. Pinning a base (as the 727 family does) spends exactly those 3
degrees of freedom, so within a pinned family a class has only finitely many
members (≤480) and moving through the family moves you BETWEEN classes. Both
"uncountably many classes" and "uncountably many members per class" hold, at
cardinality 2^ℵ₀; cardinality cannot separate them and DIMENSION is the
instrument that can — which is why "how many maximisers are there?" is
ill-posed and "what is the dimension of the maximiser set, and where are its
boundaries?" is not.

A congruence class is NOT "same region count", "same depth profile", "same
per-label profile" or "same μ". Those are INVARIANTS: a differing value proves
non-congruence, a matching value proves nothing. Every wrong class count in this
ledger came from reading an invariant as if it were a definition (§7).

**μ (the O-reduced pair invariant)** — max over H in the octahedral group of
trace(Rᵢᵀ Rⱼ H). Necessary for congruence, **not sufficient** — see §7.

**Step T** — a step in the max(3) = 67 proof. Its first route was false and was
replaced.

## 5. Workstream code-names

Older reports are named after these; without the key they are opaque.

**Golden compound** — the classical five cubes inscribed in a dodecahedron,
coordinates in ℚ(√5), 351 regions. Its sub-compounds give 1, 13, 67, 177.

**Octahedral / golden maximisers** — the two non-congruent three-cube maxima
(67 each), in ℚ(√2) and ℚ(√5) respectively.

**Dihedral family** — a closed-form one-parameter family of 3-cube compounds,
discovered from a human remark that near-miss edges appeared to lie in a plane
perpendicular to (1,1,1).

**Blueprint** — the combinatorial skeleton of a compound: how its cubes
partition into pair-relations. Searching blueprints, then optimising each over
its continuous knobs, is the branch-and-prune strategy.

**Glue / clique gluing** — building larger records by gluing dihedral-family
cliques on different axes; every record so far is such a gluing.

**Rattan** — the *rational-tangent* sweep, the slice records were found to live
in.

**nfamily** — the study of whether the dihedral family helps at n > 3 (verdict:
not as a search space, but records are family-position gluings).

**resonance4** — the algebraic search for an irrational "resonance" at n = 4
analogous to n = 3's. Resolved **negative**.

**slide3** — overlaying two sliding 3-cube triples (the 699 family).

**opencount** — the degree-agnostic exact-sign counting engine, for algebraic
points of degree > 2 that the ℚ(√d) engines cannot represent.

## 6. Method vocabulary

**Exact / two-engine rule** — no floating-point number decides anything, and
two independently written engines must agree before a count is believed.

**Gate** — a check whose expected value comes from an independent source (a
hand computation, an earlier engine, a published number), never from the code
being tested.

**Coverage artifact** — a search perfectly implemented over an accidentally
too-small parameter space. Guarded against by requiring the machinery to
reproduce the current record before its negatives count.

**Proxy invariant** — something correlated with the property you want rather
than equivalent to it. The richest source of confident wrong answers here; see
[`FAILURE_MODES.md`](FAILURE_MODES.md) §4.

**Route / signature** **(ours)** — the multiset of pair counts between the free
cube and each base cube, e.g. (9, 9, 4, 4, 4). Independent of depth profile.

**Rationally shadowed** **(ours)** — see §7; the meaning narrowed.

## 7. Terms whose meaning changed

Read these before trusting an older document.

**"Rationally shadowed"** — originally suggested that irrational record
configurations are somehow reducible to rational ones. It was only ever
established at the level of the **count**: 727 holds along a stretch of line
containing them, so rationals are dense nearby. Postscript [61](LEDGER.md#p61) then established
the configuration-level statement separately: an irrational point and its
shadow are the same combinatorial object at different parameters of one
rational family, with the type identical at the point and both neighbours in
105 of 183 cases.

**"Chamber boundary"** — was inferred from k ≥ 3 active walls. That inference
is wrong: most wall crossings leave the type unchanged, so k is not a proxy for
boundary. Postscripts [60](LEDGER.md#p60) → 61.

**"Records concentrate at high-multiplicity concurrences"** — reversed.
Measured over 1200 unselected draws, configurations counting ≥ 700 average 1.6
incidence hits, those under 650 average 92.6. The heuristic described 723.

**"W4"** — as *implemented*, the catalogue is "a free face plane through any
real triple point of the base", which is a **superset** of the pure
(1,1,1,1) type and includes some corner-on-face cases. Results attributed to
W4 refer to that catalogue.

**"12 congruence classes of 727, indexed by field"** — an artifact of using μ
(necessary, not sufficient) for congruence, and of a guard that made only some
fields countable. Now ≥ 161 configurations in 54 types, not indexed by field.

## 8. Overloaded terms

### 8.0 The rule: never use the bare noun

Every overload below is harmless in its COMPOUND form and dangerous when
abbreviated. So the convention for this project is not to rename anything — it
is to ban four bare words. Write the compound form every time, even when the
context feels obvious. (It cost a wrong step on 2026-08-04: the "360 crossing
lines" of Postscript [57](LEDGER.md#p57) were proposed as a bound on the 727 arcs, which are
lines in CONFIGURATION space, minutes after this very section was cited.)

| never write | in R^3, the cubes' own space | in configuration space |
|---|---|---|
| "point"  | triple point, corner, contact point | configuration, parameter point |
| "line"   | crossing line, edge line | arc, wall line |
| "plane"  | face plane | wall plane, locus plane |
| "isolated" | — | "isolated in the level set" vs "isolated as a solution of its conditions" — Postscript [47](LEDGER.md#p47) means the SECOND |

Two more that need a named space rather than a compound word:

* **dimension** — always say of WHAT: of a locus in configuration space, of a
  congruence class (always 3), or of the class set. "4-dimensional" and
  "1-dimensional" describe the same 727 component in different spaces.
* **degrees of freedom** — say GAUGE (rotating the whole compound; changes
  nothing observable) or MODULI (changes the congruence class). The 727
  component has 3 gauge + 1 moduli.



**Line** — almost always a *line in configuration space* (§2), not a line in
ℝ³. Base **crossing lines** (§3) are the exception: those are real lines in
space.

**Type** — the per-label vector (§2). Not "wall type" (§3), and not the
"family type" of older typology drafts.

**Point** — a *configuration* (a point of configuration space) or a *point in
ℝ³* (e.g. a triple point of the base arrangement). Both appear in the same
sentences constantly; §3's "real triple points" are the latter.

**Wall / condition** — a *wall* is the surface; a *condition* is the polynomial
whose vanishing defines it. One wall, one condition, but a condition may factor
(edge-edge conditions factor into two rational planes).

**Isolated** — for a *configuration*, means no continuum of the same count
around it (true at n = 3). For a *type*, means a zero-width chamber. The two
are different and n = 6 has the second without the first.
