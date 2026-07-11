#!/usr/bin/env python3
# Working principles: SLIDE3_SPEC_V2.md + slide3_report.md. Project index: README.md
"""SLIDE3_SPEC.md Section 1, Phase P2: exact hill-climb from the top P1
candidates over all 8 free integers (q1, p1, q2, p2, Rw, Rx, Ry, Rz).
"""
import json
import math
import subprocess
import sys
import time

from slide3_search import overlay_quats, fits_cap, gcd_reduce, LOG_PATH, ENGINE

MAXC = 512


def gcd2(q, p):
    g = math.gcd(abs(q), abs(p))
    if g > 1:
        q, p = q // g, p // g
    if q == 0 and p == 0:
        q = 1
    return q, p


def state_to_quats(state):
    q1, p1, q2, p2, rw, rx, ry, rz = state
    return overlay_quats(q1, p1, q2, p2, (rw, rx, ry, rz))


def neighbors(state, deltas=(-2, -1, 1, 2)):
    q1, p1, q2, p2, rw, rx, ry, rz = state
    out = []
    for idx in range(8):
        for d in deltas:
            s = list(state)
            s[idx] += d
            s[0], s[1] = gcd2(s[0], s[1])
            s[2], s[3] = gcd2(s[2], s[3])
            s[4], s[5], s[6], s[7] = gcd_reduce(s[4:8])
            s = tuple(s)
            if all(abs(c) <= MAXC for c in s) and s != state:
                out.append(s)
    return sorted(set(out))


def eval_states(states, log_phase='P2'):
    lines = []
    ok_states = []
    for s in states:
        quats = state_to_quats(s)
        if fits_cap(quats):
            ok_states.append((s, quats))
    if not ok_states:
        return {}
    inp = '\n'.join(';'.join(','.join(map(str, g)) for g in q)
                     for _, q in ok_states) + '\n'
    proc = subprocess.run([ENGINE, '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
    out_lines = proc.stdout.strip().split('\n') if proc.stdout.strip() else []
    assert len(out_lines) == len(ok_states)
    results = {}
    log_f = open(LOG_PATH, 'a')
    for (s, quats), line in zip(ok_states, out_lines):
        rec = json.loads(line)
        if 'error' in rec:
            continue
        total = rec['bounded']
        bd = {int(k): v for k, v in rec['by_depth'].items()}
        results[s] = (total, bd, rec['quats'])
        out = dict(q1=s[0], p1=s[1], q2=s[2], p2=s[3], R=list(s[4:8]),
                    phase=log_phase, quats=rec['quats'], total=total,
                    by_depth=bd)
        log_f.write(json.dumps(out) + '\n')
    log_f.close()
    return results


def hillclimb(start_state, max_steps=12):
    cur = tuple(start_state)
    res = eval_states([cur])
    if cur not in res:
        print(f'  start state invalid/degenerate: {cur}')
        return None
    cur_total, cur_bd, _ = res[cur]
    path = [(cur, cur_total, cur_bd)]
    print(f'  climb start {cur} total={cur_total}')
    for step in range(max_steps):
        nbrs = neighbors(cur)
        res = eval_states(nbrs)
        best_s, best_total, best_bd = None, cur_total, cur_bd
        for s, (t, bd, _) in res.items():
            if t > best_total:
                best_s, best_total, best_bd = s, t, bd
        if best_s is None:
            print(f'  step {step}: LOCAL MAX at {cur} total={cur_total}')
            break
        cur, cur_total, cur_bd = best_s, best_total, best_bd
        path.append((cur, cur_total, cur_bd))
        print(f'  step {step}: -> {cur} total={cur_total}')
    return path


def main():
    with open('/Users/dmi/carroll/slide3_p1_top.json') as f:
        top = json.load(f)
    # dedupe by (q1,p1,q2,p2,R) state, keep top ~12 distinct starts
    seen = set()
    starts = []
    for r in top:
        s = (r['q1'], r['p1'], r['q2'], r['p2'], *r['R'])
        if s in seen:
            continue
        seen.add(s)
        starts.append((r['total'], s))
        if len(starts) >= 12:
            break

    best_overall = (0, None, None)
    t0 = time.time()
    for total0, s in starts:
        print(f'\n=== hillclimb from total={total0} state={s} ===')
        path = hillclimb(s, max_steps=12)
        if path is None:
            continue
        end_state, end_total, end_bd = path[-1]
        if end_total > best_overall[0]:
            best_overall = (end_total, end_state, end_bd)
    dt = time.time() - t0
    print(f'\n=== P2 DONE in {dt:.1f}s ===')
    print(f'best overall: total={best_overall[0]} state={best_overall[1]} '
          f'by_depth={best_overall[2]}')
    with open('/Users/dmi/carroll/slide3_p2_best.json', 'w') as f:
        json.dump({'total': best_overall[0], 'state': best_overall[1],
                   'by_depth': best_overall[2]}, f)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
