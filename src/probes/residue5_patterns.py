#!/usr/bin/env python3
"""The n = 5 multi-pair residue of H1, counted: every realisable owner pattern with u <= 2 and the
dimension of its parameter space.  [P439]

[P438] settles u >= 3 by hand except one minimal case; u is the number of tying cubes owning an
UNSHARED point. The rest (u <= 2) is to be settled as [P420] settled n = 4: exact evaluation on
every cell of a low-dimensional arrangement. This script only counts that work. It enumerates no
cells.

**Patterns.** t tying cubes (2–5). Each owns 1, 2 or 3 point labels (3 = a corner, which fixes the
common edge angle θ at 120). Constraints:
- two cubes co-own at most one label (two shared planes = one cube);
- every label has an owner;
- at most 2 cubes own a label nobody else owns (u <= 2; `--u3` allows 3, to size the u = 3 case);
- at least two shared labels in total, or one label with three or more owners (one sharing pair
  is [P435]);
- no triangle of three distinct shared labels pairwise linking three cubes ([P419]);
- a cube lies in at most 3 classes, which is automatic since it owns at most 3 points.

**Placements** (the realisable model). A two-point cube's points are b and b + sθ, s = ±1. A corner
cube's are b, b + 120 and b − 120. Shared labels identify points, so the labels fall into linked
components, each with one free offset; one offset is fixed by rotation.
- A cycle of links gives `kθ ≡ 0 (mod 360)` for some integer k. A solution in [120, 180] fixes θ;
  none means the placement is impossible.
- Placements that force two distinct labels to coincide are discarded; they are another
  pattern.

Dimension = free offsets + (θ free ? 1 : 0).

Output: data/residue5_patterns.json (counts by t, u and dimension, up to relabelling).
"""
import os, sys, json, itertools, collections
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UMAX = 3 if '--u3' in sys.argv else 2


def linear_hypergraphs(t):
    """sets of shared labels: subsets of size >= 2 of range(t), pairwise meeting in <= 1 cube,
    each cube in <= 3 of them"""
    cands = [frozenset(c) for k in range(2, t + 1) for c in itertools.combinations(range(t), k)]
    out = []

    def rec(start, chosen):
        out.append(list(chosen))
        for i in range(start, len(cands)):
            c = cands[i]
            if all(len(c & d) <= 1 for d in chosen):
                deg = collections.Counter(x for d in chosen + [c] for x in d)
                if max(deg.values()) <= 3:
                    chosen.append(c); rec(i + 1, chosen); chosen.pop()
    rec(0, [])
    return out


def triangle(shared):
    for a, b, c in itertools.combinations(shared, 3):
        ab, ac, bc = a & b, a & c, b & c
        if len(ab) == len(ac) == len(bc) == 1 and len(ab | ac | bc) == 3:
            return True
    return False


def patterns(t):
    """(owner list per label) for every pattern with u <= 2, up to relabelling of cubes"""
    seen = set()
    for shared in linear_hypergraphs(t):
        if triangle(shared):
            continue
        if not (len(shared) >= 2 or any(len(c) >= 3 for c in shared)):
            continue
        base = collections.Counter(x for c in shared for x in c)
        # add unshared labels to at most 2 cubes; each cube ends with 1–3 labels
        for us in itertools.chain(*[itertools.combinations(range(t), k) for k in range(0, UMAX + 1)]):
            ranges = []
            for x in us:
                lo = 1
                hi = 3 - base[x]
                if hi < lo:
                    break
                ranges.append(range(lo, hi + 1))
            else:
                if any(base[x] == 0 for x in range(t) if x not in us):
                    continue
                for ks in itertools.product(*ranges):
                    owners = [frozenset(c) for c in shared] + [frozenset([x]) for x, k in zip(us, ks) for _ in range(k)]
                    key = canon(t, owners)
                    if key in seen:
                        continue
                    seen.add(key)
                    yield owners, len(us)


def canon(t, owners):
    best = None
    for perm in itertools.permutations(range(t)):
        k = tuple(sorted(tuple(sorted(perm[x] for x in o)) for o in owners))
        if best is None or k < best:
            best = k
    return best


