SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

(* row1 (sqrt3-tower, psiDeg~53.794): mixed sweep, class yz, fourth={1,4},
   pattern {0,0,0,1} -> types [yz,yz,yz,zy] on [{1,2},{1,3},{2,3},{1,4}] *)
assign = {{{1,2},"yz"}, {{1,3},"yz"}, {{2,3},"yz"}, {{1,4},"zy"}};
sol = solveSystem[assign, 60];
cleaned = Select[sol, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
WriteString["stdout", "n real: ", Length[cleaned], "\n"];
Do[
  Module[{vals, psiDeg},
    vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. cleaned[[i]];
    psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 8];
    WriteString["stdout", "branch ", i, ": psiDeg=", psiDeg, "\n"];
  ],
  {i, 1, Length[cleaned]}
];

out = OpenWrite["row1_branches.jsonl"];
Do[
  Check[
    WriteLine[out, ExportString[
      exportBranch[cleaned[[i]], <|"candidate"->"row1_sqrt3tower", "branch"->i,
        "system"->"mixed triangle yz + {1,4} zy, pattern 0001"|>], "JSON"]],
    WriteString["stdout", "branch ", i, " export FAILED\n"]
  ],
  {i, {5,6}}
];
Close[out];
WriteString["stdout", "DONE\n"];
