(* Resonance library: cross-class coincidence curves g_type(Delta,psi) for
   the dihedral family Rel-gauge pair, and the n=4 system builder.
   Derived/verified in derive2.py / gate_r1.py (sympy), reproduced here as
   exact polynomials (integer/rational coefficients) for Groebner solving.
   Variables: cD,sD (cos/sin of a pair difference Delta), cP,sP (cos/sin psi). *)

gXY[cD_, sD_, cP_, sP_] := 2*cD*sP^2 - cD + cP*sD - sD*sP - 2*sP^2 + 1;
gYZ[cD_, sD_, cP_, sP_] := -cD*cP*sP + cD*sP^2 + cD - cP*sD + cP*sP - sP^2 + 1;
gXZ[cD_, sD_, cP_, sP_] := cD*cP - cD*sP - cP - sD + sP;

(* the n=4 Rel-gauge unknowns: theta1=0 fixed; (c2,s2)=(cos t2,sin t2), etc,
   (cP,sP)=(cos psi,sin psi). Pair Delta_jk (j<k) = theta_k - theta_j. *)
cosDelta[cj_, sj_, ck_, sk_] := ck*cj + sk*sj;
sinDelta[cj_, sj_, ck_, sk_] := sk*cj - ck*sj;

cs[1] := {1, 0};
cs[2] := {c2, s2};
cs[3] := {c3, s3};
cs[4] := {c4, s4};

pairCosSin[{j_, k_}] := Module[{cj, sj, ck, sk},
  {cj, sj} = cs[j]; {ck, sk} = cs[k];
  {cosDelta[cj, sj, ck, sk], sinDelta[cj, sj, ck, sk]}];

gYX[cD_, sD_, cP_, sP_] := gXY[cD, -sD, cP, sP];
gZY[cD_, sD_, cP_, sP_] := gYZ[cD, -sD, cP, sP];
gZX[cD_, sD_, cP_, sP_] := gXZ[cD, -sD, cP, sP];

gOf["xy"] = gXY; gOf["yz"] = gYZ; gOf["xz"] = gXZ;
gOf["yx"] = gYX; gOf["zy"] = gZY; gOf["zx"] = gZX;
allTypes = {"xy", "yz", "xz", "yx", "zy", "zx"};

circleRels = {c2^2 + s2^2 - 1, c3^2 + s3^2 - 1, c4^2 + s4^2 - 1, cP^2 + sP^2 - 1};

(* assignments: list of {{j,k}, "type"} *)
buildEqs[assignments_] := Module[{eqs},
  eqs = Map[
    Function[a,
      Module[{cd, sd, g},
        {cd, sd} = pairCosSin[a[[1]]];
        g = gOf[a[[2]]];
        g[cd, sd, cP, sP]
      ]],
    assignments];
  Join[eqs, circleRels]];

allVars = {c2, s2, c3, s3, c4, s4, cP, sP};

(* solve a system exactly; returns list of real solutions as {c2,s2,c3,s3,c4,s4,cP,sP} rules *)
solveSystem[assignments_, opts___] := Module[{eqs, sol},
  eqs = buildEqs[assignments];
  sol = Quiet[Solve[Thread[eqs == 0], allVars, Reals]];
  sol];

Print["reslib.wl loaded"];
Get["reslib.wl"];
SetOptions["stdout", FormatType -> OutputForm];

allPairs = {{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}};
pairSubsetsK4 = Subsets[allPairs, {4}];  (* 15 *)

outStream = OpenWrite[FileNameJoin[{Directory[], "uniform_k4_results.jsonl"}]];

exportSol[subset_, ty_, sol_] := Module[{vals, line},
  vals = {c2,s2,c3,s3,c4,s4,cP,sP} /. sol;
  line = ExportString[<|
     "subset" -> subset, "type" -> ty,
     "c2"->ToString[vals[[1]],InputForm], "s2"->ToString[vals[[2]],InputForm],
     "c3"->ToString[vals[[3]],InputForm], "s3"->ToString[vals[[4]],InputForm],
     "c4"->ToString[vals[[5]],InputForm], "s4"->ToString[vals[[6]],InputForm],
     "cP"->ToString[vals[[7]],InputForm], "sP"->ToString[vals[[8]],InputForm],
     "psiDeg" -> N[180/Pi*ArcTan[vals[[7]],vals[[8]]], 10],
     "t2Deg" -> N[180/Pi*ArcTan[vals[[1]],vals[[2]]], 10],
     "t3Deg" -> N[180/Pi*ArcTan[vals[[3]],vals[[4]]], 10],
     "t4Deg" -> N[180/Pi*ArcTan[vals[[5]],vals[[6]]], 10]
   |>, "JSON"];
  WriteLine[outStream, line];
];

