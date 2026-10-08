#!/usr/bin/env python3
"""Plan item 5, step 1: what a band lemma at n = 5 would have to say.  The subset identities.

At n = 4 the band lemma closes `d2 <= Σ_S d2(S) − 6` because every triple point there has at most
one other cube containing it, so every triple point lies on Γ2. At n = 5 a triple point can lie
inside both other cubes. A triple sees it at its own level 2, while the full compound puts it at
levels 3 and 4. On three random rows (X_ℓ = E − V of the level-ℓ graph):

    Σ_{triples S} X_S(2)   =  X2 + X4
    Σ_{4-subsets S} X_S(3) =  X3 + X4

If these hold as INEQUALITIES (≤ read from right to left, as the n = 4 charging does) on
degenerate compounds too, the n = 5 chain bounds d2 + d4 (and d3 + d4), not d2 alone. With
d2(S) <= 18 it lands on C(5,2) + C(5,4) = 134 + 30. That chain needs the component lemma in the form

    (c2 − 1) + (c4 − 1)  <=  Σ_triples (c_S − 1),   and   (c3 − 1) + (c4 − 1) <= Σ_4-subsets (c_S − 1).

This probe measures the two identities' slack and the component terms.

**The chain for the total.** Add the two identities and use the proved caps d1 <= 180,
d2(S) <= 18 (ANCHOR) and d3(S) <= 24 ([P401], top level at n = 4). Then, exactly:

    457 − total = (180 − d1) + (1 − d5) + X4 + slack2 + slack3
                  + Σ_tri (18 − d2(S)) + Σ_4 (24 − d3(S)) + cslack

    cslack = Σ_tri (c_S − 1) + Σ_4 (c'_S − 1) − [(c2 − 1) + (c3 − 1) + (c4 − 1)]

Every term is checked on every row (`margin_ok`). So `max(5) <= 457` would follow from
slack2 + slack3 >= 0, cslack >= 0, and X4 >= 0.

**Rows.**
- 300 random rows of campaign_n5.
- The 300 highest totals in hillclimb_n5_log, which are near-record. As far as these identities
  can see they are generic: their slack is 0, like the random rows.
- The 393 record base.

**Gate.** The full compound's `E − V + c + 1` must equal the engine's `d_ℓ` at every level
(P403's gate). Rows that fail are void.

**Excluded.** Shared-face-plane compounds are rejected and counted; c_level is invalid there
([P246]).

**What this cannot do.** Random rows have `c = 1` everywhere, so the component inequality is
vacuous on them. Informative rows (`c_ℓ >= 2` at ℓ >= 2) are counted separately. The positive
control is the level-1 `c > 1` count, which must be nonzero on the same rows.

**`--degenerate`** (H1's hard cases): n = 5 compounds on coincidence loci.
- The 183 record plus a random fifth cube, and plus the fifth cube of the 393 base moved slightly.
- The 96 four-cycle of [P423] plus a random cube.
- n = 4 compounds from [P423]'s climbs that share a body diagonal or a 2-fold axis, plus a random
  cube.
Only `slack2 + slack3 >= 0` matters for H1. Output: data/band_n5_degenerate.json.

**`--subset-gate`**: every subset count behind H1 and H2 checked against the engine. For each
row, the level-graph `X_S + c_S + 1` must equal the engine's `d2` of each triple and `d3` of each
4-subset. The rows are all evidence rows of [P425]/[P426]. Rows that fail are void.
It also checks `X1 − X2 + X3 − X4 = 0`, the alternating sum that the triple-point vertex model
predicts in general position, and logs it beside H1's slack.
Output: data/band_n5_subset_gate.json.

(The margin identity checked in `measure` is algebra once the full-compound gate passes: every
subset term cancels. It is a bookkeeping check, not evidence.)

**`--split`**: H2 split by level on the band rows of the cslack-minimising climb
(data/band_hunt_n5_min_cache.jsonl, rows with a band and cslack <= 3). It records
Σ_tri (c_S − 1) − (c2 − 1), Σ_4 (c'_S − 1) − (c3 − 1), and the level-4 term c4 − 1, to find which
per-level statement is tight and where the level-4 components are paid for.
Output: data/band_n5_split.json.

**`--h2-controls`**: the controls for [P430]. On every evidence row (the identities, degenerate,
band-hit and min-climb rows of [P426], and the level-4 climb rows of [P429]), measured and gated
afresh, it reports:
- L2 slack `Σ_tri (c_S − 1) − (c2 − 1)`;
- L3 slack `Σ_4 (c'_S − 1) − (c3 − 1)`;
- `d4 − 2 c4`, the quantity behind 457 versus 485.
Output: data/band_n5_h2_controls.json.

Output: data/band_n5.json.
"""
import os, sys, json, itertools, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL

