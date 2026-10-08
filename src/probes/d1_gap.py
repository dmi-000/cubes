#!/usr/bin/env python3
"""The top of the d1 envelope at n = 4, recounted exactly, with per-cube splits.  [plan item 4]

frontier_n4 found only two Pareto points over (d1, d2, d3): the record (92, 66, 24) and the
golden (104, 48, 24). Nothing on file has d1 between 97 and 103. If that gap is real, then
d1 >= 97 would have to mean the golden's complete sharing (total 177), and everything else would
have d1 <= 96, so total <= 96 + 66 + 24 + 1 = 187.

**Step 1, re-verify.** The census mixes engines, and the c_level engine is frame-dependent in d1
on shared-face-plane compounds ([P419]). Here the highest-d1 configurations on file are recounted
with sphere_count, which is frame-free.

**Step 2, localise.** d1 is the sum of four per-cube counts `#D({i})`, each at most 26 ([P401]).
Per-cube d1, per-pair d2 and the sharing (shared face planes, shared body diagonals) are recorded
for each, so it can be read what a cube at 25 or 26 forces.

**`--campaign`**: the same per-cube split on the 200 000 random rows of campaign_n4.jsonl, from the
c_level engine's per-label counts (the single-bit labels; gated: they must sum to d1 on every
row). Random compounds share nothing, so this shows only the a_i = 0 envelope far from any cap.
Output: data/d1_gap_campaign.json.

**`--extra`**: two checks cited by [P423].
- Every cached top row is classified by ALL axis coincidences between cubes: face axes (3),
  body diagonals (4) and 2-fold axes (6), across every type pair, with multiplicity.
- The no-sharing compound with `d1 = 82` that the climbs found is recounted exactly.
- The compounds refuting the per-cube form (data/d1_cap_climb.json, sphere_count-confirmed) are
  classified the same way, with the excess of each cube over 20 + 2 a_i.
Output: data/d1_gap_extra.json.

Cache: data/d1_gap_cache.jsonl (keyed by config). Output: data/d1_gap.json.
"""
import os, sys, json, itertools, collections, multiprocessing as mp
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from frontier_n4 import vectors, DATA
from sphere_count import Compound, normals
from kfield import K

TOP = 60
CACHE = os.path.join(DATA, 'd1_gap_cache.jsonl')


def norm_cfg(c):
    if isinstance(c, str):
        try:
            c = [tuple(map(int, g.split(','))) for g in c.split(';')]
        except ValueError:
            return None
    if not isinstance(c, list) or len(c) != 4:
        return None
    try:
        qs = tuple(tuple(int(x) for x in q) for q in c)
    except (TypeError, ValueError):
        return None
    return qs if all(len(q) == 4 and any(q) for q in qs) else None


def sharing(qs, one):
    """shared face planes and shared body diagonals, as lists of cube-index pairs"""
    nv = [normals(q, one) for q in qs]
    def par(u, v):
        return all(a == b for a, b in zip(u, v)) or all(a == -b for a, b in zip(u, v))
    def diags(vs):
        return [tuple(s0 * vs[0][i] + s1 * vs[1][i] + s2 * vs[2][i] for i in range(3))
                for s0, s1, s2 in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))]
    planes, axes = [], []
    for i, j in itertools.combinations(range(4), 2):
        planes += [(i, j)] * sum(par(u, v) for u in nv[i] for v in nv[j])
        axes += [(i, j)] * sum(par(u, v) for u in diags(nv[i]) for v in diags(nv[j]))
    return planes, axes


def measure(qs, field='Q'):
    C = Compound(list(qs), field)
    idx = range(4)
    per_cube = [C.components(C.beat_pieces([i], [b for b in idx if b != i])) for i in idx]
    per_pair = {'%d%d' % P: C.components(C.beat_pieces(list(P), [b for b in idx if b not in P]))
                for P in itertools.combinations(idx, 2)}
    tot, bd = C.count()
    assert bd[1] == sum(per_cube) and bd[2] == sum(per_pair.values())
    one = K(1) if field == 'K' else F(1)
    planes, axes = sharing(qs, one)
    return {'total': tot, 'bd': bd, 'per_cube': per_cube, 'per_pair': per_pair,
            'shared_planes': planes, 'shared_axes': axes}


