#!/usr/bin/env python3
"""Trace the faces of Γ and find each band's region and pair, independently of the triples.  [P410]

Γ = the level-2 boundary of a 4-compound (arcs of dA_i n dA_j strictly inside exactly one cube k).
Each arc is a straight segment in R^3, so its radial image is a great-circle arc.  The faces of Γ
are traced from the rotation system: the cyclic order of arc directions in the tangent plane at
each vertex.  The label of the side of a half-edge (the compound's two farthest-reaching cubes):
{k, i} if cube i reaches farther just to the left, otherwise {k, j}.  "Farther" comes from comparing
the exact directional derivatives of the active faces of i and j along the left normal.

CHECKS (the intermediate objects of PROOF_BAND):
  F1  every face-boundary walk has ONE label all round it (G1: a region has one label)
  F2  Euler per component: walks = E - V + 2 (the trace is complete)
  F3  for c2 = 2: the face of component A containing component B, and the face of B containing
      A, carry the same label: the band region, read from both sides
  F4  that label equals the pair shared by the triples with c_S >= 2 (G4/G5's prediction)
Containment is a winding-number test, in floating point, on arcs subdivided 64 times, under a
stereographic projection from a random point.  Every decision is checked for consistency: each
component must lie in exactly one face of the other.
Output: data/band_faces.json.
"""
import os, sys, json, math, random, itertools, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params

ROOT = os.path.dirname(os.path.dirname(HERE))


def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def unit(a):
    n = math.sqrt(sum(float(x) ** 2 for x in a)); return tuple(float(x) / n for x in a)


def active_face(M, P):
    for r in range(3):
        v = dot(M[r], P)
        if v == 1: return tuple(M[r])
        if v == -1: return tuple(-x for x in M[r])
    raise ValueError('point not on a face')


def gamma(Ms):
    node, arcs = {}, []
    for i, j in itertools.combinations(range(4), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(4) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b: continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                ins = [k for k in range(4) if k not in (i, j) and CL.strictly_inside(mid, Ms[k])]
                if len(ins) != 1: continue
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, len(node)); ends.append(P)
                # left of the half-edge ends[0] -> ends[1]: left normal = mid x direction
                dirv = tuple(ends[1][z] - ends[0][z] for z in range(3))
                left = cross(mid, dirv)
                fi, fj = active_face(Ms[i], mid), active_face(Ms[j], mid)
                # larger derivative of M = smaller reach; i reaches farther on the left iff fi.left < fj.left
                di, dj = dot(fi, left), dot(fj, left)
                if di == dj: raise ValueError('degenerate side comparison')
                k = ins[0]
                lab_left = frozenset((k, i)) if di < dj else frozenset((k, j))
                lab_right = frozenset((k, j)) if di < dj else frozenset((k, i))
                arcs.append((ends[0], ends[1], lab_left, lab_right))
    return arcs


def trace(arcs):
    """half-edges h = (arc index, direction); returns walks as lists of half-edges and their labels"""
    out_at = collections.defaultdict(list)
    for e, (u, v, _, _) in enumerate(arcs):
        out_at[u].append((e, 0)); out_at[v].append((e, 1))
    def tail(h): return arcs[h[0]][0] if h[1] == 0 else arcs[h[0]][1]
    def head(h): return arcs[h[0]][1] if h[1] == 0 else arcs[h[0]][0]
    order = {}
    for P, hs in out_at.items():
        n = unit(P); a = unit(cross(n, (1.0, 0.3, 0.7))); b = cross(n, a)
        def ang(h):
            Q = unit(head(h)); t = tuple(Q[z] - dot(Q, n) * n[z] for z in range(3))
            return math.atan2(dot(t, b), dot(t, a))
        order[P] = sorted(hs, key=ang)
    def nxt(h):
        # arrive at v = head(h); leave by the half-edge just CLOCKWISE of the reverse of h, which
        # keeps the face on the LEFT
        v = head(h); rev = (h[0], 1 - h[1]); hs = order[v]; i = hs.index(rev)
        return hs[(i - 1) % len(hs)]
    def lab(h): return arcs[h[0]][2] if h[1] == 0 else arcs[h[0]][3]
    seen, walks = set(), []
    for e in range(len(arcs)):
        for s in (0, 1):
            h = (e, s)
            if h in seen: continue
            w = []
            while h not in seen:
                seen.add(h); w.append(h); h = nxt(h)
            walks.append(w)
    return walks, tail, head, lab


def comps(arcs):
    par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for u, v, _, _ in arcs:
        par[f(u)] = f(v)
    return f


