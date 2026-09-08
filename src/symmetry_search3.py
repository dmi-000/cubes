#!/usr/bin/env python3
# Working principles: SYMMETRY_SEARCH_V3.md. Project index: README.md
"""Symmetry-search V3: remaining rational families (Part A) + shared-axis
"intersection" families (Part B). Record to beat: 717 (D2:4+free2).

REUSES symmetry_search.py / symmetry_search2.py validated build_blocks /
orbit / O-dedup / dispatch / climber functions verbatim (imported, not
rewritten). Only new code here is: (1) axis-parameterized cyclic-group
quaternion generators (C2 about (1,1,1)/(1,1,0)/(0,0,1); reuses
ss.group_quats for C3/C4/C6/D2/D3/D4/D6/T which are already the unique
rational realization of those orders about their forced axes -- see the
correctness note below), and (2) the family list / driver / report.

Correctness note (why only these axis/order combinations are RATIONAL):
a finite-order rotation about axis n has quaternion (cos th/2, sin th/2 * n).
For n a coordinate axis, sin/cos th/2 must themselves be rational -> only
th=180 (order 2) and th=90 (order 4) have rational tan(th/2) (=inf, 1).
For n a body diagonal (1,1,1)/sqrt3, the sqrt3 in sin(th/2) can CANCEL the
sqrt3 in the axis normalization for th=120 (order 3) and th=60 (order 6)
-- and does NOT for th=90 (irrational). For n an edge axis (1,1,0)/sqrt2,
only th=180 (order 2, always rational for ANY rational axis, since a pure
quaternion (0,x,y,z) is always rational) survives; sqrt2 cancels nothing
for order 3/4/6. Hence: C2 is buildable about ALL THREE test axes; C4
only about (0,0,1); C3/C6 only about (1,1,1). This is exactly the
axis/order menu the spec's partitions use.

Usage: nohup caffeinate -i python3 symmetry_search3.py > symmetry_search3_run.out 2>&1 &
"""
import json
import os
import random
import time
from itertools import product

import symmetry_search as ss
import symmetry_search2 as ss2

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(HERE, 'symmetry_search3.jsonl')
REPORT_PATH = os.path.join(HERE, 'symmetry_search3_report.md')

# Redirect ALL reused logging (ss.log_eval, ss2.log) into THIS run's file.
ss.LOG_PATH = LOG_PATH
ss2.LOG_PATH = LOG_PATH
ss2.RECORD = 717   # threshold for ss2.search_blocks' flagging logic
RECORD = 717

TRIV = ss2.TRIV
gcdq = ss2.gcdq
MAXC = ss.MAXC


def log(rec):
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')


# ------------------------------------------------------- axis-parameterized C2
def custom_group_quats(gens):
    """Same BFS closure as ss.group_quats(name), parameterized by explicit
    generator quats instead of RATIONAL_GROUPS[name] -- lets us build Cn
    about an axis not in the hardcoded table (here: C2 about any axis,
    since a pure quaternion (0,x,y,z) is always a rational 180-degree
    rotation about (x,y,z) for ANY integer x,y,z)."""
    seen = {(1, 0, 0, 0): ss.rot_from_quat(1, 0, 0, 0)}
    frontier = [(1, 0, 0, 0)]
    gen_and_inv = list(gens)
    for g in gens:
        w, x, y, z = g
        gen_and_inv.append((w, -x, -y, -z))
    while frontier:
        nxt = []
        for q in frontier:
            for g in gen_and_inv:
                nq = tuple(ss.gcd_reduce(list(ss.quat_mul(q, g))))
                R = ss.rot_from_quat(*nq)
                if not any(R == r for r in seen.values()):
                    seen[nq] = R
                    nxt.append(nq)
        frontier = nxt
    return list(seen.keys())


AX111 = (1, 1, 1)
AX001 = (0, 0, 1)
AX110 = (1, 1, 0)

C2_111 = custom_group_quats([(0,) + AX111])
C2_110 = custom_group_quats([(0,) + AX110])
C2_001 = custom_group_quats([(0,) + AX001])
C3_111 = ss.group_quats('C3')   # only rational realization of order 3, axis (1,1,1)
C4_001 = ss.group_quats('C4')   # only rational realization of order 4, axis (0,0,1)
C6_111 = ss.group_quats('C6')   # only rational realization of order 6, axis (1,1,1)
D2q = ss.group_quats('D2')
D3q = ss.group_quats('D3')
D4q = ss.group_quats('D4')
D6q = ss.group_quats('D6')
Tq = ss.group_quats('T')

