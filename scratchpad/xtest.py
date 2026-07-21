from fractions import Fraction as Fr
from itertools import product

def fsign(x):
    if hasattr(x, 'sign'):
        return x.sign()
    return (x > 0) - (x < 0)

def cube_edges(one, zero):
    edges = []
    for a in range(3):
        o = [i for i in range(3) if i != a]
        for s1, s2 in product((-1, 1), repeat=2):
            c = [zero, zero, zero]
            c[o[0]] = one if s1 == 1 else -one
            c[o[1]] = one if s2 == 1 else -one
            d = [zero, zero, zero]
            d[a] = one
            edges.append((tuple(c), tuple(d), a))  # a = edge class (free axis)
    return edges

def mat_vec(M, v, zero):
    out = []
    for i in range(3):
        s = zero
        for k in range(3):
            s = s + M[i][k] * v[k]
        out.append(s)
    return tuple(out)

def cross(u, v):
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])

def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]

def sub(u, v):
    return (u[0]-v[0], u[1]-v[1], u[2]-v[2])

def pair_census(Mi, Mj, edges, zero):
    """Exact classification of all edge-edge coincidences between cube i, j.
    Returns dict: interior=[(ei,ej,class_i,class_j)], corner=[(ei,ej,class_i,class_j,point)]"""
    ei_t = [(mat_vec(Mi, c, zero), mat_vec(Mi, d, zero), a) for c, d, a in edges]
    ej_t = [(mat_vec(Mj, c, zero), mat_vec(Mj, d, zero), a) for c, d, a in edges]
    interior = []
    corner = []
    for ii, (C1, D1, ca) in enumerate(ei_t):
        for jj, (C2, D2, cb) in enumerate(ej_t):
            n = cross(D1, D2)
            if all(fsign(x) == 0 for x in n):
                continue
            w = sub(C2, C1)
            if fsign(dot(w, n)) != 0:
                continue
            idx = next(k for k in range(3) if fsign(n[k]) != 0)
            rows = [k for k in range(3) if k != idx]
            r0, r1 = rows
            a11, a12 = D1[r0], -D2[r0]
            a21, a22 = D1[r1], -D2[r1]
            b1, b2 = w[r0], w[r1]
            det = a11*a22 - a12*a21
            assert fsign(det) != 0
            t = (b1*a22 - a12*b2) / det
            s = (a11*b2 - b1*a21) / det
            # sanity
            assert fsign(t*D1[idx] - s*D2[idx] - w[idx]) == 0
            st_lo, st_hi = fsign(t+1), fsign(t-1)
            ss_lo, ss_hi = fsign(s+1), fsign(s-1)
            if not (st_lo >= 0 and st_hi <= 0 and ss_lo >= 0 and ss_hi <= 0):
                continue  # crossing outside both segments
            if st_lo > 0 and st_hi < 0 and ss_lo > 0 and ss_hi < 0:
                interior.append((ii, jj, ca, cb))
            else:
                P = tuple(C1[k] + t*D1[k] for k in range(3))
                corner.append((ii, jj, ca, cb, P))
    return interior, corner

if __name__ == '__main__':
    # self-test on rational matrices: identity pair should give 0
    ZERO_F, ONE_F = Fr(0), Fr(1)
    E = cube_edges(ONE_F, ZERO_F)
    IDENT = [[Fr(1) if i==j else Fr(0) for j in range(3)] for i in range(3)]
    inter, corn = pair_census(IDENT, IDENT, E, ZERO_F)
    print('identity pair interior', len(inter), 'corner', len(corn))
