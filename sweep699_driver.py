import sys, subprocess, json, time
sys.path.insert(0,'/Users/dmi/carroll')
from concurrent.futures import ProcessPoolExecutor
from slide3_search import overlay_quats, farey, fits_cap, LOG_PATH
ENGINE='/Users/dmi/carroll/cube_regions'
thetas=farey(16)
diagR=[(1,1,1,1),(2,1,1,1),(3,1,1,1),(4,1,1,1),(5,1,1,1),(5,2,2,2),(7,2,2,2),(7,3,3,3),(8,3,3,3),(9,4,4,4),(4,3,3,3),(3,2,2,2)]
jobs=[]
for (p1,q1) in thetas:
    for (p2,q2) in thetas:
        for R in diagR:
            q=overlay_quats(q1,p1,q2,p2,R)
            if fits_cap(q):
                jobs.append(({'phase':'P3b','q1':q1,'p1':p1,'q2':q2,'p2':p2,'R':list(R)},q))
def run(chunk):
    inp='\n'.join(';'.join(','.join(map(str,g)) for g in q) for _,q in chunk)+'\n'
    out=subprocess.run([ENGINE,'--quats-stdin'],input=inp,capture_output=True,text=True).stdout.strip().split('\n')
    recs=[]
    for (meta,quats),line in zip(chunk,out):
        r=json.loads(line)
        if 'error' in r: 
            o=dict(meta);o['error']=r['error'];recs.append(o);continue
        o=dict(meta);o['quats']=r['quats'];o['total']=r['bounded'];o['by_depth']={int(k):v for k,v in r['by_depth'].items()};recs.append(o)
    return recs
def chunk(l,n):
    k=(len(l)+n-1)//n; return [l[i:i+k] for i in range(0,len(l),k)]
t0=time.time()
allr=[]
with ProcessPoolExecutor(max_workers=4) as ex:
    for recs in ex.map(run, chunk(jobs,64)):
        allr.extend(recs)
with open(LOG_PATH,'a') as f:
    for r in allr: f.write(json.dumps(r)+'\n')
good=[r for r in allr if 'error' not in r]
good.sort(key=lambda r:-r['total'])
print(f"P3b done {len(good)} evals {time.time()-t0:.0f}s. top:")
for r in good[:15]:
    print(r['total'], f"th1={r['p1']}/{r['q1']} th2={r['p2']}/{r['q2']} R={r['R']}", r['by_depth'])
print("max total:", good[0]['total'])
