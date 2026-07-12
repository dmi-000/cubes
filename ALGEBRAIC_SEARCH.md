# Algebraic search for region-rich cube compounds

Status (2026-07-12): working, validated end-to-end. Two solvers:
1-parameter exact wall-mapping (`algebraic_demo.wl`) and multi-constraint
GroebnerBasis solving (`algebraic_groebner.wl`, `algebraic_groebner2.wl`).
Both feed `algebraic_bridge.py`, which counts the emitted configs with the
validated engine. Files: `algebraic_search.wl` (algebra layer), the two
demos, the two groebner drivers. Runs on the local `wolframscript` (the
license warning it prints is non-fatal — GroebnerBasis/Solve work).

**GroebnerBasis solve (implemented, validated, productive).** Unknown
cube A = qmat[{1,x,y,z}]; impose corner-coincidence equations with fixed
cubes; GroebnerBasis-eliminate + Solve for {x,y,z} → exact solutions.
Validation: constraining A to fix the (1,1,1) corner + one lattice corner
recovers exactly the C3 corner-stabilizer {identity, ±120° about (1,1,1)}.
Findings from it (a real scientific result, not just plumbing):
  - **Concurrence multiplicity has a SWEET SPOT.** Forcing a 12-fold
    concurrence (four cubes sharing one corner) gives only 393 — WORSE
    than the record. 723's 9-fold is near-optimal; over-concentrating
    incidence at one point merges away too many regions (the T2 / deep-
    ceiling direction).
  - **Welding A to TWO cubes at general corners** (two separate 6-fold
    coincidences, the 723-type spread) gives 689 across 26 exact
    solutions, with **d1 = 224 — a new depth-1 high, above the record's
    210** — but nets below 723 because the deep layers drop (d3=142,
    d4=88). So corner-welding is a strong depth-1 lever capped by the
    deep-count ceilings.
The solver did not beat 723, but it maps the incidence/count tradeoff
exactly and finds configs a numeric grid would not land on.

## Premise (validated, not assumed)

Record configs sit at HIGH-MULTIPLICITY POINT incidences, not edges:
- The 723 record has two **9-fold plane concurrences** — points where 9
  face-planes meet. Random configs top out at multiplicity 4.
- Those 9-fold points are **three cubes sharing a corner**: the free
  triple (cubes 3,4,5) all map the (1,1,1) corner to one common point
  (and antipodally the (−1,−1,−1) corner), so they share the whole
  (1,1,1) axis. "k cubes share corner p" ⟺ "they differ by rotations
  fixing p" ⟺ rotations about the axis through p. The algebra thus
  confirms the shared-axis families ARE the corner-sharing configs.
- **Edge concurrences are absent**: no line is shared by ≥3 planes
  (max line-multiplicity 2, identical to random) — a 3-plane edge needs
  3 coplanar normals, which neither generic nor symmetric configs hit.
  So the search targets coincident CORNERS/points, never coplanar edges.

## Method

1. **Parameterize a family over Q.** Cube = R_base · cay(axis, s), where
   `cay` is the Cayley form of a rotation about an INTEGER axis by a
   rational parameter s — rational in s (angle 2·arctan(s|axis|)), which
   keeps everything over Q so Solve/GroebnerBasis stay exact and the
   result is countable by the rational engine. s=0 → identity.
2. **Impose incidences as polynomial equations.** A wall (where the count
   can jump) is where an extra face-plane passes through a fixed vertex:
   n_face(s)·v = 1, one polynomial in the parameters per (vertex, face).
   Higher-value targets: force k planes through one unknown point x
   (k-fold concurrence) — the equations n_i(params)·x = c_i in
   (params, x); eliminate x by GroebnerBasis to get conditions on the
   family parameters. Corner coincidence R_i·corner = R_j·corner is the
   cleanest such system (creates a shared-corner = shared-axis wall).
3. **Solve exactly.** `Solve`/`GroebnerBasis` over Q; keep rational roots
   (→ rational configs, countable directly) — algebraic roots are real
   too and route to the field engines (qtower.py etc.), deferred.
4. **Count.** `algebraic_bridge.py` runs each emitted integer-quaternion
   config through `./cube_regions`; matrices → integer quats via the
   rational trace formula `mat2quat`.

## Worked example (algebraic_demo.wl)

The 723 record = two triples about (1,1,1). Fix the C₃ core; rotate the
free triple TOGETHER about (1,1,1) by rational Cayley parameter s (the
symmetry-preserving "slide"). Solve n_free-face(s)·v = 1 over the 564
core vertices → **126 exact rational walls**. Counting walls + interval
midpoints: s=0 reproduces 723 (anchor ✓); the spectrum peaks at 723
(plateau s∈{−1,0,1}) and falls to 693/687 elsewhere. So 723 is an exact
local max along this line — no numeric grid needed, the walls are exact.

## How to extend (the real hunt)

- **Multi-parameter / Gröbner.** Give the free triple independent angles
  (or a free base), impose 2+ simultaneous incidences (e.g. a free cube's
  corner coinciding with a core cube's corner, a NEW inter-triple 9-fold
  point), and `GroebnerBasis`-eliminate to solve the high-codimension
  system. These are the points a numeric grid provably misses (the
  399→705 coverage gap). Each solution → count.
- **Other axes / cores.** Repeat about (0,0,1), (1,1,0); larger shared
  corners (4 cubes at a point).
- **Algebraic (irrational) walls.** Keep non-rational real roots and
  count with the ℚ(√d)/tower engines (qtower.py, slide3_q2.py) — this is
  where a wall the rational search can never reach would show up.

## Honest limits

v1 does the 1-parameter exact wall map; the multi-constraint Gröbner
solve (the part that could beat the numeric search) is specified above
but not yet built. Not every wall raises the count — the engine, not the
algebra, decides which are rich. Wolfram Export numericizes the s-labels
in the JSON (cosmetic); the quaternions it writes are exact integers.
