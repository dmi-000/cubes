# Toward proofs of C4 (depth-3 <= 164) and C5 (depth-4 <= 102)

Working notes, 2026-07-10. Status: reduction of C4/C5/C6 to two concrete
claims (T1 combinatorial census, T2 semicontinuity), with the supporting
framework proved and the crux identified. Not yet a proof.

## 1. Framework (proved earlier, restated)

Radial functions: cube k has t_k(u) = 1/||R_k^T u||_inf on the direction
sphere S^2; cube k's ray-segment in direction u is [0, t_k(u)].
RADIAL ESCAPE LEMMA (proved): regions of containment-label S are in
bijection with connected components of
    U_S = { u in S^2 : min_{i in S} t_i(u) > max_{j notin S} t_j(u) }.
Hence depth-d total = number of cells of the "bottom-(6-d)-set diagram"
B_l (l = 6-d): the partition of S^2 by WHICH l-subset forms the l lowest
values of (t_1..t_6).
  depth 6 <-> B_0: one cell (S^2 connected): d6 = 1, a THEOREM.
  depth 5 <-> B_1 (which cube is lowest):      conjectured <= 36.
  depth 4 <-> B_2 (which pair is bottom-2):    conjectured <= 102 (C5).
  depth 3 <-> B_3 (which triple is bottom-3):  conjectured <= 164 (C4).
  depth 2, 1 <-> B_4, B_5 (top-2, top-1): the falsified/growing side.

## 2. Morse structure of one cube's radial function

t_k = 1/||R_k^T u||_inf is piecewise-projective with the combinatorics of
the cube: on S^2 it has exactly
  6 local minima  (face-center directions, value exactly 1 = inradius),
  12 saddles      (edge directions, value sqrt2),
  8 local maxima  (corner directions, value exactly sqrt3).
Check: chi(S^2) = 6 - 12 + 8 = 2. All minima share value 1; all maxima
share value sqrt3. Anchor facts (generic configs):
  - every B_1 cell of cube k around one of its face centers is nonempty
    (t_j >= 1 with equality only at j's OWN face centers) -> B_1 >= 36... 
    NO: >= 6 anchored cells per cube, but cells can MERGE around an edge
    of k (observed: 34, 32) -> only B_1 <= 36 is conjectural, >= is false
    as stated; anchored cells exist but need not be distinct.
  - dually every top-1 (depth-1) cell count >= 8 per cube (corner
    anchors, t_j <= sqrt3 with equality only at own corners) -- matches
    data (per-cube depth-1 always >= 8; observed 12..26).

## 3. The crux asymmetry

Bottom diagrams are capped (never exceed 36/102/164 in 117,422 exact
configs); top diagrams grow (118/214 and rising). Both sides have
equal-valued anchor sets (36 minima at exactly 1; 48 maxima at exactly
sqrt3). The asymmetry to explain: EXTRA cells (cells containing no
anchor) are abundant on the top side and absent(?) on the bottom side.
An extra bottom-1 cell requires a region where some t_k is strictly
lowest yet contains no local minimum of t_k -- a "shoulder" cell. Extra
top cells (shoulder cells of the max side) demonstrably exist. Why
shoulders exist above but (apparently) not below is the geometric heart;
candidate mechanism: near the floor, every t_j is convex-ish upward from
its face anchors (values near 1 force proximity to SOME face center of
SOME cube), so the sublevel sets {m < 1+eps} are exactly 36 disks -- the
bottom diagram at low levels is anchored; cells of B_1 that avoid all 36
disks would need the lowest function everywhere above 1+eps, where the
"who is lowest" boundaries are the same swap curves whose complexity is
budgeted by T1 below.

## 4. The reduction

Boundary structure: the boundary of B_l is the (l, l+1)-SWAP CURVE
Sigma_l = { u : l-th lowest value = (l+1)-th lowest value }. All
equalities t_i = t_j happen where two active FACE functions are equal,
i.e. on great circles (n_f - n_g) . u = 0 (all faces have offset 1).
Additionally each t_k changes active face across cube k's own 12
edge-direction arcs (also great circles, (n_f - n_f') . u = 0 within one
cube). So every B_l is a spherical map whose edges are great-circle arcs
drawn from an explicit finite generating set.

Euler on S^2: cells(B_l) = 2 - V_l + E_l where V_l, E_l are the vertex
and edge counts of Sigma_l (plus isolated-component corrections). So:

  T1 (generic census): for configurations in the generic stratum, the
  local vertex types of Sigma_l (triple equalities of ranked values;
  swap-curve crossings with own-edge arcs; tangencies excluded
  generically) occur in combinatorially DETERMINED numbers, forcing
    E_1 - V_1 = 34   (=> B_1 = 36)
    E_2 - V_2 = 100  (=> B_2 = 102)
    E_3 - V_3 = 162  (=> B_3 = 164).
  Evidence: B_2 = 102 in 82.6% of random configs (it IS the generic
  value); per-pair distributions vary while the SUM is conserved --
  exactly the signature of an Euler-characteristic identity rather than
  per-pair geometry.

  T2 (semicontinuity below): leaving the generic stratum can only MERGE
  bottom-diagram cells, never create more than the generic count.
  Evidence: all observed deviations go DOWN (34/32 at B_1; 86..100 at
  B_2; structured configs lower still: six6 family B_1 = 24). Warning:
  the analogous statement is FALSE for top diagrams and for pair counts
  (walls RAISED the pair count 4 -> 13), so T2 must use something
  special about the bottom side -- presumably the same floor-anchoring
  as in section 3. This is the hard half.

C6 (d5 <= 36) = T1+T2 for l=1; C5 = for l=2; C4 = for l=3. d6 = 1 done.

## 5. What would falsify the approach

A certified config with B_2 > 102 or B_3 > 164 (the campaign found none
in 117k, but the same was true of 623 in 7k); or an observed generic
config whose Sigma_l vertex census differs from T1's prediction (the
numerical check below); or a bottom-shoulder cell in any diagram.

## 6. Delegable numerical checks (specified for the agent)

For several explicit configs (records 635/631, generic mid seeds, a
sub-36 seed, six6-type): build the spherical arrangement numerically
from the quats (great-circle generating set is explicit), extract
Sigma_1, Sigma_2, Sigma_3, count V, E, F exactly enough (the arcs are
great circles; predicates are sign(det) on rational data -- can be done
in exact arithmetic), and verify: F matches the per_label-derived depth
counts (validation); E - V matches 34/100/162 on generic configs;
identify the vertex-type census (how many rank-triple points vs
own-edge crossings) -- the census IS the content of T1; check for
bottom-shoulder cells (cells of B_1 containing no face-center
direction; B_2 cells containing no minimum of the 2nd-lowest envelope).
