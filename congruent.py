#!/usr/bin/env python3
"""Are two compounds the SAME, up to a global rotation and each cube's own symmetry?

Not an invariant -- a constructive test, which is the difference between "these agree on
everything I thought to measure" and "here is the rotation carrying one to the other".

Two configurations A, B are congruent iff there is a unit quaternion g and a bijection pi
with  b_pi(i) = g * a_i * s_i  for octahedral s_i, since a cube is unchanged by its own 24
rotations. The naive search over pi and the s_i is n! * 24^n. It is not needed: whatever g
is, it must send cube 0 of A to SOME cube of B, so

    g = b_j * s^-1 * a_0^-1        for one of n choices of j and 24 of s

leaving only 24n candidates for g. Each is then checked by asking whether {g*a_i} and {b_k}
agree as SETS OF CUBES -- octahedral class by octahedral class, exactly, in integers.

Written 2026-09-07 after the six "top" n=5 bases in `n5family_keep.json` turned out to be
six spellings of ONE compound: a sweep extending all six would have done 6x the work for
one answer. The 76 kept bases are 11 compounds.
"""
import itertools, sys
sys.path.insert(0, '.')
from symmetrize import canon

def qmul(p, r):
    w,x,y,z = p; e,f,g,h = r
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)

def qconj(p):
    return (p[0], -p[1], -p[2], -p[3])

OCT = sorted({canon(t) for t in itertools.product((-1,0,1), repeat=4)
              if any(t) and sum(v*v for v in t) in (1,2,4)})

def cube_key(q):
    """the octahedral class of a cube: q and q*s are two names for the SAME cube"""
    return min(canon(qmul(q, s)) for s in OCT)

def congruent(A, B):
    """exact; returns the witnessing rotation g, or None"""
    if len(A) != len(B):
        return None
    tb = sorted(cube_key(b) for b in B)
    a0i = qconj(A[0])
    for b in B:
        for s in OCT:
            g = qmul(qmul(b, qconj(s)), a0i)
            if not any(g):
                continue
            if sorted(cube_key(qmul(g, a)) for a in A) == tb:
                return canon(g)
    return None

def classes(cfgs):
    """partition a list of configurations into congruence classes; returns list of index lists"""
    out = []
    for i, c in enumerate(cfgs):
        for grp in out:
            if congruent(cfgs[grp[0]], c) is not None:
                grp.append(i); break
        else:
            out.append([i])
    return out

if __name__ == '__main__':
    import json
    # GATE: a compound is congruent to itself, and to any respelling of itself; and the
    # tower's 393 must be congruent to the family's 393 (they were found by different
    # routes and count the same). A test that cannot fail is not a test, so a KNOWN
    # NON-congruent pair is checked too.
    TOWER = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    resp = [canon(qmul(q, OCT[i % len(OCT)])) for i, q in enumerate(TOWER)]
    assert congruent(TOWER, TOWER), 'GATE: not congruent to itself'
    assert congruent(TOWER, resp), 'GATE: not congruent to a respelling'
    n4 = TOWER[:4]
    assert congruent(TOWER, n4) is None, 'GATE: sizes differ, must not match'
    assert congruent(TOWER, [(1,0,0,0)]*5) is None, 'GATE: five identical cubes must not match'
    print('gates pass: self, respelling, and two negatives', flush=True)

    b = sorted(json.load(open('n5family_keep.json')), key=lambda kv: -kv[0])
    cfgs = [[tuple(q) for q in cf] for _, cf in b]
    cls = classes(cfgs)
    print('%d kept bases -> %d congruence classes' % (len(cfgs), len(cls)))
    reps = []
    for grp in cls:
        best = max(b[i][0] for i in grp)
        reps.append((best, cfgs[grp[0]], len(grp)))
    reps.sort(key=lambda t: -t[0])
    for c5, cf, m in reps:
        print('  n=5 %3d  x%-2d  %s' % (c5, m, ';'.join(','.join(map(str,q)) for q in cf)))
    print()
    print('the tower 393 is congruent to the family 393:',
          congruent(TOWER, reps[0][1]) is not None)
    json.dump([[c5, [list(q) for q in cf]] for c5, cf, _ in reps], open('n5family_classes.json','w'))
    print('wrote n5family_classes.json (%d representatives)' % len(reps))
