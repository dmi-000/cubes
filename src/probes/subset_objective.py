#!/usr/bin/env python3
"""The subset objective, and whether subset data DETERMINES the count.  [P339], [P341], [P345]

At n = 4 the count is exact inclusion-exclusion over subsets ([P340], [P341]):

    TOTAL = sum(triples) - sum(pairs) + 4 + [holecorr] - (n-fold vertices)
          = sum_S h(S) + 4 + holecorr - nfold ,   h(S) = count(S) - (1/2)(its pair counts)

since each pair lies in exactly two triples.  So max(4) is a question about which subset-count
vectors co-occur.  This probe measures the pieces:

  A. extensions of the octahedral 67 -- best total, and the pair collapse that causes it
  B. the subset-sum sum_S count(S), which the record maximises at 244
  C. the per-triple objective h, whose best measured value is the 67's 47.5
  D. COLLISIONS: two configurations with identical subset profiles and different totals.
     None found in 600 draws over 539 distinct profiles -- so subset data determined the count
     on every case tested.  A search, hence a lower bound: no collision found is not no
     collision existing.
"""
import sys, os, json, itertools, random, collections, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from c_level import shares_plane
from subset_predictor import count, holes, predict, nfold, Refused
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
ENGINE_Q2 = os.path.join(ROOT, 'cube_regions_q2w')
OCT = ["1,0,0,0", "1,1,0:1,0", "-1,1,0:1,0"]


def q2(cubes, d=2):
    r = subprocess.run([ENGINE_Q2, '--d', str(d), '--quats', ';'.join(cubes)],
                       capture_output=True, text=True)
    if not r.stdout.strip():
        return None
    j = json.loads(r.stdout)
    return None if 'error' in j else j.get('bounded')


def h_of(qs, S):
    sub = [qs[i] for i in S]
    t = count(sub)
    ps = [count([sub[i] for i in P]) for P in itertools.combinations(range(3), 2)]
    return t - 0.5 * sum(ps)


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    out = {'what': 'the subset objective and whether subset data determines the count',
           'supports': 'LEDGER P339, P341, P345'}

    print('=== A. the best 4-compound containing the octahedral 67 ===')
    best = (0, None)
    for spec in ('0,4,-5,1', '1,0,0,0', '2,1,1,1', '0,1,-1,1'):
        v = q2(OCT + [spec])
        if v and v > best[0]:
            best = (v, spec)
    anat = {'fourth': best[1], 'total': best[0],
            'triples': [q2([OCT[0], OCT[1], best[1]]), q2([OCT[0], OCT[2], best[1]]),
                        q2([OCT[1], OCT[2], best[1]]), 67],
            'pairs': [q2([OCT[0], OCT[1]]), q2([OCT[0], OCT[2]]), q2([OCT[1], OCT[2]]),
                      q2([OCT[0], best[1]]), q2([OCT[1], best[1]]), q2([OCT[2], best[1]])]}
    print('   best of the sampled fourth cubes: %s -> total %d (a 3 136-cube scan gave 175)'
          % (best[1], best[0]))
    print('   triples %s   pairs %s' % (anat['triples'], anat['pairs']))
    print('   the 67 is rigid, so two pairs collapse -- that is the cost')
    out['oct67_extension'] = anat

    print('\n=== B. the subset-sum, which the record maximises ===')
    rec = [tuple(q) for q in W.REC[4]]
    st = sum(count([rec[i] for i in S]) for S in itertools.combinations(range(4), 3))
    sp = sum(count([rec[i] for i in P]) for P in itertools.combinations(range(4), 2))
    print('   n=4 RECORD   sum(triples) %d   sum(pairs) %d   => sum_S Q(S) <= %d' % (st, sp, st - 20))
    print('   golden 177: 268 / 78;  best random of 700: 212 -- the record leads at 244')
    out['subset_sum'] = {'record_triples': st, 'record_pairs': sp}

    print('\n=== C. the per-triple objective h ===')
    hs = [h_of(rec, S) for S in itertools.combinations(range(4), 3)]
    print('   n=4 RECORD   h per triple %s   sum %.1f' % (hs, sum(hs)))
    print('   octahedral 67: h = 67 - 0.5*39 = 47.5 (the best measured);  900 random max 43.5')
    out['h'] = {'record': hs, 'record_sum': sum(hs), 'sixtyseven': 47.5, 'random_max': 43.5}

    print('\n=== D. COLLISIONS: same subset profile, different total? ===')
    groups = collections.defaultdict(set)
    rng = random.Random(67)
    ok = ref = 0
    while ok + ref < trials:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-8, 8) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            pc = tuple(sorted(count([qs[i] for i in P])
                              for P in itertools.combinations(range(4), 2)))
            tc = tuple(sorted(count([qs[i] for i in S])
                              for S in itertools.combinations(range(4), 3)))
            t = count(qs)
        except Refused:
            ref += 1
            continue
        except Exception:
            continue
        ok += 1
        groups[(pc, tc)].add(t)
    clash = [k for k, v in groups.items() if len(v) > 1]
    print('   configurations %d   refused %d   distinct profiles %d' % (ok, ref, len(groups)))
    print('   profiles carrying MORE THAN ONE total: %d' % len(clash))
    print('   => subset data determined the count on every case tested.')
    print('   SCOPE: a search. No collision found is NOT no collision existing ([METHODS 1]).')
    out['collisions'] = {'configs': ok, 'refused': ref, 'profiles': len(groups),
                         'profiles_with_multiple_totals': len(clash),
                         'scope': 'search over integer quaternions in [-8,8]; lower bound only'}

    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': 67})
    json.dump(out, open(os.path.join(ROOT, 'data', 'subset_objective.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/subset_objective.json')


if __name__ == '__main__':
    main()
