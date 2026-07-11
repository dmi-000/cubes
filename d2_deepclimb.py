#!/usr/bin/env python3
# Working principles: D2_DEEPCLIMB_SPEC.md. Project index: README.md
"""D2:4+free2 deep-climb + D2-sibling sweep + shallow-tail (d3-vs-total)
tradeoff mapping. Spec: D2_DEEPCLIMB_SPEC.md.

REUSES symmetry_search.py / symmetry_search2.py verbatim (imported, not
copied): build_blocks, group_quats, quat_orbit, cap_ok, gcd_reduce,
cpp_batch, aligned_seed_battery, and -- for task 2's broad resweep --
search_blocks itself (the existing validated +-1/+-2 single-component
climber). Only task 1's LARGER neighborhood (single +-1..+-6, plus a
two-component-simultaneous move set) is new code, because that is
literally what task 1 asks for: a neighborhood the existing climber
cannot express, to test whether the 717/d3=158 record sits at a saddle a
+-1/+-2 single-component climb can't leave.

Does NOT edit symmetry_search.py / symmetry_search2.py / six_cube_search_
results.md; exact_search_results.jsonl is never touched. All evals go
through the same ./cube_regions engine via ss.cpp_batch (<=4 workers,
enforced by ss.WORKERS already set to 4).

Usage: python3 d2_deepclimb.py [gate|task1|task2|all]   (default all)
"""
import json
import os
import random
import sys
import time
from itertools import combinations, product

import symmetry_search as ss
import symmetry_search2 as ss2

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(HERE, 'd2_deepclimb.jsonl')
REPORT_PATH = os.path.join(HERE, 'd2_deepclimb_report.md')
# Redirect ALL reused-function logging into THIS run's file (same pattern
# symmetry_search2.py itself uses to redirect symmetry_search.py's log).
ss.LOG_PATH = LOG_PATH
ss2.LOG_PATH = LOG_PATH
ss2.RECORD = 717   # so ss2.search_blocks flags total>717, not >699

MAXC = ss.MAXC
RECORD = 717
CEIL = {3: 164, 4: 102, 5: 36}
TRIV = ss2.TRIV
gcdq = ss2.gcdq
build_blocks = ss2.build_blocks
cap_ok = ss.cap_ok
violation = ss2.violation

D2q = ss.group_quats('D2')
assert len(D2q) == 4

# The two known 717 seeds (D2_DEEPCLIMB_SPEC.md + symmetry_search2.jsonl).
KNOWN_717 = {
    'A': [(5, 2, 2, 2), (2, 1, 1, 1), (1, 0, 0, 0)],
    'B': [(4, 1, 1, 1), (1, 0, 0, 0), (3, 1, 1, 1)],
}
BLOCKS_D2_4F2 = [D2q, TRIV, TRIV]

RNG = random.Random(20260711)


def log(rec):
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')


def eval_batch(cfgs):
    return ss2.eval_batch(cfgs)


# ============================================================ 0. GATE
def gate():
    print('=== GATE: rebuild 717 through build_blocks and check by_depth ===')
    seeds = KNOWN_717['A']
    cfg = build_blocks(BLOCKS_D2_4F2, seeds)
    assert cfg is not None, 'gate: build_blocks returned None for known-A seeds!'
    total, bd = eval_batch([cfg])[0]
    want_bd = {1: 210, 2: 210, 3: 158, 4: 102, 5: 36, 6: 1}
    ok = total == 717 and bd == want_bd
    print(f'  quats={cfg}')
    print(f'  total={total} (want 717)  by_depth={bd}')
    print(f'  want_bd={want_bd}')
    print(f'  GATE {"PASS" if ok else "FAIL"}')
    log({'phase': 0, 'tag': 'gate-A', 'seeds': [list(s) for s in seeds],
         'quats': cfg, 'total': total, 'by_depth': bd, 'gate_ok': ok})
    # second known config too (sanity, not required to match a stated bd)
    seedsB = KNOWN_717['B']
    cfgB = build_blocks(BLOCKS_D2_4F2, seedsB)
    totalB, bdB = eval_batch([cfgB])[0]
    print(f'  known-B: quats={cfgB} total={totalB} by_depth={bdB}')
    log({'phase': 0, 'tag': 'gate-B', 'seeds': [list(s) for s in seedsB],
         'quats': cfgB, 'total': totalB, 'by_depth': bdB})
    if not ok:
        print('  *** GATE FAILED -- STOPPING per spec.', flush=True)
        sys.exit(1)
    return ok


