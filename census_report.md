# Census report: (c1) exact data from both n=3 max(3)=67 witnesses

Produced by census_extract.py (exact field arithmetic only in all
decisions; floats used only for sorting/printing).  Feeds lemma
L2.c (and the bottom diagram of cluster 1) of C45_notes.md sect. 13.

## Gates

| gate | W1 octahedral Q(sqrt2) | W2 golden Q(sqrt5) |
|------|------------------------|--------------------|
| G1 exact count 67={48,18,1} | PASS (slide3_q2.exact_count_q2) | PASS (certify_six.exact_count_config) |
| G2 TOP-1 Euler F=48 | F=48 (PASS) | F=48 (PASS) |
| G2 BOTTOM Euler F=18 | F=18 (PASS) | F=18 (PASS) |
| G3 antipodal symmetry | PASS | PASS |

## Graph invariants

| quantity | W1 | W2 |
|----------|----|----|
| TOP-1: V | 62 | 56 |
| TOP-1: E | 108 | 102 |
| TOP-1: components | 1 | 1 |
| TOP-1: F = E-V+1+C | 48 | 48 |
| BOTTOM: V | 32 | 32 |
| BOTTOM: E | 48 | 48 |
| BOTTOM: components | 1 | 1 |
| BOTTOM: F = E-V+1+C | 18 | 18 |

## Vertex census

| quantity | W1 | W2 |
|----------|----|----|
| triple points | 32 | 32 |
| kinks | 30 | 24 |
| triple degree spectrum, TOP | deg 3: 32 | deg 3: 32 |
| triple degree spectrum, BOTTOM | deg 3: 32 | deg 3: 32 |
| kink degree spectrum, TOP | deg 4: 30 | deg 4: 18, deg 6: 6 |
| kink degree spectrum, BOTTOM | deg 0: 30 | deg 0: 24 |
| sum(deg-2), TOP, triple points | 32 | 32 |
| sum(deg-2), TOP, all vertices | 92 | 92 |
| sum(deg-2), BOTTOM, triple points | 32 | 32 |
| kinks lie in exactly one diagram | True | True |
| occurring elementary triples (f0,f1,f2,s01,s12) | 16 | 16 |
| ... in C3-symmetry orbits | 6 | 6 |

## The sect. 13 projection vs the data (DISCREPANCY -- READ FIRST)

Sect. 13 (L2.c) projects "at most 46 feasible triples x 2 points
= 92 V-weight, hence F <= 2 + 92/2 = 48", with L2.b assuming
"kink vertices are degree-2 and contribute 0".  The exact data
CONFIRMS the total-weight arithmetic but CORRECTS the accounting:

1. TOTAL top-1 weight sum_v(deg_v - 2) = 92 EXACTLY, for BOTH
   witnesses (F = 2 + 92/2 = 48, single-component graphs).  The
   projected budget number is right and attained with equality.
2. BUT rank-triple points carry only 32 of the 92: both witnesses
   have exactly 32 triple points, every one TRIVALENT in the TOP-1
   graph (and trivalent in the BOTTOM graph), each with a UNIQUE
   active face per cube.  There are no merged/high-degree triple
   points at either witness.
3. The remaining 60 units of weight are carried by SAME-PAIR
   double-tie vertices (classified "kink" here: only one cube
   PAIR is tied, but two or three faces per cube are active):
   - W1: 30 edge-edge contact vertices, all degree 4
     (30 x 2 = 60): two cubes sit on sector boundaries
     simultaneously, two branches of the same tie r_i = r_j
     cross.
   - W2: 18 edge-edge degree-4 vertices (36) + 6 CORNER-contact
     degree-6 vertices (24): at u ~ (1,1,1)-type directions two
     cubes are simultaneously at corners (all three faces tied,
     active sets of size 3); 36 + 24 = 60.
   So the L2.b obligation "(1) kinks are degree-2, discountable"
   is FALSE at both witnesses; the (c2)/(c3) budget must include
   same-pair multi-tie vertices.  The degeneracy-robust (c3)
   statement should budget the TOTAL weight 92 = (rank-triple
   weight) + (same-pair crossing weight), conserved under both
   kinds of merging.
