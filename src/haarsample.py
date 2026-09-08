#!/usr/bin/env python3
"""Exactly-Haar random configurations, and the count distribution over them.

WHY THIS SAMPLER.  "Volume of the space" only means something once a measure is
named.  Lebesgue measure in Cayley coordinates is INFINITE (the chart is R^3 per
cube and a half-turn is at infinity), so it cannot weight anything.  The measure
that exists and is canonical is Haar on SO(3)^(n-1) after gauge-fixing cube 0 --
the unique rotation-invariant probability measure, and the only one under which
"volume of the set reaching count c" is a well-defined number.

HOW IT IS SAMPLED EXACTLY.  Rounding a float quaternion to a rational would put
the sample in a different chamber whenever the real point sat within the rounding
of a wall -- a rounding error at exactly the place the measurement is about.  So
no rounding happens.  Draw an INTEGER 4-vector uniformly from the box [-Q,Q]^4 and
reject unless its norm^2 <= Q^2.  A uniform point of the 4-BALL has direction
exactly uniform on S^3, and only the direction of a quaternion names a rotation,
so the rotation is exactly Haar and the quaternion is exactly an integer 4-tuple.

The one approximation left is that the point is a LATTICE point of the ball, not a
continuous one; the sampler's total-variation distance from Haar is O(1/Q), which
at Q = 10^6 is ~1e-6, four orders below the Monte Carlo error 1/sqrt(K) of any
run we can afford.  That is the honest statement: exact arithmetic, exact
uniformity on S^3 up to a lattice discretisation whose size is bounded and stated.

Cube 0 is frozen at the identity (the gauge), so n cubes cost n-1 draws.
"""
import json, subprocess, sys, random, time, os
from math import gcd

ENG = './cube_regions_n'
ENGW = './cube_regions_q2w'

def haar_quat(rng, Q):
    """an integer quaternion whose rotation is Haar-distributed on SO(3)"""
    Q2 = Q * Q
    while True:
        v = [rng.randint(-Q, Q) for _ in range(4)]
        s = sum(x * x for x in v)
        if 0 < s <= Q2:
            g = 0
            for x in v:
                g = gcd(g, abs(x))
            return tuple(x // g for x in v)

def haar_config(rng, n, Q, chart=False):
    """n cubes, cube 0 the gauge; chart=True excludes half-turns.

    A half-turn (w = 0) has no Cayley representative, so a climber working in that
    chart cannot start there.  {w = 0} is a hyperplane: Haar-null in the continuum,
    but a positive fraction ~1/(2Q) of the LATTICE, so it shows up in the sample as a
    discretisation artifact and not as a property of the measure.  Rejecting it
    therefore removes an artifact rather than biasing the estimate -- and the counting
    runs (chart=False) keep them, since the engine needs no chart."""
    out = [(1, 0, 0, 0)]
    while len(out) < n:
        q = haar_quat(rng, Q)
        if chart and q[0] == 0:
            continue
        out.append(q)
    return out

def count(cfg, exe=ENG):
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    cmd = [exe, '--quats', s] if exe.endswith('_n') else [exe, '--d', '0', '--quats', s]
    try:
        return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)['bounded']
    except Exception:
        return None

if __name__ == '__main__':
    n = int(sys.argv[1]); K = int(sys.argv[2]); Q = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6
    out = 'haar_n%d_Q%d.jsonl' % (n, Q)
    done = 0
    if os.path.exists(out):
        done = sum(1 for _ in open(out))
    rng = random.Random(20260901 + 1000 * n)
    for _ in range(done):          # replay so a restart continues the same stream
        haar_config(rng, n, Q)
    t0 = time.time()
    with open(out, 'a') as f:
        for i in range(done, K):
            cfg = haar_config(rng, n, Q)
            c = count(cfg)
            f.write(json.dumps({'i': i, 'c': c, 'q': cfg}) + '\n'); f.flush()
    print('n=%d K=%d Q=%d  %.1fs  -> %s' % (n, K, Q, time.time() - t0, out))
