#!/usr/bin/env python3
"""The chamber WORD of a 727 continuum, computed exactly.

Postscript 67 classified the continua by their endpoints and found the
endpoints do not determine the line: three C3 orbits share the endpoint type
pair (4,6) with widths 0.5, 0.5 and 11.5, and chamber counts 14, 7 and 13. So
the interior is an independent invariant, and the right object is the ORDERED
SEQUENCE of chamber types along the line -- its word, of which the endpoints
are only the first and last letters.

WHY NOT SAMPLE.  A sampled word is resolution-dependent: any step misses
chambers narrower than itself, and the widths inside a single line span ~80x.
The chambers are instead computed EXACTLY: restrict every catalogue condition
to the line, take its exact roots inside the 727 stretch, and the chambers are
the intervals between consecutive roots.  Adjacent intervals whose type agrees
are merged -- a wall crossing that does not change the type is not a chamber
boundary (Postscript 58 measured that most crossings do not).

TWO CONVENTIONS, both forced by the geometry:
  * a line has no preferred direction, so the word is defined UP TO REVERSAL;
    the canonical form is min(word, reversed word).
  * types are canonicalised under the C3 relabelling of base cubes 0,1,2 --
    without that, congruent chambers get different letters and orbit-mates
    produce different words (the error that made 7 types look like 21).

GATE: members of a C3 orbit must produce the SAME word. They are congruent
line by line, so any disagreement is a bug in this file, not a finding.
"""
import collections
import json
import re
import subprocess
import sys
from fractions import Fraction as F

from continua import FIVE, FIXED_W, build_catalogues, restrict, to_quat
from continua_endpoints import roots_of, sign_surd


def perm_mask(m, k):
    out = m & ~0b111
    for s in range(3):
        if m >> s & 1:
            out |= 1 << ((s + k) % 3)
    return out


def canon(pl):
    forms = []
    for k in range(3):
        d = collections.defaultdict(int)
        for mask, v in pl.items():
            d[perm_mask(int(mask), k)] += v
        forms.append(json.dumps(sorted(d.items())))
    return min(forms)


def val(r):
    P, Q, D = r
    return float(P) + float(Q) * (D ** 0.5)


def cmp_rat(r, x):
    """sign of (P + Q sqrt D) - x for rational x -- exact."""
    P, Q, D = r
    return sign_surd(P - x, Q, D)


def counts(quats):
    inp = '\n'.join(FIXED_W + ';' + ','.join('%d:0' % v for v in q)
                    for q in quats) + '\n'
    out = subprocess.run(['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
                         input=inp, capture_output=True, text=True).stdout
    rows = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
    assert len(rows) == len(quats), (len(rows), len(quats))
    return rows


def word_of(li, a, b, cat, data):
    L = data['lines'][li]
    p0 = tuple(F(x) for x in L['p0'])
    dd = tuple(F(x) for x in L['dir'])
    roots = []
    for kind, polys in cat.items():
        for m in polys:
            co = restrict(m, p0, dd)
            if all(c == 0 for c in co) or len(co) < 2:
                continue
            rs = roots_of(co, a, b)
            if rs:
                roots.extend(rs)
    roots = sorted(set(roots), key=val)
    # sample strictly inside each gap
    bounds = [(a, None)] + [(None, r) for r in roots] + [(b, None)]
    pts, gaps = [], []
    prev = float(a)
    seq = [float(a)] + [val(r) for r in roots] + [float(b)]
    for i in range(len(seq) - 1):
        lo, hi = seq[i], seq[i + 1]
        if hi - lo < 1e-9:
            gaps.append(None)
            continue
        mid = F(round((lo + hi) / 2 * 10**6), 10**6)
        if not (lo < float(mid) < hi):
            gaps.append(None)
            continue
        q = to_quat(tuple(p0[u] + mid*dd[u] for u in range(3)), cap=10**9)
        gaps.append(q)
    live = [q for q in gaps if q]
    rows = counts(live) if live else []
    it = iter(rows)
    letters = []
    for q in gaps:
        if q is None:
            letters.append(None)
            continue
        d = next(it)
        letters.append(canon(d['per_label']) if d.get('bounded') == 727 else '.')
    # merge adjacent equal letters
    word = []
    for x in letters:
        if not word or word[-1] != x:
            word.append(x)
    return roots, letters, word


def main():
    which = [int(x) for x in sys.argv[1:]] or [9, 37, 88, 12, 24]
    cat = build_catalogues()
    data = json.load(open('typology_data.json'))
    runs = {}
    for l in open('continua_phaseA.out'):
        m = re.match(r'^line\s+(\d+): (\d+) continua \[(.*)\]', l)
        if m:
            rr = re.findall(r"'([-\d.]+)\.\.([-\d.]+)'", m.group(3))
            if rr:
                runs[int(m.group(1))] = (F(rr[0][0]), F(rr[0][1]))
    alpha = {}
    out = {}
    for li in which:
        if li not in runs:
            print('line %d carries no continuum' % li)
            continue
        a, b = runs[li]
        roots, letters, word = word_of(li, a, b, cat, data)
        for x in word:
            if x not in (None, '.') and x not in alpha:
                alpha[x] = len(alpha)
        shown = [alpha.get(x, x if x in (None, '.') else '?') for x in word]
        rev = shown[::-1]
        canon_word = min(str(shown), str(rev))
        out[li] = canon_word
        print('line %3d  t in [%s, %s]: %d exact wall crossings, %d chambers'
              % (li, a, b, len(roots), len(word)))
        print('     word %s' % shown)
    print('\nC3 gate -- orbit-mates must give the same word:')
    groups = collections.defaultdict(list)
    for li, w in out.items():
        groups[w].append(li)
    for w, ls in groups.items():
        print('   lines %-16s word %s' % (ls, w[:70]))


if __name__ == '__main__':
    main()
