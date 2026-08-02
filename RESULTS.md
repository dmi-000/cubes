# Current results

**What this file is.** Everything below is what the project believes *now*,
each item tagged with how strongly it is established. Nothing here is stated
and later retracted — claims that turned out wrong are listed once, in
[§7](#7-superseded-claims), with what replaced them.

For the dated blow-by-blow, including how each result was reached and what was
believed along the way, read the ledger
[`six_cube_search_results.md`](six_cube_search_results.md) (append-only,
ordered by write time; it has a postscript index at the top). For the
narrative synthesis read [`PROJECT.md`](PROJECT.md); for the story with the
wrong turns in place, [`JOURNEY.md`](JOURNEY.md).

Status tags:

| tag | meaning |
|---|---|
| **PROVED** | a theorem, with the proof written down and its hypotheses stated |
| **VERIFIED** | an exact count of a specific configuration, agreed by two independent engines |
| **EXHAUSTED** | a search that was complete over a stated family, not a sample |
| **CONJECTURE** | consistent with all evidence, not proved |

Last updated 2026-08-02.

---

## 1. The problem

Given *n* congruent unit cubes sharing a centre, each independently rotated,
count the bounded regions their surfaces cut space into. A region is a
connected component of constant **cube-containment** — you cross a real face
iff the set of containing cubes changes. Crossing the *infinite extension* of
a face plane, where that cube is absent, does not split a region. Every count
in this project uses that definition and exact arithmetic; no floating point
enters any decision.

## 2. Records

| n | best known | status | configuration |
|---|---|---|---|
| 2 | **13** | PROVED maximum | any angle about a shared body diagonal |
| 3 | **67** | PROVED maximum | octahedral ℚ(√2), and golden ℚ(√5) — two non-congruent maximizers |
| 4 | 183 | VERIFIED | wide-perturbation climb |
| 5 | 393 | VERIFIED | 5-subset of the n=6 record |
| 6 | **727** | VERIFIED | 393's five cubes + `7,14,1,-5` |
| 7 | **1217** | VERIFIED | the 727 six + `4,-3,-4,-4` |
| 8 | **1891** | VERIFIED | the 1217 seven + `3,-3,3,-8` |

The tower nests: 183 ⊂ 393 ⊂ 727 ⊂ 1217 ⊂ 1891, adjacent levels differing by
one cube. Depth profiles:

    727  = {214, 220, 156, 100, 36, 1}
    1217 = {278, 328, 260, 190, 118, 42, 1}
    1891 = {348, 452, 382, 302, 222, 136, 48, 1}

## 3. Theorems

- **max(2) = 13**, for any two convex cells with ≤ 6 faces each. PROVED. The
  bound is the convex-cover argument: A∖B is a union of at most 6 convex
  pieces, likewise B∖A, plus one core.
- **max(3) = 67**, for any three concentric convex ≤6-facet cells whose
  boundaries meet pairwise transversally — an open dense set including both
  maximizers. PROVED, in [`PROOF_67.md`](PROOF_67.md) +
  [`PROOF_STEP_T.md`](PROOF_STEP_T.md). Three Euler arguments: d₃ ≤ 1,
  d₂ ≤ 18 (convex cover), d₁ ≤ 48 (Euler on the top diagram, with the vertex
  weight split 32 + 60 between triple points and pairwise intersection
  polytopes). One caveat remains, inherited from the contact analysis: two
  cells meeting *tangentially* rather than transversally, a higher-codimension
  degeneracy.
- **d_{n−1} ≤ 6n for every n.** PROVED (the l = 1 ceiling law, via the anchor
  lemma: the radial envelope of any n-cube configuration has local minima only
  at the 6n face centres).
- **The one-cube increment is bounded by an Euler count on the added cube's own
  surface.** PROVED. With G the region adjacency graph including the outside
  region and G_j its bit-j subgraph, Δ_j = |V(G)| − #components(G_j) exactly,
  hence Δ_j ≤ |E(G_j)| ≤ B_j = 1 + c + Σ_v (deg(v)/2 − 1), the cell count of
  the arrangement the other cubes' face planes trace on ∂C_j. Measured slack
  1.00–1.11 over 21 (configuration, cube) pairs; G_j was a forest in all 9
  cases where it was computed, making the first inequality an equality too.
  Postscript 56.
- **727 is isolated on the 393 base, and its coincidence pattern is
  unaugmentable.** PROVED by elimination. Holding the five cubes of 393 fixed,
  a sixth has 3 degrees of freedom; its 36 active coincidence conditions cut
  that space to exactly one real point, and all 684 remaining conditions are
  inconsistent with them (Gröbner basis {1} in each case). Caveat: the Cayley
  chart used omits the 180° rotations.

## 4. Structure

- **The maximum at n = 3 requires irrational coordinates**, conditional on the
  two known maximizers being the only ones. The O-reduced invariant μ is
  rational for any rational configuration, and equals ½+√2 and 3φ/2 at the two
  maximizers. n = 3 is the only irrational rung of the tower.
- **n = 3 is the only level whose optimum set is finite and larger than one
  point.** At n = 2 the maximizers form a continuum (every angle about a body
  diagonal, plus a closed arc about an edge axis); at n = 6 the record value is
  attained by non-congruent compounds. Only at n = 3 is it exactly two isolated
  points.
- **The record tower nests at every level except n = 3.** The best triple
  inside any higher record is 63, four short of 67 — a consequence of the
  irrationality above, since every subset of a rational compound is rational.
- **727 is usually reached without a maximal pair, but not always.** Across the
  161 configurations the sixth cube's pair signature is (9,9,4,4,4) in 159
  cases, (9,9,9,4,4) once — the originally discovered record — and (13,5,4,4,4)
  once, which reaches 727 while *carrying* a 13-pair. The discovered record
  (18 interior crossings against 723's 48) is therefore atypical of its own
  plateau, and the "records avoid rigid maximal pairs" reading drawn from it
  holds for 160 of 161 configurations but is not a law.
- **727 is a plateau of at least 161 non-congruent compounds in 54
  combinatorial types**, after quotienting by each cube's 24 rotations AND by
  the base's own C₃ symmetry about (1,1,1) — which triple-counts if forgotten.
  They fall into only three depth profiles, all of which also occur rationally:
  {214,216,162,98,36,1}, {214,220,156,100,36,1}, {214,218,160,98,36,1}. Every
  class satisfies d₁+d₂+d₃+d₄ = 690 with d₅ = 36 and d₆ = 1 fixed. Eight of the
  fields reached are irrational — ℚ(√13), ℚ(√226), ℚ(√403), ℚ(√1093), ℚ(√1614),
  ℚ(√1785), ℚ(√1930), ℚ(√2741) — but every one is rationally shadowed, so
  irrationality does no work at n = 6, and the classes are NOT indexed by field
  (the O-reduced pair invariant that suggested that is only necessary for
  congruence, not sufficient). VERIFIED.
- **The irrational classes are the first configurations this project found by
  SEARCH rather than by symmetry.** The two n=3 maximizers came from the
  octahedron and the icosahedron; these came from enumerating strata.
- **Coincidence conditions are quadrics** in the Cayley coordinates of the free
  cube, and a 9-pair locus is codimension 1. So three walls meet in at most 8
  points by Bézout — which is why records sit at three-wall intersections.
- **The codimension-1 walls are exactly "four face planes concurrent"**, and
  classify by how the four distribute over cubes: (3,1) corner-on-face, (2,2)
  edge-edge, (2,1,1) edge meets a two-cube crossing line, (1,1,1,1) four planes
  from four cubes. The first two are enumerated; the last two never were.
  Corner-corner coincidence and edge-inside-a-face are codimension 2, so
  neither is a wall — though both occur in the 393 base. Postscript 57.
- **Edge-edge conditions factor into PAIRS OF RATIONAL PLANES**; corner-on-face
  conditions are IRREDUCIBLE QUADRICS. That difference decides the arithmetic:
  three planes always meet in a rational point, so edge-edge strata cannot
  contain an irrational configuration, while two planes and a quadric give a
  quadratic in one parameter — rational or ℚ(√d). The mixed family holds
  1 377 612 degree-2 solutions against 2 856 rational ones.

## 5. Conjectures

- **d₃ ≤ 164, d₄ ≤ 102, d₅ ≤ 36** and the general ceiling law
  C(l,n) = (12l−6)n − 2(l²−1) for l ≥ 2. Never exceeded in ~1M configurations;
  proved only for l = 1.
- **max(6) ≤ 729.** The envelope bound gives T ≤ S_max + 336, and 727 sits on
  the 393 five-subset, so only 729 remains available on that base. The
  constant 336 is still MEASURED. The increment it bounds is now derived
  (Postscript 56): T = S_j + Δ_j with Δ_j ≤ B_j, an exact Euler cell count on
  the added cube's surface, ≤ 11% above the true increment everywhere tested —
  but its universal ceiling at n = 6 is 872, so this conjecture is not yet a
  theorem.
- **The frustration deficit is 6(n−3)(n−2)** — the gap between the cap-sum
  1 + Σ C(l,n) and the true maximum. Exact at n = 3, 4, 5 (0, 12, 36); predicts
  max(6) = 729, max(7) = 1223, max(8) = 1907. A three-point fit, two of whose
  points are records rather than proved maxima. Its n = 6 prediction agrees
  with the envelope bound above, independently.

## 6. What searching has established

- **Extension beats native search.** A record at level n, extended by one cube,
  outperforms a full campaign at level n+1. Every record from n = 6 up was
  found this way, and improvements propagate both directions: better n=6 lifts
  n=7 and n=8 within one pass, and searching n=8 has twice improved n=7 as a
  byproduct.
- **Menu shape matters more than menu size.** 723 stood for weeks because every
  campaign sampled small quaternions; 727's sixth cube was found immediately by
  sampling component heights log-uniformly to 512. Its winning cube was inside
  the old norm bound all along — the gap was sampling density, not reach.
- **Three-wall intersection is the best search method found.** Solving one
  coincidence condition against each of three fixed cubes reaches 727 at ~30×
  the hit rate of random menus, and found 727 compounds that eight prior
  campaigns missed. Because the walls factor into planes, the whole family is
  134 784 linear systems giving 2 733 distinct configurations — EXHAUSTED in
  four minutes, max 727. A Gröbner enumeration of the same family ground
  through 1.3 million systems to cover part of it; ~99% of that work was
  re-deriving identical plane triples.
- **Irrational configurations are now countable at scale.** `cube_regions_q2`
  generalises the integer engine's scalar type to ℤ[√d] and runs ~100× faster
  than the Python algebraic path. 224,184 irrational configurations have been counted: nothing above 727. Every earlier campaign in this
  project sampled integer quaternions, so this stratum was structurally
  invisible to all of them.
- **Nothing above 727 has been found at n = 6** by: random menus (100k sixth
  cubes), swap-completion from all six five-cube bases, a balanced climb on the
  worst-subset objective, core-and-clique construction from the 183 core, the
  exhausted three-wall family (2 733 configurations), pure corner-wall triples
  (best 719), the rational half of the mixed family (best 725), or 224,184 irrational
  configurations across the fields the overflow budget admits.

## 7. Superseded claims

Each of these was believed and acted on; each is now known to be wrong. Listed
so the record is honest, and confined here so no reader picks them up as
current.

| claim | status now | corrected in |
|---|---|---|
| Off-centred cubes and general hexahedra beat the records | **REFUTED** — an artifact of counting sign-vector cells of the infinite face planes instead of containment regions | Postscript 38 |
| The n = 2 optimum (13) is rigid and near-isolated | **REFUTED** — it is a continuum: 13 holds at every angle about a body diagonal | Postscript 44 |
| Step T reduces to "deg_top ≤ deg_bot at triple points" | **REFUTED** — false; a corner with two blades gives deg_top 8 against deg_bot 4. The theorem holds by a different argument | Postscripts 42, 43 |
| 723 is the n = 6 maximum, cornered three independent ways | **SUPERSEDED** — 727 | Postscript 46 |
| n = 7 = 1211 and n = 8 = 1889 | **SUPERSEDED** — 1217 and 1891, the same day | Postscript 46 |
| 393 is reachable only as a subset of the n = 6 record | **REFUTED** — a wide-height menu on 183 reaches it bottom-up; the claim was an artifact of small-quaternion search | Postscript 46 |
| 727 is a plateau (first claim, from a second sixth cube with the same count) | **WITHDRAWN then RE-ESTABLISHED** — that cube is congruent to the original; two genuinely non-congruent 727s were later found with a different depth profile | Postscripts 46, 48 |
| The absence of irrational solutions in the wall strata says something about the problem | **ARTIFACT** — edge-edge conditions factor into rational planes, so those strata are all-rational by construction; the mixed strata are 240:1 irrational | Postscripts 49, 50 |
| Porting the algebraic engines to C++ is not worth it | **REVERSED** — that verdict rested on solution fields reaching degree 8, measured on edge-edge systems which turn out all-rational anyway; the volume is degree-2 mixed strata, and the engine found the irrational 727 | Postscripts 47, 50, 51 |
| The overflow budget's invariant is d·m² | **REFUTED** — tracing \|p\| and \|q\| separately shows the boundary is not constant in m²·d; the flat rule is over-permissive below d ≈ 38 (at d=5 it would admit m=2289 against a true limit of 1855) | Postscript 51 addendum 2 |
| The Cayley chart omitting w = 0 leaves 180° rotations unreachable | **REFUTED** — q·(0,1,0,0) is a cube self-symmetry, so the chart omits quaternion representatives, not compounds; a second chart returns an identical census | Postscript 49 addendum |
| ℚ(√13) is the only field whose strata reach 727; the irrational 727 is a fifth class | **REFUTED** — both were properties of a guard that made only 56 fields countable. Widening it gives eight fields and at least twelve classes | Postscript 51 addendum 3 |
| A 9-pair is characterised by a shared face axis | **REFUTED** — 727 contains three 9-pairs and no two of its cubes share a face axis | Postscript 47 |
| More coincidences imply a higher count | **REFUTED** — 727 has 18 interior crossings to 723's 48, and counts more | Postscript 47 |
| The E1 derivation fails because "each connected piece adds at most one region" is false for non-disk pieces | **REFUTED** — the piece bound was never needed; the real error was scoring twelve TANGENT vertices as zero, and the stated counterexample (∂B ∩ int A connected with six boundary circles) is geometrically false — it has six components | Postscripts 53, 56 |
| Records concentrate at high-multiplicity concurrences | **REVERSED** — the sweet-spot caveat was noted early (Act III: "more alignment is not better"), but the heuristic still drove the searches. Measured, the correlation is negative. Over 1200 unselected draws, configurations counting ≥ 700 average 1.6 hits on the base's triple-point walls; those counting < 650 average 92.6. The heuristic described 723, which is exactly the 54-crossing corner family | Postscripts 55, 57 |
| Corner-corner and edge-in-face are unmodelled wall types | **RECLASSIFIED** — both are codimension 2, so neither is a wall. The genuinely unenumerated codimension-1 types are (2,1,1) and (1,1,1,1) | Postscript 57 |

Two methodological errors are worth carrying forward, because both produced
plausible numbers rather than obvious failures. Counting cells of the infinite
plane arrangement instead of containment components inflated every count and
produced a string of false records. And measuring rigidity by *openness* —
perturbing randomly and asking whether the count survives — reports every
measure-zero wall as rigid, which is why the 13-pair continuum went unnoticed
for weeks.
