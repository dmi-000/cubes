#!/usr/bin/env python3
"""Region count vs Haar volume: the baseline distribution, and the basin histogram.

Reads haar_n*_Q*.jsonl (exactly-Haar starts, exact counts) and basin_n*_d*_s*.jsonl
(terminal counts of the climb from those starts).  Every number here is an estimate of
a VOLUME -- the Haar measure of a set of configurations -- so each carries a binomial
or Monte Carlo error, and counts that were never evaluated are reported as such rather
than folded into a bin.
"""
import json, glob, sys, math, statistics as st
from collections import Counter

REC = {2:13, 3:67, 4:183, 5:393, 6:727, 7:1217, 8:1895, 9:2787, 10:3925}

def load(pat, key='c'):
    out = {}
    for f in glob.glob(pat):
        n = int(f.split('_n')[1].split('_')[0])
        for line in open(f):
            d = json.loads(line)
            out.setdefault(n, []).append(d)
    return out

def baseline(Q):
    print('\n=== Haar baseline, Q=%d: distribution of the region count over VOLUME ===' % Q)
    print('  n      K unev    min    max     mean     sd   record   (rec-mean)/sd  max/rec')
    rows = {}
    for n, ds in sorted(load('haar_n*_Q%d.jsonl' % Q).items()):
        cs = [d['c'] for d in ds if d['c'] is not None]
        un = len(ds) - len(cs)
        if len(cs) < 2: continue
        m, s = st.mean(cs), st.pstdev(cs)
        r = REC.get(n)
        rows[n] = (cs, m, s)
        print('%3d %6d %4d %6d %6d %8.1f %6.1f %8s %10.2f %11.3f'
              % (n, len(cs), un, min(cs), max(cs), m, s, r,
                 (r - m) / s if r and s else float('nan'),
                 max(cs) / r if r else float('nan')))
    return rows

