#!/usr/bin/env wolframscript
Get[FileNameJoin[{Directory[], "algebraic_search.wl"}]];

(* 723 record quats: cubes 0,1,2 = C3 core about (1,1,1); 3,4,5 = free
   triple, also sharing the (1,1,1) corner. *)
q = {{4,1,1,-1},{3,3,7,3},{5,-1,-5,-5},{2,1,1,1},{1,1,1,1},{5,2,2,2}};
M = qmat /@ q;

(* --- validation: do cubes 3,4,5 share the (1,1,1) corner exactly? --- *)
c3 = corner[M[[4]], {1,1,1}];
c4 = corner[M[[5]], {1,1,1}];
c5 = corner[M[[6]], {1,1,1}];
Print["free triple (1,1,1)-corners equal? ",
      Simplify[c3 == c4 == c5], "   shared corner = ", c3];
Print["core triple share a corner? checking cubes 0,1,2 over octants..."];
octs = Tuples[{1,-1},3];
Do[If[Simplify[corner[M[[1]],s]==corner[M[[2]],s]==corner[M[[3]],s]],
      Print["  core shares corner at octant ", s, " -> ", corner[M[[1]],s]]],
   {s, octs}];

(* --- exact line search: rotate the FREE triple (cubes 3,4,5) together
   about (1,1,1) by angle with tan(half)=t. This preserves their shared
   corner, and sweeps them against the fixed core. Find the exact t where
   a free-cube face passes through a vertex of the core arrangement. --- *)
Rt = cay[{1,1,1}, s];
Mfree = Table[Rt.M[[i]], {i, {4,5,6}}];     (* free triple as functions of s *)
Mcore = M[[{1,2,3}]];

corePlanes = planesOf[Mcore];                 (* fixed, rational *)
freePlanes = planesOf[Mfree];                 (* rational in t *)

(* core arrangement vertices: common points of independent core-plane
   triples (rational). Dedup. *)
coreVerts = DeleteDuplicates[
   Select[
     Table[With[{p = corePlanes[[#]] & /@ trip},
        Module[{nn = p[[All,1]], cc = p[[All,2]], d},
          d = Det[nn]; If[d === 0, Missing[], LinearSolve[nn, cc]]]],
       {trip, Subsets[Range[Length[corePlanes]], {3}]}],
     Not[MissingQ[#]] &]];
Print["core arrangement: ", Length[coreVerts], " distinct vertices"];

(* walls: rational s such that some free-cube face plane passes through a
   core vertex. Each gives one polynomial equation Numerator[n(s).v-1]==0.
   Keep only RATIONAL roots (rational config -> rational counter). *)
sowRational[eq_] := Module[{poly, sols},
  poly = Numerator[Together[eq]];
  If[PossibleZeroQ[poly] || (PolynomialQ[poly, s] && Exponent[poly, s] < 1),
     Return[{}]];
  sols = s /. Solve[poly == 0, s];
  If[Head[sols] =!= List, Return[{}]];
  Select[sols, (Element[#, Rationals] && Abs[#] < 50) &]];

walls = DeleteDuplicates[Flatten[
   Table[sowRational[freePlanes[[f, 1]].v - freePlanes[[f, 2]]],
     {v, coreVerts}, {f, Length[freePlanes]}]]];
walls = SortBy[walls, N];
Print["found ", Length[walls], " distinct RATIONAL wall s-values (|s|<50)"];

(* emit exact configs as INTEGER QUATERNIONS for cube_regions. Include a
   tiny offset just off each wall (midpoints between consecutive walls) so
   the counter samples each open interval, plus the walls themselves. *)
samplePts = DeleteDuplicates[Join[walls,
   Table[(walls[[i]] + walls[[i+1]])/2, {i, Length[walls]-1}], {0}]];
out = Table[
   Module[{Rss = cay[{1,1,1}, sv], mall},
     mall = Join[Mcore, Table[Rss.M[[i]], {i, {4,5,6}}]];
     {sv, mat2quat /@ mall}],
   {sv, samplePts}];
Export[FileNameJoin[{Directory[], "algebraic_walls.json"}],
   {"points" -> (First /@ out), "quats" -> (Last /@ out)}];
Print["wrote ", Length[out], " candidate configs (walls + interval mids) ",
      "to algebraic_walls.json"];
Print["sample s-values: ", Take[walls, UpTo[12]]];
