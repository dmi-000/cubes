#!/usr/bin/env python3
"""[OQ 30] by derivation: the facet-centre lemma, and the parity it forces.

THE LEMMA (proved, not measured).  Let the cubes be congruent and CONCENTRIC, each
A_j = {x : |<x, v_{j,k}>| <= 1, k = 1..3} with {v_{j,k}} orthonormal.  Let u be a face normal
of A_i, so the centre of that facet is the point p = u.  Then for every j and every k,

    |<p, v_{j,k}>| = |<u, v_{j,k}>| <= ||u|| ||v_{j,k}|| = 1        (Cauchy-Schwarz)

with equality iff u = +-v_{j,k}.  So **the centre of every facet lies in every other cube**,
and in the INTERIOR of it unless two cubes share a face plane -- which is exactly the
degeneracy [P269] excludes.  One line, and it holds for every n, every level, every
configuration in the non-degenerate locus.

THE CONSEQUENCE.  Fix a facet F of A_i and write Q_j = F ∩ A_j for j != i.  Each Q_j is convex
and, by the lemma, contains p in its relative interior, so it is star-shaped about p: in polar
coordinates (theta, t) centred at p,

    x in Q_j   <=>   t <= r_j(theta).

The depth of x in relint(F) is 1 + #{j : x in A_j}, a count of conditions each of the form
`t <= r_j(theta)`, so **depth is non-increasing along every ray from the facet centre.**  With
rho_1 >= rho_2 >= ... the sorted radial functions,

    depth(theta, t) = m   <=>   rho_m(theta) < t <= rho_{m-1}(theta)

-- the region between two radial graphs.  Its components are the maximal arcs of
{theta : rho_{m-1} > rho_m}, each a disk, EXCEPT when that set is all of S^1, which gives one
annulus.  So **every face of the depth surface is a disk except for at most one annulus per
facet**, and no face has more than two boundary circles.

THE PARITY.  For a graph on S^2 with c components and faces f, sum_f (b(f) - 1) = c - 1, where
b(f) counts boundary circles.  By the consequence above every b(f) <= 2, so c - 1 is the number
of ANNULUS faces.  An annulus lies in one facet; the antipodal map sends that facet to the
OPPOSITE facet of the same cube, never to itself, so annuli come in antipodal pairs.  Hence

    c - 1 is EVEN, i.e. c_ell is ODD -- for the full 1-skeleton of the depth surface.

AND THAT CONTRADICTS THE MEASURED c = 2.  The resolution this file tests: `c_level.level_graph`
builds arcs only from ∂A_i ∩ ∂A_j with i != j.  The depth surface also creases along the EDGES
of a single cube, and those creases separate two faces just as a wall does.  The measured graph
is therefore a SUBGRAPH of the 1-skeleton, so its component count is an upper bound for the
true one.  Prediction: adding the crease edges makes c odd, and in the known c = 2 instances it
makes c = 1.

Reported either way.  A derivation that disagrees with a measurement is a bug in one of them.
"""
import sys, os, json, itertools, collections, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import level_graph, shares_plane, strictly_inside
import wall_keys as W
import provenance as PROV


def facet_centre_lemma(qs):
    """G: every facet centre strictly inside every other cube.  The lemma, as a gate."""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    worst = None
    for i in range(n):
        for k in range(3):
            for sgn in (1, -1):
                # the facet centre is the k-th face normal of cube i, signed
                p = [sgn * Ms[i][k][z] for z in range(3)]
                for j in range(n):
                    if j == i:
                        continue
                    for m in range(3):
                        v = abs(sum(Ms[j][m][z] * p[z] for z in range(3)))
                        if worst is None or v > worst:
                            worst = v
    return worst          # must be <= 1, and < 1 off the shared-plane locus


def arcs_by_kind(qs):
    """(crease arcs, wall arcs) keyed by level, with their endpoints."""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    crease = collections.defaultdict(list)
    wall = collections.defaultdict(list)

    def seg(store, ell, p, d, a, b):
        store[ell].append((tuple(p[z] + a * d[z] for z in range(3)),
                           tuple(p[z] + b * d[z] for z in range(3))))

    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s_ = sum(1 for k in range(n) if k not in (i, j)
                         and strictly_inside(mid, Ms[k]))
                seg(wall, s_ + 1, p, d, a, b)          # depth s+2, level s+1
    for i in range(n):
        V = [Ms[i][k] for k in range(3)]
        for c in range(3):
            o = [k for k in range(3) if k != c]
            for s0 in (1, -1):
                for s1 in (1, -1):
                    p = [s0 * V[o[0]][z] + s1 * V[o[1]][z] for z in range(3)]
                    d = [V[c][z] for z in range(3)]
                    cuts = sorted({F(-1), F(1)} | {t for k in range(n) if k != i
                                   for t in on_bdry_params(p, d, F(-1), F(1), Ms[k])})
                    for a, b in zip(cuts, cuts[1:]):
                        if a >= b:
                            continue
                        mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                        s_ = sum(1 for k in range(n) if k != i
                                 and strictly_inside(mid, Ms[k]))
                        seg(crease, s_, p, d, a, b)     # depth s+1, level s
    return crease, wall


