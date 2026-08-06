#!/usr/bin/env python3
"""Name a plateau end exactly: solve for the wall roots, then binary-search the
ROOT LIST rather than the real line.

Bisecting a real interval costs one engine call per bit and stops when the
quaternions overflow.  The count is constant BETWEEN consecutive wall roots, so
with the roots in hand the end is found in log2(#roots) calls, each at a
comfortable rational, and the answer is the root itself -- exact -- not a
bracket.
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from solve_ends import catalogue, count, q_of, BASE
sys.path.insert(0, "/Users/dmi/cube-compounds")
import wall_params as W

def between(a, b):
    """a small-denominator rational strictly between a < b"""
    for D in (2**k for k in range(1, 40)):
        m = F(round(float(a+b)/2*D), D)
        if a < m < b:
            return m
    return (a+b)/2

def pin(base, a0, d, lo, hi, target, label):
    pts, lines = catalogue(base)
    roots = sorted(set([s for s in W.w4_params(a0, d, pts) if lo < s < hi] +
                       [s for s in W.w3_params(a0, d, lines) if lo < s < hi]))
    kind = {}
    for s in W.w4_params(a0, d, pts): kind[s] = 'W4'
    for s in W.w3_params(a0, d, lines): kind.setdefault(s, 'W3')
    def C(s):
        return count(base+[q_of([a0[i]+s*d[i] for i in range(3)])])
    pos = [lo]+roots+[hi]
    clo, chi = C(lo), C(hi)
    print('%s: %d wall roots in the bracket; count %s at %s, %s at %s'
          % (label, len(roots), clo, float(lo), chi, float(hi)), flush=True)
    if (clo == target) == (chi == target):
        print('   bracket does not straddle the end'); return None
    i, j = 0, len(pos)-1          # count(pos[i]) side == target
    if clo != target: i, j = j, i
    while abs(i-j) > 1:
        k = (i+j)//2
        m = between(pos[k], pos[k+1]) if k+1 < len(pos) else pos[k]
        c = C(m)
        print('   probe %.12f -> %s' % (float(m), c), flush=True)
        if c == target: i = k if i < j else k+1
        else: j = k if i < j else k+1
        if i < j: i, j = min(i, j), max(i, j)
        else: i, j = max(i, j), min(i, j)
    end = pos[max(min(i, j), 1)-0] if False else roots[min(i, j) if min(i, j) < len(roots) else -1]
    return roots, kind

if __name__ == '__main__':
    pass
