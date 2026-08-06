import random, sys

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

def gen(target_idx, n_target, outpath):
    others = [row for i,row in enumerate(full) if i != target_idx]
    seen=set()
    configs=[]
    def add(w,x,y,z):
        if (w,x,y,z)==(0,0,0,0): return
        key=(w,x,y,z)
        if key in seen: return
        seen.add(key)
        cubes = others[:]
        cubes.insert(target_idx, [w,x,y,z])
        configs.append(';'.join(','.join(str(v) for v in row) for row in cubes))

    R=3
    for w in range(-R,R+1):
        for x in range(-R,R+1):
            for y in range(-R,R+1):
                for z in range(-R,R+1):
                    add(w,x,y,z)

    heights=[16,40,100,250,512]
    hi=0
    while len(configs) < n_target:
        h = heights[hi % len(heights)]
        hi += 1
        w=random.randint(-h,h); x=random.randint(-h,h)
        y=random.randint(-h,h); z=random.randint(-h,h)
        add(w,x,y,z)
        if hi > n_target*5:
            break

    with open(outpath,'w') as f:
        for c in configs:
            f.write(c+'\n')
    print(target_idx, len(configs))

gen(6, 3000, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad/task3_7th_candidates.txt')
gen(5, 3000, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad/task3_6th_candidates.txt')
