#!/usr/bin/env python3
"""A move that carries a Haar-random start ONTO the structured set, exactly.

Attempt 5 in EXPLORATION_141.md. Attempt 3 broke the 141 plateau by drawing starts from
the shared-axis ensemble, but that ensemble is Haar-null, so it answered a different
question than the one asked: it showed the target sits on a structured set, not that
random starts can reach it.

This closes the gap. Given a configuration and an axis u, each cube has a nearest rotation
about u, and it is computable in closed form with no search and no floating point. For a
unit quaternion q = (w, v), the rotations about u are (c, s*u_hat); the inner product
w*c + s*(v.u_hat) is maximised over c^2+s^2=1 at (c,s) proportional to (w, v.u_hat), so
the nearest is

    q' = ( w*(u.u),  (v.u)*u_x,  (v.u)*u_y,  (v.u)*u_z )

which is an INTEGER quaternion whenever q and u are, needing only a gcd. Geometrically it
deletes the component of the rotation axis perpendicular to u.

So a climber from a Haar-random start can take this as one move among others: project onto
each candidate axis, count, keep the best. It is a big jump rather than a local step, but
it is computed from the start configuration and reads nothing -- which is exactly what the
question asks for. If a random start plus this move passes 141, random starts are not
excluded; the old move set was.
"""
import itertools, json, random, subprocess, sys
from math import gcd
sys.path.insert(0, '.')
from haarsample import haar_config

def canon(t):
    g = 0
    for v in t:
        g = gcd(g, abs(int(v)))
    t = tuple(int(v) // (g or 1) for v in t)
    for v in t:
        if v > 0: break
        if v < 0: t = tuple(-x for x in t); break
    return t

def project(q, u):
    """the rotation about axis u nearest to q -- closed form, exact, no search"""
    w, x, y, z = q
    uu = sum(c * c for c in u)
    vu = x * u[0] + y * u[1] + z * u[2]
    return canon((w * uu, vu * u[0], vu * u[1], vu * u[2]))

def axes(bound=3):
    out = []
    for t in itertools.product(range(-bound, bound + 1), repeat=3):
        if any(t):
            a = canon(t)
            if a not in out:
                out.append(a)
    return out

def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                       capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try:
            d = json.loads(l)
            out.append((d['bounded'], int(d['by_depth'].get('1', 0))))
        except Exception:
            out.append((None, None))
    return out + [(None, None)] * (len(cfgs) - len(out))

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    AX = axes(3)
    rng = random.Random(777)
    print('%d Haar starts, each projected onto %d axes  (plateau 141, record 183)'
          % (K, len(AX)), flush=True)
    best = (0, 0, None, None)
    for i in range(K):
        cfg = haar_config(rng, n, 128, chart=True)
        base = batch([cfg])[0]
        cands = [[project(q, u) for q in cfg] for u in AX]
        res = batch(cands)
        ok = [(c, d1, u, cf) for (c, d1), u, cf in zip(res, AX, cands) if c]
        if not ok:
            continue
        top = max(ok)
        if top[0] > best[0]:
            best = top
        print('  start %2d: Haar total %s -> best projection %4d (depth-1 %3d) on axis %s'
              % (i, base[0], top[0], top[1], str(top[2])), flush=True)
    print('\nBEST from a Haar start via one projection: total %d, depth-1 %d, axis %s'
          % (best[0], best[1], best[2]), flush=True)
    if best[3]:
        print(';'.join(','.join(map(str, q)) for q in best[3]), flush=True)
