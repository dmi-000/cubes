# Plan: multi-constraint (stacked-wall) search with ℚ(√a,√b,…) verification

For a Sonnet implementation agent. Read first: six_cube_search_results.md
Postscripts 4–5 and 7 (with update), QFIELD_SPEC.md (single-field
program; this spec supersedes its priorities), golden_six.py +
golden_search.jsonl (the ℚ(√5) pilot that found 681), certify_six.py,
cube_compound_exact.py (Q5). PRIORITY: this outranks the n>6 program.

## 0. Premise (why multi-constraint)

The 681 record = golden five (one stack of exact icosahedral incidences,
ℚ(√5)) + a sixth cube whose hill-climb converges to a SECOND exact
incidence: quats (2,1,1,1) → (7,4,4,4) → (26,15,15,15) have w/x → √3,
i.e. 90° about the body diagonal (1,1,1). Every random config on the
single wall already beat the 360k-seed rational record (635 → 643..681).
Hypothesis: maxima live on high-codimension strata satisfying SEVERAL
exact constraints at once. A search can favor such configurations by
three mechanisms, in increasing subtlety:

  A. constraint-first construction — impose walls exactly by building
     them in their field, search only the residual free parameters
     (this is what golden5+1 did; it works);
  B. snap-and-verify — detect, along a climbing trajectory, integer
     quat components converging to an algebraic relation; construct
     the exact limit point; verify its count in the tower field;
  C. wall composition — enumerate the known wall vocabulary and impose
     combinations, verifying in the compositum ℚ(√a,√b,…).

The tower engine is a VERIFIER, not a search engine: bulk search stays
on rational-side approximants (fast, existing engines); exact tower
counting is reserved for the handful of limit points that matter.

## 1. Tower arithmetic (the ℚ(√n,…) verification layer)

Write `qtower.py`: recursive quadratic extensions.

- Element of K(√d): pair (p, q) with p, q ∈ K, meaning p + q·√d; base
  case K = ℚ uses Fraction. Ops are the obvious ones (mul uses ·d).
- EXACT SIGN, recursively: sign(p + q√d) = sign(p) if q = 0; sign(q)
  if p = 0; if sign(p) = sign(q), that sign; otherwise
  sign(p) · sign(p² − d·q²), where p² − d·q² ∈ K and its sign recurses.
  INVARIANT: this requires √d ∉ K (else p²−d·q² can vanish for x ≠ 0).
  Assert the tower's d-list is multiplicatively independent squarefree
  ints (no product of a sublist is a perfect square).
- Hash/eq via canonical flattened coordinate tuple; __float__ for
  diagnostics only, never in predicates.
