
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
function samplePoints(){
  pts=[];
  const N=17000;
  for(let i=0;i<N;i++){
    const p=[(Math.random()*2-1)*1.9,(Math.random()*2-1)*1.9,(Math.random()*2-1)*1.9];
    const m=labelAt(p), dep=popcount(m);
    if(dep>0) pts.push([p[0],p[1],p[2],dep,m]);
  }
  $('cloudn').textContent=`${pts.length.toLocaleString()} samples`;
}
function rot(p){
  const cx=Math.cos(rotX),sx=Math.sin(rotX),cy=Math.cos(rotY),sy=Math.sin(rotY);
  let x=p[0]*cy - p[2]*sy, z=p[0]*sy + p[2]*cy, y=p[1]*cx - z*sx;
  z=p[1]*sx + z*cx; return [x,y,z];
}
const CUBEC=[];
for(const a of[-1,1])for(const b of[-1,1])for(const c of[-1,1])CUBEC.push([a,b,c]);
const CUBEE=[[0,1],[0,2],[0,4],[1,3],[1,5],[2,3],[2,6],[3,7],[4,5],[4,6],[5,7],[6,7]];
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
    cctx.globalAlpha=0.35+0.11*q[3];
    cctx.fillStyle=DEPTH_COLORS[q[3]];
    const s=1.1+0.32*q[3];
    cctx.fillRect(q[0]-s/2,q[1]-s/2,s,s);
  }
  cctx.globalAlpha=1;
  drawPlane(S,cx,cy);
  if(showWire){
    cctx.lineWidth=1;
    for(let k=0;k<6;k++){
      const M=cubes[k];
      const cp=CUBEC.map(c=>{             // corner = M * c  (columns are normals ⇒ M^T? use rows)
        const x=M[0][0]*c[0]+M[1][0]*c[1]+M[2][0]*c[2];
        const y=M[0][1]*c[0]+M[1][1]*c[1]+M[2][1]*c[2];
        const z=M[0][2]*c[0]+M[1][2]*c[1]+M[2][2]*c[2];
        const r=rot([x,y,z]);return [r[0]*S+cx,-r[1]*S+cy];
      });
      cctx.strokeStyle=`hsl(${(k*60)} 45% 60% / .5)`;
      for(const [a,b] of CUBEE){cctx.beginPath();cctx.moveTo(cp[a][0],cp[a][1]);
        cctx.lineTo(cp[b][0],cp[b][1]);cctx.stroke();}
    }
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
  if(spin&&!dragging) rotY+=0.004;
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
    renderSlice(); samplePoints();
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
function loadPreset(mode,text,exact){ setMode(mode);$('quats').value=text;exactInfo=exact;apply(); }
$('load').onclick=()=>{exactInfo=null;apply();};
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
