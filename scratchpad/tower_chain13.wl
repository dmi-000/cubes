SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

assign = {{{1,2},"zy"}, {{1,4},"zy"}, {{2,3},"zy"}, {{3,4},"zy"}};
sol = solveSystem[assign, 60];
cleaned = Select[sol, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
branch = cleaned[[15]];
vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. branch;
psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 10];
WriteString["stdout", "psiDeg=", psiDeg, "\n"];

tanpsi = RootReduce[vals[[2]]/vals[[1]]];
WriteString["stdout", "tanpsi minpoly: ", MinimalPolynomial[tanpsi, tt], "\n"];
bval = RootReduce[1 + tanpsi^2];
WriteString["stdout", "bval simplified: ", Simplify[bval], "\n"];
beta = RootReduce[Sqrt[bval]];
WriteString["stdout", "beta minpoly (over Q): ", MinimalPolynomial[beta, tt], "\n"];

nf = Quiet[Check[ToNumberField[vals, beta], $Failed]];
If[nf === $Failed,
  WriteString["stdout", "ToNumberField[vals,beta] FAILED\n"],
  WriteString["stdout", "ToNumberField[vals,beta] SUCCEEDED\n"];
  Do[
    WriteString["stdout", i, ": ", List @@ nf[[i,2]], "\n"],
    {i, 1, Length[nf]}
  ];
];
