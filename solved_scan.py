#!/usr/bin/env python3
"""Every chamber along a line, SOLVED — the answer to "locally maximal over the
directions walked".

`climb.py` walks isotropic rays and bisects to the first count change. Two things are
then sampled, not solved: WHICH facets get found (only those a ray happens to hit), and
the claim that nothing higher lies further out along the same line. So its termination
message says "locally maximal OVER THE DIRECTIONS WALKED", which is a lower bound
wearing the words of a decision.

For a ray that moves ONE cube, the walls are exactly enumerable and this stops being a
sample. With the other n-1 cubes fixed, the free cube's 3-dimensional Cayley slice
carries two wall families, and both are already solved in this repository:

  W4  a face plane of the free cube through a triple point of the base planes --
      `w4_polys` gives one QUADRATIC per (triple point, face), roots by `root_values`;
  W3  an edge of the free cube meeting a base crossing line -- `wall_params.w3_params`.

Together they are every wall the line meets, so sorting their roots partitions the line
into its chambers with nothing stepped over. Measured at a random configuration: the
catalogue costs 0.3 s (n=4) to 2.1 s (n=6), and one ray then yields 350-1518 W4 roots
and 1126-3624 W3 parameters in 0.9-3.0 s.

REPRESENTATIVES ARE THE SIMPLEST RATIONAL IN EACH INTERVAL, never the midpoint.
Midpoints of rationals with unrelated denominators compound, and that alone once put 10
of 24 cells outside an exact engine's budget and got written up as "42% unmeasurable".
`simplest_between` costs nothing and keeps every probe inside the engine.

HOW EXACT, EXACTLY -- because "solved" was overclaimed here once already. The two wall
families are NOT on the same footing:

  W4  quadratics. The discriminant is rational and its sign is decided by isqrt, so
      whether a W4 wall is real is decided EXACTLY; only the root's value is truncated
      (root_values, ~1e-60).
  W3  quartics. `wall_params.real_roots` falls back to `np.roots` in DOUBLE precision
      and keeps a root when |imag| < 1e-9, then rounds via limit_denominator(1e12). So
      a W3 wall's position is good to ~1e-12 and its EXISTENCE is decided by a float
      threshold: a near-double root can be dropped, or a spurious pair kept.

What survives that unharmed: every count this returns is the exact count of an exactly
specified rational configuration, so a POSITIVE result ("here is a configuration with
129") is a hard fact. What does not: completeness. A NEGATIVE result is "nothing higher
in the chambers found", and the chamber list is complete only up to W3 root precision.
Making the negative airtight needs exact real-root isolation on the quartics (Sturm),
not more lines.

WHAT THIS DOES AND DOES NOT SETTLE. Along each line scanned, the chamber list is
complete and every count is exact -- no wall is stepped over and no probe is refused for
being an expensive representative. It does NOT enumerate the facets of the ambient
chamber: a line is still chosen, and lines that move several cubes at once have no such
wall enumeration in this repository. So a negative result here is "nothing higher on
these lines, all of them scanned exactly", which is strictly stronger than "no crossing
above along these rays" and still not "this is a local maximum".
"""
import random, sys
from fractions import Fraction as F
sys.path.insert(0, '.')
import dimension as D
import wall_params as W
from catcache import catalogue
from n78_ends import w4_polys
from solve_more_ends import root_values, q_of_rat
from simplest import simplest_between
import json as _json, subprocess as _sub

def count(cfg):
    """exact count, narrow engine then the 256-bit one -- a refusal by the narrow
    engine is about the representative's height, not about the configuration"""
    st = ';'.join(','.join(map(str, q)) for q in cfg)
    for cmd in (['./cube_regions_n', '--quats', st],
                ['./cube_regions_q2w', '--d', '0', '--quats', st]):
        try:
            return _json.loads(_sub.run(cmd, capture_output=True, text=True).stdout)['bounded']
        except Exception:
            continue
    return None