# ==================================================== budget-aware eval
class Budget:
    def __init__(self, cap):
        self.cap = cap
        self.n = 0
        self.exhausted = False

    def remaining(self):
        return max(0, self.cap - self.n)

    def spend(self, k):
        self.n += k
        if self.n >= self.cap:
            self.exhausted = True


TASK1_TOTALS = []   # (total, bd, seeds) collected during task1, for reporting
TASK2_TOTALS = []


def do_eval_seeds(blocks, seeds_list, tag, stage, budget, collector, flagged):
    """Evaluate a batch of seed-lists (each a list of nblk integer-quat
    tuples). Filters to valid 6-coset builds, calls the C++ engine in one
    batched call (<=4 workers via ss.cpp_batch), logs every eval, flags
    total>717 or a deep-ceiling violation. Returns list of
    (seeds, total, bd) for successful builds. Respects the eval Budget."""
    if budget.exhausted or not seeds_list:
        return []
    cfgs, metas = [], []
    for seeds in seeds_list:
        cfg = build_blocks(blocks, seeds)
        if cfg is not None:
            cfgs.append(cfg)
            metas.append(seeds)
    if not cfgs:
        return []
    res = eval_batch(cfgs)
    out = []
    for seeds, cfg, r in zip(metas, cfgs, res):
        if r is None:
            continue
        total, bd = r
        budget.spend(1)
        rec = {'phase': 1, 'tag': tag, 'stage': stage,
               'seeds': [list(s) for s in seeds], 'quats': cfg,
               'total': total, 'by_depth': bd}
        log(rec)
        collector.append((total, dict(bd), [tuple(s) for s in seeds]))
        v = violation(bd)
        if v or total > RECORD:
            flagged.append((total, seeds, bd, v))
            marker = 'RECORD>717' if total > RECORD else 'CEILING-VIOLATION'
            print(f'    *** {marker}: {tag}/{stage} total={total} {v or ""} '
                  f'seeds={[list(s) for s in seeds]}', flush=True)
        out.append((seeds, total, bd))
    return out


# ================================================= 1. large-neighborhood moves
SINGLE_DELTAS = (-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6)
TWO_DELTAS = (-2, -1, 1, 2)


def single_moves(seeds, nblk):
    out = []
    for i in range(nblk):
        for comp in range(4):
            for d in SINGLE_DELTAS:
                ns = [list(s) for s in seeds]
                ns[i][comp] += d
                ns[i] = gcdq(ns[i])
                if cap_ok(ns[i]):
                    out.append([tuple(x) for x in ns])
    return out


def two_comp_same_block_moves(seeds, nblk):
    out = []
    for i in range(nblk):
        for c1, c2 in combinations(range(4), 2):
            for d1 in TWO_DELTAS:
                for d2 in TWO_DELTAS:
                    ns = [list(s) for s in seeds]
                    ns[i][c1] += d1
                    ns[i][c2] += d2
                    ns[i] = gcdq(ns[i])
                    if cap_ok(ns[i]):
                        out.append([tuple(x) for x in ns])
    return out


def two_comp_cross_block_moves(seeds, nblk):
    """Escape-hatch neighborhood: one component moves in block i AND one
    (same-index) component moves in a DIFFERENT block j, simultaneously.
    Only tried when the single+same-block neighborhood is exhausted (see
    climb()) -- this is the joint move a one-component-at-a-time climb can
    never take, since each intermediate single-component step might not
    improve even though the joint step does."""
    out = []
    for i, j in combinations(range(nblk), 2):
        for c in range(4):
            for d1 in TWO_DELTAS:
                for d2 in TWO_DELTAS:
                    ns = [list(s) for s in seeds]
                    ns[i][c] += d1
                    ns[j][c] += d2
                    ns[i] = gcdq(ns[i])
                    ns[j] = gcdq(ns[j])
                    if cap_ok(ns[i]) and cap_ok(ns[j]):
                        out.append([tuple(x) for x in ns])
    return out


