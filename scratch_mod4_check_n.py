#!/usr/bin/env python3
# Working principles: NPLUS_SPEC.md (mod-4 at scale). Project index: README.md
"""mod-4 law check for arbitrary n using the validated C++ engine (fast):
bounded == 2n-1 (mod 4) conjectured for generic configs (mod4_check.py
established this for n=4..7 via the slow Python oracle). Read-only
analysis over campaign_n<n>.jsonl; reports the exception rate.
"""
import json
import sys


def check(n, path):
    total = 0
    exc = 0
    predicted = (2 * n - 1) % 4
    examples = []
    with open(path) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'bounded' not in r:
                continue
            total += 1
            m = r['bounded'] % 4
            if m != predicted:
                exc += 1
                if len(examples) < 10:
                    examples.append((r.get('seed'), r['bounded'], m))
    rate = exc / total if total else float('nan')
    print(f'n={n}: {total} configs, predicted bounded=={predicted} (mod 4), '
          f'{exc} exceptions ({rate:.4%})')
    if examples:
        print(f'  example exceptions (seed, bounded, mod4): {examples}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    n = int(sys.argv[1])
    path = sys.argv[2] if len(sys.argv) > 2 else f'campaign_n{n}.jsonl'
    check(n, path)
