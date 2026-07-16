# GLUE_SPEC — two-clique gluing search (does gluing family cliques beat 723?)

Task for the implementing agent (Sonnet). Background: Postscript 26 in
six_cube_search_results.md (READ-ONLY) + nfamily_report.md + the exact
machinery in nfamily_common.py (reuse it; read-only reference engines
q3_count.py, certify_six.py, C++ binary ./cube_regions_n — never edit
validated files). ≤4 cores; run sweeps detached; don't park on monitors;
write interim results into the report as you go.

## Finding that motivates this

The records are built from family-position pairs: 183 has 6/6 pairs, 393
has 10/10, 723 has 12/15 (a family 5-clique = the embedded 393 + one cube
family-linked to only two clique members). But the best SINGLE-AXIS family
members reach only 175/335/615. Hypothesis: records live in the space of
GLUINGS of family cliques on different axes; searching that structured
space may find configs ≥ the records.

## Q0 first — is 393 (or 183) itself single-axis? (this could overturn Postscript 26's Q1)

"All pairs in family position" used an axis-AGNOSTIC per-pair test. Two
different questions: (a) each pair has SOME common axis; (b) all pairs
share ONE common axis (single-axis family member). For 183 and 393
(ledger quats: n=4 `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4`; n=5
`4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1`): compute each pair's
family axis exactly (from the relative rotation's Rodrigues axis after
the 24-way relabeling that passes the R[0][1]==R[1][0] test — the axis is
the rotation axis of the relabeled relative rotation; it has zero
component along the local third coordinate, i.e. lies in the (sinψ,cosψ,0)
form) and check whether one global axis + per-cube face-axis assignment
makes ALL pairs' axes coincide. If 393 IS single-axis, extract its exact
(ψ, θ_k) — rational sines by construction — and report why the
Postscript 26 sweep menu missed them (angle not in the 33-point menu?).
This changes the story from "family can't reach records" to "the sweep
menu was too coarse" — flag prominently if so.

## The gluing space

Config = clique A ∪ G·(clique B):
- Clique A: {Rel(θ_i, ψ_A)} for i=1..a (Rel = Rodrigues by θ about
  (sinψ_A, cosψ_A, 0); rational for Pythagorean angles — reuse
  nfamily_common.rel_matrix).
- Clique B: {Rel(θ_j, ψ_B)} rotated wholesale by G (any integer
  quaternion — G rational keeps everything integer-quaternion).
- Sizes: n=6: (5,1), (4,2), (3,3); n=5: (4,1), (3,2); n=4: (3,1), (2,2).
  (a,0) singles are Postscript 26 territory — skip.

## Gates

G1: two-engine agreement (C++ vs certify_six.exact_count_config) on one
    glued config per n.
G2: reproduce 723 = {210,216,164,96,36,1} from the ledger quats with the
    C++ binary.
G3: reconstruct 723 AS a gluing: take its embedded 5-clique (cubes 0–4 =
    the 393) and cube 5, express cube 5 as G·Rel(θ,ψ_B) for some G (or
    verify it directly extends the clique structure); confirm the gluing
    parametrization can represent the known record before searching.

## Sweep

- Clique internals: start from the best-known family cliques (the 175/
  335/615 winners' parameters from nfamily_results.jsonl), the embedded
  record cliques (393 inside 723; whatever Q0 finds for 183/393), and a
  Pythagorean menu around them.
- G: integer quaternions by increasing norm (|components| ≤ 6 first, then
  widen for promising cells), composed with a coarse relative-axis menu.
- Count everything with the C++ engine; JSONL log
  (n, sizes, psiA, psiB, thetas, Gquat, quats, total, by_depth) to
  glue_results.jsonl; hill-climb the top cells (vary θ's, ψ's, G) with
  multi-restart from the top 10 candidates per (n, sizes).
- ANY config with total > the record (183/393/723) or equal with a new
  structure: verify immediately with the Python oracle and flag it at the
  TOP of the report — record-claim protocol requires two independent
  engines before anything is recorded, and the main session does the
  recording (never edit the ledger).

## Deliverables

/Users/dmi/carroll/glue_report.md (Q0 answer first, gate results, best
per (n,sizes) with quats + depth profiles, coverage statement),
glue_search.py, glue_results.jsonl.
