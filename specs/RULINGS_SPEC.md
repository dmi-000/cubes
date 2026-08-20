# RULINGS_SPEC — enumerate the rulings, solve each

METHODS.md path 1. Every wall (W3 and W4 alike) is a signature-(2,2) quadric in
the free cube's Cayley space, hence doubly ruled, and a straight line in Cayley
space is a one-parameter family of rotations — the same object as every
maximiser arc in this project. One ruling has ever been done (2026-08-10, arc
A's end point). This spec makes it systematic.

The verb is **solve**, not sweep: enumerate over walls and rational points on
them, and along each resulting ruling use METHODS.md §1 — solve for every wall
crossing and evaluate once strictly between consecutive roots. Never grid-sample
a ruling; that is exactly the lapse this run exists to correct.

Deliverables: `rulings.py`, `rulings_data.json`, `rulings_report.md`,
`rulings.log`. Add files only — do not edit LEDGER.md, METHODS.md,
MAXIMISER_TAXONOMY.md or any existing script.

## 1. The wall forms

Cayley vector `v = (x, y, z)`; `M(v)` the unnormalised rotation and
`N = 1 + x² + y² + z²`, both exactly as built in `wall_params.line_polys` (reuse
that entry layout — same signs, `M[k][i]` is row k, column i).

**W4** — a free-cube face plane passes through a base triple point `p`:

    F(v) = Σ_k p_k · M[k][i](v)  −  σ · N(v)        i ∈ {0,1,2}, σ ∈ {+1,−1}

quadratic in `(x, y, z)`. Homogenise with `w` to `F_h(x,y,z,w) = uᵀ Q u`,
`u = (x,y,z,w)`, `Q` symmetric 4×4 over ℚ.

**W3** — a free-cube edge meets a base crossing line `(p_line, d_line)`. With
`D = 2·M[:,a]` and `P = sb·M[:,b] + sc·M[:,c] − M[:,a]` (the twelve edges as
enumerated in `wall_params.w3_params`):

    G(v) = det[ D , d_line , N·p_line − P ]

is degree 4 and carries a factor `N`, which is strictly positive and contributes
no real points. Divide it out **exactly** (remainder must be 0 — assert it), then
homogenise the quadratic quotient the same way.

Use sympy for the multivariate algebra; keep every coefficient a `Fraction` or
sympy `Rational`. No floats in any decision anywhere in this spec.

## 2. The rulings

At a rational point `p₀` on the wall (`F_h(p₀,1) = 0` exactly — assert), a
direction `d = (dx,dy,dz,0)` rules the wall iff the line `p₀ + s·d` lies in it:

    F_h(p₀ + s·d) = F_h(p₀) + 2s·(p₀ᵀ Q d) + s²·(dᵀ A d)

with `A` the top-left 3×3 block of `Q`. So `p₀ᵀ Q d = 0` (linear, 2-dimensional
rational solution space) and `dᵀ A d = 0`. Parametrise the linear solution space
by a rational basis `e₁, e₂`, substitute `d = α e₁ + β e₂`, and get a binary
quadratic `a α² + b α β + c β²`. Its roots are rational iff `b² − 4ac` is a
perfect square (handle `a = 0`, and the degenerate identically-zero case, which
means the wall contains a whole plane through `p₀` — record it, don't crash).
Signature (2,2) guarantees both roots are real.

Record for every wall: the two ruling directions, and whether each is rational.
Only rational rulings can be pushed through the integer engines; count the split
(it is one of the report's headline numbers).

## 3. What to enumerate

A rational root of an existing catalogue line is a rational point on a wall, and
`wall_params` already produces those. So:

For each line below, take every W4/W3 root, keep the ones that are exactly
rational with denominator ≤ 10⁶, and for each identify **which** wall conditions
vanish there exactly (scan all conditions and test exact vanishing at `s`, the
way `wall_stratum.py` does it for W4; do the same for W3). Several walls may be
active at one point — each gives its own pair of rulings.

Lines (`BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]`, the 393
base; catalogue via `solve_ends.catalogue(base)`):

| label | base | a₀ | d |
|---|---|---|---|
| arcA (727) | BASE | (19/3, −7, −11) | (1, −3, −6) |
| 723 loop | BASE | (0, 0, 0) | (1, 1, 1) |
| n=7 1217 | BASE+[(7,14,1,-5)] | (−3/4, −1, −1) | (1, 0, 0) |
| n=8 1895 | BASE+[(7,14,1,-5),(4,-3,-4,-4)] | (−1, 1, −61/24) | (0, 0, 1) |

Dedupe (wall identity, point) pairs. If two points give the same wall, keep both
only if their rulings differ.

## 4. Solving each ruling

`exact_chambers.decompose(base, p₀, d_ruling, lo, hi, label)` already does it —
call it, do not reimplement. Window `s ∈ (−4, 4)` (yesterday's, so G1 compares).
Capture its return value plus the printed decomposition.

Per ruling record: number of W4/W3 roots on the line, roots inside the window,
chamber count, the count in each chamber, how many chambers were unevaluable,
the maximum count, and whether the count is constant.

**Unevaluable chambers are reported as unevaluated, never as count changes**
(FAILURE_MODES.md; the wide engine overflows on chambers narrower than ~10⁻⁷).

## 5. Gates — run first, print PASS/FAIL, stop on FAIL

- **G1 (regression, the important one).** Base `BASE`, arc A. The W4 wall from
  triple point `(−11/19, −31/19, −1/19)` through the arc-A end point
  `p₀ = a₀ + (19/6)·d`. Expect: `F(p₀) = 0` exactly; two real ruling directions,
  one rational and equal up to scale to `(−2/5, 3/5, 1)`, one irrational; and
  decomposing along the rational one over `(−4, 4)` gives **863 W4 + 3184 W3
  roots on the line, 10 inside, 11 chambers, count 725 in all eleven**.
- **G2.** For every ruling used: `F_h(p₀ + s·d) ≡ 0` as a polynomial in `s` —
  all three coefficients exactly zero.
- **G3.** Signature of every wall form is exactly (2,2), computed exactly (LDLᵀ /
  inertia over ℚ, not eigenvalues in floating point). Report exceptions as data;
  MAXIMISER_TAXONOMY.md §1a claims 360/360 W4 and 30/30 W3.
- **G4.** The W3 division by `N` is exact for every W3 wall used.

A gate that passes in implausibly little time, or whose two sides are identical
strings, is a bug, not a pass — check the timing and the actual values
(FAILURE_MODES.md §13a; this project has shipped a vacuously-passing gate before).

## 6. Budget, caching and logging

**Cache the expensive step before launching** (METHODS, *Cache the expensive step*).
Every campaign here has one costly intermediate and several analyses that will
want it; keep it on disk keyed by its input so the run can be killed, corrected
and relaunched for the price of the correction. Incremental output protects what
a run produced, the cache protects what it computed to get there.

Time one `decompose` call first, then choose how many rulings per line fit in
**40 minutes total**, spread across the four lines rather than exhausting the
first. Append each ruling's result to `rulings_data.json` as it completes, and
progress to `rulings.log`, so an interrupted run still leaves data. State the
coverage achieved (rulings solved / rulings available) in the report — an honest
partial is worth more than a padded total.

## 7. The report

`rulings_report.md` answers, with numbers:

1. **Is the count constant along every rational ruling?** Yesterday's single
   instance said yes (725 in all 11 chambers, 10 wall crossings registering
   nothing). One instance is not a law.
2. **Does any ruling reach a count above its line's record** (727 at n=6, 1217 at
   n=7, 1895 at n=8)? If so this is a new record — re-verify it with BOTH engines
   (`cube_regions_n` and `cube_regions_q2w --d 0`) and flag it at the top of the
   report. Do not bury it.
3. **The rational/irrational ruling split** across all walls examined.
   **CORRECTED 2026-08-11, mid-run:** the spec originally predicted "one rational
   ruling and one irrational" at a rational point, repeating a claim made on
   2026-08-10 from the arc-A wall. That is impossible. Both directions are roots
   of a binary quadratic with rational coefficients, so by Vieta one rational root
   forces the other — the two rulings at a rational point are BOTH rational (square
   discriminant) or a conjugate irrational PAIR, never one of each. The arc-A wall
   itself has both rulings rational on all three active branches (discriminants
   64/729, 64/961, 16/841). The real question, and what this run measures, is how
   often the discriminant is a square — i.e. whether these walls are split over ℚ
   generally or only at the points we happen to land on.
4. Anything the rulings do that the catalogue lines do not: chamber counts,
   whether rulings stay inside one wall-chamber, wall types crossed.

Report what the run actually shows, including negatives. A ruling that carries a
boring constant count is a result; an inflated claim is not.
