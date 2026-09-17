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

## 8. Overloaded symbols — `c`, and how each occurrence is told apart

Added 2026-09-15. The letter `c` carries five distinct meanings in this project. **Every
occurrence in the current documents is disambiguated by its immediate context** — checked, not
assumed: filtering out the occurrences that carry their context leaves nothing behind. So this
is a hazard for what gets written NEXT, not a defect in what is written now, and no rename is
proposed.

| form | meaning | how you know |
|---|---|---|
| `c_ell`, `c_1`, `c3` | connected components of the level-ℓ graph — the dominant use, 115+ occurrences | appears alongside `d_ell`, `V`, `E`, `tau3`, `W0`, or in `E − V + c + 1` |
| `c0` | the ZERO-COORDINATE INDEX of a wall key, a value in 0..2 | always inside `(frame, group, sig, c0)` or indexing a 3-vector: `m1[c0]`, `sum_{c != c0}` |
| `C3` | the cyclic group of order 3 | capital C, and the word *quotient* or *symmetry* nearby |
| `C(l, n)` | the ceiling-law function | capital C with two arguments |
| `(c2)`, `(c3)` | case labels in [P273]'s classification | wrapped in parentheses, following the word *classification* or *case* |

**The one to watch is `c0`.** It looks like "c at level 0" and is not: it is an index naming
which coordinate vanishes, a different TYPE from a component count. Misread, it would be
silently wrong rather than obviously wrong. It currently never appears outside its tuple or an
indexing expression — **keep it that way**, and if it ever needs to stand alone, write
`zero-coordinate index` in words.

**Rule for new writing:** a bare `c` means the component count. Anything else gets its context
on the same line, or a different letter.

**`h` IS NOT FREE — it means HEIGHT.** The largest absolute component of an integer quaternion:
`h = 140` and `h = 113786` name the two n = 9 representatives (`simplified_h140`,
`original_h113786`), "height" appears ~170 times in the documents, and it is the subject of
[METHODS 15] — a refusal is usually about the height of the representative, not the question.
Recorded because `h` for *hole* was proposed on 2026-09-15 and had to be withdrawn: the hole
count is a real and useful quantity (`c_ell - 1`, see 8b) but it has no free letter, and is
written out as `c_ell - 1` rather than given one.

### 8a. The two Euler relations have the same SHAPE and different content

Noticed by the user, 2026-09-15, and it is the sharpest form of the `c` collision.

    3D, the whole arrangement     V - E + F - C = 1      C = REGIONS      183, 393, 727
    2D, one level, on a sphere    V - E + F - c = 1      c = COMPONENTS   1 or 2

Both verified: the first exactly on the n = 4, 5, 6 records via `cellcomplex.complexus`
(V=194/400/790, E=498/1080/2116, F=488/1074/2054), the second as [P312]'s
`d_ell = E - V + c + 1` against the engine, 43 of 43.

**Why they differ despite the identical shape: the per-level relation is ONE DIMENSION DOWN.**
There `F_ell = d_ell` is the depth-`ell` REGION count, so regions occupy the **F** slot; in the
3D relation they occupy the **C** slot. The final term is regions in one and components in the
other.

**So `c` is NOT a region count** -- but writing `V - E + F - C = 1` with `C = 183` is completely
natural, and it puts the project's headline quantity in the same position where `c_ell ∈ {1,2}`
lives. Anyone carrying intuition from one relation to the other will be out by a dimension.

**Convention:** write `C` (capital) only for the 3D region count, `c_ell` (subscripted, lower
case) only for the per-level component count, and never either one bare in a context where both
relations are in play.

### 8b. What `c_ell ∈ {1, 2}` actually means

**`c_ell = 1`** — every face of the level-`ell` decomposition is a DISK. Equivalently: on every
cube, every maximal patch of points at that depth is simply connected.

**`c_ell = 2`** — exactly one face is an ANNULUS. On one cube, the points at that depth form a
BAND that encircles the cube, with a deeper patch enclosed inside it. The band's two edges are
the two graph components, swapped by the antipodal map — which is [P268]'s observed shape,
`0 self-antipodal + 1 pair`, arrived at independently.

**The chain, with what is verified at each step.**

1. `c - 1 = sum_f (b(f) - 1)` on a sphere, so `c = 2` forces exactly one face with two boundary
   circles — an annulus.  *Standard, and the relation is verified by [P312] 43 of 43.*
2. A face is a connected component of the depth-`m` set on ONE cube's boundary, spanning
   facets across creases, since a crease is a fold and not a separator.  *[P312].*
3. Depth is non-increasing radially from every facet centre, so a depth-band naturally rings a
   deeper core.  *The facet-centre lemma, [P311], proved.*
4. **Measured here: no facet of any `c = 2` instance carries a wrap-around band** (0 of 24
   facets, three instances).  So the annulus is not a ring around a facet centre.
