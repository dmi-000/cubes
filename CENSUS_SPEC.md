# CENSUS_SPEC — (c1) exact census data from both 67 witnesses

Task for the implementing agent (Sonnet). Background: C45_notes.md §13
(the max(3)=67 lemma tree — this task is sub-task (c1) of lemma L2.c,
plus the same extraction for the bottom diagram feeding L1). Ledger and
validated files READ-ONLY. Light compute; exact arithmetic ONLY (no
float in any decision — floats allowed for sorting/reporting).

## Objects

Config = 3 unit cubes ([−1,1]³ under rotations R_i), common center.
For direction u ∈ S²: cube i's radial reach r_i(u) = 1/max_a |n_a·u|
over its 3 unsigned face normals n_a (columns of R_i). The ACTIVE face
at u = the argmax. Everything is projective/antipodal (u ~ −u); work
with unnormalized exact direction vectors.

TOP diagram: partition of the sphere by who attains max_i r_i.
  Faces of this diagram = components of T_i = {u : r_i > max others};
  by the fibration lemma, Σ_i #components(T_i) = d1 of the compound.
BOTTOM diagram: partition by who attains min_i r_i.
  Σ_C #components(S_C = {r_C < min others}) = d2.

Swap curves r_i = r_j (active faces a on i, b on j) are GREAT CIRCLES:
|n_a·u| = |n_b·u| iff u ⊥ (n_a − n_b) or u ⊥ (n_a + n_b).

## Witnesses (both certified 67 = {48, 18, 1})

W1 octahedral, field ℚ(√2): R1 = Rx(45°), R2 = Ry(45°), R3 = Rz(45°)
   (the validated slide3_q2.py uses this triple — read-only reference
   for matrices and for the count).
W2 golden, field ℚ(√5): cubes {I, S, S²} where S is the dihedral-family
   matrix at tan ψ = φ²: S = −I/2 + (3/2)nnᵀ + (√3/2)[n]ₓ with
   n = (sin ψ, cos ψ, 0), sin ψ = φ/√3, cos ψ = 1/(φ√3). All entries
   land in ℚ(√5) (derive them yourself; use φ² = φ+1 to simplify).
   Verify S orthonormal, det 1, S³ = I exactly.

GATE G1: reproduce both counts before extracting. W2: the Python
oracle certify_six.exact_count_config accepts Q5 entries (wrap matrix
entries in cube_compound_exact.Q5; rots = objects with .m) — must give
67 = {48,18,1}. W1: reproduce 67 via slide3_q2.py (read-only) or the
oracle if ℚ(√2) wrapping is available; state which.

## Extraction (per witness, exact field arithmetic)

1. **Candidate triple points**: for each face triple (a from cube 1,
   b from 2, c from 3) and each sign pattern, u = (n_a − s₁n_b) ×
   (n_b − s₂n_c) (exact cross product; skip zero vectors). Dedupe
   projectively. Verify |n_a·u| = |n_b·u| = |n_c·u| exactly.
2. **Filters**: (ACTIVE) each of a, b, c achieves its own cube's max
   |n·u| at u (ties allowed — record them; ties = sector-boundary
   degeneracies, expected at the witnesses' corner contacts).
   Record each surviving point with its active triple, and whether it
   lies on the top diagram (the tied value is min_i max_a — i.e. the
   three r_i all equal so it is automatically on both diagrams at n=3;
   the real distinction is which LOCAL diagram arcs at it — see 4).
3. **Pair-tie vertices (kinks)**: points where a swap circle crosses a
   sector boundary of one of its two cubes (active face changes).
   Compute similarly: u = (n_a − s₁n_b) × (n_a − s₃n_a′) for a, a′ two
   faces of the SAME cube (sector boundary |n_a·u| = |n_a′·u|), and
   analogues. Needed only for the Euler cross-check.
4. **Graphs**: build both diagram graphs exactly.
   TOP-1 graph: arcs of swap circles where the tied pair is the TOP
   two (r_i = r_j ≥ r_k) and both tied faces active; vertices = the
   triple points + kinks lying on such arcs. BOTTOM graph: same with
   r_i = r_j ≤ r_k. Represent arcs combinatorially: for each great
   circle, sort all its vertices by exact angle order (use exact sign
   tests in the circle's plane basis — no floats in comparisons),
   then classify each arc between consecutive vertices by testing one
   exact interior sample point (midpoint construction in the field,
   or a rational combination) for activity + top/bottom membership.
5. **Counts and checks**:
   GATE G2 (the sharp gate — validates the whole extraction):
   Euler face count of the TOP-1 graph must equal 48 and of the
   BOTTOM graph 18, for BOTH witnesses (use F = E − V + 1 + #graph
   components per sphere; handle multiple components honestly).
   GATE G3: everything antipodally symmetric (vertex set, degrees).
6. **Report the census** (this is the deliverable for lemma (c2)):
   - number of triple points, their degree spectrum in the TOP-1
     graph, Σ_v(deg_v − 2) over triple points, and over all vertices;
   - the LIST of occurring active-face triples (a,b,c) with sign
     patterns, up to the compound's symmetry — this is the target
     list for the Platonic-elimination classification;
   - W2 merging: group coincident points; report multiplicities and
     merged degrees vs W1's (the degeneracy-robust budget (c3) needs
     exactly this comparison);
   - kink counts (should be degree-2 in their diagram).
   §13 projects "≤46 feasible triples × 2 points = 92, F ≤ 48". If
   your exact numbers disagree with that arithmetic, REPORT the
   discrepancy prominently — the data corrects the projection, not
   the other way around.

## Deliverables

census_report.md (gates, tables, degree spectra, the occurring-triples
list, W1-vs-W2 merge comparison), census_extract.py, census_data.json
(machine-readable: per witness, per vertex: exact coordinates as field
elements, active faces, degrees, diagram membership; per arc: circle,
endpoints, diagram). Do not edit the ledger or validated files.
