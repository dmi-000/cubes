#!/usr/bin/env python3
# Working principles: BLUEPRINT_SPEC.md; six_cube_search_results.md
# Postscripts 12/13/17/17-addendum/18/19 (+addenda); shared_axis_search.py
# (whose cluster/spoke genome format this file's `spec` tuples feed
# directly, unmodified); PROJECT.md. Project index: README.md.
"""blueprint_enum.py -- enumerate the n=6 "blueprint" catalog up to symmetry.

A BLUEPRINT (BLUEPRINT_SPEC.md's definition) = the partition of 6 cubes into
shared-axis clusters + free cubes, plus each cluster's KIND (onaxis: base=
None, corner sits on the axis, generically 13-capable; spoke: generic base,
generically 9-capable -- see shared_axis_search.py's docstring and Postscript
17-addendum's DOF table) and AXIS CLASS ((1,1,1)/(0,0,1)/(1,1,0)). This file
enumerates that finite space, applies the three justified prune rules
(P1 realizability, P2 frustration, P3 dominance) and prints the catalog.

CANONICALIZATION (P1, realizability -- both facts are structural, not
heuristic, and are what actually shrinks the space):

  P1a. A cluster of size 1 has no partner to share an axis with, so an
       "onaxis-1" or "spoke-1" cluster is just a single cube -- but a locked
       or axis-anchored single cube is a STRICT SPECIALIZATION of a fully
       free cube (same slot, fewer continuous DOF: axis_rot(axis,p,q) is a
       1-parameter family vs a free integer quat's ~3-parameter family, and
       a spoke-1's cube = axis_rot(axis,p,q).base has one more fixed DOF,
       the base, than a genuinely free cube). A free-cube search strictly
       dominates the constrained search over the same slot at equal budget.
       So every size-1 part of a partition becomes a FREE cube, never its
       own labeled cluster.
  P1b. Two "onaxis" clusters on the SAME axis are indistinguishable from
       their union: onaxis members are axis_rot(axis,p,q) with base=None,
       so nothing differentiates "onaxis cluster A" from "onaxis cluster B"
       on one axis except which angles you assign to which label -- a
       relabeling, not a new configuration. So at most ONE onaxis cluster
       per axis; multiple onaxis parts of a partition MERGE into one.
  P1c (scope restriction, not elimination). This catalog's numeric family
       (reused verbatim from shared_axis_search.py's build_config/
       genome_config2) puts every cluster of a blueprint on a SINGLE shared
       global axis. Blueprints whose clusters sit on genuinely DIFFERENT,
       non-parallel axes are a distinct, richer family (independent
       relative orientation between axis frames) that is NOT a
       specialization of the single-axis family and so is not, strictly,
       P1-dominated by it. It is excluded from the per-blueprint numeric
       campaign here and instead represented by ONE catalog entry, pruned
       under P3 with the concrete evidence already in hand (see below).

Applying P1a+P1b to the 11 integer partitions of 6, independently choosing
a KIND (onaxis/spoke) for every part of size >=2 and ONE axis for the whole
blueprint, gives the canonical space enumerated by canonical_blueprints():
size-2..6 clusters partitioned as (onaxis size a in {0,2,3,4,5,6}) +
(spoke sizes, a partition of 6-a into parts >=2) + (free count). Axis
choice is vacuous when there is no cluster (the all-free control), so it is
counted once, not thrice.

P2 (frustration, wholesale exclusion, not a per-entry filter): any
blueprint that would force an ALL-13 pairwise triangle recreates the golden
/octahedral wall. That wall needs an IRRATIONAL tan-half-angle (golden:
Q(sqrt5); octahedral 45 degrees: tan(22.5 deg)=sqrt2-1) -- Postscript 13.
This rational family (axis_rot always takes rational p/q) cannot express it
at all, so P2 never fires on an entry of canonical_blueprints(); its role
is to justify EXCLUDING the golden/octahedral-wall family from the search
space entirely rather than re-discovering its known ceiling. Documented via
one placeholder catalog entry citing Postscript 12's exact result: the
golden-5 + shared-axis-sixth family caps at 681 < 723 (six_cube_search_
results.md Postscript 12, "681 | the golden five + a sixth cube...").

P3 (dominance, wholesale exclusion): the deferred multi-axis family
(P1c) is represented by one placeholder entry, pruned citing Postscript
12's direct test of exactly this shape -- the T-generating different-axis
intersection C2(001)+C3(111) (forcing the tetrahedral group <C2,C3>=T) --
which reached only 613, a net loser against every rational record from 655
up (six_cube_search_results.md Postscript 12: "The T-generating different-
axis intersection ... was a net loser at 613 -- forcing the full polyhedral
symmetry HURTS"). No other P3 exclusions are applied a priori: every
remaining canonical entry is run (see blueprint_search.py) rather than
speculatively pruned without direct evidence.

Usage: python3 blueprint_enum.py     # prints the catalog and exits.
"""
import itertools

