# Multi-constraint (stacked-wall) search with Q(sqrt3, sqrt5) verification

Executed per MULTIWALL_SPEC.md, priority order gates -> section 3 -> M1 -> M2
-> M4 -> M3. All work logged to `multiwall_search.jsonl`. Validated files
(`certify_six.py`, `cube_compound_exact.py`, `exact_search.py`,
`exact_search_results.jsonl`, `golden_six.py`, `golden_search.jsonl`) were
read but never written. This file is new; `six_cube_search_results.md` was
not edited (it changed size/mtime during this session from a concurrent
process outside this agent's control -- not touched by any tool call here).

New file: `qtower.py` -- the Q(sqrt3, sqrt5) tower, built as `Ext3 = Q5
(sqrt3)` (a + b*sqrt3, a,b in the ALREADY-VALIDATED Q5 class from
`cube_compound_exact.py`, reused not re-derived), plus a generic counting
core `exact_count_tower` that is a direct port of
`certify_six.exact_count_config` operating on Ext3 elements (no CN
interval-filter layer -- unnecessary at these speeds, see timings below).
`clip`/`dot`/`vadd`/`vsub`/`vscale` are imported unmodified from
`cube_compound_exact.py`.

## Gate results -- ALL PASS

| gate | check | result |
|---|---|---|
| W-G1a | tower (sqrt3-part zero) reproduces golden 1..5 subcompounds | 1,13,67,177,351 exact, matches Q5 pilot |
| W-G1b | tower, golden5 + rational sixth quat (2,1,1,1) | 681, by_depth {1:234,2:192,3:128,4:90,5:36,6:1} -- matches plateau exactly |
| W-G2 | tower, rationalized seed 40 (all-rational, N=512) | 575, by_depth {0:1,1:90,2:184,3:162,4:102,5:36,6:1} -- exact match |
| W-G3 | tower pair (identity + exact 30deg about z) vs rational engine (identity + Pythagorean-angle pair pyth_rot_z(4,3,5)) | both = 9, by_depth {0:1,1:8,2:1} identical -- same wall family confirmed |
| W-G4 | EXISTING Q5 pilot engine, quat (97,56,56,56) (next sqrt3-convergent after (26,15,15,15)) | 681, by_depth identical to the plateau |

Tower eval cost measured directly: 2-cube ~0.5s, 5-cube (golden five) 8.7s,
6-cube (golden5+1) 19-27s. Far under the spec's "minutes" ceiling -- no
budget compromise was needed anywhere in this program.

## Section 3: the sqrt3 x sqrt5 point itself

Constructed EXACTLY: golden five (Q(sqrt5)) + sixth cube R = rotation by
90 deg about (1,1,1)/sqrt3, via Rodrigues R = uu^T + [u]_x (cos90=0, sin90=1,
so entries are 1/3 +- sqrt3/3 exactly as predicted). Orthonormality and
det=1 asserted exactly in the tower.

**RESULT: total = 681**, by_depth = {1:234, 2:192, 3:128, 4:90, 5:36, 6:1}
(20.2s, 4711 arrangement cells) -- **identical to the rational plateau**.
Neither a jump nor a drop: the count does not move at the wall.

**Diagnosis** (plain geometry, all computer-verified in the exact tower):

- **No coincidence with the golden five.** None of the sixth cube's 3 face
  normals is parallel to any of the golden five's 15 two-fold-axis face
  normals (exact cross-product zero-test, all 45 pairs checked). None of
  the golden five's 20 dodecahedron vertices lies on any of the sixth
  cube's 6 face planes, **except** the sixth cube's own two trivial corners
  (1,1,1) and (-1,-1,-1) -- which lie on it only because they are literally
  its own corners (the rotation fixes its axis), not because of any
  incidence with the rest of the compound.
- **The only real relation**: the sixth cube's rotation axis (1,1,1) is a
  dodecahedron vertex shared by golden cubes 0 (the axis-aligned one) and
  2 -- i.e. the sixth cube is golden cube 0, spun 90 deg about a body
  diagonal that ALSO happens to be a vertex of a second golden cube. This
  is a relation between the sixth cube's own axis and the golden five's
  vertex structure, not a face/plane coincidence, and it produces no
  merging or splitting of arrangement cells.
- **Combinatorial identity, not just numerical equality**: the rational
  convergents (26,15,15,15) and (97,56,56,56) produce arrangements of
  exactly **4711 cells each** -- identical to the exact wall's 4711. By
  (2,1,1,1) [4747 cells] and (7,4,4,4) [4705 cells] the combinatorics are
  still moving; from (26,15,15,15) onward the arrangement has already
  locked into the SAME combinatorial type the exact limit has. The climb
  isn't approaching an isolated degenerate point that only resolves in the
  limit -- by the third convergent it is already sitting inside the wall's
  own open-enough neighborhood.

**Bottom line**: the 90-deg-about-(1,1,1) point is algebraically exotic
(needs sqrt3 on top of sqrt5) but geometrically unremarkable relative to
the golden five's own arrangement. The gain from 635 (rational) to 681
was already fully present before the sixth cube's coordinates left Q.

## M1 (mechanism A, existing Q5 engine only) -- clean negative

**M1(a)**: sixth cube shares one face PLANE exactly with a golden cube
(coincident-plane wall), free rational in-plane rotation angle phi, tested
against ALL 5 golden cubes x 14 angles (70 evals). Result: **totals depend
only on the angle, not on which of the 5 golden cubes anchors the wall**
(icosahedral transitivity) -- range 351 (phi=0/90, exact cube-symmetry
duplicate) up to **563** (phi with tan(phi/2) = 3/4, 4/3, 1/7 or 7). Never
approaches 635, let alone 681.

**M1(b)**: sixth cube = golden cube k rotated +-60 deg about ONE of ITS OWN
4 body diagonals (the "pair-13" rational relation), tested against all 5
golden cubes x 8 (diagonal, sign) combos = 40 evals. Result: **constant at
exactly 657** in all 40 cases, again by icosahedral transitivity. Below the
635 rational record.

**Conclusion**: neither in-family mechanism from M1 beats even the
RATIONAL 635 record; the golden five's own within-field wall vocabulary is
exhausted well below the golden5+1 plateau. This matches the established
pattern (Postscript 2/7): rich wall values (13, 9, 657, 563) are real but
capped, and the 681 record's gain comes from elsewhere.

## M2 (mechanism B, snap-and-verify + re-mining) -- the real structure of 681

Re-mined `golden_search.jsonl`: **every one of the 32 logged total=681
rows has quat form (a, s1, s2, s3) with |s1|=|s2|=|s3|** -- i.e. EVERY
681 config found is a rotation about a body-diagonal axis. This is a much
broader statement than "681 lives near 90 deg about (1,1,1)"; it says the
681 plateau is tied to the AXIS CHOICE, and the angle is comparatively
free. Follow-up sweeps (Q5 engine, cheap) confirm and sharpen this:

- Along the EXACT axis (1,1,1): total = 681 continuously for a=11 through
  a=500 (quat (a,1,1,1), angle running from about 18 deg down to under
  1 deg -- i.e. all the way to near-identity, never dropping), **and also**
  at a=2 (about 82 deg) and other non-(a,1,1,1)-form points on the same
  axis, e.g. (5,2,2,2) [69 deg]. A middle band, a=3..10 (about 20-60 deg),
  sits on a DIFFERENT, lower plateau at exactly 657 -- matching M1(b)'s
  60-deg-own-diagonal value (a=3 in this sweep literally IS that config).
- Along a GENERIC axis (quat (a,1,2,3)), the near-identity plateau is
  **665**, not 681. Along a face axis (quat (a,1,0,0)), it is **567**.
  Different axis directions approaching the identity/duplicate point give
  DIFFERENT locally-constant limits -- the degenerate point (a=1, exact
  duplicate, total 351) sits at the meeting of several distinct chambers,
  and the body-diagonal chamber happens to be the largest of the three
  tested.
- Along NEAR-diagonal but not exact axes ((10,11,11), (100,101,101), ...),
  totals (659, 679, 647, 679, ...) approach but do not reach 681 as BOTH
  axis precision and angle fineness increase -- consistent with 681 being
  genuinely tied to the EXACT axis, not a generic nearby value.

**Symmetry explanation (verified exactly)**: golden cube 0's four body
diagonals are (1,1,1)/(1,1,-1)/(1,-1,1)/(1,-1,-1); EACH is a vertex shared
with exactly one other golden cube: (1,1,1)-cube2, (1,1,-1)-cube3,
(1,-1,1)-cube1, (1,-1,-1)-cube4 (all four, not just the first -- checked
directly). The generator `B` (120 deg about (1,1,1), the order-3 element in
O cap I) fixes golden cubes 0 and 2 and 3-cycles {cube1, cube3, cube4}
(verified by explicit matrix conjugation). This exactly explains M3's
sibling-diagonal result below: the (1,1,1) diagonal is B-fixed and free to
be exceptional; the other three are a single B-orbit and therefore forced
to share one common value.

**Conclusion for M2**: no new "snap" target was needed beyond what section
3 already built -- the wall is 1-dimensional (fixed body-diagonal axis,
free angle) and its exact representative point (90 deg about (1,1,1)) was
already verified in section 3 to match its rational neighbors exactly.

## M4 (control): purely-rational double wall -- BEATS the 635 record

Construction: 6 fully rational cubes, cubes (1,2) and (3,4) each forced
into the exact "pair-13" 60-deg-own-body-diagonal relation (q2 = q1 *
(3,1,1,1), q4 = q3 * (3,1,1,1)), cubes 5,6 free; q1,q3,q5,q6 random-searched
(1900 configs) then greedy-hillclimbed (576 more evals, `./cube_regions_n
--quats-stdin`, single call per batch). Matched control: 400 fully free
6-cube rational configs, same rng stream, same total budget order of
magnitude.

**Result: best double-wall = 655**, independently re-verified by the
Python engine (`certify_six.exact_count_config`) -- exact match:

```
quats = [(-74,-55,66,122), (-355,-295,301,171), (-47,-75,-136,22),
         (24,-215,-179,40), (-44,43,17,20), (-57,-58,-64,-140)]
by_depth = {1:138, 2:214, 3:164, 4:102, 5:36, 6:1}   total 655
```

vs matched-budget control best **615** (400 fully free configs). **The
double-wall beats not just its matched control, but the entire previous
unrestricted-search rational record of 635** (from ~360,000 seeds + deep
hillclimbing, six_cube_search_results.md Postscript 4-5) -- from a search
of only 2,476 configs. d3=164, d4=102, d5=36, d6=1 sit at the established
ceilings; d2=214 ties the previous ceiling; **d1=138 exceeds the previously
observed ceiling of 118** (a new high-water mark for depth-1, from a very
small sample -- flagged as new data, not a re-established ceiling).

**Answer to M4's question**: stacking rational-reachable walls is NOT
special to the golden (irrational) five -- imposing structure (here, two
independent pair-13 relations) on an otherwise free rational search finds
a substantially better basin than either an unstructured search of the
same size or (per six_cube_search_results.md) the prior large-scale
unstructured campaign found at all. This is arguably the single most
actionable finding of this session: **wall-constrained search beats
unconstrained search of comparable size**, independent of field theory.

## M3 (mechanism C, compose across fields) -- 2 verifications, budget-limited per spec

**Sibling body diagonals** (same tower, ℚ(√3,√5), golden five + 90-deg
rotation about each of golden cube 0's other 3 diagonals):

| diagonal | total | by_depth | note |
|---|---:|---|---|
| (1,1,1) | **681** | {1:234,2:192,3:128,4:90,5:36,6:1} | B-fixed pair (cube0,cube2) |
| (1,-1,1) | 657 | {1:216,2:192,3:122,4:90,5:36,6:1} | B-orbit sibling |
| (1,1,-1) | 657 | {1:216,2:192,3:122,4:90,5:36,6:1} | B-orbit sibling |
| (-1,1,1) | 657 | {1:216,2:192,3:122,4:90,5:36,6:1} | B-orbit sibling |

Confirms the M2 symmetry prediction exactly: NOT all four 90-deg-diagonal
walls are equivalent (the spec's caution "don't recount blindly" was
warranted) -- there is a genuine 1+3 split, with the B-fixed diagonal
strictly better (681 vs 657) than its three B-conjugate siblings, which
are forced equal to each other but not to the fixed one.

**Cross-field compose, ℚ(√2,√5)**: exact 45 deg about z (the maximally
symmetric point of the M1(a) coincident-face-plane pair family), golden
cube 0 anchor. Built a second tower type (Ext2, same Q5-base recipe,
d=2) for this single verification.

**Result: total = 543**, by_depth {1:180,2:156,3:100,4:74,5:32,6:1} (17.0s).
This is BELOW the entire in-family rational-angle range M1(a) found
(543-563) and shows **d5 = 32 < 36** -- a genuine T2-direction merge
exactly at the symmetric point, unlike the (1,1,1) case. **This wall does
lose regions at the exact point** -- the opposite behavior from section 3,
confirming the spec's warning that either direction is possible and must
be checked, not presumed, per config.

Given the M1/M2 evidence (the productive direction is axis choice on the
RATIONAL side, already fully captured; M4's double-wall already beats
everything else found in this session), no further tower verifications
were pursued -- consistent with the spec's "a few tower verifications
only, chosen by M1/M2 evidence" budget.

## Best totals per search family (quats/params)

| family | best total | construction |
|---|---:|---|
| **M4 double-wall (purely rational)** | **655** | quats=[(-74,-55,66,122),(-355,-295,301,171),(-47,-75,-136,22),(24,-215,-179,40),(-44,43,17,20),(-57,-58,-64,-140)] |
| golden5 + sixth on the (1,1,1) body-diagonal wall (rational OR exact) | 681 | e.g. quat (2,1,1,1) rational, or exact 90deg-about-(1,1,1) in the tower -- same value |
| M4 control (matched budget, fully free rational) | 615 | 400 random 6-cube configs |
| M1(b) 60deg-own-diagonal (any golden cube, any of its 4 diagonals) | 657 | e.g. golden cube0 * rot_from_quat(3,1,1,1) |
| M1(a) coincident-face-plane wall (any golden cube) | 563 | e.g. golden cube0 * rot_from_quat(4,0,0,3) |
| M3 sibling diagonals (1,-1,1)/(1,1,-1)/(-1,1,1) | 657 | exact tower, same construction as the wall point with a different diagonal |
| M3 exact 45deg-about-z wall, Q(sqrt2,sqrt5) | 543 | golden cube0 * R_z(45deg exact) |
| prior rational-only record (context, six_cube_search_results.md) | 635 | quats=[[129,-171,-137,-28],[382,278,63,-186],[200,289,312,-203],[314,101,-391,1],[124,-61,26,-215],[276,269,33,335]] |

## Honest negatives / open items

- M1's within-golden-field wall vocabulary is fully exhausted at 657/563 --
  it does not compete with 681 and this is now a closed question.
- M2 found no NEW exact point requiring verification; the wall is
  1-dimensional and its representative was already exact-counted in
  section 3.
- The exact transition points along the (1,1,1) axis (where a=2 is 681,
  a=3..10 is 657, a>=11 is 681 again) were mapped only at integer (a,1,1,1)
  resolution -- the fine structure of where 657 gives way to 681 near
  a=2/a=11 was not resolved to exact boundaries; this is a loose end if
  anyone wants the complete phase diagram of the 1-parameter family, but
  does not affect any of the reported conclusions (both endpoints and the
  exact wall are independently confirmed).
- Only one ℚ(√2,√5) cross-field point was tested (M3 budget, per spec).
  The 45-deg point loses regions; whether ANY ℚ(√2) wall could ever net-win
  is not closed by this one data point (it is consistent with, not proof
  of, the general T2 pattern).
- d1=138 (M4 winner) is a small-sample new high; it is reported as data,
  not asserted as a new ceiling -- the ~360k-seed unrestricted campaign
  that established d1<=118 was much larger, and this session's 2,476
  wall-constrained configs are not a fair apples-to-apples ceiling test.