if __name__ == '__main__':
    rows = baseline(30000)
    r128 = baseline(128)

    print('\n=== control: does the Q=128 lattice (used for the basin starts) shift it? ===')
    print('  n   mean(Q=30000)   mean(Q=128)   diff   +/- 2 s.e.   verdict')
    for n in sorted(set(rows) & set(r128)):
        a, ma, sa = rows[n]; b, mb, sb = r128[n]
        se = math.sqrt(sa * sa / len(a) + sb * sb / len(b))
        d = mb - ma
        print('%3d %14.1f %13.1f %7.1f %11.1f   %s'
              % (n, ma, mb, d, 2 * se, 'consistent' if abs(d) <= 2 * se else 'SHIFTED'))

    print('\n=== the top of the baseline: how much volume is near the record ===')
    for n, (cs, m, s) in sorted(rows.items()):
        r = REC.get(n)
        if not r: continue
        for frac in (0.90, 0.95, 1.00):
            k = sum(1 for c in cs if c >= frac * r)
            print('  n=%-3d volume with count >= %.0f%% of the record %-5d : %d/%d = %s'
                  % (n, frac * 100, math.ceil(frac * r), k, len(cs),
                     '%.4f' % (k / len(cs)) if k else '0  (< %.4f at 95%%)' % (3 / len(cs))))
        print()

    bs = load('basin_n*_d*_s*.jsonl')
    if bs:
        print('=== VOLUME BY TERMINAL COUNT, with UNEVALUABLE as its own category ===')
        print("An UNDETERMINED climb reached a real count before the engines gave out, and")
        print("those counts are the HIGHEST in the run -- so it is a bin of the distribution,")
        print("not a discarded sample. `best evaluable` is the count at the last accepted")
        print("configuration; `bits needed` is the chain width that would have evaluated the")
        print("tallest refused probe (climb.required_bits, calibrated on both engines).")
        import subprocess as _sp
        def _cnt(cfg):
            st = ';'.join(','.join(map(str, q)) for q in cfg)
            for cmd in (['./cube_regions_n', '--quats', st],
                        ['./cube_regions_q2w', '--d', '0', '--quats', st]):
                try:
                    return json.loads(_sp.run(cmd, capture_output=True, text=True).stdout)['bounded']
                except Exception:
                    pass
            return None
        for n in sorted(bs):
            ds = bs[n]
            fin = [d for d in ds if d.get('end') is not None]
            und = [d for d in ds if d.get('end') is None]
            tot = len(ds)
            print('\n n=%d   %d climbs   (%d terminated, %d UNEVALUABLE = %.1f%% of volume)'
                  % (n, tot, len(fin), len(und), 100.0 * len(und) / tot))
            cnt_end = Counter(d['end'] for d in fin)
            for c, k in sorted(cnt_end.items()):
                se = 2 * math.sqrt(k * (tot - k) / tot) / tot
                print('      count %-6d volume %5.3f +/- %.3f  (%d/%d)' % (c, k / tot, se, k, tot))
            if und:
                be = []
                for d in und:
                    b = d.get('best_evaluable')
                    if b is None:
                        b = _cnt([tuple(q) for q in d['cfg1']])
                    be.append(b)
                se = 2 * math.sqrt(len(und) * (tot - len(und)) / tot) / tot
                print('      UNEVALUABLE  volume %5.3f +/- %.3f  (%d/%d)'
                      % (len(und) / tot, se, len(und), tot))
                good = [b for b in be if b is not None]
                if good:
                    print('         best evaluable counts reached: %s   (max %d)'
                          % (sorted(good), max(good)))
                bits = [d['bits_needed_max'] for d in und if d.get('bits_needed_max')]
                if bits:
                    print('         chain width needed: median %.0f, max %.0f bits '
                          '(engines have 112 / 240)' % (st.median(bits), max(bits)))
                else:
                    print('         chain width needed: NOT RECORDED for these rows '
                          '(instrumented after they ran)')
        print()
        print('=== engine-refusal VOLUME: the space this apparatus cannot decide ===')
        print("A climb that ends UNDETERMINED (both engines refused every probe) is not a")
        print("failed sample -- it measures the Haar volume of the configurations where the")
        print("apparatus gives out, which is a property of the engine + representative policy")
        print("and is reportable as its own number rather than dropped.")
        print('  n   climbs   undetermined   volume        scan chambers   scan refused')
        for n in sorted(bs):
            ds = bs[n]
            und = sum(1 for d in ds if d.get('end') is None)
            tot = len(ds)
            sc = sum(d.get('scan_chambers', 0) for d in ds)
            su = sum(d.get('scan_unevaluated', 0) for d in ds)
            lo = und / tot if tot else 0
            se = 2 * math.sqrt(max(und, 1) * (tot - und) / tot) / tot if tot else 0
            print('%3d %8d %14d   %.4f +/- %.4f %11d %14s'
                  % (n, tot, und, lo, se, sc,
                     '%d (%.2f%%)' % (su, 100.0 * su / sc) if sc else '-'))
        print()
    if bs:
        print('=== basins: terminal count of the climb, by menu size ===')
        for n in sorted(bs):
            byd = {}
            for d in bs[n]:
                byd.setdefault(d.get('params', {}).get('NDIR', '?'), []).append(d)
            for nd, ds in sorted(byd.items(), key=lambda kv: (str(kv[0]))):
                fin = [d for d in ds if d.get('end') is not None]
                und = len(ds) - len(fin)
                if not fin: continue
                ends = [d['end'] for d in fin]
                starts = [d['start'] for d in fin]
                gain = [d['end'] - d['start'] for d in fin]
                print('\n n=%d NDIR=%s  K=%d  undetermined=%d' % (n, nd, len(fin), und))
                print('   start  mean %.1f   terminal mean %.1f   gain mean %.1f max %d'
                      % (st.mean(starts), st.mean(ends), st.mean(gain), max(gain)))
                print('   terminal max %d   record %s   deficit %s'
                      % (max(ends), REC.get(n), REC.get(n, 0) - max(ends)))
                print('   basin volumes (terminal count: share of Haar volume):')
                tot = len(ends)
                for c, k in sorted(Counter(ends).items()):
                    se = math.sqrt(k * (tot - k) / tot) / tot
                    print('      %5d  %5.3f +/- %.3f   (%d/%d)' % (c, k / tot, 2 * se, k, tot))
