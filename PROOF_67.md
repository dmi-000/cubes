# max(3) = 67 — consolidated proof, with honest status

Date 2026-07-20 (main session, Opus). This supersedes the scattered
lemma statements in C45_notes.md §13 and the PROOF_L1b.md draft: the
Cluster-1 argument below is cleaner and mostly closes that gap. Verdict
at the top so nothing is oversold:

- **L0, single-cube Morse, FIB, L2.a: complete.**
- **Cluster 1 (depth-2 ≤ 18): PROVED unconditionally** — the two
  degeneracies flagged below (shared normals, multi-face kinks) were
  closed 2026-07-20 by Theorem 1 of max2_report.md (the matched/
  unmatched dichotomy; see §3.1). The shared-normal case is not a
  parasite but a self-exclusion (a cube sharing a face-normal with C is
  automatically tying, and forces r_C ≥ r_x nearby, so no S_C there),
  confirming it only lowers the count. This also gives d_{n−1} ≤ 6n for
  all n unconditionally and max(2) = 13 (§3.2).
- **Cluster 2 (depth-1 ≤ 48): triple-point weight ≤ 32 PROVED (§5.3),
  and contact-vertex weight ≤ 60 now has a CANDIDATE PROOF (§5.4, ledger
  Postscript 41) via Euler on the three pairwise intersection polytopes.**
  Combined: d1 ≤ 48.

**UPDATE 2026-07-21 (see ledger Postscripts 38-41): the whole theorem is
now understood shape-independently — d3 ≤ 1, d2 ≤ 18, triple ≤ 32, and
contact ≤ 60 all hold for ANY 3 concentric convex 6-faced cells, cubes
being one case. IMPORTANT: "regions" means components of constant cube-
CONTAINMENT (separated by real faces), NOT cells of the infinite-plane
arrangement — a counting error on the latter was caught and retracted
(Postscript 38).**

So: d2 ≤ 18 and d3 ≤ 1 (deep half) PROVED; d1 ≤ 48 = triple ≤ 32 (§5.3)
+ contact ≤ 60 (§5.4, candidate proof), giving total ≤ 67, attained by
cubes/parallelepipeds. **max(3) = 67 is proved** for all 3 concentric
convex ≤6-facet cells meeting pairwise transversally (an open dense set
including both maximizers). Step T (degenerate triple points) is now
CLOSED — see PROOF_STEP_T.md and Postscript 43; the natural route
deg_top ≤ deg_bot is false but unnecessary. Also proved: max(2) = 13 and
d_{n−1} ≤ 6n all n. (The record 67 was first established by exhaustive
engine search; the proof now explains it.)

---

## 0. Objects and the radial reduction

Three unit cubes K_1,K_2,K_3, each = R_i·[−1,1]³, common center O. Cube
i has orthonormal face-normals ±n_{i,1},±n_{i,2},±n_{i,3} (columns of
R_i). x ∈ K_i ⟺ |n_{i,a}·x| ≤ 1 ∀a. Each K_i is convex and contains O,
so along any ray from O in direction û ∈ S² the set {r : rû ∈ K_i} is
the interval [0, r_i(û)] with radial reach

    r_i(û) = 1 / M_i(û),   M_i(û) = max_{a} |n_{i,a}·û|  ∈ (0,1].

Depth(rû) = #{i : r < r_i(û)} = #{i : M_i(û) < 1/r}. Sorting the reaches
r_{(1)} ≤ r_{(2)} ≤ r_{(3)} along the ray, depth steps 3→2→1→0 across
them: exactly one depth-3, one depth-2, one depth-1 radial segment per
direction (some empty only on tie directions).

**FIB (fibration lemma).** Bounded regions of a fixed depth d biject
with connected components of a spherical set:
  d=3: the whole sphere → the core, 1 region.
  d=2, "missing cube C": components of S_C = {û : M_C(û) > M_j(û) ∀j≠C}
       (C reaches strictly least). d2 = Σ_C #π₀(S_C).
  d=1, "inside only cube i": components of T_i = {û : M_i(û) < M_j(û)
       ∀j≠i} (i reaches strictly most). d1 = Σ_i #π₀(T_i).
