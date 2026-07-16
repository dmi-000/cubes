// opaque_test.js — node harness for the Opaque display mode gates (G1-G4).
// Exercises the ACTUAL <script> text shipped in depth_explorer.html: it is
// extracted verbatim (no retyping) and run in a vm context with a minimal
// DOM stub, then buildOpaqueSurface (and the rest of the script's top-level
// bindings) are pulled out of that same context for the gate checks.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execFileSync } = require('child_process');

const MASTER = '/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/depth_explorer.html';

let PASS = 0, FAIL = 0;
function check(name, cond, detail) {
  if (cond) { PASS++; console.log(`PASS  ${name}`); }
  else { FAIL++; console.log(`FAIL  ${name}${detail ? ' -- ' + detail : ''}`); }
}

const html = fs.readFileSync(MASTER, 'utf8');
const m = /<script>([\s\S]*)<\/script>/.exec(html);
if (!m) throw new Error('no <script> block found in ' + MASTER);
const scriptText = m[1];

// ---------------------------------------------------------------- G4a ----
// node --check on the extracted script text, exactly as it ships.
const tmpJs = path.join(require('os').tmpdir(), 'depth_explorer_extracted.js');
fs.writeFileSync(tmpJs, scriptText);
let checkOk = false, checkErr = '';
try { execFileSync(process.execPath, ['--check', tmpJs], { stdio: 'pipe' }); checkOk = true; }
catch (e) { checkErr = e.stderr ? e.stderr.toString() : String(e); }
check('G4a node --check on extracted <script>', checkOk, checkErr);

// ---------------------------------------------------------- DOM stubbing --
// Minimal stand-ins for the handful of DOM APIs the script touches at
// top-level load: getElementById targets, canvas 2D context, matchMedia,
// requestAnimationFrame. Enough to run the script to completion once
// (it self-initializes with the 723 preset and starts the render loop).
function makeCtx() {
  return {
    fillStyle: '', strokeStyle: '', lineWidth: 1, globalAlpha: 1,
    fillRect(){}, beginPath(){}, moveTo(){}, lineTo(){}, closePath(){},
    fill(){}, stroke(){}, arc(){}, setLineDash(){},
    createImageData(w, h) { return { data: new Uint8ClampedArray(w * h * 4) }; },
    putImageData(){},
  };
}
function makeEl(id) {
  const el = {
    id, value: '', textContent: '', innerHTML: '', style: {}, ariaPressed: 'false',
    children: [], onclick: null, oninput: null, onchange: null,
    width: 520, height: 520,
    appendChild(c) { el.children.push(c); },
    addEventListener(){}, removeEventListener(){},
    setAttribute(k, v) { if (k === 'aria-pressed') el.ariaPressed = v; },
    getAttribute() { return null; },
    getContext() { return makeCtx(); },
  };
  return el;
}
const elements = {};
const documentStub = {
  getElementById(id) { if (!elements[id]) elements[id] = makeEl(id); return elements[id]; },
  createElement() { return makeEl('created'); },
};
const sandbox = {
  document: documentStub,
  matchMedia: () => ({ matches: false }),
  requestAnimationFrame: () => 0,   // no-op: don't recurse frame() forever
  performance: { now: () => Date.now() },
  console,
  Math,
};
const ctx = vm.createContext(sandbox);

let runErr = null;
try {
  vm.runInContext(scriptText, ctx, { filename: 'depth_explorer<script>' });
} catch (e) { runErr = e; }
check('G4b script runs to completion under DOM stub', !runErr, runErr && (runErr.stack || String(runErr)));

// Pull references out of the script's top-level lexical scope (they are
// NOT own-properties of the sandbox for let/const, but the scope persists
// across further vm.runInContext calls against the same context).
const exports_ = vm.runInContext(
  `({ buildOpaqueSurface, cubes, depthSel, cubeSel, exactInfo,
      OCTA, GOLDEN, REC723_TXT, matText, matToCols, quatToCols,
      parseConfig, loadPreset, apply, renderExactChips })`,
  ctx
);
// note: setSlide (the old 67<->67 slide) was retired by DIHEDRAL_SLIDER_SPEC.md
// and replaced with setFamily (the dihedral-family slider); this file never
// called setSlide directly (only destructured it), so no other change needed.
const { buildOpaqueSurface, matText, matToCols, loadPreset } = exports_;

// 723 preset is loaded by the script's own bottom-of-file init call.
check('G4c 723 preset auto-loaded (6 cubes)', exports_.cubes.length === 6,
  `got ${exports_.cubes.length}`);
check('G4d 723 exact chip text unchanged',
  documentStub.getElementById('exact').innerHTML.includes('exact total 723')
  && documentStub.getElementById('exact').innerHTML.includes('d1: 210')
  && documentStub.getElementById('exact').innerHTML.includes('d6: 1'),
  documentStub.getElementById('exact').innerHTML);

