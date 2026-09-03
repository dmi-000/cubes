#!/usr/bin/env python3
"""Climb on a DEPTH LEVEL, and allow the walk to step down — frustration as a method.

The recorded frustration (JOURNEY Act IV): golden compounds hit the top-layer cap exactly
(depth-1 = 10n^2 - 14n, i.e. 48/104/180 at n = 3,4,5) yet total only 177 at n=4, while the
record 183 has "worse" parts. **Nobody gets both.** Summing the per-layer caps bounds the
total well above every record, and that gap is the price of frustration made visible.

Two consequences the existing walk cannot exploit, both suggested by the user:

  1. If the layers fight, maximising the TOTAL is the wrong objective to walk on. Walk on
     a single layer, or a weighted profile, land somewhere a little under max on that
     layer, and then walk on the total from there.
  2. A strictly-improving walk cannot cross a dip. Allowing a bounded number of
     non-improving moves -- an annealing step -- lets it leave a local maximum and reach
     the next wall, while the BEST-EVER configuration is kept separately so a downhill
     excursion can never lose a result.

WALLS ARE STILL DETECTED BY THE COUNT. A wall is where the combinatorics changes, and the
total count is what changes there; an objective that happens to be flat across a wall
would make the walk blind to it. So `climb.first_crossing` finds the crossings exactly as
the record climb does -- this is the same walk, reused, not a second one -- and only the
SELECTION among them uses the objective.

Best-ever is reported separately from where the walk ends, because with annealing on they
are not the same thing and reporting the endpoint would understate the run.
"""
import json, subprocess, sys, random
from fractions import Fraction as F
sys.path.insert(0, '.')
import climb as C
import dimension as D
from basin import rand_dir

def full(cfg):
    """the engine's whole answer: bounded count and the depth profile"""
    st = ';'.join(','.join(map(str, q)) for q in cfg)
    for cmd in (['./cube_regions_n', '--quats', st],
                ['./cube_regions_q2w', '--d', '0', '--quats', st]):
        try:
            d = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
            if 'bounded' in d and 'by_depth' in d:
                return d          # a refusal still returns JSON, just not an answer
        except Exception:
            pass
    return None

TOTAL = lambda d: d['bounded']

# The ceiling law C(l,n) = (12l-6)n - 2(l^2-1) caps depth n-l. At n=4 that is
# depth-1 <= 104, depth-2 <= 66, depth-3 <= 24 -- and BOTH the record and every local
# maximum the basin campaign found already sit EXACTLY at the depth-2 and depth-3 caps:
#     record 183 : {1:92, 2:66, 3:24}      best climb 141 : {1:50, 2:66, 3:24}
# The whole 42-region gap is depth-1, the only layer with headroom. So a total-count
# climb stalls for a structural reason: raising depth-1 has to disturb layers pinned at
# their cap, which can only move DOWN, so the total dips and a strictly-improving walk
# refuses the one move it needs. Weighting by headroom-to-cap removes that trap.
def CAPS(n):
    return {n - l: (12 * l - 6) * n - 2 * (l * l - 1) for l in range(1, n + 1)}

def HEADROOM(n):
    """A STATEFUL objective: headroom is a WEIGHT on candidates, not a factor on itself.

    The first version returned sum_k (cap_k - v_k) * v_k, which is a different thing
    entirely -- it is maximised at HALF of every cap, so it scored the n=4 record 1104
    and a total-99 profile 3937, ranking the record LAST. A walk on it duly climbed to
    2952 while the total fell to 111, which looked like a falsification of the
    cap-headroom idea and was a falsification of the formula.

    The weights must be fixed at the CURRENT configuration and applied to the
    candidates: w_k = cap_k - v_k(current), objective(candidate) = sum_k w_k*v_k. At a
    configuration already pinned at the depth-2 and depth-3 caps that gives w = (54,0,0)
    and the objective becomes depth-1 alone, which is the intended behaviour.
    """
    caps = CAPS(n)
    def make(cur):
        bd = {int(k): int(v) for k, v in cur['by_depth'].items()}
        w = {k: max(0, caps[k] - bd.get(k, 0)) for k in caps if k > 0}
        def f(d):
            dd = {int(k): int(v) for k, v in d['by_depth'].items()}
            return sum(w[k] * dd.get(k, 0) for k in w)
        return f
    make.stateful = True
    return make

def CAPPED(n):
    """lexicographic: maximise depth-1, break ties on the layers held at their caps"""
    caps = CAPS(n)
    def f(d):
        bd = {int(k): int(v) for k, v in d['by_depth'].items()}
        deep = sum(bd.get(k, 0) for k in caps if k >= 2)
        return 1000 * bd.get(1, 0) + deep
    return f
