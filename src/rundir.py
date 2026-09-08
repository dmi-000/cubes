#!/usr/bin/env python3
"""Create a self-contained directory for one campaign.

WHY A DIRECTORY, AND WHY IT MUST HOLD THE PRODUCER.  Two failures in one day,
both from the flat layout:

  * `census_members.py` derived both its output and its log path from the shard
    number alone and opened both with 'w'.  Relaunching at a different shard
    count reuses a number an earlier run already wrote, so the earlier run's
    records are DESTROYED, not merged.  Caught before launch on 2026-08-17; it
    would have wiped 170 completed classes.
  * `census_variety.py` writes generation 4 and nothing in the repository writes
    generations 1-3: the script was edited in place each time.  The output NAME
    was bumped every generation, so the data survives but the code that made it
    does not.  Those numbers can no longer be reproduced.

A directory per campaign fixes the first.  COPYING THE PRODUCER INTO IT fixes the
second, and that is the part a bare directory convention would miss: a run
directory holding only outputs loses its provenance the moment the script is
edited.

WHAT IS A CAMPAIGN.  Anything that shards, resumes, or writes more than one file.
A single diagnostic output is NOT one -- its `.prov.json` sidecar already records
argv and the script hash, and a directory per file would be noise.
"""
import os, shutil, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, 'runs')


def new_run(name, producers=(), note=None, argv=None):
    """runs/<name>_<UTC stamp>/ containing copies of every producer script.

    Returns the directory.  The timestamp makes a rerun a NEW directory rather
    than an overwrite -- the flat layout's destructive case cannot arise.
    """
    stamp = time.strftime('%Y%m%d-%H%M%S')
    d = os.path.join(RUNS, '%s_%s' % (name, stamp))
    os.makedirs(os.path.join(d, 'producer'), exist_ok=False)
    for p in list(producers) + [(argv or sys.argv)[0]]:
        src = p if os.path.isabs(p) else os.path.join(HERE, p)
        if os.path.exists(src) and os.path.isfile(src):
            shutil.copy2(src, os.path.join(d, 'producer', os.path.basename(src)))
    with open(os.path.join(d, 'README.md'), 'w') as f:
        f.write('# %s\n\nStarted %s\n\n    %s\n\n%s\n\n'
                '`producer/` holds the scripts AS THEY WERE at launch, so editing\n'
                'the originals later cannot orphan this data.\n'
                % (name, time.strftime('%Y-%m-%d %H:%M:%S'),
                   ' '.join(['python3'] + list(argv or sys.argv)), note or ''))
    return d


if __name__ == '__main__':
    print(new_run(sys.argv[1] if len(sys.argv) > 1 else 'run'))
