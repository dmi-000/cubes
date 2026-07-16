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

## 7. THE GENERAL LAW (2026-07-13) — supersedes the per-case ceilings

All bottom-diagram cell counts obey one formula (Postscript 19 evidence):

    cells(B_l) = C(l,n) = (12l−6)n − 2(l²−1)      [conjecture, attained
    exactly for l ≤ 4 at n = 2..7 across ~1M configs; zero violations]

equivalently, via trivalence (E = 3V/2, all measured censuses):

    V_l(n) = (24l−12)n − 4l²      [matches measured 68/200/324 at n=6]

So T1 is now: prove Σ_l has exactly V_l(n) trivalent vertices generically.
T2 unchanged (degeneracy only merges). The old targets are the cases
l=1,2,3 at n=6 (36, 102, 164). The l=1 case reduces to the no-shoulder
lemma: m(û) = 1/max|n·û| has ONLY the 6n face-center minima (two-form
case = ridge, provable; crux = no triple-form sub-unit peak).
Top layer: d1 ≤ C(n−1,n) = 10n² − 14n, attained by golden for n ≤ 5.

## 8. Proof shape (Platonic-elimination framing, per Chris Cole 2026-07-13)

The cap proof is a Platonic-style elimination + Euler:
  (i)  enumerate a-priori local vertex types of the swap curve Σ_l
       (rank-triple points, swap×own-edge crossings, tangencies, higher
       coincidences);
  (ii) ELIMINATE all but trivalent rank-triple points using the two
       rigid constraints: each cube's normal triad is ORTHONORMAL and
       all offsets = 1 (the analog of "angle sum < 360°"). Measured
       censuses show own-edge and tangency vertices contribute ZERO
       generically — the proof must forbid them, not just observe;
  (iii) count surviving triple points: per-cube Morse data (6 face
       centers, 12 edges, 8 corners; χ=2) is the rigid local unit ⇒
       census linear in n: V_l(n) = (24l−12)n − 4l²;
  (iv) Euler on S² with trivalence: cells = 2 + V/2 = C(l,n).
Generic stratum only; walls need the T2 merging/semicontinuity half.
Smallest complete instance: l=1, n=2 (six normals, two triads) — by
itself proves max(2) = 13. Fine-graining note: all candidate boundaries
lie in the fine arrangement of great circles (n_f − n_g)·û = 0; B_l is
a coarsening of it, so eliminate in the fine grid, count survivors.

## 9. Fine-grain-then-examine (Chris Cole): scope and the certification route

- GLOBAL finiteness holds with NO family restriction: the count is
  determined by signs of finitely many polynomials in the rotation
  entries, so config space splits into finitely many chambers (count
  constant on each). The maximum is attained on a chamber. In principle
  the exam is finite.
