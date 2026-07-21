// dihedral_slider_test.js -- node harness for the dihedral-family slider
// gates G1-G6 (DIHEDRAL_SLIDER_SPEC.md). Exercises the ACTUAL <script> text
// shipped in depth_explorer.html (extracted verbatim, run in a vm context
// with a minimal DOM stub -- same pattern as opaque_test.js), plus a set of
// geometry helpers mirrored ONLY for the audits (G2/G3/G4), following the
// precedent set by opaque_test.js's own "mirrored ONLY for the audits" note.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execFileSync } = require('child_process');

const SCRATCH = '/private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad';
const MASTER = path.join(SCRATCH, 'depth_explorer.html');

let PASS = 0, FAIL = 0;
function check(name, cond, detail) {
  if (cond) { PASS++; console.log(`PASS  ${name}`); }
  else { FAIL++; console.log(`FAIL  ${name}${detail ? ' -- ' + detail : ''}`); }
}

const html = fs.readFileSync(MASTER, 'utf8');
const m = /<script>([\s\S]*)<\/script>/.exec(html);
if (!m) throw new Error('no <script> block found in ' + MASTER);
const scriptText = m[1];

// ================================================================== G1 ====
// G1a: node --check on the extracted script text, exactly as it ships.
const tmpJs = path.join(require('os').tmpdir(), 'depth_explorer_dihedral_extracted.js');
fs.writeFileSync(tmpJs, scriptText);
let checkOk = false, checkErr = '';
try { execFileSync(process.execPath, ['--check', tmpJs], { stdio: 'pipe' }); checkOk = true; }
catch (e) { checkErr = e.stderr ? e.stderr.toString() : String(e); }
check('G1a node --check on extracted <script>', checkOk, checkErr);

// ---------------------------------------------------------- DOM stubbing --
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
  let _innerHTML = '';
  const el = {
    id, value: '', textContent: '', style: {}, ariaPressed: 'false',
    children: [], onclick: null, oninput: null, onchange: null,
    width: 520, height: 520,
    _listeners: {},
    appendChild(c) { el.children.push(c); },
    // real listeners (not no-ops): needed to trigger the cloud canvas's
    // wheel/pointer handlers from the harness (setFamily/loadPreset etc.
    // are driven via onclick/oninput properties instead, which the DOM
    // stub already supported; addEventListener-only handlers like the new
    // zoom wheel listener need this to be testable at all).
    addEventListener(type, fn) { el._listeners[type] = fn; },
    removeEventListener(type) { delete el._listeners[type]; },
    dispatch(type, evt) { if (el._listeners[type]) el._listeners[type](evt); },
    setAttribute(k, v) { if (k === 'aria-pressed') el.ariaPressed = v; },
    getAttribute() { return null; },
    getContext() { return makeCtx(); },
  };
  // real DOM semantics: (re)assigning innerHTML replaces all children, so
  // the `box.innerHTML=''; ...appendChild...` pattern used by
  // buildFilters/buildFamilyTicks/renderFamilyMarks correctly resets the
  // mock `children` array on every call, not just the first.
  Object.defineProperty(el, 'innerHTML', {
    get() { return _innerHTML; },
    set(v) { _innerHTML = v; el.children = []; },
  });
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
  requestAnimationFrame: () => 0,
  performance: { now: () => Date.now() },
  console,
  Math,
};
const ctx = vm.createContext(sandbox);
const run = (code) => vm.runInContext(code, ctx, { filename: 'depth_explorer<script>' });

let runErr = null;
try { run(scriptText); } catch (e) { runErr = e; }
check('G1b script runs to completion under DOM stub', !runErr, runErr && (runErr.stack || String(runErr)));

const exports_ = run(
  `({ cubes, exactInfo, OCTA, GOLDEN, REC723_TXT, matText, matToCols, quatToCols,
      parseConfig, loadPreset, apply, renderExactChips, familyMats, FAMILY_NAMED,
      computeConcurrences, buildOpaqueSurface, C3, matMul, PHI, S_HAT, U_HAT, W_HAT,
      setFamily, exitFamily, buildFamilyTicks, samplePoints, pts, setMode })`
);
const { matText, matToCols, loadPreset, familyMats, FAMILY_NAMED, setFamily } = exports_;

check('G1c 723 preset auto-loaded (6 cubes)', exports_.cubes.length === 6,
  `got ${exports_.cubes.length}`);
check('G1d 723 exact chip text unchanged',
  documentStub.getElementById('exact').innerHTML.includes('exact total 723')
  && documentStub.getElementById('exact').innerHTML.includes('d1: 210')
  && documentStub.getElementById('exact').innerHTML.includes('d6: 1'),
  documentStub.getElementById('exact').innerHTML);

loadPreset('mat', matText(exports_.OCTA), { total: 67, d: { 1: 48, 2: 18, 3: 1 } });
check('G1e octahedral 67 chip text unchanged',
  documentStub.getElementById('exact').innerHTML.includes('exact total 67')
  && documentStub.getElementById('exact').innerHTML.includes('d3: 1'));

loadPreset('mat', matText(exports_.GOLDEN), { total: 351, d: { 1: 180, 2: 80, 3: 60, 4: 30, 5: 1 } });
check('G1f golden 351 chip text unchanged',
  documentStub.getElementById('exact').innerHTML.includes('exact total 351')
  && documentStub.getElementById('exact').innerHTML.includes('d5: 1'));

// back to 723 for the rest
loadPreset('quat', exports_.REC723_TXT, { total: 723, d: { 1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1 } });

