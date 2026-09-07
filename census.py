#!/usr/bin/env python3
"""Signature census: draw, signature, count, append. One row per configuration.

PHASE 1 IS DELIBERATELY NOT FILTERED. The point of the filter is to skip counts, but the
signature currently costs 0.8x a count, so filtering only pays at a skip rate above 76%
-- and more importantly, the relation between signature and count is what we are trying to
MEASURE, which needs the count on every draw. Filtering now would bias exactly the
distribution being characterised. The filter switches on later, from these ceilings.

MERGE SEMANTICS: rows are appended, never reduced. Keeping only the best count per
signature would destroy the spread, and the spread IS the measurement -- 0 of 12 repeated
signatures pinned the count, with spreads of 6-44. Two machines reporting different maxima
for one signature are two samples of a distribution, not two candidates for one slot.

Ensembles are a parameter because the whole point is breadth: `haar` is the null ensemble,
`axis` the one-shared-axis family that broke the 141 plateau, `twoaxis` the richer one that
holds depth-2 at its cap. Different shards should run different ensembles.
"""
import json, os, random, subprocess, sys, time
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from signature import signature
from sharedaxis import q_axis
from symmetrize import axes, project
from haarsample import haar_config, haar_quat
from math import gcd as _gcd

def qmul_prim(p, r):
    w, x, y, z = p; e, f, g, h = r
    q = (w*e - x*f - y*g - z*h, w*f + x*e + y*h - z*g,
         w*g - x*h + y*e + z*f, w*h + x*g - y*f + z*e)
    d = 0
    for v in q:
        d = _gcd(d, abs(v))
    return tuple(v // (d or 1) for v in q)

AX = axes(3)
VALS = [F(p, q) for q in (1,2,3,4,5,6,7,8) for p in range(-8,9) if p and gcd(abs(p), q) == 1]

def draw(kind, rng, n):
    if kind == 'haar':
        return haar_config(rng, n, 128, chart=True)
    if kind == 'axis':
        ax = rng.choice(AX)
        return [(1,0,0,0)] + [q_axis(ax, rng.choice(VALS)) for _ in range(n-1)]
    if kind == 'twoaxis':
        u, v = rng.choice(AX), rng.choice(AX)
        return [(1,0,0,0)] + [q_axis(u if rng.random() < 0.5 else v, rng.choice(VALS))
                              for _ in range(n-1)]
    if kind == 'chain':
        # cube k is cube k-1 rotated about a FRESH axis: consecutive pairs share an axis,
        # non-consecutive pairs do not. Makes PAIRS special rather than the whole set --
        # the structure JOURNEY Act IV attributes to the record, and one no star-shaped
        # shared-axis family can produce.
        out = [(1, 0, 0, 0)]
        for _ in range(n - 1):
            r = q_axis(rng.choice(AX), rng.choice(VALS))
            out.append(qmul_prim(out[-1], r))
        return out
    if kind == 'threeaxis':
        us = [rng.choice(AX) for _ in range(3)]
        return [(1, 0, 0, 0)] + [q_axis(rng.choice(us), rng.choice(VALS)) for _ in range(n-1)]
    if kind == 'mixed':
        ax = rng.choice(AX)
        k = max(1, (n - 1) // 2)
        out = [(1, 0, 0, 0)] + [q_axis(ax, rng.choice(VALS)) for _ in range(k)]
        while len(out) < n:
            out.append(haar_quat(rng, 128))
        return out
    if kind == 'project':                    # a Haar draw carried onto the structured set
        cfg = haar_config(rng, n, 128, chart=True)
        return [project(q, rng.choice(AX)) for q in cfg]
    raise ValueError(kind)

def full(cfg):
    """count, depth profile, and -- when there is no count -- WHY.

    An unevaluable configuration is not a lost draw. The signature is computed from the
    quaternions with no engine involved, so a refused configuration can still be
    signatured and placed in the table, and evaluability becomes a FEATURE to correlate
    rather than a hole in the sample. Two causes are distinguished because they mean
    opposite things: DEGENERATE is a property of the configuration (coincident cubes, a
    non-generic plane triple) and is the kind of structure records have, while a budget
    refusal is a property of the representative and this project has twice measured it to
    be an artifact -- 1040 refusals at the n=9 record became 0 on a cheaper representative.
    """
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    p = subprocess.run(['./cube_regions_n', '--quats', s], capture_output=True, text=True)
    try:
        d = json.loads(p.stdout)
        if d.get('bounded'):
            return d['bounded'], d.get('by_depth'), None
    except Exception:
        pass
    # THE ERROR IS IN STDOUT, AS JSON -- not stderr, which is always empty. Reading
    # stderr made every refusal classify as 'other' and hid the actual cause for a whole
    # census. The engine reports {"error": "..."} and exits 0.
    msg = ''
    try:
        msg = str(json.loads(p.stdout).get('error', ''))[:120]
    except Exception:
        msg = (p.stderr.strip().splitlines() or ['(no output)'])[-1][:120]
    low = msg.lower()
    why = ('single-region' if 'single region' in low
           else 'degenerate' if ('degener' in low or 'non-generic' in low)
           else 'budget' if ('budget' in low or 'overflow' in low)
           else 'other')
    return None, None, (why, msg)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    kind = sys.argv[2] if len(sys.argv) > 2 else 'haar'
    shard = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    host = sys.argv[4] if len(sys.argv) > 4 else 'a'
    out = 'census_n%d_%s_%s%d.jsonl' % (n, kind, host, shard)
    done = sum(1 for _ in open(out)) if os.path.exists(out) else 0
    rng = random.Random(hash((kind, shard, host)) & 0xffffffff)
    for _ in range(done):
        draw(kind, rng, n)                   # replay so a restart continues the stream
    print('census n=%d ensemble=%s shard=%s%d  (%d already recorded) -> %s'
          % (n, kind, host, shard, done, out), flush=True)
    t0 = time.time(); i = done; nrec = 0; unev = 0
    with open(out, 'a') as f:
        while True:
            cfg = draw(kind, rng, n)
            c, bd, err = full(cfg)
            sg = signature(cfg)              # computable with no engine, refused or not
            if not c:
                unev += 1; i += 1
                f.write(json.dumps({'sig': [list(t) for t in sg], 'count': None,
                                    'unevaluable': err[0], 'msg': err[1],
                                    'height': max(abs(x) for q in cfg for x in q),
                                    'cfg': [list(q) for q in cfg],
                                    'ens': kind, 'host': host, 'shard': shard}) + '\n')
                f.flush(); continue
            f.write(json.dumps({'sig': [list(t) for t in sg], 'count': c,
                                'depth': bd, 'cfg': [list(q) for q in cfg],
                                'ens': kind, 'host': host, 'shard': shard}) + '\n')
            f.flush(); i += 1; nrec += 1
            if nrec % 50 == 0:
                print('   %d recorded, %d unevaluable, %.1f/min' % (nrec, unev,
                      60.0 * nrec / max(time.time() - t0, 1)), flush=True)
