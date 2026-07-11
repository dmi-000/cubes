#!/usr/bin/env python3
import sys, math
sys.path.insert(0, '/Users/dmi/carroll')
sys.path.insert(0, '/tmp')
from slide3_search import farey, gcd_reduce, theta_deg
from sweep import run

# three base cells: (q1,p1,q2,p2,Rratio(p,q for b/a))
cells = [
    ('A', 3, 1, 9, 2, (2, 5)),   # th1=36.87 th2=25.06 R=(5,2,2,2)
    ('B', 9, 5, 12, 7, (1, 3)),  # th1=58.11 th2=60.51 R=(3,1,1,1)
    ('C', 11, 7, 2, 1, (2, 5)),  # th1=64.89 th2=53.13 R=(5,2,2,2)
]

FA = farey(24)          # theta candidates (p,q) -> tan(theta/2)=p/q
RFA = farey(20)         # R ratio candidates b/a=p/q -> R=(q,p,p,p)
TW = 6.0                # theta window +/- deg
RW = 0.14               # R ratio window +/-


def near_thetas(theta_c):
    out = []
    for (p, q) in FA:
        if abs(theta_deg(q, p) - theta_c) <= TW:
            out.append((q, p))
    return out


def near_Rs(ratio):
    rc = ratio[0] / ratio[1]
    out = []
    for (p, q) in RFA:
        if abs(p / q - rc) <= RW:
            out.append(tuple(gcd_reduce([q, p, p, p])))
    return sorted(set(out))


def build():
  jobs = []
  seen = set()
  for name, q1c, p1c, q2c, p2c, rr in cells:
    th1c = theta_deg(q1c, p1c)
    th2c = theta_deg(q2c, p2c)
    t1s = near_thetas(th1c)
    t2s = near_thetas(th2c)
    Rs = near_Rs(rr)
    print(f'cell {name}: th1c={th1c:.2f} th2c={th2c:.2f} |t1|={len(t1s)} |t2|={len(t2s)} |R|={len(Rs)} -> {len(t1s)*len(t2s)*len(Rs)}')
    for (q1, p1) in t1s:
      for (q2, p2) in t2s:
        for R in Rs:
          key = (q1, p1, q2, p2, R)
          if key in seen:
            continue
          seen.add(key)
          meta = dict(cell=name, q1=q1, p1=p1, q2=q2, p2=p2, R=list(R))
          jobs.append((meta, (q1, p1, q2, p2, R)))
  return jobs


if __name__ == '__main__':
  jobs = build()
  print('total jobs (dedup):', len(jobs))
  run(jobs, 'P3_local', chunk_mult=8)