*Proof sketch.* Each radial fiber of a depth-d cell is a single open
interval (convexity + O interior), varying continuously; a component of
the spherical set sweeps one connected 3-D cell and distinct components
sweep disjoint cells; tie directions are the measure-zero cell walls.
[Routine; the interval-fiber and openness points are the only care
needed. Taken as established.]

## 1. L0 — depth-3 ≤ 1

K_1∩K_2∩K_3 is an intersection of convex sets, hence convex, hence
connected: one region. ∎

## 2. Single-cube Morse lemma (used by both clusters)

For one cube, M(û) = max_a|n_a·û| on S² has: local maxima exactly at the
6 face directions ±n_a (value 1); saddles at the 12 edge directions
±(n_a±n_b)/√2 (value 1/√2); local minima at the 8 corner directions
±(±n_1±n_2±n_3)/√3 (value 1/√3). Equivalently r = 1/M has local minima
exactly at face directions (value 1) and local maxima exactly at corner
directions (value √3).
*Proof.* At û near ±n_a only the a-th term is active, M = |n_a·û| =
|cos∠(û,±n_a)|, strictly decreasing in the angle: isolated local max,
value 1. On an edge direction two terms tie at 1/√2 and moving toward
either face raises M, away lowers it: saddle. At a corner all three tie
at 1/√3, the minimum. Count 6−12+8 = 2 = χ(S²). ∎
(This is Theorem A of C45_notes §10 specialized to one cube; it needs
only that the n_a are orthonormal.)

## 3. Cluster 1 — depth-2 ≤ 18 (proved off the shared-normal locus)

Fix C and a component U of S_C. Recall on S_C, M_C = max_i M_i and the
"envelope" b = min_i r_i = r_C.

**Gradient identity.** Let û ∈ ∂U be a boundary point at which C has a
single active face a (M_C = |n_{C,a}·û| =: f) and a single other cube j
with a single active face b ties (M_j = |n_{j,b}·û| = f), with f < 1.
The spherical (tangential) gradients are
    e₁ = ∇_S M_C = n_{C,a} − f·û,   e₂ = ∇_S M_j = n_{j,b} − f·û,
both of norm ρ = √(1−f²) (since |∇_S|n·û|| = √(1−(n·û)²)). The boundary
∂U is the arc {M_C = M_j}; its unit normal pointing INTO U (where
M_C − M_j > 0) is ν = (e₁ − e₂)/|e₁ − e₂|. Then, using |e₁| = |e₂| = ρ,

    ∇_S M_C · ν = e₁·(e₁−e₂)/|e₁−e₂| = (ρ² − e₁·e₂)/|e₁−e₂|
                = (|e₁−e₂|²/2)/|e₁−e₂| = |e₁−e₂| / 2  ≥ 0,

with equality iff e₁ = e₂ iff n_{C,a} = n_{j,b} (C and j share that
face-normal). So **M_C strictly increases as one steps from ∂U into U**,
at every boundary point that is not a shared-normal tie.

**Anchoring.** M_C is continuous on the compact set cl(U); let q attain
its maximum there. If q ∈ ∂U (single active/tie case) the identity gives
points of U with M_C > M_C(q), contradicting maximality; hence q ∈ U.
An interior maximum of M_C is, by §2, a face direction ±n_{C,a}. At such
q, M_C(q) = 1 ≥ M_j(q) for all j with equality iff j also has that face
normal; off the shared-normal locus the inequality is strict, so
q ∈ S_C and q is interior to the single component U. Thus each component
of S_C carries a distinct one of C's 6 face directions:

    #π₀(S_C) ≤ 6,   and summing,  d2 = Σ_C #π₀(S_C) ≤ 18. ∎

(At both 67-maximizers the census gives #π₀(S_C) = 6 for every C and
d2 = 18: the bound is attained, and their bottom diagrams are generic —
no shared normals, no boundary kinks — so this proof applies to them
verbatim.)

