#!/usr/bin/env python3
"""Deep parallel hillclimb for n=4, seeded from the 171 record found by
S1's structured-family climb, plus perturbed restarts. Exact via
cube_regions_n --n 4. Logs every eval to n4_search.jsonl (phase 'deepclimb')
so it merges with the rest of the record."""
import json, math, random, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, '/Users/dmi/carroll')
BIN = '/Users/dmi/carroll/cube_regions_n'
LOG = '/Users/dmi/carroll/n4_search.jsonl'
WORKERS = 4
MAXC = 512

def gcd_reduce(ints):
    g = math.gcd(*[abs(c) for c in ints])
    q = [c // g for c in ints] if g > 1 else list(ints)
    if not any(q):
        q = [1, 0, 0, 0]
    return q

def canon(quats):
    out = []
    for q in quats:
        q = gcd_reduce(list(q))
        for c in q:
            if c != 0:
                if c < 0:
                    q = [-x for x in q]
                break
        out.append(tuple(q))
    return tuple(out)

def cpp_eval(quats):
    qstr = ';'.join(','.join(str(c) for c in q) for q in quats)
    try:
        out = subprocess.run([BIN, '--n', '4', '--quats', qstr],
                              capture_output=True, text=True, timeout=30).stdout
        r = json.loads(out)
        return None if 'error' in r else r
    except Exception:
        return None

memo = {}
logf = open(LOG, 'a')

def log_rec(**kw):
    logf.write(json.dumps(kw) + '\n')
    logf.flush()

def eval_many(pool, quats_list, tag):
    keys = [canon(q) for q in quats_list]
    todo, seen = [], set()
    for k in keys:
        if k not in memo and k not in seen:
            seen.add(k)
            todo.append(k)
    results = list(pool.map(lambda k: cpp_eval(list(map(list, k))), todo))
    for k, r in zip(todo, results):
        memo[k] = r
        if r is not None:
            log_rec(kind='rational', phase='deepclimb', tag=tag,
                     quats=[list(q) for q in k], bounded=r['bounded'],
                     by_depth=r['by_depth'])
    return [memo[k] for k in keys]

def neighbors(quats, deltas=(-2, -1, 1, 2)):
    out = []
    for i in range(len(quats)):
        for j in range(4):
            for d in deltas:
                q = [list(x) for x in quats]
                q[i][j] += d
                if all(c == 0 for c in q[i]):
                    continue
                cq = canon(q)
                if any(abs(c) > MAXC for qq in cq for c in qq):
                    continue
                out.append([list(x) for x in cq])
    return out

def climb(pool, start, tag, max_iters=200):
    cur = [list(q) for q in canon(start)]
    r = eval_many(pool, [cur], tag + ':start')[0]
    if r is None:
        return None, None
    cur_total = r['bounded']
    it = 0
    while it < max_iters:
        it += 1
        nbrs = neighbors(cur)
        results = eval_many(pool, nbrs, f'{tag}:it{it}')
        best_i, best_score = -1, cur_total
        for i, rr in enumerate(results):
            if rr is not None and rr['bounded'] > best_score:
                best_i, best_score = i, rr['bounded']
        if best_i < 0:
            break
        cur, cur_total = nbrs[best_i], best_score
    return cur, cur_total

def perturb(quats, nmoves, rng):
    q = [list(x) for x in quats]
    for _ in range(nmoves):
        i, j = rng.randrange(len(q)), rng.randrange(4)
        q[i][j] += rng.choice((-3, -2, -1, 1, 2, 3))
        if all(c == 0 for c in q[i]):
            q[i][j] += 1
    cq = canon(q)
    if any(abs(c) > MAXC for qq in cq for c in qq):
        return None
    return [list(x) for x in cq]

def main():
    seed171 = [[2, 1, -2, 0], [2, -1, -2, 0], [3, 0, 1, 0], [2, 0, -1, 4]]
    rng = random.Random(20260712)
    best = {'total': 0, 'quats': None}

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        # 1) climb straight from the 171 seed (should confirm local max)
        cur, total = climb(pool, seed171, 'from171')
        print(f'climb from171: {total}', flush=True)
        if total and total > best['total']:
            best.update(total=total, quats=cur)

        # 2) many perturbed restarts from the 171 seed
        for rs in range(40):
            pq = perturb(seed171, rng.randrange(1, 5), rng)
            if pq is None:
                continue
            cur, total = climb(pool, pq, f'restart171_{rs}')
            print(f'restart {rs}: {total}', flush=True)
            if total and total > best['total']:
                best.update(total=total, quats=cur)
                print(f'  <-- NEW BEST {total}', flush=True)

        # 3) a batch of fresh random starts, climbed (independent basins)
        for rs in range(20):
            q = [[rng.randint(-400, 400) for _ in range(4)] for _ in range(4)]
            cur, total = climb(pool, q, f'freerandom_{rs}')
            print(f'freerandom {rs}: {total}', flush=True)
            if total and total > best['total']:
                best.update(total=total, quats=cur)
                print(f'  <-- NEW BEST {total}', flush=True)

    print(f'\n=== FINAL BEST: {best["total"]}  quats={best["quats"]} ===',
          flush=True)

if __name__ == '__main__':
    main()
