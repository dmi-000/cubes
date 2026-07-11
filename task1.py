#!/usr/bin/env python3
"""Task 1: global (1,1,1)-diagonal fine sweep.
  P3c: Farey(16)^2 theta x farey(10) R
  P3d: (Farey(20)^2 \ Farey(16)^2) theta x farey(8) R  (only new-in-20 pairs)
"""
import sys
sys.path.insert(0, '/Users/dmi/carroll')
sys.path.insert(0, '/tmp')
from slide3_search import farey, gcd_reduce
from sweep import run


def rgrid(n):
    return [tuple(gcd_reduce([q, p, p, p])) for (p, q) in farey(n)]


def build_full(tn, rn):
    tg = farey(tn)
    rg = sorted(set(rgrid(rn)))
    jobs = []
    for (p1, q1) in tg:
        for (p2, q2) in tg:
            for R in rg:
                meta = dict(q1=q1, p1=p1, q2=q2, p2=p2, R=list(R))
                jobs.append((meta, (q1, p1, q2, p2, R)))
    return jobs, len(tg), len(rg)


def build_new(tn_big, tn_small, rn):
    tg_big = farey(tn_big)
    small = set(farey(tn_small))
    rg = sorted(set(rgrid(rn)))
    jobs = []
    for i, (p1, q1) in enumerate(tg_big):
        for (p2, q2) in tg_big:
            # include pair if at least one theta is new-in-big
            if (p1, q1) in small and (p2, q2) in small:
                continue
            for R in rg:
                meta = dict(q1=q1, p1=p1, q2=q2, p2=p2, R=list(R))
                jobs.append((meta, (q1, p1, q2, p2, R)))
    return jobs, len(tg_big), len(rg)


if __name__ == '__main__':
    phase = sys.argv[1] if len(sys.argv) > 1 else 'P3c'
    if phase == 'P3c':
        jobs, nt, nr = build_full(16, 10)
        print(f'P3c Farey(16)^2 x farey(10)R: theta={nt} R={nr} jobs={len(jobs)}')
        run(jobs, 'P3c', chunk_mult=10)
    elif phase == 'P3d':
        jobs, nt, nr = build_new(20, 16, 8)
        print(f'P3d Farey(20)\\(16) x farey(8)R: theta={nt} R={nr} jobs={len(jobs)}')
        run(jobs, 'P3d', chunk_mult=10)
