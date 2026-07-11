# Spec: C++ exact region counter (`cube_regions.cpp`)

Port of `certify_six.exact_count_config` + the seed chain of `mt_sim.py`
to a single-file C++17 program using pure integer arithmetic. Target:
~100x speedup over the Python/Fraction pipeline (6 s -> <100 ms per
configuration) to enable mass falsification searches and exact
hill-climbing.

## Number system: integer homogeneous coordinates, __int128

Everything is exact integer arithmetic; no rationals, no GMP.

- Configuration = 6 integer quaternions (w,x,y,z), |components| <= 512
  (after gcd reduction), from the validated seed chain (below) or given
  explicitly (hill-climbing moves).
- For quaternion q: n = w^2+x^2+y^2+z^2 <= 4*512^2 ~ 2^20.
  Rotation matrix = M/n with M integer (entries |.| <= n).
- Cube k's face planes: column j of M/n is the unit normal; the plane
  (column_j / n) . x = +-1 clears to INTEGER plane
      a x + b y + c z = +-n,      |a|,|b|,|c|,|n| <= 2^20.
  Represent planes as integer 4-vectors (a,b,c,d) meaning a x+b y+c z = d.
  Box planes: x = +-4 etc.
- VERTICES: never chain interpolations (overflow + non-canonical).
  Every vertex of every cell is the intersection of exactly 3 planes of
  the arrangement (36 cube planes + 6 box planes; generic configs only).
  Each cell vertex carries its defining plane triple; its coordinates are
  computed by Cramer's rule as homogeneous integers (X,Y,Z,W):
      W = det3(plane rows a,b,c),  X,Y,Z = the RHS-substituted dets.
  |det3| <= 6 * (2^20)^3 ~ 2^62.6  -> fits int128 comfortably.
  Canonicalize: divide (X,Y,Z,W) by gcd, force W > 0. This canonical
  4-tuple is the vertex identity for hashing/equality (exact dedup).
- PREDICATES: side-of-plane sign = sign(a X + b Y + c Z - d W),
  magnitude <= 4 * 2^20 * 2^63 ~ 2^85 -> int128 safe. All comparisons
  are integer signs; zero = exactly on plane (handle like Python port).
- Overflow budget: quaternion scale 512 is a hard cap in this design
  (document in --help). At N=512 worst cases sit ~40 bits below int128
  limits.

## Algorithm: port `exact_count_config` from certify_six.py EXACTLY

Same steps, same order, same asserts (they carry the correctness):
1. bounding box cell [-4,4]^3 (6 faces as quad loops).
2. clip every cell by each of the 36 planes in order (both closed halves;
   points with sign 0 belong to both; a cell splits only if it has
   strictly + and strictly - vertices). Faces as vertex loops; cut
   vertices from plane triples: (face plane, edge's other plane, cutting
   plane). The edge's other plane = the unique non-face plane shared by
   the two endpoint triples (assert uniqueness; generic configs).
   Cap face construction: chain the per-face zero-point pairs into a
   cycle (port the Python logic, including consecutive-duplicate dedup
   and the >=3-vertex checks).
3. label each cell by testing its centroid against every cube's 3 plane
   pairs. Centroid of vertex set in homogeneous coords: sum of
   (X_i/W_i) -> use exact rational sum with int128 after reducing, or
   simpler: pick ANY interior point exactly: average of two vertices of
   the cell that are not... (careful: pairs of vertices may have their
   midpoint on a face for degenerate cells) -- safest is the true
   centroid: accumulate X_i * prod(W_j)/W_i style with int128 risk ->
   RECOMMENDED: compute centroid with long-double first as a filter and
   verify the label with exact integer predicates at a rational point
   built as the average of all vertices over a common denominator using
   128-bit only if the config keeps W's small after reduction; if that
   overflows, fall back to: exact average of the two endpoint vertices
   of any interior segment... SIMPLEST SAFE CHOICE (do this): centroid
   test per plane via summed sign: sign( sum_i (a X_i + b Y_i + c Z_i
   - d W_i) * sgn?? ) -- NO. Just do: for each cell keep one vertex
   triple-free interior point computed as the exact vertex-average with
   arbitrary-size big integers ONLY at this step (a tiny bigint helper
   for 256-bit add/mul/compare, or __int128 with pre-reduction; vertex
   count per cell <= ~30). A 256-bit fixed-width helper (four uint64
   limbs, signed) is ~80 lines and removes all doubt. Label predicates
   at the centroid then use 256-bit muls (plane coeffs 2^20 x centroid
   2^~130 fine).
4. facet identity: (plane id, sorted set of canonical vertex keys);
   assert every facet group has exactly 2 cells.
5. coincident-plane owners classes (port as-is; generic random configs
   have singleton classes, but keep the logic + asserts for structured
   inputs).
