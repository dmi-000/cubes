#!/usr/bin/env python3
"""Extents, endpoints, chambers and wrapping for 727 arcs B and C."""
import hashlib, json, math, subprocess
from fractions import Fraction as F
from tangent_finder import counts, BASE5

ARCS = [('B', [F(4,35), F(2,5), F(-41,35)], [F(1), F(1), F(-4)]),
        ('C', [F(245,29), F(-295,29), F(428,29)], [F(1), F(-3,2), F(9,4)])]


def profiles(pts):
    lines = []
    for p in pts:
        den = 1
        for x in p:
            den = den * x.denominator // math.gcd(den, x.denominator)
        q = (den,) + tuple(int(x*den) for x in p)
        lines.append(';'.join(','.join(map(str, c)) for c in BASE5) + ';'
                     + ','.join(map(str, q)))
    out = []
    for i in range(0, len(lines), 2000):
        r = subprocess.run(['./cube_regions_n', '--quats-stdin'],
                           input='\n'.join(lines[i:i+2000])+'\n',
                           capture_output=True, text=True)
        out += [json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')]
    return out


def at(a0, v, s):
    return [a0[i] + s*v[i] for i in range(3)]


def refine(a0, v, lo, hi, target, depth=14):
    """Bisect the transition between lo (target) and hi (not target)."""
    for _ in range(depth):
        mid = (lo + hi) / 2
        c = counts([at(a0, v, mid)], BASE5)[0]
        if c == target:
            lo = mid
        else:
            hi = mid
    return lo, hi


for name, a0, v in ARCS:
    print('=== arc %s : through %s along %s ==='
          % (name, tuple(str(x) for x in a0), tuple(str(x) for x in v)), flush=True)
    ss = [F(n, 16) for n in range(-480, 481)]
    res = [d.get('bounded') for d in profiles([at(a0, v, s) for s in ss])]
    runs = []
    for s, c in zip(ss, res):
        if runs and runs[-1][0] == c:
            runs[-1][2] = s
        else:
            runs.append([c, s, s])
    good = [r for r in runs if r[0] == 727]
    print('  727 on %d run(s) over s in [-30,30] at step 1/16; total %d of %d samples'
          % (len(good), sum(1 for c in res if c == 727), len(res)), flush=True)
    for c, lo, hi in sorted(good, key=lambda r: -(r[2]-r[1]))[:4]:
        print('     [%s, %s]  width %s' % (lo, hi, hi-lo), flush=True)
    if good:
        main = max(good, key=lambda r: r[2]-r[1])
        # endpoints, bisected
        loB = refine(a0, v, main[1], main[1]-F(1,16), 727)
        hiB = refine(a0, v, main[2], main[2]+F(1,16), 727)
        cl = counts([at(a0, v, loB[1])], BASE5)[0]
        ch = counts([at(a0, v, hiB[1])], BASE5)[0]
        print('  endpoints of the widest run, bisected to 2^-14:', flush=True)
        print('     lower  727 down to s=%.9f   then %s' % (float(loB[0]), cl), flush=True)
        print('     upper  727 up   to s=%.9f   then %s' % (float(hiB[0]), ch), flush=True)
        # chambers inside the widest run
        n = 240
        step = (main[2]-main[1]) / n
        pts = [at(a0, v, main[1] + step*k) for k in range(n+1)]
        ds = profiles(pts)
        sigs, prev = [], None
        for k, d in enumerate(ds):
            if d.get('bounded') != 727:
                continue
            h = hashlib.md5(json.dumps(d['per_label'], sort_keys=True).encode()).hexdigest()[:6]
            if h != prev:
                sigs.append((h, main[1] + step*k))
                prev = h
        print('  chambers inside the widest run: %d' % len(sigs), flush=True)
        print('     first walls at s = %s' % ', '.join(str(x[1]) for x in sigs[:6]), flush=True)
    # wrap test
    q = (0,) + tuple(int(x) for x in
                     [v[i]*max(x.denominator for x in v) for i in range(3)])
    line = ';'.join(','.join(map(str, c)) for c in BASE5) + ';' + ','.join(map(str, q))
    r = subprocess.run(['./cube_regions_n', '--quats', line],
                       capture_output=True, text=True)
    inf = json.loads(r.stdout).get('bounded')
    far = counts([at(a0, v, F(1000)), at(a0, v, F(-1000))], BASE5)
    print('  wrap test: s=+1000 -> %s, s=-1000 -> %s, s=INF -> %s%s\n'
          % (far[0], far[1], inf, '   WRAPS' if inf == 727 else '   does not wrap'), flush=True)
