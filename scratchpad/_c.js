
const DEPTH_COLORS=['#07090c','#420a68','#932667','#dd513a','#fca50a','#f2d24b','#fcffa4'];
const $=id=>document.getElementById(id);
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---- presets. Matrices are row-major floats; the exact region counts are
// theorems from the exact counters (this viewer samples, so it shows the
// depth GEOMETRY of a sqrt(n) compound but cannot itself count regions). ----
const REC723_TXT=`4,1,1,-1
3,3,7,3
5,-1,-5,-5
2,1,1,1
1,1,1,1
5,2,2,2`;
const OCTA=[
 [[1,0,0],[0,0.707107,-0.707107],[0,0.707107,0.707107]],
 [[0.707107,0,0.707107],[0,1,0],[-0.707107,0,0.707107]],
 [[0.707107,-0.707107,0],[0.707107,0.707107,0],[0,0,1]]];
const GOLDEN=[
 [[1,0,0],[0,1,0],[0,0,1]],
 [[0.809017,-0.5,-0.309017],[0.309017,0.809017,-0.5],[0.5,0.309017,0.809017]],
 [[0.809017,-0.5,-0.309017],[-0.309017,-0.809017,0.5],[0.5,0.309017,0.809017]],
 [[-0.809017,0.5,0.309017],[0.309017,0.809017,-0.5],[0.5,0.309017,0.809017]],
 [[-0.809017,0.5,0.309017],[-0.309017,-0.809017,0.5],[0.5,0.309017,0.809017]]];
const matText=mats=>mats.map(M=>M.flat().map(x=>(+x.toFixed(6)).toString()).join(',')).join('\n');

// ---- the 67<->67 sliding family (Postscript 9 / SLIDE3_SPEC_V2):
// T(t) = { S(t), C·S(t), C²·S(t) },  C = 120° about (1,1,1),
// S(t) = R(AXIS, t·DELTA)·S_OCT.  t=0: octahedral compound (√2, count 67);
// t=1: golden 3-cycle triple (√5, count 67); interior: generic ≈37.
// Constants validated against the exact engines (delta = 40.306°).
const S_OCT=[[1,0,0],[0,0.7071068,-0.7071068],[0,0.7071068,0.7071068]];
const C3=[[0,0,1],[1,0,0],[0,1,0]];
const SLIDE_AXIS=[-0.442177,-0.828653,0.343239];
const SLIDE_DELTA=40.3060*Math.PI/180;
function matMul(A,B){
  const R=[[0,0,0],[0,0,0],[0,0,0]];
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)
    R[i][j]=A[i][0]*B[0][j]+A[i][1]*B[1][j]+A[i][2]*B[2][j];
  return R;
}
function rodrigues(a,th){
  const K=[[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]];
  const K2=matMul(K,K), s=Math.sin(th), c1=1-Math.cos(th);
  const R=[[1,0,0],[0,1,0],[0,0,1]];
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)R[i][j]+=s*K[i][j]+c1*K2[i][j];
  return R;
}
function slideMats(t){
  const S=matMul(rodrigues(SLIDE_AXIS,t*SLIDE_DELTA),S_OCT);
  return [S, matMul(C3,S), matMul(C3,matMul(C3,S))];
}

function quatToCols(q){
  let [w,x,y,z]=q, n=w*w+x*x+y*y+z*z;
  return [
    [(w*w+x*x-y*y-z*z)/n, 2*(x*y+w*z)/n, 2*(x*z-w*y)/n],
    [2*(x*y-w*z)/n, (w*w-x*x+y*y-z*z)/n, 2*(y*z+w*x)/n],
    [2*(x*z+w*y)/n, 2*(y*z-w*x)/n, (w*w-x*x-y*y+z*z)/n]
  ];
}
// row-major rotation matrix -> [col0,col1,col2] (the face normals)
const matToCols=M=>[[M[0][0],M[1][0],M[2][0]],[M[0][1],M[1][1],M[2][1]],[M[0][2],M[1][2],M[2][2]]];

