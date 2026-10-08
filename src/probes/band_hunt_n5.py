#!/usr/bin/env python3
"""Plan item 5, step 2: hunt for bands at n = 5 (c_ℓ >= 2 at some ℓ >= 2), to test H2 of [P425].

H2 (the combined component lemma)

    (c2 − 1) + (c3 − 1) + (c4 − 1)  <=  Σ_triples (c_S − 1) + Σ_4-subsets (c'_S − 1)

is vacuous unless the full compound has a disconnected level graph above level 1. No such row was
seen in 601 ([P425]). This searches for them.

**Starts.**
- `carry`: the 8 known n = 4 bands ([P408], [P409]) with a fifth cube that nearly copies one of the
  four. The copy shifts ranks by one, so the band can reappear at level 2 or 3.
- `fifth`: the same bands with a random fifth cube.
- `random`: random compounds.

**Climb.** Greedy on (max_{ℓ>=2} c_ℓ, Σ_{ℓ>=2} c_ℓ). Moves change one coordinate of one cube by 1–3;
there is also a refinement move (double a quaternion, then step). Shared-face-plane compounds are
rejected (c_level is invalid there).

**Every hit** is measured in full by `band_n5.measure`: H1's slacks, `cslack`, and the margin
identity, against the engine's per-depth counts through the Euler gate.

**Stopping rule** (set before the run).
- A hit with `cslack < 0`, confirmed by the gate, refutes H2.
- A budget that ends with no hit leaves H2 UNTESTED at that level; it does not show H2 holds.

**Positive control.** The count of compounds with `c1 >= 2` seen along the way.

**`--min`** (the hard test): from the 8 lowest-cslack hits, climbs MINIMISE cslack while keeping a
band (c_ℓ >= 2 at some ℓ >= 2), accepting any step that does not raise it. Each step is fully
measured and gated. This is [P410]'s band_cslack test, moved to n = 5. Output:
data/band_hunt_n5_min.json; every evaluated row goes to data/band_hunt_n5_min_cache.jsonl.

**`--min4`**: where are level-4 bands paid for? From hits with c4 >= 2, climbs keep c4 >= 2 and
minimise one of:
- `four34 = Σ_4 (c'_S − 1) − (c3 − 1) − (c4 − 1)` (4-subsets pay for levels 3 and 4);
- `tri24 = Σ_tri (c_S − 1) − (c2 − 1) − (c4 − 1)` (triples pay for levels 2 and 4).
A negative value refutes that split; the combined H2 can still hold. Output:
data/band_hunt_n5_min4.json.

**`--c4`**: the one test that could fail the 457 condition of [P430]. From compounds with c4 = 2,
16 climbs maximise c4 (tie-break: minimise d4 − 2c4), using only the full level graph. That is
cheap, since no subsets are needed. Every compound reaching c4 >= 3, or d4 − 2c4 < 5, is then
measured in full and gated.
Output: data/band_hunt_n5_c4.json.

Output: data/band_hunt_n5.json.
"""
import os, sys, json, random, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from band_n5 import measure

ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, 'data')
STEPS = 600


def bands():
    out = []
    for f in ('band_hunt.json', 'band_hunt_7.json'):
        out += [h['qs'] for h in json.load(open(os.path.join(DATA, f)))['hits']]
    out.append([[1, 0, 0, 0], [16, 0, 1, -1], [43, 33, 3, 52], [81, 27, -32, -10]])  # P409
    return [[tuple(q) for q in b] for b in out]


def cs(qs):
    if CL.shares_plane(qs):
        return None
    g = CL.level_graph(qs)
    return {l: g[l]['c'] for l in g}


def score(c):
    hi = [c.get(l, 1) for l in (2, 3, 4)]
    return (max(hi), sum(hi))


