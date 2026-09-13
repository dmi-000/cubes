#!/usr/bin/env python3
"""Read the wall census and ask what PREDICTS a count change.

[OPEN_QUESTIONS 33] asks two things and this answers the second only if the data
supports it: (a) which walls bound the count plateau, (b) is there a readable
criterion -- from the group's cube indices, the condition type, the degree -- that
says in advance which ones do.

WHAT IS ADDED HERE.  The census records the count on either side of each crossing.
For a crossing at a RATIONAL parameter the count ON the wall is also computable,
and it is the more interesting number: at the 727 record itself the count is HIGHER
on the wall than on either side, so a coincidence can create regions rather than
destroy them.  Irrational crossings cannot be evaluated in rational arithmetic and
are counted as unevaluated, never scored as "no change".

EVERY RATE BELOW IS OVER THE CROSSINGS THESE RAYS MEET.  That is a population, not
a theorem: a rate of "k of m walls preserve the count" is a statement about m
solved crossings and nothing wider.  It is a lower bound on the phenomenon's
prevalence and not an estimate of a probability.
"""
import sys, os, json, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import dimension as D
import wall_census as C


def add_on_wall(doc, limit=None):
    """Count exactly ON each rational crossing.  Cached in the document."""
    quats = [tuple(q) for q in doc['quats']]
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    n = len(quats)
    done = 0
    for label, ray in doc['rays'].items():
        dirn = [F(x) for x in ray['direction']]
        for cr in ray['crossings']:
            if 'count_on' in cr:
                continue
            if cr['rational'] is None:
                cr['count_on'] = None
                cr['count_on_note'] = 'irrational parameter: not evaluable exactly'
                continue
            s = F(cr['rational'])
            cr['count_on'] = D.count_at([pt[k] + s * dirn[k] for k in range(len(pt))], n)
            done += 1
            if limit and done >= limit:
                return done
    return done


def rows(doc, attributable_only=True):
    for label, ray in doc['rays'].items():
        for cr in ray['crossings']:
            if attributable_only and cr.get('n_walls') != 1:
                continue
            yield label, ray, cr


def report(doc):
    att = [(l, r, c) for l, r, c in rows(doc)]
    ch = [c for _, _, c in att if c['changes'] is True]
    pr = [c for _, _, c in att if c['changes'] is False]
    un = [c for _, _, c in att if c['changes'] is None]
    print('RAYS %d | crossings %d | attributable to ONE wall %d'
          % (len(doc['rays']),
             sum(r['n_crossings'] for r in doc['rays'].values()), len(att)))
    print('   count CHANGES   %4d' % len(ch))
    print('   count PRESERVED %4d' % len(pr))
    print('   UNEVALUATED     %4d   (engine refusal or a window edge -- not "no change")'
          % len(un))
    tot = len(ch) + len(pr)
    if tot:
        print('   => %d of %d solved single-wall crossings PRESERVE the count (%.0f%%)'
              % (len(pr), tot, 100.0 * len(pr) / tot))

    print('\nG2 constancy failures per ray (any nonzero invalidates that ray):')
    bad = {l: r['constancy_failures'] for l, r in doc['rays'].items()
           if r['constancy_failures']}
    print('   ', bad if bad else 'none')
    ue = sum(r['unevaluable_intervals'] for r in doc['rays'].values())
    print('unevaluable intervals (engine refusals): %d' % ue)

    print('\nDELTA distribution on count-changing crossings:')
    for d, k in sorted(collections.Counter(c['delta'] for c in ch).items()):
        print('   %+4d  %d' % (d, k))

    def split(fn, name):
        tab = collections.defaultdict(lambda: [0, 0])
        for _, _, c in att:
            if c['changes'] is None:
                continue
            tab[fn(c)][0 if c['changes'] else 1] += 1
        print('\n%s:' % name)
        for k in sorted(tab, key=str):
            a, b = tab[k]
            print('   %-28s changes %3d | preserves %3d   (%.0f%% preserve)'
                  % (k, a, b, 100.0 * b / (a + b)))

    split(lambda c: c['conditions'][0]['size'], 'by GROUP SIZE (1 = one normal, 2 = pair)')
    split(lambda c: c['conditions'][0]['degree'], 'by POLYNOMIAL DEGREE on the ray')
    split(lambda c: c['conditions'][0]['tight_at_base'], 'by TIGHT AT THE RECORD')
    split(lambda c: c['n_conditions'], 'by NUMBER OF CONDITION RECORDS at the crossing')
    split(lambda c: c['conditions'][0]['sign_change'], 'by SIGN CHANGE (false = touched, not crossed)')
    split(lambda c: len(c['conditions'][0]['cubes']), 'by NUMBER OF CUBES in the condition')
    split(lambda c: tuple(c['conditions'][0]['cubes']), 'by CUBE SET')

    on = [c for _, _, c in att if c.get('count_on') is not None]
    if on:
        print('\nON the wall, for the %d rational crossings evaluated:' % len(on))
        pat = collections.Counter()
        for c in on:
            b, o, a = c['count_before'], c['count_on'], c['count_after']
            if None in (b, a):
                continue
            if b == a == o:
                pat['flat: on-wall count equals both sides'] += 1
            elif b == a and o > b:
                pat['PUNCTURE: same both sides, HIGHER on the wall'] += 1
            elif b == a and o < b:
                pat['pinch: same both sides, LOWER on the wall'] += 1
            elif o == b or o == a:
                pat['step: on-wall count equals one side'] += 1
            else:
                pat['step with its own value on the wall'] += 1
        for k, v in pat.most_common():
            print('   %-46s %d' % (k, v))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    path = os.path.join(ROOT, 'data', 'wall_census_n%d.json' % n)
    doc = json.load(open(path))
    got = add_on_wall(doc)
    if got:
        json.dump(doc, open(path, 'w'), indent=1)
        print('counted ON the wall at %d new rational crossings (cached)\n' % got)
    report(doc)


if __name__ == '__main__':
    main()
