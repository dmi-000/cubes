# DIHEDRAL_SLIDER_SPEC — replace the 67↔67 slide with the dihedral-family slider

Task for the implementing agent (Sonnet). Self-contained. Background (only if
needed): Postscript 25 in six_cube_search_results.md, DIHEDRAL_FAMILY_NEXT.md.

## Files

- **Master (edit)**: `depth_explorer.html`
- **Mirror (sync when gates pass)**: `depth_explorer.html`
- **Report (create)**: `dihedral_slider_report.md`
- **Test harness (create/extend)**: scratchpad `dihedral_slider_test.js`
- Never edit six_cube_search_results.md or validated files; do not publish
  artifacts (main session does).

## What changes

The viewer currently has a "67 ↔ 67 slide" group (preset button `pSlide`,
slider `slidePos`, `slideMats(t)` built from constants S_OCT / C3 / SLIDE_AXIS
/ SLIDE_DELTA). That path connects the two 67-region triples but leaves the
exact-coincidence family, which is why interior positions show dashed "ghost"
near-crossings. **Replace it** with a slider along the dihedral family, where
every position has exact edge crossings.

### The family (exact closed form)

Constants: ŝ = (1,1,1)/√3, u = (1,−1,0)/√2, w = ŝ×u = (1,1,−2)/√6,
C = 120° rotation about (1,1,1) = [[0,0,1],[1,0,0],[0,1,0]].

Seed matrix, ψ in radians:
```
M(ψ) columns = [ cosψ·w + sinψ·ŝ , −sinψ·w + cosψ·ŝ , u ]
```
Cubes: { M(ψ), C·M(ψ), C²·M(ψ) } (same convention as the current slideMats).

Slider range ψ ∈ [0°, 90°]. Named positions (show tick marks / snap points
with labels; snapping within ~0.3° is fine, position readout shows ψ in
degrees):

| ψ | exact value | what it is |
|---|---|---|
| 0° | 0 | shared-axis compound (all cubes share the (1,1,1) face axis), 48 crossings |
| 35.264° | arcsin(1/√3) | **octahedral 67** (30 crossings) |
| 45° | π/4 | face-diagonal compound, ℚ(√6), **exact count 49** = {30,18,1}, 24 crossings |
| 54.736° | arctan(√2) | mirror octahedral 67 (30 crossings) |
| 69.095° | arctan(φ²), φ golden ratio | **golden 67** (18 interior crossings + 54 corner contacts) |
| 90° | π/2 | shared-axis compound again, 48 crossings |

### UI

- Replace the `pSlide` preset + `slideGrp` block: same interaction pattern
  (mini button loads the family mode, range slider drives ψ, live matrix
  update, works with all display modes incl. opaque). Label the group
  "Dihedral family — exact crossings everywhere".
- Explanatory hint text (adapt freely, keep short): this family rotates one
  cube ±120° about an axis in its own face plane, tilting that axis from a
  face axis (ψ=0) through the octahedral 67, the face-diagonal compound
  (exact count 49), the mirror octahedral, and the golden 67 (tan ψ = φ²);
  edge crossings stay EXACT at every ψ — unlike the old slide, which left
  the family and opened the dashed ghost gaps. Mention: certified counts
  67 / 49 / 67 at the marked points; other ψ not yet exactly counted.
- Keep the ghost-ring machinery itself (it is generic); on this family it
  should find (near-)zero ghosts — that's a validation, not a bug.
- Remove now-dead slide constants/functions only if nothing else uses them;
  if the concurrence/ghost code paths reference slideMats, refactor
  minimally. `git`-less project: preserve a copy of the removed block in a
  comment is NOT wanted — the old constants remain documented in the ledger.

## Hard gates (report all; all must pass)

G1. `node --check` on the extracted script; script runs under the DOM stub;
    the three preset chips (723 / octahedral 67 / golden 351) byte-identical.
G2. Exactness along the family: in the harness, for 25 uniformly random ψ,
    build the three matrices and verify (a) each is orthonormal to 1e-12,
    (b) every edge-pair line-coplanarity value that the ring code classifies
    as a crossing is < 1e-9, (c) ghost detector reports 0 ghosts with gap in
    (1e-6, 0.02).
G3. Crossing counts at the named positions (segment-interior, |t|<0.999,
    same tolerance the ring code uses): ψ=0° → 48, arcsin(1/√3) → 30,
    45° → 24, arctan(√2) → 30, arctan(φ²) → 18 interior (plus corner
    contacts — count and report them; expected 54), 90° → 48.
G4. Congruence spot-check: at ψ=arcsin(1/√3) the compound's pairwise
    O-reduced invariant equals ½+√2 (1.914213562) to 1e-9; at arctan(φ²)
    it equals 3φ/2 (2.427050983).
G5. No regressions in other modes (opaque/wireframe/concurrence/slice work
    on the presets; reuse the existing opaque_test.js checks if convenient).
G6. Mirror synced only after G1–G5.

## Working style

Run everything yourself; don't park on monitors; report when gates pass with
numbers, timings, and any decisions the spec left open.
