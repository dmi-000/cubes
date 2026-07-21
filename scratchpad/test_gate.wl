Get["reslib.wl"];
cD0 = -1/2; sD0 = Sqrt[3]/2;
psiOct = ArcSin[1/Sqrt[3]];
psiGold = ArcTan[GoldenRatio^2];
valYZ = Simplify[gYZ[cD0, sD0, Cos[psiOct], Sin[psiOct]]];
valXZ = Simplify[gXZ[cD0, sD0, Cos[psiGold], Sin[psiGold]]];
Print["GATE R1: gYZ(Delta=120,psi=oct) = ", valYZ, "  (want 0)"];
Print["GATE R1: gXZ(Delta=120,psi=gold) = ", valXZ, "  (want 0)"];
