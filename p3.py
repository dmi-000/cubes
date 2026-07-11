   import sys, math
   sys.path.insert(0,'.')
   from slide3_search import overlay_quats, hamilton, gcd_reduce
   from itertools import combinations

   def qconj(q): return (q[0],-q[1],-q[2],-q[3])

   def canon(q):
       q = gcd_reduce(list(q))
       # canonical sign: first nonzero positive
       for c in q:
           if c!=0:
               if c<0: q=[-x for x in q]
               break
       return tuple(q)

   configs = {
    'A': (7,2,2,1,(4,-1,-1,-1)),
    'B': (8,3,5,2,(2,1,1,1)),
    'C': (7,4,5,3,(3,1,1,1)),
    'D': (2,1,8,5,(4,1,1,1)),
   }
   for name,(q1,p1,q2,p2,R) in configs.items():
       quats = overlay_quats(q1,p1,q2,p2,R)
       print(f"--- config {name}: {quats}")
       for i,j in combinations(range(6),2):
           qi, qj = quats[i], quats[j]
           rel_body = canon(hamilton(qconj(qi), qj))   # qi^-1 * qj
           n = sum(c*c for c in rel_body)
           w = rel_body[0]
           # angle
           ang = 2*math.degrees(math.acos(max(-1,min(1, w/math.sqrt(n)))))
           # special forms
           note=''
           v = sorted(abs(c) for c in rel_body[1:])
           if v[0]==v[1]==v[2]!=0:
               note += ' DIAG-AXIS'
               if abs(w)==3*v[0]: note+=' 60deg-own-diagonal(pair13)'
               if abs(w)==v[0]: note+=' 120deg(cube-sym)'
           if v[0]==0 and v[1]==0:
               note += ' FACE-AXIS'
           if v[0]==0 and v[1]==v[2]:
               note += ' EDGE-AXIS'
           print(f"  pair({i},{j}): rel={rel_body} ang={ang:7.2f}{note}")
   EOF