4. Occurring elementary active triples: 16 (W1) and 16 (W2), in 6/6 C3-orbits -- far below
   the projected <= 46.  Verified: each occurring triple is
   realized at EXACTLY 2 (antipodal) vertices, and each triple
   point realizes exactly one elementary triple; 16 x 2 = 32 =
   the triple-point count.  The "x 2 points per feasible
   triple" heuristic of sect. 13 is exact on the occurring
   triples; the slack is entirely in "<= 46 feasible" vs 16
   occurring.
5. BOTTOM graphs: both witnesses give the exact GENERIC census
   V=32, E=48, F=18, all 32 triple points trivalent, no kinks at
   all -- matching the general law V_1(n) = 12n - 4 = 32 of
   sect. 7 with NO degeneracy correction on the bottom side.
   (Both diagrams share the same 32 rank-triple points: at n=3
   all three reaches are equal there, so each is a vertex of
   both diagrams, trivalent in each: 6 arcs alternate
   top/bottom around every triple point.)

## W1 octahedral Q(sqrt2): occurring elementary triples (classification target list)

Faces are column indices 0,1,2 of each cube's rotation; triple
(f0,f1,f2) means face f_k of cube k is active and tied at the
point; s01 = sign((n0.u)(n1.u)), s12 = sign((n1.u)(n2.u)).
Grouped in orbits of the C3 symmetry of the compound.

- orbit (3): (0,0,0) s01=+1 s12=+1; (1,1,1) s01=+1 s12=+1; (2,2,2) s01=+1 s12=+1   [vertex ids: [12, 19, 27, 34, 42, 49]]
- orbit (3): (0,0,1) s01=+1 s12=-1; (2,1,1) s01=-1 s12=+1; (2,0,2) s01=-1 s12=-1   [vertex ids: [9, 17, 26, 35, 44, 52]]
- orbit (3): (0,2,0) s01=+1 s12=+1; (1,1,0) s01=+1 s12=+1; (1,2,2) s01=+1 s12=+1   [vertex ids: [1, 4, 11, 50, 57, 60]]
- orbit (3): (0,2,1) s01=+1 s12=-1; (2,1,0) s01=-1 s12=+1; (1,0,2) s01=-1 s12=-1   [vertex ids: [2, 16, 24, 37, 45, 59]]
- orbit (3): (1,0,1) s01=-1 s12=-1; (2,2,1) s01=+1 s12=-1; (2,0,0) s01=-1 s12=+1   [vertex ids: [8, 20, 23, 38, 41, 53]]
- orbit (1): (1,2,0) s01=+1 s12=+1   [vertex ids: [5, 56]]

## W2 golden Q(sqrt5): occurring elementary triples (classification target list)

Faces are column indices 0,1,2 of each cube's rotation; triple
(f0,f1,f2) means face f_k of cube k is active and tied at the
point; s01 = sign((n0.u)(n1.u)), s12 = sign((n1.u)(n2.u)).
Grouped in orbits of the C3 symmetry of the compound.

- orbit (1): (0,0,0) s01=+1 s12=+1   [vertex ids: [14, 41]]
- orbit (3): (0,0,1) s01=+1 s12=+1; (1,0,0) s01=+1 s12=+1; (0,1,0) s01=+1 s12=+1   [vertex ids: [8, 15, 16, 39, 40, 47]]
- orbit (3): (0,1,2) s01=+1 s12=-1; (2,0,1) s01=-1 s12=+1; (1,2,0) s01=-1 s12=-1   [vertex ids: [3, 13, 20, 35, 42, 52]]
- orbit (3): (0,2,1) s01=+1 s12=+1; (1,0,2) s01=+1 s12=+1; (2,1,0) s01=+1 s12=+1   [vertex ids: [4, 12, 21, 34, 43, 51]]
- orbit (3): (0,2,2) s01=+1 s12=-1; (2,0,2) s01=-1 s12=+1; (2,2,0) s01=-1 s12=-1   [vertex ids: [5, 6, 22, 33, 49, 50]]
- orbit (3): (1,2,2) s01=-1 s12=-1; (2,1,2) s01=+1 s12=-1; (2,2,1) s01=-1 s12=+1   [vertex ids: [25, 26, 27, 28, 29, 30]]

