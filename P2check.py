   import sys, subprocess, json
   sys.path.insert(0,'.')
   from slide3_search import overlay_quats, fits_cap, LOG_PATH
  
   lines=[]
   metas=[]
   # theta fixed at winner cell (8,3),(5,2); R=(a,1,1,1) sweep + (a,-1,-1,-1)
   for a in list(range(1,41)):
       for s in (1,-1):
           R=(a,s,s,s)
           quats=overlay_quats(8,3,5,2,R)
           if not fits_cap(quats): continue
           metas.append({'phase':'P3probe','q1':8,'p1':3,'q2':5,'p2':2,'R':list(R)})
           lines.append(';'.join(','.join(map(str,g)) for g in quats))
   inp='\n'.join(lines)+'\n'
   out=subprocess.run(['./cube_regions','--quats-stdin'],input=inp,capture_output=True,text=True).stdout.strip().split('\n')
   import math
   res=[]
   logf=open(LOG_PATH,'a')
   for meta,line in zip(metas,out):
       rec=json.loads(line)
       if 'error' in rec:
           r=dict(meta); r['error']=rec['error']; logf.write(json.dumps(r)+'\n'); continue
       total=rec['bounded']
       a=meta['R'][0]; s=meta['R'][1]
       ang=2*math.degrees(math.atan2(math.sqrt(3),a))*s
       r=dict(meta); r['quats']=rec['quats']; r['total']=total
       r['by_depth']={int(k):v for k,v in rec['by_depth'].items()}
       logf.write(json.dumps(r)+'\n')
       res.append((s,a,ang,total))
   logf.close()
   res.sort()
   for s,a,ang,total in res:
       print(f"R=({a},{s},{s},{s}) angle={ang:7.2f}deg  total={total}")
   EOF
