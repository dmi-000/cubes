# RESONANCE4_SPEC — solve the coincidence-alignment conditions for non-uniform 4-cube family resonances, algebraically

Task for the implementing agent (Sonnet). Background: six_cube_search_results.md
Postscripts 25 (+addenda) and 26 (+addendum), C45_notes.md §12 (the four
theorems — Rel gauge, mirror, periodicity, coincidence identity),
nfamily_report.md and nfamily_common.py (exact machinery — REUSE it),
q3_count.py / q6_count.py (field-engine clone recipe). All ledger/validated
files READ-ONLY. ≤4 cores; detached long runs; write interim findings into
the report as you go.

## Why

At n=3 the family's region-count spikes (+12 over the plateau) sit at
resonances — parameter points where CROSS-class edge coincidences align on
top of Theorem F's identical same-class ones: the octahedral 67 at
ψ=arcsin(1/√3) (y-z class extras), the golden 67 at ψ=arctan(φ²) (x-z
class). At n=4 the rational family plateau is 175 and the record is 183 —
a gap of 8, SMALLER than the n=3 resonance boost. The uniform n=4 chain
(90° spacing) is degenerate (Postscript 26: collapses to 93), so any n=4
resonance must be non-uniform. Nobody has looked. Goal: find ALL n=4 family
resonances algebraically and exactly count the candidates. Anything ≥183
is a headline; anything >175 already interesting.

## Setup (use the Rel gauge)

Config: cubes k=1..4 = Rel(θ_k, ψ)·[−1,1]³, θ_1=0, Rel = rotation by θ
about n(ψ)=(sinψ, cosψ, 0). Pair structure depends only on (Δ=θ_j−θ_k, ψ).
Fundamental domain: ψ ∈ (0°, 45°] (Theorems M+P); dedupe θ-tuples by
congruence invariants at the end rather than trying to quotient a priori.

## Plan

1. **Pair-level cross-class conditions, exactly.** For each cross-class
   type (x-y, y-z, x-z) derive the edge-line coplanarity polynomial
   g_type(Δ, ψ) — a polynomial in (cosΔ, sinΔ, cosψ, sinψ) — using the
   Rel closed form. Verify symbolically (sympy or wolframscript; the
   algebraic_*.wl files show the Wolfram pattern) that within each type
   the several label-pairs' conditions agree up to sign (the n=3 evidence:
   all four y-z extras share ONE curve). GATE R1: the n=3 known
   resonances must fall out — substituting Δ=120° must yield
   ψ=arcsin(1/√3) as a root of the y-z condition and ψ=arctan(φ²) for
   x-z (exactly, not numerically).
2. **Resonance systems at n=4.** Six pairs, each optionally placed on one
   of the three cross-class curves: enumerate condition systems with
   k = 2, 3, 4 conditions (k=1 gives 3-parameter families — record the
   curves but they're not isolated resonances; k up to 4 = DOF count).
   Solve each system EXACTLY: rationalize with c²+s²=1 side relations
   (variables cψ,sψ,cθ2,sθ2,cθ3,sθ3,cθ4,sθ4), Gröbner bases via
   wolframscript (preferred; see algebraic_groebner*.wl) or sympy
   resultants. Collect all REAL solutions in the fundamental domain,
   dedupe by pairwise-invariant fingerprints.
3. **Also sweep the corner-contact resonance type**: conditions |t|=1
   (vertex events, the ψ=45°/tetrahedral-angle mechanism at n=3 — note
   that n=3 resonance was count-NEGATIVE, 49<55; still map them).
   Secondary priority — do after step 2 results are in.
4. **Exact counts of every candidate.** Field ladder: rational →
   C++ engine; single quadratic ℚ(√d) → clone engine (recipe = the six
   literal replacements that produced q3_count.py/q6_count.py from
   slide3_q2.py — diff them to see; pick d from the solution's field);
   degree-4 towers ℚ(√a,√b) → qtower.py pattern (D_LIST swap).
   Higher-degree fields: do NOT approximate — report the minimal
   polynomial and mark the count open (or implement certified-interval
   sign resolution only if straightforward). GATE R2: before counting any
   new candidate, reproduce 67 for the n=3 octahedral point through your
   ladder (ℚ(√2) — slide3_q2.py is validated and read-only, use it as
   the reference for a fresh clone's output).
5. **Verdict**: table of all n=4 resonances (parameters as exact
   algebraic numbers + minimal polynomials, field, count, depth profile),
   comparison vs 175 (family plateau), 183 (record), 195 (cap-sum).
   Anything ≥183: verify with a second engine (certify_six oracle works
   for any entries expressible in its field; otherwise two independent
   clone engines) and FLAG AT TOP — record protocol: the main session
   records, never edit the ledger.

## Deliverables

/Users/dmi/carroll/resonance4_report.md, resonance4_solve.py (or .wl),
resonance4_results.jsonl (candidates + counts). Honest coverage: which
condition systems were solved, which timed out, degree/field of every
solution.
