import random
import sys
sys.path.insert(0, '/Users/dmi/carroll')
import symmetry_search as ss

rng = random.Random(123)

def test(gname, n=200, cap=50):
    qlist = ss.group_quats(gname)
    from collections import Counter
    c = Counter()
    for _ in range(n):
        q = tuple(ss.gcd_reduce([rng.randint(-cap, cap) for _ in range(4)]))
        orb = ss.quat_orbit(qlist, q, ss.O_Q5)
        c[len(orb)] += 1
    print(gname, dict(c))

for g in ['D3', 'C2', 'T', 'D2', 'C6']:
    test(g)
