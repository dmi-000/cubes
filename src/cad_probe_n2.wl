#!/usr/bin/env wolframscript
(* CAD feasibility probe for the unrestricted n=2 chamber exam.

   Working principles: C45_notes.md sections 9 and 11; Postscript 24.

   Chris Cole's fine-graining program: decompose the pair configuration
   space (a 3-parameter quaternion chart) into chambers on which the
   region count is constant, then examine one point per chamber to find
   the maximum. The walls where the arrangement combinatorics can change
   include the vertex-on-plane conditions: a corner v of the rotated
   cube lies on a face plane of the axis-aligned cube, i.e.
   ((R q . v)_i)^2 = N(q)^2, a quartic in the quaternion chart q=(1,x,y,z).

   This probe measures whether Wolfram's CylindricalDecomposition can
   handle the wall set. VERDICT (2026-07-13, this machine): the 24 V-F
   conditions reduce to 12 distinct quartics; CAD on just FOUR of them
   completes in ~4 min with a ~4.6-million-leaf cell tree; the full set
   (plus ~dozens of edge-edge coplanarity quartics) is infeasible.
   Unrestricted fine-graining is impractical even at n=2 — certification
   must go per-family, or via Theorem A + Euler census (C45 sect. 10).

   Usage: wolframscript -file cad_probe_n2.wl [nWalls] [seconds]
*)

R[{w_, x_, y_, z_}] := {{w^2+x^2-y^2-z^2, 2(x y - w z), 2(x z + w y)},
                        {2(x y + w z), w^2-x^2+y^2-z^2, 2(y z - w x)},
                        {2(x z - w y), 2(y z + w x), w^2-x^2-y^2+z^2}};
Nn[{w_, x_, y_, z_}] := w^2 + x^2 + y^2 + z^2;

q = {1, x, y, z};
verts = Tuples[{1, -1}, 3];
walls = DeleteDuplicates[Expand /@ Flatten[
    Table[((R[q].v)[[i]])^2 - Nn[q]^2, {v, verts}, {i, 3}]]];
Print["distinct V-F wall quartics: ", Length[walls]];

args = Rest[$ScriptCommandLine];
nW  = If[Length[args] >= 1, ToExpression[args[[1]]], 4];
tmax = If[Length[args] >= 2, ToExpression[args[[2]]], 240];

Print["attempting CAD on ", nW, " walls, time limit ", tmax, "s ..."];
res = TimeConstrained[
    CylindricalDecomposition[And @@ Thread[Take[walls, nW] != 0], {x, y, z}],
    tmax, $TimedOut];
Print[If[res === $TimedOut,
    "TIMED OUT",
    "finished; cell-tree leaf count = " <> ToString[LeafCount[res]]]];
