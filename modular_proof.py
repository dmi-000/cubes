#!/usr/bin/env python3
"""Prove (or refute) that 393's flat is MODULAR in the 727 lattice.

P156 verified a CONSEQUENCE of modularity -- every 393 chamber cut into exactly
62 -- on 25 of 74 544 chambers.  That is evidence, not proof, and the converse
does not hold: uniform subdivision does not by itself imply modularity.  This
checks the definition directly.

X is modular iff for EVERY flat Y of L(A):

    rank(X) + rank(Y) = rank(X v Y) + rank(X ^ Y)

With flats represented as the CLOSED SET OF WALLS containing them (zaslavsky.Flats),
the lattice operations are concrete: X v Y = closure(X union Y), and X ^ Y =
X intersect Y -- the intersection of two closed sets is closed, so no closure is
needed on the meet.  Note the order convention: a LARGER wall-set is a SMALLER
subspace and a HIGHER rank.

X here is the flat of the 18 "old" walls -- the ones that project exactly onto
393's arrangement (P154).  A_X is therefore 393's arrangement, and Stanley's
modular factorisation theorem says modularity of X forces chi_{A_X} | chi_A,
which P155 observed as an exact fact without an explanation.  This supplies it.

The submodular inequality  rank(X)+rank(Y) >= rank(X v Y)+rank(X ^ Y)  holds in
any geometric lattice, so every failure is in one direction; the deficiency is
reported rather than just a boolean, because HOW modularity fails would say which
walls break it.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from zaslavsky import Flats, chambers

W, nc = walls_of(BASE + [(7, 14, 1, -5)])
n3 = 12
old = [i for i, w in enumerate(W) if all(x == 0 for x in w[n3:])]
print('727: %d walls, ambient %d | old(393) walls: %d' % (len(W), nc, len(old)), flush=True)

t0 = time.time()
print('enumerating flats via the chamber recursion...', flush=True)
n, states, nflats, secs = chambers(W, label='727:')
assert n == 4621728, 'chamber gate failed: %d' % n
print('  chamber gate PASS (4,621,728); %d flats reachable' % nflats, flush=True)

L = Flats(W)
# rebuild the flat set (the run above used its own Flats instance)
X, rX = L.closure_of_basis([]), 0
b = []
for i in old:
    L._add(b, L.w[i])
X = L.closure_of_basis(b)
rX = len(b)
print('X = closure(old walls): %d walls, rank %d' % (bin(X).count('1'), rX), flush=True)

def rank_of(mask):
    bb = []
    for j in range(L.m):
        if mask >> j & 1:
            L._add(bb, L.w[j])
    return len(bb)

# re-derive every flat, cheaply, by re-running the recursion on this instance
memo = {}
sys.setrecursionlimit(10000)
def N(i, flat):
    if i < 0: return 1
    k = (i, flat)
    if k in memo: return memo[k]
    if flat >> i & 1:
        memo[k] = 0; return 0
    r = N(i-1, flat) + N(i-1, L.extend(flat, i))
    memo[k] = r
    return r
N(L.m - 1, L.empty)
flats = sorted(L._basis)
print('%d flats collected (%.0fs)' % (len(flats), time.time()-t0), flush=True)

rank_cache = {}
def rk(mask):
    v = rank_cache.get(mask)
    if v is None:
        v = rank_of(mask); rank_cache[mask] = v
    return v

bad, checked, t1 = [], 0, time.time()
for Y in flats:
    rY = rk(Y)
    meet = X & Y
    bb = []
    for j in range(L.m):
        if (X | Y) >> j & 1:
            L._add(bb, L.w[j])
    join = L.closure_of_basis(bb)
    lhs = rX + rY
    rhs = rk(join) + rk(meet)
    checked += 1
    if lhs != rhs:
        bad.append({'Y_mask': Y, 'rank_Y': rY, 'lhs': lhs, 'rhs': rhs,
                    'deficiency': lhs - rhs})
        if len(bad) <= 5:
            print('   VIOLATION: rank(X)+rank(Y)=%d vs rank(XvY)+rank(X^Y)=%d '
                  '(deficiency %d)' % (lhs, rhs, lhs-rhs), flush=True)
    if checked % 100000 == 0:
        print('   %d/%d checked, %d violations (%.0fs)'
              % (checked, len(flats), len(bad), time.time()-t1), flush=True)

print('\n%d flats checked, %d violations' % (checked, len(bad)))
print('X IS MODULAR: %s' % ('PROVED' if not bad else 'REFUTED'))
json.dump({'n_flats': checked, 'n_violations': len(bad),
           'modular': not bad, 'first_violations': bad[:20],
           'secs': time.time()-t0},
          open(os.path.join(HERE, 'modular_proof.json'), 'w'), indent=1)