for name, gq, want in [('C2_111', C2_111, 2), ('C2_110', C2_110, 2),
                        ('C2_001', C2_001, 2)]:
    assert len(gq) == want, f'{name} order {len(gq)} != {want}'

FREEB = [(1, 0, 0, 0), (2, 1, 1, 1), (3, 1, 1, 1), (5, 2, 2, 2),
         (2, 1, 0, 0), (3, 2, 1, 0)]


def combo_starts(batteries, cap=150):
    combos = list(product(*batteries))
    if len(combos) > cap:
        stride = len(combos) / cap
        combos = [combos[int(i * stride)] for i in range(cap)]
    return [list(c) for c in combos]


# ============================================================== GATES
def run_gates():
    print('=== GATES (must pass before trusting anything below) ===', flush=True)
    cfg1 = ss2.build_blocks([D2q, TRIV, TRIV], [(5, 2, 2, 2), (2, 1, 1, 1), (1, 0, 0, 0)])
    assert cfg1 is not None, 'GATE1: D2-cluster+free+aligned failed to build 6 cosets'
    tot1, bd1 = ss.cpp_batch([cfg1])[0]
    print(f'  GATE1 (D2-cluster+free+aligned): total={tot1} (want 717) '
          f'{"PASS" if tot1 == 717 else "FAIL"}', flush=True)
    if tot1 != 717:
        raise SystemExit('GATE1 FAILED -- shared-axis builder is wrong. Stopping per spec.')

    cfg2 = ss2.build_blocks([C3_111, C3_111], [(3, 1, 0, 0), (41, 28, 22, 14)])
    assert cfg2 is not None, 'GATE2: C3+C3-on-(1,1,1) failed to build 6 cosets'
    tot2, bd2 = ss.cpp_batch([cfg2])[0]
    print(f'  GATE2 (C3+C3 on (1,1,1)):        total={tot2} (want 699) '
          f'{"PASS" if tot2 == 699 else "FAIL"}', flush=True)
    if tot2 != 699:
        raise SystemExit('GATE2 FAILED -- shared-axis builder is wrong. Stopping per spec.')
    print('  BOTH GATES PASS.\n', flush=True)
    return {'gate717': tot1, 'gate699': tot2}


# ========================================================== generic runner
ALL_RESULTS = {}


def run_family(tag, blocks, explicit_starts, n_random, climb_steps, rng,
                note='', part='A'):
    t0 = time.time()
    best, nev, nres, flagged = ss2.search_blocks(
        'V3', blocks, tag, explicit_starts, n_random, climb_steps, rng, note=note)
    dt = time.time() - t0
    rec = dict(best=best, evals=nev, restarts=nres, flagged=flagged,
               note=note, part=part, dt=dt,
               nblocks=len(blocks), n_explicit=len(explicit_starts),
               n_random=n_random, climb_steps=climb_steps)
    ALL_RESULTS[tag] = rec
    for tot, seeds, bd, v in flagged:
        log({'phase': 3, 'tag': tag, 'part': part, 'FLAG': v or 'RECORD',
             'total': tot, 'seeds': [list(s) for s in seeds]})
    return rec