ROOT = os.path.dirname(os.path.dirname(HERE))
BASE393 = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]


def X(g, l):
    return g[l]['E'] - g[l]['V'] if l in g else 0


def C(g, l):
    return g[l]['c'] if l in g else 1


def measure(args):
    qs, bd = args
    qs = [tuple(q) for q in qs]
    if CL.shares_plane(qs):
        return {'excluded': 'shared plane'}
    full = CL.level_graph(qs)
    gate = all(full[l]['E'] - full[l]['V'] + full[l]['c'] + 1 == bd[str(l)] for l in full)
    tri = [CL.level_graph([qs[i] for i in S]) for S in itertools.combinations(range(5), 3)]
    four = [CL.level_graph([qs[i] for i in S]) for S in itertools.combinations(range(5), 4)]
    slack2 = sum(X(g, 2) for g in tri) - (X(full, 2) + X(full, 4))
    slack3 = sum(X(g, 3) for g in four) - (X(full, 3) + X(full, 4))
    cslack = (sum(C(g, 2) - 1 for g in tri) + sum(C(g, 3) - 1 for g in four)
              - sum(C(full, l) - 1 for l in (2, 3, 4)))
    tri_d2 = [X(g, 2) + C(g, 2) + 1 for g in tri]
    four_d3 = [X(g, 3) + C(g, 3) + 1 for g in four]
    total = sum(bd[str(l)] for l in range(1, 6))
    terms = {'d1': 180 - bd['1'], 'd5': 1 - bd['5'], 'X4': X(full, 4), 'slack2': slack2, 'slack3': slack3,
             'anchor_tri': sum(18 - d for d in tri_d2), 'top_four': sum(24 - d for d in four_d3),
             'cslack': cslack}
    return {
        'qs': qs, 'gate': gate, 'bd': bd, 'total': total,
        'X': {l: X(full, l) for l in range(1, 5)}, 'c': {l: C(full, l) for l in range(1, 5)},
        'slack2': slack2, 'slack3': slack3, 'cslack': cslack,
        'cslack2': sum(C(g, 2) - 1 for g in tri) - ((C(full, 2) - 1) + (C(full, 4) - 1)),
        'cslack3': sum(C(g, 3) - 1 for g in four) - ((C(full, 3) - 1) + (C(full, 4) - 1)),
        'tri_c': [C(g, 2) for g in tri], 'four_c': [C(g, 3) for g in four],
        'tri_d2': tri_d2, 'four_d3': four_d3, 'terms': terms,
        'margin_ok': 457 - total == sum(terms.values()),
    }


