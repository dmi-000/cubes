SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

(* Scan given types over all 15 subsets, dump (subset,type,branch#,psiDeg,thetaDegs)
   summaries only (fast, no ToNumberField) so we can locate which system produces
   each target psiDeg. *)
typesToScan = {"yz", "zy", "xz", "zx"};

out = OpenWrite["scan_summary.jsonl"];
Do[
  Do[
    Module[{assign, sol, cleaned, t0, t1},
      assign = Map[{#, ty} &, subset];
      t0 = AbsoluteTime[];
      sol = solveSystem[assign, 25];
      t1 = AbsoluteTime[];
      If[sol === $TimedOut || !ListQ[sol],
        WriteLine[out, ExportString[<|"subset"->subset,"type"->ty,"status"->"timeout_or_fail","time"->N[t1-t0,3]|>,"JSON"]];
        WriteString["stdout", "TIMEOUT subset=",subset," type=",ty,"\n"],
        cleaned = Select[sol, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
        Do[
          Module[{vals, psiDeg, t2Deg, t3Deg, t4Deg},
            vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. cleaned[[bi]];
            psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 10];
            t2Deg = N[180/Pi*ArcTan[vals[[3]], vals[[4]]], 10];
            t3Deg = N[180/Pi*ArcTan[vals[[5]], vals[[6]]], 10];
            t4Deg = N[180/Pi*ArcTan[vals[[7]], vals[[8]]], 10];
            WriteLine[out, ExportString[<|"subset"->subset,"type"->ty,"branch"->bi,
              "psiDeg"->psiDeg,"t2Deg"->t2Deg,"t3Deg"->t3Deg,"t4Deg"->t4Deg|>,"JSON"]];
          ],
          {bi, 1, Length[cleaned]}
        ];
        WriteString["stdout", "ok subset=",subset," type=",ty," time=",N[t1-t0,3],"s nreal=",Length[cleaned],"\n"];
      ];
    ],
    {subset, pairSubsetsK4}
  ],
  {ty, typesToScan}
];
Close[out];
WriteString["stdout", "SCAN DONE\n"];
