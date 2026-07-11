import sys; sys.path.insert(0,"/Users/dmi/carroll")
import time
from cube_compound_exact import build_axes, find_cubes
from golden_rotations import Rot, rot_from_quat
from certify_six import exact_count_config
axes=build_axes(); triples=find_cubes(axes)
g5=[Rot([[axes[t[j]][i] for j in range(3)] for i in range(3)]) for t in triples]
GT=[g5[1],g5[3],g5[4]]
def ev(R):
    Rm=rot_from_quat(*R); six=GT+[Rm*c for c in GT]
    t0=time.time(); tot,bd=exact_count_config(six,verbose=False)
    return tot,{int(k):v for k,v in bd.items()},time.time()-t0
for R in [(1,0,0,0),(2,1,1,1),(3,1,1,1),(2,1,0,0),(5,1,2,3)]:
    tot,bd,dt=ev(R); print(f"R={R}: total={tot} bd={bd} ({dt:.1f}s)",flush=True)
