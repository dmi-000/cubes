import sys; sys.path.insert(0,"/Users/dmi/carroll")
import time
from cube_compound_exact import build_axes, find_cubes, ONE
from golden_rotations import Rot, rot_from_quat
from certify_six import exact_count_config

axes=build_axes(); triples=find_cubes(axes)
g5=[Rot([[axes[t[j]][i] for j in range(3)] for i in range(3)]) for t in triples]
# golden 3-cycle triple = cubes {1,3,4}
GT=[g5[1],g5[3],g5[4]]

def eval_overlay(Rquat, label=''):
    R=rot_from_quat(*Rquat)
    six=GT+[R*c for c in GT]
    t0=time.time()
    total,bd=exact_count_config(six,verbose=False)
    return total,{int(k):v for k,v in bd.items()},time.time()-t0

# Gate: R=identity -> coincident golden triples -> should be 67
tot,bd,dt=eval_overlay((1,0,0,0))
print(f"GATE R=identity: total={tot} bd={bd} ({dt:.1f}s) [expect 67]")

# various R: diagonal (1,1,1) rotations, face rotations, random small
import itertools
cands=[(1,0,0,0),(2,1,1,1),(3,1,1,1),(5,2,2,2),(1,1,0,0),(2,1,0,0),(3,1,0,0),
       (1,1,1,0),(2,1,1,0),(3,2,1,1),(5,1,2,3),(4,3,2,1),(1,2,3,4),(7,4,4,4),
       (2,1,1,-1),(3,2,2,2),(1,1,2,0)]
best=(0,None,None)
for R in cands:
    tot,bd,dt=eval_overlay(R)
    mark=' <<<' if tot>681 else ''
    print(f"R={R}: total={tot} bd={bd} ({dt:.1f}s){mark}")
    if tot>best[0]: best=(tot,R,bd)
print("BEST golden-overlay:", best)
