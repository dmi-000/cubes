#!/usr/bin/env python3
"""Do shells avoid symmetric configurations?

Postscript 121: every cube here is centrally symmetric and concentric, so the
antipodal map permutes bounded regions as an involution and
count == #{self-antipodal regions} (mod 2).  The innermost region is always
self-antipodal, so an EVEN count means a second one exists -- a SHELL, a region
wrapping the origin without containing it.

Shells are rare and unevenly distributed, and the distribution is the puzzle:

    octahedral 67 (symmetry order 24):    0 even faces of  728
    golden     67 (symmetry order  6):  148 even faces of 2196
    all-members census:                    6 even counts of  826

CONJECTURE: high symmetry forbids shells.  Tested here by computing the exact
rotational symmetry order of every configuration and correlating it with parity.

SYMMETRY, EXACTLY.  A symmetry is a rotation g with {g R_i} = {R_j} as a set of
cubes, each cube being defined only up to its own 24 rotations.  Since g must
carry cube 0 to some cube j, g = R_j P R_0^-1 for one of the 24 signed
permutations P -- so the candidates are a finite list of n*24, each checked
exactly over Fractions.  No sampling, no tolerance.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from base_points import mat

def signed_perms():
    """the 24 rotation matrices of the cube: signed permutations with det +1"""
    out=[]
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1,-1),repeat=3):
            M=[[0]*3 for _ in range(3)]
            for i in range(3): M[i][p[i]]=s[i]
            det=(M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                 -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                 +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
            if det==1: out.append([[F(x) for x in r] for r in M])
    return out

OCT=signed_perms()

def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def tr(A): return [[A[j][i] for j in range(3)] for i in range(3)]

def canon(R):
    """canonical form of a cube's rotation: smallest representative of R*OCT"""
    return min(tuple(x for row in mul(R,P) for x in row) for P in OCT)

def symmetry_order(quats):
    Rs=[mat(q) for q in quats]
    keys=sorted(canon(R) for R in Rs)
    # COUNT DISTINCT ROTATIONS, not candidate (j,P) pairs.  Two cubes equal up to
    # octahedral symmetry yield the same g from different j, and counting pairs
    # then double-counts: two identical cubes gave 48 where the answer is 24.
    R0inv=tr(Rs[0]); found=set()
    for j in range(len(Rs)):
        for P in OCT:
            g=mul(mul(Rs[j],P),R0inv)
            if sorted(canon(mul(g,R)) for R in Rs)==keys:
                found.add(tuple(x for row in g for x in row))
    return len(found)

def count(cfg):
    s=';'.join(','.join(map(str,q)) for q in cfg)
    m=max(abs(v) for q in cfg for v in q)
    cmd=([HERE+'/cube_regions_n','--quats',s] if m<=512
         else [HERE+'/cube_regions_q2w','--d','0','--quats',s])
    try: return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout.strip().splitlines()[-1])['bounded']
    except Exception: return None

if __name__=='__main__':
    BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    R={6:BASE+[(7,14,1,-5)]}
    R[7]=R[6]+[(4,-3,-4,-4)]; R[8]=R[7]+[(24,-24,24,-61)]; R[9]=R[8]+[(56,56,55,56)]
    rs=json.load(open(os.path.join(HERE,'members_all.json')))
    ev=[r for r in rs if r['count']%2==0]
    print('EVEN-count configurations (a shell exists), %d of %d:'%(len(ev),len(rs)),flush=True)
    for r in ev:
        cfg=[R[r['n']][i] for i in r['idxs']]
        print('   n=%d k=%d count=%-4d symmetry order %d'
              %(r['n'],r['k'],r['count'],symmetry_order(cfg)),flush=True)
    print('\nODD-count sample of the same shapes (no shell):',flush=True)
    shapes={(r['n'],r['k']) for r in ev}
    seen=0
    for r in rs:
        if r['count']%2==1 and (r['n'],r['k']) in shapes and seen<10:
            cfg=[R[r['n']][i] for i in r['idxs']]
            print('   n=%d k=%d count=%-4d symmetry order %d'
                  %(r['n'],r['k'],r['count'],symmetry_order(cfg)),flush=True)
            seen+=1