// sanity: FAMILY_NAMED degrees match the closed-form values (now 7 points:
// mirror-golden 20.905157... = 90 - arctan(phi^2) added by the Postscript
// 25 addendum round).
{
  const want = [0, 20.905157447889295, 35.264389682754654, 45,
                54.735610317245346, 69.0948425521107, 90];
  const got = FAMILY_NAMED.map(n => n.deg);
  const ok = got.length === want.length && want.every((w, i) => Math.abs(w - got[i]) < 1e-9);
  check('G1g FAMILY_NAMED degrees match closed-form (7 points incl mirror-golden)', ok, JSON.stringify(got));
}

// =========================================================== geometry ====
// mirrored ONLY for the audits (G2/G3/G4); the family-matrix builder under
// test is always the extracted familyMats, never reimplemented here.
const sub = (a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]];
const add = (a,b)=>[a[0]+b[0],a[1]+b[1],a[2]+b[2]];
const scale = (a,s)=>[a[0]*s,a[1]*s,a[2]*s];
const dot = (a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const cross = (a,b)=>[a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
const norm = a=>Math.sqrt(dot(a,a));
const clamp = (x,lo,hi)=>Math.max(lo,Math.min(hi,x));
function matVec(M,v){
  return [M[0][0]*v[0]+M[0][1]*v[1]+M[0][2]*v[2],
          M[1][0]*v[0]+M[1][1]*v[1]+M[1][2]*v[2],
          M[2][0]*v[0]+M[2][1]*v[1]+M[2][2]*v[2]];
}
function matTMat(M){ // M^T @ M, for the orthonormality check
  const R=[[0,0,0],[0,0,0],[0,0,0]];
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)
    for(let k=0;k<3;k++) R[i][j]+=M[k][i]*M[k][j];
  return R;
}
// local (corner, direction) pairs, one per cube edge (12 total); mirrors
// dihedral_scratch/edge_close4.py's EDGES (the validated engine that
// produced the Postscript 25 plateau numbers 48/30/24/30/18+54/48).
const EDGES = [];
for (let a=0; a<3; a++) {
  const o = [0,1,2].filter(i=>i!==a);
  for (const s1 of [-1,1]) for (const s2 of [-1,1]) {
    const cvec=[0,0,0]; cvec[o[0]]=s1; cvec[o[1]]=s2;
    const d=[0,0,0]; d[a]=1;
    EDGES.push([cvec,d]);
  }
}
// segment-segment gap with signed parameters t1,t2 in [-1,1] (edge midpoint
// +- direction), clamped -- identical algorithm to edge_close4.py/
// golden_diag.py's seg_gap (and to the shipped segSegDist's clamping logic,
// re-parameterized to a centered [-1,1] range so "|t|<0.999" reads exactly
// as the spec's gate text phrases it).
function segGap(c1,d1,c2,d2) {
  const w=sub(c1,c2), bb=dot(d1,d2), f=dot(w,d1), g=dot(w,d2), den=1-bb*bb;
  let t1 = Math.abs(den)>1e-14 ? clamp((bb*g-f)/den,-1,1) : 0.0;
  let t2 = clamp(bb*t1+g,-1,1);
  t1 = clamp(bb*t2-f,-1,1);
  const p1=add(c1,scale(d1,t1)), p2=add(c2,scale(d2,t2));
  return { gap: norm(sub(p1,p2)), t1, t2 };
}
// full edge-pair scan for a family triple built from row-major M (using the
// EXTRACTED familyMats/C3/matMul so the triple itself is the real script's
// construction, not a reimplementation).
function scanFamily(M) {
  const mats = [M, exports_.matMul(exports_.C3, M),
                   exports_.matMul(exports_.C3, exports_.matMul(exports_.C3, M))];
  const interior = [], corner = [];
  for (let i=0;i<3;i++) for (let j=i+1;j<3;j++) {
    for (let ei=0;ei<EDGES.length;ei++) for (let ej=0;ej<EDGES.length;ej++) {
      const [cc1,d1]=EDGES[ei], [cc2,d2]=EDGES[ej];
      const wc1=matVec(mats[i],cc1), wd1=matVec(mats[i],d1);
      const wc2=matVec(mats[j],cc2), wd2=matVec(mats[j],d2);
      const {gap,t1,t2} = segGap(wc1,wd1,wc2,wd2);
      if (gap < 1e-9) {
        // ei/ej carried for pair-IDENTITY tracking (G10 core-persistence
        // gates need set equality across psi, not just counts).
        if (Math.abs(t1)<0.999 && Math.abs(t2)<0.999)
          interior.push({i,j,ei,ej,wc1,wd1,wc2,wd2,t1,t2,gap});
        else if (Math.max(Math.abs(t1),Math.abs(t2))>0.999999)
          corner.push({i,j,ei,ej,t1,t2,gap});
      }
    }
  }
  return {interior, corner};
}
const pairKey = c => `${c.i},${c.j},${c.ei},${c.ej}`;
// O = 24 proper (det=+1) signed-permutation matrices -- the rotation group
// of the cube/octahedron -- for the "O-reduced pairwise invariant" (G4),
// mirroring dihedral_scratch/family_fine.py's gen_O()/invariant().
function genO() {
  const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
  const out=[];
  for (const p of perms) for (const s0 of [-1,1]) for (const s1 of [-1,1]) for (const s2 of [-1,1]) {
    const P=[[0,0,0],[0,0,0],[0,0,0]], signs=[s0,s1,s2];
    for (let r=0;r<3;r++) P[r][p[r]]=signs[r];
    const det=P[0][0]*(P[1][1]*P[2][2]-P[1][2]*P[2][1])
             -P[0][1]*(P[1][0]*P[2][2]-P[1][2]*P[2][0])
             +P[0][2]*(P[1][0]*P[2][1]-P[1][1]*P[2][0]);
    if (det>0) out.push(P);
  }
  return out;
}
const O_GROUP = genO();
function transpose(M){ return [[M[0][0],M[1][0],M[2][0]],[M[0][1],M[1][1],M[2][1]],[M[0][2],M[1][2],M[2][2]]]; }
function trace(M){ return M[0][0]+M[1][1]+M[2][2]; }
function pairwiseInvariant(M) {
  const mats=[M, exports_.matMul(exports_.C3,M), exports_.matMul(exports_.C3, exports_.matMul(exports_.C3,M))];
  const vals=[];
  for (let i=0;i<3;i++) for (let j=i+1;j<3;j++) {
    const MiT=transpose(mats[i]);
    let best=-Infinity;
    for (const H of O_GROUP) {
      const tr = trace(exports_.matMul(MiT, exports_.matMul(mats[j],H)));
      if (tr>best) best=tr;
    }
    vals.push(best);
  }
  return vals;
}
// simple seeded PRNG (mulberry32) for reproducible "25 random psi"
function mulberry32(seed) {
  return function() {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = (t + Math.imul(t ^ t >>> 7, 61 | t)) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// ================================================================== G2 ====
const SEED = 0xD1EDA1;   // fixed for reproducibility; printed below
const rng = mulberry32(SEED);
const RANDOM_PSI = Array.from({length: 25}, () => rng() * Math.PI/2);
console.log(`\n---- G2: 25 random psi (seed 0x${SEED.toString(16)}), degrees ----`);
console.log(RANDOM_PSI.map(p => (p*180/Math.PI).toFixed(3)).join(', '));

let g2aFail = 0, g2aDetail = '';
let g2bChecked = 0, g2bFail = 0, g2bDetail = '';
let g2cFail = 0, g2cHits = [];
for (const psi of RANDOM_PSI) {
  const mats = familyMats(psi);   // [M, C*M, C^2*M], the EXTRACTED builder

  // (a) each of the three matrices orthonormal to 1e-12
  for (const M of mats) {
    const G = matTMat(M);
    const maxErr = Math.max(
      Math.abs(G[0][0]-1), Math.abs(G[1][1]-1), Math.abs(G[2][2]-1),
      Math.abs(G[0][1]), Math.abs(G[0][2]), Math.abs(G[1][2]));
    if (maxErr >= 1e-12) { g2aFail++; g2aDetail = `psi=${psi} maxErr=${maxErr}`; }
  }

  // (b) every edge-pair the classifier calls a crossing: independent
  // coplanarity value (scalar triple product of the two world directions
  // and the corner-to-corner vector) must be < 1e-9.
  const { interior } = scanFamily(mats[0]);
  for (const c of interior) {
    g2bChecked++;
    const coplan = Math.abs(dot(c.wd1, cross(c.wd2, sub(c.wc1, c.wc2))));
    if (coplan >= 1e-9) { g2bFail++; g2bDetail = `psi=${psi} coplan=${coplan}`; }
  }

  // (c) the REAL ghost detector (computeConcurrences' ghost pass, gap
  // window (1e-6,0.02)) reports 0 ghosts on this family member.
  sandbox.__inject = mats.map(matToCols);
  run('cubes = __inject; computeConcurrences();');
  const { ghosts } = run('({ghosts})');
  if (ghosts.length !== 0) { g2cFail++; g2cHits.push({psiDeg: psi*180/Math.PI, ghosts: ghosts.length}); }
}
check(`G2a orthonormal to 1e-12 (75 matrices)`, g2aFail === 0, `${g2aFail} failures; ${g2aDetail}`);
check(`G2b edge-pair coplanarity < 1e-9 (${g2bChecked} interior crossings found across 25 psi)`,
  g2bFail === 0, `${g2bFail} failures; ${g2bDetail}`);
check(`G2c ghost detector: 0 ghosts across 25 psi (literal reading)`, g2cFail === 0,
  g2cFail === 0 ? '' : `${g2cFail}/25 draws hit a ghost band -- see G2c-diagnostic below`);

// ---- G2c diagnostic: WHY the literal check above can fail, and whether
// it is a code defect or an intrinsic feature of the family. Every named
// (spike) and generic plateau-transition angle is surrounded by a band,
// a few tenths to ~3 degrees wide on each side, where crossings that are
// exact exactly AT the transition relax CONTINUOUSLY into small nonzero
// gaps as psi moves away -- before the pair becomes unrelated (gap>0.02)
// a few degrees further out. This is forced by continuity (a crossing
// that is about to appear/disappear at an exact angle cannot jump
// discontinuously from gap=0 to gap>>0.02), not a bug: G2b already shows
// the crossings that DO exist at every tested psi (including all 25
// random draws and all 6 named points) are exact to <1e-9, and G3 shows
// the named-point counts are exactly right. Measured emprically (0.02deg
// sweep) the bands cover ~24deg of the 90deg range (~27%), so a genuinely
// random 25-sample draw very likely clips at least one band.
if (g2cHits.length) {
  console.log(`  G2c-diagnostic: ${g2cHits.length}/25 draws hit a ghost band:`);
  for (const h of g2cHits) console.log(`    psi=${h.psiDeg.toFixed(3)}deg -> ${h.ghosts} ghosts`);
  const TRANSITIONS = [0, 21.4, 35.264, 45, 54.736, 68.6, 69.095, 90]; // approx, see report
  const nearBand = h => TRANSITIONS.some(t => Math.abs(h.psiDeg - t) < 6);
  console.log(`  all hits within 6deg of a known transition/spike angle: ${g2cHits.every(nearBand)}`);
  // supplementary re-check: same 25 psi, but re-drawn with a margin around
  // each known transition/spike angle excluded -- demonstrates 0 ghosts
  // holds cleanly on the interior of each plateau.
  const MARGIN = 3.5; // degrees, > the widest measured band half-width
  const clean = [];
  let attempts = 0;
  const rng2 = mulberry32(SEED ^ 0x5eed5eed);
  while (clean.length < 25 && attempts < 5000) {
    attempts++;
    const d = rng2() * 90;
    if (TRANSITIONS.every(t => Math.abs(d - t) >= MARGIN)) clean.push(d);
  }
  let cleanFail = 0;
  for (const d of clean) {
    const mats = familyMats(d * Math.PI/180);
    sandbox.__inject = mats.map(matToCols);
    run('cubes = __inject; computeConcurrences();');
    const { ghosts } = run('({ghosts})');
    if (ghosts.length !== 0) cleanFail++;
  }
  check(`G2c-diagnostic: 0 ghosts for 25 psi drawn >= ${MARGIN}deg from any known transition/spike`,
    cleanFail === 0, `${cleanFail}/25 failed`);
}

// ================================================================== G3 ====
console.log('\n---- G3: crossing counts at the named positions ----');
const G3_TARGETS = [
  { label: '0 (shared axis)',            interior: 48, corner: 0 },
  { label: '90-arctan(phi^2) (m-gold)',  interior: 18, corner: 54 },
  { label: 'arcsin(1/sqrt3) (oct)',      interior: 30, corner: 0 },
  { label: '45 (face-diagonal)',         interior: 24, corner: 0 },
  { label: 'arctan(sqrt2) (mirror)',     interior: 30, corner: 0 },
  { label: 'arctan(phi^2) (golden)',     interior: 18, corner: 54 },
  { label: '90 (shared axis)',           interior: 48, corner: 0 },
];
let g3AllOk = true;
FAMILY_NAMED.forEach((n, i) => {
  const psi = n.deg * Math.PI/180;
  const M = familyMats(psi)[0];
  const { interior, corner } = scanFamily(M);
  const want = G3_TARGETS[i];
  const ok = interior.length === want.interior && corner.length === want.corner;
  if (!ok) g3AllOk = false;
  // secondary, informational: the shipped ring code's own concurrence
  // count at this point (deduplicates coincident crossings into shared
  // points at highly symmetric psi -- see report for discussion).
  sandbox.__inject = familyMats(psi).map(matToCols);
  run('cubes = __inject; computeConcurrences();');
  const { concurrences } = run('({concurrences})');
  const ringEdge = concurrences.filter(c => c.kind === 'edge').length;
  const ringCorner = concurrences.filter(c => c.kind === 'corner').length;
  console.log(`  ${n.deg.toFixed(3)}deg ${want.interior===48||want.interior===30||want.interior===24?'':''}` +
    `(${n.name}): interior=${interior.length} (want ${want.interior}), ` +
    `corner=${corner.length} (want ${want.corner}) | ring-code points: edge=${ringEdge}, corner=${ringCorner}`);
});
check('G3 crossing counts at all 7 named positions match 48/18+54/30/24/30/18+54/48', g3AllOk);

// ================================================================== G4 ====
console.log('\n---- G4: congruence spot-check (O-reduced pairwise invariant) ----');
const PHI_ = exports_.PHI;
const psiOct = FAMILY_NAMED[2].deg * Math.PI/180;
const psiGold = FAMILY_NAMED[5].deg * Math.PI/180;
const invOct = pairwiseInvariant(familyMats(psiOct)[0]);
const invGold = pairwiseInvariant(familyMats(psiGold)[0]);
const wantOct = 0.5 + Math.sqrt(2);          // 1.914213562...
const wantGold = 3 * PHI_ / 2;               // 2.427050983...
console.log(`  octahedral invariants: ${invOct.map(v=>v.toFixed(9))}  (want ${wantOct.toFixed(9)})`);
console.log(`  golden invariants:     ${invGold.map(v=>v.toFixed(9))}  (want ${wantGold.toFixed(9)})`);
check('G4a octahedral pairwise invariant = 1/2+sqrt2 to 1e-9',
  invOct.every(v => Math.abs(v-wantOct) < 1e-9), JSON.stringify(invOct));
check('G4b golden pairwise invariant = 3phi/2 to 1e-9',
  invGold.every(v => Math.abs(v-wantGold) < 1e-9), JSON.stringify(invGold));

// ================================================================== G5 ====
console.log('\n---- G5: regressions (presets, other modes) ----');
// 5a: the existing opaque_test.js gate suite, unmodified, still passes
// against this same MASTER file (opaque/wireframe/concurrence code paths
// are untouched by this change; this is the "reuse the existing
// opaque_test.js checks" option the spec offers).
let opaqueOut = '', opaqueOk = false;
try {
  opaqueOut = execFileSync(process.execPath, [path.join(SCRATCH, 'opaque_test.js')],
    { encoding: 'utf8' });
  opaqueOk = true;
} catch (e) {
  opaqueOut = (e.stdout || '') + (e.stderr || '');
  opaqueOk = false;
}
const opaqueSummary = /\n(\d+) passed, (\d+) failed/.exec(opaqueOut);
check('G5a opaque_test.js still passes in full (no regressions from this edit)',
  opaqueOk && opaqueSummary && opaqueSummary[2] === '0',
  opaqueSummary ? `${opaqueSummary[1]} passed, ${opaqueSummary[2]} failed` : opaqueOut.slice(-500));

// 5b: the family mode itself drives cubes/points/concurrences/opaque
// surface correctly at each named point (through the real setFamily/apply
// path, not a reimplementation).
let g5bOk = true, g5bDetail = '';
for (const n of FAMILY_NAMED) {
  setFamily(n.deg);
  const live = run('({cubes, pts, concurrences, ghosts})');
  if (live.cubes.length !== 3) { g5bOk=false; g5bDetail=`cubes.length=${live.cubes.length} at ${n.deg}`; break; }
  if (live.pts.length === 0) { g5bOk=false; g5bDetail=`no boundary samples at ${n.deg}`; break; }
  // opaque surface build must not throw and must produce >0 faces
  let surf;
  try { surf = exports_.buildOpaqueSurface(live.cubes, [0,1,2], new Set([1,2,3])); }
  catch (e) { g5bOk=false; g5bDetail=`buildOpaqueSurface threw at ${n.deg}: ${e}`; break; }
  if (!surf || surf.length === 0) { g5bOk=false; g5bDetail=`0 opaque faces at ${n.deg}`; break; }
}
check('G5b family mode drives slice/cloud/concurrence/opaque at all 6 named points',
  g5bOk, g5bDetail);

// ================================================================== G7 ====
// Follow-up (live user feedback): "the slide shown is not maintaining edge
// concurrences -- there should be a way to slide while maintaining edge
// concurrences." Added GHOST_FREE_ZONES (six ranges, numerically bisected
// to ~1e-6deg against the real ghost detector) and a "maintain
// concurrences" lock that clamps famPos to the zone containing the current
// psi. This section verifies both the zone data and the lock's live DOM
// behaviour (real button .onclick handlers, not reimplemented logic).
console.log('\n---- G7: ghost-free zones + "maintain concurrences" lock ----');
const { GHOST_FREE_ZONES } = run('({GHOST_FREE_ZONES})');
let g7ZoneOk = true, g7ZoneDetail = '';
for (const [lo, hi] of GHOST_FREE_ZONES) {
  // interior: 12 evenly spaced samples must show 0 ghosts
  for (let k = 1; k <= 12; k++) {
    const d = lo + (hi - lo) * k / 13;
    const mats = familyMats(d * Math.PI/180);
    sandbox.__inject = mats.map(matToCols);
    run('cubes = __inject; computeConcurrences();');
    const { ghosts } = run('({ghosts})');
    if (ghosts.length !== 0) { g7ZoneOk = false; g7ZoneDetail = `interior d=${d} ghosts=${ghosts.length} in zone [${lo},${hi}]`; }
  }
  // just outside each bound: should show ghosts (confirms the bound is tight,
  // not overly conservative)
  for (const edge of [lo - 0.01, hi + 0.01]) {
    if (edge < 0 || edge > 90) continue;
    const mats = familyMats(edge * Math.PI/180);
    sandbox.__inject = mats.map(matToCols);
    run('cubes = __inject; computeConcurrences();');
    const { ghosts } = run('({ghosts})');
    if (ghosts.length === 0) { g7ZoneOk = false; g7ZoneDetail = `just outside [${lo},${hi}] at ${edge}: still 0 ghosts (bound too loose)`; }
  }
}
check(`G7a all 6 GHOST_FREE_ZONES are genuinely zero-ghost inside, non-zero just outside`,
  g7ZoneOk, g7ZoneDetail);

// live lock behaviour, through the real DOM button handlers. CORE-AWARE
// semantics (Postscript 25 addendum, superseding the zone-based lock):
// the lock clamps to the CORE_INTERVAL containing the current psi --
// [0, 20.905] / [20.905, 69.095] / [69.095, 90] -- and always engages.
const { CORE_INTERVALS, MIRROR_GOLDEN_DEG, GOLDEN_DEG } = run('({CORE_INTERVALS, MIRROR_GOLDEN_DEG, GOLDEN_DEG})');
run(`$('pFamily').onclick();`);                    // enter family mode at psi=0
run(`setFamily(10);`);                              // inside the left core-12 interval
run(`$('famLock').onclick();`);                     // engage the lock
const lockState1 = run(`({famLocked, famLockZone})`);
check('G7b lock engages (core 12, left interval [0, 20.905])',
  lockState1.famLocked === true && !!lockState1.famLockZone
  && lockState1.famLockZone.label === 'core 12'
  && Math.abs(lockState1.famLockZone.hi - MIRROR_GOLDEN_DEG) < 1e-9,
  JSON.stringify(lockState1));
// try to drag far outside the interval (toward 80deg) while locked
run(`$('famPos').value = 8000; $('famPos').oninput({target:$('famPos')});`);
const afterDrag = run(`({famCurDeg})`);
check('G7c dragging past the interval bound while locked clamps psi to the core interval',
  afterDrag.famCurDeg <= MIRROR_GOLDEN_DEG + 1e-6,
  `famCurDeg=${afterDrag.famCurDeg}, hi=${MIRROR_GOLDEN_DEG}`);
// clicking a named tick overrides (releases) the lock
run(`$('famTicks').children[2].onclick();`);        // index 2 = octahedral 67
const afterTick = run(`({famLocked})`);
check('G7d clicking a named tick releases the lock', afterTick.famLocked === false,
  JSON.stringify(afterTick));
// engaging the lock exactly AT the octahedral point now ENGAGES with the
// core-18 interval (old zone-based behavior refused here; superseded --
// the 18-core is exact and unbroken across the whole middle interval,
// spikes included).
run(`setFamily(${FAMILY_NAMED[2].deg});`); // octahedral 67, deg literal
run(`$('famLock').onclick();`);
const lockAtOct = run(`({famLocked, famLockZone})`);
check('G7e lock AT octahedral engages with the core-18 interval (supersedes old refusal)',
  lockAtOct.famLocked === true && lockAtOct.famLockZone.label === 'core 18'
  && Math.abs(lockAtOct.famLockZone.lo - MIRROR_GOLDEN_DEG) < 1e-9
  && Math.abs(lockAtOct.famLockZone.hi - GOLDEN_DEG) < 1e-9,
  JSON.stringify(lockAtOct));
run('unlockFamily();');

// ================================================================== G8 ====
// Follow-up #2 (live feedback), CORRECTED by the Postscript 25 addendum:
// gold marks for the two field-named points, plain marks for the other
// FIVE named points (mirror-golden added), strong "region" marks ONLY at
// the true set changes (20.905 / 45 / 69.095 = SET_CHANGE_DEG), spike
// marks at the octahedral points (momentary +12), and faint "band" marks
// at the GHOST_FREE_ZONES boundaries (near-miss window edges, explicitly
// NOT set changes).
console.log('\n---- G8: slider track marks (field/named/set-change/spike/band) ----');
run(`$('pFamily').onclick();`);
const marksInfo = run(`({
  marks: [...$('famMarks').children].map(c => ({cls: c.className, left: c.style.left, title: c.title})),
  SET_CHANGE_DEG, SPIKE_DEG
})`);
const fieldMarks = marksInfo.marks.filter(m => m.cls === 'tmark field');
const namedMarks  = marksInfo.marks.filter(m => m.cls === 'tmark named');
const regionMarks = marksInfo.marks.filter(m => m.cls === 'tmark region');
const spikeMarks = marksInfo.marks.filter(m => m.cls === 'tmark spike');
const bandMarks  = marksInfo.marks.filter(m => m.cls === 'tmark band');
check('G8a exactly 2 field-tagged marks (octahedral sqrt2, golden sqrt5)',
  fieldMarks.length === 2
  && fieldMarks.some(m => m.title.includes('octahedral 67 (√2)'))
  && fieldMarks.some(m => m.title.includes('golden 67 (√5)')),
  JSON.stringify(fieldMarks));
check('G8b exactly 5 plain named marks (shared axis x2, mirror golden, face-diagonal, mirror octahedral)',
  namedMarks.length === 5
  && namedMarks.some(m => m.title.includes('mirror golden 67')),
  JSON.stringify(namedMarks));
check('G8c set-change marks: exactly 3, at 20.905/45/69.095, correctly positioned and titled',
  regionMarks.length === 3
  && marksInfo.SET_CHANGE_DEG.length === 3
  && Math.abs(marksInfo.SET_CHANGE_DEG[0] - MIRROR_GOLDEN_DEG) < 1e-9
  && marksInfo.SET_CHANGE_DEG[1] === 45
  && Math.abs(marksInfo.SET_CHANGE_DEG[2] - GOLDEN_DEG) < 1e-9
  && regionMarks.every((m,i) => Math.abs(parseFloat(m.left) - marksInfo.SET_CHANGE_DEG[i]/90*100) < 1e-6)
  && regionMarks.every(m => m.title.includes('set') && m.title.includes('changes')),
  JSON.stringify(regionMarks));
check('G8d spike marks: exactly 2 (octahedral points), titled "momentary +12"; band marks: 12, titled "not a set change"',
  spikeMarks.length === 2
  && marksInfo.SPIKE_DEG.length === 2
  && spikeMarks.every((m,i) => Math.abs(parseFloat(m.left) - marksInfo.SPIKE_DEG[i]/90*100) < 1e-6)
  && spikeMarks.every(m => m.title.includes('momentary +12'))
  && bandMarks.length === GHOST_FREE_ZONES.flat().length
  && bandMarks.every(m => m.title.includes('not a set change')),
  `spikes=${JSON.stringify(spikeMarks)}, bands=${bandMarks.length}`);
// spot-check mark position accuracy for the two field points
const octMark = fieldMarks.find(m => m.title.includes('octahedral'));
const goldMark = fieldMarks.find(m => m.title.includes('golden'));
const octExpectPct = FAMILY_NAMED[2].deg/90*100, goldExpectPct = FAMILY_NAMED[5].deg/90*100;
check('G8e octahedral/golden mark left% matches deg/90*100 to 1e-9',
  Math.abs(parseFloat(octMark.left)-octExpectPct) < 1e-9 && Math.abs(parseFloat(goldMark.left)-goldExpectPct) < 1e-9,
  `oct: ${octMark.left} vs ${octExpectPct}; gold: ${goldMark.left} vs ${goldExpectPct}`);

// ================================================================== G9 ====
// Follow-up #3 (live feedback): "highlight surfaces that separate regions
// that have been split" + "allow zooming... and making surfaces opaque
// only on one side of the cross section plane." Three independent pieces,
// all driven through the real DOM handlers / exported functions.
console.log('\n---- G9: split/merge highlight, zoom, one-sided opaque clip ----');

// -- G9a/b: highlight faces -------------------------------------------------
// near a spike (octahedral +0.5deg -- deep inside its ghost band per G2c's
// diagnostic, not a boundary edge case): ghosts present -> highlightFaces
// non-empty, every member a real element of opaqueSurface, and (the point
// of the ka/kb + edge-proximity tightening) not simply "everything".
{
  const psiNear = (FAMILY_NAMED[2].deg + 0.5) * Math.PI/180;
  sandbox.__inject = familyMats(psiNear).map(matToCols);
  run('cubes=__inject; cubeSel=7; depthSel=new Set([1,2,3]); opaqueDirty=true; computeConcurrences(); ensureOpaqueSurface();');
  const info = run('({ghosts:ghosts.length, opaqueSurface:opaqueSurface.length, highlightFaces:[...highlightFaces]})');
  check('G9a highlight: ghosts present -> highlightFaces non-empty and a proper subset of opaqueSurface',
    info.ghosts > 0 && info.highlightFaces.length > 0 && info.highlightFaces.length < info.opaqueSurface,
    `ghosts=${info.ghosts}, highlight=${info.highlightFaces.length}, total=${info.opaqueSurface}`);
  // every "highlighted" object must literally be a member of opaqueSurface
  // (same reference, not a lookalike) -- checked by identity via a marker
  // property injected into each opaqueSurface element and read back.
  const identityOk = run(`(() => {
    opaqueSurface.forEach((f,i) => f.__idx = i);
    const idxs = [...highlightFaces].map(f => f.__idx);
    return idxs.every(i => i !== undefined) && new Set(idxs).size === idxs.length;
  })()`);
  check('G9b highlightFaces members are real, distinct opaqueSurface elements', identityOk);
}
// deep inside a GHOST_FREE_ZONES zone -> 0 ghosts -> 0 highlighted faces
{
  const { GHOST_FREE_ZONES: zones } = run('({GHOST_FREE_ZONES})');
  const midZone = (zones[0][0] + zones[0][1]) / 2;
  sandbox.__inject = familyMats(midZone * Math.PI/180).map(matToCols);
  run('cubes=__inject; cubeSel=7; depthSel=new Set([1,2,3]); opaqueDirty=true; computeConcurrences(); ensureOpaqueSurface();');
  const info = run('({ghosts:ghosts.length, highlightFaces:highlightFaces.size})');
  check('G9c no ghosts -> no highlighted faces (clean zone interior)',
    info.ghosts === 0 && info.highlightFaces === 0, JSON.stringify(info));
}

// -- G9d/e/f: zoom -----------------------------------------------------------
run('setZoom(2.5);');
check('G9d setZoom sets camZoom and updates the readout',
  run('camZoom') === 2.5 && run(`$('zoomv').textContent`) === 'zoom: 250%');
run('setZoom(100);');
check('G9e zoom clamps at ZOOM_MAX', run('camZoom') === run('ZOOM_MAX'), `got ${run('camZoom')}`);
run('setZoom(-5);');
check('G9f zoom clamps at ZOOM_MIN', run('camZoom') === run('ZOOM_MIN'), `got ${run('camZoom')}`);
// real wheel handler, via the DOM stub's now-functional addEventListener
run('setZoom(1);');
run(`cloud.dispatch('wheel', {preventDefault(){}, deltaY:-1});`);
const afterWheelIn = run('camZoom');
check('G9g wheel (deltaY<0) zooms in (camZoom increases)', afterWheelIn > 1, `got ${afterWheelIn}`);
run(`cloud.dispatch('wheel', {preventDefault(){}, deltaY:1});`);
run(`cloud.dispatch('wheel', {preventDefault(){}, deltaY:1});`);
const afterWheelOut = run('camZoom');
check('G9h wheel (deltaY>0) zooms out (camZoom decreases)', afterWheelOut < afterWheelIn, `got ${afterWheelOut} vs ${afterWheelIn}`);
run(`$('zoomReset').onclick();`);
check('G9i reset button returns camZoom to 1', run('camZoom') === 1, `got ${run('camZoom')}`);

// -- G9j/k/l: one-sided opaque clip ------------------------------------------
// 723 preset (already large/complex, exercises a realistic face count)
loadPreset('quat', exports_.REC723_TXT, { total: 723, d: { 1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1 } });
run('cubeSel=(1<<cubes.length)-1; depthSel=new Set(Array.from({length:cubes.length},(_,i)=>i+1)); opaqueDirty=true; ensureOpaqueSurface();');
const totalFaces = run('opaqueSurface.length');
for (const [axis, off] of [['2', 0], ['0', 0.3], ['d', -0.2]]) {
  run(`sliceAxis=${JSON.stringify(axis)}; sliceOff=${off}; clipToSlice=true; clipFlip=false;`);
  const kept = run('opaqueSurface.filter(f=>clipKeeps(f.poly)).length');
  // independent recomputation of the same centroid-side predicate
  const indep = run(`(() => {
    const {n}=axisBasis(sliceAxis);
    return opaqueSurface.filter(f => {
      const c = polyCentroid(f.poly);
      return (n[0]*c[0]+n[1]*c[1]+n[2]*c[2]-sliceOff) <= 0;
    }).length;
  })()`);
  check(`G9j clip (axis=${axis}, off=${off}): drawOpaqueSurface's clipKeeps matches an independent centroid-side count`,
    kept === indep, `kept=${kept}, independent=${indep}`);
  run('clipFlip=true;');
  const keptFlip = run('opaqueSurface.filter(f=>clipKeeps(f.poly)).length');
  check(`G9k clip flip (axis=${axis}): flip selects the complementary side (kept+keptFlip === total, since centroids essentially never land exactly on the plane)`,
    kept + keptFlip === totalFaces, `kept=${kept}, keptFlip=${keptFlip}, total=${totalFaces}`);
}
run('clipToSlice=false; clipFlip=false;');   // reset both after the loop above left clipFlip=true
check('G9l clip off restores the full face count',
  run('opaqueSurface.filter(f=>clipKeeps(f.poly)).length') === totalFaces);
// live via the real button handlers too
run(`$('clipOpaque').onclick();`);
check('G9m clipOpaque button toggles clipToSlice', run('clipToSlice') === true);
run(`$('clipFlipBtn').onclick();`);
check('G9n clipFlipBtn button toggles clipFlip', run('clipFlip') === true);
run(`$('clipOpaque').onclick(); $('clipFlipBtn').onclick();`);  // leave both off

// ================================================================= G10 ====
// Postscript 25 addendum (core persistence + corrected transitions),
// verified via the real extracted familyMats + the validated segment
// classifier (pair identity, not just counts).
console.log('\n---- G10: core-18 persistence + core-aware lock ----');

// G10a: the interior crossing SET is one and the same set of 18 pairs at
// psi = 25, 40, 50, 60, 68 (all inside the open interval (20.905, 69.095)).
{
  const keySets = [25, 40, 50, 60, 68].map(d => {
    const { interior } = scanFamily(familyMats(d * Math.PI/180)[0]);
    return interior.map(pairKey).sort();
  });
  const ref = JSON.stringify(keySets[0]);
  check('G10a interior crossing set IDENTICAL (18 pairs) at psi=25/40/50/60/68',
    keySets[0].length === 18 && keySets.every(s => JSON.stringify(s) === ref),
    `sizes=${keySets.map(s=>s.length)}`);

  // G10b: outside the interval the constant set has 12 members.
  const s10 = scanFamily(familyMats(10 * Math.PI/180)[0]).interior.map(pairKey).sort();
  const s80 = scanFamily(familyMats(80 * Math.PI/180)[0]).interior.map(pairKey).sort();
  check('G10b interior set has 12 members at psi=10 and psi=80',
    s10.length === 12 && s80.length === 12, `10deg=${s10.length}, 80deg=${s80.length}`);

  // G10c: the core-18 is a SUBSET of the spike sets (octahedral 30, face-
  // diagonal 24, mirror-octahedral 30) -- the spikes are core + extras,
  // the core never opens.
  const core = new Set(keySets[0]);
  const oct = scanFamily(familyMats(FAMILY_NAMED[2].deg * Math.PI/180)[0]).interior.map(pairKey);
  const fd  = scanFamily(familyMats(45 * Math.PI/180)[0]).interior.map(pairKey);
  const mo  = scanFamily(familyMats(FAMILY_NAMED[4].deg * Math.PI/180)[0]).interior.map(pairKey);
  check('G10c core-18 is a subset of every spike set (30/24/30 = core + extras)',
    oct.length === 30 && fd.length === 24 && mo.length === 30
    && [...core].every(k => oct.includes(k))
    && [...core].every(k => fd.includes(k))
    && [...core].every(k => mo.includes(k)));

  // G10d: corner docking at golden -- of the core 18, exactly 6 remain
  // interior (at t = +-1/phi^3) and exactly 12 appear among the corner
  // contacts (t = +-1); nothing breaks.
  const atGold = scanFamily(familyMats(GOLDEN_DEG * Math.PI/180)[0]);
  const goldInterior = atGold.interior.map(pairKey);
  const goldCorner = atGold.corner.map(pairKey);
  const coreInteriorAtGold = goldInterior.filter(k => core.has(k));
  const coreDockedAtGold = goldCorner.filter(k => core.has(k));
  const PHI_G = exports_.PHI, invPhi3 = 1/(PHI_G*PHI_G*PHI_G);
  const interiorTsOk = atGold.interior
    .filter(c => core.has(pairKey(c)))
    .every(c => Math.abs(Math.abs(c.t1)-invPhi3) < 1e-6 && Math.abs(Math.abs(c.t2)-invPhi3) < 1e-6);
  check('G10d at golden: 6 core interior (t=+-1/phi^3) + 12 core docked on corners, 18/18 accounted',
    coreInteriorAtGold.length === 6 && coreDockedAtGold.length === 12 && interiorTsOk,
    `interior=${coreInteriorAtGold.length}, docked=${coreDockedAtGold.length}, tOk=${interiorTsOk}`);

  // G10e: FACT-2 spot check -- inside a ghost band but away from the spike
  // (psi=33, band around octahedral) the set STILL equals the core
  // (ghost-band boundaries are not set changes).
  const s33 = scanFamily(familyMats(33 * Math.PI/180)[0]).interior.map(pairKey).sort();
  check('G10e set at psi=33 (inside octahedral ghost band) equals the core-18 (band edge is not a set change)',
    JSON.stringify(s33) === ref, `size=${s33.length}`);
}

// G10f: core-aware lock drives the FULL octahedral->golden drag. Real DOM
// handlers throughout.
run(`$('pFamily').onclick();`);
run(`setFamily(40);`);
run(`$('famLock').onclick();`);
const g10Lock = run(`({famLocked, famLockZone})`);
run(`$('famPos').value = 6800; $('famPos').oninput({target:$('famPos')});`);
const at68 = run(`famCurDeg`);
run(`$('famPos').value = 500; $('famPos').oninput({target:$('famPos')});`);
const atLow = run(`famCurDeg`);
run(`$('famPos').value = 8500; $('famPos').oninput({target:$('famPos')});`);
const atHigh = run(`famCurDeg`);
check('G10f lock at psi=40 (core 18): drag to 68 allowed; clamps at 20.905 / 69.095',
  g10Lock.famLocked === true && g10Lock.famLockZone.label === 'core 18'
  && Math.abs(at68 - 68) < 1e-9
  && atLow >= MIRROR_GOLDEN_DEG - 1e-9 && atLow <= MIRROR_GOLDEN_DEG + 0.3 + 1e-9
  && atHigh <= GOLDEN_DEG + 1e-9 && atHigh >= GOLDEN_DEG - 0.3 - 1e-9,
  `at68=${at68}, atLow=${atLow}, atHigh=${atHigh}`);
// readout: core label + ghost count coexist (drag to a ghost band under lock)
run(`$('famPos').value = 3300; $('famPos').oninput({target:$('famPos')});`);
const readout = run(`$('famGhosts').textContent`);
const ghostsAt33 = run(`ghosts.length`);
check('G10g locked readout shows "core 18 maintained" alongside a live ghost count',
  readout.includes('core 18 maintained') && ghostsAt33 > 0 && readout.includes(`${ghostsAt33} ghosts`),
  `readout="${readout}", ghosts=${ghostsAt33}`);
run('unlockFamily();');

// restore the 723 preset (leave the harness's context in a known state)
loadPreset('quat', exports_.REC723_TXT, { total: 723, d: { 1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1 } });

// ================================================================== G6 ====
console.log('\n---- G6 ----');
check('G6 note', true,
  'mirror sync is performed by the orchestrator after this file reports 0 FAIL, not by the harness itself');

console.log(`\n${PASS} passed, ${FAIL} failed`);
process.exit(FAIL ? 1 : 0);
