# HANDOFF_SPEC — chase the corner-handoff network (can >18 concurrences travel octahedral → golden?)

Task for the implementing agent (Sonnet). Self-contained; background in
six_cube_search_results.md Postscript 25 + addenda 1–2, working scripts in
dihedral_scratch/ (bigfamily.py, pairmap.py, loopholes.py,
trace10.py, window26.py — read these, they define every construction used
below). Ground rules: never edit six_cube_search_results.md or validated
files; write results to new files; ≤4 cores; run detached, don't park on
monitors.

## The question

In the "big family" (three cubes, each with a face-axis ⊥ the common axis
ŝ=(1,1,1)/√3, per-cube phases θ_k about ŝ, COMMON tilt ψ — seed matrix
`cubeM(θ,ψ)` in bigfamily.py), we know:

- A fixed set of 18 exact edge concurrences survives the C₃ path
  (θ = 0/120/240, ψ: 35.264° → 69.095°) from the octahedral compound to the
  golden compound.
- A chain path θ = (0, Δc(ψ), 2Δc(ψ)) carries 26 for ψ ∈ [35.264°, ≈44.5°],
  where Δc(ψ) is the curve on which ALL four cross-class "extra"
  coincidences of a pair hold identically (trace10.py). At ψ≈44.5° the
  extras' crossing points slide off the edge segments through cube corners
  (|t|→1) and the count drops to 18.
- Golden has 60 exact contacts total (6 interior + 54 corner), so there is
  room for >18 to arrive.

**A corner handoff**: when a contact point exits an edge through a vertex
(|t|=1), the same physical point may continue as a contact on an adjacent
edge of that vertex (different label). The three edges at a cube vertex are
one of each axis class, and same-class line coincidences hold identically
across the whole family while cross-class ones hold only on special curves
(loopholes.py/trace10.py) — so handoffs couple to the curve geometry.

**Decide**: what is the maximum number of physical concurrence points that
can be carried CONTINUOUSLY (handoffs allowed) from the octahedral triple to
the golden triple along any path x(t) = (θ₂(t), θ₃(t), ψ(t)) in the big
family? Specifically: is >18 achievable end-to-end? Report the best found
with a witness path.

## Definitions (implement exactly)

- Contact (pair k,l; labels ei,ej ∈ 0..11 from the EDGES table): gap<1e-9
  with |t1|,|t2| ≤ 1+1e-6. Interior if both |t|<1−1e-6; corner otherwise.
- Physical contact trajectory: a map t ↦ contact point p(t), continuous
  (enforce via step-to-step linking: at consecutive path samples, link
  contacts whose points are within δ_link; choose the path step so contact
  points move ≪ δ_link; δ_link ≈ 0.05 with step-halving verification —
  halve the step and check the linking is unchanged).
- A trajectory is CARRIED end-to-end if it links from a contact of the
  octahedral compound (t=0) to a contact of the golden compound (t=1)
  without any unlinked step. Label changes en route (handoffs) are allowed
  and expected; record them.

## Gates before any exploration counts

G1 (consistency repair): pairmap.py reported the golden PAIR at
(Δ=120°, ψ_g) as 6 interior labels, but docking.py reports the golden
TRIPLE as 6 interior total (2 per pair). These cannot both be right if the
triple's three pairs (Δ = 120, 120, 240) behave symmetrically. Recompute
both carefully (mind: pair (0,2) sits at Δ=240, and f(Δ) need not equal
f(360−Δ); mind strict-inequality thresholds at |t| exactly 1), find the
error or the explanation, and document it in the report. Everything
downstream depends on trusting these counts.

G2: reproduce the known baselines with YOUR trajectory-linking code (not
just static counts): the C₃ path must yield exactly 18 carried
trajectories; the chain path must carry 26 until ψ≈44.5° and 18 carried
end-to-end if simply continued along C₃ afterwards.

G3 (handoff calibration): drive the C₃ path THROUGH the golden point
(ψ: 68° → 70.2°) and characterize what happens to each of the 18 core
trajectories at ψ_g = 69.0948°: which survive (relabeled or not), which
die. The known set change is 18→12 across golden; your linker must
reproduce a consistent story (e.g., 12 dock at corners — determine whether
each docks-and-dies or hands off to one of the 12-set labels beyond).

## Exploration plan (after gates)

1. **Wall rescue, greedy**: follow the chain path to the ψ≈44.5° wall.
   At the wall, for each dying extra contact: enumerate its handoff
   candidates (adjacent edges at the vertex it exits through; the
   candidate contact exists iff that pair's line-coincidence holds there —
   same-class: always; cross-class: only if on the relevant curve).
   Search locally in the FULL 3-space (θ₂, θ₃, ψ) — not just the chain —
   for a direction that keeps the dying contact (or its handoff
   continuation) alive while not killing more than it saves. Each
   cross-class contact alive = one equality constraint; with 3 parameters
   you can hold at most 2 such constraints while still moving. Track the
   active constraint set explicitly.
2. **Backwards from golden**: golden has 60 contacts. Run the same
   analysis backwards (ψ decreasing from 69.095°) and see how many
   trajectories can be carried INTO golden from below and along which
   constraint curves; try to meet the forward front in the middle.
3. **Subset flood-fill (complementary, coarser)**: for candidate carried
   sets S (core-18 + specific extras/handoff chains), map the validity
   region of S on a (θ₂, θ₃, ψ) grid (cross-class members: |coplanarity|
   < 1e-3 thickening, then exact projection check on the winners) and
   flood-fill connectivity between the two endpoints' neighborhoods.
4. Report the maximum end-to-end carried count found, the witness path
   (as a polyline in (θ₂,θ₃,ψ) with per-segment active constraints, saved
   as JSONL), and — equally valuable — the OBSTRUCTION picture if 18 is
   the max: which wall kills the 19th trajectory on every attempted
   route, and why (e.g., "the extras' handoff candidates are cross-class
   pairs whose curves do not intersect the golden basin").

## Deliverables

- handoff_report.md — verdict, gate results, method,
  numbers, obstruction analysis or witness path.
- dihedral_scratch/handoff_*.py — scripts.
- handoff_witness.jsonl if >18 achieved.

Honesty requirements: this search gives a LOWER bound on the max plus
local obstruction evidence — say so; do not claim a proven maximum unless
the obstruction argument is airtight (e.g., a label-set argument that no
handoff target exists). If runs are long, run detached and report interim
state in the report file as you go.