def placements(t, owners):
    """yield the dimension of each consistent sign/role placement"""
    labels = range(len(owners))
    cube_pts = {x: [i for i in labels if x in owners[i]] for x in range(t)}
    corner = any(len(v) == 3 for v in cube_pts.values())
    multi = [x for x in range(t) if len(cube_pts[x]) == 2]
    # for 2-point cubes: which label is the base, and the sign; for corners: the role order
    choices = []
    for x in range(t):
        ps = cube_pts[x]
        if len(ps) == 2:
            choices.append([(x, (ps[0], ps[1]), s) for s in (1, -1)])
        elif len(ps) == 3:
            choices.append([(x, perm, 1) for perm in itertools.permutations(ps)])
        else:
            choices.append([(x, tuple(ps), 0)])
    for combo in itertools.product(*choices):
        # union-find with offsets: pos(label) = pos(root) + c*θ + d (d in degrees, from corners)
        par = {i: (i, 0, Fr(0)) for i in labels}

        def find(i):
            p, c, d = par[i]
            if p == i:
                return i, 0, Fr(0)
            r, c2, d2 = find(p)
            par[i] = (r, c + c2, d + d2)
            return par[i]
        thetas = None          # None = free; else set of allowed θ values
        ok = True
        for x, ps, s in combo:
            if len(ps) == 2:
                links = [(ps[0], ps[1], s, Fr(0))]
            elif len(ps) == 3:
                links = [(ps[0], ps[1], 0, Fr(120)), (ps[0], ps[2], 0, Fr(-120))]
            else:
                links = []
            for a, b, c, d in links:
                # pos(b) = pos(a) + c θ + d
                ra, ca, da = find(a)
                rb, cb, db = find(b)
                if ra != rb:
                    par[rb] = (ra, ca + c - cb, da + d - db)
                else:
                    # cycle: ca + cθ + d == cb (mod 360) in θ-coefficient and degrees
                    k = ca + c - cb
                    dd = da + d - db
                    sols = set()
                    if k == 0:
                        if dd % 360 != 0:
                            ok = False
                        continue
                    for j in range(-10, 11):
                        th = (Fr(360) * j - dd) / k
                        if 120 <= th <= 180:
                            sols.add(th)
                    thetas = sols if thetas is None else thetas & sols
                    if not thetas:
                        ok = False
        if not ok:
            continue
        if corner:
            thetas = {Fr(120)} if thetas is None else thetas & {Fr(120)}
            if not thetas:
                continue
        # distinct labels must not be forced to coincide: same root, same θ-coefficient and offset
        roots = collections.defaultdict(list)
        for i in labels:
            r, c, d = find(i)
            roots[r].append((c, d))
        clash = False
        for r, v in roots.items():
            for (c1, d1), (c2, d2) in itertools.combinations(v, 2):
                if c1 == c2 and (d1 - d2) % 360 == 0:
                    clash = True
                if thetas is not None and all(((c1 - c2) * th + d1 - d2) % 360 == 0 for th in thetas):
                    clash = True
        if clash:
            continue
        comps = len(roots)
        theta_free = 1 if (thetas is None and multi) else 0
        yield comps - 1 + theta_free


def main():
    by = collections.Counter()
    npat = collections.Counter()
    for t in range(2, 6):
        for owners, u in patterns(t):
            dims = sorted(set(placements(t, owners)))
            if not dims:
                by[(t, u, 'impossible')] += 1
                continue
            npat[(t, u)] += 1
            by[(t, u, max(dims))] += 1
    print('patterns with u <= 2 (up to relabelling), by (t, u): %s' % sorted(npat.items()), flush=True)
    print('by (t, u, max placement dimension): %s' % sorted(by.items(), key=str), flush=True)
    json.dump({'patterns': {str(k): v for k, v in npat.items()}, 'by_dim': {str(k): v for k, v in by.items()}},
              open(os.path.join(ROOT, 'data', 'residue5_patterns%s.json' % ('_u3' if UMAX == 3 else '')), 'w'), indent=1)


if __name__ == '__main__':
    main()
