# INCREMENT_BOUND_SPEC — the repaired one-cube increment bound

Supersedes the failed attempt of Postscript 53 (`increment_bound.py`, kept as
documentation of that failure). Deliverable: `increment_bound2.py`.

## 0. What is being proved

The increment identity is exact: for a compound S of n cubes and any cube j,

    T = count(S \ {j}) + Delta_j.

E1 (Postscript 18) bounds Delta_j by a MEASURED constant (336 at n=6). The
goal is a bound DERIVED from the geometry of the configuration.

### The chain

Write S_j = S with cube j removed. Let G be the region adjacency graph of S
INCLUDING the outside (label 0) region as a node, and let G_j be its spanning
subgraph keeping only the "bit j" edges — those joining two regions whose
labels differ exactly in bit j. (Every adjacency edge changes exactly one bit;
that is an established structural gate of `region_adjacency.py`.)

Forgetting cube j merges precisely the regions joined by bit-j edges, and
merging is transitive, so the regions of S_j are the connected components of
G_j. Hence, with N = |V(G)| = T + 1,

    Delta_j = N - #components(G_j)                                       (I)
            <= |E(G_j)|                                                  (II)
            <= W_j                                                       (III)
            <= K_j                                                       (IV)
            <= B_j                                                       (V)

where
  W_j = number of WALLS on dC_j (connected components of the shared boundary
        between two regions that lie on dC_j); >= |E(G_j)| because the simple
        graph counts a region pair once however many walls it has,
  K_j = number of connected components of dC_j minus the other cubes'
        boundaries — the "mask cells" of dC_j, each of which is a single wall
        or a piece of the outer boundary,
  B_j = number of cells of the arrangement cut on dC_j by the other cubes'
        face PLANES (which refines the mask cells, since d(other cube) is
        contained in the union of its face planes).

(I) is an identity; (II) is "a graph on N nodes with c components has at least
N - c edges"; (III), (IV), (V) are refinements. B_j is computable from the
configuration alone by Euler's formula — that is the deliverable.

### The formula for B_j

Work in cube j's own frame (apply R_j^T to everything), so C_j = [-1,1]^3 and
dC_j is the standard cube surface, topologically a sphere.

Each other-cube face plane P meets dC_j in a CLOSED CURVE when it cuts the
interior. The union of these curves is a graph embedded on a sphere. For any
graph embedded on the sphere with c connected components, V vertices, E edges,
Euler gives F = 1 + c + E - V, and with E = sum_v deg(v)/2,

    B_j = 1 + c + SUM_v ( deg(v)/2 - 1 ),                                (*)

the sum over vertices v of the arrangement, deg(v) = 2 * (number of trace
curves through v). Isolated closed curves (no vertices) contribute only
through c.

Checks of (*): one circle -> 2; two disjoint circles -> 3; two circles crossing
twice -> 4; three great circles -> 8.

### Why the earlier attempt failed

`increment_bound.py` used F = 2 + V, which assumes every face is a disk (c = 1
and no isolated curves), and it counted a vertex only when the intersection
line of two planes met the OPEN interior of C_j. Both are wrong at
degeneracies, and the records are degenerate. In the n=2 13-pair
(quaternions (1,0,0,0) and (0,1,1,1)) all twelve of A's edge lines are TANGENT
to dB — min |R p|_inf = 1 exactly, never < 1 — so the old code found V = 0 and
reported a bound of 2 against Delta = 12. Counting the tangential vertices
(two triple points at (1,1,1), (-1,-1,-1); six double points (1,-1,0),
(1,0,-1), (-1,1,0), (-1,0,1), (0,1,-1), (0,-1,1)) formula (*) gives
1 + 1 + (2*2 + 6*1) = 12 = Delta, exactly tight.

## 1. Algorithm for B_j (exact rational arithmetic ONLY)

INVARIANT: `fractions.Fraction` throughout; no float ever decides a
comparison. A wrong verdict on "does this line touch the cube" silently
weakens or breaks the bound, and the whole point of the exercise is the
degenerate cases where such a verdict is delicate.

Given quaternions q_0..q_{n-1} and an index j:

1. R_k = rotation matrix of q_k (exact, denominator = |q|^2; copy `mat()` from
   `increment_bound.py`). Change frame: M_k = R_j^T R_k.

