import sys, itertools, time
sys.path.insert(0, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad')
from harness import run_batch

base_cubes = [
    [4,1,1,-1],
    [3,3,7,3],
    [5,-1,-5,-5],
    [2,1,1,1],
    [1,1,1,1],
    [7,14,1,-5],
    [4,-3,-4,-4],
    [24,-24,24,-61],
]

positions = [(c,k) for c in range(8) for k in range(4)]  # 32 positions
deltas = [-3,-2,-1,1,2,3]

def make_config(mods):
    # mods: dict pos-> delta
    cubes = [row[:] for row in base_cubes]
    for (c,k), d in mods.items():
        cubes[c][k] += d
    return ';'.join(','.join(str(x) for x in row) for row in cubes)

configs = []
metas = []

# single-position changes
for pos in positions:
    for d in deltas:
        mods = {pos: d}
        configs.append(make_config(mods))
        metas.append((pos, d))

# two-position changes
pos_pairs = list(itertools.combinations(positions, 2))
for p1, p2 in pos_pairs:
    for d1 in deltas:
        for d2 in deltas:
            mods = {p1: d1, p2: d2}
            configs.append(make_config(mods))
            metas.append(((p1,d1),(p2,d2)))

print(f'Total task1 configs: {len(configs)}', file=sys.stderr)

t0 = time.time()
results, elapsed = run_batch(configs, workers=8, tag='task1')
print(f'run_batch elapsed: {elapsed:.1f}s wall for {len(configs)} configs', file=sys.stderr)

best = -1
best_list = []
above = []
none_count = 0
for meta, (b, obj) in zip(metas, results):
    if b is None:
        none_count += 1
        continue
    if b > best:
        best = b
        best_list = [(meta, b, obj)]
    elif b == best:
        best_list.append((meta, b, obj))
    if b > 1895:
        above.append((meta, b, obj))

print(f'none/error count: {none_count}', file=sys.stderr)
print(f'BEST bounded = {best}', file=sys.stderr)
print(f'Number achieving best: {len(best_list)}', file=sys.stderr)
for meta, b, obj in best_list[:5]:
    print('  meta=', meta, 'bounded=', b, 'quats=', obj.get('quats') if isinstance(obj, dict) else obj, file=sys.stderr)

print(f'Configs strictly above 1895: {len(above)}', file=sys.stderr)
for meta, b, obj in above:
    print('  ABOVE meta=', meta, 'bounded=', b, 'quats=', obj.get('quats') if isinstance(obj, dict) else obj, file=sys.stderr)

with open('/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad/task1_summary.txt','w') as f:
    f.write(f'total={len(configs)} best={best} none={none_count}\n')
    for meta, b, obj in best_list:
        f.write(f'BEST {meta} {b} {obj.get("quats")}\n')
    for meta, b, obj in above:
        f.write(f'ABOVE1895 {meta} {b} {obj.get("quats")}\n')
