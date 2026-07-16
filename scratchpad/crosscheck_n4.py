#!/usr/bin/env python3
"""Cross-check cube_regions_n --n 4 against certify_six.exact_count_config oracle."""
import sys, json, subprocess
sys.path.insert(0, '/Users/dmi/carroll')
from golden_rotations import rot_from_quat
from certify_six import exact_count_config

def cpp_count(quats):
    qstr = ';'.join(','.join(str(c) for c in q) for q in quats)
    out = subprocess.run(['/Users/dmi/carroll/cube_regions_n', '--n', '4', '--quats', qstr],
                          capture_output=True, text=True, check=True).stdout
    return json.loads(out)

seeds = [1, 2, 3, 17, 999]
for s in seeds:
    out = subprocess.run(['/Users/dmi/carroll/cube_regions_n', '--n', '4', '--seed', str(s)],
                          capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    quats = d['quats']
    cpp_total = d['bounded']
    cpp_bd = d['by_depth']
    rots = [rot_from_quat(*q) for q in quats]
    total, by_depth = exact_count_config(rots, verbose=False)
    match = (total == cpp_total) and ({str(k): v for k,v in by_depth.items()} == cpp_bd or
                                       {int(k): v for k,v in cpp_bd.items()} == by_depth)
    print(f"seed {s}: cpp={cpp_total} {cpp_bd}  oracle={total} {dict(sorted(by_depth.items()))}  MATCH={match}")