def winding(walk, tail, head, x, z):
    """winding number of the walk's image around x, stereographic projection from z"""
    def proj(p):
        p = unit(p); s = 1.0 - dot(p, z)
        a = unit(cross(z, (0.3, 1.0, 0.2))); b = cross(z, a)
        return (dot(p, a) / s, dot(p, b) / s)
    X = proj(x); tot = 0.0; prev = None
    for h in walk:
        P, Q = unit(tail(h)), unit(head(h))
        for s in range(65):
            t = s / 64.0
            R = unit(tuple(P[z_] * (1 - t) + Q[z_] * t for z_ in range(3)))
            a = proj(R); ang = math.atan2(a[1] - X[1], a[0] - X[0])
            if prev is not None:
                dlt = ang - prev
                while dlt > math.pi: dlt -= 2 * math.pi
                while dlt < -math.pi: dlt += 2 * math.pi
                tot += dlt
            prev = ang
    return round(tot / (2 * math.pi))


def analyse(qs):
    Ms = [rowsT(R) for R in frames([tuple(q) for q in qs])]
    arcs = gamma(Ms)
    walks, tail, head, lab = trace(arcs)
    f = comps(arcs)
    f1 = all(len({lab(h) for h in w}) == 1 for w in walks)
    bycomp = collections.defaultdict(list)
    for w in walks: bycomp[f(tail(w[0]))].append(w)
    V = collections.Counter(); E = collections.Counter()
    for u, v, _, _ in arcs: E[f(u)] += 1
    for P in {a[0] for a in arcs} | {a[1] for a in arcs}: V[f(P)] += 1
    f2 = all(len(bycomp[c]) == E[c] - V[c] + 2 for c in bycomp)
    res = {'c2': len(bycomp), 'F1_one_label_per_walk': f1, 'F2_euler': f2, 'walks': len(walks)}
    if len(bycomp) != 2:
        return res
    rnd = random.Random(1)
    A, B = list(bycomp)
    labels, consistent = [], True
    for X_, Y_ in ((A, B), (B, A)):
        x = next(P for P in {a[0] for a in arcs} if f(P) == Y_)
        hits = []
        for w in bycomp[X_]:
            # reference point just left of the walk's first half-edge: in the face by construction
            h = w[0]; P, Q = unit(tail(h)), unit(head(h)); m = unit(tuple(P[z]+Q[z] for z in range(3)))
            l = unit(cross(m, tuple(Q[z]-P[z] for z in range(3))))
            y = unit(tuple(m[z] + 1e-7 * l[z] for z in range(3)))
            z = unit(tuple(rnd.gauss(0, 1) for _ in range(3)))
            if winding(w, tail, head, x, z) == winding(w, tail, head, y, z):
                hits.append(lab(w[0]))
        consistent &= len(hits) == 1
        labels.append(sorted(hits[0]) if len(hits) == 1 else [sorted(h) for h in hits])
    res.update({'F3_same_label_both_sides': consistent and labels[0] == labels[1],
                'band_label': labels[0], 'labels_seen': labels})
    return res


def main():
    rows = json.load(open(os.path.join(ROOT, 'data', 'band_components.json')))
    out, good = [], 0
    for r in rows:
        a = analyse(r['qs'])
        shared = sorted(set.intersection(*[set(S) for S in r['disconnected_triples']]))
        a['triple_pair'] = shared
        a['F4_agrees_with_triples'] = a.get('band_label') == shared
        ok = a['F1_one_label_per_walk'] and a['F2_euler'] and a.get('F3_same_label_both_sides') and a['F4_agrees_with_triples']
        good += bool(ok)
        print('c2 %d walks %3d F1 %s F2 %s F3 %s band label %s triples %s F4 %s'
              % (a['c2'], a['walks'], a['F1_one_label_per_walk'], a['F2_euler'],
                 a.get('F3_same_label_both_sides'), a.get('labels_seen'), shared, a['F4_agrees_with_triples']))
        out.append(a | {'qs': r['qs']})
    # control: the 183 record (c2 = 1, d2 = 66, a half-turn cube) must trace with F1 and F2 too
    rec = analyse([(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)])
    print('control, 183 record: c2 %d walks %d F1 %s F2 %s' % (rec['c2'], rec['walks'],
          rec['F1_one_label_per_walk'], rec['F2_euler']))
    good -= not (rec['c2'] == 1 and rec['F1_one_label_per_walk'] and rec['F2_euler'])
    print('%d of %d pass F1-F4, and the control %s' % (good, len(rows), 'passes' if good == len(rows) else 'or the control FAILS'))
    out.append(rec | {'qs': 'control: 183 record'})
    json.dump(out, open(os.path.join(ROOT, 'data', 'band_faces.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
