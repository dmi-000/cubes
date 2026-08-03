#!/usr/bin/env python3
"""G1/G3/G5 for the widened engine: is cube_regions_q2w the SAME engine?

WIDE_ENGINE_SPEC.md widens the validated ℚ(√d) engine's scalar from 128 to
256 bits so the 284 634 mixed-strata configurations rejected by the old chain
budget can be counted.  A widened engine is only worth having if it is
provably the same engine on everything the old one could already do, so the
gate is equivalence, not plausibility: identical `bounded` AND identical
`by_depth` on every configuration inside the NARROW budget.

Input comes from `mixed_q2_hits.jsonl`, the configurations the narrow engine
actually counted, so every case is known to be inside its budget -- no
guessing about where the old boundary was.

INVARIANT: both engines see byte-identical input, and the comparison is on
the full depth profile, not just the total.  Two different region complexes
can share a total; agreeing on the profile is a much stronger statement, and
it is free.
"""
import collections
import json
import subprocess
import sys
import time


def run(binary, d, lines):
    t0 = time.time()
    p = subprocess.run([binary, '--d', str(d), '--quats-stdin'],
                       input='\n'.join(lines) + '\n',
                       capture_output=True, text=True)
    dt = time.time() - t0
    out = []
    for ln in p.stdout.splitlines():
        if ln.startswith('{'):
            j = json.loads(ln)
            out.append((j.get('bounded'), tuple(sorted(j.get('by_depth', {}).items()))))
        else:
            out.append(None)
    return out, dt, p.stderr


def main():
    byd = collections.defaultdict(list)
    for ln in open('mixed_q2_hits.jsonl'):
        r = json.loads(ln)
        q = r['quat']
        # components are comma-separated, quaternions semicolon-separated;
        # getting this backwards makes BOTH engines emit the same parse error
        # and the gate passes vacuously -- so the counts are asserted below
        key = ','.join('%d:%d' % (a, b) for a, b in
                       [tuple(c) for c in q])
        byd[r['d']].append(key)
    fixed = '4:0,1:0,1:0,-1:0;3:0,3:0,7:0,3:0;5:0,-1:0,-5:0,-5:0;2:0,1:0,1:0,1:0;1:0,1:0,1:0,1:0'

    total = mismatch = 0
    tn = tw = 0.0
    print('%-10s %7s %9s %9s  %s' % ('d', 'configs', 'narrow_s', 'wide_s', 'verdict'))
    for d in sorted(byd, key=lambda k: -len(byd[k])):
        cfgs = sorted(set(byd[d]))
        lines = [fixed + ';' + c for c in cfgs]
        a, dta, ea = run('./cube_regions_q2', d, lines)
        b, dtb, eb = run('./cube_regions_q2w', d, lines)
        if len(a) != len(b):
            print('  d=%d LENGTH MISMATCH %d vs %d' % (d, len(a), len(b)))
            mismatch += 1
            continue
        # a gate that compares two empty lists, or two lists of errors, is
        # worse than no gate: require a real count on every row
        assert len(a) == len(lines), (d, len(a), len(lines))
        nreal = sum(1 for x in a if x[0] is not None)
        if nreal != len(lines):
            print('  d=%d: only %d/%d rows produced a count -- NOT a valid gate'
                  % (d, nreal, len(lines)))
            mismatch += len(lines) - nreal
        bad = [(c, x, y) for c, x, y in zip(cfgs, a, b) if x != y]
        total += len(cfgs)
        tn += dta
        tw += dtb
        mismatch += len(bad)
        print('%-10d %7d %9.2f %9.2f  %s' %
              (d, len(cfgs), dta, dtb,
               'IDENTICAL' if not bad else 'MISMATCH %d' % len(bad)), flush=True)
        for c, x, y in bad[:3]:
            print('     %s  narrow=%s  wide=%s' % (c, x, y))
    print('\nG1: %d configurations across %d fields, %d mismatches'
          % (total, len(byd), mismatch))
    print('G5: narrow %.2fs, wide %.2fs, ratio %.2fx'
          % (tn, tw, tw / tn if tn else float('nan')))


if __name__ == '__main__':
    main()
