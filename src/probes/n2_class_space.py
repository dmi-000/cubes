#!/usr/bin/env python3
"""Are the mirror-plane 13s at n = 2 new CLASSES, or members of the two known families?

THE QUESTION.  [P76] found count 13 at isolated angles for rotation axes lying in a mirror plane
of the cube (e.g. axis (1,2,0) at two angles), in addition to the two known one-parameter families:
    B  rotations about a BODY diagonal, any angle except the cube's own symmetries
    E  rotations about an EDGE axis (a face diagonal), with cos(theta) in [-1/3, 1/3]
A pair's class is its relative rotation R up to R ~ g R h, g and h in the cube's 24-element
rotation group O, so an axis is NOT a class invariant.  `shapes.svg` drew n = 2 as "2 arcs +
isolated classes"; LEVELS.md says the mirror-plane 13s "trace further curves".  Neither was checked.

METHOD, exact, no sampling within the box.  Every primitive integer quaternion (w,x,y,z) with
max |component| <= H whose axis (x,y,z) lies in a mirror plane (a coordinate plane: one of x,y,z
zero; or a diagonal plane: two of |x|,|y|,|z| equal), counted exactly by the engine.  For each 13,
all 24 x 24 pairs (g, h) are tried, and g R h is tested exactly (integer matrices) for being in
B or in E.  A 13 in neither is a genuinely new class.

GATES.  Controls that must land where they are known to: members of B at several angles (body
diagonal axes), members of E inside the interval, and the known count-13 rational point
1,0,0,0;2,2,3,0 of [P233].
"""
import sys, os, itertools, json, subprocess, math
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ENGINE = os.path.join(ROOT, 'cube_regions_n')


def mat(q):
    """integer matrix M and scale N with R = M / N (rotation by quaternion q)."""
    w, x, y, z = q
    N = w * w + x * x + y * y + z * z
    M = [[w*w + x*x - y*y - z*z, 2*(x*y - w*z), 2*(x*z + w*y)],
         [2*(x*y + w*z), w*w - x*x + y*y - z*z, 2*(y*z - w*x)],
         [2*(x*z - w*y), 2*(y*z + w*x), w*w - x*x - y*y + z*z]]
    return M, N


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def octahedral():
    """the 24 signed permutation matrices of determinant +1."""
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            P = [[0] * 3 for _ in range(3)]
            for i in range(3):
                P[i][perm[i]] = sg[i]
            det = (P[0][0] * (P[1][1] * P[2][2] - P[1][2] * P[2][1])
                   - P[0][1] * (P[1][0] * P[2][2] - P[1][2] * P[2][0])
                   + P[0][2] * (P[1][0] * P[2][1] - P[1][1] * P[2][0]))
            if det == 1:
                out.append(P)
    assert len(out) == 24
    return out


O = octahedral()


def axis_and_cos(M, N):
    """(axis vector up to scale, cos theta as a Fraction) for R = M/N; axis None for R = I."""
    tr = M[0][0] + M[1][1] + M[2][2]
    c = (F(tr, N) - 1) / 2
    a = (M[2][1] - M[1][2], M[0][2] - M[2][0], M[1][0] - M[0][1])
    if a != (0, 0, 0):
        return a, c
    if c == 1:
        return None, c                                   # the identity
    # half-turn: R + I has rank 1, any nonzero column is the axis
    for j in range(3):
        col = (M[0][j] + (N if j == 0 else 0), M[1][j] + (N if j == 1 else 0), M[2][j] + (N if j == 2 else 0))
        if col != (0, 0, 0):
            return col, c
    return None, c


def is_body(a):
    return a is not None and abs(a[0]) == abs(a[1]) == abs(a[2]) != 0


def is_edge(a):
    if a is None:
        return False
    s = sorted(abs(t) for t in a)
    return s[0] == 0 and s[1] == s[2] != 0


def classify(q):
    """which known family the class of q meets: 'B', 'E', or None."""
    M, N = mat(q)
    hit = set()
    for g in O:
        gM = mul(g, M)
        for h in O:
            X = mul(gM, h)
            a, c = axis_and_cos(X, N)
            if a is None:
                continue
            if is_body(a) and c != 1:
                hit.add('B')
            if is_edge(a) and F(-1, 3) <= c <= F(1, 3):
                hit.add('E')
            if len(hit) == 2:
                return hit
    return hit


def count(q):
    r = subprocess.run([ENGINE, '--quats', '1,0,0,0;%d,%d,%d,%d' % q], capture_output=True, text=True)
    j = json.loads(r.stdout)
    return j.get('bounded')


def in_mirror(q):
    x, y, z = (abs(t) for t in q[1:])
    if (x, y, z) == (0, 0, 0):
        return False
    return x == 0 or y == 0 or z == 0 or x == y or y == z or x == z


def main():
    H = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    ALL = '--all' in sys.argv          # every axis, not only mirror-plane ones: the exhaustive form
    # --- gates -------------------------------------------------------------------------------
    gates = {'B body-diagonal (3,1,1,1)': ((3, 1, 1, 1), 'B'), 'B body-diagonal (1,2,2,2)': ((1, 2, 2, 2), 'B'),
             'E edge axis t=1/2 (2,1,1,0)': ((2, 1, 1, 0), 'E'), 'E edge axis t=1 (1,1,1,0)': ((1, 1, 1, 0), 'E'),
             'P233 point (2,2,3,0)': ((2, 2, 3, 0), None)}
    print('GATES')
    for name, (q, want) in gates.items():
        cl, n = classify(q), count(q)
        ok = (want in cl) if want else True
        print('   %-30s count %-3s classes %-10s %s' % (name, n, sorted(cl), 'PASS' if ok and n == 13 else 'CHECK'))
    # --- the enumeration ---------------------------------------------------------------------
    seen, tot, thirteen, fam = set(), 0, [], {}
    for q in itertools.product(range(-H, H + 1), repeat=4):
        if q[0] < 0 or (q[0] == 0 and q <= tuple(-t for t in q)):
            continue                                        # q and -q are one rotation
        if math.gcd(*q) != 1 or (not ALL and not in_mirror(q)):
            continue
        tot += 1
        if count(q) != 13:
            continue
        cl = classify(q)
        key = ''.join(sorted(cl)) or 'NEW'
        fam.setdefault(key, []).append(q)
        thirteen.append((q, key))
    print('\nheight <= %d: %d primitive %s rotations counted, %d count 13'
          % (H, tot, 'ALL' if ALL else 'mirror-plane', len(thirteen)))
    offm = [q for q, k in thirteen if not in_mirror(q)]
    print('   of the 13s, %d have an axis OFF every mirror plane' % len(offm))
    for k, v in sorted(fam.items()):
        print('   %-4s %4d   e.g. %s' % (k, len(v), v[:6]))
    json.dump({'H': H, 'all_axes': ALL, 'counted': tot, 'thirteen': len(thirteen),
               'by_family': {k: [list(x) for x in v] for k, v in fam.items()}},
              open(os.path.join(ROOT, 'data', 'n2_class_space.json'), 'w'), indent=1)
    print('wrote data/n2_class_space.json')


if __name__ == '__main__':
    main()
