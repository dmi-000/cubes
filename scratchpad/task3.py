import sys, random, time
sys.path.insert(0, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad')
from harness import run_batch

full = [
    [4,1,1,-1],
    [3,3,7,3],
    [5,-1,-5,-5],
    [2,1,1,1],
    [1,1,1,1],
    [7,14,1,-5],
    [4,-3,-4,-4],
    [24,-24,24,-61],
]

random.seed(7)

def build(target_idx, n_candidates, tag):
    others = [row for i,row in enumerate(full) if i != target_idx]
    def make(w,x,y,z):
        cubes = others[:]
        cubes.insert(target_idx, [w,x,y,z])
        return ';'.join(','.join(str(v) for v in row) for row in cubes)

    configs = []
    metas = []
    seen = set()
    def add(w,x,y,z):
        if (w,x,y,z)==(0,0,0,0):
            return
        key=(w,x,y,z)
        if key in seen:
            return
        seen.add(key)
        configs.append(make(w,x,y,z))
        metas.append(key)

    # small exhaustive R=3 -> 7^4=2401
    R=3
    for w in range(-R,R+1):
        for x in range(-R,R+1):
            for y in range(-R,R+1):
                for z in range(-R,R+1):
                    add(w,x,y,z)

    # random at several heights to fill up to n_candidates
    heights = [16, 40, 100, 250, 512]
    hi = 0
    while len(configs) < n_candidates:
        h = heights[hi % len(heights)]
        hi += 1
        w = random.randint(-h,h); x = random.randint(-h,h)
        y = random.randint(-h,h); z = random.randint(-h,h)
        add(w,x,y,z)
        if hi > n_candidates * 5:
            break

    print(f'[{tag}] total configs: {len(configs)}', file=sys.stderr)
    t0=time.time()
    results, elapsed = run_batch(configs, workers=8, tag=tag)
    print(f'[{tag}] run_batch elapsed: {elapsed:.1f}s wall for {len(configs)} configs', file=sys.stderr)

    scored = []
    none_count = 0
    for meta, (b, obj) in zip(metas, results):
        if b is None:
            none_count += 1
            continue
        scored.append((b, meta, obj))
    scored.sort(key=lambda t: -t[0])
    print(f'[{tag}] none/error count: {none_count}', file=sys.stderr)
    seen_counts = []
    for b, meta, obj in scored:
        if b not in seen_counts:
            seen_counts.append(b)
        if len(seen_counts) > 10:
            break
    print(f'[{tag}] TOP 10 distinct counts: {seen_counts}', file=sys.stderr)
    for b, meta, obj in scored[:10]:
        print(f'  [{tag}] bounded={b} quats={obj.get("quats")}', file=sys.stderr)
    above = [t for t in scored if t[0] > 1895]
    print(f'[{tag}] Configs strictly above 1895: {len(above)}', file=sys.stderr)
    for b, meta, obj in above:
        print(f'  [{tag}] ABOVE bounded={b} quats={obj.get("quats")}', file=sys.stderr)

    with open(f'/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad/{tag}_summary.txt','w') as f:
        f.write(f'total={len(configs)} none={none_count}\n')
        f.write(f'top10_counts={seen_counts}\n')
        for b, meta, obj in scored[:20]:
            f.write(f'TOP {b} {obj.get("quats")}\n')
        for b, meta, obj in above:
            f.write(f'ABOVE1895 {b} {obj.get("quats")}\n')
    return scored, above

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    if which in ('7th','both'):
        build(6, 3000, 'task3_7th')  # index 6 = 7th cube (4,-3,-4,-4)
    if which in ('6th','both'):
        build(5, 3000, 'task3_6th')  # index 5 = 6th cube (7,14,1,-5)
