(* Resonance library: cross-class coincidence curves g_type(Delta,psi) for
   the dihedral family Rel-gauge pair, and the n=4 system builder.
   Derived/verified in derive2.py / gate_r1.py (sympy), reproduced here as
   exact polynomials (integer/rational coefficients) for Groebner solving.
   Variables: cD,sD (cos/sin of a pair difference Delta), cP,sP (cos/sin psi). *)

gXY[cD_, sD_, cP_, sP_] := 2*cD*sP^2 - cD + cP*sD - sD*sP - 2*sP^2 + 1;
gYZ[cD_, sD_, cP_, sP_] := -cD*cP*sP + cD*sP^2 + cD - cP*sD + cP*sP - sP^2 + 1;
gXZ[cD_, sD_, cP_, sP_] := cD*cP - cD*sP - cP - sD + sP;

(* the n=4 Rel-gauge unknowns: theta1=0 fixed; (c2,s2)=(cos t2,sin t2), etc,
   (cP,sP)=(cos psi,sin psi). Pair Delta_jk (j<k) = theta_k - theta_j. *)
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

(* assignments: list of {{j,k}, "type"} *)
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

(* solve a system exactly; returns list of real solutions as {c2,s2,c3,s3,c4,s4,cP,sP} rules *)
solveSystem[assignments_, opts___] := Module[{eqs, sol},
  eqs = buildEqs[assignments];
  sol = Quiet[Solve[Thread[eqs == 0], allVars, Reals]];
  sol];

Print["reslib.wl loaded"];