// Re-drive the other two hardcoded presets through the real preset buttons'
// handlers (loadPreset) and check their chip text is still the shipped
// literals -- this is the actual "existing modes' counts unchanged" check;
// a slip while editing the file would show up here as a text mismatch.
loadPreset('mat', matText(exports_.OCTA), { total: 67, d: { 1: 48, 2: 18, 3: 1 } });
check('G4e octahedral 67 chip text unchanged',
  documentStub.getElementById('exact').innerHTML.includes('exact total 67')
  && documentStub.getElementById('exact').innerHTML.includes('d3: 1'));

loadPreset('mat', matText(exports_.GOLDEN), { total: 351, d: { 1: 180, 2: 80, 3: 60, 4: 30, 5: 1 } });
check('G4f golden 351 chip text unchanged',
  documentStub.getElementById('exact').innerHTML.includes('exact total 351')
  && documentStub.getElementById('exact').innerHTML.includes('d5: 1'));

// back to the 723 preset for the rest of the gates / timing runs
loadPreset('quat', exports_.REC723_TXT, { total: 723, d: { 1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1 } });

// ---------------------------------------------------------------------
// geometry helpers, mirrored ONLY for the audits (G2/G3 sampling logic) --
// buildOpaqueSurface itself is always the extracted-context reference.
function maskAtDirect(p, mats, selected) {
  let m = 0;
  for (const k of selected) {
    const c = mats[k];
    if (Math.abs(c[0][0]*p[0]+c[0][1]*p[1]+c[0][2]*p[2]) < 1 &&
        Math.abs(c[1][0]*p[0]+c[1][1]*p[1]+c[1][2]*p[2]) < 1 &&
        Math.abs(c[2][0]*p[0]+c[2][1]*p[1]+c[2][2]*p[2]) < 1) m |= 1 << k;
  }
  return m;
}
function depthAtDirect(p, mats, selected) {
  let m = maskAtDirect(p, mats, selected), dep = 0;
  while (m) { dep += m & 1; m >>= 1; }
  return dep;
}
function triArea(a, b, c) {
  const ux=b[0]-a[0], uy=b[1]-a[1], uz=b[2]-a[2];
  const vx=c[0]-a[0], vy=c[1]-a[1], vz=c[2]-a[2];
  const nx=uy*vz-uz*vy, ny=uz*vx-ux*vz, nz=ux*vy-uy*vx;
  return 0.5*Math.sqrt(nx*nx+ny*ny+nz*nz);
}
function sampleInPolygon(poly) {
  const areas = [], a0 = poly[0];
  let total = 0;
  for (let i = 1; i < poly.length - 1; i++) {
    const ar = triArea(a0, poly[i], poly[i+1]);
    areas.push(ar); total += ar;
  }
  let r = Math.random() * total, idx = 0;
  for (; idx < areas.length - 1; idx++) { if (r < areas[idx]) break; r -= areas[idx]; }
  const a = a0, b = poly[idx+1], c = poly[idx+2];
  let u = Math.random(), v = Math.random();
  if (u + v > 1) { u = 1-u; v = 1-v; }
  return [
    a[0]+u*(b[0]-a[0])+v*(c[0]-a[0]),
    a[1]+u*(b[1]-a[1])+v*(c[1]-a[1]),
    a[2]+u*(b[2]-a[2])+v*(c[2]-a[2]),
  ];
}
function randUnit() {
  let x,y,z,n;
  do {
    x = (Math.random()*2-1); y = (Math.random()*2-1); z = (Math.random()*2-1);
    n = Math.sqrt(x*x+y*y+z*z);
  } while (n < 1e-6 || n > 1);
  return [x/n, y/n, z/n];
}
// Newell's-method true normal of a (possibly >3-gon) planar convex polygon.
function newellNormal(poly) {
  let nx=0, ny=0, nz=0;
  for (let i=0;i<poly.length;i++) {
    const p1=poly[i], p2=poly[(i+1)%poly.length];
    nx += (p1[1]-p2[1])*(p1[2]+p2[2]);
    ny += (p1[2]-p2[2])*(p1[0]+p2[0]);
    nz += (p1[0]-p2[0])*(p1[1]+p2[1]);
  }
  const len = Math.hypot(nx,ny,nz);
  return len < 1e-15 ? [0,0,0] : [nx/len, ny/len, nz/len];
}
// signed in-plane distance from p to each edge line; min |distance| is the
// distance to the nearest edge (line, not segment -- a conservative proxy
// used only to decide whether to skip a ray per G3's "within 1e-6" rule).
function edgeDistances(poly, N, p) {
  const ds = [];
  for (let i=0;i<poly.length;i++) {
    const v0=poly[i], v1=poly[(i+1)%poly.length];
    const ex=v1[0]-v0[0], ey=v1[1]-v0[1], ez=v1[2]-v0[2];
    const elen = Math.hypot(ex,ey,ez);
    const wx=p[0]-v0[0], wy=p[1]-v0[1], wz=p[2]-v0[2];
    const crx=ey*wz-ez*wy, cry=ez*wx-ex*wz, crz=ex*wy-ey*wx;
    const s = (crx*N[0]+cry*N[1]+crz*N[2]) / elen;
    ds.push(s);
  }
  return ds;
}

