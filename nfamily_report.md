# N-FAMILY report — does the dihedral/big family help at n > 3?

Executes `NFAMILY_SPEC.md`. Answer up front: **no** — the family is a rich
exact-coincidence scaffold, and it already *is* buried inside the n=4/5/6
records (Q3's headline result), but as a *search space to maximize over*
it falls further and further behind the true records as n grows (deficit
8 at n=4, 58 at n=5, 108 at n=6). Full numbers, gates, and an honest
coverage statement below.

## The exact arithmetic (new, not in prior postscripts)

Derived and verified symbolically (sympy, one-off use — see chat) before
any numeric work: the relative rotation between family members j and k
depends **only** on (Δθ = θ_k − θ_j, ψ), and is *exactly* the Rodrigues
rotation by angle Δθ about the fixed axis n(ψ) = (sinψ, cosψ, 0):

```
Rel(Δ, ψ) = [ cosΔ·cos²ψ + sin²ψ,     cosψ·sinψ·(1−cosΔ),   cosψ·sinΔ ]
            [ cosψ·sinψ·(1−cosΔ),     cosΔ·sin²ψ + cos²ψ,  −sinΔ·sinψ ]
            [ −cosψ·sinΔ,             sinΔ·sinψ,             cosΔ     ]
```

Since a global rotation of the whole compound never changes region counts,
WLOG set θ₁ = 0 (cube 1 = identity gauge); then cube k's matrix is exactly
`Rel(θ_k, ψ)`. This is a *much* simpler representative of the family than
the original A/B/ŝ frame (`dihedral_scratch/bigfamily.py`) — no irrational
face-axis vectors ever appear, confirming the spec's "key arithmetic fact"
directly: Pythagorean ψ and θ's ⇒ every cube's matrix is rational ⇒
integer quaternions after clearing denominators, in ONE common frame,
with **no compounding needed for independent (non-chain) phases** —
Δθ_k = θ_k directly when θ₁=0, so random-phase-tuple configs stay small
regardless of n; only literal *chains* θ_k = k·a compound denominators
(≈ r_a^k), which caps chain length in practice (see coverage note).

Code: `nfamily_common.py` (exact core: `PyAngle`, `rel_matrix`,
square-root-free `matrix_to_quat_exact` — a Cayley-style extraction, not
textbook Shepperd, so G0 holds unconditionally for *any* rational rotation,
not just family members — `exact_pair_crossings`, `family_axis_test`).

## Gates

All three gates pass (`nfamily_gates.py`, full transcript in
`nfamily_gates.out`):

- **G0** (exact round-trip): chain triple a=asin(3/5)=36.8699°,
  ψ=asin(4/5)=53.1301°. All three matrices pass orthonormality+det=1 and
  quat→matrix round-trips bit-for-bit exact (`fractions.Fraction`, no
  floats). Quats: (1,0,0,0), (15,4,3,0), (20,12,9,0). **PASS**.
- **G1** (two-engine agreement): same n=3 chain — C++ `cube_regions_n`
  and `certify_six.exact_count_config` both give **43** = {1:26, 2:16,
  3:1}. One n=4 family config (chain extended to k=0..3) — both give
  **143** = {1:64, 2:54, 3:24, 4:1}. **PASS** (exact match, both totals
  and full depth histograms).
- **G2** (record reproduction): `cube_regions_n` on the ledger's 723 quats
  (`4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2`) reproduces
  **723** = {1:210, 2:216, 3:164, 4:96, 5:36, 6:1} exactly. **PASS**.

## Q3 — do the records already contain family structure? (answered first; it shapes the reading of Q1/Q2/Q4)

Two independent exact tests per pair (no floats): (a) interior edge-edge
crossing count (`nfamily_common.exact_pair_crossings`), (b) a **new**
direct confirmation test derived here — a pair (Mi,Mj) is in family
position iff the relative rotation R=Mi^T·Mj, after searching the cube's
24-element own-symmetry relabelings, has R[0][1]==R[1][0] exactly (the
antisymmetric part of R has zero component along cube i's own axis; this
falls straight out of the Rel(Δ,ψ) closed form above — its rotation axis
always has zero third component). The two tests agreed on **all 34 pairs
checked, zero mismatches** (`nfamily_q3_records.py`, `nfamily_q3_records.json`):

| n | record | pairs in family position | crossings pattern |
|---|---|---|---|
| 3 | 67 (octahedral, ℚ(√2) witness) | **3/3** | all 10 |
| 4 | 183 | **6/6 (all pairs)** | all 6 |
| 5 | 393 | **10/10 (all pairs)** | all 6 |
| 6 | 723 | **12/15** | 12 pairs @ 6, 3 pairs @ 0 |

**n=3 caveat, stated honestly.** README lists the 67 record's field as
ℚ(√2)/ℚ(√5) — it has **no integer-quaternion representative** (unlike
n=4/5/6). Postscript 9 identifies the octahedral witness as S_oct=Rx(45°)
C-orbited about (1,1,1); this is *literally* the family at ψ=arcsin(1/√3)
(irrational, not Pythagorean), so the spec's "integer quats" framing
doesn't apply verbatim. Rather than skip it, both tests were redone in
exact ℚ(√2) arithmetic (reusing the validated `slide3_q2.py` field class,
read-only) and independently reproduce the ledger's "30 interior
crossings" as 10/pair × 3 pairs — the first *exact* (not 1e-16 numeric)
confirmation of that number.

**The finding.** The 183 and 393 records are not "mostly family, with
some free cubes" — **every single pair** is in family position (some
common axis + equal tilt, not necessarily the literal (1,1,1) axis — the
axis test is axis-agnostic). The 723 record is 12/15: cubes {0,1,2,3,4}
form a fully-family-position 5-clique (this is exactly the 393 record,
consistent with 723 ⊃ 393 from Postscript 16), and cube 5 is family-linked
to cubes 3,4 only, generic (0 crossings) against 0,1,2. This sharpens the
ledger's existing "723 contains a C₃ orbit about (1,1,1)" observation into
an exact, exhaustive, pairwise fact: **the records are built almost
entirely out of family pairs**, glued together — the open question this
reframes is not "does the family appear in records" (yes, overwhelmingly)
but "why can't *purely* family constructions reach as high" (Q1's answer).

## Q1 — how high do family counts go at n=4/5/6?

Sweep: 9,218 exact-integer-quaternion configs (`nfamily_sweep.py` →
`nfamily_results.jsonl`) — 234 chain configs (θ_k=k·a, all feasible
(a,ψ) pairs from a 33-point Pythagorean menu, filtered to the C++
engine's |quat component|≤512 cap), 8,966 independent-random-phase
configs (~3,000/n), 18 finer-resolution chain configs (a from primitive
Pythagorean triples up to r≤400, at the two winning ψ), plus up to 6
rounds of single-coordinate neighbor hill-climbing per n. Runtime ≈115s
on ≤4 cores (well under the 10k–50k / ≤4-core budget — stopped once the
maxima repeated across multiple independent hits and neighbor search
stalled).

| n | family best (verified) | record | cap-sum bound | deficit vs record | vs cap-sum |
|---|---|---|---|---|---|
| 3 | 67 (=record, at the two irrational special points) | 67 | 67 | 0 | matches (Postscript 23: cap-sum tight at n=3) |
| 4 | **175** | 183 | 195 | **−8** | −20 |
| 5 | **335** | 393 | 429 | **−58** | −94 |
| 6 | **615** | 723 | 801 | **−108** | −186 |

Best members (quats, verified against the Python oracle
`certify_six.exact_count_config` — both engines agree exactly on total
*and* full depth histogram):

- **n=4, total 175**, chain a=71.0754°, ψ=36.8699° (≡ψ=53.1301° by the
  ψ↔90−ψ mirror symmetry, see Q2): quats `(1,0,0,0),(7,3,4,0),(12,21,28,0),
  (-91,183,244,0)`. Depth {1:92, 2:58, 3:24, 4:1}.
- **n=5, total 335**, chain a=67.3801°, ψ=36.8699°: quats
  `(1,0,0,0),(15,6,8,0),(25,36,48,0),(-45,138,184,0),(119,-72,-96,0)`.
  Depth {1:114, 2:110, 3:80, 4:30, 5:1}.
- **n=6, total 615**, chain a=53.1301°, ψ=36.8699°: quats
  `(1,0,0,0),(10,3,4,0),(15,12,16,0),(10,33,44,0),(-35,72,96,0),
  (190,-123,-164,0)`. Depth {1:168, 2:172, 3:152, 4:86, 5:36, 6:1}.

All three maxima were **hit at least twice** by independent configs
(different (a,ψ) or random tuples landing on the same total), and none of
3,000 random-phase tuples or 6 rounds of neighbor search per n beat the
chain optimum — strong internal evidence these are the plateau ceiling
of the *Pythagorean-sampled* family, not sampling noise. **The deficit
grows with n** (−8, −58, −108): the family gets *relatively less*
competitive as n increases, the opposite of "helps at n>3."

**Why, given Q3's finding that records ARE (mostly) family pairs**: the
records are not *pure* chains/orbits under one common axis — 723's
structure is "C₃-orbit-of-3 + 3 free cubes" (README), i.e. it wins by
COMBINING two different family cliques (or a family clique + free cubes)
rather than putting every cube on one common axis. A single-axis n-cube
family (this sweep's scope) is a strict subset of "n cubes built from
family-position pairs" — Q3 shows the latter, richer combinatorial space
is what the records actually exploit.

## Q2 — do the n=3 structural facts persist? (deep layers stable, d1 varies)

Yes, cleanly, at every n tested — and in one case (n=4) startlingly
precisely. Chain sweep at fixed ψ=36.8699°, total vs a (depth histograms
in `nfamily_results.jsonl`, `kind:"chain"`/`"chain_fine"`):

- **n=4**: d4=1 always; **d3=24 stable across the entire tested a-range
  except the two extremes** (drops to 20 below a≈28°, to 16 at the
  degenerate a=90° shared-axis point); d2 varies (46–58); d1 does most of
  the work (44–92). **d3=24 in the family EXACTLY equals the record's
  d3=24** (183 = {1:92,2:66,3:24,4:1}). Even more strikingly, the
  family's *best* member (175) matches the record's d1=92 AND d3=24 AND
  d4=1 exactly — **the entire 8-point deficit sits in d2 alone (58 vs
  66)**.
- **n=5**: d5=1 always; **d4=30 stable** across a≈28–67° (drops to 28 at
  a=22.6°, collapses to 12 at a=90°); d3 varies less than d1/d2 (70–80).
  The family's best (335) has d4=30 and d5=1 matching the record (393)
  exactly; d3 is *slightly ahead* of the record (80 vs 78); the 58-point
  deficit is concentrated in d1 (114 vs 156, −42) and d2 (110 vs 128,
  −18).
- **n=6**: d6=1 always; **d5=36 stable** at every non-degenerate a tested
  (36.87°, 53.13°; collapses to 8 at a=90°). Family best (615) matches
  the record's d5=36 and d6=1 exactly; the 108-point deficit spreads
  across d1(−42), d2(−44), d3(−12), d4(−10).

**Generalization of the n=3 law** ("d3=1, d2=18 across the whole middle
band, all variation in d1"): at n=4/5/6 it is the **top two depths**
(d_n=1 and d_{n−1} at its family-typical value) that stay pinned across
the family AND coincide exactly with the true record's own d_n, d_{n−1}
— the records buy their extra total almost entirely in the *shallow*
layers (d1, d2), which is exactly where unconstrained (non-family)
degrees of freedom pay off. This is the clearest generalization yet of
the project's recurring "deep structure conserved, d1 is what varies"
principle (ledger, Postscript 17).

**Symmetry bonus (new)**: ψ and 90°−ψ give *identical* totals and depth
profiles at every n tested (e.g. n=6: ψ=36.87° and ψ=53.13° both give
615) — the ψ↔90−ψ mirror symmetry noted for the n=3 C₃ slice
(Postscript 25 addendum 3, "symmetric about 45°") persists exactly at
n=4,5,6.

## Q4 — chain-path spikes

The clearest, most robust finding: **a = 90° (chain phase differences
that are exact multiples of 90°) is a severe NEGATIVE spike at every n
tested**, and it gets relatively worse — not better — as n grows:

| n | a=90° total | best non-degenerate neighbor | drop |
|---|---|---|---|
| 4 | 93 | 155 (a=79.6°) | −62 |
| 5 | 93 | 335 (a=67.4°) | −242 |
| 6 | 93 | 615 (a=53.1°) | −522 |

Strikingly, **all three totals at a=90° are identical (93)**, regardless
of n — strong evidence that phase differences of exactly 90° make cubes
beyond a small fixed subset *redundant* under the cube's own 90° self-
symmetry (exactly the concern flagged in `DIHEDRAL_FAMILY_NEXT.md` Task 4:
"cube self-symmetry makes 90° orbits trivial"). So: **the negative sign
dominates and its relative damage grows sharply with n** — a family with
n cubes chained at 90° behaves like a much smaller compound.

No positive spike analogous to n=3's "+12 at the octahedral 67s" was
found within the Pythagorean-sampled a-range at n=4/5/6 — see the
coverage caveat below for why this is inconclusive rather than negative.
"Near the tetrahedral resonance" (109.47°) was not separately isolated:
Pythagorean angles that land a *chain's base step* near 109.47° while
staying inside the |quat|≤512 cap for the needed k are scarce (the
109.47° role in the ledger's addendum 4 is specifically a psi=45°,
theta2=109.47° *point* on the C₃ pair-curve, not a chain base step, so it
doesn't directly transplant to this sweep's parametrization); this is
flagged as unexplored rather than resolved.

## Honest coverage statement

- **Fundamental (not budget) gap**: this sweep is restricted to
  Pythagorean (ψ,θ) by construction — that's what makes it exactly
  countable by the fast integer-quaternion engine. n=3's own true maxima
  (both 67s) sit at **irrational** ψ (arcsin(1/√3), arctan(φ²)) — points
  a dense Pythagorean grid can get arbitrarily close to but never lands
  on exactly, and Postscript 25 shows these are *isolated* spikes
  (measure zero), not the edge of an open plateau, so a discrete grid,
  however fine, need not sample near one by chance. **The plateau ceilings
  reported for Q1 (175/335/615) are lower bounds on the true continuous
  family's supremum, not proven maxima.** Finding n=4/5/6 analogues of
  the octahedral/golden spike (if they exist) needs a targeted
  symmetry-driven search (candidate special axes/tilts tied to the
  compound's own high-symmetry directions) with a ℚ(√d) tower engine, the
  same method that found the n=3 spikes — out of scope for an
  integer-quaternion-only sweep and not attempted here.
- **Budget used**: 9,218 configs, ≈115s wall-clock on ≤4 cores — well
  under the 10k–50k allowance; stopped because all three maxima recurred
  across independent samples and 6 rounds of neighbor hill-climbing per n
  found nothing beyond the chain optimum, not because of a time/config
  limit. A larger random sample or deeper multi-coordinate hill-climbing
  could still be run (`nfamily_sweep.py --random N --neighbor-rounds K`)
  but diminishing returns were already visible (random tuples never beat
  the best chain member at any n).
- **Chain length is denominator-limited**: only 44/70/120 of the 33×33
  (ψ,a) menu pairs reach n=6/5/4 respectively before the chain's
  compounding denominators exceed the C++ engine's |component|≤512 cap
  (independent random-phase configs don't have this limit — no
  compounding when θ₁=0). This caps how finely 'a' can be resolved in the
  chain sweep specifically (see the sparse `chain_fine` results); the
  random-phase tier has no such restriction and dominates the raw config
  count.
- **Neighbor search is shallow**: single-coordinate, 33-point-menu-step
  hill-climbing, 6 rounds, from a single incumbent best per n (not
  multi-restart from several top candidates, not multi-coordinate). It
  plateaued fast (no improvement after round 1 in all three n), which is
  itself evidence of a real local optimum, but a more thorough climb
  (multi-restart, 2-coordinate moves) was not run.
- Q3's crossing/axis-test machinery is new code, gated only by internal
  cross-validation (34/34 agreement between the two independent exact
  tests, plus a negative control on 200 random small-integer quaternion
  pairs giving an 5.5% false-positive rate under the 24-way relabeling
  search — not itself formally bounded, but consistent with "rare,
  structured" rather than "generic").

## Files

- `nfamily_common.py` — exact arithmetic core (Rel(Δ,ψ) closed form,
  square-root-free quat extraction, exact edge-crossing counter, family
  axis test, Pythagorean-angle menus).
- `nfamily_gates.py`, `nfamily_gates.out` — G0/G1/G2, all PASS.
- `nfamily_q3_records.py`, `nfamily_q3_records.json` — Q3 record analysis
  (n=3 via ℚ(√2), n=4/5/6 via integer quats).
- `nfamily_sweep.py` — sweep driver (chains, random, neighbor rounds).
- `nfamily_results.jsonl` — 9,218 exact results (n, kind, ψ, θ's/a, quats,
  total, by_depth).
