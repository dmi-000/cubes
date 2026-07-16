# OPAQUE_SPEC — opaque-surface rendering mode for depth_explorer.html

Task for the implementing agent (Sonnet). Self-contained; read this file plus the
viewer source. Do not read other project docs unless something here is ambiguous.

## Files

- **Master (edit this)**: `depth_explorer.html`
- **Mirror (copy master here when done)**: `depth_explorer.html`
- **Report (create)**: `opaque_report.md` — what you built, how the
  gates were verified, piece counts and timings for the presets.
- **Test harness (create)**: scratchpad `opaque_test.js` — node script exercising the
  geometry functions (see Gates).
- Never edit `six_cube_search_results.md` or any file listed as validated/read-only
  in README.md. Do not publish artifacts; the main session does that.

## Context

depth_explorer.html is a self-contained (no external resources — strict CSP) canvas-2D
viewer for compounds of n rotated unit cubes ([−1,1]³, so side 2). It already has:
rotation matrices per cube (`mats`), a 3D→2D projection `rot(p)` (view rotation ∘
optional (1,1,1) pre-rotation), a depth-cue helper `cue(z)` (z = view-space depth,
range ≈ ±2.4), a depth palette, per-depth filter chips, per-cube checkboxes, display
modes for the region-wall view (point cloud / wireframe / concurrence rings / ghost
rings), presets (723 record, octahedral √2 pair, golden triple), the 67↔67 slide
slider, and spin toggles. Read the source before changing anything.

"Depth" of a point = number of cubes containing it. The depth function changes by
exactly ±1 across a cube face.

## Feature

Add an **Opaque** display option to the Region-walls view: render, as opaque shaded
polygons, the boundary surface of the body

    B = { p : (number of SELECTED cubes containing p) ∈ [dmin, dmax] }

where the selected cubes come from the existing cube checkboxes and [dmin, dmax]
from the existing depth chips (the set of checked depths; if the checked set is
non-contiguous, treat membership as "depth ∈ checked set" — the boundary test below
handles that uniformly). Unselected cubes contribute nothing (neither to depth nor
to cutting planes).

### Geometry (exact plane arithmetic, float evaluation is fine)

For each selected cube k and each of its 6 faces:
1. Start from the face square (a quad in the plane `n·p = 1` in cube-k coordinates).
2. Clip/split it by the traces of all 6 face planes of every *other selected* cube
   (recursive convex-polygon splitting by lines in the face plane; keep pieces with
   area > 1e-9).
3. For each piece, compute depth at `centroid ± ε·normal` (ε ≈ 1e-4) by direct
   point-in-cube tests over the selected cubes.
4. The piece is a boundary polygon of B iff exactly one of the two sides is in the
   depth set. Keep it, tagged with the inside-side depth (for color).

Factor this as a pure function, e.g.
`buildOpaqueSurface(mats, selected, depthSet) -> [{poly:[[x,y,z],...], depth, normal}]`
so the node test harness can call it standalone (either by duplicating it in the
harness via extraction, or by structuring the script so the function has no DOM
dependencies and can be `eval`'d from the extracted <script> — your choice, but the
harness must exercise the *same* code text that ships in the HTML, not a re-write).

### Rendering

- Painter's algorithm: sort boundary polygons by view-space centroid z each frame
  (geometry is view-independent; recompute geometry only when mats/filters/slide-t
  change, re-sort every frame).
- Fill color: existing depth palette keyed by the piece's inside depth; flat shading
  = palette color scaled by `0.55 + 0.45·|N·L|` with a fixed light direction, then
  by the existing `cue(z)`. Stroke each polygon with a subtle darker edge (~1px).
- Piece counts appear in the existing counts line (e.g. "· 214 faces").
- Must coexist with the slide slider (recompute on t change; target ≤ ~150 ms for
  the 6-cube preset — report actual timing) and with both spin modes.
- Do not break any existing mode; Opaque is one more option in the same control the
  other wall-display modes use (match the existing UI pattern — if modes are radio
  chips, add a chip; if a select, add an option).

## Hard gates (all must pass before you report success; put results in the report)

G1. **Single cube**: one cube selected, depth set {1} → exactly 6 quads, total area
    24 (side-2 cube). Exercise via the node harness.
G2. **Membership audit**: for each preset (octahedral pair with depth set {2}; golden
    triple with {3}; golden triple with {1,2,3}; 723 six-cube with {2,...}), sample
    ≥ 2000 random output-polygon points at ±ε along the normal: every polygon must
    separate in-set from out-of-set. Zero violations allowed.
G3. **Ray audit (no missing faces)**: cast ≥ 2000 random rays through the origin
    region; the sorted crossing parameters of the polygon set must toggle membership
    consistently with direct point-in-B tests at midpoints between crossings (skip
    rays passing within 1e-6 of any polygon edge). Zero violations allowed.
G4. **No regressions**: extract the <script> and `node --check` it; load the page
    logic far enough to confirm the existing modes' counts on the 723 preset are
    unchanged (the preset histogram chips must still read the same).
G5. Mirror synced (`diff` master vs mirror empty) only after G1–G4 pass.

## Working style

Run everything yourself, detached where long-running; do not park on monitors. If a
gate fails, fix and re-run; only report when gates pass or you are genuinely blocked.
Keep code style matched to the existing file (plain JS, no frameworks). Comments only
for invariants (e.g. why ε has its value, why sorting is per-frame but geometry
cached).