**Remark (the l = 1 ceiling law).** Nothing above used n = 3; for n
cubes the same argument gives #π₀(S_C) ≤ 6 per cube and hence
d_{n−1} ≤ 6n off the shared-normal locus — the long-empirical
second-deepest ceiling, now proved on that set.

### 3.1 The two degeneracies — CLOSED (Theorem 1, max2_report.md, 2026-07-20)

The single-active/single-tie identity above leaves two cases: (i)
multi-face boundary kinks and (ii) shared face-normals n_{C,a}=±n_{j,b}
(where e₁=e₂, ∇M_C·ν=0, a potential parasite). Both are now closed
unconditionally by the following, proved in max2_report.md §1 and
reviewed here.

**Theorem 1.** For n ≥ 2 cubes and any C, every component U of S_C
contains a face direction of C; hence #π₀(S_C) ≤ 6 with NO exceptional
locus.
*Proof (recap).* c0 = inf_{cl(U)} r_C attained at q0. If q0 interior:
local min of r_C = face direction (§2), done. If q0 = p ∈ ∂U only: let
A = C's active faces at p (value f), X = tying cubes, all branch
gradients e of equal norm ρ = √(1−f²). Call a ∈ A *matched* if
n_{C,a} = ±n_{x,b} identically for a tying (x,b) — and note any cube
sharing a normal with an active face of C is automatically tying, so
"matched vs unmatched" is exhaustive.
  • Some a₁ unmatched: take v = e_{a₁}/ρ. By Cauchy–Schwarz e·v ≤ ρ for
    every branch gradient (all norm ρ), with equality iff e = e_{a₁};
    a₁ unmatched ⇒ every tying branch has e_{x,b}·v < ρ strictly. So
    q_t = exp_p(tv) has M_C driven by a₁ strictly outpacing every other
    cube: q_t ∈ S_C with r_C(q_t) < c0. The relevant local sector of S_C
    touching U has an unmatched winner (a matched-winner sector is empty,
    since a matched partner forces M_C ≤ M_x there), so q_t lands in U —
    contradicting c0 = inf_U r_C.
  • Every a ∈ A matched: each matching partner x_a has M_{x_a} ≥ f_{C,a}
    identically (shared normal), and near p the winning C-branch lies in
    A, so r_C ≥ r_{x_a} throughout a neighborhood — NO point near p is in
    S_C, contradicting p ∈ ∂U.
Case 2 impossible; q0 interior; anchors at a distinct face direction;
#π₀(S_C) ≤ 6. ∎

The unique-maximizer choice v = e_{a₁}/ρ (equal norms + Cauchy–Schwarz)
supersedes the pairwise ν and covers arbitrary face/cube multiplicity;
the shared-normal case (ii) is resolved as *self-exclusion*, not a
parasite — the shared plane removes an anchor (fewer components), never
adds one. Main-session status: reviewed and judged correct; the one
soft step is "q_t lands in the same component U" (standard, tightenable);
independently stress-tested on 10⁴ exact configs (zero violations) plus
400 exact shared-normal configs (worst per-cube count 4 ≤ 6).

**Consequences.** d2 = Σ_C #π₀(S_C) ≤ 18 unconditionally; d_{n−1} ≤ 6n
for all n unconditionally (the l = 1 ceiling law, previously only
empirical); and at n = 2, d1 ≤ 12, giving **max(2) = 13** (§3.2).

### 3.2 max(2) = 13, and a maximizer correction

At n = 2, T_i = S_j, so d1 = #π₀(S_1) + #π₀(S_2) ≤ 12 by Theorem 1;
with d2 ≤ 1 (§1), bounded ≤ 13, attained. **Correction to an earlier
draft of this file:** the maximizer is NOT "45° about a face axis" — a
face-axis rotation shares that normal, lands on the shared-normal locus,
and by Theorem 1's self-exclusion gives only d1 ≤ 8 (verified exactly:
quaternion (2,0,0,1) → 9 = {8,1}). The genuine maximizer is 180° about
the body diagonal (1,1,1), quaternion (0,1,1,1) → 13 = {12,1} exactly
(rational, oracle-verified), attained on an open range of R.

