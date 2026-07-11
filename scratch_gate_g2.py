#!/usr/bin/env python3
# Working principles: NPLUS_SPEC.md (gate G2cross). Project index: README.md
"""G2cross: for n in {2,3,4,5,7,8}, three seeds each (777,778,779 -- the
spec's known n=7 values, reused across n for a uniform, reproducible
gate), C++ (./cube_regions_n) must match the Python oracle
certify_six.exact_count_config exactly: total AND depth histogram.
Known check: n=7 seeds 777/778/779 -> 973, 993, 873."""
import json
import subprocess
import time

from mt_sim import sim_quats
from golden_rotations import rot_from_quat
from certify_six import exact_count_config

NS = [2, 3, 4, 5, 7, 8]
SEEDS = [777, 778, 779]

mism = 0
checked = 0
for n in NS:
    for seed in SEEDS:
        t0 = time.time()
        quats = sim_quats(seed, n=n)
        rots = [rot_from_quat(*q) for q in quats]
        py_total, py_depth = exact_count_config(rots, verbose=False)
        py_depth = {int(k): v for k, v in py_depth.items()}
        pt = time.time() - t0

        out = subprocess.run(['./cube_regions_n', '--n', str(n), '--seed', str(seed)],
                              capture_output=True, text=True, check=True).stdout
        r = json.loads(out.strip())
        cpp_total = r['bounded']
        cpp_depth = {int(k): v for k, v in r['by_depth'].items()}

        checked += 1
        ok = (cpp_total == py_total and cpp_depth == py_depth)
        if not ok:
            mism += 1
        print(f'n={n} seed={seed}: py={py_total} cpp={cpp_total} '
              f'{"OK" if ok else "MISMATCH"} (py {pt:.1f}s, cpp {r["us"]/1e6:.3f}s)'
              + ('' if ok else f'\n   py_depth={py_depth}\n   cpp_depth={cpp_depth}'))

print(f'\n{checked} checks, {mism} mismatches' + ('  -- PASS' if mism == 0 else '  -- FAIL'))