def main():
    jobs = []
    for l, _ in zip(open(os.path.join(ROOT, 'data', 'campaign_n5.jsonl')), range(300)):
        r = json.loads(l)
        jobs.append((r['quats'], r['by_depth']))
    hc = {}
    for l in open(os.path.join(ROOT, 'data', 'hillclimb_n5_log.jsonl')):
        try:
            r = json.loads(l)
        except ValueError:
            continue
        if 'by_depth' in r:
            hc.setdefault(json.dumps(r['quats']), (r['bounded'], r['by_depth']))
    for k in sorted(hc, key=lambda k: -hc[k][0])[:300]:
        jobs.append((json.loads(k), hc[k][1]))
    e = CL.engine(BASE393)
    jobs.append((BASE393, e['by_depth']))
    with mp.Pool(8) as p:
        res = p.map(measure, jobs)
    excl = sum('excluded' in r for r in res)
    res = [r for r in res if 'excluded' not in r]
    void = sum(not r['gate'] for r in res)
    ok = [r for r in res if r['gate']]
    print('rows %d: %d shared-plane excluded, %d void by the Euler gate, %d evaluated' % (len(jobs), excl, void, len(ok)))
    print('  margin identity 457 - total = sum of terms: %d of %d rows' % (sum(r['margin_ok'] for r in ok), len(ok)))
    print('  max d2(S) over triples %d (cap 18), max d3(S) over 4-subsets %d (cap 24)'
          % (max(max(r['tri_d2']) for r in ok), max(max(r['four_d3']) for r in ok)))
    for key in ('slack2', 'slack3', 'cslack', 'cslack2', 'cslack3'):
        print('  %-8s histogram %s' % (key, sorted(collections.Counter(r[key] for r in ok).items())))
    lvl1 = sum(r['c'][1] > 1 for r in ok)
    informative = [r for r in ok if any(r['c'][l] >= 2 for l in (2, 3, 4))]
    print('  positive control: rows with c1 > 1: %d' % lvl1)
    print('  informative rows (c_l >= 2 at some l >= 2): %d' % len(informative))
    print('  rows with a disconnected subset diagram: triples %d, 4-subsets %d'
          % (sum(max(r['tri_c']) > 1 for r in ok), sum(max(r['four_c']) > 1 for r in ok)))
    r393 = ok[-1] if ok and ok[-1]['qs'] == BASE393 else None
    print('  393 base: total %s, terms %s' % ((r393['total'], r393['terms']) if r393 else ('excluded or void', '')))
    json.dump({'rows': ok, 'excluded': excl, 'void': void, 'level1_c_gt1': lvl1,
               'informative': len(informative)},
              open(os.path.join(ROOT, 'data', 'band_n5.json'), 'w'), indent=1, default=str)


def degenerate():
    import random
    sys.path.insert(0, HERE)
    from d1_gap import coincidences
    rnd = random.Random(55)
    rec = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (1, 1, 1, 1)]
    cyc = [(1, 0, 0, 0), (1, 3, 0, 2), (4, -9, 0, -6), (5, 3, 0, 2)]
    rq = lambda: tuple(rnd.randint(-9, 9) or 1 for _ in range(4))
    cfgs = [('record+random', rec + [rq()]) for _ in range(40)]
    cfgs += [('record+near393', rec[:3] + [tuple(x + rnd.randint(-1, 1) for x in (2, 1, 1, 1)), rec[3]]) for _ in range(20)]
    cfgs += [('cycle4+random', cyc + [rq()]) for _ in range(40)]
    shared = []
    for l in open(os.path.join(ROOT, 'data', 'd1_cap_climb_cache.jsonl')):
        r = json.loads(l)
        if sum(r['m']['a']) >= 2:
            shared.append([tuple(map(int, g.split(','))) for g in r['k'].split(';')])
    rnd.shuffle(shared)
    pick = []
    for qs in shared:
        if coincidences(qs):
            pick.append(qs)
        if len(pick) >= 60:
            break
    cfgs += [('sharing+random', qs + [rq()]) for qs in pick]
    jobs, kinds, failed = [], [], 0
    for kind, qs in cfgs:
        try:
            jobs.append((qs, CL.engine(qs)['by_depth']))
            kinds.append(kind)
        except Exception:
            failed += 1
    print('engine failures (unevaluated): %d' % failed)
    with mp.Pool(8) as p:
        res = p.map(measure, jobs)
    excl = sum('excluded' in r for r in res)
    ok = [(k, r) for k, r in zip(kinds, res) if 'excluded' not in r and r['gate']]
    void = len(res) - excl - len(ok)
    print('rows %d: %d shared-plane excluded, %d void by the gate, %d evaluated' % (len(res), excl, void, len(ok)))
    print('margin identity holds: %d of %d' % (sum(r['margin_ok'] for _, r in ok), len(ok)))
    for kind in dict.fromkeys(kinds):
        h = collections.Counter(r['slack2'] + r['slack3'] for k, r in ok if k == kind)
        print('  %-15s slack2+slack3 histogram %s' % (kind, sorted(h.items())))
    neg = [r for _, r in ok if r['slack2'] + r['slack3'] < 0]
    print('H1 violations: %d; degenerate rows (slack > 0): %d' % (len(neg), sum(r['slack2'] + r['slack3'] > 0 for _, r in ok)))
    json.dump({'rows': [dict(r, kind=k) for k, r in ok], 'excluded': excl, 'void': void, 'violations': neg},
              open(os.path.join(ROOT, 'data', 'band_n5_degenerate.json'), 'w'), indent=1, default=str)


