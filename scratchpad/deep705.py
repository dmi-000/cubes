import sys, json, itertools
sys.path.insert(0, '/Users/dmi/carroll')
import symmetry_search as ss

C3 = ss.group_quats('C3')

def build(s1, s2):
    cfg = []
    for s in (s1, s2):
        s = tuple(ss.gcd_reduce(list(s)))
        if not ss.cap_ok(s):
            return None
        cfg += ss.quat_orbit(C3, s, ss.O_Q5)
    if len(cfg) != 6:
        return None
    if len({ss.coset_key(ss.rot_from_quat(*q), ss.O_Q5) for q in cfg}) != 6:
        return None
    return cfg

def evalc(cfgs):
    return ss.cpp_batch(cfgs, workers=4)

# deep hill-climb from 705 point, both seeds move, radius up to 4 per step,
# also 2-component simultaneous moves on the S2 seed.
best_total = 705
best = ((3,1,0,0),(21,14,11,7))
cur = best
seen = set()
CEIL={3:164,4:102,5:36}
def viol(bd):
    for d,c in CEIL.items():
        if bd.get(d,0)>c: return f'd{d}={bd[d]}'
    if bd.get(6,0)!=1: return f'd6={bd.get(6)}'
    return None

for step in range(40):
    s1, s2 = cur
    cands = []
    deltas1 = [0]  # keep S1 near canonical; also allow small moves
    moves = list(range(-4,5))
    # single-component moves on both seeds
    for si, seed in enumerate((s1,s2)):
        for comp in range(4):
            for d in moves:
                if d==0: continue
                q=list(seed); q[comp]+=d
                ns=(tuple(ss.gcd_reduce(list(s1))), tuple(ss.gcd_reduce(q))) if si==1 else (tuple(ss.gcd_reduce(q)), tuple(ss.gcd_reduce(list(s2))))
                cands.append(ns)
    # two-component moves on S2
    for c1,c2 in itertools.combinations(range(4),2):
        for d1 in (-2,-1,1,2):
            for d2 in (-2,-1,1,2):
                q=list(s2); q[c1]+=d1; q[c2]+=d2
                cands.append((s1, tuple(ss.gcd_reduce(q))))
    # dedupe & build
    uniq=[]
    for c in cands:
        if c in seen: continue
        seen.add(c)
        uniq.append(c)
    cfgs=[]; metas=[]
    for c in uniq:
        cfg=build(*c)
        if cfg is not None:
            cfgs.append(cfg); metas.append(c)
    if not cfgs:
        break
    res=evalc(cfgs)
    step_best=None
    for meta,cfg,r in zip(metas,cfgs,res):
        if r is None: continue
        total,bd=r
        with open('/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/deep705.jsonl','a') as f:
            f.write(json.dumps({'seeds':[list(meta[0]),list(meta[1])],'total':total,'by_depth':bd,'quats':cfg})+'\n')
        v=viol(bd)
        if v and total>0:
            print('VIOLATION', total, v, meta, flush=True)
        if total>705:
            print('BEAT705', total, meta, bd, flush=True)
        if step_best is None or total>step_best[1]:
            step_best=(meta,total)
    if step_best and step_best[1]>best_total:
        best_total=step_best[1]; best=step_best[0]; cur=step_best[0]
        print(f'step {step}: improved to {best_total} at {best}', flush=True)
    else:
        print(f'step {step}: local max, best={best_total} at {best}', flush=True)
        break

print('DEEP705 DONE best', best_total, best, flush=True)