def climb(seeds0, nblk, blocks, tag, max_steps, budget, flagged,
          collector=TASK1_TOTALS):
    """Greedy hill-climb with the large neighborhood. Primary pass =
    single(+-1..+-6) + two-component-same-block(+-1/+-2); if that finds no
    improving move, try the cross-block two-component escape pass before
    declaring a local max. Returns dict with final seeds/total/bd/steps/
    escapes/is_local_max (True only if the FULL neighborhood, incl.
    escape, found nothing better -- i.e. a certified local max at this
    radius)."""
    cur = [gcdq(s) for s in seeds0]
    cfg0 = build_blocks(blocks, cur)
    if cfg0 is None:
        # Degenerate start (a perturbed seed collapsed the compound to
        # fewer than 6 distinct cubes, or built an invalid frame). Not a
        # find and not a bug -- skip this restart instead of aborting.
        return {'seeds': cur, 'total': -1, 'bd': {}, 'steps': 0,
                'escapes': 0, 'is_local_max': False, 'skipped': True}
    cur_total, cur_bd = eval_batch([cfg0])[0]
    budget.spend(1)
    log({'phase': 1, 'tag': tag, 'stage': 'climb-start',
         'seeds': [list(s) for s in cur], 'quats': cfg0,
         'total': cur_total, 'by_depth': cur_bd})
    collector.append((cur_total, dict(cur_bd), [tuple(s) for s in cur]))
    steps, escapes = 0, 0
    is_local_max = False
    for step in range(max_steps):
        if budget.exhausted:
            break
        cands = single_moves(cur, nblk) + two_comp_same_block_moves(cur, nblk)
        results = do_eval_seeds(blocks, cands, tag, f'climb{step}', budget,
                                 collector, flagged)
        steps += 1
        moved = False
        if results:
            best = max(results, key=lambda t: t[1])
            if best[1] > cur_total:
                cur, cur_total, cur_bd = best[0], best[1], best[2]
                moved = True
        if moved:
            continue
        # primary neighborhood exhausted -- try the cross-block escape
        if budget.exhausted:
            break
        esc_cands = two_comp_cross_block_moves(cur, nblk)
        esc_results = do_eval_seeds(blocks, esc_cands, tag,
                                     f'climb{step}-escape', budget,
                                     collector, flagged)
        if esc_results:
            best = max(esc_results, key=lambda t: t[1])
            if best[1] > cur_total:
                cur, cur_total, cur_bd = best[0], best[1], best[2]
                escapes += 1
                continue
        is_local_max = True
        break
    return {'seeds': cur, 'total': cur_total, 'bd': cur_bd, 'steps': steps,
            'escapes': escapes, 'is_local_max': is_local_max}


def perturb(seeds, nblk, rng, nmoves):
    """5-10 random small (+-1/+-2) moves off a base config, one component
    of one random block per move, re-gcd + cap each move."""
    cur = [list(s) for s in seeds]
    for _ in range(nmoves):
        i = rng.randrange(nblk)
        comp = rng.randrange(4)
        d = rng.choice(TWO_DELTAS)
        cur[i][comp] += d
        cur[i] = list(gcdq(cur[i]))   # gcdq returns a tuple; keep cur[i] mutable
        if not cap_ok(cur[i]):
            cur[i][comp] -= d   # undo an out-of-cap move
            cur[i] = list(gcdq(cur[i]))
    return [tuple(s) for s in cur]


TASK1_BUDGET = 20000


