# Plan: show what regions were merged/split at each transition point

## Context

Follow-up to the dihedral-family-slider work in `depth_explorer.html`
(scratchpad master, mirrored to `depth_explorer.html`).
So far: replaced the old 67↔67 slide with a slider along the exact
dihedral family; added a "maintain concurrences" lock (clamps dragging to
one of 6 numerically-bisected zero-ghost ψ-ranges); added track marks for
the two field-named points (octahedral √2, golden √5) and for all 15 ψ
where the exact crossing/region-count set changes (`REGION_CHANGE_DEG`).

Latest ask: **"when the region count changes, please show what regions
were merged or split."**

I can't ask clarifying questions directly (no `AskUserQuestion` from a
subagent), so this plan states the design decision I'd make and why, and
flags it clearly so it can be corrected before I execute.

## The core constraint (why this isn't a one-line feature)

The viewer has no exact CSG/region-counting engine — computing the exact
total region count for a generic ψ is explicitly **open research work**
(`DIHEDRAL_FAMILY_NEXT.md` Task 1; only 3 of the 6 named points have a
certified total: 67/49/67). So I cannot literally say "region #14 merged
with region #22" anywhere except at those 3 points, and even there I'd
need to build a new region-adjacency engine I don't have.

What I *can* compute precisely, with tools already proven out in this
session (`dihedral_slider_test.js`'s segment-pair classifier, validated
against `dihedral_scratch/edge_close4.py`'s published numbers): **exactly
which edge-pairs gain or lose an exact crossing at each transition**, and
for each, the two cubes involved and their containment (depth) masks —
i.e. "a wall between a depth-1 cell and a depth-2 cell appears/disappears
here," not a specific numbered region.

**Decision (stated, not asked)**: ship the edge/crossing-level detail as
the answer to "what merged or split," worded carefully as "the crossing
event that causes a local region split/merge" rather than claiming a
literal region catalogue. This is the only level actually buildable
without new infrastructure, and it directly explains the mechanism the
user is asking about (an edge-crossing appearing = a wall splits a
cell into two of the same depth-adjacent masks; disappearing = the
reverse). If this undersells what was wanted, say so and I'll scope up to
a real 3D-cell-identity version (see "Stretch option" below) — that's a
materially bigger, riskier piece of work (needs a region-adjacency graph
built from `buildOpaqueSurface`'s polygon data, which doesn't currently
track cell adjacency, only per-face pieces).

## What I found while investigating (relevant, changes the approach slightly)

I re-derived the transition points properly for this feature: bisecting
on the **integer interior-crossing-count changing** (via the same
`segGap`/`EDGES` classifier already validated for G2/G3/G7) rather than
on "ghosts > 0" (the fuzzy 0.02-gap window used for `GHOST_FREE_ZONES`,
which is a few degrees wide and not the true transition point, just a
numerical near-miss window around it). This is the correct oracle for
"where does the count change" and gives a much tighter, more defensible
location.

Two complications surfaced:
1. The two *un-named* generic transitions (~21°, ~69°ish) are not yet in
   closed form (`DIHEDRAL_FAMILY_NEXT.md` Task 1 flags this as open); I
   bisected them numerically to ~1e-6°: **20.863680°** and (see below)
   an unresolved second value near **69.07°**.
2. That second one is only **~0.4°** from the golden point (69.095°,
   itself a spike with a different signature — crossings hand over to
   corner contacts there, not a simple count step). My first bisection
   pass, using too wide a bracket, likely straddled both events and
   produced a not-yet-trustworthy result (count-below/above readings
   didn't match the expected 18→12 plain step). Before shipping numbers
   for this specific transition I need a narrower, more careful bisection
   (bracket tightly below 69.0 to stay clear of golden's own band) and a
   direct check that the "before" and "after" crossing-count readings
   make sense as a clean step, not a blend of two events. This is a
   solvable numerical-hygiene issue, not a blocker on the design, but
   it's real remaining work, called out here so it isn't silently glossed
   over in the delivered numbers.

## Implementation plan

1. **Add an exact classifier to the shipped script** (not just the test
   harness): port `EDGES`, `segGap`, and a `familyCrossingSet(psiDeg)` /
   `familyCornerSet(psiDeg)` pair of functions into `depth_explorer.html`
   itself (small, self-contained, already validated logic — this is the
   same code `dihedral_slider_test.js` already exercises against the
   real `familyMats`, just now also live in the product for the new UI
   to call). Returns a `Map` keyed by `"cubeI,cubeJ,edgeI,edgeJ"`.

2. **Precompute `TRANSITIONS`** (offline, in a scratchpad script, the same
   way `GHOST_FREE_ZONES` was derived) — for all 8 transition angles
   (0°, ~20.86°, 35.264°, 45°, 54.736°, ~69.0-ish° [pending the fix
   above], 69.095°, 90°):
   - bisect the precise ψ (already have 6 of 8 in closed form; the 2
     generic ones numeric to ~1e-6°, with the one fix pending),
   - sample the crossing set (and corner set, for golden) at ψ±0.02°
     (small enough to stay clear of neighboring transitions given their
     spacing, large enough to be outside the immediate degenerate point),
   - symmetric-diff the two sides → `gained` / `lost` edge-pair index
     lists (as `{i,j,ei,ej}`, cube axis `a = ei>>2` gives a rough "which
     face-direction" label for a human-readable description),
   - store `{deg, countBefore, countAfter, gained, lost}` (and a
     `cornerGained/cornerLost` variant for golden's hand-over).
   Bake this into `depth_explorer.html` as a `TRANSITIONS` constant
   (same pattern as `GHOST_FREE_ZONES`/`FAMILY_NAMED` — literal numeric
   data with a comment citing how it was derived and that the two
   generic angles aren't yet closed-form).

3. **UI** (my default choice, since I can't ask): both of —
   - **Info panel**: small block under the slider, live-updating, that
     shows the *nearest* transition's data whenever ψ is within some
     small window of it (reuse the existing `famGhosts`-row style):
     e.g. "ψ≈20.86°: 12→18 crossings (+6, split) — cube 1↔cube 2 x-edges,
     cube 1↔cube 3 y-edges, ..." with the depth-mask pair per group
     (e.g. "depth {1,2} ↔ {1,3}"). Blank/hidden when ψ is far from any
     transition.
   - **3D highlight**: when near a transition, draw the specific
     gained/lost crossing point(s) as a distinct-colored ring in the
     cloud view (green = gained/split, red = lost/merge), reusing the
     existing ring-drawing code path (`CONC_COL`-style) with a new
     `kind`. This is the part that directly shows *where* the
     merge/split happens in the compound, which seems closest to what
     was actually asked for.
   I'd skip a separate tick-tooltip UI (the existing marks already have a
   `title` attribute; I'd extend that title text to include a one-line
   summary of the transition instead of adding a third UI surface) unless
   told otherwise.

4. **Wording**: hint text and panel copy will say "crossing" and
   "depth-mask boundary," not "region N," and will include one line
   making the open-research caveat explicit (no claim of an exact total
   region-count delta, only the crossing-level mechanism) — consistent
   with how the rest of this feature has been captioned so far.

5. **Testing**: extend `dihedral_slider_test.js` with a new gate section
   (G9) verifying: `TRANSITIONS` data is internally consistent (gained/
   lost sets are disjoint, non-empty, and their sizes match
   `countAfter-countBefore` where that's a simple step); the live info
   panel and 3D highlight update correctly when driving `setFamily`
   through the real DOM handlers (same pattern as G7/G8 — no
   reimplementation of the feature under test, only mirrored audit
   helpers). Fix the pending ~69°-region bisection issue and re-verify
   before baking it into `TRANSITIONS`.

6. **Rollout**: same pattern as before — get the new gates green, copy
   scratchpad `depth_explorer.html` → `depth_explorer.html`,
   md5-verify, update `dihedral_slider_report.md` with a new section.

## Stretch option (not default — only if the edge-level answer isn't enough)

Full 3D-cell identity would need: (a) building an adjacency graph over
`buildOpaqueSurface`'s output pieces (which faces bound which 3D cell —
not currently tracked, `buildOpaqueSurface` only returns per-face
polygons with a depth/mask, not cell-to-cell adjacency), (b) sampling
just-below/just-above a transition and matching cells by nearby centroid
+ mask to detect the specific split (one cell → two) or merge (two cells
→ one). This is real, scoped, buildable work, but bigger and slower than
the plan above, and still numeric (float), not exact — so it would show
"these two rendered cells look like they merged" rather than a certified
combinatorial fact. Flagging it here so the tradeoff is visible; my
default is not to build this unless asked.

## Open items before I execute

- Confirm the region-detail-level decision above (edge/crossing-level,
  captioned honestly) is acceptable, or that the stretch option is
  wanted instead.
- Confirm the UI choice (info panel + 3D highlight) or redirect it.
- I still owe a clean re-bisection of the ~69°-ish generic transition
  before that specific row of `TRANSITIONS` data can be trusted; every
  other transition's before/after crossing sets are already validated
  with the same method used for `GHOST_FREE_ZONES`/G3/G7.
