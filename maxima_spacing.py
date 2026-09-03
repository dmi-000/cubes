#!/usr/bin/env python3
"""How far apart are local maxima, in units of the thing a walk actually crosses?

The question decides whether annealing can work at all. A bounded number of downhill
steps can only reach another local maximum if the two are a few WALLS apart; if they are
thousands of chambers apart, no step budget bridges them and the only way between them is
a jump -- which is what a random restart already is.

Distance is taken in the space itself, not in a chart of it, and quotiented by everything
the configuration is defined up to:
  * the GAUGE -- both configurations are moved so cube 0 is the identity;
  * each cube's OCTAHEDRAL symmetry -- a cube is invariant under 24 rotations, so the
    per-cube distance is the minimum over that orbit;
  * the global residual rotation left after gauging, which is cube 0's own 24-element
    symmetry;
  * the ORDER of the cubes -- a compound is a set, so the free cubes are matched by the
    permutation minimising the distance.
The result is the largest per-cube rotation angle under the best matching, in degrees.

The unit to compare against is the CHAMBER: the facet censuses report the distance from a
configuration to its nearest wall. Their ratio is the number of walls between maxima.
"""
import json, glob, itertools, math, sys, re
from math import gcd

def qmul(p, r):
    w, x, y, z = p; e, f, g, h = r
    return (w*e - x*f - y*g - z*h, w*f + x*e + y*h - z*g,
            w*g - x*h + y*e + z*f, w*h + x*g - y*f + z*e)

def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])

def canon(t):
    g = 0
    for v in t:
        g = gcd(g, abs(int(v)))
    t = tuple(int(v) // (g or 1) for v in t)
    for v in t:
        if v > 0: break
        if v < 0: t = tuple(-x for x in t); break
    return t

OCT = sorted({canon(t) for t in itertools.product((-1, 0, 1), repeat=4)
              if any(t) and sum(v * v for v in t) in (1, 2, 4)})

def angle(p, q):
    """geodesic angle in SO(3) between two rotations, minimised over cube symmetry"""
    best = math.pi
    np_ = math.sqrt(sum(v * v for v in p))
    for s in OCT:
        r = qmul(q, s)
        nr = math.sqrt(sum(v * v for v in r))
        c = abs(sum(a * b for a, b in zip(p, r))) / (np_ * nr)
        best = min(best, 2 * math.acos(min(1.0, c)))
    return best

def gauge(cfg):
    g = qconj(cfg[0])
    return [canon(qmul(g, q)) for q in cfg]

def dist(A, B):
    A, B = gauge(A), gauge(B)
    free_a, free_b = A[1:], B[1:]
    best = math.pi
    for s in OCT:                              # cube 0's residual symmetry
        Bs = [canon(qmul(q, s)) for q in free_b]
        for perm in itertools.permutations(range(len(Bs))):
            d = max(angle(free_a[i], Bs[perm[i]]) for i in range(len(Bs)))
            best = min(best, d)
    return math.degrees(best)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    seen, cfgs = set(), []
    for f in glob.glob('basin_n*_d*_s*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            if len(d['cfg0']) != n:
                continue
            c = d.get('end') if d.get('end') is not None else d.get('best_evaluable')
            key = tuple(map(tuple, d['cfg1']))
            if c is None or key in seen:
                continue
            seen.add(key); cfgs.append((c, [tuple(q) for q in d['cfg1']]))
    print('n=%d: %d distinct local maxima from the basin campaign' % (n, len(cfgs)), flush=True)
    ds = []
    for i in range(len(cfgs)):
        for j in range(i + 1, len(cfgs)):
            ds.append((dist(cfgs[i][1], cfgs[j][1]), cfgs[i][0], cfgs[j][0]))
    ds.sort()
    print('pairwise separation, degrees (max per-cube rotation angle, best matching):')
    print('   min %.2f   1st pct %.2f   median %.2f   max %.2f'
          % (ds[0][0], ds[len(ds)//100][0], ds[len(ds)//2][0], ds[-1][0]))
    print('   closest pairs: %s' % [('%.2f' % d, a, b) for d, a, b in ds[:5]])
    near = [d for d, _, _ in ds if d < 1.0]
    print('   pairs closer than 1 degree: %d of %d' % (len(near), len(ds)))
    # the unit: distance to the nearest wall, from the facet censuses
    walls = []
    for f in glob.glob('basin_n*.log') + ['climb.log', 'n9_new_climb.log']:
        try:
            for l in open(f):
                m = re.search(r'at\s+([0-9.e-]+)\s+count outside', l)
                if m:
                    walls.append(float(m.group(1)))
        except IOError:
            pass
    if walls:
        walls.sort()
        med = walls[len(walls)//2]
        print('\nchamber scale from %d facet distances: min %.3g median %.3g max %.3g'
              % (len(walls), walls[0], med, walls[-1]))
        print('   (Cayley units; a degree of rotation is ~%.4f in Cayley near the identity)'
              % math.tan(math.radians(0.5)))
        step = math.tan(math.radians(0.5))
        print('   median separation %.2f deg -> ~%.3g Cayley -> ~%.0f walls apart'
              % (ds[len(ds)//2][0], ds[len(ds)//2][0] * step, ds[len(ds)//2][0] * step / med))