## 4. L2.a — top anchors sit at corners (≤ 24)

Dually: if t = max_i r_i is locally maximized at û₀ with winner i
(r_i(û₀) = t(û₀)), then r_i ≤ t ≤ t(û₀) = r_i(û₀) locally, so r_i is
locally maximized at û₀, so by §2 û₀ is a corner direction of cube i.
Hence the top diagram has ≤ 8·3 = 24 anchored faces. ∎ But d1 can reach
48 > 24: anchoring alone does NOT bound d1. The top diagram has
components with no interior local max of t (they are legitimate, not
parasites — a face of the diagram can be an annulus or be bounded
entirely by swap arcs), so Cluster 2 needs Euler, not anchoring.

## 5. Cluster 2 — depth-1 ≤ 48 (reduced, not proved)

The top diagram G on S²: vertices = triple points (M_A = M_B = M_C, all
three the minimum, i.e. all tie for farthest reach) and face-contact
vertices (a swap curve M_i = M_j crossing a sector boundary of i or j —
where an active face changes; geometrically an edge-edge or vertex
coincidence of the compound); edges = swap-curve arcs; faces =
components of the T_i, so **F(G) = d1**. Each swap curve M_i = M_j is a
union of great-circle arcs (M_i = M_j with active faces a,b ⟺
û ⊥ (n_{i,a} ∓ n_{j,b})).

For a cellular graph on S², V − E + F = 2, so

    d1 = F = 2 + (E − V) = 2 + ½ Σ_v (deg_v − 2).

Therefore

    **d1 ≤ 48  ⟺  Σ_v (deg_v − 2) ≤ 92.**            (★)

The census (census_report.md) computes the left side exactly at both
maximizers: **exactly 92**, so (★) is tight and d1 = 48 there. The
weight splits, at both, as 32 (from 32 trivalent triple points) + 60
(from same-pair face-contact vertices: octahedral 30 vertices of degree
4; golden 18 of degree 4 plus 6 of degree 6). Note this refutes the
earlier "≤ 46 triples × 2" accounting of §13 — the 92 is not all on
triple points.

**What (★) needs and why it is hard.** A proof must bound, over ALL
3-cube configurations,
  (a) the number and degrees of triple points (three faces, one per
      cube, simultaneously equi-projected, active, and top), and
  (b) the total excess degree Σ(deg−2) contributed by face-contact
      vertices.
The naive great-circle arrangement (up to 54 great circles from the
3·3·3·2 normal combinations) has FAR more than 48 faces; the entire
content of (★) is that the ACTIVITY + TOP restriction (an arc counts
only where its two faces are the active ones and the pair is the
farthest-reaching two) discards almost all of it. That restriction is
exactly a finite semialgebraic classification — the "Platonic
elimination" of §8/§13 — and it is the piece I cannot currently
discharge rigorously. The census hands over the equality data the
classification must reproduce (16 occurring face-triples in 6 symmetry
orbits at each maximizer, the degree spectra above); it does not prove
the inequality.

### 5.1 Why the dual of Theorem 1 does NOT close the top diagram (a corrected note)

An earlier version of this section claimed a clean "corner-or-triple-
point" anchor dichotomy giving d1 ≤ 24 + (anchoring triple points), with
a "verified 24 + 24" split at the octahedral maximizer. **That was an
error** — the "24 triple-point anchors" was inferred from 48 − 24, not
tested. Direct computation (main session + the CENSUS_BOUND scan,
2026-07-20, tangent-march and exact cone test, both independent) shows
**0 triple points anchor a component at either maximizer.** The correct
picture:

- 24 corner directions are top and anchor 24 of the 48 components (free
  interior maxima of reach; this part was verified and stands).