5. Therefore it closes by going around the CUBE, through several facets.  *Forced by 1, 2 and
   4 — a deduction, not a mechanism claim.*

**This explains the confinement to level 1 ([P319]).** A band has to run all the way round
without being cut, and the outermost shell is where the depth patches are largest and least
fragmented; deeper levels are nearly pure degree-3 and broken into many small faces
([P315]). It also explains the rarity — 1.6 % — and why a transition is a pure RECONNECTION
([P321], `dV = dE = 0`): the band closes or breaks when two arcs touch and rewire, which
creates and destroys nothing.

### 8c. The other overloaded symbols, worst first

Audited 2026-09-16, prompted by "b for band?" — `b` is not free either. Ordered by how
plausible a wrong reading would look, because a collision that produces nonsense is harmless and
one that produces a believable number is not.

**1. `l` versus `ell` — THE DANGEROUS ONE. The two level indices run in OPPOSITE directions.**

    C(l, n) = (12l - 6)n - 2(l^2 - 1)      l counts from the INSIDE:  l = 1 is the innermost
    d_ell, c_ell, V_ell, E_ell             ell counts from the OUTSIDE: ell = 1 is the outermost
    the bridge:   l = n - ell

This is already explicit in the glossary and easy to miss: the anchor lemma is "the proved
`l = 1` case, `d_{n-1} <= 6n`" — `l = 1` and `d_{n-1}` are the same level. Mixing them gives a
ceiling for the wrong layer, which is a plausible number rather than an absurd one. **Verify the
direction before quoting any ceiling.**

**2. `d1` versus `d_1` — one underscore apart, 235 uses against 12.**

    d1, d2      DENOMINATORS in the wall polynomial: P = ... - (m2[c0] d1 - m1[c0] d2)
    d_1, d_ell, d3   the DEPTH COUNTS, the region totals per level

**3. `m`** — `m_v` is the number of levels a vertex appears at ([P248]); `m1[...]`, `m2[...]`
are the NORMAL VECTORS of the wall formula; a bare `m` is usually a depth index.

**4. `b`** — `b_v` is the number of cube BODIES through a vertex ([P248]'s `m_v = b_v - 1`, and
the same thing as a "b-fold point"); `b(f)` is the number of BOUNDARY CIRCLES of a face. Bodies
and circles, same letter. **So `b` is not available for *band* either.**

**5. `c`** — five meanings, see 8 and 8a.

**Decided: the hole count is written out.** `c_ell - 1`, or the word *holes*. It has no free
letter — `h` is height (8), `b` is bodies and boundary circles, `c` is components — and
inventing one against that much traffic is how the collisions above got made.

### 8d. Negative level indices — proposed, and they retire the `l` / `ell` collision

Suggested by the user, 2026-09-16: use one level index with a sign, the way a negative array
index counts from the far end.

    d_{+1}  outermost layer          ell = +k  counts INWARD  from the outside  (existing use)
    d_{-1}  innermost layer          ell = -k  counts OUTWARD from the inside   (new)
    bridge:  d_{-k} = d_{n-k}

**This eliminates 8c's worst collision.** The ceiling law's inward-counting `l` was a second
letter for the same axis running the other way; it becomes `-ell` and the letter `l` is retired:

    old:  C(l, n) bounds the depth-l count, l = n - ell     two letters, opposite directions
    new:  d_{-k} <= C(k, n)                                 one index, signed

**IT ALSO MAKES TWO RESULTS n-INDEPENDENT.** Measured on the records:

    n     d_{-k}, inner -> outer            ceiling C(k,n)                 slack
    4     24, 66, 92                        24, 66, 104                    0, 0, 12
    5     30, 78, 128, 156                  30, 84, 134, 180               0, 6, 6, 24
    6     36, 100, 156, 220, 214            36, 102, 164, 222, 276         0, 2, 8, 2, 62
    7     42, 118, 190, 260, 328, 278       42, 120, 194, 264, 330, 392    0, 2, 4, 4, 2, 114

- **`d_{-1} = 6n` exactly at every record.** In outward indexing this is `d_{n-1}`, a name that
  changes with every level; inward it is always `d_{-1}`.
- **The slack concentrates at the OUTERMOST layer** — 12, 24, 62, 114 — while the inner layers
  sit at or within a few of their caps. That is [P258]'s "the caps cannot all be attained"
  localised: the frustration lives at the outside.

**BOTH SIGNS EARN THEIR KEEP**, which is why one direction was never enough: holes occur only at
`ell = +1` ([P319], outermost) and ceiling saturation only at `ell = -1` (innermost). The
arrangement has two ends and they behave differently.

**Adoption is additive, not a rename.** Positive indices keep their current meaning and all
existing `d_ell` / `c_ell` references stand; negative indices are new vocabulary for statements
that are natural from the inside. Nothing needs rewriting.
