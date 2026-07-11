#!/usr/bin/env python3
# Working principles: MULTIWALL_SPEC.md + multiwall_report.md. Project index: README.md
"""M4 (control): purely-rational double wall -- two independent 60-deg-about-
own-body-diagonal pair relations among 6 otherwise-free rational cubes,
climbed with the C++ engine (./cube_regions_n --quats-stdin). Does stacking
TWO rational-reachable walls beat the 635 rational record, or is the golden
(irrational) stack special? Logs to multiwall_search.jsonl.
"""
import json
import math
import random
import subprocess

LOG = '/Users/dmi/carroll/multiwall_search.jsonl'
ENGINE = '/Users/dmi/carroll/cube_regions_n'
MAXC = 512
QD = (3, 1, 1, 1)   # 60deg about (1,1,1): exact rational quaternion


def qmul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2)


def gcd_reduce(q):
    g = math.gcd(*[abs(c) for c in q])
    if g > 1:
        q = tuple(c // g for c in q)
    if not any(q):
        q = (1, 0, 0, 0)
    return q


def rand_quat(rng, bound=150):
    while True:
        q = tuple(rng.randint(-bound, bound) for _ in range(4))
        if any(q):
            return gcd_reduce(q)


def build_config(q1, q3, q5, q6):
    """cube1=q1, cube2=q1*QD (pair-wall #1), cube3=q3, cube4=q3*QD
    (pair-wall #2), cube5=q5, cube6=q6 free."""
    q2 = gcd_reduce(qmul(q1, QD))
    q4 = gcd_reduce(qmul(q3, QD))
    quats = [q1, q2, q3, q4, q5, q6]
    if any(abs(c) > MAXC for q in quats for c in q):
        return None
    return quats


def run_batch(configs):
    """configs: list of (tag, quats). Runs via --quats-stdin, one call for
    the whole batch (fast: engine startup amortized)."""
    lines = [';'.join(','.join(str(c) for c in q) for q in quats)
             for _, quats in configs]
    proc = subprocess.run([ENGINE, '--quats-stdin'], input='\n'.join(lines),
                           capture_output=True, text=True, timeout=300)
    out = []
    for (tag, quats), line in zip(configs, proc.stdout.strip().split('\n')):
        rec = json.loads(line)
        out.append((tag, quats, rec['bounded'], rec['by_depth']))
    return out


def log(rec):
    with open(LOG, 'a') as f:
        f.write(json.dumps(rec) + '\n')
        f.flush()


def main():
    rng = random.Random(2026)
    best = (0, None, None)

    # --- random search: 400 double-wall configs
    batch = []
    for i in range(400):
        while True:
            q1, q3, q5, q6 = (rand_quat(rng) for _ in range(4))
            quats = build_config(q1, q3, q5, q6)
            if quats is not None:
                break
        batch.append((f'rand{i}', quats))
    results = run_batch(batch)
    for tag, quats, total, bd in results:
        rec = dict(family='M4_doublewall', tag=tag, quats=quats, total=total,
                    by_depth=bd)
        log(rec)
        if total > best[0]:
            best = (total, tag, quats)
    print(f'M4 random search (400): best = {best}')

    # --- matched control: 400 FULLY free 6-cube rational configs (same rng
    # stream continuation), no wall structure at all
    cbatch = []
    for i in range(400):
        quats = [rand_quat(rng, bound=512) for _ in range(6)]
        cbatch.append((f'ctrl{i}', quats))
    cresults = run_batch(cbatch)
    cbest = (0, None, None)
    for tag, quats, total, bd in cresults:
        rec = dict(family='M4_control_free6', tag=tag, quats=quats,
                    total=total, by_depth=bd)
        log(rec)
        if total > cbest[0]:
            cbest = (total, tag, quats)
    print(f'M4 control (400 fully free): best = {cbest}')

    # --- greedy hillclimb on the double-wall family from its best random
    # start: neighbors perturb q1, q3, q5, q6 by +-1/+-2 on one component
    total0, tag0, quats0 = best
    q1, q2, q3, q4, q5, q6 = quats0
    cur = (q1, q3, q5, q6)
    cur_total = total0
    print(f'hillclimb start: {cur} total={cur_total}')
    for step in range(10):
        nbrs = []
        for idx in range(4):
            base = list(cur)
            q = list(base[idx])
            for comp in range(4):
                for delta in (-2, -1, 1, 2):
                    qn = list(q)
                    qn[comp] += delta
                    qn = gcd_reduce(tuple(qn))
                    cand = list(base)
                    cand[idx] = qn
                    nbrs.append(tuple(cand))
        # build configs, filter overflow
        nbatch = []
        seen = set()
        for nb in nbrs:
            if nb in seen:
                continue
            seen.add(nb)
            quats = build_config(*nb)
            if quats is not None:
                nbatch.append((nb, quats))
        results = run_batch([(str(n), q) for n, q in nbatch])
        best_nb, best_total, best_bd = None, cur_total, None
        for (tag, quats, total, bd), (nb, _) in zip(results, nbatch):
            rec = dict(family='M4_doublewall_climb', step=step, tag=tag,
                       quats=quats, total=total, by_depth=bd)
            log(rec)
            if total > best_total:
                best_nb, best_total, best_bd = nb, total, bd
        if best_nb is None:
            print(f'  step {step}: LOCAL MAX at {cur} total={cur_total}')
            break
        cur, cur_total = best_nb, best_total
        print(f'  step {step}: moved to {cur} total={cur_total}', flush=True)

    print(f'\nM4 FINAL: double-wall best = {cur_total} at quats={cur}')
    print(f'M4 control (free6, same budget) best = {cbest[0]}')
    print(f'rational record (unrestricted search, 360k seeds) = 635')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