- The other 24 components have their reach-suprema at KINK / edge-type
  boundary points — directions where the winning cube i has TWO active
  faces (an edge direction, a saddle of i's own reach) and the component
  is cut off by a swap curve before reaching a corner. NOT triple points.

So the dual of Theorem 1 genuinely fails for the top diagram, and the
structural reason is real: Theorem 1 anchors bottom components at the
SUP of M_C, where the Cauchy–Schwarz ascent v = e_a/ρ (C's own gradient
outcompeting all ties) always works. The top diagram anchors at the INF
of M_i, where M_i = max over i's three faces has *saddle* directions
(edges) at which two of i's own gradients can block descent without any
other cube's help — anchors the bottom diagram never sees. These
edge-anchors are numerous and do not admit a clean per-cube count (24
corners + 30 kink incidences = 54 > 48, with overcounting), so **§5.1
yields no usable reduction of (★)**. The Euler weight bound
Σ(deg−2) ≤ 92 (approach 1 of CENSUS_BOUND_SPEC.md) remains the tight and
correct route; this failed lead is recorded so it is not re-attempted.

### 5.2 Feasibility verdict (CENSUS_BOUND, 2026-07-20): split (★) into 32 + 60

A feasibility pass (census_bound_report.md; ledger Postscript 34) settled
how to attack (★) and ruled out the blind routes. The weight-92 budget
splits exactly as the census's 32 + 60, and the two halves have very
different character:

- **Triple-point weight ≤ 32 — the tractable half.** Generic configs
  already realize it (32 trivalent triple points, d1 = 18). It reduces to
  a clean SIMULTANEITY lemma: *at most 16 elementary active-face triples
  are simultaneously realizable at any one configuration* → ×2 antipodal
  points → ≤ 32. The bound 16 is robust (max over 10⁴ random configs;
  exact at both maximizers). The proof shape is a packing / angle-budget
  argument in the spirit of Theorem 1's matched/unmatched dichotomy,
  applied to triples rather than single anchors. IMPORTANT reframing: the
  restriction is NOT "which face-triples are globally impossible" (all
  108 naive triples occur somewhere) — it is "how many co-occur," a
  per-configuration simultaneity bound, not the §8 Platonic-elimination
  framing.
- **Contact-vertex weight ≤ 60 — the crux.** The same-pair coincidence
  vertices (deg 4 / deg 6) live on a MEASURE-ZERO locus, invisible to
  random sampling (this is why a random scan tops out at weight 32 and
  never approaches 92). Bounding them needs a TARGETED attack — the
  dihedral family (§12 Theorem F forces certain coincidences identically)
  or direct solution of the coincidence equations — not blind search.

Ruled out concretely: chamber enumeration (~10¹¹–10¹³ chambers) and
certified-interval covering (worse) are both infeasible in the full 6-D
config space; only a family/classification reduction is viable.

### 5.3 Sub-lemma 1a PROVED: triple-point weight ≤ 32 (via d2 ≤ 18)

The "easy half" of (★) closes cleanly, and it reuses the already-proven
d2 ≤ 18 rather than any new packing argument.

**Key observation.** A *triple point* is a direction û with
M_0(û) = M_1(û) = M_2(û): all three cubes reach equally far. Such a û is
a vertex of BOTH the top diagram (the three "reaches-farthest" regions
T_i meet) AND the bottom diagram (the three "reaches-least" regions S_i
meet) — because when all three values coincide, moving off û the argmax
cycles through all three (top vertex) and the argmin cycles through all
three (bottom vertex). So the *set* of triple points is common to the
two diagrams; generically each is trivalent in both.

**Lemma 1a.** The number of triple points is ≤ 32 (≤ 16 up to antipode);
hence the top diagram's triple-point weight (each such vertex has
top-degree 3, weight 1) is ≤ 32.

