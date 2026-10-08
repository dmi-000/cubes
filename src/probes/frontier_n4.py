#!/usr/bin/env python3
"""The joint frontier of (d1, d2, d3) at n = 4, from every per-depth count on file.  [plan item 4]

The proved caps are d1 <= 104, d2 <= 66, d3 <= 24, d4 <= 1 ([P401], [P410], [P422]), summing
to 195. The record 183 is (92, 66, 24, 1) and the golden 177 is (104, ., ., .): no compound seen
has all three at their caps. This collects every n = 4 depth vector already computed, keeps the
Pareto-maximal ones, and fits the linear inequalities that the frontier suggests.

**What this is.** A census of SAMPLED and CLIMBED compounds. Its frontier is a lower bound on the
true frontier, never an upper one; a trade-off read from it is a conjecture to derive.

**Caveats carried into the output.**
- Rows come from different engines over the project's history (c_level, sphere_count, census).
  The c_level engine is frame-dependent on shared-face-plane compounds ([P419], d1 only).
- A row is n = 4 when its depth keys are exactly 0..4, or 1..4 (some files mix n).
- Duplicates (same depth vector) are merged; one source is kept per vector, with a count.

Output: data/frontier_n4.json.
"""
import os, sys, json, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, 'data')
KEYS = ('by_depth', 'depth', 'depths', 'bd')


def vectors(obj):
    """yield (depth dict, enclosing record) for every depth dict inside obj"""
    if isinstance(obj, dict):
        for k in KEYS:
            v = obj.get(k)
            if isinstance(v, dict) and set(map(str, v)) in ({'0', '1', '2', '3', '4'}, {'1', '2', '3', '4'}):
                d = {int(a): b for a, b in v.items()}
                d.setdefault(0, 1)
                yield d, obj
        for v in obj.values():
            if isinstance(v, (dict, list)):
                yield from vectors(v)
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                yield from vectors(v)


def config(rec):
    for k in ('quats', 'cfg', 'qs', 'k', 'q'):
        if k in rec:
            return rec[k]
    return None


def main():
    seen = {}
    count = collections.Counter()
    nrows = 0
    bad = collections.Counter()
    files = sorted(glob.glob(os.path.join(DATA, '*.jsonl')) + glob.glob(os.path.join(DATA, '*.json')))
    for f in files:
        name = os.path.basename(f)
        if name == 'frontier_n4.json':
            continue
        if f.endswith('.jsonl'):
            recs = []
            for line in open(f):
                try:
                    recs.append(json.loads(line))
                except ValueError:
                    pass
        else:
            try:
                recs = [json.load(open(f))]
            except (ValueError, UnicodeDecodeError):
                continue
        for r in recs:
            for d, rec in vectors(r):
                if not all(isinstance(d[i], int) for i in range(5)):
                    continue
                if d[0] != 1 or d[4] > 1:
                    bad[name] += 1
                    continue
                nrows += 1
                v = (d[1], d[2], d[3], d[4])
                count[v] += 1
                if v not in seen:
                    seen[v] = {'file': name, 'config': config(rec)}
    vs = list(seen)
    def dominated(a):
        return any(b != a and all(b[i] >= a[i] for i in range(3)) for b in vs)
    front = sorted((v for v in vs if not dominated(v)), key=lambda v: (-sum(v), v))
    print('rows %d, distinct vectors %d, rejected (d0 != 1 or d4 > 1) %s' % (nrows, len(vs), dict(bad)))
    print('max per depth: d1 %d  d2 %d  d3 %d' % tuple(max(v[i] for v in vs) for i in range(3)))
    print('Pareto frontier over (d1, d2, d3), %d points:' % len(front))
    for v in front:
        print('  d1 %3d  d2 %2d  d3 %2d  d4 %d  total %3d  seen %5d  %s'
              % (v + (sum(v), count[v], seen[v]['file'])))
    # best total for each fixed d3, and each fixed d2
    for i, nm in ((2, 'd3'), (1, 'd2')):
        best = {}
        for v in vs:
            t = sum(v)
            if t > best.get(v[i], (0,))[0]:
                best[v[i]] = (t, v)
        print('best total by %s: %s' % (nm, sorted((k, b[0]) for k, b in best.items())[-10:]))
    json.dump({'rows': nrows, 'distinct': len(vs),
               'frontier': [{'d': list(v), 'total': sum(v), 'seen': count[v], **seen[v]} for v in front],
               'all': [[*v, count[v]] for v in sorted(vs)]},
              open(os.path.join(DATA, 'frontier_n4.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
