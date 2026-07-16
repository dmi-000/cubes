# NFAMILY_SPEC — does the dihedral/big family help at n > 3?

Task for the implementing agent (Sonnet). Self-contained. Background:
six_cube_search_results.md Postscript 25 + addenda 1–4 (READ-ONLY — never
edit it or any validated file; write results to new files). Constructions
and working code: dihedral_scratch/bigfamily.py (the
family), q3_count.py + q6_count.py (exact engines,
read-only reference), records in README.md / exact_search_results.jsonl
(read-only ground truth). ≤4 cores; run long jobs detached; don't park on
monitors.

## The family, generalized to n cubes

ŝ = (1,1,1)/√3, u(θ) = cosθ·(1,−1,0)/√2 + sinθ·(1,1,−2)/√6, w = ŝ×u.
Cube k = image of [−1,1]³ under M_k = cubeM(θ_k, ψ) with columns
[cosψ·w + sinψ·ŝ | −sinψ·w + cosψ·ŝ | u] — i.e. each cube has a face-axis
u(θ_k) perpendicular to the common axis ŝ, phases θ_k free, tilt ψ COMMON
to all cubes. Every cube pair then has exact edge-line coincidences; pair
structure depends only on (θ_k−θ_l, ψ).

**Key arithmetic fact (verify as gate G0)**: the relative rotations
M_1⁻¹M_k are RATIONAL matrices whenever ψ and all phase differences are
Pythagorean angles (sin, cos rational). Rational rotation matrices have
rational projective quaternions, hence integer quaternions after clearing
denominators — so these configs are countable by the FAST C++ engine
(./cube_regions_n --n K --quats '...', integer quats only) and verifiable
by the Python oracle (certify_six.exact_count_config, any n). Chains
θ_k = k·a with a Pythagorean give all differences Pythagorean
automatically (angle addition keeps sin/cos rational).

## Questions to answer

Q1. How high do region counts go on the family at n = 4, 5, 6? Compare
    against the records (183 / 393 / 723) and the cap-sum bounds
    (1+(n−1)(16n²−17n+6)/3 = 195 / 429 / 801). Report the best members
    with quats + depth profiles.
Q2. Do the n=3 structural facts persist: deep layers stable along the
    family (at n=3, d3=1 and d2=18 across the whole middle band — all
    variation in d1)? What are the analogous stable layers at n=4,5,6?
Q3. Do the RECORDS already contain family structure? For each record
    config (n=3 quats 1,0,0,0;... — get them from README.md; n=4 183;
    n=5 393; n=6 723), count exact edge-edge crossings between every cube
    pair (exact rational arithmetic on the integer quats — a pair in
    "family position" carries ≥4 exact crossings; generic pairs carry 0).
    Also test directly: for each record pair, does there exist a common
    axis s with a face-axis of each cube ⊥ s and equal tilts? (Equivalent
    check: exact crossings ≥ 4 is strong evidence; the axis test is the
    confirmation.) Report the "family-likeness" fingerprint of each
    record.
Q4. Chain paths: at n=4,5,6 do chain configs θ = (0, a, 2a, ...) with a
    near the tetrahedral resonance / near 360/n show count spikes
    relative to neighbors (the n=3 family spikes +12 at the 67s but −6
    at 45° — which sign dominates at higher n)?

## Gates (must pass before sweep results count)

G0 (arithmetic): build the rational relative matrices for a chain triple
   (a = 36.87° = asin(3/5), ψ = 53.13° = asin(4/5)), convert to integer
   quaternions, verify quat→matrix round-trip is exact (fractions module,
   no floats in the check).
G1 (two engines agree): count that n=3 chain config with BOTH the C++
   engine and certify_six.exact_count_config — totals and depth profiles
   must match exactly. Repeat for one n=4 family config.
G2 (record reproduction): the C++ binary must reproduce 723 from the
   ledger quats (4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2 →
   723 = {210,216,164,96,36,1}) before any sweep negatives are trusted.

## Sweep design (after gates)

- ψ menu: Pythagorean angles covering (0°, 90°) at roughly 2–5° spacing
  (the (p,q,r) list in q3_count.py's driver is a ready-made menu).
- Phases: (a) chains θ_k = k·a with a from the same menu scaled to
  useful ranges (~360/n ± 40°); (b) a few hundred random Pythagorean
  phase tuples per n; (c) neighborhoods of anything that scores high.
- Budget: C++ engine is ~0.05–0.5 s/config; 10k–50k configs over ≤4
  cores is fine. Write every result as JSONL
  (n, psi, thetas, quats, total, by_depth) to nfamily_results.jsonl.
- Verify every claimed best-of-n with the Python oracle (two engines)
  before reporting it.

## Deliverables

- nfamily_report.md — answers to Q1–Q4 with numbers,
  gate results, best configs (quats), and an honest statement of sweep
  coverage.
- nfamily_sweep.py (+ helpers), nfamily_results.jsonl.
- Do NOT edit six_cube_search_results.md; the main session merges
  findings.
