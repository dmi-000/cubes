# census_bound: feasibility report on (★) Σ_v(deg_v−2) ≤ 92

Run against CENSUS_BOUND_SPEC.md, feasibility-first mode. This is **not**
a proof of (★); it is the requested feasibility verdict with concrete
numbers, plus one negative result (approach 4, killed and confirmed by
main session mid-run — see below). Produced by `census_bound.py`, which
reuses `census_extract.py`'s validated exact machinery (`build_circles`,
`gen_candidates`, `classify_vertices`, `build_graph`, `euler_face_count`)
unchanged — those functions are generic over any field-element type
exposing `+,-,*,/,neg,eq,hash,sign(),float()`, so they run verbatim
against the exact Q(√2)/Q(√5) witnesses (loads-bearing claims) and
against a float field wrapper `FF` fed by Haar-random rotations (fast
statistical scans, explicitly permitted by the spec for speed).

## Verdict, up front

| approach | verdict | evidence |
|---|---|---|
| 1. Euler weight / active-face-triple classification | **the tractable route** | per-config realizable triples capped at exactly 16 (matches both maximizers) over 10⁴ random configs; the harder half (60 of 92) is a measure-zero contact-vertex locus invisible to random sampling — needs targeted, not blind, search |
| 2. Chamber enumeration | **infeasible as literally stated** | pilot shows chamber angular diameter ≲0.02–0.05 rad in a 6-D domain of size O(π) per axis; extrapolates to ≳10¹¹–10¹³ chambers |
| 3. Certified interval covering | **infeasible for the same reason as 2, likely worse** | not independently piloted (see reasoning below); inherits approach 2's wall density plus the extra cost of rigorous (non-heuristic) interval evaluation |
| 4. Anchor-reduction (PROOF_67 §5.1) | **DEAD — refuted, not just unproven** | exact cone test gives 0/32 anchoring triple points at BOTH maximizers, not the claimed 24; confirmed independently by brute-force real-function search (0.6–2.4% margins, not float noise). Main session has corrected PROOF_67 §5.1 and marked the route dead. |

Gates: **G1 PASS** (census_extract reproduces 67={48,18,1} at both
witnesses, unchanged). **G2 PASS** (this script's own weight computation
gives exactly 92 at both maximizers, matching census_extract's own
report). **G3 PASS** (10,000 Haar-random configs, 0 violations of
Σ(deg−2)≤92; observed max was 32, far below 92 — see the "generic
stratum" finding below for why that gap is itself informative, not a
weak test).

---

## Gates in detail

### G1 (exact, census_extract unchanged)

```
W1 octahedral (Q(√2)): total=67 by_depth={0:1, 1:48, 2:18, 3:1}
W2 golden     (Q(√5)): total=67 by_depth={0:1, 1:48, 2:18, 3:1}
GATE G1: PASS
```

### G2 (exact, this script's independent recomputation of the weight)

```
W1 octahedral: Σ(deg-2) = 92  F=48 V=62 E=108 C=1  triples=32 kinks=30  PASS
W2 golden:     Σ(deg-2) = 92  F=48 V=56 E=102 C=1  triples=32 kinks=24  PASS
```

Both exactly reproduce census_report.md's numbers via an independent
code path (this script's own `analyze_top`, not a copy-paste of
`census_tables`), which is itself a useful cross-check of
census_extract.py's correctness.

### G3 (float, 10,000 Haar-random 3-cube configurations)

```
10000 configs, 4 procs, 298s total (30 ms/config); 2/10000 skipped
  (float-precision-limited exact-tie assertion — see "float-pipeline
  notes" below; negligible, not a geometric finding)
weight Σ(deg-2): max=32  mean=27.02   >92 violations: 0
triple-point count: min=8 max=32 mean=27.02  (weight == triple count
  in EVERY sampled config: see "generic stratum" below)
occurring-elementary-triples per config: min=4 max=16 mean=13.51
distinct occurring elementary triples across all 10000 configs: 108/108
distribution of triple-point count (=weight), all multiples of 4:
  {8:3, 12:18, 16:118, 20:1046, 24:2602, 28:3529, 32:2682}
```