Do[
  Do[
    Module[{assign, sol, t0, t1, cleaned, res},
      assign = Map[{#, ty} &, subset];
      t0 = AbsoluteTime[];
      res = TimeConstrained[
        Quiet[solveSystem[assign]],
        25, $TimedOut];
      t1 = AbsoluteTime[];
      If[res === $TimedOut || !ListQ[res],
        WriteLine[outStream, ExportString[<|"subset"->subset,"type"->ty,"status"->"timeout_or_fail","time"->N[t1-t0,4]|>,"JSON"]];
        WriteString["stdout", "TIMEOUT/FAIL subset=", subset, " type=", ty, " time=", N[t1-t0,3], "\n"];
        Continue[]];
      cleaned = Select[res, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
      Do[exportSol[subset, ty, s], {s, cleaned}];
      WriteString["stdout", "ok subset=",subset," type=",ty," time=",N[t1-t0,3],
        "s nsol=",Length[res]," nrealpos=",Length[cleaned],"\n"];
      Streams[] // Quiet;
    ],
    {ty, allTypes}],
  {subset, pairSubsetsK4}];

Close[outStream];
WriteString["stdout", "DONE uniform k4 sweep\n"];
(* Targeted mixed-ORIENTATION k=4 sweep: triangle {12,13,23} + one pair to
   cube 4, orientations mixed WITHIN one class. Rationale: the n=3
   octahedral resonance itself is mixed-orientation (pairs at Delta =
   120,120,240: the 240 pair rides the reversed curve g(cD,-sD)), so the
   uniform-orientation sweep structurally cannot contain the n=3-embedded
   resonances. Classes yz (octahedral) and xz (golden); orientation
   patterns halved by the global mirror (Theorem M: negate all thetas =
   flip every orientation, congruent compound). *)
Get["reslib.wl"];

triangle = {{1,2},{1,3},{2,3}};
fourthChoices = {{1,4},{2,4},{3,4}};
classPairs = {{"yz","zy"}, {"xz","zx"}};

outStream = OpenWrite[FileNameJoin[{Directory[], "mixed_k4_results.jsonl"}]];

exportSol[label_, sol_] := Module[{vals, line},
  vals = {c2,s2,c3,s3,c4,s4,cP,sP} /. sol;
  line = ExportString[<|
     "system" -> label,
     "c2"->ToString[vals[[1]],InputForm], "s2"->ToString[vals[[2]],InputForm],
     "c3"->ToString[vals[[3]],InputForm], "s3"->ToString[vals[[4]],InputForm],
     "c4"->ToString[vals[[5]],InputForm], "s4"->ToString[vals[[6]],InputForm],
     "cP"->ToString[vals[[7]],InputForm], "sP"->ToString[vals[[8]],InputForm],
     "psiDeg" -> N[180/Pi*ArcTan[vals[[7]],vals[[8]]], 10],
     "t2Deg" -> N[180/Pi*ArcTan[vals[[1]],vals[[2]]], 10],
     "t3Deg" -> N[180/Pi*ArcTan[vals[[3]],vals[[4]]], 10],
     "t4Deg" -> N[180/Pi*ArcTan[vals[[5]],vals[[6]]], 10]
   |>, "JSON"];
  WriteLine[outStream, line]];

Do[Do[Do[
  Module[{plus, minus, assign, label, res, t0, t1, cleaned},
    {plus, minus} = cls;
    (* orientation pattern: bit i of pat = orientation of condition i;
       condition list = triangle(3) + fourth(1). Fix bit1=0 (global mirror). *)
    Do[
      Module[{bits, types},
        bits = IntegerDigits[pat, 2, 4];
        If[bits[[1]] == 1, Continue[]];   (* mirror-halved *)
        types = If[# == 0, plus, minus] & /@ bits;
        assign = MapThread[{#1, #2} &, {Join[triangle, {fourth}], types}];
        label = <|"class"->plus, "fourth"->fourth, "pattern"->bits|>;
        t0 = AbsoluteTime[];
        res = TimeConstrained[Quiet[solveSystem[assign]], 30, $TimedOut];
        t1 = AbsoluteTime[];
        If[res === $TimedOut || !ListQ[res],
          WriteLine[outStream, ExportString[<|"system"->label,"status"->"timeout_or_fail","time"->N[t1-t0,4]|>,"JSON"]];
          WriteString["stdout", "TIMEOUT class=",plus," fourth=",fourth," pat=",bits,"\n"],
          cleaned = Select[res, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
          Do[exportSol[label, s], {s, cleaned}];
          WriteString["stdout", "ok class=",plus," fourth=",fourth," pat=",bits,
            " time=",N[t1-t0,3],"s nsol=",Length[res]," kept=",Length[cleaned],"\n"]];
      ],
      {pat, 0, 15}];
  ],
  {cls, classPairs}], {fourth, fourthChoices}], {dummy, {1}}];

Close[outStream];
WriteString["stdout", "DONE mixed k4 sweep\n"];