# ================================================================= PART A
def part_a(rng):
    print('\n########## PART A: rational families never re-swept full-quat ##########',
          flush=True)

    # ---- C4:4+free2  (core orbit4 full-quat + 2 free full-quat) ----
    c4b4 = ss2.aligned_seed_battery(C4_001, 4)
    starts = combo_starts([c4b4, FREEB, FREEB], cap=120)
    run_family('C4:4+free2', [C4_001, TRIV, TRIV], starts, n_random=40,
               climb_steps=10, rng=rng,
               note='(full-quat core+free, C4 about (0,0,1))')

    # ---- C4:4+2  (orbit4 generic + orbit2 aligned, same C4 group) ----
    # NOTE: the standard 3-form seed battery (z-axial/body-diag/face-diag)
    # realizes NO orbit-2 locus for C4 about (0,0,1) -- z-axial is FIXED
    # (orbit 1, it IS the rotation axis), body-diag/face-diag give orbit 4
    # (computed, not assumed). Skipped; recorded as a coverage gap, not a
    # silent omission.
    c4b2 = ss2.aligned_seed_battery(C4_001, 2)
    if c4b2:
        starts = combo_starts([c4b4, c4b2], cap=120)
        run_family('C4:4+2', [C4_001, C4_001], starts, n_random=30,
                   climb_steps=10, rng=rng, note='(two C4 orbits, 4+2)')
    else:
        ALL_RESULTS['C4:4+2'] = dict(best={'total': None}, skipped=True,
            note='no orbit-2 alignment locus found in the 3-form battery '
                 'for C4 about (0,0,1); computed, not assumed -- genuinely '
                 'skipped, not silently dropped', part='A')
        print('  C4:4+2          SKIPPED (no orbit-2 locus found by battery)',
              flush=True)

    # ---- D4:4+free2, D4:2+2+2 ----
    d4b4 = ss2.aligned_seed_battery(D4q, 4)
    d4b2 = ss2.aligned_seed_battery(D4q, 2)
    starts = combo_starts([d4b4, FREEB, FREEB], cap=120)
    run_family('D4:4+free2', [D4q, TRIV, TRIV], starts, n_random=40,
               climb_steps=10, rng=rng, note='(full-quat core+free)')
    starts = combo_starts([d4b2, d4b2, d4b2], cap=120)
    run_family('D4:2+2+2', [D4q, D4q, D4q], starts, n_random=40,
               climb_steps=10, rng=rng, note='(three D4 orbit-2 blocks)')

    # ---- D6:6, D6:4+2 ----
    d6b6 = ss2.aligned_seed_battery(D6q, 6)
    d6b4 = ss2.aligned_seed_battery(D6q, 4)
    d6b2 = ss2.aligned_seed_battery(D6q, 2)
    starts = [[q] for q in d6b6]
    run_family('D6:6', [D6q], starts, n_random=50, climb_steps=12, rng=rng,
               note='(single D6 orbit-6)')
    if d6b4 and d6b2:
        starts = combo_starts([d6b4, d6b2], cap=100)
        run_family('D6:4+2', [D6q, D6q], starts, n_random=30, climb_steps=10,
                   rng=rng, note='(two D6 orbits, 4+2)')

    # ---- D3:3+free3 (new: D3's known orbit-3 core + FULL-QUAT free cubes,
    # not paired with a second D3 orbit as in the V2 D3:3+3 family) ----
    d3b3 = ss2.aligned_seed_battery(D3q, 3)
    starts = combo_starts([d3b3, FREEB, FREEB, FREEB], cap=150)
    run_family('D3:3+free3', [D3q, TRIV, TRIV, TRIV], starts, n_random=40,
               climb_steps=8, rng=rng, note='(D3 orbit-3 core + 3 full-quat free)')

    # ---- T:4+free2 re-confirm through the generic block framework, fresh
    # full-quat free random restarts (superset of V2's run) ----
    tb4 = ss2.aligned_seed_battery(Tq, 4)
    starts = combo_starts([tb4, FREEB, FREEB], cap=120)
    run_family('T:4+free2(reconfirm)', [Tq, TRIV, TRIV], starts, n_random=40,
               climb_steps=10, rng=rng,
               note='(re-run via generic block framework, fresh full-quat free)')

    # ---- D3:3+3 re-confirm with full-quat-seeded explicit anchors (the V2
    # grid already covers the alignment locus exhaustively at 657; this
    # just re-confirms via the block framework with the SAME battery) ----
    starts = combo_starts([d3b3, d3b3], cap=150)
    run_family('D3:3+3(reconfirm)', [D3q, D3q], starts, n_random=20,
               climb_steps=8, rng=rng, note='(two D3 orbit-3 blocks, reconfirm)')