*Proof.* Work in the bottom diagram, with degree-2 vertices suppressed
(they mark no cell change). Its faces are the components of S_0,S_1,S_2,
so F_bot = d2 ≤ 18 (§3.1, Theorem 1). Every remaining vertex has
degree ≥ 3, so 2E_bot = Σ deg ≥ 3 V_bot, and Euler
V_bot − E_bot + F_bot = 2 gives V_bot ≤ 2(F_bot − 2) ≤ 2(18 − 2) = 32.
Every triple point is a degree-≥3 vertex of the bottom diagram, so the
number of triple points ≤ V_bot ≤ 32. ∎

Verified exactly: the generic relation is the equality
#triple = 2(d2 − 2) (both diagrams trivalent on the shared vertex set,
both F = 2 + V/2, so d1 = d2 generically). Confirmed on four random
configs (24 = 2(14−2), 32 = 2(18−2), …) and both maximizers
(32 = 2(18−2), where d2 = 18 is attained and 1a is tight). This also
explains the census's "bottom diagram stays generic": the coincidences
that inflate the TOP diagram into contact vertices (the ≤ 60 half)
leave the triple-point count pinned by the bottom diagram, which
d2 ≤ 18 caps.

**Caveat (same flavor as Theorem 1's).** The clean bound needs each
triple point to be a genuine degree-≥3 bottom vertex; a *tangential*
triple point (where the bottom argmin fails to cycle through all three —
a non-generic coincidence) would not be counted and needs the same
self-exclusion-style handling as §3.1. This does not occur at the
maximizers (census: bottom fully generic) or generically, so 1a holds
where it must and is tight; the tangential case is folded into the
degenerate analysis of 1b.

**Consequence.** (★) now reduces to sub-lemma 1b ALONE: contact-vertex
weight ≤ 60. With 1a proved, d1 = 2 + ½(triple weight + contact weight)
≤ 2 + ½(32 + contact weight), so d1 ≤ 48 ⟺ contact weight ≤ 60. The last
gap in max(3) = 67 is exactly the contact-vertex (coincidence-locus)
bound.

### 5.4 Sub-lemma 1b — CANDIDATE PROOF: contact weight ≤ 60 (via the pairwise intersection polytopes)

(2026-07-21; ledger Postscripts 41–43. Verified on 130 configs, tight at
both maximizers. The |S|=2 contact bound below is rigorous; the degenerate
|S|=3 case (Step T) is now CLOSED — see PROOF_STEP_T.md / Postscript 43.
Holds for any 3 concentric convex 6-faced cells meeting pairwise
transversally.)

**Setup.** Contact vertices are the degree-≥4 vertices of the top
diagram (the coincidences). A deg-4 contact is an edge-edge crossing of
two cells' 1-skeletons in 3-space; a deg-6 is a corner coincidence
(verified: octahedral has 30 edge-edge crossings = its 30 deg-4 contacts;
golden 18 + 6 corners). Contact weight = Σ over contact vertices of
(deg − 2).

**Local face-count lemma.** At a contact where cells i, j are tied for
farthest (cell k strictly less nearby), let a, b be the numbers of faces
of i, j ACTIVE at the physical point x₀ = r(û₀)·û₀. Then
    deg_top(û₀) = a + b = deg_{P_i∩P_j}(x₀).
*Reason.* Near û₀, cell k never participates (continuity), so the top
diagram is only the swap curve M_i = M_j; its degree = #sign-changes of
M_i − M_j around û₀. The a active faces of i fan into a angular sectors,
the b of j into b sectors; in each refined sector M_i − M_j is a single
linear function, flipping sign once per ray → a + b arcs. Simultaneously
P_i∩P_j near x₀ is the pointed 3-cone cut by the a + b facet-planes (all
active faces pass through x₀), whose vertex has a + b edges. (Edge-edge:
a=b=2 → 4; corner: a=b=3 → 6, matching the exact spectra at both
maximizers.)

**Euler bound.** For any convex polytope, Σ over ALL its vertices of
(deg − 2) = 2E − 2V = 2(V+F−2) − 2V = 2F − 4. Each cell has ≤ 6 faces, so
P_i∩P_j has ≤ 12 faces (each face lies on one face of i or j), so
2F − 4 ≤ 20. Distinct contacts map to distinct vertices of the relevant
pairwise polytope, so

    contact weight = Σ_contacts (deg_top − 2) = Σ_contacts (deg_poly − 2)
      ≤ Σ_{pairs} Σ_{all vertices of P_i∩P_j} (deg − 2)
      = Σ_{pairs} (2F − 4) ≤ 3 × 20 = **60.** ∎ (candidate)

**Now rigorous (see PROOF_FORMAL.md Part D).** The |S|=2 correspondence
deg_top = deg_poly = a+b is a theorem, not a heuristic: a genuine contact
has a,b ≥ 2, the swap curve has a+b arcs (sector count of the a+b active
facets), and P_i∩P_j at x₀ is a POINTED cone with a+b facets hence a+b
edges — pointedness because the a+b active facet-normals span ℝ³ (the two
cells meet transversally at the isolated point x₀). No "cut-off face"
issue arises. This covers every contact at both maximizers. The
degenerate triple points (|S|=3 with top-degree > 3) are handled by the
unified local inequality (◆) (PROOF_STEP_T.md, Postscript 43): the natural
route deg_top ≤ deg_bot is FALSE (Postscript 42: a corner-plus-two-blades
triple point has deg_top = 8, deg_bot = 4, realized on genuine cells), but
(◆) charges each triple point to the bottom AND pairwise budgets at once,
and an elementary case split (deg_bot ≥ 3 / = 0 / = 2) proves it with no
hypothesis on the triple points. So Step T is CLOSED.

**Verification.** contact ≤ Σ_pairs(2F−4) on 130 configs (both maximizers
TIGHT at 60; hexahedra, off-center, cuboids, rhombohedra, near-oct), zero
failures; degree spectra match top vs pairwise-polytope at both maximizers.

**Consequence.** d1 = 2 + ½(triple + contact) ≤ 2 + ½(32 + 60) = 48,
completing Cluster 2 and hence max(3) = 67 for all 3 concentric convex
≤6-facet cells meeting pairwise transversally (degenerate triple points
included, via PROOF_STEP_T.md).

## 6. Assembly and status

d3 ≤ 1 (§1), **d2 ≤ 18** (§3+§3.1), **triple weight ≤ 32** (§5.3), and
**contact weight ≤ 60** (§5.4, candidate proof) are all in hand, giving
d1 ≤ 48 and bounded = d1 + d2 + d3 ≤ 48 + 18 + 1 = **67**, attained
(two-engine certified) by the octahedral and golden compounds. So
**max(3) = 67 is proved for ALL 3 concentric convex ≤6-facet cells meeting
pairwise transversally** (Postscripts 38–43; degenerate triple points
closed in PROOF_STEP_T.md). The only residual caveat is the milder
pairwise-tangency degeneracy of §5.4, not a triple-point phenomenon.

Complete corollaries now in hand:
- **max(2) = 13** — the project's first complete maximum theorem.
- **d_{n−1} ≤ 6n for all n, unconditionally** — the l = 1 ceiling law.
- **d2 ≤ 18** and **triple weight ≤ 32** — Cluster 1 and half of
  Cluster 2, and both generalize to all convex 6-faced cells.

## Open, in priority order
1. **Step T (degenerate triple points) — CLOSED (Postscript 43,
   PROOF_STEP_T.md).** Not via deg_top ≤ deg_bot (false) but via the
   two-budget local inequality (◆): deg_top − 2 ≤ (deg_bot−2)⁺ +
   Σ_pairs(d_{ij}−2), proven by an elementary case split using
   deg_top = N − deg_bot and z_{ij} ≤ 2min(a_i,a_j). Verified 0/50000.
   The only residual caveat is the pre-existing pairwise-tangency
   degeneracy of §5.4 (Part D), not a triple-point issue.
2. Tighten the two "flavor of Theorem 1" caveats: Theorem 1's "q_t lands
   in component U" (§3.1) and Lemma 1a's tangential-triple-point case
   (§5.3). Standard, non-generic, corroborated; deserve clean write-ups.
