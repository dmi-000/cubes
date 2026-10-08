#!/usr/bin/env python3
"""(L) at the low-end vertices, the residue the per-direction lemma leaves.  [P419]

[P419]'s exhaustive per-direction lemma shows (L) can fail only where few ends exist:
- four-fold vertices (all four cubes tie, none outer) with `C12 <= 2`;
- triple vertices (three tie, one outer) whose bottom degree is `<= 2`.
At such vertices nearly every active point is SHARED. Random sampling rarely produces them,
so this generates them directly.

**Generator.**
- A pool of 2-6 positions on the circle.
- Each cube owns 1 or 2 of them, or 3 at a corner. A two-point cube's points are theta(F)
  apart (one common F); at a corner, every cube has three points 120 degrees apart.
- Two cubes co-own at most one point (two would make them one cube).

Only realisable owner patterns are kept, and only low-end vertices are scored.

**Score.** The excess `max(0, (deg_Γ − 2) − Σ_S (deg_S − 2))`, from patch_charging_local's exact
circle model.
- Also tallied: how many low-end vertices are genuine vertices of Γ (degree >= 3), since (L) is
  automatic below that.
- The sharing structure each configuration implies is recorded. A point owned by a set K means K
  shares a plane.
- Implied structures outside the eight realisable ones ([P419]) are counted separately, since
  they are not cubes.

**Control.** Swapping in [P405]'s blades must still fire (inherited from patch_charging_local).
Here the control is that low-end vertices with degree >= 3 DO occur, so the residue is not
vacuous. Output: data/lowend_check.json.
"""
import os, sys, json, random, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from patch_charging_local import N, CUBES, TRIPLES, analyse, classify, tie_degree, level_tie, cdist, theta_units

ROOT = os.path.dirname(os.path.dirname(HERE))


def low_end(pts, outer):
    """True if the vertex is in the residue: four-fold with C12 <= 2, or triple (one outer) with
    bottom degree <= 2."""
    T = sorted(pts)
    dist = {x: [min(cdist(w, p) for p in pts[x]) for w in range(N)] for x in T}
    def deg(members, level):
        return tie_degree([level_tie(dist, members, level, w) for w in range(N)])[1]
    if len(T) == 4 and not outer:
        return deg(T, 3) <= 2
    if len(T) == 3 and len(outer) == 1:
        return deg(T, 2) <= 2
    return False


def structure(pts):
    """implied sharing classes: owner sets of size >= 2"""
    owners = collections.defaultdict(set)
    for x, ps in pts.items():
        for p in ps:
            owners[p].add(x)
    return sorted(''.join(sorted(o)) for o in owners.values() if len(o) >= 2)


def realisable(classes):
    """the eight structures: classes pairwise meet in <= 1 cube, no triangle of three classes
    meeting pairwise in three distinct cubes, no 4-cycle of pair classes."""
    cl = [set(c) for c in classes]
    for a, b in itertools.combinations(cl, 2):
        if len(a & b) > 1:
            return False
    for a, b, c in itertools.combinations(cl, 3):
        ab, bc, ca = a & b, b & c, c & a
        if ab and bc and ca and len(ab | bc | ca) == 3:
            return False
    pairs = [c for c in cl if len(c) == 2]
    for quad in itertools.combinations(pairs, 4):
        deg = collections.Counter(x for c in quad for x in c)
        if len(deg) == 4 and all(v == 2 for v in deg.values()):
            return False
    return True


def config(rnd):
    corner = rnd.random() < 0.2
    th = 480 if corner else 4 * round(theta_units(rnd.uniform(1 / 3 + 1e-3, 1 / 2)) / 4)
    T = list(CUBES) if rnd.random() < 0.5 else rnd.sample(CUBES, 3)
    outer = set() if len(T) == 4 else {x for x in CUBES if x not in T}
    # a pool closed under +-th steps from a few seeds, so two-point cubes can be placed
    seeds = [4 * rnd.randrange(N // 4) for _ in range(rnd.randint(1, 3))]
    pool = set()
    for s in seeds:
        for k in range(-2, 3):
            pool.add((s + k * th) % N)
    pool = sorted(pool)
    pts = {}
    for x in T:
        k = 3 if corner else rnd.choice([1, 2])
        base = rnd.choice(pool)
        if k == 1:
            pts[x] = {base}
        elif k == 2:
            pts[x] = {base, (base + rnd.choice([th, -th])) % N}
        else:
            pts[x] = {base, (base + th) % N, (base - th) % N}
    for x, y in itertools.combinations(T, 2):
        if len(pts[x] & pts[y]) > 1:
            return None
    return pts, outer


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    rnd = random.Random(4191)
    st = collections.Counter()
    by_struct = collections.Counter()
    fails = []
    n = 0
    while n < trials:
        c = config(rnd)
        if c is None:
            continue
        n += 1
        pts, outer = c
        cls = structure(pts)
        if not cls:
            continue                                  # no sharing: [P405] covers it
        if not low_end(pts, outer):
            st['not_low_end'] += 1
            continue
        if not realisable(cls):
            st['low_end_unrealisable_structure'] += 1
            continue
        r = analyse(pts, outer)
        if r is None:
            st['low_end_off_G'] += 1
            continue
        dG, dS = r
        st['low_end_deg_%s' % ('>=3' if dG >= 3 else '<=2')] += 1
        ex = max(0, (dG - 2) - sum(d - 2 for d in dS.values()))
        st['excess_%d' % ex] += 1
        by_struct[(' '.join(cls), 'deg>=3' if dG >= 3 else 'deg<=2')] += 1
        if ex and len(fails) < 20:
            fails.append({'pts': {k: sorted(v) for k, v in pts.items()}, 'outer': sorted(outer),
                          'deg_G': dG, 'deg_S': dS, 'classes': cls})
    print(dict(sorted(st.items())))
    for k, v in sorted(by_struct.items()):
        print('   %-24s %-7s %d' % (k[0], k[1], v))
    print('control (low-end vertices of degree >= 3 occur): %s' % (st['low_end_deg_>=3'] > 0))
    json.dump({'stats': dict(st), 'by_structure': {'%s|%s' % k: v for k, v in by_struct.items()},
               'failures': fails}, open(os.path.join(ROOT, 'data', 'lowend_check.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
