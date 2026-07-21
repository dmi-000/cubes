# CRITERION_SPEC — the local create-vs-merge criterion, as a lookup table

Task for the implementing agent (Sonnet). Background: ledger Postscripts
30 (events) and 31 (census); events_report.md, census_report.md,
census_extract.py / census_data.json (REUSE the exact spherical-diagram
machinery), PROOF_67.md §5 (the top-diagram Euler picture). Ledger and
validated files READ-ONLY. Light compute; exact arithmetic in decisions.

## The question, now sharp

Postscript 30 killed the "±1 region per coincidence" guess but proved
that every event's entire count change lands in depth-1 (deep layers
conserved). Postscript 31 explained why: coincidences are exactly
vertices of the TOP diagram, and d1 = F(top) = 2 + ½Σ_v(deg_v − 2). So
when a coincidence appears or disappears as a parameter crosses a wall,
Δd1 = ½·Δ[Σ_v(deg_v − 2)] = the change in total top-diagram vertex
weight. **A coincidence CREATES regions iff it adds vertex weight, MERGES
iff it removes weight.** The task: turn this into a finite, exact lookup
table over coincidence types — the closed criterion the events catalogue
reduced to but did not write down.

## Plan

1. **Enumerate coincidence event types.** A wall in parameter space is
   where the top diagram's combinatorial type changes. Classify by the
   local geometric event:
   - a swap arc r_i=r_j sweeping through a triple point (three-cube
     tie appears/annihilates),
   - an interior edge-edge coincidence forming/breaking (a degree-4
     contact vertex, as in the octahedral 30),
   - a corner/vertex-vertex contact (degree-6, as in golden's 6),
   - an active-face change (kink) crossing a swap arc,
   - the no-coincidence combinatorial wall (Postscript 30 event #2:
     weight changes with the coincidence census frozen — the top
     diagram re-triangulates with no vertex added; this is the third
     class and MUST be included).
   For each, the local picture is a small planar graph transition.
2. **Compute the local Δweight exactly** for each type: the before/after
   degrees of the vertices involved, hence Δ[Σ(deg−2)] and Δd1 = half
   that. Do this by exact local analysis (the great-circle arcs meeting
   at the event, via the census machinery restricted to a neighborhood),
   NOT by differencing global counts — the point is the LOCAL rule.
3. **Validate against every Postscript-30 event.** For all 12 tabulated
   events (events.jsonl), the sum of local Δweight contributions over the
   coincidences involved must reproduce the measured Δd1 exactly. This is
   the gate: local rule ⇒ global deltas, 12/12.
4. **State the criterion.** A table: event type → Δd1 sign and magnitude.
   Explain the apparent anomalies with it: octahedral +12 (interior
   creates), 45° −6 (interior merges — same geometric type, opposite
   sign: resolve WHY, i.e. which side of the wall the region sits),
   golden +2/point (corner), the n=4 175→151 sign decoupling, the n=5
   pair-dependent −2 vs −4. If the sign genuinely depends on more than
   the local type (e.g. on a global orientation), say so precisely — a
   negative result ("no purely-local criterion exists, here is the
   minimal extra data needed") is a valid, valuable outcome.

## Gates

G1: reproduce (via census_extract machinery) the top-diagram weights 92
    at both 67 witnesses and the bottom-diagram genericity — i.e. the
    machinery is the validated one.
G2: for each of the 12 events, local Δweight summed = measured Δd1
    (exact). Any mismatch is a bug or a genuine nonlocality — diagnose
    which.
G3: the deep-layer conservation (Δd2=Δd3=0 except the two d1+d2 events)
    falls out of "coincidences are top-diagram-only" — confirm the
    bottom diagram is unchanged across each event exactly.

## Deliverables

criterion_report.md (the lookup table + the resolved explanations of the
Postscript-30 anomalies + honest statement of any nonlocality),
criterion.py, criterion_events.jsonl (per event type: local graph
transition, Δweight, Δd1, sign). Never edit the ledger or validated
files.
