SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

triangle = {{1,2},{1,3},{2,3}};
fourthChoices = {{1,4},{2,4},{3,4}};
classPairs = {{"yz","zy"}, {"xz","zx"}};

out = OpenWrite["scan_mixed_summary.jsonl"];

Do[
  Do[
    Module[{plus, minus},
      {plus, minus} = cls;
      Do[
        Module[{bits, types, assign, label, res, cleaned},
          bits = IntegerDigits[pat, 2, 4];
          If[bits[[1]] == 1, Continue[]];
          types = If[# == 0, plus, minus] & /@ bits;
          assign = MapThread[{#1, #2} &, {Join[triangle, {fourth}], types}];
          label = <|"class"->plus, "fourth"->fourth, "pattern"->bits|>;
          res = solveSystem[assign, 30];
          If[res === $TimedOut || !ListQ[res],
            WriteString["stdout", "TIMEOUT class=",plus," fourth=",fourth," pat=",bits,"\n"],
            cleaned = Select[res, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
            Do[
              Module[{vals, psiDeg, t2Deg, t3Deg, t4Deg},
                vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. cleaned[[bi]];
                psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 10];
                t2Deg = N[180/Pi*ArcTan[vals[[3]], vals[[4]]], 10];
                t3Deg = N[180/Pi*ArcTan[vals[[5]], vals[[6]]], 10];
                t4Deg = N[180/Pi*ArcTan[vals[[7]], vals[[8]]], 10];
                WriteLine[out, ExportString[<|"label"->label,"branch"->bi,
                  "psiDeg"->psiDeg,"t2Deg"->t2Deg,"t3Deg"->t3Deg,"t4Deg"->t4Deg|>,"JSON"]];
              ],
              {bi, 1, Length[cleaned]}
            ];
            WriteString["stdout", "ok class=",plus," fourth=",fourth," pat=",bits," nreal=",Length[cleaned],"\n"];
          ];
        ],
        {pat, 0, 15}
      ];
    ],
    {cls, classPairs}
  ],
  {fourth, fourthChoices}
];
Close[out];
WriteString["stdout", "MIXED SCAN DONE\n"];
