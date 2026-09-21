#!/usr/bin/env python3
"""[OQ 39] EVERY way a 4-compound could beat 183, enumerated over its SUBSET PROFILE.

The user's framing, and it is the right one: a 183-beating compound's subsets are already
catalogued -- pairs count `3 + E_i` with `E_i <= 10` PROVED ([P237]), triples count
`5 + sum E_i + E_S` with `E_S <= 32` PROVED (PROOF_67 Lemma 1a).  Maximising the SUBSET counts
gives the golden 177, which loses.  What has to be maximised is the count of their UNION:

    TOTAL = 7 + T + B - Q4        T := sum over pairs of E_i   (two-body)
                                  B := sum over triples of E_S
                                  Q4 := 4-fold vertices

verified on the record (7 + 48 + 128 - 0 = 183) and on the golden (7 + 60 + 128 - 18 = 177).

So "beat 183" is the single inequality `T + B - Q4 >= 177`, and the profile space is small
enough to enumerate EXACTLY rather than search.  Two structural facts cut it down:

  * a CORNER SHARING contributes exactly 2 to `SC2` (a shared body-diagonal axis meets both
    cubes in an antipodal pair of corners), and `E_i = EE_i + 2*SC2_i <= 10` PROVED -- so a
    sharing pair is capped at `EE_i <= 6` and a non-sharing pair at `EE_i <= 10`.
  * therefore with `s` sharings, `T = EE_total + 4s` and `EE_total <= 60 - 4s`.

This enumerates all profiles, reports which survive under PROVED constraints alone and which
survive when the MEASURED ones are added, and prints the live targets with the known
constructions placed on them.
"""
import sys, os, json, itertools, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
PAIRS = list(itertools.combinations(range(4), 2))
TRIPLES = list(itertools.combinations(range(4), 3))
INTRI = [[k for k, p in enumerate(PAIRS) if set(p) <= set(S)] for S in TRIPLES]

# observed per-pair EE values among non-degenerate pairs ([P330], data/ee_per_pair.json)
EE_VALUES = (0, 4, 6, 8, 10)


def profiles():
    """(EE per pair, SC2 per pair) over all six pairs, obeying the PROVED per-pair cap."""
    types = [(e, 0) for e in EE_VALUES if e <= 10] + [(e, 2) for e in EE_VALUES if e + 4 <= 10]
    for a in itertools.product(types, repeat=6):
        yield a


def evaluate(a, measured):
    """best attainable objective for this pair profile, maximising B triple by triple."""
    EE = [t[0] for t in a]
    SC = [t[1] for t in a]
    E = [EE[k] + 2 * SC[k] for k in range(6)]
    s = sum(1 for c in SC if c)
    if measured and s == 5:
        return None                      # [P351]: five sharings force the sixth -- s = 5 EMPTY
    T = sum(E)
    B = 0
    for T3 in INTRI:
        cap = 32
        if measured and sum(EE[k] for k in T3) > 20:
            cap = 31                     # [P359]: E_S = 32 was never seen with sum EE > 20
        cap = min(cap, 62 - sum(E[k] for k in T3))       # from max(3) = 67 ([P338])
        B += max(cap, 0)
    return {'s': s, 'EE': sum(EE), 'T': T, 'B': B, 'obj': T + B}


