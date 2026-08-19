#!/usr/bin/env python3
"""Does WALL STRUCTURE point toward records, when coincidence count and subset
spectrum do not?

Two candidate compasses are refuted. "More coincidences implies a higher count" is
in the REFUTED table (727 has 18 interior crossings to 723's 48 and counts more).
The subset spectrum is worse than useless as a pointer: the configuration with the
MAXIMAL possible spectrum at n = 4 -- every triple a 67, every pair a 13 -- counts
177, six BELOW the record (Postscript 135).

The wall system is what remains. Postscript 136 found the two non-congruent 183s
share 88 of their 108 wall labels. If wall-sharing with a record TRACKS the count,
it is a compass; if configurations at 175 share just as many, it is another
certificate.

TEST: the wide-perturbation campaign retained every configuration reaching >= 175.
Compute each one's tight wall labels and measure the overlap with the canonical
183's, index-invariantly (maximised over cube relabellings, since labels are
index-dependent -- Postscript 137).

PREDICTION IF WALLS ARE A COMPASS: overlap rises with count.
PREDICTION IF NOT:                  overlap is flat across 175 / 179 / 183.
Either outcome is informative, which is what makes it worth running.
"""
import itertools, os, sys
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from collections import defaultdict
from wall_sharing import labels

def relabel(L, perm):
    return {(perm[i], tuple(sorted((perm[c],k,s) for c,k,s in g))) for i,g in L}

def best_overlap(LA, LB, n):
    return max(len(relabel(LA,{i:p[i] for i in range(n)})&LB)
               for p in itertools.permutations(range(n)))

KNOWN=[(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
ref=labels(KNOWN,0)
print('canonical 183: %d wall labels'%len(ref),flush=True)

seen=set(); rows=[]
for l in open(os.path.join(HERE,'wideclimb_n4.log') if False else HERE+'/wideclimb_n4.log'):
    if 'CFG peak=' not in l: continue
    head,cfgs=l.split('CFG peak=')[1].split(' ',1)
    peak=int(head); c=tuple(tuple(int(x) for x in g.split(',')) for g in cfgs.strip().split(';'))
    if c in seen: continue
    seen.add(c); rows.append((peak,c))
print('%d distinct retained configurations'%len(rows),flush=True)

by=defaultdict(list)
for peak,c in rows:
    L=labels(list(c),0)
    ov=best_overlap(L,ref,4)
    by[peak].append((len(L),ov))
    print('   peak %3d: %3d labels, overlap with the 183 wall set %3d'%(peak,len(L),ov),flush=True)
print()
print('peak | configs | mean labels | mean overlap with 183 | overlap as %% of 108')
for p in sorted(by):
    v=by[p]; ml=sum(x[0] for x in v)/len(v); mo=sum(x[1] for x in v)/len(v)
    print('%4d |   %3d   |    %5.1f    |        %5.1f          |   %4.1f%%'
          %(p,len(v),ml,mo,100*mo/108))
