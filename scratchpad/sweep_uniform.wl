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