let cubes=[];            // array of N [col0,col1,col2]
let exactInfo=null;      // {total, d:{depth:count}} when a preset is loaded
function parseConfig(txt, mode){
  const rows=txt.trim().split(/\n+/).map(r=>r.trim()).filter(Boolean);
  if(rows.length<2||rows.length>8) throw `need 2–8 cubes, got ${rows.length}`;
  return rows.map((r,i)=>{
    const v=r.split(/[,\s]+/).map(Number);
    if(mode==='quat'){
      if(v.length!==4||v.some(isNaN)) throw `line ${i+1}: need 4 numbers w,x,y,z`;
      if(v.every(c=>c===0)) throw `line ${i+1}: quaternion is zero`;
      return quatToCols(v);
    }
    if(v.length!==9||v.some(isNaN)) throw `line ${i+1}: need 9 numbers (row-major 3×3)`;
    return matToCols([[v[0],v[1],v[2]],[v[3],v[4],v[5]],[v[6],v[7],v[8]]]);
  });
}

// membership: which cubes contain point p -> bitmask; depth = popcount
function labelAt(p){
  let m=0;
  for(let k=0;k<cubes.length;k++){
    const c=cubes[k];
    if(Math.abs(c[0][0]*p[0]+c[0][1]*p[1]+c[0][2]*p[2])<1 &&
       Math.abs(c[1][0]*p[0]+c[1][1]*p[1]+c[1][2]*p[2])<1 &&
       Math.abs(c[2][0]*p[0]+c[2][1]*p[1]+c[2][2]*p[2])<1) m|=1<<k;
  }
  return m;
}
const popcount=m=>{let c=0;while(m){c+=m&1;m>>=1;}return c;};

// ---- visibility filters (reduce clutter: isolate depths and/or cubes) ----
let depthSel=new Set([1,2,3,4,5,6]);      // which depths to show
let cubeSel=63;                            // bitmask of cubes to show (all six)
function visible(mask,dep){ return dep>0 && depthSel.has(dep) && (mask&cubeSel)!==0; }

// ---- colour helpers ----
function hex2rgb(h){return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];}
function hslToRgb(h,s,l){
  h/=360;const a=s*Math.min(l,1-l);
  const f=n=>{const k=(n+h*12)%12;return Math.round(255*(l-a*Math.max(-1,Math.min(k-3,9-k,1))));};
  return [f(0),f(8),f(4)];
}
const DEPTH_RGB=DEPTH_COLORS.map(hex2rgb);
const BG_RGB=[7,9,12];
const labelRgbCache=new Array(64);      // distinct hue per containment set, memoized
function labelRgb(m){
  if(labelRgbCache[m]) return labelRgbCache[m];
  const h=(m*2654435761>>>0)%360;
  return labelRgbCache[m]=hslToRgb(h,0.60,(34+8*popcount(m))/100);
}

// ---- cross-section ----
const RANGE=2.0;                        // half-extent of the slice view
let colorMode='depth', sliceAxis='2', sliceOff=0;
const slice=$('slice'), sctx=slice.getContext('2d');

