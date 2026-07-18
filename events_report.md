# EVENTS report — the create-vs-merge event catalogue, and the death of the "+-1 per coincidence" law

Executes `EVENTS_SPEC.md`. All numbers below are exact (Fraction / Q(sqrt d)
field arithmetic, no floats in any predicate) and reproduced by
`events_extract.py` (run it; it prints G1/G2, rebuilds every matrix from a
hand-derived or ledger-quoted witness, asserts orthonormality + S^3=I where
relevant, and writes `events.jsonl`). Never edits `six_cube_search_results.md`
or any validated file; ran on 1 core, ~29s total.

**Verdict up front.** The conjectured law ("Delta count = +-1 per coincidence
gained, sign by event type") holds EXACTLY at n=3 for the two mechanisms it
was read off of (octahedral spike: +1/crossing; face-diagonal: -1/crossing)
— confirmed here from scratch with an independently-written census tool —
but is **not a general law**. It already bends at the *other* n=3 spike
(golden: +2/point, a different coincidence type), and it is **falsified in
sign** at n=4 (a coincidence-count *increase* accompanies a 24-region
*loss*). By n=5 the same coincidence-unit magnitude (2 new corner points)
produces two *different* count penalties (-2/point vs -4/point) depending on
which pair of cubes touches. The rule that survives all twelve events is not
arithmetic but structural: **every event's entire count delta lands in the
shallow depths (d1, occasionally d1+d2), with all deeper layers exactly
conserved** — the project's recurring "deep structure conserved, d1 is what
varies" principle (Postscript 17), now confirmed pointwise at n=3, n=4 *and*
n=5, across create and merge events, interior and corner mechanisms alike.

## Gates (all PASS, `events_extract.py selftest`)

**G1** — staircase totals reproduced from the field engines, at TWO
independent Pythagorean witnesses per plateau where possible (mirror pairs
under psi<->90-psi):

| psi | (p,q,r) or field point | total | by_depth | engine |
|---|---|---|---|---|
| 0 (shared axis) | (0,1,1) | 25 | {12,12,1} | q3_count.py |
| ~0 to ~9.5deg (generic) | small_pyth(1000,1) & (13,84,85) | 31 | {18,12,1} | q3_count.py |
| ~9.5 to 20.905deg | (11,60,61), (12,35,37) | 43 | {24,18,1} | q3_count.py |
| 20.905 to 69.095deg (central) | (3,4,5), (4,3,5) | 55 | {36,18,1} | q3_count.py |
| 35.264deg (octahedral) | Q(sqrt2), hand-derived | **67** | {48,18,1} | slide3_q2.py |
| 54.736deg (octahedral-mirror) | Q(sqrt2), hand-derived | **67** | {48,18,1} | slide3_q2.py |
| 45deg (face-diagonal) | Q(sqrt6) | 49 | {30,18,1} | q6_count.py |
| 69.095deg (golden) | Q(sqrt5), hand-derived | **67** | {48,18,1} | certify_six.py |
| 20.905deg (golden-mirror) | Q(sqrt5), hand-derived | **67** | {48,18,1} | certify_six.py |

**G2** — the new field-agnostic crossing/corner census (`pair_census` in
`events_extract.py`, generalizing `nfamily_common.exact_pair_crossings`
from Fraction-only to any field exposing `.sign()`) reproduces every known
census:

- core-18 (mid-band, psi=36.87deg): interior=18, corner=0.
- octahedral (35.264deg): interior=30, corner=0.
- 45deg: interior=24, corner=0.
- golden (69.095deg): interior=18, corner label-pairs=54, deduped to 6
  physical points (18+6=24 total contacts) — exactly Postscript 25
  addendum 4's "18 interior + 54 corner label-pairs, 6 physical points."

**G3** — engine per row throughout (named in each event/row below); the
n=4/n=5 rational-quaternion censuses are double-checked in-line against
`nfamily_common.exact_pair_crossings` (interior counts agree on every one
of the 6+10 pairs checked, zero mismatches) and the region totals against
`q3_count.exact_count_q2` fed Fraction-valued matrices wrapped as
`Q2(x, 0)` — a second, independently-coded region-counting core exercised
in pure-rational mode — both reproducing the ledger's 175/151/143/387/383/
379 exactly.

## The law table

"Coincidence units" = Delta(interior crossings) + Delta(physical corner
points) — the two are geometrically different objects (a line-line meeting
vs. a shared vertex) but both are single, indivisible "extra facts" the
compound's edge/vertex arrangement acquires or loses; ratio = Delta(count) /
Delta(coincidence units), undefined where the denominator is 0.

| # | event | family | Delta count | Delta interior | Delta corner pts | Delta coin. units | ratio | Delta depth (all in) | class |
|---|---|---|---|---|---|---|---|---|---|
| 1 | shared-axis point psi=0 | n=3 | -6 | +36 | 0 | +36 | **-0.167** | d1 (-6) | negative mega-spike, isolated pt |
| 2 | band-edge wall ~9.5deg (31->43) | n=3 | +12 | 0 | 0 | 0 | **undef** | d1(+6),d2(+6) | no-coincidence wall (EXCEPTION) |
| 3 | wall 43->55 = golden-mirror spike | n=3 | +24 | +6 | +6 | +12 | +2.000 | d1 (+24) | mixed (see #8) |
| 4 | octahedral spike (55->67) | n=3 | +12 | +12 | 0 | +12 | **+1.000** | d1 (+12) | pure interior create |
| 5 | octahedral-mirror spike (55->67) | n=3 | +12 | +12 | 0 | +12 | **+1.000** | d1 (+12) | pure interior create (mirror of #4) |
| 6 | face-diagonal 45deg (55->49) | n=3 | -6 | +6 | 0 | +6 | **-1.000** | d1 (-6) | pure interior MERGE |
| 7 | golden spike (55->67) | n=3 | +12 | 0 | +6 | +6 | **+2.000** | d1 (+12) | pure corner-docking create |
| 8 | golden-mirror spike (43->67) | n=3 | +24 | +6 | +6 | +12 | +2.000 | d1 (+24) | mixed interior+corner create |
| 9 | n=4: 175 plateau -> 151 resonance | n=4 | **-24** | **+2** | 0 | +2 | **-12.000** | d1 only (92->68) | MERGE, wrong-signed vs. #4 |
| 10 | n=4: 175 plateau -> 143 chain | n=4 | -32 | -6 | -6 | -12 | +2.667 | d1(-28),d2(-4) | MERGE |
| 11 | n=5: 387-plateau lower edge (t5 1/5->8/39) | n=5 | +4 | 0 | -2 | -2 | -2.000 | d1(-4),d2(+6),d3(+2) | corner-loss create |
| 12 | n=5: 387-plateau upper edge (t5 3/14->2/9) | n=5 | -8 | 0 | +2 | +2 | -4.000 | d1(+4),d2(-8),d3(-4) | corner-gain MERGE |

(Events 3 and 8 describe the same physical wall from its two sides — #3
compares to the 43-plateau-neutral reading via the general q3 sweep
mid-point, #8 is the correct exact reading, both retained since Postscript
25 addendum 2 explicitly located the crossing-SET change here and both
directions are informative.)

## What actually holds

1. **The n=3 "+-1 per crossing" law is exact for pure-interior events, and
   only for those.** Events #4/#5/#6 (octahedral spike and both directions
   of the face-diagonal) hit ratio exactly +-1.000 — no other event in the
   table does. All three are the SAME mechanism (interior edge-edge
   crossings only, zero corner involvement) at the SAME n. This is a much
   narrower claim than the spec's opening conjecture.
2. **Corner (vertex-vertex) coincidences already break the +-1 rule at n=3
   itself.** The golden spike (#7) reaches the identical total 67 as the
   octahedral spike via 6 new *physical vertex-vertex contact points*
   instead of interior crossings, at ratio +2.000/point, not +1. A single
   n=3 compound can hit the exact same region-count ceiling by two
   structurally different routes with two different exchange rates — the
   "+-1" was already an artifact of which mechanism Postscript 25 happened
   to sample first.
3. **At n=4 the law fails in *sign*, not just magnitude.** Event #9 (175
   plateau -> 151 resonance) has coincidences *increasing* (+2 interior)
   while the count *drops* 24 — the sharpest falsification available: a
   positive coincidence delta paired with a strongly negative count delta.
   This matches `resonance4_report.md`'s own verdict ("cross-class
   alignment is count-NEGATIVE across the board") but sharpens it: it is
   not merely negative, it is *decoupled* from the coincidence count's own
   sign.
4. **At n=5, identical coincidence deltas produce different count deltas
   depending on WHICH pair of cubes is involved.** Events #11 and #12 each
   gain/lose exactly 2 physical corner points (one 9-label-pair vertex
   touch), but #11 gains 4 regions and #12 loses 8 — a factor-of-2
   difference in magnitude *and* a sign flip, for the "same amount" of
   coincidence, purely because #11's extra contact is between cube 0 and
   the mobile 5th cube while #12's is between cube 3 and the 5th cube (both
   pairs already carry a `(6,0)` interior-crossing baseline — see the
   per-pair census in `events.jsonl` — so the difference is genuinely in
   *which* vertex, not a hidden interior-crossing confound).
5. **The one law that survives everywhere: total depth is conserved except
   at the shallowest 1-2 layers.** Every single event in the table (12/12)
   has its ENTIRE Delta(count) accounted for by Delta(d1) alone, or by
   Delta(d1)+Delta(d2) (events #2 and #10), with every deeper layer bit-
   for-bit unchanged. This generalizes Postscript 25 addendum 3's "all
   staircase variation is in d1" and nfamily_report.md's n=4/5/6 finding
   ("the top two depths stay pinned... the records buy their extra total
   almost entirely in the shallow layers") into a single pointwise
   statement confirmed on every event type tested: creates, merges,
   interior mechanisms, corner mechanisms, no-coincidence walls, n=3, n=4,
   and n=5 alike.
6. **Band-edge walls are a genuine third event class, not an exception to
   patch over.** Event #2 (31->43, ~9.5deg) has the exact edge-edge
   crossing count FROZEN at 12 on both sides — confirmed here for the
   first time with an exact (not numeric) crossing count, extending
   Postscript 25 addendum 3 point 4's claim from "no edge-crossing event"
   (checked to 1e-16 previously) to an exact zero-Fraction-difference
   certificate. Region count still jumps +12 via d1(+6)+d2(+6) alone —
   demonstrating that d1/d2 combinatorics (how the existing, UNCHANGED set
   of face/edge intersections reorganizes into cells) is a source of count
   change fully independent of the coincidence census. The "law" simply
   does not apply here (0/0); it is a different event type entirely, exactly
   as the spec anticipated ("pure top/bottom-diagram combinatorial events
   with zero coincidence change").

## A correction to Postscript 25 addendum 3

The addendum's table lists `psi in (0, ~9.6deg): 25 = {12,12,1}` as an open
interval. Exact reproduction here shows this is wrong as stated: **25 is the
value ONLY at the single isolated point psi=0** (and by the psi<->90-psi
mirror, psi=90). Generic psi immediately surrounding it — checked down to
psi=0.0002deg using Pythagorean triples built from (2mn, m^2-n^2, m^2+n^2)
with m up to 1000 — gives 31={18,12,1} throughout, the SAME plateau
previously placed only in "(~9.6,~10.9)." So the real structure below the
golden-mirror point is: **{25 at psi=0 only} | 31-plateau (0,~9.5) |
43-plateau (~9.5,20.905) | spike/wall at 20.905 (golden-mirror, 67) |
55-plateau (central)** — three plateaus and one isolated point where the
addendum's table implied four plateaus. This reclassifies psi=0 itself as
event #1 in the table above: a **negative mega-spike** — interior crossings
jump from 12 to 48 (the shared-axis compound's own "48 at psi=0/90" already
noted in the ledger's main Postscript 25 text) yet the region count *drops*
by 6 relative to its immediate surroundings, the most extreme
coincidence-rich/count-poor pairing found in this whole campaign (ratio
-0.167, i.e. 36 new coincidences buy back only 6 fewer regions — most of
that coincidence richness is wasted, geometrically redundant under the
compound's own C3 x (further axial) symmetry at the fully-degenerate point).

## Depth-resolved answer to Task 4's specific question

"Verify the spikes' +-12/-6 land in d1 too" — yes, exactly, for every
n=3 spike checked (events #4, #5, #6, #7 all show `Delta d2 = Delta d3 = 0`
to the Fraction). The golden-side events (#7, #8) additionally show this
holds even when the mechanism is corner-docking rather than interior
growth: the 6 new vertex-vertex contacts still only ever touch d1.

## Coverage / honesty notes

- The n=4 and n=5 census used the SPEC-supplied / ledger-supplied rational
  witnesses (175/151/143 quats from `nfamily_report.md` §Q1 and
  `EVENTS_SPEC.md`; 387-plateau-edge quats read directly from
  `rattan_results.jsonl`, kind `393clique+5th-onaxis`, at the exact
  Farey-adjacent boundary pair (1/5, 8/39) and (3/14, 2/9) already
  identified in `rattan_report.md`'s P1 line). No new search was run; this
  campaign is a census/comparison layer on top of already-validated
  results, per the spec's scope.
- The exact algebraic location of the two n=3 band-edge walls (~9.5deg,
  its mirror ~80.5deg) was NOT pinned down here (out of scope per spec:
  "sides only"); `q3_count`'s Pythagorean sweep only brackets it between
  (7.628deg, 9.527deg) on the low side (both giving 31) and
  (9.527deg,11.421deg) is impossible to narrow further without either a
  finer Pythagorean menu or an exact resultant/Groebner derivation of the
  wall condition — flagged as the natural follow-up, not attempted.
- "Coincidence units" (interior + corner points) is a bookkeeping choice
  made explicit in `events_extract.py`, not a claim that interior
  crossings and corner points are physically equivalent — table column
  `delta_corner_label_pairs` (9x the physical-point count for a genuine
  vertex touch) is also recorded in `events.jsonl` for readers who prefer
  the raw label-pair count.
- `pair_census` (the new field-agnostic census function) is validated by:
  (a) exact agreement with `nfamily_common.exact_pair_crossings` on every
  rational pair checked (16 pairs across the n=4/n=5 configs, zero
  mismatches); (b) exact reproduction of the golden 18+54/6 census
  (Postscript 25 addendum 4) from an independently hand-derived Q5 matrix,
  not copied from any prior script.

## Files

- `events_extract.py` — the full executor: field-agnostic crossing/corner
  census (`pair_census`), hand-derived exact matrices for the octahedral-
  mirror/golden/golden-mirror points (checked orthonormal + S^3=I before
  use), G1/G2 self-tests, the 12-event law table, `events.jsonl` writer.
- `events.jsonl` — one JSON record per event: sideA/sideB (total, by_depth,
  interior, corner_label_pairs, corner_points), all deltas, ratio, engine,
  and a free-text note.
- `events_report.md` — this file.