def subset_gate_row(args):
    src, qs = args
    qs = [tuple(q) for q in qs]
    bad, unev = [], []
    for k, l in ((3, 2), (4, 3)):
        for S in itertools.combinations(range(5), k):
            sub = [qs[i] for i in S]
            g = CL.level_graph(sub)
            e = CL.engine(sub)
            if 'by_depth' not in e:
                unev.append([S, str(e)[:120]])
                continue
            if X(g, l) + C(g, l) + 1 != e['by_depth'][str(l)]:
                bad.append(S)
    full = CL.level_graph(qs)
    alt = X(full, 1) - X(full, 2) + X(full, 3) - X(full, 4)
    return {'src': src, 'qs': qs, 'bad_subsets': bad, 'unevaluated_subsets': unev, 'alt': alt}


def subset_gate():
    rows = []
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_n5.json')))['rows']:
        rows.append(('identities', r['qs'], r['slack2'] + r['slack3']))
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_n5_degenerate.json')))['rows']:
        rows.append(('degenerate', r['qs'], r['slack2'] + r['slack3']))
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_hunt_n5.json')))['measured']:
        rows.append(('band_hits', r['qs'], r['slack2'] + r['slack3']))
    for l in open(os.path.join(ROOT, 'data', 'band_hunt_n5_min_cache.jsonl')):
        r = json.loads(l)
        if r['band'] or r['slack2'] + r['slack3'] > 0:
            rows.append(('min_climb', r['qs'], r['slack2'] + r['slack3']))
    with mp.Pool(8) as p:
        res = p.map(subset_gate_row, [(src, qs) for src, qs, _ in rows])
    by = collections.defaultdict(lambda: [0, 0, 0])
    alt = collections.defaultdict(collections.Counter)
    for (src, _, sl), r in zip(rows, res):
        by[src][0] += 1
        by[src][1] += bool(r['bad_subsets'])
        by[src][2] += bool(r['unevaluated_subsets'])
        alt[(src, 'generic' if sl == 0 else 'degenerate')][r['alt']] += 1
        r['h1_slack'] = sl
    for src, (n, b, u) in by.items():
        print('%-11s rows %4d  void by the subset gate %d  unevaluated (engine refused a subset) %d' % (src, n, b, u))
    errs = collections.Counter(x[1][:60] for r in res for x in r['unevaluated_subsets'])
    print('  engine refusals: %s' % dict(errs))
    for k in sorted(alt):
        print('  X1-X2+X3-X4 on %-26s %s' % (k, sorted(alt[k].items())))
    json.dump({'rows': res}, open(os.path.join(ROOT, 'data', 'band_n5_subset_gate.json'), 'w'), indent=1, default=str)


