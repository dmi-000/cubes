const vm = require('vm');
const fs = require('fs');

const src = fs.readFileSync(__dirname + '/_c.js', 'utf8');

function makeCtx() {
  return {
    fillStyle: '', strokeStyle: '', lineWidth: 1, globalAlpha: 1,
    createImageData(w, h) { return { data: new Uint8ClampedArray(w * h * 4) }; },
    putImageData() {}, fillRect() {}, strokeRect() {}, beginPath() {}, moveTo() {},
    lineTo() {}, closePath() {}, fill() {}, stroke() {}, arc() {}, setLineDash() {},
    save() {}, restore() {}, clearRect() {},
  };
}

function makeEl(id) {
  const el = {
    id, textContent: '', innerHTML: '', value: '', style: {}, children: [],
    width: (id === 'slice' || id === 'cloud') ? 520 : undefined,
    height: (id === 'slice' || id === 'cloud') ? 520 : undefined,
    appendChild() {}, addEventListener() {}, setPointerCapture() {},
    setAttribute() {}, getAttribute() { return null; },
    ariaPressed: 'false',
    getContext() { return makeCtx(); },
  };
  return el;
}

const elCache = {};
const sandbox = {
  console,
  Math, Array, Object, Number, String, Boolean, JSON, Set, Uint8Array, Int8Array,
  Uint8ClampedArray, parseInt, isNaN,
  document: {
    getElementById(id) { return elCache[id] || (elCache[id] = makeEl(id)); },
  },
  matchMedia() { return { matches: false }; },
  requestAnimationFrame() { /* no-op: avoid recursing */ },
};
sandbox.window = sandbox;
vm.createContext(sandbox);
// `const`/`let` top-level bindings in a vm context do NOT become properties
// of the sandbox object, only `var` does — so append an exporter using `var`
// that closes over the script's lexical scope to hand back what we need.
const exporter = `
var __exports__ = {
  slideMats: slideMats, matToCols: matToCols, segSegDist: segSegDist,
  cubeEdgeSegs: cubeEdgeSegs, computeConcurrences: computeConcurrences,
  getCubes: function(){ return cubes; }, setCubes: function(c){ cubes = c; },
  getConcurrences: function(){ return concurrences; },
  getGhosts: function(){ return ghosts; }
};
`;
vm.runInContext(src + '\n' + exporter, sandbox, { filename: 'depth_explorer_inline.js' });
const api = sandbox.__exports__;

// ---- functional check: use the script's own slideMats/matToCols/cubes/
// computeConcurrences/segSegDist/cubeEdgeSegs via the sandbox global scope ----
function setCubesFromSlide(t) {
  const mats = api.slideMats(t);
  api.setCubes(mats.map(api.matToCols));
}

function countEdgePairsByGap(lo, hi) {
  const cubes = api.getCubes();
  const edgeSets = cubes.map((_, k) => api.cubeEdgeSegs(k));
  let n = 0;
  const gaps = [];
  for (let ka = 0; ka < cubes.length; ka++)
    for (let kb = ka + 1; kb < cubes.length; kb++)
      for (const ea of edgeSets[ka])
        for (const eb of edgeSets[kb]) {
          const { dist } = api.segSegDist(ea[0], ea[1], eb[0], eb[1]);
          if (dist > lo && dist < hi) { n++; gaps.push(dist); }
        }
  return { n, gaps };
}

for (const t of [0, 0.5, 1]) {
  setCubesFromSlide(t);
  const exact = countEdgePairsByGap(-1, 1e-6); // dist < 1e-6 (essentially exact)
  const ghost = countEdgePairsByGap(1e-6, 0.02);
  console.log(`t=${t}: exact(<1e-6)=${exact.n}  ghost(1e-6..0.02)=${ghost.n}  gaps=${ghost.gaps.map(g=>g.toFixed(4)).join(',')}`);
}

// also run computeConcurrences() proper (populates ghosts/concurrences)
// and check counts + cloudn text.
for (const t of [0, 0.5, 1]) {
  setCubesFromSlide(t);
  api.computeConcurrences();
  console.log(`t=${t} computeConcurrences: concurrences=`, api.getConcurrences().length, 'ghosts=', api.getGhosts().length);
  console.log(`cloudn text @${t}:`, elCache['cloudn'].textContent);
}

// smoke-test the render paths (renderSlice / drawCloud) don't throw now
// that ghosts are populated, using the no-op canvas-context stubs.
const rendererExporter = `
var __render__ = { renderSlice: renderSlice, drawCloud: drawCloud };
`;
vm.runInContext(rendererExporter, sandbox);
setCubesFromSlide(0.5);
sandbox.pts = [];
api.computeConcurrences();
sandbox.__render__.renderSlice();
sandbox.__render__.drawCloud();
console.log('renderSlice/drawCloud ran without throwing at t=0.5, ghosts=', api.getGhosts().length);