def start(rnd, kind, B):
    if kind == 'random':
        return [(1, 0, 0, 0)] + [tuple(rnd.randint(-9, 9) or 1 for _ in range(4)) for _ in range(4)]
    b = B[rnd.randrange(len(B))]
    if kind == 'carry':
        k = rnd.randrange(4)
        five = tuple(3 * x + rnd.randint(-1, 1) for x in b[k])
        return b + [five]
    return b + [tuple(rnd.randint(-9, 9) or 1 for _ in range(4))]


def move(rnd, qs):
    qs = [list(q) for q in qs]
    i = rnd.randrange(len(qs))
    if rnd.random() < 0.1:
        qs[i] = [2 * x for x in qs[i]]
    qs[i][rnd.randrange(4)] += rnd.choice((-3, -2, -1, 1, 2, 3))
    if not any(qs[i]):
        qs[i][0] = 1
    return [tuple(q) for q in qs]


def run(args):
    kind, seed = args
    rnd = random.Random(seed)
    B = bands()
    cur = start(rnd, kind, B)
    c = cs(cur)
    while c is None:
        cur = move(rnd, cur)
        c = cs(cur)
    hits, log, lvl1 = [], [], 0
    for _ in range(STEPS):
        nxt = move(rnd, cur)
        nc = cs(nxt)
        if nc is None:
            continue
        lvl1 += nc.get(1, 1) >= 2
        log.append((nxt, nc))
        if score(nc)[0] >= 2:
            hits.append(nxt)
        if score(nc) >= score(c):
            cur, c = nxt, nc
    return {'kind': kind, 'seed': seed, 'best': cur, 'best_c': c, 'evaluated': len(log),
            'level1_hits': lvl1, 'hits': [list(map(list, h)) for h in hits]}


def main():
    jobs = [(k, s) for k in ('carry', 'fifth', 'random') for s in range(8)]
    res = []
    with mp.Pool(8) as p:
        for r in p.imap_unordered(run, jobs):
            print('%-6s seed %d  evaluated %d  best c %s  band hits %d  level-1 c>=2 %d'
                  % (r['kind'], r['seed'], r['evaluated'], r['best_c'], len(r['hits']), r['level1_hits']), flush=True)
            res.append(r)
    uniq = {}
    for r in res:
        for h in r['hits']:
            uniq.setdefault(json.dumps(h), h)
    print('distinct band hits: %d' % len(uniq), flush=True)
    todo = list(uniq.values())[:400]
    jobs2 = [(h, {k: v for k, v in CL.engine([tuple(q) for q in h])['by_depth'].items()}) for h in todo]
    with mp.Pool(8) as p:
        ms = p.map(measure, jobs2)
    ms = [m for m in ms if 'excluded' not in m]
    gated = [m for m in ms if m['gate']]
    print('measured %d (cap 400), gate-void %d' % (len(ms), len(ms) - len(gated)))
    for key in ('cslack', 'slack2', 'slack3'):
        print('  %-7s histogram %s' % (key, sorted(collections.Counter(m[key] for m in gated).items())))
    print('  margin identity holds: %d of %d' % (sum(m['margin_ok'] for m in gated), len(gated)))
    print('  levels carrying the band: %s' % sorted(collections.Counter(
        tuple(l for l in (2, 3, 4) if m['c'][l] >= 2) for m in gated).items()))
    viol = [m for m in gated if m['cslack'] < 0]
    print('  H2 violations (cslack < 0): %d' % len(viol))
    json.dump({'runs': res, 'measured': gated, 'violations': viol, 'void': len(ms) - len(gated),
               'distinct_hits': len(uniq)},
              open(os.path.join(DATA, 'band_hunt_n5.json'), 'w'), indent=1, default=str)


def measured(qs):
    if CL.shares_plane(qs):
        return None
    try:
        bd = CL.engine(qs)['by_depth']
    except Exception:
        return None
    m = measure((qs, bd))
    return m if 'excluded' not in m and m['gate'] else None


def has_band(m):
    return any(m['c'][l] >= 2 for l in (2, 3, 4))