- Practically the chamber count is astronomical (~10^60+ at n=6 by
  sign-pattern bounds), so effective enumeration NEEDS a fixed family
  (Chris's caveat). Executed instances: the 1-param algebraic slide
  (126 walls solved exactly, every chamber examined — the family max
  CERTIFIED); the sphere census (fine-grain S² by great circles).
- Upgrade path: certify the low-knob blueprint families by Gröbner/CAD
  chamber enumeration (turns "no blueprint beat 723 at coverage" into
  proven per-family maxima).
- Reduce-then-certify route to global proofs: prove E1 ⇒ n=6 max
  reduces to n=5 classes ≥388 ⇒ recursion downward; base case n=2 is a
  3-DIMENSIONAL space — full chamber enumeration (CAD) is feasible NOW
  and would give an unconditional computer-assisted proof of
  max(2) = 13 with no lemma needed. n=3 (6-dim) borderline with
  symmetry reduction.

## 10. THEOREM A (proven, 2026-07-13): the anchor lemma — no shoulder critical points, any n

STATEMENT. For any n rotations, let M(û) = max over the 3n face normals
n_i of |n_i·û| on S². Every local maximum of M has value 1 and occurs at
û = ±n_i. Equivalently: the radial envelope m = 1/M (distance to the
nearest cube boundary) has local minima ONLY at the 6n face-center
directions, all at value 1.

PROOF (sandwich). Let û0 be a local max of M, and let n_i be any ACTIVE
normal (|n_i·û0| = M(û0)). Near û0: |n_i·û| ≤ M(û) ≤ M(û0) = |n_i·û0|,
so û0 is a local maximum of the single function f_i(û) = |n_i·û|. But
f_i = |cos∠(û, n_i)| is strictly decreasing in the angle on (0, π/2)
and has local maxima only at û = ±n_i, with value 1. So M(û0) = 1 and
û0 = ±n_i. ∎

REMARKS. (1) The same sandwich applied inside one cube shows t_k's local
minima are exactly its 6 face centers. (2) This kills the "three-form
peak" crux of §3/§8 — it was a phantom: a peak of a max forces EACH
active piece to peak, which single forms cannot do below value 1. No
case analysis, no orthonormality even needed (any unit normals!).
(3) Numerically corroborated: exactly 6n envelope maxima, all at value
1, in every sampled configuration (and the earlier zero-shoulder
censuses).

RESIDUAL GAP for the cap C(1,n) = 6n (cells of the bottom-1 diagram):
Theorem A anchors every cell whose envelope-inf is attained in its
INTERIOR. Still to exclude: "parasite" cells — components of
{t_k < others} whose inf of t_k is attained only on the boundary tie
curve. Local analysis does not forbid them (boundary-min geometry is
consistent); empirically none exist. Two routes: (a) the Euler/census
count (§8), (b) Morse route: #components of {t_j − t_k > 0} ≤ #local
maxima of t_j − t_k — bound the difference's maxima.

## 11. CAD feasibility verdict (Chris's unrestricted fine-graining, n=2)

Probe: the 24 vertex-on-plane walls reduce to 12 distinct quartics in
the quaternion chart; Wolfram's CylindricalDecomposition on just FOUR
of them completes in ~4 min with a 4.6-million-leaf cell tree. Full
V-F + edge-edge wall set: infeasible on this hardware (doubly-
exponential growth). Conclusion: even at n=2 the UNRESTRICTED chamber
exam is impractical; certification must go family-by-family (few-knob
blueprints), or through Theorem A + census. Chris's "only works if we
fix a family" — quantified.

## 12. Four theorems around the dihedral family (proved 2026-07-16)

Notation. s_hat = (1,1,1)/sqrt3. Family gauge (Postscript 26): with the
first cube's frame as reference, cube k of a family configuration is
Rel(theta_k, psi) applied to [-1,1]^3, where Rel(theta, psi) is the
rotation by angle theta about the axis n(psi) = (sin psi, cos psi, 0).
(Equivalently the world frame M(theta,psi) = [cos psi w + sin psi s_hat |
-sin psi w + cos psi s_hat | u(theta)], w = s_hat x u; the two are related
by M(0,psi)^T M(theta,psi) = Rel(theta,psi), verified symbolically.)

### Theorem M (mirror symmetry).
For every n, every phase tuple {theta_k}, and every psi:
config({theta_k}, psi) is congruent (by an improper isometry) to
config({-theta_k}, 90deg - psi). In particular region counts and full
depth profiles agree.

Proof. Let P be the coordinate swap x<->y (orthogonal, det = -1, a
symmetry of the cube: P[-1,1]^3 = [-1,1]^3). P n(psi) = (cos psi,
sin psi, 0) = n(90-psi). Conjugating a rotation by an improper
orthogonal map reverses the sense: P Rel(theta,psi) P^-1 =
Rel(-theta, 90-psi). Hence for each k,
P (Rel(theta_k,psi) [-1,1]^3) = Rel(-theta_k, 90-psi) P[-1,1]^3
= Rel(-theta_k, 90-psi) [-1,1]^3. So P maps the first compound onto the
second; isometries preserve the region complex. QED.

Corollaries. (a) For chains theta_k = k a, negating a is undone by the
relabeling k -> n+1-k (a constant phase shift = global rotation), so
chain(a, psi) ~ chain(a, 90-psi) — the psi<->90-psi degeneracy observed
in every sweep (Postscript 26) is now proven for all n. (b) The C3 slice
{0,120,240} is invariant under negation as a set, so the n=3 staircase
(Postscript 25 addendum 3) is exactly symmetric about psi=45. All sweep
domains can be rigorously halved.

### Theorem P (90-degree periodicity).
config({theta_k}, psi + 90deg) = config({theta_k}, psi) — the SAME
compound, not merely congruent.

Proof (world frame). col1(psi+90) = col2(psi), col2(psi+90) = -col1(psi),
col3 unchanged; so M(theta, psi+90) = M(theta,psi) K with
K = [e2|-e1|e3] = rot(e3, 90deg), a rotation symmetry of the cube. Each
cube is unchanged as a set. QED. (So the family's true parameter space is
psi in [0,45] after Theorem M.)

### Theorem F (the coincidence identity).
For every psi, every phase tuple, and every cube pair (j,k) of a family
configuration, all three SAME-CLASS edge-line coincidence conditions hold
identically: for each axis class, the designated edge lines of cube j and
cube k are exactly coplanar (hence, being non-parallel for theta_j !=
theta_k mod 90, intersecting).

Proof. Work in the world frame; write c = cos psi, s = sin psi,
u_k = u(theta_k), w_k = s_hat x u_k.
(z-class) Cube k's four u-edges have centers +-col1 +- col2, i.e.
heights (dot with s_hat) in {+-(s+c), +-(c-s)} — the SAME height set for
every cube, since col1.s_hat = s, col2.s_hat = c independently of theta.
Two edges of equal height lie in one plane perpendicular to s_hat; any
two non-parallel coplanar lines meet. This proves the z-z coincidences.
(y-class) For the representative pair: cube j edge with center
M_j(-1,0,1) = -col1_j + u_j, direction col2_j; cube k edge center
M_k(-1,0,-1) = -col1_k - u_k, direction col2_k. The coplanarity form is
f = [(-col1_k - u_k) - (-col1_j + u_j)] . (col2_j x col2_k).
Expand col2 = -s w + c s_hat and use, for any two unit horizontals,
w_j x s_hat = ... the only nonzero products are
w_j x w_k = sin(D) s_hat, s_hat x w_k = -u_k, w_j x s_hat = u_j,
u_j.w_k = -sin D, w_j.u_k = +sin D, u.w own-cube = 0, all heights of
w, u zero (D = theta_k - theta_j). Then
col2_j x col2_k = s^2 sin(D) s_hat - s c (u_j - u_k)   ... (i)
Delta-center  = -c (w_k - w_j) - (u_j + u_k)            ... (ii)
Dot (i).(ii): the s_hat term kills (all of (ii) is horizontal); the
remaining term is s c^2 (w_k - w_j).(u_j - u_k)
= s c^2 [ w_k.u_j - w_j.u_j(=0) - w_k.u_k(=0) + w_j.u_k ]
= s c^2 [ -sin D + sin D ] = 0 identically. The other three y-pairs
follow by composing with the central symmetry of either cube (edge ->
antipodal edge, an isometry of both cubes). This proves y-y.
(x-class) By Theorem P the same compound arises at psi - 90deg with the
cube frames relabeled by K = rot(e3,90), which maps x-edges to y-edges;
the x-x identity at psi is therefore the y-y identity at psi - 90,
already proven for all psi. QED.

Remark. Segment-INTERIOR validity (|t|<=1) is what varies with
(theta, psi) and produces the plateau/spike structure; Theorem F says the
line coincidences never break. The core-18 persistence claim of
Postscript 25 addendum 1 additionally needs |t(psi)| < 1 on the open
golden-to-golden interval — the t's are explicit algebraic functions, so
this is provable by Sturm-sequence certification (listed below), not yet
done.

### Theorem R (rational-invariant obstruction) and the conditional
irrationality of the n=3 maximum.
If all quaternions of a configuration are rational, then for every cube
pair the O-reduced invariant mu(i,j) = max over H in O of
trace(R_i^T R_j H) is rational (each trace is a rational number; O is
the 24 integer rotation matrices). mu is invariant under congruence of
compounds: a global isometry G cancels in R_i^T R_j (improper G reduces
to proper since -I is a cube symmetry), and per-cube relabelings H_k
permute the double coset over which the max is taken. The octahedral 67
has mu = 1/2 + sqrt2 and the golden 67 has mu = 3 phi/2 (both exact,
Postscript 25); both are irrational. Hence NO rational configuration is
congruent to either known 67 compound.

Corollary. If the two known compounds are the only maximizers of n=3 (up
to congruence) — supported by their isolation (Postscript 17) and every
search to date, but unproven — then the n=3 maximum REQUIRES irrational
coordinates, while n=2 (max 13, attained by integer pairs inside the 183
record) and every current record at n>=4 are rational. n=3 would be the
unique irrational level of the tower.

### Provable next (methods identified, real work):
1. Certified staircase: the addendum-3 plateau values are constant on
   their intervals — isolate all combinatorial-event roots (finitely
   many polynomials in sin psi) via Sturm sequences / exact resultants;
   turns sampled counts into interval theorems.
2. Core-18 segment bounds: |t(psi)| < 1 on (20.905, 69.095) for the 18
   explicit algebraic crossing parameters, equality exactly at the
   endpoints with the docking values t = +-1, +-1/phi^3.
3. The pair-curve identity (all four cross-class extras share one zero
   curve): the four conditions are exchanged by the pair's dihedral
   symmetries — reduce to one, then the curve is the regular zero set
   through the octahedral point (gradient nonvanishing verified).
4. max(3) = 67 itself: still the two lemmas of Postscript 23 (trivalent
   census + parasite exclusion) — unchanged, the real prize.