function axisBasis(a){                   // returns {n, u, v} orthonormal
  if(a==='0') return {n:[1,0,0],u:[0,1,0],v:[0,0,1]};
  if(a==='1') return {n:[0,1,0],u:[0,0,1],v:[1,0,0]};
  if(a==='2') return {n:[0,0,1],u:[1,0,0],v:[0,1,0]};
  const s=1/Math.sqrt(3);               // (1,1,1) diagonal
  return {n:[s,s,s], u:[0.70710678,-0.70710678,0],
          v:[0.40824829,0.40824829,-0.81649658]};
}
function renderSlice(){
  const W=slice.width,H=slice.height;
  const {n,u,v}=axisBasis(sliceAxis);
  const img=sctx.createImageData(W,H);
  const d=img.data;
  const off=sliceOff;
  // depth grid, also used for component counting
  const grid=new Int8Array(W*H);
  for(let j=0;j<H;j++){
    const vv=RANGE-(2*RANGE)*j/(H-1);
    for(let i=0;i<W;i++){
      const uu=-RANGE+(2*RANGE)*i/(W-1);
      const p=[u[0]*uu+v[0]*vv+n[0]*off, u[1]*uu+v[1]*vv+n[1]*off,
               u[2]*uu+v[2]*vv+n[2]*off];
      const m=labelAt(p), dep=popcount(m);
      const shown=visible(m,dep);
      grid[j*W+i]=shown?dep:0;
      const rgb = !shown ? BG_RGB : (colorMode==='depth'?DEPTH_RGB[dep]:labelRgb(m));
      const o=(j*W+i)*4;
      d[o]=rgb[0];d[o+1]=rgb[1];d[o+2]=rgb[2];d[o+3]=255;
    }
  }
  sctx.putImageData(img,0,0);
  // faint centre crosshair
  sctx.strokeStyle='rgba(205,214,223,.18)';sctx.lineWidth=1;
  sctx.beginPath();sctx.moveTo(W/2,0);sctx.lineTo(W/2,H);
  sctx.moveTo(0,H/2);sctx.lineTo(W,H/2);sctx.stroke();
  // mark concurrences lying in (or near) this slice, at their in-plane spot
  if(showConc){
    const {n,u,v}=axisBasis(sliceAxis);
    for(const cc of concurrences){
      const d=n[0]*cc.p[0]+n[1]*cc.p[1]+n[2]*cc.p[2]-sliceOff;
      if(Math.abs(d)>0.05) continue;
      const uu=u[0]*cc.p[0]+u[1]*cc.p[1]+u[2]*cc.p[2];
      const vv=v[0]*cc.p[0]+v[1]*cc.p[1]+v[2]*cc.p[2];
      const px=(uu+RANGE)/(2*RANGE)*W, py=(RANGE-vv)/(2*RANGE)*H;
      sctx.strokeStyle=CONC_COL[cc.kind];sctx.lineWidth=1.6;
      sctx.beginPath();sctx.arc(px,py,3+0.6*cc.mult,0,7);sctx.stroke();
    }
    // ghost near-crossings lying in (or near) this slice: dashed, fading
    sctx.setLineDash([3,3]);
    for(const g of ghosts){
      const d=n[0]*g.p[0]+n[1]*g.p[1]+n[2]*g.p[2]-sliceOff;
      if(Math.abs(d)>0.05) continue;
      const uu=u[0]*g.p[0]+u[1]*g.p[1]+u[2]*g.p[2];
      const vv=v[0]*g.p[0]+v[1]*g.p[1]+v[2]*g.p[2];
      const px=(uu+RANGE)/(2*RANGE)*W, py=(RANGE-vv)/(2*RANGE)*H;
      sctx.strokeStyle='#7fc9ff';sctx.lineWidth=1.4;
      sctx.globalAlpha=0.65*(1-g.gap/0.02);
      sctx.beginPath();sctx.arc(px,py,4,0,7);sctx.stroke();
    }
    sctx.setLineDash([]);
    sctx.globalAlpha=1;
  }
  countCells(grid,W,H);
}
// connected components (4-conn) of each depth value in the slice raster
function countCells(grid,W,H){
  const seen=new Uint8Array(W*H), counts=[0,0,0,0,0,0,0];
  const stack=[];
  for(let s=0;s<W*H;s++){
    if(seen[s]) continue;
    const dep=grid[s]; seen[s]=1;
    if(dep===0) continue;
    counts[dep]++; stack.length=0; stack.push(s);
    while(stack.length){
      const q=stack.pop(), qx=q%W, qy=(q/W)|0;
      const nb=[[qx-1,qy],[qx+1,qy],[qx,qy-1],[qx,qy+1]];
      for(const [nx,ny] of nb){
        if(nx<0||ny<0||nx>=W||ny>=H) continue;
        const t=ny*W+nx;
        if(!seen[t]&&grid[t]===dep){seen[t]=1;stack.push(t);}
      }
    }
  }
  drawLegend(counts);
  const tot=counts.reduce((a,b)=>a+b,0);
  $('slcount').textContent=`${tot} cells in slice`;
}
function drawLegend(counts){
  let h='';
  for(let dpt=1;dpt<=cubes.length;dpt++){
    h+=`<div class="lrow"><span class="sw" style="background:${DEPTH_COLORS[dpt]}"></span>`
      +`<span>depth ${dpt}${dpt===cubes.length?' — core':''}</span>`
      +`<span class="n">${counts?counts[dpt]:''}</span></div>`;
  }
  $('legend').innerHTML=h;
}

