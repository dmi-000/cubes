# Handoff report: can >18 edge concurrences be carried octahedral → golden?

Task: HANDOFF_SPEC.md. Verdict up front: **no path was found that carries
more than 18 physical edge-concurrence points continuously from the
octahedral 3-cube compound to the golden 3-cube compound.** 18 is the best
found, it is reproduced independently by the trajectory-linking code
(not just static counts), and a fairly wide local search around the
natural bottleneck (the ψ≈45° wall) finds a specific, describable
obstruction rather than merely "nothing turned up." This is reported
honestly as a **lower bound of 18, plus local obstruction evidence** — not
a proof that 18 is the ceiling.

Scripts (new, this task): `dihedral_scratch/handoff_common.py` (geometry:
EDGES table, `cubeM(theta,psi)`, contact classification exactly per the
spec's definitions), `handoff_linker.py` (trajectory linker with
δ_link-based step-to-step linking and handoff detection),
`handoff_g1.py`, `handoff_g2.py`, `handoff_g3.py` (the three gates),
`handoff_explore.py` (the exploration). All are self-contained and do not
`exec()` any file from `cubes/scratchpad/`; none of the ledger or
validated files were modified.

**Note on the spec's own file paths.** HANDOFF_SPEC.md says the background
scripts live in `/Users/dmi/carroll/dihedral_scratch/`; they are actually
in `/Users/dmi/carroll/cubes/scratchpad/` (`dihedral_scratch/` exists but
only contains an unrelated handful of `edge_close*.py` files). Read from
the real location; wrote new deliverables to `dihedral_scratch/` as
instructed.

---

## G1: consistency repair — PASS (error found and explained)

`pairmap.py`'s "golden pair: interior=6" and `docking.py`'s "golden triple:
6 interior total (2 per pair)" are **not actually in conflict** — they
answer different questions, and HANDOFF_SPEC's own background text
("golden has 60 exact contacts total, 6 interior + 54 corner") is where the
real arithmetic slip lives.

Recomputing carefully (full unrestricted 144-label scan per pair, unclipped
closest-approach `t`, strict `|t|` thresholds, both Δ=120° and Δ=240°
checked separately per the "mind f(Δ)≠f(360−Δ)" warning):

| quantity | value |
|---|---|
| single pair (Δ=120°) at ψ_g, full scan | 6 interior + 18 corner = 24 |
| single pair (Δ=240°) at ψ_g, full scan | 6 interior + 18 corner = 24 (same counts, different specific labels — no violation of f(Δ)≠f(360−Δ), the label *sets* differ, the *counts* happen to match) |
| full triple (3 pairs), full scan | **18 interior + 54 corner = 72** label-pair contacts |
| triple, deduplicated to **physical points** | **18 interior points + 6 corner points = 24 distinct points** (each corner point is a genuine cube-vertex-to-cube-vertex coincidence, registering 3×3=9 label-pairs; 6×9=54) |
| persistent core-18 only (docking.py's restricted list), at ψ_g | 6 interior + 12 corner = 18 (matches docking.py exactly) |

**The repair:** `pairmap.py`'s "6" is a *per-pair* figure; tripled across
the triple's 3 pairs it is 18, not 6. `docking.py`'s "6 interior total" is
the fate of one *pre-selected* list of 18 labels (the persistent
octahedral→golden core, inherited from a ψ=50° snapshot) — it never
re-scanned for new labels that only become interior/corner exactly at
golden, so it was never in the business of reporting golden's total
contact count. Golden has its **own** 12 new interior label-pairs (6 new
distinct physical points) beyond the persisting core-6 — the golden-side
analogue of the octahedral point's own 12 extra crossings (Postscript 25's
30 = 18 core + 12 extra at the octahedral point). The spec's "60 total (6
interior + 54 corner)" mixes a per-pair interior figure with a
triple-total corner figure — an apples-to-oranges sum, not a real count of
anything. Corrected figures above. `handoff_g1.py` reproduces this
end-to-end.

Downstream trust: the persistent core-18's fate at golden (6 interior + 12
corner, 0 broken) **is** correct and is what G2/G3 build on. Golden's
additional 6 new interior physical points are real and became the target
of the "backwards from golden" exploration (§ Exploration, Part 2).

---

## G2: baseline reproduction — PASS

