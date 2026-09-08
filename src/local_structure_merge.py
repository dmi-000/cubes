#!/usr/bin/env python3
"""Merge the seed-sharded 12a re-measurement and report it with its method parameters.

Each `local_structure.py` seed is an INDEPENDENT sample, so the eight are pooled by
weighting each seed's rate by its n -- not averaged, which would weight a short run equally
with a long one. Per-seed values are also printed, because the spread ACROSS seeds is the
only honest error bar here: a rate quoted from one seed cannot be distinguished from noise,
which is what made the first correction's per-ensemble directions collapse
([FAILURE_MODES 27a]).

METHOD PARAMETERS, printed with the result rather than buried:
  * perturbation:  q -> q*2^k + e_i on cubes 1..n-1, cube 0 held as the gauge; the relative
    displacement is 1/(2^k * |q|), so the scale is NOMINAL and varies with the base's
    height. It is not "every configuration moved by exactly 2^-k".
  * both normal conventions are scored on the SAME perturbed configurations.
  * GATE A (k=0) must read 0.0 / 100% in both columns or the run is void.
"""
import glob, json, sys

files = sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else 'ls_*.json'))
if not files:
    sys.exit('no seed files matched')

seeds = {}
for fn in files:
    d = json.load(open(fn))
    meta = d.pop('_meta', {})
    seeds[fn] = (meta, {int(k): v for k, v in d.items()})

scales = sorted(next(iter(seeds.values()))[1])
print('merged %d seeds, %d configurations each\n'
      % (len(seeds), next(iter(seeds.values()))[0].get('n', 0)))

print('%-10s %22s %24s' % ('', 'CORRECTED normals', 'BROKEN normals (12a used)'))
print('%-10s %10s %11s %10s %11s   %s'
      % ('scale', 'med L1', 'unchanged', 'med L1', 'unchanged', 'per-seed unchanged (corrected)'))
ok = True
for k in scales:
    tot = sum(s[1][k]['n'] for s in seeds.values())
    unch = sum(s[1][k]['unchanged_pct'] * s[1][k]['n'] for s in seeds.values()) / tot
    bunch = sum(s[1][k]['broken_unchanged_pct'] * s[1][k]['n'] for s in seeds.values()) / tot
    meds = sorted(s[1][k]['median_l1'] for s in seeds.values())
    bmeds = sorted(s[1][k]['broken_median_l1'] for s in seeds.values())
    per = sorted(round(s[1][k]['unchanged_pct'], 1) for s in seeds.values())
    med = meds[len(meds)//2]; bmed = bmeds[len(bmeds)//2]
    tag = '  <-- GATE A' if k == 0 else ''
    print('2^-%-7s %10.1f %10.1f%% %10.1f %10.1f%%   %s%s'
          % (k, med, unch, bmed, bunch, per, tag))
    if k == 0 and (med != 0 or abs(unch - 100.0) > 1e-9 or bmed != 0):
        ok = False

print()
if not ok:
    print('GATE A FAILED on the merged data -- the whole measurement is void.')
    sys.exit(1)
print('GATE A passes: a zero perturbation is scored as no change, in both columns.')
print('So a nonzero "unchanged" rate below is a property of the space, not of the comparison.')
print()
print('VOID original (TAXONOMY 12a, broken normals, script does not survive):')
print('   2^-4 med 66.0 / 2^-8 med 66.0 / 2^-14 med 71.0, unchanged 0% at every scale')
print()
print('Scale: q -> q*2^k + e_i on cubes 1..n-1; relative displacement 1/(2^k*|q|), so the')
print('scale is NOMINAL and varies with base height. 2^-20 and 2^-26 lie outside anything')
print('12a tested.')
