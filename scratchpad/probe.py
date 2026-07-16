import math, random
from golden_rotations import Rot, rot_from_quat, closure
from cube_compound_exact import Q5
from itertools import permutations, product

def signed_perm_int_mats():
    mats = []
    for perm in permutations(range(3)):
        for signs in product((1,-1), repeat=3):
            M = [[0]*3 for _ in range(3)]
            for i in range(3):
                M[i][perm[i]] = signs[i]
            det = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                   -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                   +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
            if det == 1:
                mats.append(M)
    return mats
O_INT = signed_perm_int_mats()
def embed_q5(M):
    return Rot([[Q5(x) for x in row] for row in M])
O_Q5 = [embed_q5(M) for M in O_INT]

def coset_key(R, Oset=O_Q5):
    return min((R*o).to_str() for o in Oset)

def orbit_size(Gelems, seed):
    return len({coset_key(g*seed) for g in Gelems})

GROUPS = {
 'C2': [(0,0,0,1)],
 'C3': [(1,1,1,1)],
 'C4': [(1,0,0,1)],
 'C6': [(3,1,1,1)],
 'D2': [(0,0,0,1),(0,1,0,0)],
 'D3': [(1,1,1,1),(0,1,-1,0)],
 'D4': [(1,0,0,1),(0,1,0,0)],
 'D6': [(3,1,1,1),(0,1,-1,0)],
 'T': [(1,1,1,1),(1,1,1,-1)],
 'O': [(1,0,0,1),(1,1,1,1)],
}

def gcd_reduce(ints):
    g = math.gcd(*[abs(x) for x in ints])
    if g>1: ints=[i//g for i in ints]
    if not any(ints): ints=[1,0,0,0]
    return ints

rng = random.Random(42)
seed_forms = {
  'identity': [(1,0,0,0)],
  'z-aligned (a,0,0,d)': [(a,0,0,d) for a,d in [(1,1),(2,1),(1,2),(3,1),(1,3),(5,2),(4,1)]],
  'body-diag (a,b,b,b)': [(a,b,b,b) for a,b in [(1,1),(2,1),(1,2),(3,1),(1,3),(5,2),(4,1)]],
  'face-diag (a,b,-b,0)': [(a,b,-b,0) for a,b in [(1,1),(2,1),(1,2),(3,1),(1,3)]],
  'generic random': [tuple(gcd_reduce([rng.randint(-60,60) for _ in range(4)])) for _ in range(8)],
}

for gname, gens in GROUPS.items():
    Gelems = closure([rot_from_quat(*q) for q in gens])
    print(f'--- G={gname} |G|={len(Gelems)} ---')
    for form, quats in seed_forms.items():
        sizes = set()
        for q in quats:
            s = rot_from_quat(*q)
            sizes.add(orbit_size(Gelems, s))
        print(f'  {form:24s}: orbit sizes seen = {sorted(sizes)}')
