#!/usr/bin/env wolframscript
(* Algebraic search for region-rich cube compounds.

   Working principles: ALGEBRAIC_SEARCH.md.

   Premise (validated in ALGEBRAIC_SEARCH.md): record configs sit at
   HIGH-MULTIPLICITY plane incidences.  The 723 record has two 9-fold
   concurrences = two triples of cubes each sharing the (1,1,1) corner,
   i.e. each triple is a rotation-about-(1,1,1) family.  "k cubes share a
   corner p" <=> "they differ by rotations fixing p" <=> rotations about
   the axis through p.  So the search space is: cubes built as
   R_base . Rot_axis(theta_i), and we solve -- exactly, over Q or an
   algebraic extension -- for the theta_i / base params that create EXTRA
   face-plane concurrences (each extra concurrence is one polynomial
   equation), then count each solution with cube_regions.

   This file provides the algebra layer; algebraic_bridge.py rationalizes
   solutions and counts them exactly. Cayley (tan half-angle) rational
   parameterization keeps rotation matrices rational in the parameter, so
   Groebner/Solve stay over Q. *)

(* ---- quaternion (w,x,y,z) -> SO(3) matrix, columns = face normals ---- *)
qmat[{w_, x_, y_, z_}] := Module[{n = w^2 + x^2 + y^2 + z^2},
  (1/n) {
    {w^2 + x^2 - y^2 - z^2, 2 (x y - w z),       2 (x z + w y)},
    {2 (x y + w z),         w^2 - x^2 + y^2 - z^2, 2 (y z - w x)},
    {2 (x z - w y),         2 (y z + w x),       w^2 - x^2 - y^2 + z^2}}];
cols[m_] := Transpose[m];   (* the 3 column normals *)

(* rotation about an INTEGER axis by a rational Cayley parameter s.
   R(s) = (I - S)^-1 (I + S), S = s [axis]_x with axis integer.  This is
   RATIONAL in s for every rational s (the angle is 2 arctan(s|axis|), but
   the matrix stays over Q -- exactly what keeps Groebner/Solve over Q and
   the resulting configs feedable to the rational counter).  s=0 -> I. *)
cay[axis_, s_] := Module[{K},
  K = s {{0, -axis[[3]], axis[[2]]}, {axis[[3]], 0, -axis[[1]]},
         {-axis[[2]], axis[[1]], 0}};
  Inverse[IdentityMatrix[3] - K].(IdentityMatrix[3] + K)];

(* rational rotation matrix -> integer quaternion (w,x,y,z) via the trace
   formula (w-branch): q ~ (1+r11+r22+r33, r32-r23, r13-r31, r21-r12),
   rational when R rational; clear denominators + gcd-reduce to integers.
   Valid when 1+tr(R) != 0 (never the pi-rotation branch here). *)
mat2quat[r_] := Module[{q, dens, L, ints, g},
  q = {1 + r[[1,1]] + r[[2,2]] + r[[3,3]], r[[3,2]] - r[[2,3]],
       r[[1,3]] - r[[3,1]], r[[2,1]] - r[[1,2]]};
  dens = Denominator /@ q; L = LCM @@ dens;
  ints = q L; g = GCD @@ ints; If[g != 0, ints = ints/g]; ints];

(* the 36 planes of a compound: for each cube matrix, each column c gives
   planes c.x=+1 and (-c).x=+1. Return list of {normal, offset=1}. *)
planesOf[mats_] := Flatten[Table[
   With[{cs = cols[m]}, Flatten[Table[{{cs[[j]], 1}, {-cs[[j]], 1}}, {j, 3}], 1]],
   {m, mats}], 1];

(* condition that planes p1,p2,p3,p4 share a common point: the 3 from an
   independent triple fix x; the 4th passes through it. Returned as the
   4x4 augmented determinant (=0 necessary), a polynomial in the params. *)
concur4[{n1_, c1_}, {n2_, c2_}, {n3_, c3_}, {n4_, c4_}] :=
  Det[{Append[n1, -c1], Append[n2, -c2], Append[n3, -c3], Append[n4, -c4]}];

(* corner of cube m in the (s1,s2,s3) octant = m.(s1,s2,s3) *)
corner[m_, s_] := m.s;

Print["algebraic_search.wl loaded: qmat, cay, planesOf, concur4, corner"];
