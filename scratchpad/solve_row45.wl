SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

(* row4 (pentagonal, 58.283) and row5 (golden-nested, 38.173): both are
   branches of subset {12,13,23,24}, type xz, uniform sweep. *)
assign = Map[{#, "xz"} &, {{1,2},{1,3},{2,3},{2,4}}];
sol = solveSystem[assign, 60];
cleaned = Select[sol, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
WriteString["stdout", "n real: ", Length[cleaned], "\n"];
Do[
  Module[{vals, psiDeg},
    vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. cleaned[[i]];
    psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 8];
    If[Abs[psiDeg-58.28252559]<0.001 || Abs[psiDeg-38.17270763]<0.001,
      WriteString["stdout", "branch ", i, ": psiDeg=", psiDeg, "\n"]];
  ],
  {i, 1, Length[cleaned]}
];

out = OpenWrite["row45_branches.jsonl"];
Do[
  Check[
    WriteLine[out, ExportString[
      exportBranch[cleaned[[i]], <|"candidate"->"row45_pentagonal_or_golden", "branch"->i,
        "system"->"uniform subset {12,13,23,24} type xz"|>], "JSON"]],
    WriteString["stdout", "branch ", i, " export FAILED\n"]
  ],
  {i, {56,64}}
];
Close[out];
WriteString["stdout", "DONE\n"];
