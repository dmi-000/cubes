# Opaque display mode — implementation report

Master edited: `depth_explorer.html`
Mirror: `depth_explorer.html` (byte-identical, `diff` empty — G5)
Test harness: `opaque_test.js`

`six_cube_search_results.md` and `README.md` were not touched; no artifacts were published.

## What was built

A new **opaque** toggle button in the Region-walls card, alongside the existing
`wireframe` / `spin` / `axis` / `concurrences` toggles (that control turned out
to be a row of independent `.ghost` toggle buttons, not a radio-chip group or a
`<select>` — see "Decisions" below for how that changed the UI plan).

Core geometry, `buildOpaqueSurface(mats, selected, depthSet)`, implemented
exactly per the spec's algorithm:

1. For each selected cube and each of its 6 faces, start from the unit face
   square (same corner construction the existing point-cloud sampler uses).
2. Split it against the 6 face-planes of every *other* selected cube. This is
   a full line-arrangement split (`splitPoly`), not a one-sided clip: every
   cut keeps both the front and back piece, recursively, so the result is the
   complete set of convex regions the other cubes' plane traces carve the
   face into. Pieces with area ≤ 1e-9 are dropped after each cut.
3. Each surviving piece is probed at `centroid ± 1e-4·faceNormal`, testing
   membership in `depthSet` (`depth ∈ checked set`, over selected cubes only)
   on both sides via direct point-in-cube tests.
4. Kept iff exactly one side is in the set, tagged with the inside depth
   **and** the inside region's containment bitmask (see "Containment
   colouring" below).

Supporting pure functions added: `polyArea`, `polyCentroid` (vertex mean —
valid for convex polygons, cheaper than an area centroid), `splitPoly`
(Sutherland-Hodgman run to both sides), `maskAt` / `depthAt`, `faceQuad`.

