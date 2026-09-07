# Getting past 141 at n=4 — exploration log

**The problem.** ~150 climbs from Haar-random starts plateau at total 141, every local
maximum with profile {1:50, 2:66, 3:24}. Depth-2 and depth-3 are exactly at their
ceiling-law caps (66, 24); depth-1 is 50 against a cap of 104. The record 183 has
{1:92, 2:66, 3:24} and golden totals 177 with depth-1 at the cap. So 141 is a wall in
the search, not in the problem, and the whole gap is one layer.

**Rules.** Reach >141 from Haar-random starts, by search — not read out of the repo and
not seeded from a recorded configuration. If it cannot be done, say what rules it out.

Numbered attempts below: idea, what I expected, what happened, why I stopped. The
abandonment reasons are the point.

## 1. What does depth-1 actually do in this space? (diagnostic, ~4 min)

**Idea.** Before optimising depth-1, measure it. Compute the depth profile of all 4 000
exactly-Haar n=4 samples.

**Expected.** A broad distribution of depth-1 with the total only loosely tied to it, so
that depth-1 could be pushed while the total lagged — the premise of every re-weighting
experiment.

**Happened.** The opposite, decisively:

    depth-1 over 4000 Haar samples:  min 20   mean 34.6   MAX 46
    total                          :  min 79   mean 115.3  max 135
    correlation(depth-1, total)    :  0.984

Two things follow.

