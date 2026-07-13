#!/usr/bin/env python3
# Working principles: BLUEPRINT_SPEC.md; blueprint_enum.py (catalog source);
# shared_axis_search.py (REUSED verbatim: genome format, build_config,
# cluster_quats, random_genome/locked_genome, climb, multi_restart -- none
# of that machinery is rewritten here, only driven with a smaller
# per-blueprint budget over the full catalog and a different log target);
# six_cube_search_results.md Postscripts 12/17/17-addendum/18/19; PROJECT.md.
"""blueprint_search.py -- run the knob search (spoke-angle grid + free-cube
hill-climb, exactly shared_axis_search.py's climb()/multi_restart()) over
EVERY surviving blueprint in blueprint_enum.py's catalog.

Self-contained driver: run this once, detached (nohup), and it writes
blueprint_search.jsonl (every eval) and blueprint_search_report.md (the
final report) itself when done -- no external monitor loop needed. The
report file is rewritten after every blueprint finishes, so progress is
visible via `ls -la blueprint_search_report.md` / `tail` at any time
without blocking on this process.

GATE (task item 2): blueprint 47 (onaxis3+spoke3 on (1,1,1), the exact
skeleton of the 723 record) must (a) survive the catalog (asserted in
blueprint_enum.py) and (b) have its knob optimization reproduce 723 -- both
via shared_axis_search.run_gates()'s exact hardcoded reconstruction AND via
this script's own optimizer seeded with the same construction. Both must
pass before the main sweep runs.

Budget: reduced from shared_axis_search.py's per-template budget (which
used n_random_free=8, steps=22, restarts_wide=6 for ~13-17k evals and
10-23 minutes per n=6 template) to fit 67 blueprints in one detached run;
see BUDGET_DEFAULT/BUDGET_GATE below. This is a real, disclosed coverage
reduction -- the report states it explicitly per BLUEPRINT_SPEC.md's
"state the per-blueprint coverage honestly" requirement.

Any total > 723 is flagged immediately AND cross-checked against the
independent Python oracle (certify_six.exact_count_config via
golden_rotations.rot_from_quat, the same cross-check pattern used in
symmetry_search.py's gate_E) before being reported as real.

Usage:
  python3 blueprint_search.py            # gate, then full sweep + report
  python3 blueprint_search.py gate       # gate only, then stop
"""
import json
import os
import random
import sys
import time

import blueprint_enum as be
import shared_axis_search as sas
from certify_six import exact_count_config
from golden_rotations import rot_from_quat

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(HERE, 'blueprint_search.jsonl')
REPORT_PATH = os.path.join(HERE, 'blueprint_search_report.md')
RECORD = 723

BUDGET_DEFAULT = dict(n_random_free=2, steps_free=6, restarts_wide_free=1,
                       n_random_locked=1, steps_locked=4, restarts_wide_locked=0)
BUDGET_GATE = dict(n_random_free=6, steps_free=18, restarts_wide_free=4,
                    n_random_locked=2, steps_locked=12, restarts_wide_locked=2)

# ------------------------------------------------------------ log override
# shared_axis_search.climb()/multi_restart() call the module-level name
# `log` inside shared_axis_search's own namespace -- monkeypatching
# sas.log redirects every eval THIS process logs to OUR file
# (blueprint_search.jsonl) instead of shared_axis_search.jsonl (which a
# separate, still-running shared_axis_search.py process owns -- writing to
# it here would race that process and is not this task's file to modify).
_CURRENT_BP = {'id': None, 'tag': None}


def log(rec):
    rec = dict(rec)
    rec['bp_id'] = _CURRENT_BP['id']
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')


sas.log = log


def verify_with_oracle(quats):
    """Independent Python-oracle cross-check (certify_six.exact_count_config
    via golden_rotations.rot_from_quat) -- the same pattern symmetry_search.
    py's gate_E uses to cross-check the C++ engine. Returns (total, by_depth
    with depth-0 stripped)."""
    rots = [rot_from_quat(*q) for q in quats]
    total, bd = exact_count_config(rots, verbose=False)
    bd_pos = {k: v for k, v in bd.items() if k != 0}
    return total, bd_pos


