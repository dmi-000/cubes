# CENSUS_BOUND_SPEC — prove Σ_v(deg_v − 2) ≤ 92 (⇔ d1 ≤ 48 ⇔ max(3)=67)

Task for the implementing agent (Sonnet, proof-grade). Background:
PROOF_67.md §5 (the reduction — READ IT), census_report.md /
census_data.json (the equality data: 92 = 32 + 60 at both maximizers),
census_extract.py (validated exact spherical-diagram machinery — REUSE),
C45_notes.md §§8,11,13,15. Ledger and validated files READ-ONLY.
≤4 cores; detached. HEAVY — scope carefully and report feasibility
HONESTLY before burning large compute; a rigorous "here is why it does
/ does not reduce to a finite check of size N" is itself a deliverable.

## The target

Cluster 2 of max(3)=67 is EXACTLY (Euler on the top diagram, F = 2 +
½Σ_v(deg_v−2)) the single inequality

    Σ_v (deg_v − 2) ≤ 92   over all 3-cube configurations.     (★)

Attained with equality at both 67-maximizers (census: 32 units on 32
trivalent triple points + 60 on same-pair contact vertices — octahedral
30×deg4, golden 18×deg4 + 6×deg6). Everything else in max(3)=67 is done
(PROOF_67.md); (★) is THE remaining gap. Proving it proves max(3)=67.

## Why it is not trivial and what must be controlled

The swap curves r_i=r_j are arcs of the great circles û⊥(n_{i,a}∓n_{j,b})
— up to 3·3·3·2 = 54 great circles. Their UNRESTRICTED arrangement has
far more than 48 faces; (★) holds only because an arc is an EDGE of the
top diagram solely where its two faces are ACTIVE (each is its cube's
max-projection face) and the tied pair is the TOP two (reaches ≥ the
third cube). The entire content is that this activity+top restriction
caps the weight at 92. C45_notes §11 warns that full symbolic CAD over
the wall set is infeasible even at n=2; do NOT attempt blind CAD.

## Approaches (assess feasibility of each FIRST, in the report)

1. **Combinatorial arrangement bound.** Bound (★) by pure counting:
   (a) # triple points and their degrees — a triple point needs one
   active+top face per cube simultaneously equi-projected; classify the
   feasible active-face triples (the "Platonic elimination" of §8) and
   show ≤ N₃ of them, each contributing ≤ its degree−2; (b) the
   contact-vertex weight — active-face-change events on top swap arcs.
   The census says the honest split is 32 + 60, NOT §13's guessed
   "46 triples × 2"; the classification must target the real structure.
   Goal: a hand-checkable finite case analysis (like the five-Platonic-
   solids proof), computer-ENUMERATED but human-auditable.
2. **Symmetry-reduced exhaustive combinatorial-type enumeration.** The
   top diagram's combinatorial type is constant on chambers of the wall
   arrangement in config space (SO(3)² fixing one cube, ~6-D mod
   symmetry). If the number of realizable combinatorial types is finite
   and enumerable, compute Σ(deg−2) on each and verify ≤ 92. Feasibility
   hinges on the chamber count — ESTIMATE it before committing; if it is
   astronomically large, this route is out and say so.
3. **Certified-interval verification** (the F1 fallback, analogue of
   MAX2_SPEC Strategy A but at n=3): cover a fundamental domain of
   config space with boxes and certify Σ(deg−2) ≤ 92 on each via
   interval evaluation of the top-diagram vertex set. Rigorous if it
   completes; the risk is the 6-D covering not terminating in feasible
   time. Report the box-count growth on a pilot sub-domain before scaling.
4. **Anchor-reduction route — DEAD (do not attempt).** PROOF_67.md §5.1
   posited d1 = 24 (corners) + (anchoring triple points). This was
   REFUTED 2026-07-20 (this scan + main-session verification): 0 triple
   points anchor at either maximizer; the 24 non-corner components anchor
   at kink/edge-type points, not triple points, with no clean per-cube
   count (24 corners + 30 kinks = 54 > 48, overcounting). The dual of
   Theorem 1 does not close the top diagram. See PROOF_67 §5.1 (corrected)
   for why. Focus the feasibility verdict on approaches 1 and 2.

## Gates

G1: census_extract machinery reproduces Σ(deg−2)=92 at both maximizers
    and =32/32 on the bottoms (validated tooling).
G2: whatever bound/enumeration you build, it returns EXACTLY 92 (not
    just ≤92) at both maximizers — the equality cases must be tight, or
    the bound is not calibrated to reality.
G3: it returns ≤92 on a batch of ~10⁴ random configs (necessary
    condition; a single >92 would refute (★) and is itself a headline —
    re-verify exactly and FLAG).

## Deliverables

census_bound_report.md — **FIRST a feasibility verdict** on approaches
1–4 (which is tractable, with concrete size estimates: how many
realizable active-face triples, how many top-diagram chambers on a pilot
sub-domain, and — for approach 4 — the empirical anchoring-triple-point
count distribution and whether "≤ 24 anchor" holds). This feasibility
pass is the PRIMARY deliverable of this run; do NOT burn large compute
on a full classification/covering before the estimates say it will
terminate. THEN whatever partial or full result the estimates justify. A
rigorous reduction of (★) to a finite check of stated size, even
unexecuted, is real progress. If (★) is actually proved, state it as
"max(3) = 67 is proved" with the full certificate. census_bound.py and
any enumeration/empirical logs. Never edit the ledger or validated files;
main session records a theorem only after independent re-verification.

## Gate note

Reuse census_extract.py's validated exact spherical-diagram machinery
for anything load-bearing (triple-point extraction, degree computation,
the cone/anchoring test). Empirical scans (approach 4's anchoring
statistics, approach 2's chamber counts) may use floats for SPEED, but
any claimed bound or equality-at-the-maximizer must be exact.
