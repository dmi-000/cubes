#!/usr/bin/env python3
# Working principles: NPLUS_SPEC.md (gate G1regression). Project index: README.md
"""G1regression: --n 6 must reproduce exact_search_results.jsonl (ground
truth, read-only) with zero mismatches on totals AND depth histograms.

NOTE: the oracle file's seed range is 40..7009 (not 0..199 as the spec's
prose assumed -- checked directly). We use the intersection with [0,200):
seeds 40..199, 160 configs. This is the full range of oracle coverage
available for "seeds 0..199"; the rest of 0..199 was never run through
the Python pipeline. Reported honestly rather than silently changed."""
import json
import subprocess

oracle = {}
for line in open('exact_search_results.jsonl'):
    r = json.loads(line)
    if r.get('seed') is not None and 0 <= r['seed'] < 200:
        oracle[r['seed']] = (r['bounded'], {int(k): v for k, v in r['by_depth'].items()})

print(f'oracle seeds in [0,200): {len(oracle)} (range {min(oracle)}..{max(oracle)})')

out = subprocess.run(['./cube_regions_n', '--n', '6', '--seeds', str(min(oracle)), str(max(oracle)+1)],
                      capture_output=True, text=True, check=True).stdout

mism = 0
checked = 0
for line in out.splitlines():
    r = json.loads(line)
    s = r['seed']
    if s not in oracle:
        continue
    checked += 1
    ob, od = oracle[s]
    cb = r['bounded']
    cd = {int(k): v for k, v in r['by_depth'].items()}
    if cb != ob or cd != od:
        mism += 1
        print(f'MISMATCH seed {s}: cpp bounded={cb} depth={cd}  oracle bounded={ob} depth={od}')

print(f'checked {checked} seeds, {mism} mismatches' + ('  -- PASS' if mism == 0 else '  -- FAIL'))
