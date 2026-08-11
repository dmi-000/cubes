# EVENTS_SPEC — the create-vs-merge event catalogue

Task for the implementing agent (Sonnet). Background: ledger
Postscripts 25 (+addenda 2–4), 28, 29; q3_count.py / q6_count.py /
slide3_q2.py (validated field engines, read-only); nfamily_common.py
(exact pair-crossing counter — REUSE); rattan_results.jsonl,
resonance4_results.jsonl (existing exact counts). Ledger and validated
files READ-ONLY. ≤2 cores (other campaigns may share the machine).

## The question

When a compound acquires an extra exact coincidence (edge-edge
crossing, corner contact, …), the region count jumps. Known data
points suggest a striking law: Δcount = ±1 PER coincidence gained,
with the sign depending on the event type:

- dihedral family, octahedral spike ψ=35.264°: crossings 18→30
  momentarily (+12), count 55→67 (+12): **+1 per crossing**.
- family at ψ=45°: crossings 18→24 (+6), count 55→49 (−6):
  **−1 per crossing**.
- n=4: family plateau 175 vs the yz-resonance 151 (−24) — coincidence
  delta UNKNOWN (you will measure it).

Goal: an exact event catalogue rich enough to state (or refute) the
law and classify the sign mechanism.

## Tasks

1. **Dihedral family events (n=3), exact.** For each wall/spike of the
   staircase (Postscript 25 addendum 3): ψ = 20.905°, 35.264°, 45°,
   54.736°, 69.095°, plus the band-edge walls near 9.6°/80.4° and any
   others in the q3 sweep data. For each event tabulate EXACTLY:
   count and depth profile on both sides (staircase data / q3_count at
   Pythagorean ψ) and AT the wall where the field permits:
   35.264° and 54.736° are ℚ(√2) points of the family (verify! the
   S(ψ) entries simplify), 45° is ℚ(√6) (q6_count validated), 69.095°
   is ℚ(√5), 20.905° is the mirror golden (Theorem M ⇒ same counts as
   69.095°). And the exact coincidence census at/near the wall:
   number of exact edge-edge coincidences by type (segment-interior
   |t|<1 vs corner |t|=1; class x/y/z; label pair) via the exact
   crossing counter on the exact matrices. Band-edge walls at
   non-quadratic ψ: sides only, plus a statement of what (if any)
   coincidence structure changes there — Postscript 25 found NONE
   (walls not tied to crossing-set changes); confirm and flag those
   events as law-EXCEPTIONS or as a different event type (they may be
   pure top/bottom-diagram combinatorial events with zero coincidence
   change — that itself is a key datum).
2. **The n=4 resonance pair.** Exact coincidence census for (a) a
   family plateau config counting 175 (rational — take one from
   nfamily_results/glue data or build a chain), (b) the 151 resonance
   (rational! quats 1,0,0,0;-1,2,1,0;2,2,1,0;7,-2,-1,0), (c) a 143
   variant if expressible rationally. Does Δcount = −24 match the
   coincidence delta at −1 per extra coincidence? Count BOTH
   edge-edge coincidences and vertex-vertex/corner contacts.
3. **The 387 plateau edges (n=5).** From rattan_results.jsonl (kind
   393clique+5th-onaxis): identify the exact t₅ interval of the 387
   plateau and the counts just outside both ends. For the boundary
   t₅ values (plateau-edge Farey points and their neighbors): exact
   coincidence census on each side. What event bounds the plateau?
4. **Law table.** One row per event: exact ψ or t (algebraic form),
   Δcoincidences by type, Δtotal, Δd_i per depth, ratio, sign,
   event classification (momentary spike / set change / plateau edge /
   no-coincidence wall). State the law as the data supports it,
   including exceptions. Depth-resolved version: which layer do the
   created/destroyed regions live in? (Known: all staircase variation
   is in d1; verify the spikes' ±12/−6 land in d1 too.)

## Gates (before any new claims)

G1: reproduce the known staircase totals 25/31/43/55 and spikes
    67 (35.264°), 49 (45°), 67 (69.095°) with the field engines.
G2: crossing counter reproduces the known censuses: core-18 on the
    middle band, 30 at octahedral, 24 at 45°, 18 interior + corner
    contacts at golden (54 label-pairs = 24 physical points,
    Postscript 25 addendum 4).
G3: any NEW exact count must be produced by a validated engine
    (q3/q6/slide3_q2/C++ for rational/oracle) — name the engine per
    row; two engines for anything used as a load-bearing claim.

## Deliverables

events_report.md (the law table + verdict + mechanism notes),
events_extract.py, events.jsonl (one record per event, machine-
readable, exact values as strings). Never edit the ledger; main
session records.
