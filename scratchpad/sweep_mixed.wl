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