# ================================================================= PART B
def part_b(rng):
    print('\n########## PART B: shared-axis intersection families ##########',
          flush=True)

    S1, S2 = (3, 1, 0, 0), (41, 28, 22, 14)          # 699 anchor
    D2ANCH = (5, 2, 2, 2)                             # 717 anchor
    ID = (1, 0, 0, 0)

    # ---- C2 (0,0,1) + C4 (0,0,1) union, partition 2+4, common face axis ----
    c4b4 = ss2.aligned_seed_battery(C4_001, 4)
    starts = combo_starts([[(1, 0, 3, 0), (1, 0, 5, 0), (1, 0, 7, 0),
                            (3, 0, 5, 0), (2, 0, 5, 0), (5, 0, 9, 0)],
                           c4b4], cap=100)
    run_family('C2+C4 on (0,0,1)', [C2_001, C4_001], starts, n_random=50,
               climb_steps=10, rng=rng,
               note='(shared face axis, partition 2+4)', part='B')

    # ---- C3+C3 on (1,1,1), gated family, fresh 50-start search ----
    starts = [[S1, S2], [(3, 1, 0, 0), (41, 14, 28, 22)],
              [(3, 0, 1, 0), (41, 28, 22, 14)]]
    run_family('C3+C3 on (1,1,1)', [C3_111, C3_111], starts, n_random=50,
               climb_steps=12, rng=rng,
               note='(shared body-diagonal, partition 3+3, GATED at 699)',
               part='B')

    # ---- C2 x3 on (1,1,1), partition 2+2+2, common body-diagonal axis ----
    starts = combo_starts([[(1, 1, -1, 0), (2, 1, -1, 0), (1, 2, -1, 0)],
                           [(1, 0, 1, -1), (2, 0, 1, -1), (1, 0, 2, -1)],
                           [(1, 1, 0, -1), (2, 1, 0, -1), (1, 2, 0, -1)]],
                          cap=120)
    run_family('C2x3 on (1,1,1)', [C2_111, C2_111, C2_111], starts,
               n_random=50, climb_steps=10, rng=rng,
               note='(three C2 orbits, all about (1,1,1))', part='B')

    # ---- C2 x3 on (1,1,0), partition 2+2+2, common edge axis ----
    starts = combo_starts([[(1, 1, -1, 0), (2, 1, -1, 0)],
                           [(1, 0, 0, 1), (2, 0, 0, 1)],
                           [(1, 1, 1, 0), (2, 1, 1, 0)]], cap=100)
    run_family('C2x3 on (1,1,0)', [C2_110, C2_110, C2_110], starts,
               n_random=50, climb_steps=10, rng=rng,
               note='(three C2 orbits, all about (1,1,0))', part='B')

    # ---- C3+C2+free on (1,1,1), partition 3+2+1, common body-diagonal ----
    starts = combo_starts([[S1, S2], [(1, 1, -1, 0), (2, 1, -1, 0)], FREEB],
                          cap=120)
    run_family('C3+C2+free on (1,1,1)', [C3_111, C2_111, TRIV], starts,
               n_random=50, climb_steps=10, rng=rng,
               note='(shared body-diagonal, partition 3+2+1)', part='B')

    # ---- D2-cluster+free+aligned, GATED at 717, fresh 50-start search
    # (the 717 record's own family, re-run through this campaign) ----
    d2b4 = ss2.aligned_seed_battery(D2q, 4)
    starts = combo_starts([d2b4, FREEB, [ID]], cap=120) + \
             [[D2ANCH, (2, 1, 1, 1), ID]]
    run_family('D2-cluster+free+aligned', [D2q, TRIV, TRIV], starts,
               n_random=50, climb_steps=10, rng=rng,
               note='(717 template: D2 orbit4 core + free + explicit-aligned '
                    'anchor start; GATED at 717)', part='B')

    # ---- core+free template, varied core size/axis ----
    # C2 core(2)+free4, three axis choices
    for axname, gq, axseeds in [
        ('(1,1,1)', C2_111, [(1, 1, -1, 0), (2, 1, -1, 0)]),
        ('(0,0,1)', C2_001, [(1, 2, 0, 0), (1, 3, 0, 0)]),
        ('(1,1,0)', C2_110, [(1, 1, -1, 0), (2, 1, -1, 0)]),
    ]:
        starts = combo_starts([axseeds, FREEB, FREEB, FREEB, FREEB], cap=150)
        run_family(f'C2core2+free4 on {axname}', [gq, TRIV, TRIV, TRIV, TRIV],
                   starts, n_random=50, climb_steps=8, rng=rng,
                   note='(core+free template, core size 2)', part='B')

    # C3 core(3)+free3 on (1,1,1)
    starts = combo_starts([[S1, S2, (1, 1, 1, 1)], FREEB, FREEB, FREEB],
                          cap=150)
    run_family('C3core3+free3 on (1,1,1)', [C3_111, TRIV, TRIV, TRIV], starts,
               n_random=50, climb_steps=8, rng=rng,
               note='(core+free template, core size 3)', part='B')

    # ---- intersection reading: C2(0,0,1) + C3(1,1,1) + free1, DIFFERENT
    # axes on purpose so <C2,C3> generates T (order12) rather than the
    # common-axis C6 -- compare vs forcing the FULL T orbit (Part A's
    # T:4+free2) ----
    c3seeds = [(3, 1, 0, 0), (3, 0, 1, 0), (5, 2, 0, 0)]
    starts = combo_starts([[(1, 2, 0, 0), (1, 3, 0, 0)], c3seeds, FREEB],
                          cap=120)
    run_family('C2(001)+C3(111)+free1 [T-generating]',
               [C2_001, C3_111, TRIV], starts, n_random=50, climb_steps=10,
               rng=rng,
               note='(DIFFERENT axes -- <C2,C3> generates T; compare vs '
                    'T:4+free2 forced-full-orbit)', part='B')