def split():
    rows = []
    for l in open(os.path.join(ROOT, 'data', 'band_hunt_n5_min_cache.jsonl')):
        r = json.loads(l)
        if r['band'] and r['cslack'] <= 3:
            rows.append(r['qs'])
    rows = list({json.dumps(q): q for q in rows}.values())
    jobs = [(q, CL.engine([tuple(x) for x in q])['by_depth']) for q in rows]
    with mp.Pool(8) as p:
        ms = [m for m in p.map(measure, jobs) if 'excluded' not in m and m['gate']]
    out = collections.Counter()
    for m in ms:
        a = sum(x - 1 for x in m['tri_c']) - (m['c'][2] - 1)
        b = sum(x - 1 for x in m['four_c']) - (m['c'][3] - 1)
        out[(a, b, m['c'][4] - 1, m['cslack'])] += 1
    print('distinct rows %d, measured and gated %d' % (len(rows), len(ms)))
    print('(tri − (c2−1), four − (c3−1), c4 − 1, cslack): count')
    for k, v in sorted(out.items()):
        print('   %s: %d' % (k, v))
    json.dump({'split': [[list(k), v] for k, v in out.items()]},
              open(os.path.join(ROOT, 'data', 'band_n5_split.json'), 'w'), indent=1)


def h2_controls():
    src = []
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_n5.json')))['rows']:
        src.append(('identities', r['qs']))
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_n5_degenerate.json')))['rows']:
        src.append(('degenerate', r['qs']))
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_hunt_n5.json')))['measured']:
        src.append(('band_hits', r['qs']))
    for l in open(os.path.join(ROOT, 'data', 'band_hunt_n5_min_cache.jsonl')):
        r = json.loads(l)
        if r['band'] or r['slack2'] + r['slack3'] > 0:
            src.append(('min_climb', r['qs']))
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_hunt_n5_min4.json')))['rows']:
        src.append(('level4_climb', r['qs']))
    seen, jobs, kinds = set(), [], []
    for k, q in src:
        key = json.dumps(q)
        if key in seen:
            continue
        seen.add(key)
        try:
            jobs.append((q, CL.engine([tuple(x) for x in q])['by_depth']))
            kinds.append(k)
        except Exception:
            pass
    with mp.Pool(8) as p:
        ms = p.map(measure, jobs)
    out = collections.defaultdict(lambda: {'rows': 0, 'L2': collections.Counter(), 'L3': collections.Counter(),
                                           'd4m2c4': collections.Counter(), 'c4': collections.Counter()})
    bad = 0
    for k, m in zip(kinds, ms):
        if 'excluded' in m or not m['gate']:
            bad += 1
            continue
        o = out[k]
        o['rows'] += 1
        o['L2'][sum(x - 1 for x in m['tri_c']) - (m['c'][2] - 1)] += 1
        o['L3'][sum(x - 1 for x in m['four_c']) - (m['c'][3] - 1)] += 1
        o['d4m2c4'][m['bd']['4'] - 2 * m['c'][4]] += 1
        o['c4'][m['c'][4]] += 1
    print('distinct rows %d; excluded or void %d' % (len(jobs), bad))
    for k, o in out.items():
        print('%-13s rows %4d  min L2 slack %d  min L3 slack %d  min d4-2c4 %d  c4 values %s'
              % (k, o['rows'], min(o['L2']), min(o['L3']), min(o['d4m2c4']), dict(o['c4'])))
    neg = sum(1 for o in out.values() for key in ('L2', 'L3') for v in o[key] if v < 0)
    print('negative L2/L3 slack values: %d' % neg)
    json.dump({k: {kk: (dict(vv) if isinstance(vv, collections.Counter) else vv) for kk, vv in o.items()}
               for k, o in out.items()},
              open(os.path.join(ROOT, 'data', 'band_n5_h2_controls.json'), 'w'), indent=1)


if __name__ == '__main__' and '--h2-controls' in sys.argv:
    h2_controls()
elif __name__ == '__main__' and '--split' in sys.argv:
    split()
elif __name__ == '__main__' and '--subset-gate' in sys.argv:
    subset_gate()
elif __name__ == '__main__' and '--split' not in sys.argv and '--h2-controls' not in sys.argv:
    degenerate() if '--degenerate' in sys.argv else main()