## W1-vs-W2 merge comparison (for the (c3) robust budget)

Within each witness all candidate constructions were deduped
projectively; "multiplicity" of a degenerate vertex = number of
active tied face-pairs of its cube pair (= deg/2 in its single
diagram).

- W1 octahedral Q(sqrt2): triple points all multiplicity 3 (trivalent x2 diagrams); same-pair contact vertices by multiplicity: {2: 30}
- W2 golden Q(sqrt5): triple points all multiplicity 3 (trivalent x2 diagrams); same-pair contact vertices by multiplicity: {2: 18, 3: 6}

The witnesses realize the SAME global weights (92 top, 32
bottom) through different local contact patterns: W1 spreads
the 60 same-pair units over 30 edge-edge double crossings;
W2 concentrates 24 of them into 6 corner contacts (golden
corner coincidences, multiplicity 3) and keeps 18 edge-edge.
The (c3) budget must therefore be weight-preserving under
merging of same-pair contacts as well as of rank-triple points.

## Full vertex tables

### W1 octahedral Q(sqrt2)

| id | float coords | type | active (c0;c1;c2) | deg_top | deg_bot | antipode |
|----|--------------|------|-------------------|--------|---------|----------|
| 0 | (-1.0000, -2.4142, -2.4142) | kink | 1;12;02 | 4 | 0 | 61 |
| 1 | (-1.0000, -2.4142, -1.0000) | triple | 1;1;0 | 3 | 3 | 60 |
| 2 | (-1.0000, -2.4142, 1.0000) | triple | 2;1;0 | 3 | 3 | 59 |
| 3 | (-1.0000, -2.4142, 2.4142) | kink | 2;01;02 | 4 | 0 | 58 |
| 4 | (-1.0000, -1.0000, -2.4142) | triple | 1;2;2 | 3 | 3 | 57 |
| 5 | (-1.0000, -1.0000, -1.0000) | triple | 1;2;0 | 3 | 3 | 56 |
| 6 | (-1.0000, -1.0000, -0.4142) | kink | 01;12;0 | 4 | 0 | 55 |
| 7 | (-1.0000, -1.0000, 0.4142) | kink | 02;01;0 | 4 | 0 | 54 |
| 8 | (-1.0000, -1.0000, 1.0000) | triple | 2;0;0 | 3 | 3 | 53 |
| 9 | (-1.0000, -1.0000, 2.4142) | triple | 2;0;2 | 3 | 3 | 52 |
| 10 | (-1.0000, -0.4142, -1.0000) | kink | 01;2;02 | 4 | 0 | 51 |
| 11 | (-1.0000, -0.4142, -0.4142) | triple | 0;2;0 | 3 | 3 | 50 |
| 12 | (-1.0000, -0.4142, 0.4142) | triple | 0;0;0 | 3 | 3 | 49 |
| 13 | (-1.0000, -0.4142, 1.0000) | kink | 02;0;02 | 4 | 0 | 48 |
| 14 | (-1.0000, 0.0000, 0.0000) | kink | 0;02;01 | 4 | 0 | 47 |
| 15 | (-1.0000, 0.4142, -1.0000) | kink | 02;2;12 | 4 | 0 | 46 |
| 16 | (-1.0000, 0.4142, -0.4142) | triple | 0;2;1 | 3 | 3 | 45 |
| 17 | (-1.0000, 0.4142, 0.4142) | triple | 0;0;1 | 3 | 3 | 44 |
| 18 | (-1.0000, 0.4142, 1.0000) | kink | 01;0;12 | 4 | 0 | 43 |
| 19 | (-1.0000, 1.0000, -2.4142) | triple | 2;2;2 | 3 | 3 | 42 |
| 20 | (-1.0000, 1.0000, -1.0000) | triple | 2;2;1 | 3 | 3 | 41 |
| 21 | (-1.0000, 1.0000, -0.4142) | kink | 02;12;1 | 4 | 0 | 40 |
| 22 | (-1.0000, 1.0000, 0.4142) | kink | 01;01;1 | 4 | 0 | 39 |
| 23 | (-1.0000, 1.0000, 1.0000) | triple | 1;0;1 | 3 | 3 | 38 |
| 24 | (-1.0000, 1.0000, 2.4142) | triple | 1;0;2 | 3 | 3 | 37 |
| 25 | (-1.0000, 2.4142, -2.4142) | kink | 2;12;12 | 4 | 0 | 36 |
| 26 | (-1.0000, 2.4142, -1.0000) | triple | 2;1;1 | 3 | 3 | 35 |
| 27 | (-1.0000, 2.4142, 1.0000) | triple | 1;1;1 | 3 | 3 | 34 |
| 28 | (-1.0000, 2.4142, 2.4142) | kink | 1;01;12 | 4 | 0 | 33 |
| 29 | (0.0000, -1.0000, 0.0000) | kink | 12;1;01 | 4 | 0 | 32 |
| 30 | (0.0000, 0.0000, -1.0000) | kink | 12;02;2 | 4 | 0 | 31 |
| 31 | (0.0000, 0.0000, 1.0000) | kink | 12;02;2 | 4 | 0 | 30 |
| 32 | (0.0000, 1.0000, 0.0000) | kink | 12;1;01 | 4 | 0 | 29 |
| 33 | (1.0000, -2.4142, -2.4142) | kink | 1;01;12 | 4 | 0 | 28 |
| 34 | (1.0000, -2.4142, -1.0000) | triple | 1;1;1 | 3 | 3 | 27 |
| 35 | (1.0000, -2.4142, 1.0000) | triple | 2;1;1 | 3 | 3 | 26 |
| 36 | (1.0000, -2.4142, 2.4142) | kink | 2;12;12 | 4 | 0 | 25 |
| 37 | (1.0000, -1.0000, -2.4142) | triple | 1;0;2 | 3 | 3 | 24 |
| 38 | (1.0000, -1.0000, -1.0000) | triple | 1;0;1 | 3 | 3 | 23 |
| 39 | (1.0000, -1.0000, -0.4142) | kink | 01;01;1 | 4 | 0 | 22 |
| 40 | (1.0000, -1.0000, 0.4142) | kink | 02;12;1 | 4 | 0 | 21 |
| 41 | (1.0000, -1.0000, 1.0000) | triple | 2;2;1 | 3 | 3 | 20 |
| 42 | (1.0000, -1.0000, 2.4142) | triple | 2;2;2 | 3 | 3 | 19 |
| 43 | (1.0000, -0.4142, -1.0000) | kink | 01;0;12 | 4 | 0 | 18 |
| 44 | (1.0000, -0.4142, -0.4142) | triple | 0;0;1 | 3 | 3 | 17 |
| 45 | (1.0000, -0.4142, 0.4142) | triple | 0;2;1 | 3 | 3 | 16 |
| 46 | (1.0000, -0.4142, 1.0000) | kink | 02;2;12 | 4 | 0 | 15 |
| 47 | (1.0000, 0.0000, 0.0000) | kink | 0;02;01 | 4 | 0 | 14 |
| 48 | (1.0000, 0.4142, -1.0000) | kink | 02;0;02 | 4 | 0 | 13 |
| 49 | (1.0000, 0.4142, -0.4142) | triple | 0;0;0 | 3 | 3 | 12 |
| 50 | (1.0000, 0.4142, 0.4142) | triple | 0;2;0 | 3 | 3 | 11 |
| 51 | (1.0000, 0.4142, 1.0000) | kink | 01;2;02 | 4 | 0 | 10 |
| 52 | (1.0000, 1.0000, -2.4142) | triple | 2;0;2 | 3 | 3 | 9 |
| 53 | (1.0000, 1.0000, -1.0000) | triple | 2;0;0 | 3 | 3 | 8 |
| 54 | (1.0000, 1.0000, -0.4142) | kink | 02;01;0 | 4 | 0 | 7 |
| 55 | (1.0000, 1.0000, 0.4142) | kink | 01;12;0 | 4 | 0 | 6 |
| 56 | (1.0000, 1.0000, 1.0000) | triple | 1;2;0 | 3 | 3 | 5 |
| 57 | (1.0000, 1.0000, 2.4142) | triple | 1;2;2 | 3 | 3 | 4 |
| 58 | (1.0000, 2.4142, -2.4142) | kink | 2;01;02 | 4 | 0 | 3 |
| 59 | (1.0000, 2.4142, -1.0000) | triple | 2;1;0 | 3 | 3 | 2 |
| 60 | (1.0000, 2.4142, 1.0000) | triple | 1;1;0 | 3 | 3 | 1 |
| 61 | (1.0000, 2.4142, 2.4142) | kink | 1;12;02 | 4 | 0 | 0 |

