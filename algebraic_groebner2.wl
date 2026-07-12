#!/usr/bin/env wolframscript
(* Productive Groebner solve: weld a fresh cube A to TWO different existing
   cubes at general (non-lattice) corners -- creating two separate corner
   coincidences (the 723-type structure of several moderate concurrences),
   not one over-concentrated point (which we found LOWERS the count: a
   12-fold concurrence gave 393 vs the 9-fold record 723).

   Working principles: ALGEBRAIC_SEARCH.md.
   For fixed A-corners cA=(1,1,1), cB=(1,1,-1) (cA.cB = 1), enumerate pairs
   of base-cube corners (P,Q) with P.Q = 1 (consistency), solve A mapping
   cA->P, cB->Q via GroebnerBasis/Solve, keep rational A, emit for counting. *)

Get[FileNameJoin[{Directory[], "algebraic_search.wl"}]];

solveTwoCorners[cA_, P_, cB_, Q_] := Module[{A, eqs, sol},
  A = qmat[{1, x, y, z}];
  eqs = Numerator[Together[#[[1]] - #[[2]]]] & /@ Join[
     Thread[A.cA == P], Thread[A.cB == Q]];
  sol = Solve[Thread[eqs == 0], {x, y, z}, Reals];
  {x, y, z} /. sol];
quatOf[{xx_, yy_, zz_}] := Module[{q = {1, xx, yy, zz}},
  If[AllTrue[q, (Element[#, Rationals] &)],
     With[{r = q (LCM @@ (Denominator /@ q))}, r/(GCD @@ r)], q]];

q723 = {{4,1,1,-1},{3,3,7,3},{5,-1,-5,-5},{2,1,1,1},{1,1,1,1},{5,2,2,2}};
base = q723[[;;5]];                (* weld A to the 5-cube base *)
M = qmat /@ base;
octs = Tuples[{1,-1},3];

(* all base corners with their source cube, deduped *)
corners = DeleteDuplicates[
   Flatten[Table[{M[[c]].s, c}, {c, Length[M]}, {s, octs}], 1],
   (#1[[1]] === #2[[1]]) &];
Print["base has ", Length[corners], " distinct corners"];

(* fixed A-corners *)
cA = {1,1,1}; cB = {1,1,-1};  (* cA.cB = 1 *)
(* consistent target pairs (P,Q) from DIFFERENT source cubes with P.Q=1 *)
pairs = Select[Subsets[corners, {2}],
   (#[[1,2]] =!= #[[2,2]] && #[[1,1]].#[[2,1]] == 1) &];
Print["consistent (P,Q) target pairs (diff cubes, P.Q=1): ", Length[pairs]];

allA = {};
Do[
  Module[{P = pr[[1,1]], Q = pr[[2,1]], sols},
    sols = Quiet[solveTwoCorners[cA, P, cB, Q]];
    allA = Join[allA, quatOf /@ sols];
    (* also the swapped assignment P<->Q *)
    sols = Quiet[solveTwoCorners[cA, Q, cB, P]];
    allA = Join[allA, quatOf /@ sols]],
  {pr, pairs}];

allA = DeleteDuplicates[Select[allA,
   (VectorQ[#, IntegerQ] && Max[Abs[#]] <= 4000) &]];
Print["distinct rational A solutions: ", Length[allA]];
Export[FileNameJoin[{Directory[], "groebner_solutions.json"}],
   {"base5" -> base, "Aquats" -> allA}];
Print["wrote ", Length[allA], " welded-A configs to groebner_solutions.json"];
