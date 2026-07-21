Get["reslib.wl"];
cD0 = -1/2; sD0 = Sqrt[3]/2;
psiGold = ArcTan[GoldenRatio^2];
valXZ = gXZ[cD0, sD0, Cos[psiGold], Sin[psiGold]];
Print["numeric: ", N[valXZ, 30]];
Print["FullSimplify: ", FullSimplify[valXZ, GoldenRatio^2 == GoldenRatio+1]];
Print["FullSimplify plain: ", FullSimplify[valXZ]];