# =============================================================== GATE
def gate():
    print('=== GATE: hardcoded reconstruction (shared_axis_search.run_gates) ===', flush=True)
    gates = sas.run_gates()  # raises SystemExit if either fails -- required behavior
    assert gates['gate723'] == 723

    print('=== GATE: catalog membership ===', flush=True)
    catalog = be.build_catalog()
    gate_rows = [r for r in catalog if r.get('is_gate')]
    assert len(gate_rows) == 1 and gate_rows[0]['status'] == 'SURVIVOR', \
        'GATE blueprint missing or pruned -- catalog is broken'
    gate_row = gate_rows[0]
    print(f'  blueprint {gate_row["id"]} ({gate_row["tag"]}) is a SURVIVOR.  PASS', flush=True)

    print('=== GATE: knob optimization reproduces 723 from this blueprint\'s own search ===', flush=True)
    rng = random.Random(20260713)
    seed723 = {'axis_name': '(1,1,1)',
               'clusters': [{'kind': 'spoke', 'base': (4, 1, 1, -1),
                              'angles': [(0, 1), (1, 1), (-1, 1)]},
                             {'kind': 'onaxis', 'base': None,
                              'angles': [(1, 2), (1, 1), (2, 5)]}],
               'free': []}
    _CURRENT_BP['id'], _CURRENT_BP['tag'] = gate_row['id'], gate_row['tag']
    rec = run_blueprint(gate_row['tag'], '(1,1,1)', gate_row['spec'], RECORD,
                         BUDGET_GATE, start_genomes=[seed723], rng=rng)
    ok = rec['free_best'] is not None and rec['free_best'] >= RECORD
    print(f'  optimizer best = {rec["free_best"]} (want >=723)  '
          f'{"PASS" if ok else "FAIL"}', flush=True)
    if not ok:
        raise SystemExit('GATE FAILED -- blueprint search pipeline did not reproduce 723.')
    print('  GATE PASSES.\n', flush=True)
    return gates, gate_row, rec


# ========================================================= per-blueprint run
ALL_RESULTS = {}


def run_blueprint(tag, axis_name, spec, record, budget, start_genomes=(), rng=None):
    t0 = time.time()
    locked_starts = ([sas.locked_genome(axis_name, spec, rng)]
                      if budget['n_random_locked'] > 0 else [])
    locked = sas.multi_restart(spec, axis_name, budget['n_random_locked'], rng,
                                steps=budget['steps_locked'],
                                restarts_wide=budget['restarts_wide_locked'],
                                tag=tag, part='locked', start_genomes=locked_starts)
    free = sas.multi_restart(spec, axis_name, budget['n_random_free'], rng,
                              steps=budget['steps_free'],
                              restarts_wide=budget['restarts_wide_free'],
                              tag=tag, part='free', start_genomes=start_genomes)
    dt = time.time() - t0
    rec = dict(tag=tag, axis=axis_name, spec=spec, record=record,
               locked_best=locked['best_total'], free_best=free['best_total'],
               locked_genome=locked['best_genome'], free_genome=free['best_genome'],
               free_bd=free['best_bd'], evals=locked['evals'] + free['evals'], dt=dt)
    ALL_RESULTS[tag] = rec
    return rec


def handle_possible_beat(bp_row, rec):
    """If free_best > 723, verify immediately with the Python oracle before
    trusting it, and log a prominent FLAG record."""
    fb = rec['free_best']
    if fb is None or fb <= RECORD:
        return None
    cfg = sas.genome_config2(rec['free_genome'])
    py_total, py_bd = verify_with_oracle(cfg)
    verified = (py_total == fb)
    flag = dict(FLAG='CANDIDATE BEATS 723', bp_id=bp_row['id'], tag=rec['tag'],
                cpp_total=fb, oracle_total=py_total, verified=verified,
                quats=cfg, by_depth=rec['free_bd'])
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(flag) + '\n')
    print(f'  !!!! candidate {fb} > 723 for {rec["tag"]}: '
          f'oracle={py_total} verified={verified} !!!!', flush=True)
    return flag


