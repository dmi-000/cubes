# Theorem S — the subset-to-whole inequality, proved for all n

Status: **proved** (2026-09-07), conditional on nothing new. Both geometric
ingredients are existing project theorems; the two new steps are combinatorial.
Gate: `anchor_split.py`, `anchor_gate_*.jsonl`.

This closes [OQ 31] and, at n = 4, the inequality [P264]/[P265] identified as the
single remaining obstacle to the n = 4 ceiling law.

## Statement

For n >= 3 unit cubes with a common centre, indexed by S,

    sum over the (n-1)-subsets T of S  of  d_(n-2)(T)   <=   6n(n-2)  +  d_(n-1)(S).

At n = 4 this reads **`sum_T d2(T) <= 48 + d3`**, exactly the inequality of [P264].
At n = 3 it reads `sum over the three pairs of d1(pair) <= 18 + d2`.

## Ingredients (both already proved in this project)

**FIB** (fibration lemma, PROOF_67 section 2). For a configuration on an index
set A, its bounded regions of depth |A|-1 -- inside every cube of A but one --
biject with the connected components of a spherical set. Writing r_i(u) for the
radial reach of cube i in direction u, and for C in A and R a set of other cubes

    S_C(R)  =  { u in S^2 : r_C(u) < r_i(u) for every i in R }     (open)

the statement is `d_(|A|-1)(A) = sum over C in A of #pi0(S_C(A \ {C}))`.

**ANCHOR** ([P33] Theorem 1, unconditional, all n). Every connected component of
`S_C(R)` contains a face-centre direction of C. Hence `#pi0(S_C(R)) <= 6`, which
is the l = 1 ceiling law `d_(n-1) <= 6n`.

Everything below is about ONE cube C. Fix C, let `F` be its six face-centre
directions, and for `R` a set of other cubes write

    c(R) = #pi0(S_C(R)),   k(R) = |F n S_C(R)|,   delta(R) = 6 - c(R).

ANCHOR gives `c(R) <= k(R) <= 6`, so the deficit splits into two nonnegative parts

    delta(R)  =  m(R)  +  s(R),      m(R) = 6 - k(R),   s(R) = k(R) - c(R)

-- `m` counts anchors LOST (some cube of R reaches inside that face centre) and
`s` counts anchors SHARED (two anchors in one component). The whole proof is that
these two behave oppositely under adding cubes to R, and that each is controlled
by the (n-1)-subsets for a different reason.

## Lemma 1 (anchors intersect; the reason the argument exists)

For u in F: `u in S_C(R)` iff `u in S_C({i})` for every i in R. Immediate from
the definition. Writing `alpha_i = F \ S_C({i})` for the anchors of C killed by
cube i acting alone,

    m(R) = | union of alpha_i over i in R |.

This is the step that a region count cannot imitate. Non-emptiness of a set is
NOT compatible with intersection -- `K n B` may be empty though `K` and `B` are
not -- which is why [P265]'s attempt to bound region counts before merging lost a
factor of three. Membership of a FIXED six-point witness set is compatible with
intersection, and ANCHOR is exactly what supplies the fixed witness set.

## Lemma 2 (anchor loss is subadditive over the (n-1)-subsets)

