# Theorem NP (No Parasites) — DRAFT proof closing gap L1.b, all n

Status: draft (2026-07-17, main session). The argument looks complete
to me; it needs a hardening pass (semialgebraic local-structure
lemmas stated precisely) and an independent read before it is
recorded as proved. Consequences if it holds: max(2) = 13 complete
(with L0 + FIB); d2 <= 18 at n=3 (cluster 1 of the max(3)=67 plan
complete); d_{n-1} <= 6n for ALL n (the l=1 ceiling law, proven).

## Statement

For any n >= 2 unit cubes with common center and any C, every
component U of S_C = {u in S^2 : r_C(u) < min_{i != C} r_i(u)}
contains a face direction of C. Hence #components(S_C) <= 6, and by
the fibration lemma d_{n-1} <= 6n.

Notation: r_i(u) = 1/max_a f_a(u) over cube i's three unsigned face
normals, f_a(u) = |n_a . u|. "Active" at u = attaining the max. On
S_C the bottom envelope b = min_i r_i equals r_C.

## Ingredients

(I1) Single-cube Morse structure (from Theorem A's sandwich + direct
check): r_C has local minima exactly at C's 6 face directions
(value 1), local maxima exactly at its 8 corner directions
(value sqrt3), saddles exactly at its 12 edge directions (value
sqrt2). Euler check 6 - 12 + 8 = 2; M_C = 1/r_C is a perfect Morse
function.

(I2) Equal gradient norms on ties. At any p with tied active faces
(f_a(p) = f_b(p) = f, faces of any cubes), the spherical gradients
satisfy |grad f_a| = |grad f_b| = sqrt(1 - f^2), since
n_a = +-(f p + grad f_a) etc. Nonzero when f < 1.

(I3) All relevant boundary pieces are GREAT-CIRCLE arcs: swap ties
f_a = f_b between cubes and sector boundaries f_a = f_a' within a
cube are both loci u _|_ (n_a -+ n_b). Two distinct great circles
always cross transversally (planes through O meet in a line) — NO
tangencies, hence NO cusps between distinct boundary arcs.

(I4) Sector convexity. Near any p in bd(U), the local piece of S_C is
{v : (g_c - g_x).v >= 0 for all tying cubes x} to first order — an
intersection of half-planes through 0 in T_pS^2, i.e. ONE convex
cone: S_C has exactly one local sector at p, and it belongs to U.
(With C-kinks, the local set only grows: max over C's active faces;
the single-face cone is contained in it.)

## Proof

Let U be a component of S_C and c0 = inf_U r_C, attained on the
compact closure of U.

Case 1: attained at an interior point q0. Then q0 is a local min of
r_C (U open), so by (I1) q0 is a face direction of C. Anchor found.

Case 2: attained only on bd(U), at p. Then r_C(p) = c0 and
r_C = r_x(p) for a nonempty set X of tying cubes; let c be an active
face of C at p and, for x in X, a_x an active face of x. All active
values equal 1/c0 =: f < 1 (f = 1 would force p to be a common face
direction of C and of some x, i.e. n_{a_x} = +-n_c, the degenerate
case handled below). Write g_c, g_x for the spherical gradients of
f_c, f_{a_x} at p; by (I2) all have equal nonzero norm.

Claim: there exists v in T_pS^2 with g_c.v > 0 and
(g_c - g_x).v > 0 for all x in X. If not, by Gordan's theorem there
are lambda_0, lambda_x >= 0, not all zero, with
lambda_0 g_c + sum_x lambda_x (g_c - g_x) = 0, i.e.
(lambda_0 + L) g_c = sum lambda_x g_x with L = sum lambda_x. Taking
norms and using |g_x| = |g_c|: lambda_0 + L <= L, so lambda_0 = 0;
then equality in the triangle inequality with equal norms forces
g_x = g_c for every x with lambda_x > 0. But g_x = g_c together with
f_{a_x}(p) = f_c(p) means the two level caps have the same center:
n_{a_x} = +-n_c (parallel faces). In that case cube x satisfies
r_x <= 1/f_{a_x} = 1/f_c = r_C throughout a neighborhood of p
(x's max is at least its a_x-value), so no point near p has
r_C < r_x — contradicting p in bd(S_C). So the degenerate branch
cannot occur at a boundary point of S_C at all, and the claim holds.

Take such a v. For small t > 0, q_t = exp_p(tv) satisfies, with
strict first-order margins: f_c(q_t) > f_c(p) (so
r_C(q_t) <= 1/f_c(q_t) < c0), and f_c(q_t) > f_{a_x}(q_t) for all
x in X; combined with strict slack at p for every non-tying cube and
every non-active face, this gives r_C(q_t) < r_i(q_t) for all
i != C, i.e. q_t in S_C, with r_C(q_t) < c0.

Absorption: q_t lies in U. The strict cone directions satisfy every
defining inequality of the local sector of S_C at p strictly, so q_t
lies in that sector for small t; by (I4) the sector is unique and
connected, and since p in bd(U), the sector is U's (any connected
subset of S_C meeting U lies in U). By (I3) the sector is an honest
positive-angle sector — the bounding arcs are arcs of distinct great
circles through p, which cannot be mutually tangent, so no cusp
degeneration pinches the sector away from the strict cone.

Then r_C(q_t) < c0 = inf_U r_C with q_t in U — contradiction. So
Case 2 is impossible and every component anchors at a face direction
of C. Distinct components are disjoint, so #components <= 6. QED.

## Remarks

- Corner directions of C cannot lie in S_C (r_C = sqrt3 >= r_x
  everywhere, strict outside corner-corner coincidences), and by (I1)
  those are the only local maxima of r_C: a parasite would have had
  chi <= 0 (only saddles) — the Morse picture that made parasites
  look topologically possible. The proof above never needs this; it
  kills them at the inf point directly.
- Degeneracies are handled INSIDE the argument: parallel-face ties
  self-exclude from bd(S_C); f = 1 boundary points force parallel
  faces; multi-face kinks and multi-cube ties only add constraints
  with the same equal-norm structure, and Gordan's theorem handles
  any number of them.
- The witnesses' own degeneracies (golden corner contacts) are
  boundary events of the TOP diagram, not of S_C interiors; the
  bottom-cluster bound applies to them verbatim.

## What this settles (once hardened)

1. n=2: d1 <= 6 + 6 = 12 (components of T_A = S_B and T_B = S_A),
   d2 <= 1 (L0, convexity), so max(2) = 13 with the witness. FIRST
   COMPLETE MAXIMUM THEOREM, modulo the write-up of L0/FIB.
2. n=3: d2 <= 18 — cluster 1 of the max(3) = 67 plan is COMPLETE.
   Remaining for 67: cluster 2 only (d1 <= 48: L2.a free, L2.b
   annulus obligation, L2.c census — census data extraction running).
3. All n: d_{n-1} <= 6n, previously the empirically-exact l=1
   ceiling law, now proven.

## Hardening checklist (before recording as a theorem)

- [ ] Precise statement of the local sector structure of a
      semialgebraic open set at a boundary point, with (I3) ruling
      out cusps (finitely many great circles through p; local
      components of S_C near p are the connected components of the
      complement of their arcs where the defining inequalities hold;
      convexity of the defining cone gives uniqueness).
- [ ] The exp_p(tv) strictness argument written with explicit
      first-order margins (compact subcone, uniform epsilon).
- [ ] FIB written carefully (fiber = single interval; tie boundaries).
- [ ] L0 written (one line, convexity).
- [ ] Independent read / adversarial check, then ledger postscript.
