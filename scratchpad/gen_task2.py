import random

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
seen = set()
configs = []

def add(w,x,y,z):
    if (w,x,y,z)==(0,0,0,0):
        return
    key=(w,x,y,z)
    if key in seen:
        return
    seen.add(key)
    configs.append(first7_str + f';{w},{x},{y},{z}')

R = 4
for w in range(-R,R+1):
    for x in range(-R,R+1):
        for y in range(-R,R+1):
            for z in range(-R,R+1):
                add(w,x,y,z)

heights = [16, 40, 100, 250, 512]
per_height = 800
for h in heights:
    for _ in range(per_height):
        w=random.randint(-h,h); x=random.randint(-h,h)
        y=random.randint(-h,h); z=random.randint(-h,h)
        add(w,x,y,z)

with open('/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad/task2_candidates.txt','w') as f:
    for c in configs:
        f.write(c+'\n')
print(len(configs))