def run_task1():
    print('\n=== TASK 1: deep-climb the two known 717 configs, LARGER '
          'neighborhood (single +-1..+-6, two-component +-1/+-2 same-block, '
          'cross-block escape) ===')
    budget = Budget(TASK1_BUDGET)
    flagged = []
    results = {}
    t0 = time.time()

    # -- direct climbs from the two known 717 configs (no perturbation) --
    for tag_base, seeds0 in KNOWN_717.items():
        r = climb(seeds0, 3, BLOCKS_D2_4F2, f'deepclimb-{tag_base}',
                  max_steps=8, budget=budget, flagged=flagged)
        results[tag_base] = r
        print(f'  direct climb from known-{tag_base}: '
              f'{seeds0} -> total={r["total"]} steps={r["steps"]} '
              f'escapes={r["escapes"]} local_max={r["is_local_max"]} '
              f'budget_used={budget.n}/{budget.cap}', flush=True)
        if budget.exhausted:
            print('  *** task1 budget exhausted during direct climbs.',
                  flush=True)
            break

    # -- ~30 perturbed restarts (5-10 random small moves off 717) --
    restarts = []
    n_restarts_target = 30
    n_restarts_done = 0
    for k in range(n_restarts_target):
        if budget.exhausted:
            break
        base_tag = 'A' if k % 2 == 0 else 'B'
        base = KNOWN_717[base_tag]
        nmoves = RNG.randint(5, 10)
        seeds0 = perturb(base, 3, RNG, nmoves)
        r = climb(seeds0, 3, BLOCKS_D2_4F2,
                  f'deepclimb-restart{k}-from{base_tag}', max_steps=5,
                  budget=budget, flagged=flagged)
        r['base'] = base_tag
        r['perturb_moves'] = nmoves
        r['start_seeds'] = seeds0
        restarts.append(r)
        n_restarts_done += 1
        print(f'  restart {k:2d} (base {base_tag}, {nmoves} moves off): '
              f'total={r["total"]} local_max={r["is_local_max"]} '
              f'budget={budget.n}/{budget.cap}', flush=True)

    dt = time.time() - t0
    best_overall = max(
        [(results[k]['total'], k, results[k]) for k in results] +
        [(r['total'], f'restart{i}', r) for i, r in enumerate(restarts)],
        key=lambda t: t[0]) if (results or restarts) else None
    print(f'\n  TASK1 done: {budget.n} evals, {dt:.0f}s, '
          f'{n_restarts_done}/{n_restarts_target} restarts completed.')
    if best_overall:
        print(f'  best: total={best_overall[0]} from {best_overall[1]}')
    return {'direct': results, 'restarts': restarts, 'flagged': flagged,
            'evals': budget.n, 'budget': TASK1_BUDGET, 'dt': dt,
            'n_restarts_done': n_restarts_done,
            'n_restarts_target': n_restarts_target}


# ================================================== 2. broad D2-family sweep
TASK2_BUDGET = 16000


def aligned_starts(block_batteries, cap):
    combos = list(product(*block_batteries))
    if len(combos) > cap:
        stride = len(combos) / cap
        combos = [combos[int(i * stride)] for i in range(cap)]
    return [list(c) for c in combos]


