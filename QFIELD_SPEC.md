# Spec: extend the exact 6-cube search to ℚ(√d) rotations

PRIORITY: this program outranks the n>6 campaigns for compute and agent
attention (user directive 2026-07-10). Hand to an implementation agent
after the current golden-wall agent finishes (it owns golden_six.py /
golden_search.jsonl / golden_wall_report.md until then). Read first:
six_cube_search_results.md Postscripts 4-5 and 7, golden_wall_report.md
(the ℚ(√5) pilot), cube_compound_exact.py (Q5), certify_six.py.

## 1. Why fields, and which (get this right — it is easy to overclaim)

The count is constant on finitely many ℚ-semialgebraic strata, so the
max is attained at real-algebraic configs; the needed field depends on
the winning stratum. Field taxonomy of known wall families:

- ℚ (rational — already searched, 200k configs): all coincident-plane
  walls; octahedral relations; the pair-13 wall (60° about a shared
  body diagonal is a RATIONAL matrix); the pair-9 wall as a FAMILY
  (two cubes sharing a face axis give 9 bounded regions at EVERY
  generic angle, and Pythagorean angles are rational — the family is
  rational-reachable; only its symmetric 45° point is not).
- ℚ(√2): exact 45° relations about rational axes (the maximally
  symmetric point of the shared-axis pair family; 45°-related triples
  mixing axes). cos/sin 45° = √2/2.
- ℚ(√3): exact 30°/60° relations about rational axes; three cubes
  equally spaced about one axis ({0°,30°,60°} — spacing 90°/3).
- ℚ(√5): the icosahedral group lives here — the golden five-compound
  and every sub-wall of it. NOT single-axis 36° turns (sin 36° is
  degree 4 over ℚ); it is the full icosahedral matrices that are
  ℚ(√5). Pilot searched by the golden agent.
- Degree ≥ 4: k ≥ 4 cubes equally spaced about one axis (cos(90°/k),
  k=4 → ℚ(√(2+√2)), k=5 → cos 18°); towers ℚ(√2,√3) etc. for mixed
  relations. Mostly documented-only — EXCEPT the tower ℚ(√3,√5),
  which the golden pilot made CONCRETELY NECESSARY (see Postscript 7
  update): the 681-record climb converges to the sixth cube at exactly
  90° about (1,1,1) (a ℚ(√3) incidence) on top of the ℚ(√5) golden
  five. Implementing degree-4 tower arithmetic (basis 1,√3,√5,√15;
  exact sign via two nested quadratic sign tests or interval
  refinement with a separation bound) to count the actual wall point
  is IN SCOPE and high priority. Universal fallback for anything
  worse: interval-filtered exact sign on minimal polynomials (the CN
  design anticipates it).

The scientific question, sharpened by the census work (Postscript 5):
walls MERGE deep cells (T2 direction) but can ADD shallow ones (six6:
d1=120 > record 118). Can any exact-incidence wall net-win the total?
√5 is the strongest candidate (only known wall that leads its n: 351 vs
~317 generic at n=5); √2/√3 walls are the cheap next tests.

## 2. Engine: field-generic Python counter

`certify_six.exact_count_config` already computes over CN-wrapped Q5;
Q5 appears explicitly only in a few constructors (Q5(4), Q5(Fr(..)),
plane_key reading x.a/x.b) — see how golden_six.py shimmed rotations.

- Write `qfield.py`: class Qd — pair of Fractions (a + b·√d), d a
  squarefree positive int fixed per instance/class. Copy Q5's API
  exactly (add/sub/neg/mul/rmul/truediv/sign/eq/hash/float/repr);
  the ONLY d-dependence is the ·d in multiplication and in sign
  (compare a² vs d·b² with the sign cases). Q5 must remain untouched
  and Qd(…, d=5) must agree with it (gate below).
- Write `count_qd.py`: a field-parameterized clone of
  exact_count_config (constructor injected; do not edit certify_six.py)
  OR reuse golden_six.py's approach if it already parameterized — read
  it first and reuse rather than re-derive; keep ONE counting core.
- Rotation inputs: 3×3 matrices with Qd entries, columns exact unit
  vectors. Build them via Rodrigues about exact rational unit axes
  (Pythagorean quadruples) with (cosθ, sinθ) ∈ Qd² — e.g. (√2/2, √2/2)
  for 45°, (1/2, √3/2) for 60°, (√3/2, 1/2) for 30° — composed with
  rational rotations from integer quaternions (rot_from_quat). Assert
  orthonormality exactly after every composition.

## 3. Validation gates (hard, before any search)

- GQ1 (field regression): Qd with d=5 reproduces Q5 golden results:
  five-compound = 351, sub-compounds 1/13/67/177.
- GQ2 (rational embedding): 6 rational cubes through the Qd path (b=0)
  reproduce a known seed's total AND depth histogram (seed 0 or 2228).
- GQ3 (√2 known value): pair at exact 45° about z = 9 bounded regions,
  equal to the rational engine's count for a Pythagorean-angle pair
  about z (compute both; they must agree at 9 — same wall family).
- GQ4 (√3): pair at exact 60° about z = 9 likewise.
- GQ5 (coincidence): any exact-duplicate-cube config must return the
  count without the duplicate (exercises owners_of; do not weaken the
  coincident-plane invariant).
If a gate fails, stop and report; never search on an ungated engine.

## 4. Search program (log every eval: field, construction, params,
total, by_depth, per-family jsonl files qfield_<tag>.jsonl)

Measure per-eval time first; Python is ~5-30 s/config — budget ~10²-10³
evals per family, hill-climb the best (moves: ±1/±2 on one integer
quat component of the FREE cubes, re-gcd, |c| ≤ 512).

- F1 (√3, the sharpest cheap test): three cubes at exactly {0°,30°,60°}
  about z + three free rational cubes, vs the SAME three free cubes
  with the axis-triple at nearby rational angles. Does exact spacing
  create concurrences that change counts, and in which direction?
- F2 (√2): pair at exact 45° about a face axis + four free rational
  cubes, vs nearby-rational-angle controls (this extends the pair-9
  wall into the 6-cube total question).
- F3 (√5, continue the pilot): whatever golden_wall_report.md leaves
  open — likely golden4 + TWO free rational cubes (the four-cube golden
  sub-wall at 177 leaves the 5th cube free too; 8 free integer quat
  components) if golden5+1 disappoints.
- F4 (controls): every wall family gets a matched rational control at
  the same free-cube parameters; the DELTA is the measurement. Track
  d1/d2 vs records 118/214 and d3/d4/d5 vs 164/102/36 separately.

## 5. Phase 2 (only if any quadratic wall shows a net total gain)

C++ ℤ[√d]: predicate signs need a² vs d·b² comparisons — that SQUARES
bit-lengths relative to the rational engine (current worst predicates
~2^85 → squared ≈ 2^170 exceeds int128). A C++ Qd engine needs a
256-bit exact tier (or big-int fallback) — do the budget analysis
before writing code; do not port blindly. Binary name cube_regions_q;
never overwrite ./cube_regions or ./cube_regions_n.

## 6. Deliverables

qfield.py, count_qd.py (or extended golden_six.py core), gate log,
qfield_*.jsonl, and a report in qfield_report.md (do NOT edit
six_cube_search_results.md — the main session merges; Postscripts 6
and 7 are taken). Report the F1/F2 deltas even if zero — a clean
null ("exact quadratic incidences never change the count vs in-family
rational angles") would itself justify closing the quadratic program
and is a publishable-quality negative. Honest negatives welcome.
