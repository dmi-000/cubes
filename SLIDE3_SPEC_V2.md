# SLIDE3 correction (V2): the RIGHT continuous 3-cube family

Supersedes SLIDE3_SPEC.md section 0. The V1 agent proved a real but
NEGATIVE result about the WRONG family; the user has identified the
correct one. Read slide3_report.md section 0 (V1) first, then this.
Records to beat unchanged: overall 681, rational 655; n=3 wall value 67.
All V1 infrastructure is reusable: slide3_q2.py (Q(√2) exact counter),
qtower.py (Q(√3,√5)), cube_compound_exact.Q5, golden_six.golden_five(),
the C++ engine `./cube_regions_n --n 3`. Do NOT edit validated files or
six_cube_search_results.md; write slide3_report.md (append a V2 section)
and slide3_search.jsonl.

## What V1 got wrong

V1 tested C(θ) = {Rx(θ), Ry(θ), Rz(θ)} — each cube spun about its OWN
coordinate axis. That family (a) is a flat plateau at 55 that jumps to
67 only at the isolated θ=45° octahedral point, and (b) provably never
reaches a golden triple. BOTH pathologies come from the same mistake:
spinning about the coordinate axes imposes an extra octahedral S3
symmetry that pins all three pairwise traces to cos²θ+2cosθ. That is
NOT the family the user means.

TWO corrections are needed:

1. **The congruence test in V1 is invalid for cubes.** V1 compared raw
   pairwise relative-rotation traces tr(Mi Mjᵀ) and concluded "no
   golden 3-subset has three equal traces." But a cube has 24-fold
   octahedral self-symmetry, so each orientation Mi is only defined up
   to right-multiplication by O (24 elts); the meaningful invariant is
   the DOUBLE-COSET O·(Mi Mjᵀ)·O, i.e. the trace MINIMIZED (or the
   full multiset) over the 24×24 symmetry pairs — equivalently the
   minimal rotation angle bringing cube j onto cube i. Redo every
   congruence/matching check this way. Prediction to verify: the golden
   3-subset that is a single 3-CYCLE orbit under the (1,1,1) three-fold
   rotation DOES have three equal symmetry-reduced relative rotations
   (all = 120° about (1,1,1), trace 0) — V1's "artifact" traces come
   from golden_six storing non-orbit representatives.

2. **The correct family = a common-3-fold-axis orbit, seed rotating
   about the RIGHT axis** (the user: "the 3 cubes all rotate together,
   and the point where their edges intersect slides between the middle
   and the corner").

## The correct construction (build and verify exactly)

Fix the common 3-fold axis n = (1,1,1)/√3 and C = rotation by 120°
about n (rational matrix; = the x→y→z cyclic permutation). A 3-fold-
symmetric triple is the C-orbit of a single seed cube S:
    T(S) = { S, C·S, C²·S }.
The V1 family is the special case S = Rx(θ) (bad seed path). The user's
family is the C-orbit of a seed that rotates about a DIFFERENT axis so
the triple slides continuously between the two named endpoints:

- **Octahedral endpoint** S_oct: the seed whose C-orbit is the standard
  3-cube compound. Its exact orientation lives in Q(√2) (45° content);
  recover it from V1's exact octahedral construction (slide3_q2.py
  already builds the θ=45° compound at count 67) by identifying which
  single cube, C-orbited, reproduces that compound. Edge crossings at
  MIDPOINTS ("the middle").
- **Dodecahedral endpoint** S_dod: the seed whose C-orbit is the golden
  3-cycle subset. Take golden_five() (Q(√5)); find the 3-fold rotation
  about n inside the icosahedral group that 3-cycles exactly three of
  the five cubes (A5 on 5 points: an order-3 element fixes 2, cycles 3
  — that cycled triple is S_dod's orbit). Edge crossings at the
  GOLDEN-RATIO point ("the corner"). Confirm its exact count is 67.

**The slide.** Let Δ = S_dod · S_octᵀ (a single rotation; its axis â
and angle δ are exact in the compositum Q(√2,√5) — use qtower.py, and
if √2 and √5 must coexist extend it to depth-2 basis {1,√2,√5,√10}).
The one-parameter family is
    S(t) = R_â(t·δ) · S_oct ,   T(t) = { S(t), C·S(t), C²·S(t) },
t ∈ [0,1], with T(0)=octahedral, T(1)=dodecahedral. This keeps 3-fold
symmetry for all t (C-orbit by construction) and is the literal "rotate
together while the crossing slides middle→corner."

VALIDATION (the geometric check the user gave — do it, it's cheap and
decisive): for a representative interior t, compute the exact
intersection point of a chosen edge of cube S(t) with a face-plane of
cube C·S(t); confirm its position along that edge moves monotonically
from the midpoint (t=0) to the golden-section point (t=1). If it does,
the family is right; if not, the seed axis â is misidentified — say so.

COUNT PROFILE along the slide: rational t are unavailable (Δ is
irrational), so sample S(t) at exact algebraic t-values you can build
(e.g. bisections/rational-angle steps of R_â in the tower) and count
with the tower engine; also bracket with nearby RATIONAL seeds fed to
the fast C++ engine. Report total + histogram vs 55/67; is it a plateau,
monotone, or does it peak in the interior?

## Then: the overlay search (the actual objective — unchanged from V1)

Two such triples: X(t₁, t₂, R) = T(t₁) ∪ R·T(t₂), R ∈ SO(3). Search
t₁, t₂, and the relative rotation R (integer-quat grid + climb) for the
maximum 6-cube region count, beating 655 (rational) / 681 (overall).
Constraint-first is the proven winner (Postscripts 7–8): preferentially
place R so the two triples share alignment relations — a common 3-fold
axis (built 681 at n=6), a 60° body-diagonal pair relation (built 655),
or so that an edge-crossing of triple 1 meets one of triple 2. Gates
S1/S2 from V1 still apply (coincident triples reproduce the single-
triple count; one C++-vs-oracle cross-check). Exact-wall R values that
need √2/√3/√5 get tower verification; bulk stays rational for speed.

## Deliverables & handover

Append a "## V2" section to slide3_report.md: the symmetry-reduced
congruence result (does the golden 3-cycle subset now match?), the
exact S_oct/S_dod seeds, the edge-crossing slide validation, the count
profile T(t), and the overlay-search landscape (best config + quats,
promising (t₁,t₂,R) regions with active constraints and the field each
needs, dead regions, and the first move for a follow-on agent). Chart
the space well enough that a fresh Sonnet agent can resume from the
report + slide3_search.jsonl alone. Honest negatives welcome.