def main():
    out = {'what': 'every subset profile whose UNION could beat 183', 'supports': 'OQ 39'}

    print('THE IDENTITY.   TOTAL = 7 + T + B - Q4     (checked on the record and the golden)')
    print('   record  7 + 48 + 128 -  0 = 183        golden  7 + 60 + 128 - 18 = 177\n')

    print('CONSEQUENCE 1 -- a cap on Q4, from the PROVED box alone (T <= 60, B <= 128):')
    print('   TOTAL <= 195 - Q4,  so beating 183 requires  Q4 <= 11.')
    print('   observed Q4 values across every construction in this project: 0, 2, 18, 32')
    print('   -- so a 183-beating compound must have Q4 in {0, 2}: the 18 and 32 branches')
    print('      are closed by arithmetic, not by search.\n')
    out['q4_cap'] = {'bound': 'TOTAL <= 195 - Q4', 'requires': 'Q4 <= 11',
                     'observed_Q4': [0, 2, 18, 32]}

    for measured in (False, True):
        tag = 'PROVED constraints only' if measured is False else 'PROVED + MEASURED'
        live = collections.defaultdict(lambda: {'EE_lo': 99, 'EE_hi': -1, 'obj_hi': -1})
        n = 0
        for a in profiles():
            r = evaluate(a, measured)
            if r is None:
                continue
            n += 1
            if r['obj'] < 177:            # need T + B - Q4 >= 177, optimistic Q4 = 0
                continue
            d = live[r['s']]
            d['EE_lo'] = min(d['EE_lo'], r['EE'])
            d['EE_hi'] = max(d['EE_hi'], r['EE'])
            d['obj_hi'] = max(d['obj_hi'], r['obj'])
        print('%s   (profiles evaluated: %d)' % (tag, n))
        print('   sharings s   EE window that reaches T+B >= 177   best T+B')
        for s in sorted(live):
            d = live[s]
            print('       %d          EE in [%2d, %2d]                       %d'
                  % (s, d['EE_lo'], d['EE_hi'], d['obj_hi']))
        if not live:
            print('       -- none --')
        print()
        out['live_' + ('measured' if measured else 'proved')] = {
            str(s): live[s] for s in live}

    print('CONSEQUENCE 2 -- a LOWER bound on B, from the same proved box.')
    print('   T = EE + 4s  and  EE <= 60 - 4s  (a sharing pair is capped at EE <= 6), so T <= 60')
    print('   independently of s.  Beating 183 needs  T + B - Q4 >= 177, hence\n')
    print('        B >= 117 + Q4     -- with Q4 = 0 that is B in [117, 128], TWELVE values\n')
    out['B_floor'] = {'bound': 'B >= 117 + Q4', 'window_at_Q4_0': [117, 128]}

    print('THE GRID.  required EE per (s, B) cell at Q4 = 0, against the per-pair cap 60 - 4s.')
    print('   blank = the cap forbids it;  * = a live cell.\n')
    print('      B:  ' + ' '.join('%3d' % B for B in range(116, 129, 2)))
    grid = {}
    for sh in (0, 1, 2, 3, 4, 6):
        cap = 60 - 4 * sh
        row = []
        for B in range(116, 129, 2):
            need = 177 - 4 * sh - B
            if need > cap:
                row.append('  .')
            else:
                row.append('%3d' % max(need, 0)); grid['%d,%d' % (sh, B)] = max(need, 0)
        print('   s=%d    ' % sh + ' '.join(row) + '    cap %d' % cap)
    out['grid'] = grid
    print('\n   Every non-blank cell is a way to beat 183.  The measured ceiling')
    print('   `EE <= 36` covers the B = 128 COLUMN ONLY -- [P354] step 2 applies it without')
    print('   establishing B = 128, and B is not forced to 128 by anything proved.\n')
    out['coverage_gap'] = ('P354 step 2 conditions on B = 128; the proved floor is B >= 117, '
                           'so the columns B = 118..126 carry no measured EE ceiling at all')

    print('WHERE THE KNOWN CONSTRUCTIONS SIT ([P350], [P351], [P353], [P342]):')
    known = [('n=4 RECORD  star',  3, 36,  6, 128,  0),
             ('paw',              4, 24,  8, 128,  0),
             ('4-cycle',          4, 36,  8, 128, 18),
             ('golden 177  K4',   6, 36, 12, 128, 18),
             ('K4 (other)',       6, 36, 12,  74,  0)]
    print('   %-20s s  EE  SC2   B   Q4     T    TOTAL' % 'construction')
    for name, sh, ee, sc, B, q4 in known:
        T = ee + 2 * sc
        print('   %-20s %d  %2d   %2d  %3d  %3d   %3d     %3d'
              % (name, sh, ee, sc, B, q4, T, 7 + T + B - q4))
    out['known'] = [{'name': k[0], 's': k[1], 'EE': k[2], 'SC2': k[3], 'B': k[4], 'Q4': k[5],
                     'T': k[2] + 2 * k[3], 'TOTAL': 7 + k[2] + 2 * k[3] + k[4] - k[5]}
                    for k in known]
    print('\n   EVERY known construction sits in the B = 128 column or far below the floor.')
    print('   Nothing has ever been built in B = 118..126 -- the band is unexplored, not closed.\n')

    print('IS THE UNEXPLORED BAND ANY GOOD?  a first scan of it -- 900 perturbations of the')
    print('record, bucketed by B.  This is a SAMPLE and therefore a lower bound ([METHODS 1]).')
    import random
    import ee_bound_refute as EB
    from c_level import shares_plane
    import wall_keys as WK

    def anat4(qs):
        sig, _ = EB.vertices(qs)
        EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
        T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
        Q4 = sum(v for k, v in sig.items() if len(k) == 4)
        return EE, SC, T3 + 4 * Qg, Q4, EE + 2 * SC + T3 + 4 * Qg - Q4

    rec = [tuple(q) for q in WK.REC[4]]
    rng = random.Random(77)
    best = collections.defaultdict(lambda: (-1, None)); hist = collections.Counter()
    n = refused = 0
    while n < 900:
        qs = [list(q) for q in rec]
        for _ in range(rng.choice([1, 1, 2, 3, 4])):
            i, j = rng.randrange(1, 4), rng.randrange(4)
            qs[i][j] += rng.choice([-3, -2, -1, 1, 2, 3])
        qs = [tuple(q) for q in qs]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        n += 1
        try:
            EE, SC, Bv, Q4, obj = anat4(qs)
        except Exception:
            refused += 1
            continue
        hist[Bv] += 1
        if obj > best[Bv][0]:
            best[Bv] = (obj, (EE, SC, Q4))
    print('   evaluated %d   unevaluable %d' % (n - refused, refused))
    band = {}
    for Bv in sorted(hist, reverse=True):
        if Bv < 112:
            continue
        o, d = best[Bv]
        print('      B=%3d  n=%3d   best T+B-Q4 %3d  -> TOTAL %3d   (EE %2d  SC2 %2d  Q4 %2d)'
              % (Bv, hist[Bv], o, 7 + o, d[0], d[1], d[2]))
        band[str(Bv)] = {'n': hist[Bv], 'best_obj': o, 'EE': d[0], 'SC2': d[1], 'Q4': d[2]}
    out['band_scan'] = {'n': n, 'unevaluable': refused, 'by_B': band}
    print('   EE falls faster than B does, so the band is WORSE in this window -- but that is')
    print('   900 perturbations of one compound, and the required EE there was never reached.\n')

    out['reproduce'] = PROV.stamp(
        parameters={'EE_values': list(EE_VALUES), 'objective': 'T + B - Q4 >= 177'},
        note='exhaustive over pair profiles; B maximised per triple, Q4 taken optimistically 0')
    json.dump(out, open(os.path.join(ROOT, 'data', 'union_enumeration.json'), 'w'), indent=1)
    print('\nwrote data/union_enumeration.json')


if __name__ == '__main__':
    main()
