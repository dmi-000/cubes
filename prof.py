import sys, cProfile, pstats, io, signal
sys.path.insert(0,'/Users/dmi/cube-compounds')
import sympy as sp, dimension as D
from subset_topology import RECORDS
Q = RECORDS[7]
cfg = [Q[i] for i in (0,2,4,6)]          # the n=7 k=4 class shard 3 is on
D.QZERO[:] = [cfg[0]]
pt = D.point_of(cfg); n = len(cfg)
vars_ = sp.symbols('c0:%d' % (3*(n-1)))
Rs = D.frames(vars_, cfg[0])
def run(): D.conditions(Rs, n, vars_, pt, D.quats_of(pt, cfg[0]))
def onalarm(*a): raise KeyboardInterrupt
signal.signal(signal.SIGALRM, onalarm); signal.alarm(150)
pr = cProfile.Profile(); pr.enable()
try: run()
except KeyboardInterrupt: pass
pr.disable()
s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(12)
print('\n'.join(s.getvalue().split('\n')[4:20]))