2. Planes. For every k != j, every axis a in 0..2 and sign s in {+1,-1}: the
   plane is m . y = s with m = column a of M_k. Store each as a canonical
   exact tuple (normalise so the first nonzero component of (m, -s) is
   positive, and scale to primitive integers if you like — the requirement is
   that two identical planes get identical keys, so duplicate face planes
   shared by two cubes are counted ONCE).

3. Classify each plane by L = sum |m_i| (the support function of [-1,1]^3):
     L > |s|  -> cuts the interior, trace is a closed curve. KEEP.
     L == |s| -> tangent: touches dC_j in a face, an edge or a corner. DROP,
                 but count it in a `degenerate_tangent` tally that the report
                 prints. (Dropping is safe for an upper bound: a tangency set
                 is a point, a segment or a face; a point or an arc does not
                 disconnect a sphere, and a whole face lies inside one mask
                 cell already bounded by the other planes. A configuration
                 with a nonzero tally is FLAGGED, not silently trusted.)
     L < |s|  -> misses the cube. DROP.

4. Vertices. For every unordered pair of kept planes (P, P'):
   - Their intersection is a line unless the normals are parallel (then skip;
     parallel distinct planes never meet).
   - Clip the line to the closed box [-1,1]^3 exactly (standard slab clipping
     with Fractions, tracking t_lo <= t_hi). If empty, skip.
   - The points of the line ON dC_j are the clipped endpoints t_lo and t_hi
     (they satisfy |y|_inf = 1 by construction); if t_lo == t_hi the line
     touches at a single point, which is ONE vertex.
   - DEGENERACY TO DETECT: if the whole clipped segment lies on dC_j (i.e.
     some coordinate is constantly +-1 along it — the line lies in a face
     plane of C_j), the two traces share an ARC, formula (*) does not apply,
     and the run must report `arc_overlap` for that (config, j) rather than
     claim a bound.
   - Collect the endpoint(s) as exact rational 3-tuples.

5. Dedupe vertices exactly. For each distinct vertex v, deg(v) = 2 * #{kept
   planes P : m_P . v == s_P}. (Count the planes through v, not the pairs —
   three planes through one point give deg 6, not deg 12.)

6. c = number of connected components of the curve union: union-find over the
   kept planes, joining P and P' whenever both pass through a common vertex.
   A kept plane through no vertex is its own component.

7. B_j = 1 + c + sum_v (deg(v)/2 - 1).

## 2. Gates (all must be run; report every number)

G1 — n=2 degenerate. quats (1,0,0,0), (0,1,1,1). For j=0 and j=1: Delta_j = 12
   (T = 13, single cube = 1). REQUIRE B_j = 12 exactly, with c = 1, two
   vertices of degree 6 and six of degree 4, at the eight points listed in
   section 0. This is the case the old bound got wrong; if it does not
   reproduce, stop and report rather than adjusting the gate.

G2 — the four configurations of `increment_bound.py` CONFIGS (727 record, 723,
   393 at n=5, 183 at n=4), every j: print a table
   config, j, T, S_j, Delta_j, B_j, slack = B_j/Delta_j, verdict.
   REQUIRE B_j >= Delta_j for all 21 rows. Region counts come from
   `./cube_regions_n --quats` exactly as the old script does.

G3 — generic agreement. Take a few random rational quaternion pairs with small
   entries (n=2) whose edge lines meet dC_j transversally (no tangency, no
   triple points). REQUIRE B_j == 2 + V, where V is the count produced by the
   old `increment_bound.py` predicate — the corrected formula must reduce to
   the old one exactly when the configuration is generic. Print how many of
   the sampled pairs were generic; if none are, widen the sample.

G4 — vertex self-check. Every vertex emitted must satisfy both its plane
   equations exactly and have |v|_inf == 1 exactly. Assert, do not print.

## 3. Report

Write `increment_bound2_report.md` containing: the gate results, the G2 table,
the observed slack distribution (min/median/max of B_j/Delta_j), the tally of
degenerate tangent planes and any arc_overlap flags per configuration, and one
paragraph on whether the bound is tight (slack 1.00) anywhere besides G1.

Do NOT edit `LEDGER.md` — the ledger is written only by the
main session. Do not modify `increment_bound.py`.