AXES = ['(1,1,1)', '(0,0,1)', '(1,1,0)']


def integer_partitions(n, max_part=None):
    """All partitions of n as non-increasing tuples (standard recursive
    generator). len(list(integer_partitions(6))) == 11, the exact list the
    spec names (6; 5+1; 4+2; 4+1+1; 3+3; 3+2+1; 3+1+1+1; 2+2+2; 2+2+1+1;
    2+1+1+1+1; 1x6)."""
    if max_part is None:
        max_part = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, max_part), 0, -1):
        for rest in integer_partitions(n - k, k):
            yield (k,) + rest


PARTITIONS_6 = list(integer_partitions(6))
assert len(PARTITIONS_6) == 11


# ------------------------------------------------------------ Stage-A count
def stage_a_count():
    """Pre-canonicalization illustrative count: every part of size>=2
    independently picks (kind in {onaxis,spoke}) x (axis in 3 classes) --
    the space before P1b's same-axis-onaxis-merge and before P1c's
    single-global-axis restriction. Purely for reporting the size of the
    reduction; not itself searched."""
    total, rows = 0, []
    for p in PARTITIONS_6:
        k = sum(1 for x in p if x >= 2)
        cnt = (2 * 3) ** k
        total += cnt
        rows.append((p, k, cnt))
    return total, rows


def stage_aprime_count():
    """Same as stage_a_count but with ONE global axis per blueprint (P1c's
    scope restriction) instead of an independent axis per cluster; kind
    (onaxis/spoke) is still independent per cluster (P1b's merge not yet
    applied). This isolates how much of the Stage-A -> canonical reduction
    is "single axis" vs "onaxis clusters merge"."""
    total, rows = 0, []
    for p in PARTITIONS_6:
        k = sum(1 for x in p if x >= 2)
        cnt = (2 ** k) * (3 if k >= 1 else 1)
        total += cnt
        rows.append((p, k, cnt))
    return total, rows


# --------------------------------------------------------- canonical space
def canonical_blueprints():
    """Yield the canonical (a, spoke_sizes, n_free) keys: a = onaxis
    cluster size (0 or in 2..6), spoke_sizes = sorted-descending tuple of
    spoke cluster sizes (each >=2), n_free = number of free cubes.
    a + sum(spoke_sizes) + n_free == 6 always. One entry per equivalence
    class under P1a+P1b (verified: no two distinct raw partition+kind
    assignments collapse to the same key by accident, since the key IS the
    canonical form)."""
    seen = []
    for a in (0, 2, 3, 4, 5, 6):
        r = 6 - a
        for part in integer_partitions(r):
            spoke_sizes = tuple(sorted((x for x in part if x >= 2), reverse=True))
            n_free = sum(1 for x in part if x == 1)
            key = (a, spoke_sizes, n_free)
            if key not in seen:
                seen.append(key)
    return seen


def blueprint_tag(a, spoke_sizes, n_free, axis_name):
    parts = []
    if a:
        parts.append(f'onaxis{a}')
    for s in spoke_sizes:
        parts.append(f'spoke{s}')
    if n_free:
        parts.append(f'free{n_free}')
    if not parts:
        parts.append('allfree6')
    body = '+'.join(parts)
    axis_short = {'(1,1,1)': '111', '(0,0,1)': '001', '(1,1,0)': '110'}[axis_name]
    if a == 0 and not spoke_sizes:
        return f'n6_{body}'          # axis-independent control
    return f'n6_{body}_ax{axis_short}'


def to_spec(a, spoke_sizes, n_free):
    """Return (cluster_specs, n_free) in EXACTLY shared_axis_search.py's
    `spec` format: cluster_specs = [('onaxis'|'spoke', size), ...]. This is
    the reuse point -- shared_axis_search.random_genome/locked_genome/
    multi_restart/run_template all consume this format unmodified."""
    cluster_specs = []
    if a:
        cluster_specs.append(('onaxis', a))
    for s in spoke_sizes:
        cluster_specs.append(('spoke', s))
    return (cluster_specs, n_free)


