(* Local re-derivation of resonance4_solve.wl's polynomial definitions.
   This is a FRESH file (not an edit of the read-only resonance4_solve.wl);
   it reproduces the same g_type formulas (copied by hand from the report/
   read-only source, per OPENCOUNT_SPEC's "re-run relevant parts" instruction)
   so we can solve INDIVIDUAL targeted systems without triggering the
   original file's full 90+48-system sweep side effects. *)

gXY[cD_, sD_, cP_, sP_] := 2*cD*sP^2 - cD + cP*sD - sD*sP - 2*sP^2 + 1;
gYZ[cD_, sD_, cP_, sP_] := -cD*cP*sP + cD*sP^2 + cD - cP*sD + cP*sP - sP^2 + 1;
gXZ[cD_, sD_, cP_, sP_] := cD*cP - cD*sP - cP - sD + sP;

cosDelta[cj_, sj_, ck_, sk_] := ck*cj + sk*sj;
sinDelta[cj_, sj_, ck_, sk_] := sk*cj - ck*sj;

cs[1] := {1, 0};
cs[2] := {c2, s2};
cs[3] := {c3, s3};
cs[4] := {c4, s4};

pairCosSin[{j_, k_}] := Module[{cj, sj, ck, sk},
  {cj, sj} = cs[j]; {ck, sk} = cs[k];
  {cosDelta[cj, sj, ck, sk], sinDelta[cj, sj, ck, sk]}];

gYX[cD_, sD_, cP_, sP_] := gXY[cD, -sD, cP, sP];
gZY[cD_, sD_, cP_, sP_] := gYZ[cD, -sD, cP, sP];
gZX[cD_, sD_, cP_, sP_] := gXZ[cD, -sD, cP, sP];

gOf["xy"] = gXY; gOf["yz"] = gYZ; gOf["xz"] = gXZ;
gOf["yx"] = gYX; gOf["zy"] = gZY; gOf["zx"] = gZX;
allTypes = {"xy", "yz", "xz", "yx", "zy", "zx"};

circleRels = {c2^2 + s2^2 - 1, c3^2 + s3^2 - 1, c4^2 + s4^2 - 1, cP^2 + sP^2 - 1};

buildEqs[assignments_] := Module[{eqs},
  eqs = Map[
    Function[a,
      Module[{cd, sd, g},
        {cd, sd} = pairCosSin[a[[1]]];
        g = gOf[a[[2]]];
        g[cd, sd, cP, sP]
      ]],
    assignments];
  Join[eqs, circleRels]];

allVars = {c2, s2, c3, s3, c4, s4, cP, sP};

solveSystem[assignments_, tlimit_:25] := Module[{eqs, sol},
  eqs = buildEqs[assignments];
  sol = TimeConstrained[Quiet[Solve[Thread[eqs == 0], allVars, Reals]], tlimit, $TimedOut];
  sol];

allPairs = {{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}};
pairSubsetsK4 = Subsets[allPairs, {4}];

(* ---- ToNumberField-based exact export of one solution branch ---- *)
exportBranch[sol_, tagAssoc_] := Module[
  {vals, psiDeg, t2Deg, t3Deg, t4Deg, nf, genRoot, tvar, genMinPoly, deg,
   genNumeric, coeffVecs, rec},
  vals = {cP, sP, c2, s2, c3, s3, c4, s4} /. sol;
  psiDeg = N[180/Pi*ArcTan[vals[[1]], vals[[2]]], 12];
  t2Deg = N[180/Pi*ArcTan[vals[[3]], vals[[4]]], 12];
  t3Deg = N[180/Pi*ArcTan[vals[[5]], vals[[6]]], 12];
  t4Deg = N[180/Pi*ArcTan[vals[[7]], vals[[8]]], 12];
  nf = ToNumberField[vals];
  genRoot = nf[[1, 1]];
  tvar = Symbol["tgen"];
  genMinPoly = MinimalPolynomial[genRoot, tvar];
  deg = Exponent[genMinPoly, tvar];
  genNumeric = N[genRoot, 40];
  coeffVecs = Table[PadRight[List @@ nf[[i, 2]], deg], {i, 1, Length[nf]}];
  rec = <|
    "tag" -> tagAssoc,
    "psiDeg" -> psiDeg, "t2Deg" -> t2Deg, "t3Deg" -> t3Deg, "t4Deg" -> t4Deg,
    "field_degree" -> deg,
    "minpoly_coeffs" -> Map[ToString[#, InputForm] &, CoefficientList[genMinPoly, tvar]],
    "gen_numeric_re" -> ToString[Re[genNumeric], InputForm],
    "gen_numeric_im" -> ToString[Im[genNumeric], InputForm],
    "cP" -> Map[ToString[#, InputForm] &, coeffVecs[[1]]],
    "sP" -> Map[ToString[#, InputForm] &, coeffVecs[[2]]],
    "c2" -> Map[ToString[#, InputForm] &, coeffVecs[[3]]],
    "s2" -> Map[ToString[#, InputForm] &, coeffVecs[[4]]],
    "c3" -> Map[ToString[#, InputForm] &, coeffVecs[[5]]],
    "s3" -> Map[ToString[#, InputForm] &, coeffVecs[[6]]],
    "c4" -> Map[ToString[#, InputForm] &, coeffVecs[[7]]],
    "s4" -> Map[ToString[#, InputForm] &, coeffVecs[[8]]]
  |>;
  rec
];

Print["reslib_local.wl loaded"];
