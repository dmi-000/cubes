#!/usr/bin/env python3
"""Cross-check: golden four-cube compound (177) via certify_six.exact_count_config,
built directly from the golden axes (no quaternion round-trip needed since the
compound lives in Q(sqrt5), degree 2, while the quaternion double cover of the
full <O,I> group needs Q(sqrt2,sqrt5), degree 4 -- see golden_rotations.py docstring).
We instead build each cube's rotation matrix directly: columns = the cube's own
three orthogonal unit axes (a valid rotation up to a possible reflection, which
we fix by forcing det=+1)."""
import sys
sys.path.insert(0, '/Users/dmi/carroll')
from cube_compound_exact import build_axes, find_cubes, ONE, ZERO, Q5
from certify_six import exact_count_config

axes = build_axes()
triples = find_cubes(axes)
print("triples (axis indices):", triples)

class FakeRot:
    __slots__ = ('m',)
    def __init__(self, m):
        self.m = m

def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))

def is_orthonormal(m):
    for i in range(3):
        for j in range(3):
            s = Q5(0)
            for k in range(3):
                s = s + m[k][i]*m[k][j]
            target = ONE if i == j else Q5(0)
            if (s - target).sign() != 0:
                return False
    return True

rots = []
for t in triples[:4]:
    cols = [axes[i] for i in t]  # each axes[i] is (x,y,z) in Q5
    # matrix with these as COLUMNS j=0,1,2 ; m[i][j] = cols[j][i]
    m = [[cols[j][i] for j in range(3)] for i in range(3)]
    d = det3(m)
    if d.sign() < 0:
        # flip one column to fix handedness (swap two axes) -- keep same cube
        cols = [cols[0], cols[2], cols[1]]
        m = [[cols[j][i] for j in range(3)] for i in range(3)]
        d = det3(m)
    assert d.sign() > 0, f"det sign {d.sign()}"
    assert is_orthonormal(m), "not orthonormal"
    rots.append(FakeRot(m))
    print("cube axes idx", t, "det", d, "OK")

total, by_depth = exact_count_config(rots, verbose=True)
print("TOTAL:", total, "by_depth:", dict(sorted(by_depth.items())))