def full_skeleton(qs):
    """The 1-skeleton of every depth surface S_ell = boundary of the depth->=(ell+1) body.

    THE PAIRING TOOK THREE ATTEMPTS, each killed by the parity gate, and the corrections are
    kept because each was a plausible reading:

      1. creases at ell + walls at ell          -- level-0 got creases and no walls at all
      2. creases at ell + walls at ell+1        -- the top level got creases and no walls
      3. creases at ell + walls at ell AND ell+1   <- correct

    A face of S_ell is a piece of a facet at depth ell+1.  Going outward it ends where the depth
    DROPS to ell, on a wall arc of depth ell+1 (level ell); going inward it ends where the depth
    RISES to ell+2, on a wall arc of depth ell+2 (level ell+1).  Both bound it.  A crease at
    depth ell+1 (level ell) bounds it too, where the facet changes without the depth changing.
    """
    crease, wall = arcs_by_kind(qs)
    out = {}
    for ell in sorted(set(crease) | set(wall)):
        segs = crease.get(ell, []) + wall.get(ell, []) + wall.get(ell + 1, [])
        if not segs:
            continue
        idx = {}
        for a, b in segs:
            for P in (a, b):
                idx.setdefault(P, len(idx))
        par = list(range(len(idx)))

        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        for a, b in segs:
            par[f(idx[a])] = f(idx[b])
        comp = collections.Counter(f(x) for x in range(len(par)))
        out[ell] = {'V': len(idx), 'E': len(segs), 'c': len(comp),
                    'sizes': sorted(comp.values(), reverse=True)}
    return out


def parse(spec):
    return [tuple(int(v) for v in q.split(',')) for q in spec.split(';')]


def hunt(trials, seed=11, lo=-25, hi=25):
    """Integer draws until c = 2 appears in the WALL graph -- the measured quantity."""
    rng = random.Random(seed)
    found = []
    for _ in range(trials):
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(lo, hi) for _ in range(4))
                               for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            g = level_graph(qs)
        except Exception:
            continue
        hits = {l: v for l, v in g.items() if v['c'] > 1}
        if hits:
            found.append((qs, hits))
    return found


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    out = {'what': 'the facet-centre lemma, and whether the crease edges reconcile the '
                   'measured c with the parity the lemma forces',
           'question': 'OPEN_QUESTIONS 30', 'lemma_checks': [], 'instances': []}

    for n in (4, 5, 6):
        qs = [tuple(q) for q in W.REC[n]]
        w = facet_centre_lemma(qs)
        out['lemma_checks'].append({'config': 'record n=%d' % n, 'max_abs_inner': str(w),
                                    'lemma_holds': bool(w <= 1), 'strict': bool(w < 1)})
        print('lemma at record n=%d: max |<facet centre, face normal>| = %s  (<=1: %s)'
              % (n, w, w <= 1), flush=True)

    print('hunting for c > 1 in %d integer draws...' % trials, flush=True)
    found = hunt(trials)
    print('found %d configurations with c > 1 in the wall graph' % len(found), flush=True)
    for qs, hits in found[:6]:
        w = facet_centre_lemma(qs)
        full = full_skeleton(qs)
        rows = []
        for l, v in sorted(hits.items()):
            fv = full.get(l, {})
            rows.append({'level': l, 'wall_c': v['c'], 'wall_sizes': v['sizes'],
                         'full_c': fv.get('c'), 'full_V': fv.get('V'),
                         'full_sizes': fv.get('sizes')})
            print('   %s  level %s: wall c=%d %s -> full 1-skeleton c=%s %s'
                  % (';'.join(','.join(map(str, q)) for q in qs), l, v['c'], v['sizes'],
                     fv.get('c'), fv.get('sizes')), flush=True)
        out['instances'].append({'quats': [list(q) for q in qs],
                                 'lemma_max_abs_inner': str(w), 'levels': rows})
    out['reproduce'] = PROV.stamp(parameters={'trials': trials})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'facet_radial.json'), 'w'),
              indent=1, default=str)
    print('written data/facet_radial.json')


if __name__ == '__main__':
    main()