// ---- 3D depth cloud ----
const cloud=$('cloud'), cctx=cloud.getContext('2d');
let pts=[], showWire=true, spin=!reduceMotion, rotX=-.5, rotY=.7, dragging=false;
let showConc=true, concurrences=[], ghosts=[];
function samplePoints(){
  // Boundary-hugging sampling: every region wall lies on some cube's face
  // square, so sample points ON the face squares and nudge them just
  // inside/outside along the face normal. The cloud then renders the
  // arrangement's actual walls (each wall two-toned by the depths on its
  // two sides) instead of volumetric fog.
  pts=[];
  const N=26000, del=0.02, nc=cubes.length;
  for(let i=0;i<N;i++){
    const k=(Math.random()*nc)|0, j=(Math.random()*3)|0,
          s=Math.random()<0.5?-1:1;
    const a=(j+1)%3, b=(j+2)%3, c=cubes[k];
    const u=Math.random()*2-1, v=Math.random()*2-1;
    const tj=s*(1+(Math.random()<0.5?-del:del));  // just inside / just outside
    const p=[c[j][0]*tj+c[a][0]*u+c[b][0]*v,
             c[j][1]*tj+c[a][1]*u+c[b][1]*v,
             c[j][2]*tj+c[a][2]*u+c[b][2]*v];
    const m=labelAt(p), dep=popcount(m);
    if(dep>0) pts.push([p[0],p[1],p[2],dep,m]);
  }
  $('cloudn').textContent=`${pts.length.toLocaleString()} boundary samples`;
}

