SetDirectory["/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad"];
Get["reslib_local.wl"];

(* row3 (sqrt6) candidate: same system as chain (subset {12,14,23,34}, type zy), branch 13 *)
assign = {{{1,2},"zy"}, {{1,4},"zy"}, {{2,3},"zy"}, {{3,4},"zy"}};
sol = solveSystem[assign, 60];
cleaned = Select[sol, (Element[(sP/.#), Reals] && (sP/.#) > 1/1000) &];
branch = cleaned[[13]];
vals = {cP,sP,c2,s2,c3,s3,c4,s4} /. branch;
psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 10];
WriteString["stdout", "psiDeg=", psiDeg, "\n"];

(* attempt tower construction: tanpsi in Q(sqrt6), b = 1+tanpsi^2, beta=Sqrt[b] *)
tanpsi = FullSimplify[vals[[2]]/vals[[1]]];
tanpsiRR = RootReduce[tanpsi];
WriteString["stdout", "tanpsi minpoly: ", MinimalPolynomial[tanpsiRR, tt], "\n"];
bval = RootReduce[1 + tanpsiRR^2];
WriteString["stdout", "bval = ", bval, "  simplified: ", Simplify[bval], "\n"];
beta = RootReduce[Sqrt[bval]];
WriteString["stdout", "beta minpoly (over Q): ", MinimalPolynomial[beta, tt], "\n"];

nf = Quiet[Check[ToNumberField[vals, beta], $Failed]];
If[nf === $Failed,
  WriteString["stdout", "ToNumberField[vals,beta] FAILED -- beta is not primitive for the compositum\n"],
  WriteString["stdout", "ToNumberField[vals,beta] SUCCEEDED\n"];
  Do[
    WriteString["stdout", i, ": ", List @@ nf[[i,2]], "\n"],
    {i, 1, Length[nf]}
  ];
];

(* also get bval as explicit p + q Sqrt[6] rationals *)
bvalRadical = ToRadicals[bval];
WriteString["stdout", "bval radical form: ", bvalRadical, "\n"];
