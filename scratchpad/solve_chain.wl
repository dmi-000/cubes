SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

(* CHAIN candidate: subset {12,14,23,34}, type "zy" uniform, per
   resonance4_results.jsonl line 65. Target psiDeg ~= 37.5096. *)
assign = {{{1,2},"zy"}, {{1,4},"zy"}, {{2,3},"zy"}, {{3,4},"zy"}};
t0 = AbsoluteTime[];
sol = solveSystem[assign, 90];
t1 = AbsoluteTime[];
WriteString["stdout", "solve time: ", N[t1-t0,3], "s\n"];
If[sol === $TimedOut || !ListQ[sol],
  WriteString["stdout", "TIMEOUT/FAIL\n"];
  Exit[1]
];
WriteString["stdout", "nsol=", Length[sol], "\n"];
cleaned = Select[sol, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
WriteString["stdout", "n real positive-sP: ", Length[cleaned], "\n"];
Do[
  Module[{vals, psiDeg},
    vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. cleaned[[i]];
    psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 8];
    WriteString["stdout", "branch ", i, ": psiDeg=", psiDeg, "\n"];
  ],
  {i, 1, Length[cleaned]}
];

out = OpenWrite["chain_branches.jsonl"];
Do[
  Module[{rec},
    Check[
      rec = exportBranch[cleaned[[i]], <|"candidate"->"chain_subset_zy", "branch"->i, "subset"->{{1,2},{1,4},{2,3},{3,4}}, "type"->"zy"|>];
      WriteLine[out, ExportString[rec, "JSON"]],
      WriteString["stdout", "branch ", i, " export FAILED (degenerate field)\n"]
    ]
  ],
  {i, {13,14,15,16}}
];
Close[out];
WriteString["stdout", "DONE\n"];