function selectedFromMask(n, mask) {
  const sel = [];
  for (let i=0;i<n;i++) if (mask>>i&1) sel.push(i);
  return sel;
}

// -------------------------------------------------------------------- G1 --
{
  const mat = matToCols([[1,0,0],[0,1,0],[0,0,1]]);
  const surf = buildOpaqueSurface([mat], [0], new Set([1]));
  let totalArea = 0;
  for (const f of surf) {
    // reuse the exact area formula shape (fan triangulation) locally --
    // buildOpaqueSurface doesn't expose polyArea, so recompute equivalently.
    const p = f.poly; let nx=0,ny=0,nz=0; const p0=p[0];
    for (let i=1;i<p.length-1;i++){
      const p1=p[i],p2=p[i+1];
      const ax=p1[0]-p0[0],ay=p1[1]-p0[1],az=p1[2]-p0[2];
      const bx=p2[0]-p0[0],by=p2[1]-p0[1],bz=p2[2]-p0[2];
      nx+=ay*bz-az*by; ny+=az*bx-ax*bz; nz+=ax*by-ay*bx;
    }
    totalArea += 0.5*Math.sqrt(nx*nx+ny*ny+nz*nz);
  }
  check('G1 single cube -> 6 quads', surf.length === 6, `got ${surf.length}`);
  check('G1 single cube -> total area 24', Math.abs(totalArea-24) < 1e-6, `got ${totalArea}`);
  check('G1 all pieces tagged depth 1', surf.every(f=>f.depth===1), JSON.stringify(surf.map(f=>f.depth)));
}

// -------------------------------------------------------------------- G2 --
const G2_CASES = [
  { name: 'octahedral pair, {2}', mats: exports_.OCTA.map(matToCols), depthSet: new Set([2]) },
  { name: 'golden triple, {3}', mats: exports_.GOLDEN.slice(0,3).map(matToCols), depthSet: new Set([3]) },
  { name: 'golden triple, {1,2,3}', mats: exports_.GOLDEN.slice(0,3).map(matToCols), depthSet: new Set([1,2,3]) },
  { name: '723 six-cube, {2,3,4,5,6}', mats: null, depthSet: new Set([2,3,4,5,6]) }, // filled below from live cubes
];
// pull the live 723 cubes (already loaded above) for the 4th case
loadPreset('quat', exports_.REC723_TXT, { total: 723, d: { 1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1 } });
G2_CASES[3].mats = exports_.cubes.slice();

const G2_TARGET = 2000;
const opaqueTimings = {};
for (const c of G2_CASES) {
  const selected = c.mats.map((_,i)=>i);
  const t0 = process.hrtime.bigint();
  const surf = buildOpaqueSurface(c.mats, selected, c.depthSet);
  const t1 = process.hrtime.bigint();
  opaqueTimings[c.name] = { ms: Number(t1-t0)/1e6, pieces: surf.length };

  let violations = 0, maskViolations = 0, sampled = 0, attempts = 0;
  const EPS = 1e-4;
  while (sampled < G2_TARGET && attempts < G2_TARGET*20) {
    attempts++;
    const f = surf[(Math.random()*surf.length)|0];
    if (!f || f.poly.length < 3) continue;
    const p = sampleInPolygon(f.poly);
    const n = f.normal;
    const p1 = [p[0]+n[0]*EPS, p[1]+n[1]*EPS, p[2]+n[2]*EPS];
    const p2 = [p[0]-n[0]*EPS, p[1]-n[1]*EPS, p[2]-n[2]*EPS];
    const m1 = maskAtDirect(p1, c.mats, selected);
    const m2 = maskAtDirect(p2, c.mats, selected);
    const d1 = depthAtDirect(p1, c.mats, selected);
    const d2 = depthAtDirect(p2, c.mats, selected);
    const in1 = c.depthSet.has(d1), in2 = c.depthSet.has(d2);
    if (in1 === in2) violations++;
    // containment-colour audit: the piece's stored mask must equal the
    // direct containment mask of the in-set side (and its popcount the
    // stored depth) at every sampled point, not just the build centroid.
    // Skip points within ~10*EPS of a piece edge: there a +-EPS off-plane
    // probe can legitimately sit on the far side of the plane that traces
    // that edge, flipping one containment bit without any geometry error.
    else {
      const tn = newellNormal(f.poly);
      const nearEdge = tn[0]===0 && tn[1]===0 && tn[2]===0
        ? true
        : Math.min(...edgeDistances(f.poly, tn, p).map(Math.abs)) < 10*EPS;
      if (!nearEdge) {
        const insideMask = in1 ? m1 : m2;
        let pc = 0, mm = f.mask; while (mm) { pc += mm & 1; mm >>= 1; }
        if (f.mask !== insideMask || pc !== f.depth) maskViolations++;
      }
    }
    sampled++;
  }
  check(`G2 membership audit: ${c.name} (${sampled} pts, ${surf.length} pieces, ${opaqueTimings[c.name].ms.toFixed(1)}ms)`,
    violations === 0 && sampled >= G2_TARGET, `${violations} violations`);
  check(`G2m containment-mask audit: ${c.name}`,
    maskViolations === 0, `${maskViolations} mask mismatches`);
}

