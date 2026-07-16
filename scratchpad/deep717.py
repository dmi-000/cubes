import sys, json, itertools
sys.path.insert(0, '/Users/dmi/carroll')
import symmetry_search as ss

D2 = ss.group_quats('D2')
TRIV = [(1, 0, 0, 0)]
BLOCKS = [D2, TRIV, TRIV]
CEIL = {3: 164, 4: 102, 5: 36}

def build(seeds):
    cfg = []
    for ql, s in zip(BLOCKS, seeds):
        s = tuple(ss.gcd_reduce(list(s)))
        if not ss.cap_ok(s):
            return None
        cfg += ss.quat_orbit(ql, s, ss.O_Q5)
    if len(cfg) != 6:
        return None
    if len({ss.coset_key(ss.rot_from_quat(*q), ss.O_Q5) for q in cfg}) != 6:
        return None
    return cfg

def viol(bd):
    for d, c in CEIL.items():
        if bd.get(d, 0) > c: return f'd{d}={bd[d]}'
    if bd.get(6, 0) != 1: return f'd6={bd.get(6)}'
    return None

start = [(5, 2, 2, 2), (2, 1, 1, 1), (1, 0, 0, 0)]
best_total = 717
best = tuple(tuple(x) for x in start)
cur = best
seen = set()
LOG = '/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/deep717.jsonl'

for step in range(60):
    cands = []
    for bi in range(3):
        for comp in range(4):
            for d in range(-4, 5):
                if d == 0: continue
                ns = [list(x) for x in cur]
                ns[bi][comp] += d
                cands.append(tuple(tuple(ss.gcd_reduce(x)) for x in ns))
    # 2-component moves within each block
    for bi in range(3):
        for c1, c2 in itertools.combinations(range(4), 2):
            for d1 in (-2, -1, 1, 2):
                for d2 in (-2, -1, 1, 2):
                    ns = [list(x) for x in cur]
                    ns[bi][c1] += d1; ns[bi][c2] += d2
                    cands.append(tuple(tuple(ss.gcd_reduce(x)) for x in ns))
    uniq = []
    for c in cands:
        if c in seen: continue
        seen.add(c); uniq.append(c)
    cfgs, metas = [], []
    for c in uniq:
        cfg = build(c)
        if cfg is not None:
            cfgs.append(cfg); metas.append(c)
    if not cfgs:
        break
    res = ss.cpp_batch(cfgs, workers=4)
    step_best = None
    for meta, cfg, r in zip(metas, cfgs, res):
        if r is None: continue
        total, bd = r
        with open(LOG, 'a') as f:
            f.write(json.dumps({'seeds': [list(x) for x in meta], 'total': total,
                                'by_depth': bd, 'quats': cfg}) + '\n')
        v = viol(bd)
        if v and total > 0:
            print('VIOLATION', total, v, meta, flush=True)
        if total > 717:
            print('BEAT717', total, meta, bd, flush=True)
        if step_best is None or total > step_best[1]:
            step_best = (meta, total)
    if step_best and step_best[1] > best_total:
        best_total = step_best[1]; best = step_best[0]; cur = step_best[0]
        print(f'step {step}: improved to {best_total} at {best}', flush=True)
    else:
        print(f'step {step}: local max, best={best_total} at {best}', flush=True)
        break

print('DEEP717 DONE best', best_total, best, flush=True)