def job(qs):
    return list(qs), measure(qs)


def main():
    best = {}
    for name in sorted(os.listdir(DATA)):
        if not name.endswith(('.json', '.jsonl')) or name.startswith(('frontier_n4', 'd1_gap')):
            continue
        f = os.path.join(DATA, name)
        try:
            recs = ([json.loads(l) for l in open(f) if l.strip()] if name.endswith('.jsonl')
                    else [json.load(open(f))])
        except (ValueError, UnicodeDecodeError):
            continue
        for r in recs:
            for d, rec in vectors(r):
                for k in ('quats', 'cfg', 'qs', 'k', 'q'):
                    if k in rec:
                        qs = norm_cfg(rec[k])
                        if qs and d[1] > best.get(qs, (-1,))[0]:
                            best[qs] = (d[1], d[2], d[3], name)
                        break
    ranked = sorted(best, key=lambda q: -best[q][0])[:TOP]
    print('configs on file: %d; recounting the top %d by d1 (on file %d..%d)'
          % (len(best), len(ranked), best[ranked[0]][0], best[ranked[-1]][0]), flush=True)
    done = {}
    if os.path.exists(CACHE):
        for l in open(CACHE):
            r = json.loads(l)
            done[tuple(map(tuple, r['qs']))] = r['m']
    todo = [q for q in ranked if q not in done]
    with mp.Pool(8) as p, open(CACHE, 'a') as fc:
        for qs, m in p.imap_unordered(job, todo):
            m['bd'] = {str(k): v for k, v in m['bd'].items()}
            done[tuple(map(tuple, qs))] = m
            fc.write(json.dumps({'qs': qs, 'm': m}) + '\n'); fc.flush()
    rows = []
    moved = 0
    for q in ranked:
        m = done[q]
        f1, f2, f3, src = best[q]
        mv = (m['bd']['1'], m['bd']['2'], m['bd']['3']) != (f1, f2, f3)
        moved += mv
        rows.append({'qs': q, 'file': src, 'on_file': [f1, f2, f3], **m, 'moved': mv})
    rows.sort(key=lambda r: -r['bd']['1'])
    for r in rows[:25]:
        print('d1 %3d (file %3d%s)  d2 %2d  d3 %2d  total %3d  per-cube %s  planes %d axes %d  %s'
              % (r['bd']['1'], r['on_file'][0], ' MOVED' if r['moved'] else '', r['bd']['2'],
                 r['bd']['3'], r['total'], r['per_cube'], len(r['shared_planes']),
                 len(r['shared_axes']), r['file']))
    print('rows whose recount differs from the file: %d of %d' % (moved, len(rows)))
    # the golden, in Q(sqrt5)
    R5 = K(0, 0, 1, 0)
    golden = [(R5, K(1), K(1), K(1)), (R5, K(1), K(-1), K(-1)), (R5, K(-1), K(1), K(-1)),
              (R5, K(-1), K(-1), K(1))]
    g = measure(golden, 'K')
    g['bd'] = {str(k): v for k, v in g['bd'].items()}
    print('golden: total %d  bd %s  per-cube %s  per-pair %s  planes %d axes %d'
          % (g['total'], g['bd'], g['per_cube'], g['per_pair'], len(g['shared_planes']),
             len(g['shared_axes'])))
    json.dump({'top': TOP, 'rows': rows, 'moved': moved, 'golden': g},
              open(os.path.join(DATA, 'd1_gap.json'), 'w'), indent=1, default=str)