def LAYER(k):
    return lambda d: d['by_depth'].get(str(k), 0)
def WEIGHTED(w):
    return lambda d: sum(w.get(int(k), 0) * v for k, v in d['by_depth'].items())

def walk(cfg, objective, label, ndir=12, iters=25, anneal=0, seed=0, verbose=True):
    rng = random.Random(seed)
    cubes = list(cfg)
    d0 = full(cubes)
    if d0 is None:
        return None
    obj = objective(d0) if getattr(objective, 'stateful', False) else objective
    cur = obj(d0)
    best = (cur, d0['bounded'], list(cubes))
    stall = 0
    for it in range(1, iters + 1):
        D.set_field(0); D.QZERO[:] = [cubes[0]]
        pt = D.point_of(cubes)
        if pt is None:
            break
        n = len(cubes); ncols = 3 * (n - 1)
        base = C.cfg_at(pt, cubes[0]); rec = C.cnt(base)
        bsub = tuple(C.cnt([base[i] for i in range(n) if i != j]) for j in range(n))
        den = (max(abs(v) for v in cubes[-1]) or 1) * C.M
        if getattr(objective, 'stateful', False):
            dcur = full(cubes)                 # weights are re-derived at each new point
            if dcur is not None:
                obj = objective(dcur); cur = obj(dcur)
        cands, unev = [], 0
        for _ in range(ndir):
            v0 = rand_dir(rng, ncols)
            for sgn in (1, -1):
                r = C.first_crossing(pt, tuple(sgn * x for x in v0), den, rec,
                                     cubes[0], ncols, n, bsub)
                if r['why'] != 'crossed':
                    if 'unevaluable' in r['why']:
                        unev += 1
                    continue
                dd = full(r['cfg'])
                if dd is None:
                    unev += 1; continue
                cands.append((obj(dd), dd['bounded'], r['cfg']))
        if not cands:
            if verbose:
                print('   [%s] iter %d: no crossing evaluated (%d unevaluable); stop'
                      % (label, it, unev), flush=True)
            break
        cands.sort(key=lambda t: -t[0])
        top = cands[0]
        up = top[0] > cur
        if not up and stall >= anneal:
            if verbose:
                print('   [%s] iter %d: no improving move and anneal budget spent; stop'
                      % (label, it), flush=True)
            break
        # height control, the same rule the record climb uses
        pt2 = D.point_of(top[2])
        if pt2 is not None:
            _, cf2 = C.simplify_point(pt2, top[1], top[2][0], ncols)
            if C.cnt(cf2) == top[1]:
                top = (top[0], top[1], cf2)
        cubes = list(top[2]); cur = top[0]
        stall = 0 if up else stall + 1
        if cur > best[0]:
            best = (cur, top[1], list(cubes))
        if verbose:
            print('   [%s] iter %2d: objective %s (total %d) %s  height %d  [%d unevaluable]'
                  % (label, it, cur, top[1], 'UP' if up else 'DOWN (anneal %d/%d)' % (stall, anneal),
                     max(abs(x) for q in cubes for x in q), unev), flush=True)
    return best

if __name__ == '__main__':
    from haarsample import haar_config
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    AN = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    rng = random.Random(555 + n)
    print('n=%d  record is %s ; best basin climb so far 141 (n=4)'
          % (n, {4: 183, 5: 393, 6: 727}.get(n)), flush=True)
    for k in range(K):
        cfg = haar_config(rng, n, 128, chart=True)
        d0 = full(cfg)
        print('\nstart %d: total %d, profile %s' % (k, d0['bounded'], d0['by_depth']), flush=True)
        a = walk(cfg, TOTAL, 'total,no-anneal', anneal=0, seed=k)
        print('   -> total-objective, no anneal : best total %d' % a[1], flush=True)
        b = walk(cfg, TOTAL, 'total,anneal', anneal=AN, seed=k)
        print('   -> total-objective, anneal %d  : best total %d' % (AN, b[1]), flush=True)
        c = walk(cfg, LAYER(1), 'layer1', anneal=AN, seed=k)
        print('   -> LAYER-1 objective          : best depth-1 %d, its total %d' % (c[0], c[1]), flush=True)
        if c[2]:
            e = walk(c[2], TOTAL, 'layer1-then-total', anneal=AN, seed=k)
            print('   -> then total from there      : best total %d' % e[1], flush=True)
        g = walk(cfg, CAPPED(n), 'capped(depth1 first)', anneal=AN, seed=k)
        print('   -> CAPPED objective           : best total %d (depth-1 %d)'
              % (g[1], g[0] // 1000), flush=True)
        h = walk(cfg, HEADROOM(n), 'headroom-weighted', anneal=AN, seed=k)
        print('   -> HEADROOM-weighted          : best total %d' % h[1], flush=True)
