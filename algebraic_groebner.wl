#!/usr/bin/env wolframscript
(* Multi-constraint algebraic solve via Groebner bases.

   Working principles: ALGEBRAIC_SEARCH.md (section "How to extend").

   The 1-parameter demo finds walls along one line. This finds the
   0-dimensional (isolated) high-codimension points: configs satisfying
   SEVERAL incidence constraints at once -- exactly the points a numeric
   grid misses. Method: an unknown cube A = qmat[{1,x,y,z}] (3 projective
   DOF); impose incidence equations (corner coincidences with fixed
   cubes); GroebnerBasis-eliminate and Solve for {x,y,z}; each solution is
   an exact (rational or algebraic) cube feeding the counter. *)

Get[FileNameJoin[{Directory[], "algebraic_search.wl"}]];

(* solve for an unknown cube A=qmat[{1,x,y,z}] whose corner cA maps to the
   fixed point P, and corner cB maps to fixed point Q. Two corner
   constraints pin the rotation to a finite set (consistent iff
   cA.cB == P.Q and |cA|=|P|,|cB|=|Q|). Returns exact {x,y,z} solutions. *)
solveTwoCorners[cA_, P_, cB_, Q_] := Module[{A, eqs, gb, sol},
  A = qmat[{1, x, y, z}];
  eqs = Join[Thread[A.cA == P], Thread[A.cB == Q]];
  (* clear denominators (qmat has 1/(1+x^2+y^2+z^2)) *)
  eqs = Numerator[Together[#[[1]] - #[[2]]]] & /@ eqs;
  sol = Solve[Thread[eqs == 0], {x, y, z}, Reals];
  {x, y, z} /. sol];

(* build integer quaternion from a solved {x,y,z} (rational or algebraic).
   For rational solutions this is exact; algebraic ones are returned as-is
   for the field-engine path. *)
quatOf[{xx_, yy_, zz_}] := Module[{q = {1, xx, yy, zz}, r},
  If[AllTrue[q, (Element[#, Rationals] &)],
     r = q * (LCM @@ (Denominator /@ q)); r/(GCD @@ r), q]];

(* --- demonstration: solve for a 6th cube A that JOINS the free triple's
   shared corner (1,1,1) -- turning the 9-fold concurrence into a 12-fold
   one -- while a second corner of A lands on a chosen target.  Both are
   corner constraints with matching Gram, so the system is consistent and
   0-dimensional; GroebnerBasis eliminates and Solve returns exact A's. --- *)
q723 = {{4,1,1,-1},{3,3,7,3},{5,-1,-5,-5},{2,1,1,1},{1,1,1,1},{5,2,2,2}};

(* constraint 1: A.(1,1,1) == (1,1,1)  (join the free triple's corner)
   constraint 2: A.(1,-1,-1) == R, with (1,1,1).R == (1,1,1).(1,-1,-1) = -1
   so pick several consistent targets R (the other (sum=-1) unit corners)
   and solve each; count the resulting 6-cube configs. *)
targetsR = Select[Tuples[{1,-1},3], (Total[#] == -1) &];  (* sum = -1 corners *)
Print["consistent second-corner targets R (sum=-1): ", targetsR];

allA = {};
Do[
  Module[{sols = solveTwoCorners[{1,1,1}, {1,1,1}, {1,-1,-1}, R]},
    Print["R = ", R, " -> ", Length[sols], " exact A solution(s): ",
          quatOf /@ sols];
    allA = Join[allA, quatOf /@ sols]],
  {R, targetsR}];

allA = DeleteDuplicates[Select[allA, VectorQ[#, IntegerQ] &]];  (* rational A *)
Print["distinct rational A quats found: ", Length[allA]];
(* emit configs: the 5 base cubes (drop cube 5) + each solved A as the 6th *)
Export[FileNameJoin[{Directory[], "groebner_solutions.json"}],
   {"base5" -> q723[[;;5]], "Aquats" -> allA}];
Print["wrote groebner_solutions.json"];