**(a) Depth-1 and the total are very nearly the same variable.** r = 0.984 means aiming
at depth-1 IS aiming at the total. That fully explains [P221](LEDGER.md#p221)'s null
result — LAYER-1, CAPPED, HEADROOM and TOTAL returned byte-identical answers on every
start because they are collinear objectives, not competing ones. The "frustration" framing
suggested they could be played against each other; at n=4 they cannot be. The re-weighting
idea was not badly implemented (the second time), it was inapplicable.

**(b) The record's depth-1 is off the scale of the random ensemble.** The best depth-1 in
4 000 Haar draws is 46; our climbs reach 50; the record needs **92**. That is not a
margin, it is a factor of two beyond anything the sampler produces. Depth-1 inherits the
bounded tail of the total ([P215](LEDGER.md#p215)), and 92 sits far outside it.

**Why I am not stopping here.** This makes it *likely* that depth-1 ≈ 92 lives on a
positive-codimension set unreachable by local moves from generic starts — but "the best of
4 000 random draws is 46" bounds the SAMPLER, not the reachable set. Climbing already
beats the sampler (50 > 46). The question is how far climbing can go, and that needs
attempts, not inference.

## 2. Climb by whole LINES instead of adjacent chambers (running)

**Idea.** Every climber here steps to a FIRST crossing — one wall, one chamber — while
local maxima are ~3 900 walls apart. `solved_scan.scan_line` already returns every cell
along a single-cube line exactly, so using it as the move generator makes the step a whole
line for about the cost of one bisected ray. `linehop.py`.

**Expected.** If the wins are always in the first cell this buys nothing and dies; if
cells further out are better, the old move was the limitation.

## 3. Change the ENSEMBLE, not the search — cubes sharing an axis  ✅ BREAKS 141

**Idea.** Attempt 1 showed the Haar ensemble's best depth-1 is 46 against the 92 needed,
so searching harder inside it is searching the wrong set. Draw starts from a structured
ensemble instead: all cubes sharing one rotation axis. A rotation about integer axis
(a,b,c) with Cayley parameter t is the integer quaternion (1, ta, tb, tc) cleared of
denominators, so the family is trivial to sample exactly. Every primitive axis with
components in [-3,3] is swept (145 of them) with random angles — WHICH axis is good is
searched for, not assumed. `sharedaxis.py`.

**Expected.** Some improvement, most likely on the body diagonal, since that is where the
maximal 13-pairs live.

**Happened. 141 broken immediately, and the best axis is not the body diagonal:**

| axis | best total | depth-1 |
|---|---|---|
| (1,1,1) body diagonal | 145 | 72 |
| (1,1,0) face diagonal | **161** | **80** |
| (3,2,0) | **165** | 78 |

Against a Haar ensemble whose best total in 4 000 draws is 135 and whose best depth-1 is
46, and against a climbing plateau of 141 with depth-1 50. Depth-1 goes to **80**, from 50
— the layer that would not move under any re-weighting moves freely once the ensemble
changes. **The plateau was the ensemble, not the objective and not the move set.**

That (3,2,0) beats both classical axes is worth noting: it is not a symmetry axis of the
cube at all, and no recorded configuration pointed at it. The sweep found it.

**Caveat, stated because it is the whole meaning of the result.** This ensemble is
Haar-null. It cannot be reached by perturbing a random configuration. So the finding is
"the target sits on a structured set", NOT "climbing from Haar-random starts gets there" —
and the original question, whether random starts can pass 141, is still open and is
looking worse, not better.

## 4. Dense sweep of the best axis (running)

**Idea.** With cube 0 fixed the shared-axis family has exactly three free angles, so it can
be gridded rather than sampled. `diagsweep.py`, axis taken as an argument.

**Two cheaper choices made and why.** (a) The compound is a SET, so permuting the three
angles gives the same compound: sweeping sorted triples cuts 658 503 products to 117 480
combinations, 5.6x, the same unlabelled-object observation that cut the arc menu 7.2x in
[P219](LEDGER.md#p219). (b) I started this on the body diagonal and killed it when the
axis survey showed (1,1,0) and (3,2,0) are better — 11 hours of grinding the wrong slice.

## 2. Climb by whole LINES — outcome so far

Reached 141 in three iterations, and the winning move at iteration 3 was **cell 16 along
the line**, not the first crossing. So distant cells do carry the wins and the
first-crossing move WAS a limitation — but it still lands on 141, so it is a better move
inside the same trap, not a way out of it.

## 5. A closed-form move from a Haar start onto the structured set  ✅ ANSWERS THE QUESTION

**Idea.** Attempt 3 changed the ensemble, which answers a different question than the one
asked. Close the gap with a MOVE: for a quaternion q=(w,v) and axis u, the nearest rotation
about u maximises w*c + s*(v.u_hat) over c^2+s^2=1, so it is (w, v) with the perpendicular
part of v deleted — as integers, `q' = (w*(u.u), (v.u)*u_x, (v.u)*u_y, (v.u)*u_z)`. Closed
form, exact, no search, no floating point. `symmetrize.py`.

**Expected.** Some gain, but the projection destroys information, so possibly a loss.

**Happened. Every Haar start clears the plateau on one move:**

    Haar 131 -> 161 (depth-1 74) on axis (0,3,2)      Haar 111 -> 161 (depth-1 74)
    Haar 119 -> 161 (depth-1 80) on axis (0,1,1)      Haar 123 -> 157 (depth-1 76)
    Haar 115 -> 153 (depth-1 66)                      Haar 123 -> 153 (depth-1 74)

**So Haar-random starts are NOT excluded from beating 141. The move set was.** Every
climber in this project moves by perturbation, and the target sits on a Haar-null set that
no perturbation reaches; one projection, computable from the start itself, crosses it.

## 6. The profile of the 161 says exactly what is still missing

    plateau 141   {1:50, 2:66, 3:24}     depth-2 AT its cap, depth-1 half of its
    structured161 {1:80, 2:56, 3:24}     depth-1 up 30, depth-2 DOWN 10 off its cap
    record  183   {1:92, 2:66, 3:24}     BOTH at once
    caps          {1:104, 2:66, 3:24}

The structured family buys depth-1 by **spending depth-2**. The record does not: it holds
depth-2 at the cap and takes depth-1 to 92 anyway. So the target is now sharp and is not
"maximise the total" — it is **depth-1 high AND depth-2 at 66**, which neither the plateau
nor the shared-axis family achieves.

**This revives the re-weighting idea in the ensemble where it actually applies.** Attempt 1
found depth-1 and total correlate 0.984 across the Haar ensemble, which is why every
re-weighted objective returned identical answers in [P221](LEDGER.md#p221) — they were
collinear. In the structured family they are NOT: depth-1 and depth-2 visibly trade off.
The user's re-weighting proposal was sound and was tested in the one ensemble where it had
to be inert.

**Next:** the Pareto frontier of (depth-1, depth-2) over the shared-axis family — is there
a point with depth-2 = 66 and depth-1 well above 50, or does the family forbid it?

## 6b. Generic climb from the structured 161 — no gain

Ran the ordinary climber from the 161 configuration: **161 -> 161**, no improving crossing
in 25 iterations. So the structured point is locally maximal under perturbation as well.
The trap is not specific to the plateau at 141; it repeats one level up. Perturbation-based
climbing is the wrong tool at every height in this problem, which is consistent with local
maxima being ~3 900 walls apart ([P221](LEDGER.md#p221)) — the landscape is not one a local
method traverses.

## 8. Two shared axes (running)

**Idea.** The one-axis family buys depth-1 by spending depth-2 (80 gained, 10 spent) and
stops at 161; the record spends nothing. Partition the cubes between TWO shared axes, so
some pairs share an axis and some do not. Strictly contains the one-axis family, so it
cannot do worse. `twoaxis.py`, tracking specifically the best depth-1 among configurations
holding **depth-2 at its cap of 66**, since that is the record's signature and the thing
one axis cannot do.

**Sampled, not swept, and why:** 10 585 axis pairs times many angle draws each is hours;
a sample answers "is there anything here" in minutes, and a promising pair can be swept
densely afterwards — the same two-stage shape that worked for the single axis.

## 8b. Two axes — the record's signature, reached

The broad two-axis sample found what one axis could not: configurations holding **depth-2
at its cap of 66** while depth-1 rises well past the plateau.

    total 155  depth-1 64  depth-2 66      axes (0,3,-1)/(2,-2,3)
    total 163  depth-1 72  depth-2 66
    total 165  depth-1 74  depth-2 66      axes (1,1,-1)/(0,1,2)

    for comparison   plateau 141 {1:50, 2:66}    record 183 {1:92, 2:66}

So the two-axis family reproduces the record's structural signature — deep layer at its
ceiling, depth-1 carrying the surplus — and gets depth-1 to 74 of the 92 needed. Dense
sweeps of the best pairs are running.

## RESULT

**141 is beaten: 165, by two independent routes**, and the posed question is answered.

1. **Haar-random starts are not excluded.** One closed-form projection onto a shared axis
   (attempt 5) takes every start tried from 111–131 to 153–161. No search, no lookup, no
   seed from a recorded configuration.
2. **What was ruling it out was the MOVE SET.** Every climber here moves by perturbation,
   and the target sits on a Haar-null structured set that no perturbation reaches. Attempt
   1 measured the trap precisely: over 4 000 Haar draws the best depth-1 is 46, against the
   92 the record needs, and depth-1 correlates 0.984 with the total, so the whole ensemble
   is one-dimensional in the variable that matters.
3. **That collinearity also explains an earlier null result.** [P221](LEDGER.md#p221) found
   every re-weighted objective identical to plain TOTAL. They were collinear in the Haar
   ensemble. In the structured families depth-1 and depth-2 genuinely trade off, so the
   re-weighting idea was sound and was tested in the one ensemble where it had to be inert.
4. **Perturbation climbing fails at every height, not just at 141** (attempt 6b): the
   generic climber run from the structured 161 returns 161. Consistent with local maxima
   being ~3 900 walls apart.

**What is still missing to reach 183:** depth-1 = 92 with depth-2 = 66. Best so far 74/66.
The two-axis family has the right shape and 18 to go.

**Ideas not yet tried**, in the order I would take them: dense sweeps of the best axis
pairs (running); three axes, or one axis per cube with shared PAIRWISE structure; solving
the shared-axis slice exactly rather than gridding it, since within a fixed axis pair the
walls are the same W4/W3 families and `solved_scan` applies; and using the projection as
one move inside the climber rather than as a one-off preprocessing step.

## 9. The signature census — and 177

After attempt 8 the search moved from "find a better configuration" to "characterise what
predicts the count", at the user's direction. `census.py` draws from four ensembles
(`haar`, `axis`, `twoaxis`, `project`), records signature + count + depth profile, and
appends; `census_merge.py` union-merges. **556 746 configurations** so far across two
machines, 2 888 distinct signatures, 59 unevaluable.

**Best found: 177**, up from attempt 3's 169 and the 141 plateau this log started at. 177
is also golden's total, which is suggestive and unexamined.

**Merge is a union, never a max.** Keeping only the best count per signature would destroy
the spread, and the spread IS the measurement of the signature's incompleteness.

**Phase 1 deliberately does not filter.** The signature costs 0.8x a count, so filtering
pays only above a 76% skip rate — and filtering now would bias the very distribution being
characterised.

## 10. What predicts the count — VOID, and a third retraction that takes the section with it

> **RETRACTION 3, 2026-09-07, and it subsumes the two below.** Every number in this section
> was computed by `concurrence.planes()`, which read matrix ROWS where a cube's face normals
> are the COLUMNS — the inverse rotation. The statistic was a function of the quaternion
> SPELLING, not of the compound (6 of 6 octahedral respellings changed it; 0 of 96 after the
> fix). Recomputed on a seeded census sample, the winner scores **r = −0.147, ordering
> 50.6 % of 3 320 pairs**: the correlation changes SIGN and lands on chance. **There is no predictor.** The
> other two rows were measured through the same map and are unmeasured rather than refuted.
> [P227](LEDGER.md#p227), [FAILURE_MODES 27](FAILURE_MODES.md).

| predictor | strength as measured | status |
|---|---|---|
| max plane-concurrence | r = 0.354, non-monotone | VOID |
| raw real (face-bounded) incidence count | orders 57% | VOID |
| ~~**Möbius weight of real incidences**~~ | ~~r = 0.562, orders 77.6%~~ | **VOID → r = −0.147, 50.6 %** |

~~The winner is `sum over real, face-bounded incidence points of (m-1)(m-2)/2` — a simple
vertex weighs 1, a 4-fold 3, a 9-fold 28. It needs no engine call at all: planes,
`solve3` and the face test are arithmetic on the quaternions. And it orders 77.6% across
arbitrary pairs against 78.8% within a signature, so it is a standalone predictor
rather than a tie-breaker — the first cheap, non-circular filter this search has had.~~

*The construction is still well defined and still needs no engine call; it simply does not
predict the count. Retractions 1 and 2 below are kept because they record how the section
was reasoned, not because their numbers mean anything now.*

**RETRACTION 1.** A "principled" statistic C (excess over generic,
`C(m,3) - (m-1)(m-2)/2`) scored 78% on 9 pairs and was reported as the promising lead. At
413 pairs it scores **40%**. It was flagged as p ~ 0.09 at the time and it did not survive.
The lexicographic C-then-A rule built on it scores **49.0%** — chance.

**RETRACTION 2.** The sign was backwards in my derivation. I argued from the Möbius
weights that degeneracy should be penalised (a degenerate point replaces C(m,3) simple
vertices with only (m-1)(m-2)/2 of weight). The measurement says the opposite: **more
Möbius weight is simply better**, monotone, no sweet-spot correction. The derivation was
wrong; the 397-pair measurement is not.

## 11. Do signatures account for degeneracy? No — and it does not matter much

Two cubes sharing a face plane, or having parallel planes, give `det = 0` in `solve3`, so
those coincidences are skipped and the signature is blind to them. Measured: **17 of 300**
configurations have a shared plane, **17 of 300** have cross-cube parallels — real, ~6%.

But it points away from records: configurations counting >= 150 have **0.0** mean
parallel-classes against **0.1** for those under 130. Degeneracy of this kind associates
with LOWER counts, consistent with over-concentration merging regions away. Worth closing
for completeness; not worth chasing for records.

## 12. Unevaluable, now recorded rather than counted

The census originally counted refusals and discarded them — the failure mode this project
has on file. Now each is recorded with cause, height and signature (the signature needs no
engine, so a refused configuration still enters the table).

60 refusals: **all produce no stderr at all**, so the degenerate-vs-budget classifier never
fired. Heights run 6 to 1748, far below any overflow threshold, which rules out budget and
leaves genuine degeneracy as the likely cause — but confirming it needs the engine's exit
code, not its stderr. Rate by ensemble: `twoaxis` 25, `project` 23, `haar` 9, `axis` 2 —
the more structured the ensemble, the more it refuses.