**G3 PASS with zero violations.** No config exceeded weight 32 — well
under 92. This is expected, not a weak test: see below for why.

---

## The central structural finding: (★)'s 92 splits into an easy 32 and a hard, measure-zero 60

Every one of the 10,000 random (Haar, hence measure-theoretically
generic) configurations had **zero contact-vertex ("kink") weight** —
every vertex of the TOP-1 diagram was a plain trivalent triple point
(deg 3, contributing exactly 1 to the weight), and the triple-point
count never exceeded 32. This is the sharpest single fact this run
produced:

- The **32-weight budget** (triple points, deg-2=1 each, ≤32 of them) is
  realized by *generic* configurations and is comfortably hit by random
  sampling — it is the "easy half" of (★), and per-config counts cluster
  tightly (mode 28, then 32; distribution is quantized in multiples of
  4, itself worth a remark: triple points appear to vanish/merge in
  blocks of 4 under generic perturbation, consistent with the compound's
  built-in symmetry constraints even for asymmetric configs).
- The **60-weight budget** (same-pair contact vertices: 30×deg4 at W1,
  18×deg4+6×deg6 at W2) requires an EXACT algebraic coincidence (a
  cube's own edge/corner exactly aligning with an inter-cube tie) — a
  measure-zero condition in the 6-D configuration space. Uniform random
  sampling, however large, will **never** produce a single such vertex;
  it is structurally invisible to G3-style scanning. This is why G3's
  observed ceiling (32) sits so far under 92: the test is sound (0
  violations, real signal) but is only ever exercising the easy half of
  (★). A random-sampling-only "verification" of (★) would be
  systematically blind to the hard half, and should not be read as
  evidence that 92 is loose — it isn't reachable by chance at all.

Practical upshot for Approach 1: **(★) should be attacked as two
separate sub-lemmas**, matching the census's own 32+60 accounting
(census_report.md, already flagged there as the correction to
C45_notes §13's discredited "46×2" projection):

  (a) triple-point weight ≤ 32 — looks tractable; see the per-config-16
      finding below, which gives a clean route to `≤32` via
      `(occurring triples per config) × (2 antipodal points each) × (1
      weight each, trivalent) ≤ 16 × 2 × 1 = 32`, matching the observed
      ceiling exactly and matching both maximizers exactly (G2).
  (b) same-pair contact-vertex weight ≤ 60 — this is where the real
      difficulty lives; it is a codimension-≥1 coincidence-locus
      classification that a feasibility pass cannot probe by random
      sampling (see "what G3-style scanning cannot do," below).

---

## Approach 1: Euler weight classification — TRACTABLE, with a concrete target number

**Central number: 16.** Over all 10,000 random configs, the count of
*realizable active-face triples* — (f0,f1,f2,s01,s12) tuples
simultaneously equi-projected + active + top, in census_extract's own
`elementary_triples` classification — never exceeded **16** in a single
configuration (min 4, mean 13.51, max 16). Both known 67-maximizers
independently hit exactly 16 (census_report.md, confirmed here via an
independent code path). Stripped of sign data, the *bare* face-triples
(f0,f1,f2) realized at each maximizer number 16 as well (16 distinct out
of the naive 27 = 3×3×3, with **no repeats** — every occurring
(f0,f1,f2) has a unique sign pattern at both witnesses; verified exactly
from census_data.json). So "16" is a robust constant across three
different ways of counting it (5-tuple-with-signs per config, bare
face-triple per config, both maximizers exactly) — this is the strongest
concrete number this run produced and the natural target for a
hand-checkable sub-lemma: **"at most 16 elementary active-face triples
are simultaneously realizable at any one configuration."**

Global vs. per-config restriction — an important distinction the task
asked to quantify: across the whole 10,000-config sample, **all 108** of
the naive 3×3×3×2×2 = 108 elementary-triple slots occurred in *some*
configuration (i.e. essentially nothing is globally forbidden — almost
any combinatorial triple can happen somewhere in configuration space).
The restriction (★) needs is entirely a **per-config** one: not "which
triples can ever occur" but "how many can occur *simultaneously*." That
reframes the classification target correctly: Approach 1 is not a
Platonic-style elimination of impossible triples (few of the 108 are
truly impossible), it is a **simultaneity bound** — closer in spirit to
a packing/incompatibility argument (e.g. an orthonormality/angle-budget
argument bounding how many of the 3 cubes' 3×3 face-pairings can be
tied-and-farthest at once) than to the naive "eliminate degenerate
vertex types" framing of C45_notes §8.

Note on the spec's cited "naive 3·3·3·2 = 54": that figure (from
CENSUS_BOUND_SPEC.md's own text) describes the swap-*circle* count per
cube pair × cross combinations, not the elementary-triple space; the
actual naive elementary-triple space, using census_extract's own
(f0,f1,f2,s01,s12) classification, is 3×3×3×2×2 = 108 (108/108 realized
somewhere; ≤16 per config). Both framings point the same direction
(strong per-instance restriction, weak global restriction); 108 is the
number this script's reused machinery actually computes and is reported
as such rather than forced to match 54.

**Feasibility verdict for 1(a) (triple weight ≤ 32):** tractable. The
per-config-≤16 fact, if provable as a clean sub-lemma (plausibly via an
orthonormality/Cauchy–Schwarz-style simultaneity argument on the 3×3
active-face assignments, in the spirit of Theorem 1's matched/unmatched
dichotomy but applied to *triples* rather than single-cube anchors),
directly gives triple weight ≤ 16×2 = 32 by the antipodal-pairing fact
census_report.md already established exactly at both maximizers.

**Feasibility verdict for 1(b) (contact weight ≤ 60):** open, and this
run could not move it — see "what G3-style scanning cannot do" below.
Not a dead end, but a genuinely different (targeted, not random) search
is needed to gather empirical data on it at all.

---

## What G3-style random scanning cannot do (and what would be needed for 1(b))

Because same-pair contact vertices require an exact coincidence, no
amount of additional random sampling will produce empirical data on
their degree spectrum beyond the two known maximizers. A short,
unsuccessful side-experiment (perturbing the octahedral witness by a
random rotation of cubes 2–3, holding cube 1 fixed) produced
inconsistent, likely-buggy output (identical kink/weight counts across
perturbation scales spanning 0.3 down to 0.0003 rad) and was abandoned
rather than reported as a finding — flagged here for honesty, not
included in the numbers above. Confirming or refuting a bound like
"contact weight ≤ 60" empirically would need either (a) a symmetry-aware
parametrized family known to force coincidences identically (C45_notes
§12's dihedral family `Rel(theta,psi)`, already implemented in
`nfamily_common.py`/`glue_search.py`, was identified but not exercised
here — Theorem F of that section proves certain edge-line coincidences
hold *identically* along that family, which is exactly the kind of
non-generic locus needed), or (b) directly solving the coincidence
equations. Both are real work beyond this feasibility pass's scope; the
recommendation is to make (b)'s classification the next targeted task,
explicitly NOT via blind random scanning.

---

## Approach 2: chamber enumeration — INFEASIBLE as stated, with a concrete extrapolation

Pilot: around several random base configurations, cube 1 is held fixed
(WLOG by symmetry) and cubes 2, 3 are perturbed by a random rotation of
fixed angular magnitude (the "box scale") and random axis; the
combinatorial signature (F, V, E, n_triple, n_kink, and the full set of
occurring elementary triples of the TOP-1 diagram) is recorded for each
probe, and distinct signatures are counted.

```
box_scale (rad)   distinct combinatorial signatures / 61 probes, per base config
0.02              2,  4,  2,  5      (4 bases, seed 42)
0.05              8,  6,  2,  13
0.15              33, 20, 11, 36
0.30              45, 30, 27, 48
0.60              51, 46, 47, 59
1.00              60, 59, 55, 61     (essentially every probe a distinct chamber)
```

(census_bound_pilot_log.json / census_bound_pilot2.log; an earlier
independent sweep at seed 7 gave the same picture — 4–19 distinct at
0.05 rad rising to 49–59 at 0.6 rad — so the density estimate is
reproducible, not a seed artifact.)

Even at the *smallest* tested scale (0.02 rad ≈ 1.1°) 2–5 probes out of
61 already land in distinct chambers, and by 0.3–1.0 rad the count
saturates near "every probe distinct" (55–61 of 61) — meaning the true
chamber angular diameter, in the full 6 real dimensions explored (two
extra cubes' rotations, cube 1 fixed), is well under 0.05 rad in typical
directions. Extrapolating this local density (chamber ~ ball of radius
~0.03–0.05 rad in the 6-D domain) against the full domain (each of the
two free cubes' rotations ranges over an SO(3) of angular extent ~π)
gives, by a crude volume-ratio estimate ((π/0.04)^6 ≈ 2·10¹²),
**chamber count on the order of 10¹¹–10¹³** for full unrestricted
enumeration — consistent with (and an extrapolation of) C45_notes §11's
independently-obtained finding that even the *much smaller* n=2 case
(3-D quaternion chart, only 4 of 12 relevant quartics) already produced
a 4.6-million-leaf CAD tree. n=3's config space is 6-D with up to 72
candidate circles (54 cross + 18 own), each a higher-degree constraint;
full chamber enumeration is not tractable on any foreseeable hardware
without a drastic symmetry/family reduction (as C45_notes §9 already
concluded: "chamber count astronomical (~10^60+ at n=6 by sign-pattern
bounds)... effective enumeration NEEDS a fixed family").

**Verdict: infeasible.** Approach 2 as literally stated (full
combinatorial-type enumeration of the unrestricted 6-D config space) is
out of reach; this matches the spec's own warning (C45_notes §11) and
this pilot adds a concrete, independently-measured density estimate
confirming it rather than just citing the n=2 precedent.

---

## Approach 3: certified interval covering — not separately piloted; expected infeasible

Not independently run (feasibility-first prioritization: approach 2's
pilot already answers the load-bearing question about wall/chamber
density, and approach 3 inherits the identical combinatorial complexity
plus the extra burden of RIGOROUS interval evaluation of the vertex/degree
structure across each box, rather than a single floating-point sample).
Given approach 2's measured chamber diameter (≲0.02 rad) against a
domain of size O(π) per axis, a certified covering would need a
comparable or larger number of boxes (interval boxes must be small
enough not to straddle a wall to get a useful ≤92 certificate cheaply;
straddling boxes need recursive subdivision, which is exactly the
CAD-style blowup C45_notes §11 already found infeasible at n=2 alone).
**Verdict: infeasible for essentially the same reason as approach 2,
likely worse in constant factor.** Not recommended as a next step ahead
of approach 1's targeted sub-lemma work.

---

## Approach 4: anchor-reduction (PROOF_67 §5.1) — DEAD, refuted

This run tested the specific empirical claim underpinning approach 4
("verified at the octahedral maximizer: ... anchoring 24 of the 48
components; the other 24 sit at triple points") directly, per the
spec's instruction to test empirically first via the cone condition
`e_i ∈ cone{e_x − e_i}`.

**Result: 0 of the 32 triple points anchor any component, at BOTH
maximizers**, not 24. This was established two independent ways:

1. **Exact.** `analyze_anchoring` in `census_bound.py`, using
   census_extract's exact Q(√2)/Q(√5) witnesses directly (no floats),
   implements the tangential-gradient + 2-D cone-membership test exactly
   as specified (`e_i ∈ cone{e_x−e_i : x≠i}`, tested via exact sign()
   comparisons on the 2-D coordinates in `make_basis(u)`). Result:
   `anchor-count histogram: {0: 32}` at both W1 and W2 — every one of
   the 64 (32×2 maximizers) triple points has n_anchors=0.
2. **Direct/float, non-linearized.** A brute-force real-function search
   (sample many directions at several radii around each triple point,
   evaluate the *actual* r_i functions, not the linearized tangent
   model) confirms: at every triple point tested, all three cubes have a
   genuine improving direction with *substantial* margin (0.6–2.4% reach
   improvement at radius 0.01–0.03 rad — far above any float-noise
   floor). Both methods agree with each other and with the corner-anchor
   count (24/24 corners at both maximizers ARE genuinely blocked, as
   §5.1's case (a) claims — only case (b), the triple-point anchoring
   claim, is wrong).

The likely true mechanism for the "other 24" (W1) / "other 24" (W2, with
a partial signal of some contact-vertex involvement) components' actual
argmax was not resolved in this run (candidate: an interior stationary
point along a swap-curve *edge*, not at any vertex — consistent with
PROOF_67 §4's own remark that some top-diagram faces have "no interior
local max ... bounded entirely by swap arcs" — but this was not
confirmed and should not be treated as established).

**This finding was relayed to and independently confirmed by the main
session mid-run** (via two independent methods: tangent-march from the
census triple points, and the same exact cone test), which has corrected
PROOF_67.md §5.1 and marked approach 4 dead. No further effort was spent
on it past that point, per the coordinator's redirection. This is
reported here as a completed, useful negative result — exactly the kind
of "kill a wrong lead cleanly" outcome a feasibility pass exists to
produce — not as a shortfall of this run.

---

## Notes on the float-pipeline machinery (for anyone reusing census_bound.py)

- `FF` (the float field wrapper) required **snapped equality/hashing**
  (round to 1e-6 before `__eq__`/`__hash__`), not raw float equality.
  census_extract's candidate deduplication relies on python
  `set()`/`dict()` keying on exact field-element equality, which holds
  bit-for-bit under Fraction/Q2/Q5 arithmetic but not under naive floats
  (different construction paths for "the same" ray produce slightly
  different float tuples). Without the snap, converting the *exact* W1
  witness's own rotations to float and running the unmodified pipeline
  inflated 32 triples / 30 kinks to 152 / 158 (spurious near-duplicate
  vertices) — a real bug, not an activity/sign issue. With the snap,
  the float pipeline exactly reproduces 92/48/32/30 (W1) and 92/48/32/24
  (W2) when fed the exact witnesses converted to float — this is the
  validation gate for trusting the float scan's other numbers.
- `EPS` (the sign-zero threshold) is calibrated to 1e-6, not the naive
  ~1e-14 float64 machine epsilon, because census_extract's candidate
  construction chains several cross-products and a division-by-smallest-
  coordinate normalization (`canon_ray`) that amplifies relative error;
  empirically residuals at the exact-tie assertion in `classify_sample`
  cluster at ~1e-9..1e-7 under this pipeline.
- 2/10,000 configs in the G3 scan hit `classify_sample`'s strict
  exact-tie assertion despite the above calibration and were skipped
  (logged, not silently dropped) — negligible rate, not a geometric
  finding.

---

## Deliverables

- `census_bound.py` — the script (exact anchor/cone test, float `FF`
  field, random-config generator, G1/G2/G3 gates, approach-1/2 stat
  collection). Reuses census_extract.py unchanged (imported, not
  copied); never edits it or any other read-only/validated file.
- `census_bound_report.md` — this file.
- `census_bound_gates_log.json`, `census_bound_gates.log` — exact G1/G2
  and exact anchor-census output.
- `census_bound_scan_log.json`, `census_bound_scan.log` — the 10,000-
  config G3 scan (float).
- `census_bound_pilot_log.json`, `census_bound_pilot.log` — the
  approach-2 chamber-density pilot sweep.

## Recommended next step

Pursue Approach 1(a) as a hand-checkable sub-lemma first (it is fully
specified by the ≤16 finding above and looks close to provable by a
simultaneity/orthonormality argument), then treat 1(b) (contact-vertex
weight ≤ 60) as its own targeted classification task using the
C45_notes §12 dihedral family (or direct coincidence-equation solving)
rather than random scanning — NOT approaches 2, 3, or 4.
