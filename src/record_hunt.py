#!/usr/bin/env python3
# Working principles: specs/NPLUS_SPEC.md (engine contract), README.md (project index).
"""Record hunt at n = 4..8: extension menus + greedy climbs, exact counts only.

Every count here comes from cube_regions_n (integer-quaternion exact engine).
INVARIANTS this file must preserve:
  * |component| <= 512 after gcd reduction -- the int128 overflow budget in
    specs/CPP_SPEC.md.  A config violating this is silently WRONG, not slow, so it
    is rejected before evaluation, never clamped.
  * A "region" is a component of constant cube-containment; only the project
    engines count that.  Never substitute an LP/grid/sign-vector counter here
    (Postscript 38: that error produced a whole retracted postscript).
  * Records are only claimed after a second engine agrees (certify_six).  This
    script deliberately does NOT claim records; it reports candidates.

Modes:
  extend   base config of n cubes + a menu of candidate (n+1)-th cubes
  climb    greedy +-1/+-2 single-component climb, then wide-perturbation
           restarts, from one or more start configs
  subsets  every drop-one-cube subset of a config (feeds the lower-n hunts)
  campaign extend -> climb the best few -> subsets of the winner (one job)
"""
import argparse
import json
import math
import os
import random
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions_n')
CAP = 512