def run_min(args):
    start_qs, seed = args
    rnd = random.Random(seed)
    cur = [tuple(q) for q in start_qs]
    m = measured(cur)
    log = []
    for _ in range(250):
        nxt = move(rnd, cur)
        nm = measured(nxt)
        if nm is None:
            continue
        log.append({'qs': nxt, 'cslack': nm['cslack'], 'slack2': nm['slack2'], 'slack3': nm['slack3'],
                    'c': nm['c'], 'margin_ok': nm['margin_ok'], 'band': has_band(nm)})
        if has_band(nm) and nm['cslack'] <= m['cslack']:
            cur, m = nxt, nm
    return {'seed': seed, 'end': cur, 'end_cslack': m['cslack'], 'end_c': m['c'], 'log': log}


def main_min():
    d = json.load(open(os.path.join(DATA, 'band_hunt_n5.json')))
    starts = [m['qs'] for m in sorted(d['measured'], key=lambda m: m['cslack'])[:8]]
    with mp.Pool(8) as p:
        res = p.map(run_min, [(q, 500 + i) for i, q in enumerate(starts)])
    allrows = [r for x in res for r in x['log']]
    with open(os.path.join(DATA, 'band_hunt_n5_min_cache.jsonl'), 'w') as f:
        for r in allrows:
            f.write(json.dumps(r, default=str) + '\n')
    band = [r for r in allrows if r['band']]
    print('evaluated %d, with a band %d, margin identity holds on %d'
          % (len(allrows), len(band), sum(r['margin_ok'] for r in allrows)))
    print('cslack over band rows: %s' % sorted(collections.Counter(r['cslack'] for r in band).items()))
    print('slack2+slack3 over all rows: %s' % sorted(collections.Counter(r['slack2'] + r['slack3'] for r in allrows).items()))
    print('max c at levels 2-4 among band rows: %s' % max(max(r['c'][l] for l in (2, 3, 4)) for r in band))
    for x in res:
        print('  run %d: end cslack %d, c %s' % (x['seed'], x['end_cslack'], x['end_c']))
    json.dump({'runs': [{k: v for k, v in x.items() if k != 'log'} for x in res], 'evaluated': len(allrows),
               'band_rows': len(band), 'min_cslack': min(r['cslack'] for r in band),
               'violations_H2': [r for r in band if r['cslack'] < 0],
               'violations_H1': [r for r in allrows if r['slack2'] + r['slack3'] < 0]},
              open(os.path.join(DATA, 'band_hunt_n5_min.json'), 'w'), indent=1, default=str)


def splits(m):
    st = sum(x - 1 for x in m['tri_c'])
    sf = sum(x - 1 for x in m['four_c'])
    return {'four34': sf - (m['c'][3] - 1) - (m['c'][4] - 1), 'tri24': st - (m['c'][2] - 1) - (m['c'][4] - 1),
            'cslack': m['cslack']}


def run_min4(args):
    start_qs, seed, obj = args
    rnd = random.Random(seed)
    cur = [tuple(q) for q in start_qs]
    m = measured(cur)
    log = []
    for _ in range(200):
        nxt = move(rnd, cur)
        nm = measured(nxt)
        if nm is None:
            continue
        sp = splits(nm)
        log.append({'qs': nxt, 'c': nm['c'], **sp})
        if nm['c'][4] >= 2 and sp[obj] <= splits(m)[obj]:
            cur, m = nxt, nm
    return {'seed': seed, 'obj': obj, 'end': splits(m), 'end_c': m['c'], 'log': log}


