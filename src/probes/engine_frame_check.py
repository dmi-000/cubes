#!/usr/bin/env python3
"""Is the engine frame-dependent on shared-plane compounds?  [P419]

Found 2026-10-04 on shared_plane_scope's best star compound.
- The engine counts 77 (`d1 = 34`) in the identity frame and in an x-axis rotation of it.
- It counts 75 (`d1 = 32`) under three generic rotations.
- sphere_count, which is rotation-invariant, gives 75 in every frame.
So the engine overcounts there in axis-aligned frames.

This re-counts, in a generic frame (the global rotation (3,1,1,1)), every compound whose engine
count this session relied on in the identity frame:
- shared_plane_scope's cache (runs 1 and 2);
- shared_oracle's rows, the compound and its four triples;
- the 3 000 highest totals of [P411]'s shared_plane_climb cache.

Any row whose two frames disagree is re-counted with sphere_count, the arbiter.
Output: data/engine_frame_check.json.
"""
import os, sys, json, itertools, collections, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul
from sphere_count import Compound

ROOT = os.path.dirname(os.path.dirname(HERE))
GENERIC = (3, 1, 1, 1)


def eng(qs, rot=None):
    q2 = [qmul(rot, q) for q in qs] if rot else qs
    e = CL.engine(q2)
    if 'by_depth' not in e:
        return None
    return e.get('bounded'), {k: v for k, v in e['by_depth'].items() if k != '0'}


def check(qs):
    """[(subset, identity-frame count, generic-frame count)] for the compound and its triples."""
    out = []
    for sub in [tuple(range(len(qs)))] + list(itertools.combinations(range(len(qs)), 3)):
        q = [qs[i] for i in sub]
        a, b = eng(q), eng(q, GENERIC)
        out.append((sub, a, b))
    return qs, out


def parse(k):
    return [tuple(map(int, g.split(','))) for g in k.split(';')]


def main():
    keys = set()
    for line in open(os.path.join(ROOT, 'data', 'shared_plane_scope_cache.jsonl')):
        try:
            keys.add(json.loads(line)['k'])
        except ValueError:
            pass
    n_scope = len(keys)
    for r in json.load(open(os.path.join(ROOT, 'data', 'shared_oracle.json')))['rows']:
        keys.add(';'.join(','.join(map(str, q)) for q in r['qs']))
    climb = {}
    for line in open(os.path.join(ROOT, 'data', 'shared_plane_climb_cache.jsonl')):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get('t') is not None:
            climb[r['k']] = r['t']
    keys |= set(sorted(climb, key=lambda k: -climb[k])[:3000])
    jobs = [parse(k) for k in sorted(keys)]
    with mp.Pool(8) as p:
        res = p.map(check, jobs)
    stats = collections.Counter()
    bad = []
    for qs, out in res:
        for sub, a, b in out:
            kind = 'compound' if len(sub) == 4 else 'triple'
            if a is None or b is None:
                stats[kind + '_unevaluated'] += 1
            elif a == b:
                stats[kind + '_agree'] += 1
            else:
                stats[kind + '_DISAGREE'] += 1
                bad.append({'qs': qs, 'sub': sub, 'identity': a, 'generic': b})
    for b in bad[:40]:
        q = [b['qs'][i] for i in b['sub']]
        t, bd = Compound(q).count()
        b['sphere_count'] = (t, {str(k): v for k, v in bd.items()})
        b['which_right'] = ('generic' if t == b['generic'][0] and bd[2] == b['generic'][1].get('2')
                            else 'identity' if t == b['identity'][0] else 'neither')
    print('compounds checked: %d (scope cache %d)' % (len(res), n_scope))
    print(dict(stats))
    print('re-counted with sphere_count (first %d disagreements): %s'
          % (min(40, len(bad)), dict(collections.Counter(b.get('which_right') for b in bad[:40]))))
    d2diff = [b for b in bad if b['identity'][1].get('2') != b['generic'][1].get('2')]
    print('disagreements that change d2: %d' % len(d2diff))
    json.dump({'stats': dict(stats), 'disagreements': bad}, open(os.path.join(ROOT, 'data',
              'engine_frame_check.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
