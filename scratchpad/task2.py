import sys, random, time, itertools
sys.path.insert(0, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad')
from harness import run_batch

first7 = [
    [4,1,1,-1],
    [3,3,7,3],
    [5,-1,-5,-5],
    [2,1,1,1],
    [1,1,1,1],
    [7,14,1,-5],
    [4,-3,-4,-4],
]
first7_str = ';'.join(','.join(str(x) for x in row) for row in first7)

random.seed(42)

def make(w,x,y,z):
    return first7_str + f';{w},{x},{y},{z}'

configs = []
metas = []
seen = set()

def add(w,x,y,z):
    if (w,x,y,z) == (0,0,0,0):
        return
    key = (w,x,y,z)
    if key in seen:
        return
    seen.add(key)
    configs.append(make(w,x,y,z))
    metas.append(key)

# exhaustive-ish small range |component| <= 4 (9^4=6561; kept small given ~28-30 configs/sec effective throughput)
R = 4
for w in range(-R,R+1):
    for x in range(-R,R+1):
        for y in range(-R,R+1):
            for z in range(-R,R+1):
                add(w,x,y,z)

print(f'after exhaustive R={R}: {len(configs)}', file=sys.stderr)

# random samples at various height scales
heights = [16, 40, 100, 250, 512]
per_height = 800
for h in heights:
    for _ in range(per_height):
        w = random.randint(-h,h)
        x = random.randint(-h,h)
        y = random.randint(-h,h)
        z = random.randint(-h,h)
        add(w,x,y,z)

print(f'total task2 configs: {len(configs)}', file=sys.stderr)

t0=time.time()
results, elapsed = run_batch(configs, workers=8, tag='task2')
print(f'run_batch elapsed: {elapsed:.1f}s wall for {len(configs)} configs', file=sys.stderr)

scored = []
none_count = 0
for meta, (b, obj) in zip(metas, results):
    if b is None:
        none_count += 1
        continue
    scored.append((b, meta, obj))

scored.sort(key=lambda t: -t[0])
print(f'none/error count: {none_count}', file=sys.stderr)
print('TOP 10 distinct counts:', file=sys.stderr)
seen_counts = []
for b, meta, obj in scored:
    if b not in seen_counts:
        seen_counts.append(b)
    if len(seen_counts) > 10:
        break
for c in seen_counts:
    print(f'  count={c}', file=sys.stderr)

print('TOP configs overall (top 10 rows):', file=sys.stderr)
for b, meta, obj in scored[:10]:
    print(f'  bounded={b} quats={obj.get("quats")}', file=sys.stderr)

above = [t for t in scored if t[0] > 1895]
print(f'Configs strictly above 1895: {len(above)}', file=sys.stderr)
for b, meta, obj in above:
    print(f'  ABOVE bounded={b} quats={obj.get("quats")}', file=sys.stderr)

with open('/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad/task2_summary.txt','w') as f:
    f.write(f'total={len(configs)} none={none_count}\n')
    f.write(f'top10_counts={seen_counts}\n')
    for b, meta, obj in scored[:20]:
        f.write(f'TOP {b} {obj.get("quats")}\n')
    for b, meta, obj in above:
        f.write(f'ABOVE1895 {b} {obj.get("quats")}\n')