def main_min4():
    d = json.load(open(os.path.join(DATA, 'band_hunt_n5.json')))
    for m in d['measured']:
        m['c'] = {int(k): v for k, v in m['c'].items()}
    c4 = [m for m in d['measured'] if m['c'][4] >= 2]
    starts = [m['qs'] for m in sorted(c4, key=lambda m: splits(m)['four34'])[:4]]
    jobs = [(q, 900 + i, obj) for obj in ('four34', 'tri24') for i, q in enumerate(starts)]
    with mp.Pool(8) as p:
        res = p.map(run_min4, jobs)
    for obj in ('four34', 'tri24'):
        rows = [r for x in res if x['obj'] == obj for r in x['log'] if r['c'][4] >= 2]
        print('%s: %d rows with c4 >= 2; histogram of four34 %s; tri24 %s; cslack %s' % (
            obj, len(rows), sorted(collections.Counter(r['four34'] for r in rows).items()),
            sorted(collections.Counter(r['tri24'] for r in rows).items()),
            sorted(collections.Counter(r['cslack'] for r in rows).items())))
    json.dump({'runs': [{k: v for k, v in x.items() if k != 'log'} for x in res],
               'rows': [r for x in res for r in x['log']]},
              open(os.path.join(DATA, 'band_hunt_n5_min4.json'), 'w'), indent=1, default=str)


def c4_score(qs):
    if CL.shares_plane(qs):
        return None
    g = CL.level_graph(qs)
    if 4 not in g:
        return None
    d4 = g[4]['E'] - g[4]['V'] + g[4]['c'] + 1
    return {'c4': g[4]['c'], 'd4': d4, 'c': {l: g[l]['c'] for l in g}}


def run_c4(args):
    start_qs, seed = args
    rnd = random.Random(seed)
    cur = [tuple(q) for q in start_qs]
    m = c4_score(cur)
    log = []
    for _ in range(STEPS):
        nxt = move(rnd, cur)
        nm = c4_score(nxt)
        if nm is None:
            continue
        log.append({'qs': nxt, **nm})
        key = lambda x: (x['c4'], -(x['d4'] - 2 * x['c4']))
        if key(nm) >= key(m):
            cur, m = nxt, nm
    return {'seed': seed, 'end': cur, 'end_score': m, 'log': log}


def main_c4():
    d = json.load(open(os.path.join(DATA, 'band_hunt_n5_min4.json')))
    starts = []
    for r in d['rows']:
        c = {int(k): v for k, v in r['c'].items()}
        if c[4] >= 2:
            starts.append(r['qs'])
    rnd = random.Random(44)
    starts = rnd.sample(starts, min(16, len(starts)))
    with mp.Pool(8) as p:
        res = p.map(run_c4, [(q, 4400 + i) for i, q in enumerate(starts)])
    rows = [r for x in res for r in x['log']]
    print('evaluated %d; c4 histogram %s' % (len(rows), sorted(collections.Counter(r['c4'] for r in rows).items())))
    print('min d4 - 2c4 by c4: %s' % {c: min(r['d4'] - 2 * r['c4'] for r in rows if r['c4'] == c)
                                      for c in sorted({r['c4'] for r in rows})})
    hard = list({json.dumps(r['qs']): r['qs'] for r in rows if r['c4'] >= 3 or r['d4'] - 2 * r['c4'] < 5}.values())[:200]
    full = []
    if hard:
        jobs = [(q, CL.engine([tuple(x) for x in q])['by_depth']) for q in hard]
        with mp.Pool(8) as p:
            full = [m for m in p.map(measure, jobs) if 'excluded' not in m and m['gate']]
        print('hard cases measured and gated: %d; min L2 slack %s, min L3 slack %s, min d4-2c4 %s' % (
            len(full), min((sum(x - 1 for x in m['tri_c']) - (m['c'][2] - 1)) for m in full),
            min((sum(x - 1 for x in m['four_c']) - (m['c'][3] - 1)) for m in full),
            min(m['bd']['4'] - 2 * m['c'][4] for m in full)))
    else:
        print('no compound reached c4 >= 3 or d4 - 2c4 < 5')
    json.dump({'runs': [{k: v for k, v in x.items() if k != 'log'} for x in res], 'evaluated': len(rows),
               'c4_hist': dict(collections.Counter(r['c4'] for r in rows)), 'hard_measured': full},
              open(os.path.join(DATA, 'band_hunt_n5_c4.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    if '--c4' in sys.argv:
        main_c4()
    elif '--min4' in sys.argv:
        main_min4()
    elif '--min' in sys.argv:
        main_min()
    else:
        main()