Using the actual trajectory-linking code (δ_link=0.05, step-halving
verified):

- **C3 path** (θ fixed at 120°/240°, ψ: 35.264°→69.095°, N=400 and N=800
  steps): **18 carried end-to-end**, identical starting-label set at both
  resolutions, 0 handoff events needed (each of the 18 stays on its own
  label the whole way — golden's corner docking doesn't require a
  relabeling to count as "reaching a golden contact").
- **Chain path** (θ=(0,Δ_c(ψ),2Δ_c(ψ)), ψ: 35.264°→44.9°, N=300 and
  N=600): peak simultaneous contact count **26**, reproduced at both
  resolutions (matches window26.py's static-count table exactly: 10+10+6
  from ψ=35.264° to ψ=44°, dropping at the ψ=45° wall).
- **Chain, continued via C3 after the wall** (chain to ψ=44°, linear
  θ-transition back to 120°/240° over ψ∈[44°,45.5°], then C3 to golden):
  **18 carried end-to-end**, confirming the "26 then 18 if simply
  continued along C3" baseline with an actual continuous, linked path
  rather than just comparing two static snapshots.

---

## G3: handoff calibration through golden — PASS, and a genuine finding

Driving the plain C3 path through ψ∈[68°,70.2°] (881 steps, ~0.0025°
resolution) and linking with δ_link=0.05: **all 18 core trajectories are
carried continuously through the golden point itself** — golden is not a
break point for the linker (gap<1e-9 holds exactly at ψ_g for all 18).
What changes is the interior/corner classification, and past golden the
18 split three ways, 6 each:

- **6 stay interior** on the same label throughout (never approach `|t|=1`
  near golden at all — e.g. `(0,1,5,4)`).
- **6 dock at golden (`|t|=1` exactly) and genuinely hand off** to a
  different label at the same cube vertex — e.g. `(0,1,0,1)` → 
  `(0,1,4,5)`. Verified by hand that the vertex is shared: cube-0's edge 0
  exits through corner (−1,−1,−1), exactly where cube-0's edge 4 also
  sits. The target labels are themselves members of the same
  "always-coplanar" same-class identity family as the core-18 (verified:
  `(4,5)` and `(5,4)` both have machine-zero line-coplanarity for *all*
  θ,ψ) — they simply weren't part of the *original* 18-label selection,
  which was made once at the octahedral point.
- **6 genuinely die** at golden (`(0,1,8,8)`, `(0,1,11,11)` type) — no
  same-class or cross-class candidate at their exit vertex stays in
  [−1,1] on the far side within δ_link.

Net: 12 of 18 survive continuously past golden (6 same-label + 6 via
verified corner handoff), independently reproducing the family's known
ψ-plateau structure (12-crossing plateau beyond golden) as a nontrivial,
untuned cross-check on the linker. This is a real, working handoff — but
it happens *along the standard C3 path* and changes what survives *past*
golden, not what *arrives at* golden (still 18, per G2). It is the
existence proof that handoff machinery finds genuine geometric handoffs
when they're there, which is why the exploration's negative result below
carries some weight.

---

## Exploration: chasing the ψ≈45° wall, and backwards from golden

