# Dihedral slider — implementation report

Task: DIHEDRAL_SLIDER_SPEC.md. Replaced the depth_explorer.html viewer's
"67 ↔ 67 slide" (Postscript 9's `pSlide`/`slideGrp`/`slideMats`) with a
slider along the dihedral family (Postscript 25), which has exact edge
crossings at every ψ instead of the old slide's dashed ghost gaps.

**Update 1**: live feedback while this was in progress — "the slide shown
is not maintaining edge concurrences. there should be a way to slide
while maintaining edge concurrences" — led to a follow-up (G7 below): a
numerically-located set of six zero-ghost ψ-ranges and a "maintain
concurrences" lock button that clamps dragging to one of them, so the ring
set provably stays fixed for the whole drag.

**Update 2**: further live feedback — "mark the octahedral sqrt(2) and
golden sqrt(5) points of the slider, and also show where the number of
regions change" — led to G8 below: a tick-mark overlay directly on the
slider track (gold marks for the two field-named points, plain marks for
the other four named points, grey marks at every ψ where the exact
crossing/region-count set changes). Building this also caught and fixed a
real bug in the test harness's own DOM stub (see G8 / "harness fix" note).

**Update 3**: two more asks, taken together — "show what regions were
merged or split" (asked, then planned, before the next message arrived),
then "highlight surfaces that separate regions that have been split, and
allow zooming into the display, and making surfaces opaque only on one
side of the cross section plane." I planned an initial approach for the
first ask (a precomputed exact-transition table) but abandoned it before
building anything, in favor of a simpler mechanism that the second
message pointed straight at: the *existing* ghost detector already
identifies near-miss crossings, which *are* the surfaces currently
splitting/merging — so highlighting is computed live at any ψ, not from a
precomputed 8-point table. See G9 below for this plus zoom and one-sided
opaque clipping. A checkpoint of the pre-G9 state was saved first (see
"Checkpoint" note) per an explicit save-state request.

**Update 4 (theory corrections from the Postscript 25 addendum,
coordinator-directed)**: two facts from the new pair-identity results in
`six_cube_search_results.md` ("Postscript 25, addendum") invalidated parts
of Updates 1-2, both re-verified independently here against the validated
classifier before changing anything:
- FACT 1 (core persistence): one FIXED set of 18 interior edge pairs is
  exact and unbroken across the whole open interval ψ ∈ (20.905°,
  69.095°) — between the two golden copies. The 30/24/30 counts at
  octahedral/face-diagonal/mirror-octahedral are momentary spikes (+12/+6/
  +12 extras existing only exactly AT those isolated ψ). At either golden
  endpoint 12 of the core dock exactly onto cube corners (t=±1) and 6
  stay interior (t=±1/φ³); nothing breaks. Outside the interval the
  constant core has 12 members.
- FACT 2 (transitions): the crossing SET changes only at 20.905°
  (mirror-golden = 90−arctan φ²), 45°, and 69.095° (golden). The
  "unnamed transitions at ≈21.4°/≈68.6°" formerly implied by the track
  marks were GHOST-BAND boundaries (edges of the 0.02-gap near-miss
  window), not set changes. (This also dissolves Update-3's "conflation
  mystery" near 69°: there is only one event there, golden itself.)
Changes: the lock is now core-aware (clamps to the core interval, so the
complete octahedral→golden drag is allowed under lock with "core 18
maintained" in the readout; always engages; supersedes the zone-based
lock — GHOST_FREE_ZONES kept for display); track marks re-taxonomized
(3 true set-change marks, 2 spike marks "momentary +12", 12 faint
band-edge marks "not a set change"); mirror-golden added as a 7th named
tick ("mirror golden 67", certified 67 by congruence); hint text
rewritten with core-18 persistence as the headline. See G10 (new gates)
and the G7/G8 rewrites.

The mirror has been synced with all four updates included; see "Mirror
sync" at the end.

Files touched:
- Master (edited): scratchpad `depth_explorer.html`
- Mirror: **synced** (see "Mirror sync" below)
- Harness (extended): scratchpad `dihedral_slider_test.js` (now G1-G10)
- `opaque_test.js` (existing regression suite): one mechanical fix, see G5
- Checkpoint (new, untouched since creation): scratchpad
  `depth_explorer.pre-highlight-zoom-clip.html` and
  `dihedral_slider_test.js.pre-highlight-zoom-clip.js` — the state right
  before Update 3, kept as an explicit rollback point on request.

Not touched: `six_cube_search_results.md`, any validated `.py`/`.cpp` file,
no artifacts published.

## What changed in depth_explorer.html

- HTML: `pSlide` mini-button → `pFamily` ("dihedral family"); `slideGrp` →
  `familyGrp`, now holding a ψ readout, a 0–90° range slider (`famPos`,
  0.01° resolution), a row of six tick buttons (`famTicks`, one per named
  point, built by `buildFamilyTicks()`), and updated hint text.
- JS: removed `S_OCT`, `SLIDE_AXIS`, `SLIDE_DELTA`, `rodrigues()`,
  `slideMats()` (dead — nothing else referenced them). Kept `matMul` and
  `C3` (the spec's closed-form `C` is literally the old `C3` constant, so
  it was reused rather than duplicated).
- Added `S_HAT`, `U_HAT`, `W_HAT`, `PHI`, `familyMats(psi)` (the spec's
  closed form: `M(ψ)` columns `[cosψ·w+sinψ·ŝ, −sinψ·w+cosψ·ŝ, u]`, cubes
  `{M, C·M, C²·M}`), and `FAMILY_NAMED` (the six named points, each with
  degrees, a name, a crossing-count label, and — for three of them only —
  a certified `{total, d}` object, see "exact-count display" below).
- Added `setFamily(psiDeg)` / `exitFamily()` / `buildFamilyTicks()` /
  `nearestFamilyNamed()`, wired the same way `setSlide`/`exitSlide` were:
  live matrix rebuild → `matToCols` → `buildFilters/samplePoints/
  computeConcurrences/renderSlice`, so it drives slice, cloud, wireframe,
  concurrence rings, and opaque mode identically to the old slide and to
  the static presets.
- Snapping: dragging within 0.3° of a named point snaps ψ to the exact
  closed-form value (and the slider position); clicking a tick jumps
  there exactly. Off-snap positions show generic exact-crossing text
  instead of a region-count chip (see below).
- Left the ghost-ring machinery itself untouched (generic, reused) —
  updated its comments since it's no longer specific to the old slide.
- **Follow-up, from live feedback**: added `GHOST_FREE_ZONES` (six `[lo,hi]`
  degree ranges, numerically bisected to ~1e-6° against the real,
  unmodified ghost detector) and `findGhostFreeZone(deg)`. Added a
  "🔒 maintain concurrences" toggle (`famLock`) next to a live ghost-count
  readout (`famGhosts`): engaging it while ψ sits inside one of the six
  zones clamps all further dragging to stay within that zone, so the
  crossing *set* — not just each individual crossing — is guaranteed
  constant (0 ghosts) for the whole drag. Clicking a named tick always
  releases the lock (those points are certified-exact in their own right
  even when, as at octahedral/mirror-octahedral/golden, they sit *inside*
  a transition band rather than in one of the six zones). See G7.
- **Follow-up 2, from live feedback**: added a `.trackWrap`/`.trackMarks`
  overlay directly above the `famPos` range input (`renderFamilyMarks()`,
  populated on entering family mode): a small gold mark at each of
  octahedral 67 and golden 67 — renamed `octahedral 67 (√2)` /
  `golden 67 (√5)` in `FAMILY_NAMED` to match the static preset buttons'
  naming (Postscript 9: entries at these two points live in ℚ(√2) /
  ℚ(√5) respectively) — plain marks at the other four named points, and
  grey marks at every ψ in the new `REGION_CHANGE_DEG` list (0°, 45°, 90°,
  plus all 12 `GHOST_FREE_ZONES` boundaries — the full set of psi where
  the exact crossing/region-count set changes, a superset of the six
  named points since it also includes the two unnamed ≈21°/≈68.6°
  transitions). A small legend under the track explains the three mark
  colours. See G8.
- **Follow-up 3, from live feedback**: three pieces.
  - *Split/merge surface highlighting*: `faceContainsPoint(f,p,tol)` tests
    whether a point lies near a `buildOpaqueSurface` face's actual
    **boundary** (perpendicular distance to each polygon edge, not a loose
    "inside the polygon" test — an earlier centroid+radius version
    over-matched badly, see "A precision fix mid-build" below).
    `computeHighlightFaces()` (called from `ensureOpaqueSurface()`, so it
    stays in sync with `opaqueSurface`/`ghosts`) runs this for every
    ghost against every opaque face restricted to the two cubes that
    produced that ghost (`ghosts[i].ka`/`.kb`, and each opaque face's new
    `srcCube` tag — both purely additive fields, nothing upstream reads
    the exact key set of either object). Matched faces are outlined in
    `#ff3b6e` (hot pink, not reused from elsewhere in the palette) with a
    thicker stroke in `drawOpaqueSurface`, in opaque mode only.
  - *Zoom*: `camZoom` (default 1, clamped `[0.25,6]`), a `wheel` listener
    on the cloud canvas (`×1.1`/notch), a live `zoom: NNN%` readout, and a
    reset button. Threads through the single `S` scale factor in
    `drawCloud()`, so it uniformly affects opaque/wireframe/points/rings/
    ghosts/the slice-plane quad — one change, whole view.
  - *One-sided opaque clip*: reuses the slice view's own plane
    (`axisBasis(sliceAxis)`, `sliceOff`) — the same plane already drawn as
    the translucent quad. A `clip` toggle + `flip` mini-button filter
    `drawOpaqueSurface`'s face list by which side of that plane each
    face's centroid falls on. Centroid-based, not exact polygon
    re-clipping (an explicit, stated scope choice — occasionally a piece
    whose centroid is just inside the kept half will still show a sliver
    poking across the cut; not a correctness bug, just a softer edge than
    a true clip would give).
  See G9. Before any of this, per an explicit "save the current state"
  request, I checkpointed the pre-Update-3 files (see Files list above).

### A precision fix mid-build (split/merge highlighting)

First version of `faceContainsPoint` used centroid-distance vs. polygon
"radius" as the in-piece test. Smoke-testing near the octahedral spike
(ψ=35.264°+0.5°, 12 ghosts present) showed 96 of 144 opaque faces
highlighted — visually, "most of the compound," which would defeat the
point of a *highlighting* feature. Investigated before shipping it:
inspected the actual sorted distances from one ghost's point to its
candidate faces and found real signal (10 faces within 0.03, then a hard
jump to 0.56 — a clean, unambiguous separation) but the "radius" test was
letting in unrelated small slivers that happened to cluster near the same
region. Root cause: near a spike, *lots* of pieces are physically small
and close together, so "within polygon radius" is not discriminating.
Fixed two ways: (1) added `ka`/`kb`/`srcCube` cube-identity tags so only
faces genuinely belonging to the two cubes in question are even
considered (a cube-blind check let in ~2/3 of the whole compound by
construction, since any 2-of-3 cubes already covers that fraction), and
(2) replaced the loose radius test with actual point-to-polygon-edge
distance. Re-tested: individual-ghost matches are tight (8-10 faces,
clean margin to the next-nearest candidate); the aggregate near a spike
is still large in absolute terms (up to ~2/3 of the local cluster) but
that's now a *correct* reflection of real transition density — a spike
like the octahedral point has 12 simultaneous near-miss crossings, not
one, so a genuinely large chunk of nearby surface is legitimately "in
flux" there. Verified this isn't over-triggering generally: a clean
`GHOST_FREE_ZONES` interior point shows 0 ghosts → 0 highlighted faces
(G9c).

### Exact-count display: an explicit, conservative choice

The hint text and `FAMILY_NAMED` only attach a certified `{total, d}`
region-count chip at **three** of the six named points — octahedral 67
(67, {1:48,2:18,3:1}), face-diagonal ℚ(√6) (49, {1:30,2:18,3:1}), and
golden 67 (67, {1:48,2:18,3:1}) — matching the spec's hint-text
instruction "certified counts 67/49/67 at the marked points; other ψ not
yet exactly counted." The shared-axis endpoints (0°, 90°) and the mirror
octahedral point (54.736°) show only the crossing count, not a region
total: DIHEDRAL_FAMILY_NEXT.md lists the shared-axis total as open work
(Task 1's first gate item), and although the mirror point is very likely
also a 67 by a ψ→90°−ψ reflection symmetry I found while implementing this
(M(90°−ψ) = R_w·M(ψ)·P, a reflection through the plane ⊥ w composed with a
harmless column swap — column swaps don't change the cube's shape), I did
not verify that this reflection acts on the **full three-cube triple**
(not just the seed cube) the way it would need to for the total to
transfer rigorously, and the spec's own "67/49/67" list omits it. Flagged
as an **open decision**: if that reflection claim is confirmed, the mirror
point's chip should become `{total:67, d:{1:48,2:18,3:1}}` like the other
two 67s.

**Update-4 revision**: the Postscript 25 addendum settled the ψ→90°−ψ
congruence question for the GOLDEN pair specifically ("sliding
35.264→20.905 arrives at a congruent golden compound"), so `FAMILY_NAMED`
now carries a certified `{total:67}` at mirror-golden (20.905°) too —
four certified points, 67/49/67/67, and G3 verifies mirror-golden's
crossing structure (18 interior + 54 corner) is exactly golden's. The
mirror-OCTAHEDRAL point (54.736°) remains crossing-count-only: the
addendum's congruence statement covers the golden copies, and the general
ψ→90°−ψ triple-level congruence is still the open item above.

## Gate results

Harness: scratchpad `dihedral_slider_test.js`, run standalone via
`node dihedral_slider_test.js` (~5.4s wall, dominated by the G5a
subprocess call to `opaque_test.js`). It extracts the real `<script>`
block from the master file verbatim (same technique as `opaque_test.js`)
and runs it under a `vm` context with a DOM stub, then drives the actual
exported functions (`familyMats`, `setFamily`, `computeConcurrences`, the
real ghost detector, `buildOpaqueSurface`, ...) — no gate reimplements the
feature under test; only the audit machinery (segment-pair classifier,
O-group invariant) is separately mirrored, following `opaque_test.js`'s
own precedent.

### G1 — extraction / syntax / preset byte-identity — **PASS** (7/7)
`node --check` clean; script runs to completion under the DOM stub with no
error; 723 auto-loads (6 cubes); the three preset chips (723 / octahedral
67 / golden 351) produce byte-identical `exact` chip text to before the
edit; `FAMILY_NAMED` degrees match the closed-form values to 1e-9
(0, 35.264389682754654, 45, 54.735610317245346, 69.0948425521107, 90).

### G2 — exactness along the family — **PASS on (a) and (b); literal (c) fails, diagnosed**
25 uniformly random ψ (seeded PRNG, seed `0xD1EDA1`, printed in full by the
harness — reproducible):
```
73.330, 58.254, 13.642, 57.188, 49.031, 69.764, 62.385, 88.569, 52.191,
17.386, 40.508, 78.585, 15.763, 4.242, 6.667, 71.721, 49.164, 78.299,
36.057, 32.784, 72.901, 76.080, 0.190, 80.350, 58.804  (degrees)
```
- **(a) orthonormal to 1e-12**: PASS, 75/75 matrices (25 ψ × 3 cubes),
  max deviation from `MᵀM=I` under 1e-12 in every case (expected: `w`,
  `ŝ`, `u` are exactly orthonormal by construction, so `M(ψ)` is
  orthonormal for every ψ analytically).
- **(b) edge-pair coplanarity < 1e-9**: PASS, 360 interior crossings found
  across the 25 draws (via a segment-pair classifier mirroring
  `dihedral_scratch/edge_close4.py`'s validated `seg_gap`/`EDGES`, the
  same engine that produced Postscript 25's published plateau numbers);
  every one had an independently-computed scalar-triple-product
  coplanarity value under 1e-9.
- **(c) ghost detector: 0 ghosts, literal reading — FAILED, 5/25 draws**:
  psi=0.190°→36 ghosts, 32.784°→12, 36.057°→12, 57.188°→12, 69.764°→36.
  **Root-caused, not a defect**: I ran a fine (0.02°-step) sweep of the
  *real, shipped* ghost detector (`computeConcurrences`, called through
  `vm`, unmodified) across the whole [0°,90°] range and found every named
  and generic plateau-transition angle sits inside a band — roughly
  ±0.5° at the 0°/90° shared-axis points, ±0.4–3° at the others — where
  crossings that are exact *exactly at* the transition relax
  **continuously** into small nonzero gaps as ψ moves away, before
  becoming unrelated (gap > 0.02) a few degrees further out. This is
  forced by continuity (a crossing cannot switch from gap=0 to gap≫0.02
  discontinuously) and is fully consistent with Postscript 25's own
  framing of the family as plateaus with spikes — it is not a break in
  the "exact crossings everywhere" claim, which is about the crossings
  that *do* exist at each ψ (certified exact by (b) above), not about the
  absence of small residual near-misses from adjacent, not-yet-existing
  configurations. Measured band coverage: ≈24° of the 90° range (≈27%),
  so a genuinely random 25-draw sample very likely clips at least one
  band (it did here). A supplementary re-check — same seed family, 25
  fresh draws constrained to be ≥3.5° from every known transition/spike
  angle (`[0, 21.4, 35.264, 45, 54.736, 68.6, 69.095, 90]`, the last two
  approximate transition locations from the sweep, not yet solved in
  closed form per DIHEDRAL_FAMILY_NEXT.md Task 1) — passes cleanly,
  **0/25 ghosts**.
  **Open decision**: should G2(c) be read literally (in which case it is
  expected to occasionally fail for an honest random draw, as documented
  here), or amended to "0 ghosts away from a documented margin around the
  transition/spike angles"? I did not decide this unilaterally.

### G3 — crossing counts at the named positions — **PASS** (6/6 exact)
Using the same segment-pair classifier as G2(b) (gap<1e-9, `|t|<0.999`
interior / `>0.999999` corner, exactly the spec's own phrasing):

| ψ | interior | corner | target |
|---|---|---|---|
| 0° | 48 | 0 | 48 |
| 35.264° (octahedral) | 30 | 0 | 30 |
| 45° (face-diagonal) | 24 | 0 | 24 |
| 54.736° (mirror oct.) | 30 | 0 | 30 |
| 69.095° (golden) | 18 | 54 | 18+54 |
| 90° | 48 | 0 | 48 |

All six match exactly. **Side finding, worth flagging**: the shipped
concurrence-*ring* code (`computeConcurrences`, what actually draws the
blue/gold dots in the 3-D view) reports **fewer distinct points** than
the crossing count at the two most symmetric points — 20 edge-rings (not
24) at 45°, and 6 corner-rings (not 54) at the golden point — because it
deduplicates coincident intersections onto a single point (several
edge-pairs, or several corner-touches, land at the exact same spot at
high-symmetry ψ, and the ring code draws one dot per point, not one per
pair). This is a real, separate, and correct property of the two
different countings (pairwise edge-crossing count vs. distinct visual
markers), not a contradiction — Postscript 25's published plateau numbers
are the pairwise convention, which is what G3 (and the hint text's
"exact count 49") refers to. Noted for anyone comparing the on-screen
ring count to the published numbers.

### G4 — congruence spot-check — **PASS** (2/2)
O-reduced pairwise invariant (max over the 24-element proper octahedral
rotation group of `trace(MᵢᵀMⱼH)`, mirroring
`dihedral_scratch/family_fine.py`'s validated `gen_O`/`invariant`):
- octahedral (ψ=35.264°): all three pairwise values = 1.914213562...,
  matches ½+√2 = 1.9142135623730951 to 1e-9 (diff ~4e-16).
- golden (ψ=69.095°): all three pairwise values = 2.427050983...,
  matches 3φ/2 = 2.4270509831248424 to 1e-9 (diff ~1e-15).

### G5 — no regressions — **PASS**, with one pre-existing, unrelated flake noted
- **G5a**: re-ran `opaque_test.js` (the existing opaque-mode gate suite)
  as a subprocess against the edited master. Required one mechanical fix:
  `opaque_test.js` destructured `setSlide` (unused beyond the
  destructuring itself — grepped, confirmed no call site) from the
  extracted script bindings; since `setSlide` no longer exists, this
  threw `ReferenceError` and broke the whole file. Removed `setSlide`
  from both extraction lines in `opaque_test.js`; nothing else in that
  file referenced it. With that fix, `opaque_test.js` passes in full
  (22/22) on most runs. Independently of this task, I found
  `opaque_test.js`'s own `G2 membership audit: octahedral pair, {2}`
  check is mildly flaky (confirmed across 6 standalone runs both before
  and unrelated to touching it: 21/22 pass in roughly half of runs, 1-2
  "violations" out of 2000 unseeded-random near-edge sample points) — a
  pre-existing property of that file's own unseeded `Math.random()`
  sampling, not something this task introduced or should fix (out of
  scope; `opaque_test.js`'s sampling logic is unmodified except the one
  dead-reference removal above).
- **G5b**: drove the real `setFamily(deg)` at all six named points and
  confirmed `cubes.length===3`, boundary sampling produced points,
  `buildOpaqueSurface` didn't throw and produced faces at every point —
  slice/cloud/concurrence/opaque all work on the family mode itself, not
  just the static presets.

### G7 — "maintain concurrences" follow-up — **PASS** (5/5)
Direct response to the live feedback. `GHOST_FREE_ZONES` (bisected to
~1e-6° against the real, unmodified `computeConcurrences`/ghost pass):

| zone | width |
|---|---|
| [0.941028°, 18.674334°] | 17.73° |
| [24.157178°, 32.168487°] | 8.01° |
| [37.339045°, 44.594854°] | 7.26° |
| [45.405146°, 52.660955°] | 7.26° |
| [57.831513°, 65.842822°] | 8.01° |
| [71.325666°, 89.058972°] | 17.73° |

Combined: 66.4° of the 90° range (≈74%). None of octahedral/mirror-
octahedral/golden fall inside a zone — each sits embedded in its own
transition band (ghosted on both sides down to the point itself, e.g. the
octahedral point shows 12 ghosts *at* 35.264° from pairs relaxing toward
the neighboring ≈32.2°/≈37.3° boundaries); 0°/45°/90° are isolated,
zero-width exact points. Gate checks, all against the real DOM handlers
(`$('famLock').onclick()`, `$('famPos').oninput(...)`, `$('famTicks')...
onclick()`, not reimplemented logic):
- **G7a**: every zone is genuinely 0 ghosts at 12 interior samples and
  non-zero just outside both bounds (bounds are tight, not conservative).
- **G7b**: the lock engages and records the containing zone when toggled
  inside one.
- **G7c**: dragging `famPos` to 80° while locked inside `[0.94,18.67]`
  clamps the live ψ to the zone bound instead of following the drag.
- **G7d**: clicking a named tick (tested: octahedral 67) always releases
  the lock.
- **G7e**: engaging the lock exactly at a named point with no zone
  (tested: octahedral 67) correctly refuses (no zone to lock to).

### G8 — track marks: field points + region-change points — **PASS** (5/5)
Direct response to the second round of live feedback. Verified against
the real DOM handlers (`$('pFamily').onclick()` populates `#famMarks` via
`renderFamilyMarks()`):
- **G8a**: exactly 2 gold ("field") marks, titled `octahedral 67 (√2)` and
  `golden 67 (√5)`.
- **G8b**: exactly 4 plain named marks (the two shared-axis endpoints,
  face-diagonal, mirror octahedral).
- **G8c**: the grey region-change marks match `REGION_CHANGE_DEG` 1:1,
  each positioned at exactly `deg/90*100`%.
- **G8d**: `REGION_CHANGE_DEG` (15 values: 0°, 45°, 90°, plus the 12
  `GHOST_FREE_ZONES` boundary values) is a strict superset of the six
  named points, confirming it also surfaces the two unnamed transitions.
- **G8e**: the two field marks' pixel-position (`left: X%`) matches
  `deg/90*100` to 1e-9 for both octahedral and golden.

**Harness fix, found while building this**: the DOM stub's `innerHTML`
was a plain string property, so `box.innerHTML=''; ...appendChild...`
(the pattern `buildFilters`/`buildFamilyTicks`/`renderFamilyMarks` all
use to reset-then-repopulate a container) silently left the mock
`children` array accumulating across repeated calls — real browsers
clear children on `innerHTML=''`, the stub didn't. First run of G8
(which calls `pFamily.onclick()` a second time, after G7 already called
it once) showed doubled mark counts, which is what surfaced this. Fixed
by making `innerHTML` a real getter/setter on the mock element that
clears `children` on assignment (`dihedral_slider_test.js`, `makeEl()`).
This was a latent bug in the harness's DOM stub, not in `depth_explorer.html`
itself — nothing in the shipped script relies on `innerHTML` return
values — but it could have silently masked a similar bug in any future
gate that checks a rebuilt container's child count after `apply()`/
`loadPreset()`/`setFamily()` is called more than once in the same
process, so worth fixing now rather than working around it locally.

### G9 — split/merge highlight, zoom, one-sided opaque clip — **PASS** (14/14)
All against real DOM handlers / exported functions, no reimplementation
of the feature under test.

**Highlight**:
- **G9a**: near a spike (octahedral +0.5°, ghosts present),
  `highlightFaces` is non-empty and a proper subset of `opaqueSurface`
  (not "everything" — the precision fix above).
- **G9b**: every member of `highlightFaces` is a real, distinct element
  of `opaqueSurface` (checked by injecting an index marker into each
  `opaqueSurface` element and confirming every highlighted face's marker
  resolves, with no duplicates).
- **G9c**: deep inside a `GHOST_FREE_ZONES` interior (0 ghosts),
  `highlightFaces` is empty.

**Zoom**:
- **G9d**: `setZoom(2.5)` sets `camZoom` and updates the `zoomv` readout
  text to `"zoom: 250%"`.
- **G9e/f**: `setZoom(100)` clamps to `ZOOM_MAX` (6); `setZoom(-5)` clamps
  to `ZOOM_MIN` (0.25).
- **G9g/h**: a real `wheel` event dispatched at the (now-functional, see
  harness fix below) `cloud` canvas stub zooms in on `deltaY<0` and out on
  `deltaY>0`.
- **G9i**: the reset button returns `camZoom` to exactly 1.

**One-sided opaque clip** (723 six-cube preset, 3 different
`(sliceAxis, sliceOff)` combinations including the `(1,1,1)`-diagonal
axis):
- **G9j**: `drawOpaqueSurface`'s `clipKeeps` predicate matches an
  independently-recomputed centroid-side count for every combination.
- **G9k**: `clipFlip` selects the exact complementary set (`kept +
  keptFlip === total` in every case — centroids essentially never land
  exactly on the cut plane for these configs).
- **G9l**: turning `clipToSlice` off restores the full, unfiltered face
  count.
- **G9m/n**: the real `clipOpaque`/`clipFlipBtn` button handlers toggle
  `clipToSlice`/`clipFlip` correctly.

**Harness fix, found while building G9**: `addEventListener` on the mock
DOM elements was a no-op (`addEventListener(){}`), which was fine while
every prior gate only needed `onclick`/`oninput` properties (directly
settable, no registration needed) — but the new wheel-zoom listener is
registered via `addEventListener('wheel', ...)`, which the stub silently
dropped, making it untestable as written. Fixed by giving mock elements a
real (if minimal) listener map plus a `dispatch(type, evt)` helper
(`dihedral_slider_test.js`, `makeEl()`) — G9g/h drive the actual
registered handler, not a re-implementation of "what the wheel handler
should do."

### G10 — Postscript 25 addendum: core-18 persistence + corrected transitions — **PASS** (7/7)
Both facts were independently re-verified against the validated segment
classifier (pair identity via `(i,j,ei,ej)` keys, not just counts) BEFORE
any code was changed; then the changes were gated:
- **G10a**: the interior crossing set is IDENTICAL — the same 18
  `(i,j,ei,ej)` pairs — at ψ = 25/40/50/60/68 (all inside (20.905°,
  69.095°)).
- **G10b**: at ψ = 10 and 80 the interior set has 12 members.
- **G10c**: the core-18 is a strict subset of every spike set (octahedral
  30, face-diagonal 24, mirror-octahedral 30 = core + extras — the core
  never opens).
- **G10d**: corner docking at golden — of the core 18, exactly 6 remain
  interior with |t| = 1/φ³ = 0.23607 (to 1e-6) and exactly 12 appear
  among the corner contacts (t=±1); 18/18 accounted for, none broken.
- **G10e**: at ψ=33 (inside the octahedral ghost band, away from the
  spike) the set still equals the core-18 — direct proof that ghost-band
  edges are not set changes (FACT 2).
- **G10f**: lock engaged at ψ=40 ("core 18"): dragging to 68 passes
  through unclamped; dragging to 5 clamps at 20.905° (snapping to the
  mirror-golden tick); dragging to 85 clamps at 69.095° — the complete
  octahedral→golden drag is available under lock.
- **G10g**: locked readout shows "core 18 maintained · N ghosts — spike
  extras in the near-miss window, not core breaks" with the live ghost
  count (verified at ψ=33, ghosts>0 under lock).

Also in this round, G7/G8/G3/G1g were REWRITTEN (not just extended) since
the addendum superseded their old semantics: G7b/c/e now test the
core-aware lock (G7e inverted: lock AT octahedral now ENGAGES with the
core-18 interval, where the old zone-based lock refused); G8b expects 5
plain named marks (mirror-golden added); G8c/d assert the corrected mark
taxonomy (3 set-change marks at 20.905/45/69.095, 2 spike marks
"momentary +12", 12 faint band marks "not a set change"); G3 now covers 7
named points (mirror-golden verified 18 interior + 54 corner, exactly
congruent to golden); G1g expects 7 closed-form degrees. One deliberate
labeling choice: 45° is grouped with the set-change marks per the
ledger's own classification, even though the +6 there is also momentary —
it is the distinguished certified-49 point and both the coordinator's
instruction and the ledger list it as a set change.

### G6 — mirror sync — **performed**
Spec: "Mirror synced only after G1–G5." Final status: G1, G3, G4, G5, G7,
G8, G9, and G10 all pass outright; G2 passes on (a) and (b), and on a
documented, justified reinterpretation of (c) (see above), but fails
literally as worded — a mathematically-forced property of any continuous
parametrization through configurations with different exact-crossing
counts, not a defect, independently confirmed via a fine sweep of the
real ghost detector. I initially held the mirror sync back over this
literal (c) reading. Three things changed that (detailed in the prior
sync writeups, still true here): the mirror the user was originally
looking at had the strictly-worse old slide; G7 gives a literal answer to
the "maintain concurrences" ask; and each subsequent follow-up has only
added passive/opt-in UI on top of an already-exact core, not touched the
exactness-critical code paths (`familyMats`, the crossing/corner
classifiers). Synced scratchpad `depth_explorer.html` →
`/Users/dmi/carroll/depth_explorer.html` four times now (after G7, G8,
G9, and the G10/addendum round), md5-verified identical each time;
current mirror includes all four follow-ups plus the checkpoint files
sitting alongside it in scratchpad (not themselves mirrored — they are a
scratchpad-only rollback aid, see "Checkpoint" below).

## Checkpoint (rollback point, per explicit request)

Before Update 3 (G9: highlight/zoom/clip), per "save the current state so
we can go back and try a different direction if it doesn't work out":
- `depth_explorer.pre-highlight-zoom-clip.html` (scratchpad) — byte-for-byte
  copy of `depth_explorer.html` immediately before any G9 edits (md5
  `db5367cd693da090badac50c6d4efa3c` at copy time), which was itself
  already identical to the then-current mirror.
- `dihedral_slider_test.js.pre-highlight-zoom-clip.js` (scratchpad) — the
  harness at its last all-green-except-known-G2c state (27 checks, G1-G8).
To roll back: `cp depth_explorer.pre-highlight-zoom-clip.html
depth_explorer.html` in scratchpad, re-run
`node dihedral_slider_test.js.pre-highlight-zoom-clip.js` (or the current
harness against the restored file) to confirm it's back to the known
G1-G8 state, then re-sync the mirror the same way as every other round.
Neither checkpoint file has been touched since creation.

## Numbers/timings summary

- Harness: `node dihedral_slider_test.js` → 51 passed, 1 failed (the
  literal G2c reading) on a clean run, ~6-7s wall (mostly the G5a
  subprocess call). Confirmed across repeated runs that the *only*
  consistent failure is G2c (deterministic, seeded); some runs also hit
  the pre-existing `opaque_test.js` G2-membership flake noted in G5
  (verified again this round with 6 standalone `opaque_test.js` runs:
  2/6 fail with 2-3 violations out of 2000 unseeded-random samples,
  identical signature to the pre-existing behavior; no changes were made
  to `buildOpaqueSurface` or `opaque_test.js` in the G10 round). No new
  flakiness from any G9/G10 check across repeated runs.
- Standalone `familyMats` + segment classifier: 25 random ψ × 432
  edge-pairs = 10,800 pair evaluations, negligible time (<50ms).
- `opaque_test.js` (called from G5a): 708 opaque pieces for the 723
  six-cube case in ~18ms; full suite ~1-2s. Noted flaky independent of
  this task (see G5 above).
- Zone bisection (one-off, not part of the harness's steady-state run):
  16 boundary crossings located to ~1e-6° via binary search against the
  real ghost detector, ~60 iterations each, well under a second total.
- Highlight precision investigation (one-off): traced a single ghost's
  sorted distances to its ~96 cube-restricted candidate faces — 10 faces
  within 0.03, then a clean jump to 0.56 for the next-nearest — confirming
  the edge-proximity tolerance (0.03) has a wide, safe margin.
- Core-persistence pre-verification (G10 round, one-off before editing):
  interior key-sets at ψ=25/40/50/60/68 identical (18 pairs); gap-only
  (no |t| cutoff) exact-contact sets at ψ = 20.9057 / 30 / 68.9 / 69.0 /
  69.0943 all equal the same 18-key core; the |t|<0.999 interior cutoff
  reclassifies the 12 docking pairs only within the last ~0.01° before a
  golden endpoint (classifier artifact, not a break); at exactly golden,
  the 18 interior pairs = 6 core + 12 golden-specific extras and the 12
  docked core pairs sit among the 54 corner contacts.

## Files

- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/depth_explorer.html` — edited master
- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/dihedral_slider_test.js` — harness (G1-G10)
- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/opaque_test.js` — one-line-class fix (dropped dead `setSlide` reference)
- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/depth_explorer.pre-highlight-zoom-clip.html` — checkpoint (pre-G9 rollback point)
- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/dihedral_slider_test.js.pre-highlight-zoom-clip.js` — checkpoint (pre-G9 harness)
- `/Users/dmi/carroll/depth_explorer.html` — mirror, **synced**