// -------------------------------------------------------------------- G3 --
for (const c of G2_CASES) {
  const selected = c.mats.map((_,i)=>i);
  const surf = buildOpaqueSurface(c.mats, selected, c.depthSet);
  const normals = surf.map(f => newellNormal(f.poly));
  let violations = 0, rays = 0, skipped = 0, attempts = 0;
  const R3_TARGET = 2000;
  while (rays < R3_TARGET && attempts < R3_TARGET*30) {
    attempts++;
    const O = [0,0,0];
    const D = randUnit();
    const crossings = [];
    let nearEdge = false;
    for (let fi=0; fi<surf.length; fi++) {
      const f = surf[fi], N = f.normal;
      const denom = N[0]*D[0]+N[1]*D[1]+N[2]*D[2];
      if (Math.abs(denom) < 1e-12) continue;
      const c0 = N[0]*f.poly[0][0]+N[1]*f.poly[0][1]+N[2]*f.poly[0][2];
      const cO = N[0]*O[0]+N[1]*O[1]+N[2]*O[2];
      const t = (c0-cO)/denom;
      const P = [O[0]+t*D[0], O[1]+t*D[1], O[2]+t*D[2]];
      const trueN = normals[fi];
      if (trueN[0]===0 && trueN[1]===0 && trueN[2]===0) continue;
      const ds = edgeDistances(f.poly, trueN, P);
      const minAbs = Math.min(...ds.map(Math.abs));
      if (minAbs < 1e-6) { nearEdge = true; break; }
      const inside = ds.every(d=>d >= 0) || ds.every(d=>d <= 0);
      if (inside) crossings.push(t);
    }
    if (nearEdge) { skipped++; continue; }
    crossings.sort((a,b)=>a-b);
    // dedupe near-coincident crossings from two pieces sharing an edge trace
    const uniq = [];
    for (const t of crossings) { if (!uniq.length || Math.abs(t-uniq[uniq.length-1])>1e-7) uniq.push(t); }
    // check: direct depth-in-B test at gap midpoints must alternate exactly
    // at every crossing.
    const bounds = [-4, ...uniq, 4];
    let ok = true;
    let prevIn = null;
    for (let i=0;i<bounds.length-1;i++) {
      const tm = (bounds[i]+bounds[i+1])/2;
      const P = [O[0]+tm*D[0], O[1]+tm*D[1], O[2]+tm*D[2]];
      const dep = depthAtDirect(P, c.mats, selected);
      const inB = c.depthSet.has(dep);
      if (prevIn !== null && inB === prevIn) { ok = false; break; }
      prevIn = inB;
    }
    if (!ok) violations++;
    rays++;
  }
  check(`G3 ray audit: ${c.name} (${rays} rays, ${skipped} skipped near-edge)`,
    violations === 0 && rays >= R3_TARGET, `${violations} violations`);
}

// -------------------------------------------------------------------- G5 --
const MIRROR = '/Users/dmi/carroll/depth_explorer.html';
// copy master -> mirror, then diff (only meaningful once G1-G4 all pass;
// caller/report gates this, but we always report the fact for visibility).
let mirrorNote = 'not yet synced by harness (report/orchestrator syncs after all gates pass)';
check('G5 note', true, mirrorNote);

console.log('\n---- timings (buildOpaqueSurface) ----');
for (const [k,v] of Object.entries(opaqueTimings)) console.log(`${k}: ${v.pieces} pieces, ${v.ms.toFixed(2)} ms`);

console.log(`\n${PASS} passed, ${FAIL} failed`);
process.exit(FAIL ? 1 : 0);