// Concurrences: points where 4+ face-planes meet. Classified as EDGE
// crossings (max 2 planes from any one cube -> two cube edges cross) or
// CORNER coincidences (some cube contributes 3 planes -> a cube corner).
// Float arithmetic with a tolerance -- exact for rational configs, and
// close enough to reveal the sqrt(n) compounds' corner-sharing.
const det3=(a,b,c)=>a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]);
// ---- segment-segment closest distance (Ericson, Real-Time Collision
// Detection §5.1.9), clamped to both segments; feeds the ghost-ring search.
function segSegDist(p1,q1,p2,q2){
  const d1=[q1[0]-p1[0],q1[1]-p1[1],q1[2]-p1[2]];
  const d2=[q2[0]-p2[0],q2[1]-p2[1],q2[2]-p2[2]];
  const r=[p1[0]-p2[0],p1[1]-p2[1],p1[2]-p2[2]];
  const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
  const a=dot(d1,d1), e=dot(d2,d2), f=dot(d2,r), EPS=1e-12;
  let s,t;
  if(a<=EPS && e<=EPS){ s=0;t=0; }
  else if(a<=EPS){ s=0; t=Math.min(1,Math.max(0,f/e)); }
  else{
    const c=dot(d1,r);
    if(e<=EPS){ t=0; s=Math.min(1,Math.max(0,-c/a)); }
    else{
      const b=dot(d1,d2), denom=a*e-b*b;
      s=denom!==0 ? Math.min(1,Math.max(0,(b*f-c*e)/denom)) : 0;
      t=(b*s+f)/e;
      if(t<0){ t=0; s=Math.min(1,Math.max(0,-c/a)); }
      else if(t>1){ t=1; s=Math.min(1,Math.max(0,(b-c)/a)); }
    }
  }
  const c1=[p1[0]+d1[0]*s,p1[1]+d1[1]*s,p1[2]+d1[2]*s];
  const c2=[p2[0]+d2[0]*t,p2[1]+d2[1]*t,p2[2]+d2[2]*t];
  const dx=c1[0]-c2[0],dy=c1[1]-c2[1],dz=c1[2]-c2[2];
  return {dist:Math.sqrt(dx*dx+dy*dy+dz*dz),
    mid:[(c1[0]+c2[0])/2,(c1[1]+c2[1])/2,(c1[2]+c2[2])/2]};
}
// per-cube edge segments, mirroring the CUBEC/CUBEE wireframe construction
// (corner = sum_j c_j * face-normal column j).
function cubeEdgeSegs(k){
  const M=cubes[k];
  const corners=CUBEC.map(c=>[
    M[0][0]*c[0]+M[1][0]*c[1]+M[2][0]*c[2],
    M[0][1]*c[0]+M[1][1]*c[1]+M[2][1]*c[2],
    M[0][2]*c[0]+M[1][2]*c[1]+M[2][2]*c[2]]);
  return CUBEE.map(([a,b])=>[corners[a],corners[b]]);
}
function computeConcurrences(){
  concurrences=[];
  const P=[];
  for(let k=0;k<cubes.length;k++)for(let j=0;j<3;j++){
    const n=cubes[k][j];
    P.push({n,c:1,k,j}); P.push({n:[-n[0],-n[1],-n[2]],c:1,k,j});
  }
  const nP=P.length, bound=2.4, seen=new Set(), cand=[];
  for(let i=0;i<nP;i++)for(let j=i+1;j<nP;j++)for(let l=j+1;l<nP;l++){
    const a=P[i].n,b=P[j].n,c=P[l].n, D=det3(a,b,c);
    if(Math.abs(D)<1e-6) continue;
    const rhs=[P[i].c,P[j].c,P[l].c];
    const rep=col=>{const M=[a.slice(),b.slice(),c.slice()];
      M[0][col]=rhs[0];M[1][col]=rhs[1];M[2][col]=rhs[2];return det3(M[0],M[1],M[2]);};
    const x=[rep(0)/D,rep(1)/D,rep(2)/D];
    if(Math.abs(x[0])>bound||Math.abs(x[1])>bound||Math.abs(x[2])>bound) continue;
    const key=x.map(v=>Math.round(v*1000)).join(',');
    if(seen.has(key)) continue; seen.add(key); cand.push(x);
  }
  const eps=1e-4;
  // a plane counts toward a concurrence only if the point lies on its
  // ACTUAL bounded face square, not merely on the infinite plane: the
  // point's coordinates along the cube's other two axes must be within
  // [-1,1] (tolerance includes corners, which sit exactly on the edge).
  function onFace(pl,x){
    const c=cubes[pl.k];
    for(let a=0;a<3;a++){
      if(a===pl.j) continue;
      if(Math.abs(c[a][0]*x[0]+c[a][1]*x[1]+c[a][2]*x[2])>1+eps) return false;
    }
    return true;
  }
  for(const x of cand){
    let mult=0; const per={};
    for(const pl of P){
      if(Math.abs(pl.n[0]*x[0]+pl.n[1]*x[1]+pl.n[2]*x[2]-pl.c)<eps && onFace(pl,x)){
        mult++;per[pl.k]=(per[pl.k]||0)+1;
      }
    }
    if(mult>=4){
      const kind = Math.max(...Object.values(per))>=3 ? 'corner' : 'edge';
      concurrences.push({p:x,mult,kind});
    }
  }
  // ---- ghost (near) edge-crossings: on the 67<->67 slide, exact edge
  // crossings at the walls (t=0,1) open into hairline gaps in the interior.
  // Find every pair of cube edges (distinct cubes) whose closest approach
  // is a near-miss rather than exact-zero or unrelated, and record the
  // midpoint of closest approach as a faint "ghost" concurrence.
  ghosts=[];
  const edgeSets=cubes.map((_,k)=>cubeEdgeSegs(k));
  const ghostCand=[];
  for(let ka=0;ka<cubes.length;ka++)for(let kb=ka+1;kb<cubes.length;kb++){
    for(const ea of edgeSets[ka])for(const eb of edgeSets[kb]){
      const {dist,mid}=segSegDist(ea[0],ea[1],eb[0],eb[1]);
      if(dist>1e-6 && dist<0.02) ghostCand.push({p:mid,gap:dist,kind:'edge',ghost:true});
    }
  }
  ghostCand.sort((a,b)=>a.gap-b.gap);
  ghosts=ghostCand.slice(0,60);
  const mx=concurrences.reduce((a,c)=>Math.max(a,c.mult),0);
  $('cloudn').textContent=`${pts.length.toLocaleString()} samples · `
    +`${concurrences.length} concurrences${mx?` (max ${mx})`:''}`
    +(ghosts.length?` · ${ghosts.length} ghost`:'');
}
const CONC_COL={corner:'#ffd76b', edge:'#7fc9ff'};
// spin-axis toggle: 'y' = turntable about world (0,1,0);
// 'diag' = spin the MODEL about the compound's shared 3-fold axis (1,1,1)
// (pre-rotation applied before the drag/view rotation, so the C3 symmetry
// of the record configs shows as a 1/3-period repeat).
let spinAxis='y', ang111=0, P111=[[1,0,0],[0,1,0],[0,0,1]];
function updateP111(){
  const s3=1/Math.sqrt(3), a=[s3,s3,s3];
  const K=[[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]];
  const s=Math.sin(ang111), c1=1-Math.cos(ang111);
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){
    let k2=0; for(let m=0;m<3;m++) k2+=K[i][m]*K[m][j];
    P111[i][j]=(i===j?1:0)+s*K[i][j]+c1*k2;
  }
}
function pre(p){
  if(spinAxis==='y') return p;
  return [P111[0][0]*p[0]+P111[0][1]*p[1]+P111[0][2]*p[2],
          P111[1][0]*p[0]+P111[1][1]*p[1]+P111[1][2]*p[2],
          P111[2][0]*p[0]+P111[2][1]*p[1]+P111[2][2]*p[2]];
}
function viewRot(p){
  const cx=Math.cos(rotX),sx=Math.sin(rotX),cy=Math.cos(rotY),sy=Math.sin(rotY);
  let x=p[0]*cy - p[2]*sy, z=p[0]*sy + p[2]*cy, y=p[1]*cx - z*sx;
  z=p[1]*sx + z*cx; return [x,y,z];
}
function rot(p){ return viewRot(pre(p)); }
const CUBEC=[];
for(const a of[-1,1])for(const b of[-1,1])for(const c of[-1,1])CUBEC.push([a,b,c]);
const CUBEE=[[0,1],[0,2],[0,4],[1,3],[1,5],[2,3],[2,6],[3,7],[4,5],[4,6],[5,7],[6,7]];
// depth cue: rotated z in roughly [-2.4,2.4] -> [0.35 far, 1.0 near], shared
// by points/wireframe/rings so nearer geometry reads as nearer.
const cue=z=>0.35+0.65*Math.min(1,Math.max(0,(z+2.4)/4.8));
function drawCloud(){
  const W=cloud.width,H=cloud.height,S=W/5.0,cx=W/2,cy=H/2;
  cctx.fillStyle='#07090c';cctx.fillRect(0,0,W,H);
  // depth points, painter-sorted back-to-front, respecting the filters
  const proj=[];
  for(const p of pts){
    if(!visible(p[4],p[3])) continue;
    const r=rot(p); proj.push([r[0]*S+cx,-r[1]*S+cy,r[2],p[3]]);
  }
  proj.sort((a,b)=>a[2]-b[2]);
  for(const q of proj){
    const f=cue(q[2]);
    cctx.globalAlpha=(0.35+0.11*q[3])*f;
    cctx.fillStyle=DEPTH_COLORS[q[3]];
    const s=(1.1+0.32*q[3])*f;
    cctx.fillRect(q[0]-s/2,q[1]-s/2,s,s);
  }
  cctx.globalAlpha=1;
  drawPlane(S,cx,cy);
  if(showWire){
    cctx.lineWidth=1;
    for(let k=0;k<cubes.length;k++){
      const M=cubes[k];
      const cp=CUBEC.map(c=>{             // corner = sum_j c_j * (column j = face normal j)
        const x=M[0][0]*c[0]+M[1][0]*c[1]+M[2][0]*c[2];
        const y=M[0][1]*c[0]+M[1][1]*c[1]+M[2][1]*c[2];
        const z=M[0][2]*c[0]+M[1][2]*c[1]+M[2][2]*c[2];
        const r=rot([x,y,z]);return [r[0]*S+cx,-r[1]*S+cy,r[2]];
      });
      cctx.strokeStyle=`hsl(${(k*60)} 45% 60% / .5)`;
      for(const [a,b] of CUBEE){
        cctx.globalAlpha=cue((cp[a][2]+cp[b][2])/2);
        cctx.beginPath();cctx.moveTo(cp[a][0],cp[a][1]);
        cctx.lineTo(cp[b][0],cp[b][1]);cctx.stroke();
      }
    }
    cctx.globalAlpha=1;
  }
  if(showConc){
    const cm=concurrences.map(c=>{const r=rot(c.p);
      return {x:r[0]*S+cx,y:-r[1]*S+cy,z:r[2],mult:c.mult,kind:c.kind};});
    cm.sort((a,b)=>a.z-b.z);
    for(const c of cm){
      const f=cue(c.z);
      cctx.strokeStyle=CONC_COL[c.kind];cctx.globalAlpha=.92*f;cctx.lineWidth=1.6*f;
      cctx.beginPath();cctx.arc(c.x,c.y,2.2+0.7*c.mult,0,7);cctx.stroke();
    }
    cctx.globalAlpha=1;
    // ghost (near) edge-crossings: dashed, fading out as the gap widens
    const gm=ghosts.map(g=>{const r=rot(g.p);
      return {x:r[0]*S+cx,y:-r[1]*S+cy,z:r[2],gap:g.gap};});
    gm.sort((a,b)=>a.z-b.z);
    cctx.setLineDash([3,3]);
    for(const g of gm){
      const f=cue(g.z);
      cctx.strokeStyle='#7fc9ff';cctx.lineWidth=1.4*f;
      cctx.globalAlpha=f*0.65*(1-g.gap/0.02);
      cctx.beginPath();cctx.arc(g.x,g.y,4,0,7);cctx.stroke();
    }
    cctx.setLineDash([]);
    cctx.globalAlpha=1;
  }
}
// the current cross-section plane, drawn in the 3-D view so the two connect
function drawPlane(S,cx,cy){
  const {n,u,v}=axisBasis(sliceAxis), o=sliceOff, R=RANGE;
  const corners=[[-R,-R],[R,-R],[R,R],[-R,R]].map(([a,b])=>{
    const p=[u[0]*a+v[0]*b+n[0]*o, u[1]*a+v[1]*b+n[1]*o, u[2]*a+v[2]*b+n[2]*o];
    const r=rot(p); return [r[0]*S+cx,-r[1]*S+cy];
  });
  cctx.fillStyle='rgba(53,208,214,.09)';
  cctx.strokeStyle='rgba(53,208,214,.55)';cctx.lineWidth=1;
  cctx.beginPath();cctx.moveTo(corners[0][0],corners[0][1]);
  for(let i=1;i<4;i++)cctx.lineTo(corners[i][0],corners[i][1]);
  cctx.closePath();cctx.fill();cctx.stroke();
}
function frame(){
  if(spin&&!dragging){
    if(spinAxis==='y') rotY+=0.004;
    else { ang111+=0.004; updateP111(); }
  }
  drawCloud();
  requestAnimationFrame(frame);
}

