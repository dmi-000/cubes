#!/usr/bin/env python3
"""Disk cache for `solve_ends.catalogue` — METHODS 2, applied where it now bites.

The catalogue (real triple points + crossing lines of a base) is the ONE expensive
step in every endpoint solve, and it depends only on the base cubes. At n=9 base it
runs ~10 minutes and it has now been recomputed from scratch in `n78_ends`,
`solve_ends`, `solve_more_ends`, `n9_upper`, `n8_lower` and `n10_ends` — six times
for bases that repeat.

Keyed on the base cubes, so a rerun after a correction costs the correction only.
"""
import hashlib, json, os, pickle, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, 'catalogue_cache')


def catalogue(cubes, bound=4):
    os.makedirs(DIR, exist_ok=True)
    key = hashlib.sha1(json.dumps([list(map(str, q)) for q in cubes] + [bound]).encode()).hexdigest()[:16]
    path = os.path.join(DIR, 'cat_%d_%s.pkl' % (len(cubes), key))
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    from solve_ends import catalogue as _cat
    val = _cat(cubes, bound)
    tmp = path + '.tmp'
    with open(tmp, 'wb') as f:
        pickle.dump(val, f)
    os.replace(tmp, path)                 # atomic: a killed run leaves no half file
    return val


if __name__ == '__main__':
    BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    C9 = BASE + [(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
    import time
    t0 = time.time()
    pts, lines = catalogue(C9)
    print('C9 catalogue: %d triple points, %d crossing lines (%.0fs)'
          % (len(pts), len(lines), time.time() - t0), flush=True)