# ==================================================================== MAIN
def main():
    rng = random.Random(20260712)
    t0 = time.time()
    gates = run_gates()
    part_a(rng)
    part_b(rng)
    dt = time.time() - t0
    print(f'\nTotal wall time: {dt:.0f}s', flush=True)
    write_report(gates, dt)
    print(f'Report -> {REPORT_PATH}', flush=True)


def write_report(gates, dt):
    L = []
    L.append('# Symmetry search V3 report (remaining rational families '
              '+ shared-axis intersection families)\n')
    L.append('Working principles: SYMMETRY_SEARCH_V3.md. Generated by '
             'symmetry_search3.py. Reuses symmetry_search.py / '
             'symmetry_search2.py validated build_blocks/orbit/O-dedup/'
             'dispatch/climber functions unchanged. Record to beat: '
             f'**717** (D2:4+free2).\n')

    L.append('## Gates\n')
    L.append(f'- GATE1 (D2-cluster+free+aligned reproduces 717): '
             f'total={gates["gate717"]} {"PASS" if gates["gate717"]==717 else "FAIL"}')
    L.append(f'- GATE2 (C3+C3 on (1,1,1) reproduces 699): '
             f'total={gates["gate699"]} {"PASS" if gates["gate699"]==699 else "FAIL"}')
    L.append('')

    def best_total(rec):
        b = rec.get('best')
        if not b or not isinstance(b, dict):
            return None
        return b.get('total')

    all_flags = []
    overall_best = (-1, None)
    for tag, rec in ALL_RESULTS.items():
        for f in rec.get('flagged', []) or []:
            all_flags.append((tag,) + f)
        bt = best_total(rec)
        if bt is not None and bt > overall_best[0]:
            overall_best = (bt, tag)

    L.append('## Part A: rational family bests (vs 717)\n')
    L.append('| family | best | vs 717 | evals | coverage note |')
    L.append('|---|---|---|---|---|')
    for tag, rec in ALL_RESULTS.items():
        if rec.get('part') != 'A':
            continue
        if rec.get('skipped'):
            L.append(f'| {tag} | SKIPPED | -- | 0 | {rec["note"]} |')
            continue
        bt = best_total(rec)
        cmp = 'BEATS' if bt and bt > 717 else ('TIES' if bt == 717 else
              (f'{bt-717:+d}' if bt is not None else '?'))
        L.append(f'| {tag} | {bt} | {cmp} | {rec.get("evals")} | {rec.get("note","")} |')
    L.append('')

    L.append('## Part B: shared-axis intersection family bests (vs 717)\n')
    L.append('| family | best | vs 717 | evals | structure |')
    L.append('|---|---|---|---|---|')
    for tag, rec in ALL_RESULTS.items():
        if rec.get('part') != 'B':
            continue
        bt = best_total(rec)
        cmp = 'BEATS' if bt and bt > 717 else ('TIES' if bt == 717 else
              (f'{bt-717:+d}' if bt is not None else '?'))
        L.append(f'| {tag} | {bt} | {cmp} | {rec.get("evals")} | {rec.get("note","")} |')
    L.append('')

    L.append('## Records > 717 or deep-ceiling violations\n')
    if all_flags:
        for tag, tot, seeds, bd, v in all_flags:
            L.append(f'- [{tag}] total={tot} {v or "NEW RECORD"} '
                      f'seeds={[list(s) for s in seeds]}')
    else:
        L.append('None. No configuration exceeded 717 and no by_depth '
                 'breached d3<=164 / d4<=102 / d5<=36 / d6=1 across all '
                 'Part A + Part B evals.')
    L.append('')

    L.append('## Verdict\n')
    if overall_best[0] > 717:
        L.append(f'- **BEATS 717**: family `{overall_best[1]}` reached '
                 f'{overall_best[0]}. See flags above for exact seeds.')
    else:
        L.append(f'- Nothing beat 717. Overall best across every family in '
                 f'this campaign: **{overall_best[0]}** ({overall_best[1]}).')
    b_best = max(((best_total(r), tag) for tag, r in ALL_RESULTS.items()
                 if r.get('part') == 'B' and best_total(r) is not None),
                default=(None, None))
    if b_best[0] is not None:
        L.append(f'- Best Part-B shared-axis family: `{b_best[1]}` at '
                 f'{b_best[0]} ({b_best[0]-717:+d} vs 717).')
    L.append(f'- Total wall time: {dt:.0f}s.')

    with open(REPORT_PATH, 'w') as f:
        f.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