// ---- filter chips ----
function buildFilters(){
  const N=cubes.length;
  const df=$('depthFilter'); df.innerHTML='';
  for(let d=1;d<=N;d++){
    const b=document.createElement('button');
    b.className='mini';b.textContent=d;b.setAttribute('aria-pressed','true');
    b.style.color=DEPTH_COLORS[d];
    b.onclick=()=>{ b.ariaPressed=b.ariaPressed==='true'?'false':'true';
      if(b.ariaPressed==='true')depthSel.add(d);else depthSel.delete(d);
      renderSlice(); };
    df.appendChild(b);
  }
  const cf=$('cubeFilter'); cf.innerHTML='';
  for(let k=0;k<N;k++){
    const b=document.createElement('button');
    b.className='mini';b.textContent=k+1;b.setAttribute('aria-pressed','true');
    b.onclick=()=>{ const on=(cubeSel>>k&1)===0; // toggling ON if currently off
      cubeSel^=(1<<k); b.ariaPressed=String((cubeSel>>k&1)===1); renderSlice(); };
    cf.appendChild(b);
  }
}
$('dAll').onclick=()=>{depthSel=new Set(Array.from({length:cubes.length},(_,i)=>i+1));
  [...$('depthFilter').children].forEach(b=>b.ariaPressed='true');renderSlice();};