# ================================================================= REPORT
def write_report(catalog, gate_info, t_start, done_so_far, beats, in_progress=True):
    gates, gate_row, gate_rec = gate_info
    L = []
    L.append('# Blueprint branch-and-prune search report (n=6)\n')
    L.append('Working principles: BLUEPRINT_SPEC.md; blueprint_enum.py (catalog); '
             'shared_axis_search.py (reused cluster/spoke/climb machinery); '
             'six_cube_search_results.md Postscripts 12/17/17-addendum/18/19; '
             'PROJECT.md. Generated by blueprint_search.py.\n')
    status_line = 'IN PROGRESS (partial results below; rewritten after every ' \
                   'blueprint)' if in_progress else 'COMPLETE'
    L.append(f'**Status: {status_line}**\n')

    survivors = [r for r in catalog if r['status'] == 'SURVIVOR']
    p2 = [r for r in catalog if r['status'] == 'PRUNED-P2']
    p3 = [r for r in catalog if r['status'] == 'PRUNED-P3']
    L.append('## 1. Catalog\n')
    L.append(f'{len(catalog)} entries enumerated up to symmetry '
             f'(blueprint_enum.py, Stage A\' 103 -> {len(survivors)} canonical '
             f'after P1a size-1-collapse + P1b onaxis-merge): '
             f'**{len(survivors)} SURVIVOR, {len(p2)} PRUNED-P2 (frustration, '
             f'golden/octahedral wall), {len(p3)} PRUNED-P3 (dominance, '
             f'multi-axis/polyhedral-forcing)**. Full per-entry table with '
             f'prune reasons: run `python3 blueprint_enum.py`.\n')
    L.append('| id | tag | axis | status | reason |')
    L.append('|---|---|---|---|---|')
    for r in catalog:
        axis_disp = r['axis'] if r['axis'] else 'n.a.'
        L.append(f'| {r["id"]} | {r["tag"]} | {axis_disp} | {r["status"]} | {r["reason"]} |')
    L.append('')

    L.append('## 2. Gate\n')
    L.append(f'- Hardcoded reconstruction (shared_axis_search.run_gates): '
             f'183={gates["gate183"]} (want 183), 723={gates["gate723"]} '
             f'(want 723) -- {"PASS" if gates["gate723"]==723 else "FAIL"}.')
    L.append(f'- Blueprint {gate_row["id"]} ({gate_row["tag"]}) is a catalog SURVIVOR.')
    L.append(f'- This script\'s own knob optimizer (seeded from the 723 '
             f'construction, budget={BUDGET_GATE}) on that blueprint: '
             f'best={gate_rec["free_best"]} (want >=723) -- '
             f'{"PASS" if gate_rec["free_best"] and gate_rec["free_best"]>=723 else "FAIL"}.')
    L.append('')

    L.append('## 3. Per-blueprint results\n')
    L.append(f'Budget per blueprint (reduced from shared_axis_search.py\'s own '
             f'per-template budget to cover all {len(survivors)} survivors in '
             f'one detached run): {BUDGET_DEFAULT} (gate blueprint used the '
             f'larger {BUDGET_GATE}). This is coarse first-pass coverage, '
             f'disclosed as such -- see verdict.\n')
    L.append(f'{len(done_so_far)}/{len(survivors)} blueprints completed so far.\n')
    L.append('| tag | axis | locked best | free best | vs 723 | evals | dt(s) |')
    L.append('|---|---|---|---|---|---|---|')
    for tag in done_so_far:
        r = ALL_RESULTS[tag]
        fb = r['free_best']
        cmp = ('BEATS' if fb and fb > RECORD else
               ('TIES' if fb == RECORD else
                (f'{fb - RECORD:+d}' if fb is not None else '?')))
        L.append(f'| {tag} | {r["axis"]} | {r["locked_best"]} | {fb} | {cmp} | '
                 f'{r["evals"]} | {r["dt"]:.0f} |')
    L.append('')

    L.append('## 4. Candidates beating 723\n')
    if beats:
        for flag in beats:
            L.append(f'- **{flag["tag"]}**: cpp_total={flag["cpp_total"]} '
                     f'oracle_total={flag["oracle_total"]} '
                     f'verified={flag["verified"]} quats={flag["quats"]}')
    else:
        L.append('None so far.')
    L.append('')

    L.append('## 5. Verdict\n')
    if in_progress:
        L.append(f'Campaign still running ({len(done_so_far)}/{len(survivors)} '
                  f'blueprints done); this section will be replaced with the '
                  f'final verdict sentence when complete.')
    else:
        any_beat = any(f['verified'] for f in beats)
        best_overall = max((ALL_RESULTS[t]['free_best'] for t in done_so_far
                             if ALL_RESULTS[t]['free_best'] is not None), default=None)
        if any_beat:
            L.append(f'**A blueprint BEATS 723**, verified by the independent '
                     f'Python oracle (certify_six.exact_count_config). See '
                     f'Section 4.')
        else:
            L.append(f'**No blueprint beats 723** at the coverage stated above '
                     f'(budget {BUDGET_DEFAULT}, {len(survivors)}/{len(survivors)} '
                     f'canonical survivors run; best observed = {best_overall}). '
                     f'The blueprint level is exhausted up to this stated '
                     f'per-blueprint coverage -- not a proof for arbitrarily '
                     f'fine coverage, but every combinatorial skeleton in the '
                     f'rational shared-axis/free family has now been tried, '
                     f'not just the 6 hand-picked templates of Postscript 18.')
    L.append(f'\nTotal wall time so far: {time.time() - t_start:.0f}s.')
    with open(REPORT_PATH, 'w') as f:
        f.write('\n'.join(L) + '\n')


