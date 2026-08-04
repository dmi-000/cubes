#!/usr/bin/env python3
"""The epsilon-neighbourhood of a chamber, in the full 3 degrees of freedom.

The chamber WORD of a line (word_typology.py) is a 1-dimensional shadow: it
records what is to the left and right along the line and nothing else. But a
wall line is the intersection of TWO walls, so in configuration space the
neighbourhood of a point on it is cut by both, into

    the line itself            (on both walls)
    4 wall-face sectors        (on one wall, off the other, two signs each)
    4 open quadrants           (off both walls)

Nine local cells. This computes the count and the canonical type in each, and
asks what that adds over the pointwise type.

THE TEST THAT MOTIVATES IT: line 9's word contains the letter 1 twice. As a
pointwise invariant the two occurrences are identical. If their neighbourhoods
differ, then a letter is not a well-defined object without its surroundings,
and a typology of chambers must carry the neighbourhood.

CONSTRUCTION. With n1, n2 the two defining plane normals, the reciprocal
vectors u1, u2 satisfy n_i . u_j = delta_ij, so moving by s1*u1 + s2*u2 crosses
wall 1 iff s1 != 0 and wall 2 iff s2 != 0 -- the sign pair (s1, s2) names the
cell directly, with no numerical guessing about which side we landed on.

INVARIANT: exact rational arithmetic, and epsilon is CHECKED not assumed --
the same signature must come back at two different epsilons, or the sample has
left the chamber and is reporting a neighbour's neighbourhood instead.
"""
import collections
import json
import subprocess
import sys
from fractions import Fraction as F

from continua import FIVE, FIXED_W, to_quat

FIXED_N = ';'.join(','.join(map(str, q)) for q in FIVE)


def perm_mask(m, k):
    out = m & ~0b111
    for s in range(3):
        if m >> s & 1:
            out |= 1 << ((s + k) % 3)
    return out


def canon(pl):
    forms = []
    for k in range(3):
        d = collections.defaultdict(int)
        for mask, v in pl.items():
            d[perm_mask(int(mask), k)] += v
        forms.append(json.dumps(sorted(d.items())))
    return min(forms)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(a[i]*b[i] for i in range(3))


def reciprocal(n1, n2):
    """u1, u2 with n_i . u_j = delta_ij, both orthogonal to nothing in
    particular -- they need only span a complement of the line direction."""
    d = cross(n1, n2)
    det = dot(n1, cross(n2, d))
    u1 = tuple(F(x, 1)/det for x in cross(n2, d))
    det2 = dot(n2, cross(d, n1))
    u2 = tuple(F(x, 1)/det2 for x in cross(d, n1))
    return u1, u2


def batch(quats):
    inp = '\n'.join(FIXED_W + ';' + ','.join('%d:0' % v for v in q)
                    for q in quats) + '\n'
    out = subprocess.run(['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
                         input=inp, capture_output=True, text=True).stdout
    rows = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
    assert len(rows) == len(quats), (len(rows), len(quats))
    return rows


def neighbourhood(pt, u1, u2, eps):
    """9 cells: (s1, s2) in {-1,0,1}^2 scaled by eps."""
    cells, keys = [], []
    for s1 in (0, -1, 1):
        for s2 in (0, -1, 1):
            v = tuple(pt[i] + eps*(s1*u1[i] + s2*u2[i]) for i in range(3))
            q = to_quat(v, cap=10**9)
            keys.append((s1, s2))
            cells.append(q)
    live = [(k, q) for k, q in zip(keys, cells) if q]
    rows = batch([q for _, q in live]) if live else []
    out = {}
    for (k, _), d in zip(live, rows):
        tot = d.get('bounded')
        out[k] = (tot, canon(d['per_label']) if tot else None)
    for k, q in zip(keys, cells):
        if q is None:
            out[k] = (None, None)
    return out


def main():
    li = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    lo = F(sys.argv[2]) if len(sys.argv) > 2 else F(2)
    hi = F(sys.argv[3]) if len(sys.argv) > 3 else F(27, 2)
    step = F(1, 8)
    data = json.load(open('typology_data.json'))
    L = data['lines'][li]
    p0 = tuple(F(x) for x in L['p0'])
    dd = tuple(F(x) for x in L['dir'])
    n1 = tuple(F(x) for x in L['planeA'][:3])
    n2 = tuple(F(x) for x in L['planeB'][:3])
    u1, u2 = reciprocal(n1, n2)
    print('line %d, defining normals %s and %s' % (li, L['planeA'][:3],
                                                   L['planeB'][:3]))

    # chambers by sampling along the line
    ts, qs = [], []
    t = lo
    while t <= hi:
        q = to_quat(tuple(p0[u] + t*dd[u] for u in range(3)), cap=10**9)
        if q:
            ts.append(t)
            qs.append(q)
        t += step
    rows = batch(qs)
    seq = [(t, d.get('bounded'), canon(d['per_label']) if d.get('bounded') else None)
           for t, d in zip(ts, rows)]
    reps, cur = [], None
    for t, c, ty in seq:
        if cur is None or cur[0] != (c, ty):
            cur = [(c, ty), t, t]
            reps.append(cur)
        else:
            cur[2] = t
    print('chambers along the line at step 1/8: %d\n' % len(reps))

    alpha = {}
    sigs = collections.defaultdict(list)
    for (ct, a, b), idx in zip(reps, range(len(reps))):
        c, ty = ct
        if c != 727:
            continue
        if ty not in alpha:
            alpha[ty] = len(alpha)
        mid = (a + b) / 2
        pt = tuple(p0[u] + mid*dd[u] for u in range(3))
        sig = {}
        stable = True
        for eps in (F(1, 64), F(1, 256)):
            nb = neighbourhood(pt, u1, u2, eps)
            s = tuple(nb[k][0] for k in sorted(nb))
            if not sig:
                sig = s
            elif sig != s:
                stable = False
        sigs[alpha[ty]].append((str(mid), sig, stable))
        print('chamber %2d  letter %2d  t=%-10s counts by (s1,s2): %s  %s'
              % (idx, alpha[ty], mid, sig, '' if stable else '(eps-UNSTABLE)'))
    print('\nletters occurring more than once, and whether their'
          ' neighbourhoods agree:')
    for lt, lst in sorted(sigs.items()):
        if len(lst) < 2:
            continue
        same = len({s for _, s, _ in lst}) == 1
        print('   letter %2d  x%d  -> neighbourhoods %s'
              % (lt, len(lst), 'IDENTICAL' if same else 'DIFFER'))
        for m, s, _ in lst:
            print('        t=%-10s %s' % (m, s))


if __name__ == '__main__':
    main()