### W2 golden Q(sqrt5)

| id | float coords | type | active (c0;c1;c2) | deg_top | deg_bot | antipode |
|----|--------------|------|-------------------|--------|---------|----------|
| 0 | (-1.0000, -4.2361, -4.2361) | kink | 12;2;01 | 4 | 0 | 55 |
| 1 | (-1.0000, -4.2361, 4.2361) | kink | 12;01;2 | 4 | 0 | 54 |
| 2 | (-1.0000, -3.6180, 0.0000) | kink | 1;02;02 | 4 | 0 | 53 |
| 3 | (-1.0000, -2.6180, -1.6180) | triple | 1;2;0 | 3 | 3 | 52 |
| 4 | (-1.0000, -2.6180, 1.6180) | triple | 1;0;2 | 3 | 3 | 51 |
| 5 | (-1.0000, -2.0000, -2.6180) | triple | 2;2;0 | 3 | 3 | 50 |
| 6 | (-1.0000, -2.0000, 2.6180) | triple | 2;0;2 | 3 | 3 | 49 |
| 7 | (-1.0000, -1.6180, -3.2361) | kink | 2;12;01 | 4 | 0 | 48 |
| 8 | (-1.0000, -1.6180, 0.0000) | triple | 1;0;0 | 3 | 3 | 47 |
| 9 | (-1.0000, -1.6180, 3.2361) | kink | 2;01;12 | 4 | 0 | 46 |
| 10 | (-1.0000, -1.0000, -1.0000) | kink | 012;012;0 | 6 | 0 | 45 |
| 11 | (-1.0000, -1.0000, 1.0000) | kink | 012;0;012 | 6 | 0 | 44 |
| 12 | (-1.0000, -0.6180, -1.6180) | triple | 2;1;0 | 3 | 3 | 43 |
| 13 | (-1.0000, -0.6180, 1.6180) | triple | 2;0;1 | 3 | 3 | 42 |
| 14 | (-1.0000, -0.3820, 0.0000) | triple | 0;0;0 | 3 | 3 | 41 |
| 15 | (-1.0000, 0.0000, -0.6180) | triple | 0;1;0 | 3 | 3 | 40 |
| 16 | (-1.0000, 0.0000, 0.6180) | triple | 0;0;1 | 3 | 3 | 39 |
| 17 | (-1.0000, 0.2361, -1.0000) | kink | 02;1;02 | 4 | 0 | 38 |
| 18 | (-1.0000, 0.2361, 1.0000) | kink | 02;02;1 | 4 | 0 | 37 |
| 19 | (-1.0000, 0.3820, 0.0000) | kink | 0;012;012 | 6 | 0 | 36 |
| 20 | (-1.0000, 0.6180, -0.3820) | triple | 0;1;2 | 3 | 3 | 35 |
| 21 | (-1.0000, 0.6180, 0.3820) | triple | 0;2;1 | 3 | 3 | 34 |
| 22 | (-1.0000, 0.8541, 0.0000) | triple | 0;2;2 | 3 | 3 | 33 |
| 23 | (-1.0000, 1.0000, -0.2361) | kink | 01;12;2 | 4 | 0 | 32 |
| 24 | (-1.0000, 1.0000, 0.2361) | kink | 01;2;12 | 4 | 0 | 31 |
| 25 | (-1.0000, 1.6180, 0.0000) | triple | 1;2;2 | 3 | 3 | 30 |
| 26 | (0.0000, -1.0000, -1.6180) | triple | 2;2;1 | 3 | 3 | 29 |
| 27 | (0.0000, -1.0000, 1.6180) | triple | 2;1;2 | 3 | 3 | 28 |
| 28 | (0.0000, 1.0000, -1.6180) | triple | 2;1;2 | 3 | 3 | 27 |
| 29 | (0.0000, 1.0000, 1.6180) | triple | 2;2;1 | 3 | 3 | 26 |
| 30 | (1.0000, -1.6180, 0.0000) | triple | 1;2;2 | 3 | 3 | 25 |
| 31 | (1.0000, -1.0000, -0.2361) | kink | 01;2;12 | 4 | 0 | 24 |
| 32 | (1.0000, -1.0000, 0.2361) | kink | 01;12;2 | 4 | 0 | 23 |
| 33 | (1.0000, -0.8541, 0.0000) | triple | 0;2;2 | 3 | 3 | 22 |
| 34 | (1.0000, -0.6180, -0.3820) | triple | 0;2;1 | 3 | 3 | 21 |
| 35 | (1.0000, -0.6180, 0.3820) | triple | 0;1;2 | 3 | 3 | 20 |
| 36 | (1.0000, -0.3820, 0.0000) | kink | 0;012;012 | 6 | 0 | 19 |
| 37 | (1.0000, -0.2361, -1.0000) | kink | 02;02;1 | 4 | 0 | 18 |
| 38 | (1.0000, -0.2361, 1.0000) | kink | 02;1;02 | 4 | 0 | 17 |
| 39 | (1.0000, 0.0000, -0.6180) | triple | 0;0;1 | 3 | 3 | 16 |
| 40 | (1.0000, 0.0000, 0.6180) | triple | 0;1;0 | 3 | 3 | 15 |
| 41 | (1.0000, 0.3820, 0.0000) | triple | 0;0;0 | 3 | 3 | 14 |
| 42 | (1.0000, 0.6180, -1.6180) | triple | 2;0;1 | 3 | 3 | 13 |
| 43 | (1.0000, 0.6180, 1.6180) | triple | 2;1;0 | 3 | 3 | 12 |
| 44 | (1.0000, 1.0000, -1.0000) | kink | 012;0;012 | 6 | 0 | 11 |
| 45 | (1.0000, 1.0000, 1.0000) | kink | 012;012;0 | 6 | 0 | 10 |
| 46 | (1.0000, 1.6180, -3.2361) | kink | 2;01;12 | 4 | 0 | 9 |
| 47 | (1.0000, 1.6180, 0.0000) | triple | 1;0;0 | 3 | 3 | 8 |
| 48 | (1.0000, 1.6180, 3.2361) | kink | 2;12;01 | 4 | 0 | 7 |
| 49 | (1.0000, 2.0000, -2.6180) | triple | 2;0;2 | 3 | 3 | 6 |
| 50 | (1.0000, 2.0000, 2.6180) | triple | 2;2;0 | 3 | 3 | 5 |
| 51 | (1.0000, 2.6180, -1.6180) | triple | 1;0;2 | 3 | 3 | 4 |
| 52 | (1.0000, 2.6180, 1.6180) | triple | 1;2;0 | 3 | 3 | 3 |
| 53 | (1.0000, 3.6180, 0.0000) | kink | 1;02;02 | 4 | 0 | 2 |
| 54 | (1.0000, 4.2361, -4.2361) | kink | 12;01;2 | 4 | 0 | 1 |
| 55 | (1.0000, 4.2361, 4.2361) | kink | 12;2;01 | 4 | 0 | 0 |

Exact coordinates (field-element pairs) and the full arc lists
are in census_data.json.