$('cAll').onclick=()=>{cubeSel=(1<<cubes.length)-1;
  [...$('cubeFilter').children].forEach(b=>b.ariaPressed='true');renderSlice();};

// ---- wiring ----
let inputMode='quat';
function setMode(m){
  inputMode=m;
  $('fQuat').ariaPressed=String(m==='quat');
  $('fMat').ariaPressed=String(m==='mat');
  $('fmtHint').textContent = m==='quat'
    ? 'One quaternion w,x,y,z per line (2–8 cubes; decimals fine, so √n configs work).'
    : 'One row-major 3×3 rotation matrix per line: 9 numbers (2–8 cubes).';
}
function apply(){
  try{
    cubes=parseConfig($('quats').value, inputMode);
    cubeSel=(1<<cubes.length)-1;
    depthSel=new Set(Array.from({length:cubes.length},(_,i)=>i+1));
    buildFilters();
    $('err').textContent='';
    samplePoints(); computeConcurrences(); renderSlice();
    renderExactChips();
  }catch(e){ $('err').textContent=String(e); $('exact').innerHTML=''; }
}
function renderExactChips(){
  if(exactInfo){
    const d=exactInfo.d;
    $('exact').innerHTML=`<span class="chip" style="border-color:var(--accent-dim)">exact total ${exactInfo.total}</span>`
      +Object.keys(d).map(k=>`<span class="chip">d${k}: ${d[k]}</span>`).join('');
  } else {
    $('exact').innerHTML=`<span class="chip">${cubes.length} cubes — exact region count needs the exact counter</span>`;
  }
}
function loadPreset(mode,text,exact){ exitSlide();setMode(mode);$('quats').value=text;exactInfo=exact;apply(); }
function exitSlide(){ $('slideGrp').style.display='none'; }
function setSlide(t){
  const mats=slideMats(t);
  setMode('mat'); $('quats').value=matText(mats);
  exactInfo = (t===0||t===1)
    ? {total:67, d:{1:48,2:18,3:1}}
    : null;
  cubes=mats.map(matToCols);
  cubeSel=7; depthSel=new Set([1,2,3]);
  buildFilters(); $('err').textContent='';
  samplePoints(); computeConcurrences(); renderSlice();
  if(exactInfo) renderExactChips();
  else $('exact').innerHTML=`<span class="chip">interior of the family — generic ≈37; endpoints are the isolated 67 walls</span>`;
  $('slideT').textContent=`t = ${t.toFixed(3)}`;
}
$('pSlide').onclick=()=>{ $('slideGrp').style.display='flex'; $('slidePos').value=0; setSlide(0); };
$('slidePos').oninput=e=>setSlide(e.target.value/1000);
$('load').onclick=()=>{exitSlide();exactInfo=null;apply();};
$('fQuat').onclick=()=>setMode('quat');
$('fMat').onclick=()=>setMode('mat');
$('pRec').onclick=()=>loadPreset('quat',REC723_TXT,{total:723,d:{1:210,2:216,3:164,4:96,5:36,6:1}});
$('pOcta').onclick=()=>loadPreset('mat',matText(OCTA),{total:67,d:{1:48,2:18,3:1}});
$('pGold').onclick=()=>loadPreset('mat',matText(GOLDEN),{total:351,d:{1:180,2:80,3:60,4:30,5:1}});
$('mDepth').onclick=()=>{colorMode='depth';$('mDepth').ariaPressed='true';$('mLabel').ariaPressed='false';renderSlice();};
$('mLabel').onclick=()=>{colorMode='label';$('mLabel').ariaPressed='true';$('mDepth').ariaPressed='false';renderSlice();};
$('axis').onchange=e=>{sliceAxis=e.target.value;renderSlice();};
$('pos').oninput=e=>{sliceOff=e.target.value/100;$('posv').textContent=sliceOff.toFixed(3);renderSlice();};
$('wire').onclick=()=>{showWire=!showWire;$('wire').ariaPressed=String(showWire);};
$('spin').onclick=()=>{spin=!spin;$('spin').ariaPressed=String(spin);};
$('spinAxis').onclick=()=>{
  spinAxis = spinAxis==='y' ? 'diag' : 'y';
  $('spinAxis').textContent = spinAxis==='y' ? 'axis: y' : 'axis: (1,1,1)';
  $('spinAxis').ariaPressed = String(spinAxis==='diag');
};
$('conc').onclick=()=>{showConc=!showConc;$('conc').ariaPressed=String(showConc);renderSlice();};
// drag to rotate
cloud.addEventListener('pointerdown',e=>{dragging=true;cloud.setPointerCapture(e.pointerId);});
cloud.addEventListener('pointerup',()=>dragging=false);
cloud.addEventListener('pointermove',e=>{
  if(!dragging)return;
  rotY+=e.movementX*0.008; rotX+=e.movementY*0.008;
});

setMode('quat');
loadPreset('quat',REC723_TXT,{total:723,d:{1:210,2:216,3:164,4:96,5:36,6:1}});
frame();