def build_catalog():
    """Full catalog: canonical survivors (one row per axis, except the
    axis-independent all-free control counted once) + the two P2/P3
    wholesale-excluded placeholder families. Returns list of dicts."""
    rows = []
    bp_id = 0
    for (a, spoke_sizes, n_free) in canonical_blueprints():
        axis_list = AXES if (a or spoke_sizes) else [None]
        for axis_name in axis_list:
            bp_id += 1
            is_gate = (a == 3 and spoke_sizes == (3,) and n_free == 0
                       and axis_name == '(1,1,1)')
            rows.append(dict(
                id=bp_id,
                axis=axis_name,
                a=a, spoke_sizes=spoke_sizes, n_free=n_free,
                tag=blueprint_tag(a, spoke_sizes, n_free, axis_name or '(1,1,1)'),
                spec=to_spec(a, spoke_sizes, n_free),
                n=a + sum(spoke_sizes) + n_free,
                status='SURVIVOR',
                reason='realizable rational shared-axis/free family (P1 canonical form)'
                       + (' -- GATE: known 723 record' if is_gate else ''),
                is_gate=is_gate,
            ))
    # P2 placeholder: golden/octahedral all-13 wall family
    bp_id += 1
    rows.append(dict(
        id=bp_id, axis='irrational (golden Q(sqrt5) / octahedral 45deg)',
        a=None, spoke_sizes=None, n_free=None,
        tag='golden_octahedral_all13_wall', spec=None, n=6,
        status='PRUNED-P2',
        reason='all-13 triangle forces the golden/octahedral wall; needs an '
               'irrational tan-half-angle unreachable by this rational '
               'family; its best rational-extension is 681 < 723 '
               '(Postscript 12: "golden five + shared-axis sixth" = 681)',
        is_gate=False,
    ))
    # P3 placeholder: distinct-axis / polyhedral-forcing family
    bp_id += 1
    rows.append(dict(
        id=bp_id, axis='multiple distinct non-parallel axes',
        a=None, spoke_sizes=None, n_free=None,
        tag='multiaxis_polyhedral_forcing', spec=None, n=6,
        status='PRUNED-P3',
        reason='clusters on genuinely different axes (independent relative '
               'orientation) is a richer, non-single-axis family, directly '
               'tested by Postscript 12 as the T-generating C2(001)+C3(111) '
               'intersection (forces <C2,C3>=T): reached only 613, a net '
               'loser against every rational record from 655 up',
        is_gate=False,
    ))
    return rows


def print_catalog():
    rows = build_catalog()
    survivors = [r for r in rows if r['status'] == 'SURVIVOR']
    pruned_p2 = [r for r in rows if r['status'] == 'PRUNED-P2']
    pruned_p3 = [r for r in rows if r['status'] == 'PRUNED-P3']

    sa_total, sa_rows = stage_a_count()
    sap_total, sap_rows = stage_aprime_count()

    print('=== Stage A: pre-canonicalization (illustrative, not searched) ===')
    print('  independent (kind x axis) per cluster part >=2, distinct axes allowed:')
    for p, k, cnt in sa_rows:
        print(f'    partition {p!s:<22} clusters>=2: {k}  choices: {cnt}')
    print(f'  Stage A total = {sa_total}')
    print()
    print('=== Stage A\': single global axis per blueprint (P1c), kind still independent ===')
    for p, k, cnt in sap_rows:
        print(f'    partition {p!s:<22} clusters>=2: {k}  choices: {cnt}')
    print(f'  Stage A\' total = {sap_total}')
    print()
    print(f'=== Canonical catalog (after P1a size-1-collapse + P1b onaxis-merge) ===')
    print(f'  {sap_total} (Stage A\') -> {len(survivors)} canonical survivors '
          f'({sap_total - len(survivors)} collapsed as onaxis-cluster-merge duplicates)')
    print()
    print(f'{"id":>3} {"tag":<34} {"axis":<10} {"n":>2} {"status":<12} reason')
    print('-' * 130)
    for r in rows:
        axis_disp = r['axis'] if r['axis'] else '(any/n.a.)'
        print(f'{r["id"]:>3} {r["tag"]:<34} {axis_disp:<10} {r["n"]:>2} '
              f'{r["status"]:<12} {r["reason"]}')
    print()
    print(f'TOTALS: {len(rows)} catalog entries = {len(survivors)} SURVIVOR '
          f'+ {len(pruned_p2)} PRUNED-P2 + {len(pruned_p3)} PRUNED-P3')
    gate_rows = [r for r in survivors if r['is_gate']]
    assert len(gate_rows) == 1, 'GATE blueprint (onaxis3+spoke3 on (1,1,1)) must be exactly one survivor'
    print(f'GATE blueprint present among survivors: id={gate_rows[0]["id"]} '
          f'tag={gate_rows[0]["tag"]}  (must reproduce 723 -- checked by blueprint_search.py)')
    return rows


if __name__ == '__main__':
    print_catalog()