If `|R| >= 2` then for any two distinct `m, m'` in `R`,

    m(R)  <=  m(R \ {m})  +  m(R \ {m'}).

*Proof.* `union_{i in R} alpha_i = (union_{i != m} alpha_i) u alpha_m`, and
`alpha_m` is one of the sets united in `m(R \ {m'})` because `m != m'`. []

## Lemma 3 (sharing is monotone under adding cubes)

If `R' is a subset of R` then `s(R) <= s(R')`.

*Proof.* `S_C(R)` is a subset of `S_C(R')`. Put `G = F n S_C(R')` and
`G' = F n S_C(R)`, so `G'` is a subset of `G`. Two anchors joined by a path
inside `S_C(R)` are joined by that same path inside `S_C(R')`, so the partition
of `G'` by `S_C(R)`-components REFINES the restriction to `G'` of the partition
of `G` by `S_C(R')`-components; hence it has at least as many blocks. By ANCHOR
every component of either set carries an anchor, so `c` counts blocks exactly:
`c(R) = #blocks_R(G')` and `c(R') = #blocks_{R'}(G)`. Therefore

    s(R) = |G'| - #blocks_R(G')  <=  |G'| - #blocks_{R'}(G').

Finally `X -> |X| - #blocks_{R'}(X)` is nondecreasing as X grows inside G: adding
one point raises `|X|` by 1 and the block count by 0 or 1. (It is the rank
function of the partition matroid of the `S_C(R')`-component relation.) Applying
that with `X = G'` inside `G` gives `<= |G| - #blocks_{R'}(G) = s(R')`. []

Lemmas 2 and 3 pull in opposite directions, and that is the content: intersecting
with one more cube can only LOSE anchors (m grows) and can only SPLIT components
(s shrinks). The proof spends the second against the first.

## Theorem (per cube)

Let `R = S \ {C}`, so `|R| = n-1 >= 2`. Then

    sum over m in R of c(R \ {m})   <=   6(n-2)  +  c(R).

*Proof.* Pick any two distinct `m1, m2` in `R`. Then

    delta(R)  =  m(R) + s(R)
              <= [ m(R\{m1}) + m(R\{m2}) ] + s(R\{m1})        (Lemma 2, Lemma 3)
              <= sum over m in R of [ m(R\{m}) + s(R\{m}) ]     (dropped terms >= 0)
              =  sum over m in R of delta(R\{m}).

Substituting `delta = 6 - c` and rearranging:
`6 - c(R) <= 6(n-1) - sum_m c(R\{m})`. []

## Theorem S

Sum the per-cube theorem over the n choices of C and apply FIB to each side.
On the left, the pair `(C, m)` with `C != m` contributes `c(S \ {C, m})`, and
grouping by `m` gives `sum over C != m of #pi0(S_C(S\{m}\{C})) = d_(n-2)(S\{m})`,
i.e. the (n-1)-subset omitting m. On the right, `sum_C c(S\{C}) = d_(n-1)(S)`. []

## Where the slack is, and why refutation kept failing

The proof discards `sum_m m(R\{m})` down to two terms and all but one `s`. So
equality needs at most two nonzero `m` and one nonzero `s` per cube: the bound is
tight only when almost nothing is lost anywhere. At the n = 4 record every
`c = k = 6`, every `m = s = 0`, and the per-cube statement is `18 <= 12 + 6`,
tight. As soon as `d3` falls, some `c(R) < 6`, which by ANCHOR means an anchor was
lost or shared -- and the SAME loss appears in the subsets, driving the left side
down at least as fast. That is precisely the positive coupling [P265] measured as
slack growing monotonically (0, 4, 6, 11, 22, 23) as `d3` fell, and it is why
3 339 directed refutation attempts found nothing: the refutation asks for a loss
in the whole that is invisible in the parts, and Lemma 3 says there is no such
loss.

## What this closes and what it does not

**Closes.** [OQ 31]. `sum_T d2(T) <= 48 + d3` at n = 4, unconditionally, and its
generalisation to all n. The first subset-to-whole inequality in the project.

**Does not close by itself.** The chain from here to `max(4) <= 195` is [P262]/
[P263]/[P264]'s, and two of its steps are not this theorem's to give:

- `W1 = 2(d3 - 2)` is used as an EQUALITY to convert the inequality into
  `W0 <= 84`, and it FAILS GENERICALLY. **CORRECTED 2026-09-08 ([P271]):** an
  earlier version of this section said it was exact on 1 441 of 1 449 and failed
  only on a degenerate residue. That count came from [P263]'s BUDGET-ATTAINING
  slice, which is not generic. On 247 blind non-degenerate n=4 configurations the
  needed step `W1 >= 2(d3-2)` fails **2 of 211 (0.9 %) on genuinely simple
  configurations, worst deficit −4**, and 15 of 36 (41.7 %) on coincident ones
  ([P272]; an intermediate figure of "17 times, 6.9 %" was the POOL, not the
  geometry). The CONCLUSION `W0 <= 84` was violated 0 times in all 247 and is
  exactly attained at the record -- so the target stands and this ROUTE to it
  does not. [P273] reduces what is left to `w <= B`: the swallowing deficit
  never exceeds the budget deficit, measured running 5-19x the other way.
  [P274] then PROVES `W0 <= 82 + 2(tau3 + c3)` from Theorem S (0 violations in
  263; equal to 84 exactly when `tau3 = 0, c3 = 1`), and shows both of those
  conjuncts FALSE on simple non-degenerate configurations -- so what is left is a
  trade, not a conjunct: whenever `tau3 + c3 >= 2` the budget must be depressed
  by at least the `2(tau3 + c3 - 1)` the bound gives away. See [OQ 32].
- `d2 <= 66` and `d1 <= 104` both assume `c_ell <= 1` at the relevant level,
  which is [OQ 30] and is where [P259]'s antipodal dichotomy leaves a gap.

So: **the inequality is now a theorem; `max(4) <= 195` is not yet one.** What
stands between them is a degenerate-case bookkeeping step and [OQ 30], both of
which are narrower than the inequality was.

## Verification

`anchor_split.py` recomputes every quantity above by a THIRD route, independent
of both the C++ engine and the spherical picture: `K \ C` for `K` the
intersection of the cubes in R is the union of the six open convex pieces
`K n {outside face f of C}`, and a union of convex sets has one component per
component of its intersection graph -- so `c(R)` is 6 node-LPs plus 15 edge-LPs,
exact over `Fraction` (`exactlp.feasible_strict`). The gates are:

- **FIB**: `sum_C c` must equal the engine's `d3`, and `sum_{C in T} c` the
  engine's `d2(T)`, on every configuration. This is the theorem-as-oracle check
  on the bookkeeping, not on the conclusion.
- **ANCHOR**: `c == blocks` -- every component carries an anchor -- checked
  directly rather than assumed.
- **Lemma 2, Lemma 3, the per-cube theorem** and the global inequality, each
  counted separately so that a pass cannot hide which step was never exercised.

The pool (`anchor_pool.py`) is chosen for the parts, not for convenience: the
record and generic high-height samples have `c = k = 6` everywhere and exercise
NONE of the three steps, so a pool of those would be a pass that means nothing
(FAILURE_MODES 29). It is weighted to low-height configurations (anchors eaten,
components merged), the shared-normal locus ([P33]'s self-exclusion case, the
hardest for ANCHOR), and record neighbourhoods at four scales (the tight end).

### Results (2026-09-07)

**591 configurations, ZERO violations of any of the six gates.** 225 at n = 3 (complete
pool), 264 at n = 4 (including all five [P263] degenerate exceptions, which are `72 = 72`
tight), 71 at n = 5. Lemma 3 is the thinnest part of the n = 5 evidence,
exercised in only 16 cube-instances there.

Exercised, in cube-instances: Lemma 2 in 912, Lemma 3 in 710, a nonzero deficit somewhere
in 1 505, the per-cube inequality tight in 775. Tight WITH a nonzero deficit in 79 -- the
slack accounting is therefore checked where the lemmas do work, not only where they are
vacuous. Lemma 2 binding (equality with its two-term bound) in 175, Lemma 3 in 53.

Strictly stronger than the free bound `Σ_T d2(T) <= 4 x 18 = 72` in 179 of 263 n = 4
configurations, by up to 24.

Reproduce: `python3 anchor_pool.py 1 40 | python3 anchor_split.py --stdin` and
`python3 anchor_report.py`.