def canon(quats):
    """gcd-reduce each quaternion and fix the sign (q and -q are one rotation).

    Two configs with the same canon are the same compound up to nothing but
    bookkeeping, so the evaluation cache is keyed on this.  Cube ORDER is kept
    (reordering is a relabeling the engine does not care about, but deduping
    over orderings would cost more than the evals it saves)."""
    out = []
    for q in quats:
        g = math.gcd(*[abs(c) for c in q])
        q = [c // g for c in q] if g > 1 else list(q)
        for c in q:
            if c:
                if c < 0:
                    q = [-x for x in q]
                break
        out.append(tuple(q))
    return tuple(out)


def ok(quats):
    """Engine-admissible: no zero quaternion, every component within CAP."""
    return all(any(q) and all(abs(c) <= CAP for c in q) for q in canon(quats))


def fmt(quats):
    return ';'.join(','.join(str(c) for c in q) for q in quats)


class Engine:
    """Batched exact counter.  Keeps a canon-keyed cache across the whole run."""

    def __init__(self, n, workers):
        self.n = n
        self.workers = workers
        self.cache = {}
        self.evals = 0

    def _run(self, chunk):
        p = subprocess.run([BIN, '--n', str(self.n), '--quats-stdin'],
                           input='\n'.join(fmt(c) for c in chunk) + '\n',
                           capture_output=True, text=True)
        out = []
        for line in p.stdout.splitlines():
            if line.startswith('{'):
                d = json.loads(line)
                # The engine answers every input line, including with
                # {"error": ...} (e.g. a zero quaternion a climb move made).
                # Keep the slot so results stay aligned with the batch, and
                # score it -1 so it can never win a max().
                out.append((d['bounded'], d['by_depth']) if 'bounded' in d
                           else (-1, {}))
        if len(out) != len(chunk):
            raise RuntimeError('engine returned %d of %d results: %s'
                               % (len(out), len(chunk), p.stderr[:200]))
        return out

    def count(self, configs):
        """-> list of (total, by_depth) aligned with configs (cached, deduped)."""
        todo = []
        for c in configs:
            k = canon(c)
            if k not in self.cache and k not in todo:
                todo.append(k)
        if todo:
            chunks = [todo[i::self.workers] for i in range(self.workers)]
            chunks = [c for c in chunks if c]
            with ThreadPoolExecutor(max_workers=len(chunks)) as ex:
                for ch, res in zip(chunks, ex.map(self._run, chunks)):
                    for cfg, r in zip(ch, res):
                        self.cache[cfg] = r
            self.evals += len(todo)
        return [self.cache[canon(c)] for c in configs]


def log(fh, **kw):
    kw['t'] = round(time.time() - T0, 1)
    fh.write(json.dumps(kw) + '\n')
    fh.flush()


def menu(size, rng):
    """Candidate cubes at mixed scales.

    The known extension winners span three orders of magnitude -- 723's sixth
    cube is (5,2,2,2), 1879's eighth is (55,7,-148,79) -- so a single small
    range would miss half the space; heights are sampled log-uniformly."""
    out, seen = [], set()
    heights = [4, 8, 16, 40, 100, 250, 512]
    while len(out) < size:
        h = heights[rng.randrange(len(heights))]
        q = tuple(rng.randint(-h, h) for _ in range(4))
        if not any(q):
            continue
        k = canon([q])[0]
        if k in seen or max(abs(c) for c in k) > CAP:
            continue
        seen.add(k)
        out.append(list(k))
    return out


def neighbors(quats, rng, wide=0):
    """+-1/+-2 on one component (wide=0), or `wide` simultaneous +-1..3 moves."""
    if wide:
        out = []
        for _ in range(40):
            c = [list(q) for q in quats]
            for _ in range(wide):
                i = rng.randrange(len(c))
                j = rng.randrange(4)
                c[i][j] += rng.choice([-3, -2, -1, 1, 2, 3])
            if ok(c):
                out.append(c)
        return out
    out = []
    for i in range(len(quats)):
        for j in range(4):
            for d in (-2, -1, 1, 2):
                c = [list(q) for q in quats]
                c[i][j] += d
                if ok(c):
                    out.append(c)
    return out


def climb(eng, start, fh, tag, rng, restarts=0, wide=6):
    """Greedy ascent to a +-2 local max, then `restarts` wide perturbations."""
    cur = [list(q) for q in start]
    best = eng.count([cur])[0][0]
    while True:
        cand = neighbors(cur, rng)
        if not cand:
            break
        res = eng.count(cand)
        i = max(range(len(cand)), key=lambda k: res[k][0])
        if res[i][0] <= best:
            break
        cur, best = cand[i], res[i][0]
        log(fh, tag=tag, stage='climb', total=best, quats=cur,
            by_depth=res[i][1])
    top = (best, cur)
    for r in range(restarts):
        cand = neighbors(top[1], rng, wide=wide)
        if not cand:
            continue
        res = eng.count(cand)
        i = max(range(len(cand)), key=lambda k: res[k][0])
        sub, subtot = climb(eng, cand[i], fh, tag + '/r%d' % r, rng)
        if subtot > top[0]:
            top = (subtot, sub)
            log(fh, tag=tag, stage='restart_gain', total=subtot, quats=sub)
    return top[1], top[0]


def subsets(eng, quats):
    """Every drop-one-cube subset, best first -- the top-down half of the tower."""
    subs = [[q for j, q in enumerate(quats) if j != i] for i in range(len(quats))]
    sub_eng = Engine(len(quats) - 1, eng.workers)
    res = sub_eng.count(subs)
    order = sorted(range(len(subs)), key=lambda k: -res[k][0])
    return [(res[k][0], subs[k], res[k][1]) for k in order]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True,
                    choices=['extend', 'climb', 'subsets', 'campaign'])
    ap.add_argument('--base', required=True,
                    help="'w,x,y,z;...' -- the config (extend: the n cubes to extend)")
    ap.add_argument('--record', type=int, default=0,
                    help='current record at the target n (for reporting only)')
    ap.add_argument('--menu', type=int, default=4000)
    ap.add_argument('--topk', type=int, default=6)
    ap.add_argument('--restarts', type=int, default=4)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    rng = random.Random(a.seed)
    base = [[int(x) for x in g.split(',')] for g in a.base.split(';')]
    fh = open(a.out, 'a')
    log(fh, stage='start', mode=a.mode, base=base, seed=a.seed, menu=a.menu)

    if a.mode == 'subsets':
        eng = Engine(len(base), a.workers)
        for tot, sub, bd in subsets(eng, base):
            log(fh, stage='subset', total=tot, quats=sub, by_depth=bd)
            print(tot, fmt(sub), flush=True)
        return

    if a.mode == 'climb':
        eng = Engine(len(base), a.workers)
        cfg, tot = climb(eng, base, fh, 'climb', rng, restarts=a.restarts)
        log(fh, stage='done', total=tot, quats=cfg, evals=eng.evals)
        print('best', tot, fmt(cfg), flush=True)
        return

    # extend / campaign: base has n cubes, we hunt at n+1
    n1 = len(base) + 1
    eng = Engine(n1, a.workers)
    cands = [base + [q] for q in menu(a.menu, rng)]
    res = eng.count(cands)
    order = sorted(range(len(cands)), key=lambda k: -res[k][0])
    for k in order[:40]:
        log(fh, stage='extend', total=res[k][0], quats=cands[k],
            by_depth=res[k][1])
    print('extend best:', [res[k][0] for k in order[:10]], flush=True)

    if a.mode == 'extend':
        log(fh, stage='done', evals=eng.evals)
        return

    best = (res[order[0]][0], cands[order[0]])
    for k in order[:a.topk]:
        cfg, tot = climb(eng, cands[k], fh, 'seed%d' % k, rng,
                         restarts=a.restarts)
        log(fh, stage='climbed', total=tot, quats=cfg)
        print('climbed', tot, flush=True)
        if tot > best[0]:
            best = (tot, cfg)
    log(fh, stage='best', total=best[0], quats=best[1], record=a.record,
        beats_record=bool(a.record and best[0] > a.record), evals=eng.evals)
    print('BEST', best[0], fmt(best[1]), flush=True)

    # top-down half: hand the winner's subsets to the lower level for free
    for tot, sub, bd in subsets(eng, best[1]):
        log(fh, stage='winner_subset', total=tot, quats=sub, by_depth=bd)
    log(fh, stage='done', evals=eng.evals)


T0 = time.time()
if __name__ == '__main__':
    main()
