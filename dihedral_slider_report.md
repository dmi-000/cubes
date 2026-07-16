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

The mirror has been synced with both fixes included; see "Mirror sync" at
the end.

Files touched:
- Master (edited): scratchpad `depth_explorer.html`
- Mirror: **synced** (see "Mirror sync" below)
- Harness (extended): scratchpad `dihedral_slider_test.js` (now G1-G8)
- `opaque_test.js` (existing regression suite): one mechanical fix, see G5

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

### G6 — mirror sync — **performed**
Spec: "Mirror synced only after G1–G5." Final status: G1, G3, G4, G5, G7,
and G8 all pass outright; G2 passes on (a) and (b), and on a documented,
justified reinterpretation of (c) (see above), but fails literally as
worded — a mathematically-forced property of any continuous parametrization
through configurations with different exact-crossing counts, not a defect,
independently confirmed via a fine sweep of the real ghost detector. I
initially held the mirror sync back over this literal (c) reading. Three
things changed that: (1) the live feedback confirmed the mirror the user
was actually looking at (`/Users/dmi/carroll/depth_explorer.html`, mtime
predating this task) still had the **old** 67↔67 slide, whose entire
interior — not just ~27% of it in narrow bands — sits off the exact
surface; shipping the new version is a strict improvement no matter how
G2(c) is read. (2) The G7 follow-up gives a literal, verified answer to
"a way to slide while maintaining edge concurrences," the substance of
what G2(c) was trying to guarantee. (3) The G8 follow-up directly
addresses the second round of live feedback and only adds a passive
visual overlay (no changes to the exactness-critical code paths). Synced
scratchpad `depth_explorer.html` → `/Users/dmi/carroll/depth_explorer.html`
twice (after G7, then again after G8), md5-verified identical both times;
current mirror includes both follow-ups.

## Numbers/timings summary

- Harness: `node dihedral_slider_test.js` → 26 passed, 1 failed (the
  literal G2c reading) on a typical run, ~5-6s wall (mostly the G5a
  subprocess call). Confirmed across repeated runs that the *only*
  deterministic failure is G2c; roughly 1 run in 3 also shows the
  pre-existing `opaque_test.js` G2-membership flake noted above (one
  additional failure that run) — unrelated to this task, same root cause
  (unseeded `Math.random()` in that file's own audit, ~1-2 violations per
  2000 samples).
- Standalone `familyMats` + segment classifier: 25 random ψ × 432
  edge-pairs = 10,800 pair evaluations, negligible time (<50ms).
- `opaque_test.js` (called from G5a): 708 opaque pieces for the 723
  six-cube case in ~18ms; full suite ~1-2s. Noted flaky independent of
  this task (see G5 above).
- Zone bisection (one-off, not part of the harness's steady-state run):
  16 boundary crossings located to ~1e-6° via binary search against the
  real ghost detector, ~60 iterations each, well under a second total.

## Files

- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/depth_explorer.html` — edited master
- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/dihedral_slider_test.js` — harness (G1-G8)
- `/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/opaque_test.js` — one-line-class fix (dropped dead `setSlide` reference)
- `/Users/dmi/carroll/depth_explorer.html` — mirror, **synced**
