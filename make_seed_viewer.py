#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (seed-viewer artifact). Project index: README.md
"""Rebuild the seed-viewer artifact HTML from the live search log.

Reads exact_search_results.jsonl (seeds 40+) plus the hardcoded certified
batch for seeds 0-39, writes the counts snapshot into the viewer template,
and emits the final HTML ready for artifact publishing.  Run after the
background exact_search.py has advanced and the artifact should be
refreshed:

    python3 make_seed_viewer.py
    # then republish SCRATCH/seed119_viewer.html to the same artifact URL
"""
import json
import os

SCRATCH = ('/private/tmp/claude-502/-Users-dmi-carroll/'
           'c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad')
LOG = os.path.expanduser('~/carroll/exact_search_results.jsonl')

# certified batch (exact_search.py batch mode), seeds 0-39, counts only
BATCH = [559, 559, 563, 583, 563, 539, 515, 523, 587, 547, 539, 511, 595,
         503, 571, 491, 523, 519, 567, 527, 595, 579, 467, 543, 535, 527,
         563, 543, 579, 555, 543, 567, 551, 535, 587, 579, 587, 555, 519,
         591]


def main():
    data = {s: [b, None] for s, b in enumerate(BATCH)}
    with open(LOG) as f:
        for line in f:
            r = json.loads(line)
            d = r['by_depth']
            data[r['seed']] = [r['bounded'],
                               [d.get(str(k), d.get(k, 0)) for k in range(1, 7)]]
    compact = json.dumps({str(k): v for k, v in sorted(data.items())},
                         separators=(',', ':'))
    tpl = open(os.path.join(SCRATCH, 'seed_viewer_template.html')).read()
    assert '__COUNTS_JSON__' in tpl
    out = tpl.replace('__COUNTS_JSON__', compact)
    path = os.path.join(SCRATCH, 'seed119_viewer.html')
    open(path, 'w').write(out)
    best = max(data.items(), key=lambda kv: kv[1][0])
    print(f'{len(data)} seeds, best {best[1][0]} (seed {best[0]}), '
          f'{len(out)} bytes -> {path}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