def run_task2():
    print('\n=== TASK 2: broad D2 family resweep (60 restarts) + siblings '
          '(D2:2+4, D2:2+2+2) at full-quat resolution ===')
    budget = Budget(TASK2_BUDGET)
    out = {}
    t0 = time.time()

    def check_budget_wrap(nev):
        budget.spend(nev)

    # ---- 2a: D2:4+free2 resweep, more restarts + deeper climb ----
    d2b4 = ss2.aligned_seed_battery(D2q, 4)
    freeb = [(1, 0, 0, 0), (2, 1, 1, 1), (3, 1, 1, 1), (5, 2, 2, 2),
             (2, 1, 0, 0), (3, 2, 1, 0), (4, 1, 1, 1)]
    d2_starts = aligned_starts([d2b4, freeb, freeb], cap=140)
    # anchor both known 717 configs explicitly
    d2_starts += [KNOWN_717['A'], KNOWN_717['B']]
    n_random_remaining = min(60, budget.remaining() // 50)
    best, nev, nres, fl = ss2.search_blocks(
        'D2', BLOCKS_D2_4F2, 'D2:4+free2-resweep', d2_starts,
        n_random=60, climb_steps=16, rng=RNG,
        note='(broad resweep, 60 restarts + 2 known-717 anchors, r2 x16)')
    check_budget_wrap(nev)
    out['D2:4+free2-resweep'] = dict(best=best, evals=nev, restarts=nres,
                                     flagged=fl)
    print(f'  2a D2:4+free2 resweep: best={best["total"]} evals={nev} '
          f'budget={budget.n}/{budget.cap}', flush=True)

    if budget.exhausted:
        print('  *** task2 budget exhausted after 2a; skipping siblings.')
        out['dt'] = time.time() - t0
        out['evals'] = budget.n
        return out

    # ---- 2b: D2:2+4 (orbit-2 + orbit-4 under the SAME D2 group) ----
    d2b2 = ss2.aligned_seed_battery(D2q, 2)
    b_starts = []
    for _ in range(80):
        s2 = d2b2[RNG.randrange(len(d2b2))]
        s4 = gcdq([RNG.randint(-MAXC, MAXC) for _ in range(4)])
        b_starts.append([s2, s4])
    for s2 in d2b2:
        for s4 in d2b4[:6]:
            b_starts.append([s2, s4])
    best, nev, nres, fl = ss2.search_blocks(
        'D2', [D2q, D2q], 'D2:2+4', b_starts, n_random=0, climb_steps=14,
        rng=RNG, note='(orbit-2 aligned x orbit-4, 2 blocks)')
    check_budget_wrap(nev)
    out['D2:2+4'] = dict(best=best, evals=nev, restarts=nres, flagged=fl)
    print(f'  2b D2:2+4: best={best["total"]} evals={nev} '
          f'budget={budget.n}/{budget.cap}', flush=True)

    if budget.exhausted:
        print('  *** task2 budget exhausted after 2b; skipping 2c.')
        out['dt'] = time.time() - t0
        out['evals'] = budget.n
        return out

    # ---- 2c: D2:2+2+2 (three orbit-2 blocks under D2) ----
    c_starts = aligned_starts([d2b2, d2b2, d2b2], cap=120)
    best, nev, nres, fl = ss2.search_blocks(
        'D2', [D2q, D2q, D2q], 'D2:2+2+2', c_starts, n_random=20,
        climb_steps=10, rng=RNG, note='(three orbit-2 D2 blocks)')
    check_budget_wrap(nev)
    out['D2:2+2+2'] = dict(best=best, evals=nev, restarts=nres, flagged=fl)
    print(f'  2c D2:2+2+2: best={best["total"]} evals={nev} '
          f'budget={budget.n}/{budget.cap}', flush=True)

    out['dt'] = time.time() - t0
    out['evals'] = budget.n
    return out


# ============================================================== 3. tradeoff
def shallow_tail_table():
    """Scan d2_deepclimb.jsonl (this run only) for every eval with a
    by_depth, group by d3 value, report the best total seen at each d3."""
    best_by_d3 = {}
    n = 0
    with open(LOG_PATH) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            bd = r.get('by_depth')
            total = r.get('total')
            if bd is None or total is None:
                continue
            d3 = bd.get('3') if '3' in bd else bd.get(3)
            if d3 is None:
                continue
            n += 1
            cur = best_by_d3.get(d3)
            if cur is None or total > cur[0]:
                best_by_d3[d3] = (total, r.get('quats'), r.get('seeds'), bd)
    return best_by_d3, n


# =================================================================== main
def write_report(gate_ok, t1, t2, table, n_scanned):
    L = []
    L.append('# D2 deep-climb + shallow-tail tradeoff report\n')
    L.append('Working principles: D2_DEEPCLIMB_SPEC.md. Generated by '
             'd2_deepclimb.py. Reuses symmetry_search.py / '
             'symmetry_search2.py validated construction/orbit machinery '
             'and (task 2) climber unchanged; task 1 uses a NEW larger '
             'neighborhood (single +-1..+-6, two-component +-1/+-2 '
             'same-block, cross-block escape) as specified.\n')

    L.append('## Gate\n')
    L.append(f'- Rebuild 717 via `build_blocks` from seeds `[(5,2,2,2),'
             f'(2,1,1,1),(1,0,0,0)]`: **{"PASS" if gate_ok else "FAIL"}** '
             f'(total=717, by_depth={{1:210,2:210,3:158,4:102,5:36,6:1}}).\n')

    L.append('## Task 1: deep climb from the two known 717 configs\n')
    best1 = -1
    best1_info = None
    for tag, r in t1['direct'].items():
        L.append(f'- direct climb from known-{tag}: start total=717 -> '
                 f'final total=**{r["total"]}**, steps={r["steps"]}, '
                 f'escape-moves used={r["escapes"]}, '
                 f'certified local max (full neighborhood, incl. '
                 f'cross-block escape) = **{r["is_local_max"]}**, '
                 f'final seeds={[list(s) for s in r["seeds"]]}')
        if r['total'] > best1:
            best1, best1_info = r['total'], ('direct-' + tag, r)
    for i, r in enumerate(t1['restarts']):
        if r['total'] > best1:
            best1, best1_info = r['total'], (f'restart{i}', r)
    L.append(f'\n- {t1["n_restarts_done"]}/{t1["n_restarts_target"]} '
             f'perturbed restarts completed within the {t1["budget"]}-eval '
             f'task-1 budget ({t1["evals"]} evals used, {t1["dt"]:.0f}s).')
    if t1['restarts']:
        rtot = [r['total'] for r in t1['restarts']]
        L.append(f'- restart final totals: min={min(rtot)}, '
                 f'max={max(rtot)}, mean={sum(rtot)/len(rtot):.1f} '
                 f'(all measured against the 717 starting point).')
    L.append(f'\n**Task-1 best total found: {best1}** '
             f'({"NEW RECORD" if best1 > 717 else "does not beat 717"}) '
             f'via {best1_info[0] if best1_info else "n/a"}.\n')
    if t1['flagged']:
        L.append('**Flags (records>717 or ceiling violations) during task 1:**')
        for f in t1['flagged']:
            L.append(f'- {f}')
    else:
        L.append('No flags during task 1: nothing exceeded 717, no deep '
                 'ceiling (d3<=164/d4<=102/d5<=36) was breached.')
    L.append('')

    L.append('## Task 2: broad D2 family resweep + siblings\n')
    L.append('| family | best total | vs 717 | evals | restarts |')
    L.append('|---|---|---|---|---|')
    best2 = -1
    best2_fam = None
    for fam, r in t2.items():
        if fam in ('dt', 'evals'):
            continue
        b = r['best']
        tot = b['total']
        if tot > best2:
            best2, best2_fam = tot, fam
        cmp = ('BEATS' if tot > 717 else 'ties' if tot == 717 else
               f'{tot-717:+d}')
        L.append(f'| {fam} | {tot} | {cmp} | {r["evals"]} | {r["restarts"]} |')
    L.append(f'\nTask 2 total evals: {t2.get("evals", "n/a")}, '
             f'wall time {t2.get("dt", 0):.0f}s.')
    allflag2 = []
    for fam, r in t2.items():
        if isinstance(r, dict):
            allflag2 += r.get('flagged', []) or []
    if allflag2:
        L.append('\n**Flags during task 2:**')
        for f in allflag2:
            L.append(f'- {f}')
    else:
        L.append('\nNo flags during task 2.')
    L.append('')

    L.append('## Task 3: the shallow-tail (d3-vs-total) exchange-rate table\n')
    L.append(f'Aggregated over all {n_scanned} evals in this run that carry '
             f'a by_depth (both task 1 and task 2 logs).\n')
    L.append('| d3 | best total at this d3 | quats |')
    L.append('|---|---|---|')
    for d3 in sorted(table.keys()):
        tot, quats, seeds, bd = table[d3]
        L.append(f'| {d3} | {tot} | `{quats}` |')
    L.append('')
    hunt = {d3: v for d3, v in table.items() if 150 <= d3 <= 162}
    L.append('### Hunt zone d3 in [150,162]\n')
    if hunt:
        for d3 in sorted(hunt):
            tot = hunt[d3][0]
            L.append(f'- d3={d3}: best total={tot} '
                     f'({"BEATS 717" if tot > 717 else "<=717"})')
        best_hunt = max(hunt.items(), key=lambda kv: kv[1][0])
        L.append(f'\nBest in hunt zone: d3={best_hunt[0]}, '
                 f'total={best_hunt[1][0]}.')
    else:
        L.append('No evals observed with d3 in [150,162] in this run\'s log.')
    L.append('')
    if table:
        overall_best_d3, overall_best = max(table.items(),
                                             key=lambda kv: kv[1][0])
        L.append(f'**Global best in this run: total={overall_best[0]} at '
                 f'd3={overall_best_d3}.**')
        d3_158 = table.get(158)
        verdict = ('158 remains the sweet spot in this run\'s coverage: no '
                   'd3<158 config reached above the d3=158 best.')
        if d3_158 and overall_best[0] > d3_158[0] and overall_best_d3 != 158:
            verdict = (f'A d3={overall_best_d3} config beat the d3=158 '
                       f'best ({overall_best[0]} > {d3_158[0]}) -- the '
                       f'shallow-tail tradeoff extends past 158 in this run.')
        L.append(verdict)
    L.append('')

    with open(REPORT_PATH, 'w') as f:
        f.write('\n'.join(L) + '\n')
    print(f'\nReport -> {REPORT_PATH}')


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    gate_ok = True
    t1 = {'direct': {}, 'restarts': [], 'flagged': [], 'evals': 0,
          'budget': TASK1_BUDGET, 'dt': 0, 'n_restarts_done': 0,
          'n_restarts_target': 30}
    t2 = {'evals': 0, 'dt': 0}
    if mode in ('gate', 'task1', 'task2', 'all'):
        gate_ok = gate()
    if mode in ('task1', 'all'):
        t1 = run_task1()
    if mode in ('task2', 'all'):
        t2 = run_task2()
    if mode in ('task1', 'task2', 'all'):
        table, n_scanned = shallow_tail_table()
        write_report(gate_ok, t1, t2, table, n_scanned)


if __name__ == '__main__':
    main()
