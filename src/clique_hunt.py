#!/usr/bin/env python3
# Working principles: record_hunt.py (engines, menus).  Idea: the user's
# observation that two (n-1)-subsets meet in an (n-2)-subset, so a fixed
# (n-2) CORE makes the levels above it cliques rather than samples.
"""Core-and-clique record hunt.

Any two (n-1)-subsets of an n-config intersect in an (n-2)-subset.  Fix that
intersection as a CORE of n-2 cubes and every config above it is core + a
set of extra cubes, with "all subsets stay large" becoming cliqueness:

    core + {x}        -- vertex, scored at n-1
    core + {x,y}      -- edge,   scored at n
    core + {x,y,z}    -- triangle, n+1
    core + {w,x,y,z}  -- K4,     n+2

Core here is the 4-cube 183 record, which the current tower already sits on:
393 = 183 + one cube and 727 = 393 + one more, so 727 is an EDGE of this
graph and any better n=6 is a better edge.  Unlike a random menu, this
enumerates -- the good extensions of a fixed core are a finite set once
quaternion height is capped.

INVARIANT: thresholds prune the graph but never the report.  Any config whose
total beats the standing record is logged whatever its subset profile, and
records still require certify_six before being claimed.
"""
import itertools
import random

import record_hunt as R

W = 2
OUT = open('clique_hunt.jsonl', 'a')
rng = random.Random(183183)

CORE = [[1, 0, 0, 0], [0, 5, 3, 2], [1, -4, -1, 1], [1, 1, -1, -4]]   # 183
RECORDS = {5: 393, 6: 727, 7: 1217, 8: 1891}
V_MENU = 60000        # candidate cubes screened at n=5
V_KEEP = 80          # vertices carried into the pair layer
V_TRI = 40            # vertices carried into the triangle layer
T_VERTEX = 365        # keep x if core+x reaches this at n=5

eng = {k: R.Engine(k, W) for k in (5, 6, 7, 8)}


def report(level, cfg, total, tag):
    R.log(OUT, stage=tag, n=level, total=total, quats=cfg)
    if total > RECORDS[level]:
        print('*** n=%d TOTAL %d (record %d)  %s'
              % (level, total, RECORDS[level], R.fmt(cfg)), flush=True)


# ------------------------------------------------------------- vertices
def qmul(p, q):
    a, b, c, d = p
    e, f, g, h = q
    return (a * e - b * f - c * g - d * h, a * f + b * e + c * h - d * g,
            a * g - b * h + c * e + d * f, a * h + b * g - c * f + d * e)


CUBE_SYMS = [q for q in (R.canon([t])[0] for t in
                         [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1)
                          for y in (-1, 0, 1) for z in (-1, 0, 1)
                          if (w, x, y, z) != (0, 0, 0, 0)
                          and w * w + x * x + y * y + z * z in (1, 2, 4)])]
CUBE_SYMS = list(dict.fromkeys(CUBE_SYMS))


def sym_canon(q):
    """Representative of q's orbit under the cube's own 24 rotations.

    INVARIANT: two cubes whose quaternions share a sym_canon are the SAME cube,
    so they must never both enter the vertex set -- a clique built from clones
    silently counts a smaller compound (the first run of this script put 4
    clones in a K4 and reported 393, a 5-cube count, for an 8-cube config)."""
    return min(R.canon([qmul(tuple(q), h)])[0] for h in CUBE_SYMS)


cands = R.menu(V_MENU, rng)
res = eng[5].count([CORE + [q] for q in cands])
scored = sorted(zip((r[0] for r in res), cands), key=lambda t: -t[0])
verts, seen = [], set()
for s, q in scored:
    if s < T_VERTEX or len(verts) >= V_KEEP:
        continue
    k = sym_canon(q)
    if k in seen:
        continue
    seen.add(k)
    verts.append(q)
print('vertices: %d of %d screened reach %d+ ; best %s'
      % (len(verts), V_MENU, T_VERTEX, [s for s, _ in scored[:8]]), flush=True)
R.log(OUT, stage='vertices', n=5, kept=len(verts),
      best=[s for s, _ in scored[:12]])

# ---------------------------------------------------------------- edges
pairs = list(itertools.combinations(range(len(verts)), 2))
res = eng[6].count([CORE + [verts[i], verts[j]] for i, j in pairs])
edges = sorted(zip((r[0] for r in res), pairs), key=lambda t: -t[0])
print('edges: %d pairs, best %s' % (len(pairs), [s for s, _ in edges[:10]]),
      flush=True)
for s, (i, j) in edges[:10]:
    report(6, CORE + [verts[i], verts[j]], s, 'edge')

# climb the best few edges on total -- the clique layer picks the seed, the
# +-2 climb refines it
for s, (i, j) in edges[:4]:
    cfg, tot = R.climb(eng[6], CORE + [verts[i], verts[j]], OUT,
                       'edge_climb', rng, restarts=2)
    print('edge climbed: %d' % tot, flush=True)
    report(6, cfg, tot, 'edge_climbed')

# ------------------------------------------------------------ triangles
deg = {}
for s, (i, j) in edges[:400]:
    deg[i] = max(deg.get(i, 0), s)
    deg[j] = max(deg.get(j, 0), s)
top = [i for i, _ in sorted(deg.items(), key=lambda t: -t[1])[:V_TRI]]
tris = list(itertools.combinations(top, 3))
res = eng[7].count([CORE + [verts[i] for i in t] for t in tris])
best = sorted(zip((r[0] for r in res), tris), key=lambda t: -t[0])
print('triangles: %d, best %s' % (len(tris), [s for s, _ in best[:10]]),
      flush=True)
for s, t in best[:6]:
    report(7, CORE + [verts[i] for i in t], s, 'triangle')

for s, t in best[:2]:
    cfg, tot = R.climb(eng[7], CORE + [verts[i] for i in t], OUT,
                       'tri_climb', rng, restarts=1)
    print('triangle climbed: %d' % tot, flush=True)
    report(7, cfg, tot, 'triangle_climbed')

# ------------------------------------------------------------------ K4s
quad_pool = sorted({i for _, t in best[:60] for i in t})[:14]
quads = list(itertools.combinations(quad_pool, 4))
res = eng[8].count([CORE + [verts[i] for i in q] for q in quads])
bq = sorted(zip((r[0] for r in res), quads), key=lambda t: -t[0])
print('K4s: %d, best %s' % (len(quads), [s for s, _ in bq[:8]]), flush=True)
for s, q in bq[:5]:
    report(8, CORE + [verts[i] for i in q], s, 'k4')
R.log(OUT, stage='done', evals={k: eng[k].evals for k in eng})