6. phantom vs real facet at the facet centroid (same 256-bit centroid
   trick), union-find merge on phantom with label-equality assert; real
   facets must flip exactly the owning cubes' bits (assert).
7. outputs: total bounded count, per-depth histogram, per-label counts
   (the per-subset breakdown), all to one JSON line on stdout.

## Seed chain (must be bit-identical to numpy/scipy)

Port `mt_sim.py` (validated against scipy on 66 seeds):
- MT19937, init_genrand(seed) (numpy legacy seeding for seed < 2^32);
- rk_double = ((u32>>5)*67108864 + (u32>>6)) / 2^53;
- Marsaglia polar gaussian with the has_gauss cache, returns f*x2 first;
- per cube: 4 gaussians in order (x,y,z,w); normalize; flip sign so the
  largest-|component| is positive; ints = round(c*512); gcd-reduce.
- Uses C libm log/sqrt like numpy; the oracle validation below is the
  authoritative check.

## CLI

  cube_regions --seed S            # one config from the seed chain
  cube_regions --seeds A B         # range [A,B)
  cube_regions --quats 'w,x,y,z;...' (6 groups)   # explicit config
  cube_regions --selftest          # run validation suite

One JSON line per config: {"seed": S or null, "quats": [[...]x6],
"bounded": n, "by_depth": {...}, "per_label": {...}, "us": microseconds}.

## Validation gates (HARD requirements, in order, before any campaign)

1. `--selftest`: axial-6 with rational Pythagorean twists about z
   (quats for rotation about z by angle t: (w,0,0,z) ~ integer pairs
   from half-angle -- construct from the 6 twist matrices... simplest:
   pass the 6 explicit quaternions for cos/sin pairs (1,0,1),(24,7,25),
   (15,8,17),(4,3,5),(21,20,29),(5,12,13): half-angle quats are
   (c', 0, 0, s') with c'^2, s'^2 = (1 +- a/c)/2 -- NOT integer in
   general! Instead run this case via --quats with the DOUBLED-angle
   trick: a rotation by t about z has quaternion (cos t/2, 0,0, sin t/2);
   for Pythagorean (a,b,c) the HALF angle is not rational, so instead
   choose quaternions directly: q = (p, 0, 0, r) integer gives rotation
   about z with cos t = (p^2-r^2)/(p^2+r^2), sin t = 2pr/(p^2+r^2) --
   Pythagorean automatically! Use 6 distinct (p,r) pairs, e.g. (1,0),
   (5,1),(4,1),(3,1),(5,2),(2,1); the counter must return 121 exactly
   (the proven axial law), with depth histogram 24,24,24,24,24,1.
2. Oracle match: for seeds 0..199, counts AND depth histograms must
   equal `exact_search_results.jsonl` / the seed 0-39 batch values
   exactly (the jsonl is ground truth from the validated Python
   pipeline). ANY mismatch = stop, debug, do not proceed.
3. Timing report: expect <= ~100 ms/config single-threaded.

## Parallel + reproducible campaign driver (`run_campaign.py`)

- Workers = OS processes running `cube_regions --seeds A B` on disjoint
  ranges (seeds are independent and deterministic: same seed -> same
  config -> same count, any parallelism). Shard outputs
  `campaign_shard_<i>.jsonl`; a merge step sorts/dedups by seed.
- Phase A (mass falsification): seeds 3000..~500000 as budget allows,
  8 workers. Flag records and any ceiling violation:
  depth-1 > 112, depth-2 > 208, depth-3 > 164, depth-4 > 102,
  depth-5 != 36, depth-6 != 1, total > 623.
- Phase B (exact hill-climbing): from top-20 configs, moves = add
  {-2,-1,1,2} to one component of one quaternion, re-gcd (skip if any
  |component| > 512); objective = total (also runs maximizing depth-1
  alone and depth-2 alone). Greedy with random restarts, all moves
  logged as explicit quats (reproducible without the seed chain).
  Every improvement re-verified... (it IS exact; just log it).
- Phase C: breakdown analysis of everything found (per-cube depth-1,
  per-pair depth-2 distributions; is 22 the per-cube max? can two
  22-cubes coexist with high totals? do depth-3/4 sums exceed 164/102
  anywhere?). Append findings to six_cube_search_results.md.

## Conjectures under attack (state explicitly in the final report)

C1 total <= 623;  C2 depth-1 <= 112;  C3 depth-2 <= 208;
C4 depth-3 <= 164;  C5 depth-4 <= 102;  C6 depth-5 = 36, depth-6 = 1
(all for generic rationalized configurations, quaternion scale 512).
A single certified counterexample falsifies; sustained failure to
falsify across ~10^5 seeds + hill-climbing is reported as evidence, not
proof.