- Depth-2 tower ℚ(√3,√5) is the immediate need; write it generically
  (list of d's) but only gate and use depth ≤ 2 for now. Expect
  slowness: coordinates 4×, sign recursion squares magnitudes. Measure
  cost early; a config eval may take minutes — acceptable for
  verification counts, unacceptable for search.

Counting core: reuse the field-parameterized core from golden_six.py /
QFIELD work (one counting core, constructor injected). Do not modify
the validated files (certify_six.py, cube_compound_exact.py, mt_sim.py,
exact_search.py); exact_search_results.jsonl is read-only.

## 2. Gates (hard, before any verification claims)

- W-G1 (collapse to Q5): tower ℚ(√3,√5) with all √3-parts zero must
  reproduce the golden pilot: five-compound 351 (and 681 for the
  (2,1,1,1) config) with identical depth histograms.
- W-G2 (collapse to ℚ): all-rational configs through the tower path
  reproduce a known seed exactly (seed 40 = 575, by_depth in the
  pilot's gate log).
- W-G3 (pure √3): pair of cubes at exactly 30° about z = 9 bounded
  regions, agreeing with the rational engine on a Pythagorean-angle
  pair about z (same wall family, so counts must match at 9).
- W-G4 (approach consistency): rational convergent (97,56,56,56) —
  the next w/x → √3 convergent — through the EXISTING Q5 pilot engine;
  confirm it sits on the 681 plateau. This pins the off-wall value the
  exact wall point will be compared against.

## 3. First verification target: the √3×√5 point itself

Construct EXACTLY: golden five + sixth cube R = rotation by 90° about
(1,1,1)/√3. Rodrigues gives R = uuᵀ + [u]× with u = (1,1,1)/√3:
entries 1/3 ± 1/√3 = 1/3 ± √3/3 ∈ ℚ(√3). Columns are exact unit
vectors; assert orthonormality in the tower.

- Count it exactly. Compare to the plateau value 681. Either outcome
  is the headline: a jump above 681 (new incidences at the wall create
  regions, as pair 4 → 13) or a drop (merging, T2-style). Do not
  presume the direction.
- DIAGNOSE the incidence: as the convergents approach the wall, which
  near-coincidences tighten? Compare arrangement combinatorics (vertex
  triples that nearly coincide, plane pairs nearly concurrent with a
  third) between (26,15,15,15) and (97,56,56,56) at the same
  tolerance-free exact level: which facet/vertex keys change. State in
  plain geometry WHAT relation the sixth cube at 90°-about-(1,1,1)
  has to the golden five (e.g. face-plane parallelisms, edge
  alignments to icosahedral 2-fold axes). The diagnosis is what
  generalizes; the single count does not.

## 4. Multi-constraint search program (mechanisms A/B/C)

Log every eval (family, construction, params, total, by_depth) to
multiwall_search.jsonl; matched rational/in-family controls throughout
(the delta against a control is the measurement).

- M1 (mechanism A, cheap, do first): within-ℚ(√5) stacked walls — the
  sixth cube sharing an exact incidence with the golden five WITHOUT
  leaving the pilot field: (a) sixth sharing a face PLANE with a
  golden cube (coincident-plane wall; parameterize in-plane), (b)
  sixth rotated from a golden cube about one of ITS OWN face normals /
  body diagonals by rational-matrix angles (90° about face axis, 120°
  about diagonal are cube symmetries — skip; 60° about a golden
  cube's body diagonal is the pair-13 relation: impose it against
  each golden cube). These need only the EXISTING Q5 engine (~20-30
  s/eval): search their free parameters by the pilot's hill-climb.
- M2 (mechanism B): snap-and-verify automation. Along every climb
  that plateaus, for each quat component pair, run continued fractions
  on the trajectory of ratios; a stabilizing CF prefix with a
  periodic tail ⟹ quadratic surd candidate (detect √2, √3, √5, φ,
  and small a+b√d). Construct the snapped exact config, verify in the
  right field/tower. Also re-mine the EXISTING logs (hillclimb_log,
  golden_search.jsonl top plateau) for missed convergences — e.g.
  check whether OTHER components of the 681 plateau quats also drift
  toward surds.
- M3 (mechanism C): compose across fields — sixth at exactly 45°
  about a coordinate axis (ℚ(√2)) over the golden five ⟹ ℚ(√2,√5);
  90° about the OTHER body diagonals (±1,±1,1) ⟹ ℚ(√3,√5) siblings
  (symmetry may make them equivalent — check with the icosahedral
  group, don't recount blindly). Budget: a few tower verifications
  only, chosen by M1/M2 evidence.
- M4 (control): a purely-rational double wall (two 60°-diagonal pair
  relations among 6 otherwise-free cubes) climbed with the C++ engine
  ./cube_regions --quats (fast) — does stacking rational-reachable
  walls also beat 635, or is the golden stack special?

## 5. Priorities & practicalities

Order: gates → §3 (the √3×√5 point + diagnosis) → M1 → M2 → M4 → M3.
Compute etiquette: n>6 agent is capped at 4 workers; you may use up to
4 cores for M1/M4; tower verifications are single-core. If Python
tower evals exceed ~10 min/config, verify only §3 and the single best
M2 snap, and say so.

Deliverables: qtower.py, gate log, the §3 exact count + incidence
diagnosis, multiwall_search.jsonl, and multiwall_report.md (do NOT
edit six_cube_search_results.md — the main session merges; Postscripts
6/7 are taken). Honest negatives welcome: "stacking walls beyond the
golden five adds nothing" would itself be a finding.