def campaign():
    mx = collections.defaultdict(int)
    n = collections.Counter()
    rows = bad = 0
    for l in open(os.path.join(DATA, 'campaign_n4.jsonl')):
        r = json.loads(l)
        rows += 1
        pc = [r['per_label'].get(str(1 << i), 0) for i in range(4)]
        if sum(pc) != r['by_depth']['1']:
            bad += 1
            continue
        planes, axes = sharing(r['quats'], F(1))
        a = collections.Counter(x for P in axes for x in P)
        for i in range(4):
            key = '%d axes, %s' % (a[i], 'shares a plane' if any(i in P for P in planes) else 'no plane')
            mx[key] = max(mx[key], pc[i])
            n[key] += 1
    print('rows %d, per-label gate failures %d' % (rows, bad))
    for k in sorted(mx):
        print('  %-26s cubes %7d  max per-cube d1 %d' % (k, n[k], mx[k]))
    json.dump({'rows': rows, 'gate_failures': bad, 'max_per_cube': mx, 'cubes': n},
              open(os.path.join(DATA, 'd1_gap_campaign.json'), 'w'), indent=1)


def axes_of(q):
    f = normals(q, F(1))
    body = [tuple(s0 * f[0][i] + s1 * f[1][i] + s2 * f[2][i] for i in range(3))
            for s0, s1, s2 in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))]
    two = [tuple(f[a][i] + sg * f[b][i] for i in range(3)) for a, b in ((0, 1), (0, 2), (1, 2)) for sg in (1, -1)]
    return {'face': f, 'body': body, 'two': two}


def coincidences(qs):
    def par(u, v):
        return all(a == b for a, b in zip(u, v)) or all(a == -b for a, b in zip(u, v))
    A = [axes_of(q) for q in qs]
    out = []
    for i, j in itertools.combinations(range(4), 2):
        for t1 in A[i]:
            for t2 in A[j]:
                k = sum(par(u, v) for u in A[i][t1] for v in A[j][t2])
                if k:
                    out.append([i, j, t1, t2, k])
    return out


NOSHARE82 = ((13, 4, -4, 2), (3, 1, 7, 3), (15, 0, -10, -10), (-3, 3, 3, 3))


def extra():
    kinds = collections.Counter()
    for l in open(CACHE):
        r = json.loads(l)
        sig = tuple(sorted((t1, t2, k) for i, j, t1, t2, k in coincidences(r['qs'])))
        kinds[(r['m']['bd']['1'], sig)] += 1
    print('coincidence types among the %d cached top rows:' % sum(kinds.values()))
    for (d1, sig), c in sorted(kinds.items(), reverse=True):
        print('  d1 %d  rows %d  %s' % (d1, c, list(sig)))
    m = measure(NOSHARE82)
    m['bd'] = {str(k): v for k, v in m['bd'].items()}
    m['coincidences'] = coincidences(NOSHARE82)
    print('no-sharing 82: %s' % m)
    assert m['bd']['1'] == 82 and not m['shared_axes'] and not m['shared_planes']
    ref = json.load(open(os.path.join(DATA, 'd1_cap_climb.json')))['refuting_sphere']
    rk = collections.Counter()
    for k in ref:
        qs = [tuple(map(int, g.split(','))) for g in k.split(';')]
        rk[tuple(sorted((t1, t2, c) for i, j, t1, t2, c in coincidences(qs)))] += 1
    print('per-cube refuters (%d), coincidence types:' % len(ref))
    for sig, c in rk.most_common():
        print('  %3d  %s' % (c, list(sig)))
    json.dump({'top_row_coincidences': [[d1, list(sig), c] for (d1, sig), c in kinds.items()],
               'noshare82': {'qs': NOSHARE82, **m},
               'per_cube_refuters': [[list(sig), c] for sig, c in rk.items()]},
              open(os.path.join(DATA, 'd1_gap_extra.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    if '--campaign' in sys.argv:
        campaign()
    elif '--extra' in sys.argv:
        extra()
    else:
        main()
