# Canonical maximiser representatives

Every known maximiser, as an exact quaternion tuple in a form the engines accept,
with the command that reproduces its count. Nothing here is derived at read
time: paste a command and the engine prints the record.

Quaternion conventions: integer 4-tuples are rational rotations for
`cube_regions_n`; `a:b` means a + b·√d for `cube_regions_q2` / `_q2w` with
`--d d`. A cube is R·[−1,1]³ with R the rotation of the quaternion, all cubes
centred at the origin, and each quaternion matters only up to scale and up to
right multiplication by the cube's 24 symmetries.

---

## n = 2, max 13

Rotation about a body diagonal by any angle except 0 and ±120°. A whole arc, so
any of these is as canonical as any other; the count is 13 at every one.

    ./cube_regions_n --quats "1,0,0,0;3,1,1,1"

The arc is Cayley t·(1,1,1); measured 13 at t = 1/5, 1/4, 1/3, 2/5, 1/2, 3/5,
2/3, 3/4, 3/2, 2, 3 and **punctured at t = 1**, where the rotation is a cube
symmetry and the count drops to 1. Perpendicular to the arc the count is 9.
Symmetry order 12. One combinatorial type along the whole arc.

## n = 3, max 67 — two classes, both irrational

Both are {I, R, R²} with R a 120° rotation about the dihedral-family axis
n(ψ) = (sin ψ, cos ψ, 0), i.e. R = (1/2, (√3/2)·n) as a unit quaternion.

**Octahedral**, ψ = arcsin(1/√3), so R = (1, 1, √2, 0) in ℤ[√2]:

    printf '1:0,0:0,0:0,0:0;1:0,1:0,0:1,0:0;-1:0,1:0,0:1,0:0\n' \
      | ./cube_regions_q2 --d 2 --quats-stdin
    # -> 67, by_depth {1:48, 2:18, 3:1}, symmetry order 24

**Golden**, tan ψ = φ², so sin ψ = φ/√3 and (√3/2)cos ψ = √((3−√5)/8) =
(√5−1)/4 — the nested radical resolves because (3−√5) = (√5−1)²/2. Hence
R = (2, 1+√5, −1+√5, 0) in ℤ[√5]:

    printf '1:0,0:0,0:0,0:0;2:0,1:1,-1:1,0:0;-2:0,1:1,-1:1,0:0\n' \
      | ./cube_regions_q2 --d 5 --quats-stdin
    # -> 67, by_depth {1:48, 2:18, 3:1}, symmetry order 6

Their per-label profiles are IDENTICAL ({1,16,16,6,16,6,6,1}), so per-label
cannot separate them. Their symmetry orders differ, 24 against 6, which proves
non-congruence outright — an invariant independent of Theorem R's μ.

## n = 4, max 183

    ./cube_regions_n --quats "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"
    # -> 183, by_depth {1:92, 2:66, 3:24, 4:1}, symmetry order 3 (C₃)

Pair label (9,9,9,13,13,13); O-reduced pair angles three at 43.004° and three at
46.826°. All five independent climbs that reached 183 give this class.

## n = 5, max 393  ·  n = 6, max 723 and 727  ·  n = 7, max 1217  ·  n = 8, max 1891

All share the same five-cube base:

    BASE = 4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1

    ./cube_regions_n --quats "$BASE"                              # 393, sym 3
    ./cube_regions_n --quats "$BASE;5,2,2,2"                      # 723, sym 3
    ./cube_regions_n --quats "$BASE;7,14,1,-5"                    # 727, sym 1
    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4"         # 1217, sym 1
    ./cube_regions_n --quats "$BASE;7,14,1,-5;4,-3,-4,-4;3,-3,3,-8"  # 1891, sym 1

### 727 is a continuum, so no single representative is canonical

727 holds on arcs. The one fully mapped runs along Cayley direction (1,−3,−6)
through (19/3, −7, −11); with P(s) = that point + s·(1,−3,−6) as the sixth cube,
the count is 727 for s ∈ [9/4, 3], with 721 at s = 2 and 723 at s = 13/4. Some
convenient members:

    ./cube_regions_n --quats "$BASE;24,203,-321,-570"   # s = 17/8
    ./cube_regions_n --quats "$BASE;6,53,-87,-156"      # s = 5/2
    ./cube_regions_n --quats "$BASE;3,28,-48,-87"       # s = 3

and 727 in ANY quadratic field, by taking s = 5/2 + √d/100, which stays inside
the arc for every d ≤ 97:

    printf '4:0,1:0,1:0,-1:0;3:0,3:0,7:0,3:0;5:0,-1:0,-5:0,-5:0;2:0,1:0,1:0,1:0;1:0,1:0,1:0,1:0;300:0,2650:3,-4350:-9,-7800:-18\n' \
      | ./cube_regions_q2w --d 3 --quats-stdin
    # -> 727 ; works identically for d = 2, 5, 6, 7, 10, 11, 97, ...

Three further arcs are known, pairwise skew with this one and with each other:

| arc | Cayley direction | through | fields on it |
|---|---|---|---|
| A | (1, −3, −6) | (19/3, −7, −11) | 13, 1093, 2741 |
| B | (1, 1, −4) | (4/35, 2/5, −41/35) | 1614, 25561 |
| C | (1, −3/2, 9/4) | (245/29, −295/29, 428/29) | 1785, 5305 |
| D | the record's own wall line | (7, 14, 1, −5) | rational |

### 723 is also positive-dimensional

Tangent (1,1,1) at Cayley (2/5, 2/5, 2/5) — the sixth cube sliding along the
shared C₃ axis. Along it 723 holds on a UNION of intervals, the longest
s ∈ [9/32, 35/32], punctured by dips to 711, 699 and 687.

---

## Gate

Any rebuilt engine should reproduce all of these before its results are
believed. `n4_program.py gate` checks the rational subset; the two 67s and the
ℚ(√d) 727 above extend it to the quadratic-field engines, which the existing
gate does not cover.