**Where the wall is.** The chain path's four cross-class extras
`(4,10),(7,9),(9,6),(10,5)` (pair (0,1), sharing one curve Δ_c(ψ) per
Postscript 25 addendum 2) die at **exactly ψ=45.000°, θ₂=109.4712°** — not
an asymptotic approach, a genuine algebraic zero of `|t|−1`. Identifying
the actual cube vertices: cube-A's vertex (−1,1,−1) is touching cube-B's
vertex (1,−1,−1) *exactly* at this configuration — a real vertex-vertex
coincidence, giving 3×3=9 candidate edge-pair relabelings at that single
point (plus 2 more from a second, independent x-y-class vertex event
coincident at the *same* (θ₂,ψ) — ψ=45° is itself a resonance point of the
whole family, matching Postscript 25's "24 AT ψ=45 exactly").

**Wall-rescue result (9 candidates traced, both directions each):** *none*
of the 9 vertex-adjacent relabelings — `(2,10),(4,0),(2,0),(2,6),(4,6),
(9,0),(9,10),(1,5),(0,4)` — continues past the wall to reach the golden
neighborhood (θ₂=120°, ψ=69.095°) while staying in-segment the whole way.
Each either re-hits `|t|=1` within a fraction of a degree on the far side
(most of them, right back at ψ≈45°, since ψ=45° is where multiple branches
of the same algebraic curve happen to cross), or belongs to a separate
branch that runs off to ψ≈89° at θ₂≈90° or 179° (the shared-axis / ψ=90°
region) without ever passing near θ₂=120° at ψ≈69°.

**Backwards from golden.** Golden has its own extras — a **third**,
independently-verified pair-curve identity (x-z class:
`(1,9),(2,10),(9,0),(10,3)`, all four sharing one curve through the exact
golden point, confirmed by an in-plane sign-change test and by tracing).
Traced backwards (decreasing ψ), this curve's wall is at
**θ₂=180.007°, ψ=44.997°** — landing at almost the same ψ as the
octahedral-side wall (≈45°, both instances of the same family-wide
resonance) but **~70° away in θ₂**. The curve's other end runs to
θ₂≈91°, ψ≈89° (the shared-axis ψ=90° region), not back toward the
octahedral-side wall. A third cross-class family (x-y class) was checked
too, for completeness: it has its own special points at mirror-golden
(20.905°) and the same ψ=45° resonance, reinforcing the pattern (its
representatives at the wall and at golden land exactly at existing corner
points, not new interior contacts) rather than offering a new bridge.

**Grid corroboration.** A bounded (θ₂,ψ) grid map for pair(0,1)
(θ₂∈[0°,360°) step 1°, ψ∈[20°,90°] step 0.25°, fully vectorized,
101,160 cells) shows the region with pair-level count ≥7 (i.e. beyond the
6-label core) covering only 0.28% of the grid — a sparse 1-dimensional
network of curves, not an open 2-D patch, exactly as expected since each
extra is one codim-1 (cross-class) condition and holding two independently
eats the family's only "motion" parameter (ψ), per the exploration plan's
own DOF argument. This is corroborating, not decisive (see caveats below).

**The obstruction, stated plainly:** the octahedral extras (y-z class,
living near θ₂≈110°) and golden's own extras (x-z class, living near
θ₂≈180°) are *different label families on different curves*. Both curves
happen to graze the family's ψ=45° resonance line, but at θ₂ values ~70°
apart, and neither curve's far branch swings back around to link them. A
handoff rescue would need a path that holds *some* cross-class equality
constraint continuously while walking θ₂ across that 70° gap near ψ≈45° —
and no such constraint (among the ones checked: 9 wall-vertex candidates +
2 further backward-from-golden families) was found to exist there.

---

## Honesty / scope

- **This is a lower bound (18) plus local obstruction evidence, not a
  proof.** The search covered: all vertex-adjacent same/cross-class
  labels at the identified wall (9 candidates, both directions), all four
  members of golden's own extras curve (backwards), and a third
  cross-class family, plus a coarse global (θ₂,ψ) grid. It did **not**
  exhaustively search the full 96-cross-class-label space at every point
  of a fine 3-D (θ₂,θ₃,ψ) grid, nor multi-hop handoff chains through
  vertices beyond the immediate wall neighbors (e.g. a rescue that dies
  again at a *second* wall but picks up a *third* label there, etc.) —
  that is a much larger search that was out of scope for the time
  budgeted here.
- No `handoff_witness.jsonl` was produced, since no >18 path was found to
  witness.
- All work ran on a single core, well under the ≤4-core budget, and
  finished in well under a minute per script (no long-running jobs needed
  monitoring).
- `six_cube_search_results.md` and all files under `cubes/scratchpad/`
  were only read, never modified.

## Files

- `dihedral_scratch/handoff_common.py` — geometry (EDGES table, `cubeM`,
  contact classification per the spec's exact definitions).
- `dihedral_scratch/handoff_linker.py` — δ_link trajectory linker with
  handoff detection.
- `dihedral_scratch/handoff_g1.py`, `handoff_g2.py`, `handoff_g3.py` —
  the three gates (all PASS; run each directly, e.g.
  `python3 handoff_g1.py`).
- `dihedral_scratch/handoff_explore.py` — the exploration (wall rescue,
  backwards-from-golden, third-family check, grid corroboration); also
  writes `handoff_explore_log.txt`.