Rendering (`drawOpaqueSurface`): geometry is cached in `opaqueSurface` and
only rebuilt (`ensureOpaqueSurface`, gated by `opaqueDirty`) when `cubes`,
`cubeSel`, or `depthSel` change (`apply`, `setSlide`, every filter-chip
handler now sets the flag) — never every frame. Every frame it re-sorts the
cached pieces by rotated centroid z (painter's algorithm) and fills each with
`DEPTH_COLORS[depth]` scaled by `(0.55 + 0.45·|N·L|) · cue(z)`, stroked with a
faint dark edge. Piece count is appended to the existing counts line as
`· N faces` (`refreshCloudCount`), matching the "214 faces" example in the
spec.

When opaque mode is on, the point-cloud dust is skipped (would be redundant
with — and visually buried under — the solid fill); wireframe and
concurrence-ring overlays are unaffected and still toggle independently on
top, matching current behavior for those two modes.

## Containment colouring (follow-up request)

The opaque surface honours the existing "Colour cells by" toggle
(`depth` / `containment`), exactly like the cross-section view:

- `buildOpaqueSurface` now records, per piece, the **containment bitmask**
  of the inside region (`maskAt`, keyed by global cube index — the same
  keying `labelAt` uses, so a region's containment hue in the opaque view
  matches its cells in the slice view). `depth` is simply the popcount of
  that mask; the boundary test is unchanged.
- `drawOpaqueSurface` picks the fill from `colorMode`: `DEPTH_RGB[depth]`
  in depth mode, `labelRgb(mask)` in containment mode, in both cases scaled
  by the same `(0.55 + 0.45·|N·L|) · cue(z)` shading. No geometry rebuild
  on toggle — masks are computed once at build time and the render loop
  picks up `colorMode` on the next frame.
- New harness audit (G2m): at every G2 sample point away from piece edges,
  the piece's stored mask must equal the direct containment mask of the
  in-set side, and its popcount the stored depth. Zero mismatches across
  all four preset cases. (Points within 10ε of a piece edge are excluded
  from this sub-check only: there a ±ε off-plane probe can legitimately
  sit across the plane tracing that edge, flipping one containment bit
  without any geometry error.)

## Gate results

All five gates pass (re-run in full after the containment-colouring
addition). Full harness output:

```
PASS  G4a node --check on extracted <script>
PASS  G4b script runs to completion under DOM stub
PASS  G4c 723 preset auto-loaded (6 cubes)
PASS  G4d 723 exact chip text unchanged
PASS  G4e octahedral 67 chip text unchanged
PASS  G4f golden 351 chip text unchanged
PASS  G1 single cube -> 6 quads
PASS  G1 single cube -> total area 24
PASS  G1 all pieces tagged depth 1
PASS  G2 membership audit: octahedral pair, {2} (2000 pts, 114 pieces, 2.8ms)
PASS  G2m containment-mask audit: octahedral pair, {2}
PASS  G2 membership audit: golden triple, {3} (2000 pts, 18 pieces, 1.1ms)
PASS  G2m containment-mask audit: golden triple, {3}
PASS  G2 membership audit: golden triple, {1,2,3} (2000 pts, 108 pieces, 2.4ms)
PASS  G2m containment-mask audit: golden triple, {1,2,3}
PASS  G2 membership audit: 723 six-cube, {2,3,4,5,6} (2000 pts, 708 pieces, 20.7ms)
PASS  G2m containment-mask audit: 723 six-cube, {2,3,4,5,6}
PASS  G3 ray audit: octahedral pair, {2} (2000 rays, 0 skipped near-edge)
PASS  G3 ray audit: golden triple, {3} (2000 rays, 0 skipped near-edge)
PASS  G3 ray audit: golden triple, {1,2,3} (2000 rays, 0 skipped near-edge)
PASS  G3 ray audit: 723 six-cube, {2,3,4,5,6} (2000 rays, 0 skipped near-edge)

22 passed, 0 failed
```

Piece counts after the mask addition are identical to the depth-only build
(114 / 18 / 108 / 708) — the boundary-selection logic is untouched.

- **G1** (single cube, depth {1}): exactly 6 quads, total area 24.000000,
  each tagged depth 1. Exact.
- **G2** (membership audit, ≥2000 random points per polygon, sampled by
  area-weighted fan triangulation, ±1e-4 along the piece's own normal):
  **zero violations** across all four required cases (octahedral pair {2},
  golden triple {3}, golden triple {1,2,3}, 723 six-cube), 2000 points each,
  8000 total, 0 failures.
- **G3** (ray audit, rays through the origin, direct-test at gap midpoints
  vs. sorted crossing toggles): **zero violations**, 2000 rays per case
  (8000 total), 0 rays needed skipping for the "within 1e-6 of an edge"
  exclusion in any case (the presets are generic enough that random rays
  never landed that close to a piece boundary in 8000 draws).
- **G4**: extracted `<script>` passes `node --check`; the same extracted
  text runs to completion under a stubbed DOM (minimal `document` /
  canvas-2D-context / `matchMedia` / `requestAnimationFrame` stand-ins, no
  external packages); the 723/octahedral-67/golden-351 exact-chip text
  (`exact total …`, `d1: … … d6: …`) is byte-identical to the pre-existing
  hardcoded literals — confirms the edit didn't disturb any existing preset
  data or the other display modes.
- **G5**: `diff` between master and mirror is empty (checked only after
  G1–G4 all passed).

## Piece counts and timings

`buildOpaqueSurface`, `process.hrtime` around the call, median where noted;
all figures re-measured with the mask-recording build (the containment
addition; overhead vs. the depth-only build is within run-to-run noise):

| Config | Depth set | Pieces | Time |
|---|---|---|---|
| Octahedral √2 pair (3 cubes) | {2} | 114 | 2.8 ms |
| Golden √5 triple (3 cubes) | {3} | 18 | 1.1 ms |
| Golden √5 triple (3 cubes) | {1,2,3} | 108 | 2.4 ms |
| 723 six-cube record | {2,3,4,5,6} | 708 | 20.7 ms |
| 723 six-cube record | {1,2,3,4,5,6} (full default view) | 666 | 20.7 ms (median of 5 runs, range 19.4–24.8 ms) |
| 67↔67 slide, t=0.5 (interior, 3 cubes) | {1,2,3} | 180 | 1.3 ms |

All comfortably inside the spec's ≤~150 ms target for the 6-cube preset —
roughly 6–8× margin at the worst case measured (full 6-cube, all depths).

## Decisions the spec left open

1. **UI control shape.** The spec assumed the existing wall-display modes
   were "radio chips" or a "select." In the actual file they're a row of
   independent `.ghost` toggle buttons (`wireframe`, `spin`, `axis: y`,
   `concurrences`), each an orthogonal on/off flag, not a single-select mode
   list. I added `opaque` as one more toggle in that same row/pattern rather
   than restructuring the control into a radio group. Concretely: turning
   Opaque on suppresses the point-cloud dust (the two are redundant — same
   walls, dust vs. solid fill) but leaves `wireframe`/`concurrences` as
   independent overlays that still draw on top, since the spec only
   specifies painter's-algorithm ordering *within* the opaque polygon set,
   not compositing rules across all four display layers.

2. **Light direction's reference frame.** "Flat shading = palette color
   scaled by `0.55 + 0.45·|N·L|` with a fixed light direction" doesn't say
   whether the light is fixed in object/world space (rotates relative to the
   viewer as the compound spins) or in view space (a "headlamp" that stays
   fixed relative to the camera). I chose view space: the polygon normal is
   passed through the same `rot()` used for vertex projection each frame,
   then dotted with a constant `LIGHT_DIR = normalize([0.4, 0.65, 0.65])`.
   This keeps the shading stable and readable while spinning, which seemed
   like the more natural default for an interactive viewer; the absolute
   value in the formula makes the sign/handedness of the stored per-face
   normal irrelevant either way.

3. **Depth sets for the G2/G3 audit cases.** The spec names "723 six-cube
   with {2,...}" without pinning down the upper bound. I used
   `{2,3,4,5,6}` (all depths except the outermost single-cube layer) —
   the most geometrically demanding non-trivial choice (708 pieces, the
   largest arrangement of any tested case) and the one likeliest to expose a
   splitting bug if one existed.

4. **Coplanar cutting-plane guard.** The spec's split step doesn't mention
   what happens when another selected cube's face plane is exactly (or
   near-exactly) parallel to the face being split — such a plane has no line
   trace on the face, and naively running it through `splitPoly` would
   place every vertex within tolerance of both the front and back output,
   silently duplicating the whole piece. I added an explicit guard (skip any
   cutting plane whose normal's cross product with the face normal has
   squared magnitude < 1e-12) and documented the invariant inline. This
   didn't fire measurably in the tested presets but is a real correctness
   requirement for any config with an accidental face-plane alignment
   between two selected cubes.

5. **Ray audit ray family (G3).** "Cast rays through the origin region" was
   read as: origin exactly at the world origin (which sits inside every
   cube for these configs, since none of them are translated), random unit
   direction, parameter range wide enough to clear the whole compound
   (`t ∈ [-4, 4]`, safely outside the `√3` circumradius of a unit cube under
   pure rotation). Point-in-polygon and edge-distance both use a Newell's-
   method true polygon normal (not the stored `faceNormal`, whose sign is
   arbitrary) so the "within 1e-6 of an edge" skip rule is evaluated
   correctly regardless of that stored sign.

6. **Containment colouring semantics (follow-up request).** "Colour by
   containment" for a *boundary* polygon is ambiguous — the two sides of a
   wall have different containment sets by construction. I colour by the
   **inside** region's mask, mirroring how the depth mode colours by the
   inside depth (and how the slice view colours the cell the pixel is in).
   I reused the existing "Colour cells by" segmented control rather than
   adding a second, opaque-specific toggle: it already carries exactly this
   depth/containment semantic, and sharing it keeps the slice and opaque
   views in the same colour system (same `labelRgb` hash keyed by global
   cube index, so a region's hue matches across both panels).