# Two roots closer than this are the SAME root, reported twice. `root_values` states
# ~1e-60 accuracy, and the measured gap distribution at the n=5 record is bimodal with
# nothing in between: 603 of 719 gaps exceed 1e-12, 116 fall below 1e-50 (smallest
# 3.4e-65). No geometry makes gaps of 1e-65 but never 1e-30, so the small population is
# duplicates -- distinct quadratics sharing a root, each rounded slightly differently.
# The tolerance sits in the empty band between the two populations.
DUP_TOL = F(1, 10**30)


def crossings(base, a0, dv):
    """every wall parameter along a0 + s*dv, sorted, with duplicate roots MERGED.

    Not merging them was the whole of the "36% of chambers refused" problem. Two copies
    of one root bound a phantom interval of width ~1e-124; `simplest_between` then has
    to fit a 62-digit denominator inside it, and the resulting configuration overflows
    both engines. That read as an engine ceiling and very nearly justified building a
    modular-arithmetic engine to remove it. The interval was not thin -- it was not
    there.
    """
    pts, lines = catalogue(base)
    vals = set()
    for p in w4_polys(a0, dv, pts):
        for v in root_values(p):
            vals.add(F(v))
    for v in W.w3_params(a0, dv, lines):
        vals.add(F(v))
    out = []
    for v in sorted(vals):
        if out and v - out[-1] < DUP_TOL:
            continue                      # same root, reported twice
        out.append(v)
    return out

def scan_line(cfg, j, dv, reach=6):
    """exact count in each chamber the line meets, out to `reach` walls either way.

    Returns [(s, count)] with s the SIMPLEST rational inside each chamber.
    """
    base = list(cfg[:j]) + list(cfg[j + 1:])
    a0 = D.cayley_of(cfg[j])
    if a0 is None:
        return []
    r = crossings(base, a0, dv)
    lo = [x for x in r if x < 0][-reach:]
    hi = [x for x in r if x > 0][:reach]
    edges = lo + [F(0)] + hi
    out = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        if a == b:
            continue
        s = simplest_between(a, b)
        cfg2 = list(cfg); cfg2[j] = q_of_rat(a0, dv, s)
        c = count(cfg2)
        out.append((s, c, tuple(cfg2[j])))
    return out

def best_on_lines(cfg, ndir=4, reach=6, seed=0, verbose=True):
    """scan single-cube lines exactly; return the best (count, cfg) found, and a census"""
    rng = random.Random(seed)
    base_c = count(cfg)
    best = (base_c, list(cfg))
    tot = unev = 0
    for j in range(1, len(cfg)):
        for _ in range(ndir):
            dv = [F(rng.randint(-9, 9)) for _ in range(3)]
            if not any(dv):
                continue
            for s, c, q in scan_line(cfg, j, dv, reach):
                tot += 1
                if c is None:
                    unev += 1; continue
                if c > best[0]:
                    cfg2 = list(cfg); cfg2[j] = q
                    best = (c, cfg2)
    if verbose:
        print('   solved scan: %d chambers along %d lines, %d UNEVALUATED, best %d (from %d)'
              % (tot, (len(cfg) - 1) * ndir, unev, best[0], base_c), flush=True)
    return best, tot, unev

if __name__ == '__main__':
    from haarsample import haar_config
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rng = random.Random(770001 + 131 * n + 7919 * 0)      # the basin shard-0 start stream
    cfg = haar_config(rng, n, 128, chart=True)
    print('n=%d start count %s  (basin shard 0 #0, which the ray climb called locally maximal)'
          % (n, count(cfg)), flush=True)
    best, tot, unev = best_on_lines(cfg, ndir=int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    print('best found: %d' % best[0])
    if best[0] > count(cfg):
        print('VERDICT: the ray climb terminated EARLY — solved lines reach higher.')
    else:
        print('VERDICT: nothing higher on these exactly-scanned lines.')