# ================================================================= MAIN
def main():
    t_start = time.time()
    gate_info = gate()
    gates, gate_row, gate_rec = gate_info

    catalog = be.build_catalog()
    survivors = [r for r in catalog if r['status'] == 'SURVIVOR']
    rng = random.Random(20260713)

    done_so_far = [gate_row['tag']]   # already run by gate()
    beats = []
    fb0 = ALL_RESULTS[gate_row['tag']]['free_best']
    if fb0 and fb0 > RECORD:
        flag = handle_possible_beat(gate_row, ALL_RESULTS[gate_row['tag']])
        if flag:
            beats.append(flag)
    write_report(catalog, gate_info, t_start, done_so_far, beats, in_progress=True)

    for row in survivors:
        if row['tag'] == gate_row['tag']:
            continue  # already run as part of the gate
        _CURRENT_BP['id'], _CURRENT_BP['tag'] = row['id'], row['tag']
        print(f'[{row["id"]}/{len(catalog)}] running {row["tag"]} '
              f'(axis={row["axis"]}) ...', flush=True)
        rec = run_blueprint(row['tag'], row['axis'] or '(1,1,1)', row['spec'],
                             RECORD, BUDGET_DEFAULT, rng=rng)
        beat = ''
        if rec['free_best'] and rec['free_best'] > RECORD:
            flag = handle_possible_beat(row, rec)
            if flag:
                beats.append(flag)
                beat = f' <<< {"VERIFIED BEAT" if flag["verified"] else "UNVERIFIED (oracle disagrees!)"}'
        print(f'    locked={rec["locked_best"]} free={rec["free_best"]} '
              f'(record 723){beat}  evals={rec["evals"]} dt={rec["dt"]:.0f}s', flush=True)
        done_so_far.append(row['tag'])
        write_report(catalog, gate_info, t_start, done_so_far, beats, in_progress=True)

    write_report(catalog, gate_info, t_start, done_so_far, beats, in_progress=False)
    dt = time.time() - t_start
    print(f'\nDONE. {len(done_so_far)}/{len(survivors)} blueprints. '
          f'Total wall time {dt:.0f}s. Report -> {REPORT_PATH}', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'gate':
        gate()
    else:
        main()
