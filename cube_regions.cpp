// Working principles: CPP_SPEC.md. Project index: README.md
// cube_regions.cpp -- exact bounded-region counter for compounds of N
// congruent concentric cubes, ported from certify_six.py::exact_count_config
// and mt_sim.py's seed chain. Pure integer arithmetic (int64 + __int128).
// Build:  clang++ -O2 -std=c++17 -o cube_regions cube_regions.cpp
//
// N-GENERALIZATION (see NPLUS_SPEC.md): everything that was a compile-time
// "6" for cube count is now a runtime `n` (2..12 supported; the overflow
// budget below is n-independent so larger n is not unsafe, just untested).
// planes[] / owner_cube[] / owner_axis[] are sized 6n(+6 box); the
// per-cell sign-vector `mask` -- one bit per CUBE plane processed so far,
// used to recover a cell's label and real-facet ownership by pure bitmask
// logic (see the original design note below) -- needs up to 6n bits, so
// it is unsigned __int128 (128 bits, safe through n=21) instead of
// uint64_t (which silently truncated for n>10 at 6n=60..64 bits: KEEP the
// wide type even though it looks like overkill at n=6-8, that truncation
// is a silent-wrong-answer bug, not a crash). Region *labels* (which
// cubes contain a cell) are only n bits wide and stay a plain int.
//
// See CPP_SPEC.md for the full design rationale. Summary of the key
// algorithmic move (equivalent to, but safer than, the Python centroid
// approach): instead of computing an interior point's coordinates and
// testing plane signs there, we track -- for every final arrangement cell
// -- the EXACT sign (+1/-1) it took relative to each cube plane at the
// moment that plane was processed during incremental clipping. In any
// hyperplane arrangement, two adjacent cells sharing a facet on plane P
// have IDENTICAL sign for every OTHER plane and OPPOSITE sign for P; so
// this per-cell sign vector is enough to compute both the label (which
// cubes contain the cell) and the facet reality/flip test (does the facet
// lie inside a cube's actual square face) via pure bitmask logic -- no
// floating point, no big-rational centroid, no risk of a near-wall
// misclassification. Vertex COORDINATES (via plane-triple Cramer's rule,
// int128, gcd-canonicalized) are still needed, but only for facet identity
// (which two cells share the same polygon) and for building new cut
// vertices -- exactly the part the spec calls out as safe in int128.
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <array>
#include <unordered_map>
#include <map>
#include <set>
#include <algorithm>
#include <functional>
#include <stdexcept>
#include <sstream>
#include <iostream>
#include <chrono>
#include <string>

using i64 = int64_t;
using i128 = __int128;
using u128 = unsigned __int128;

// ------------------------------------------------------------- i128 utils
static inline i128 iabs128(i128 x) { return x < 0 ? -x : x; }
static inline i128 igcd128(i128 a, i128 b) {
    a = iabs128(a); b = iabs128(b);
    while (b) { i128 t = a % b; a = b; b = t; }
    return a;
}
static inline i64 igcd64(i64 a, i64 b) {
    a = a < 0 ? -a : a; b = b < 0 ? -b : b;
    while (b) { i64 t = a % b; a = b; b = t; }
    return a;
}

struct ConfigError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

// ------------------------------------------------------------------ Plane
// a*x + b*y + c*z = d.  Planes 0..6n-1 = n cubes x 3 axes x 2 signs
// (pid = k*6 + j*2 + (c==+1?0:1)).  Planes 6n..6n+5 = the 6 fixed box
// planes of [-4,4]^3 (pid = 6n + axis*2 + (sign==+1?0:1)).
struct Plane { i64 a, b, c, d; };
static int g_n = 6;         // number of cubes (runtime; default 6)
static int g_npl = 42;      // total plane count = 6*g_n + 6
static std::vector<Plane> planes;
static std::vector<int> owner_cube, owner_axis;   // sized 6*g_n

static inline int boxid(int axis, int sign) { return 6 * g_n + axis * 2 + (sign > 0 ? 0 : 1); }

// -------------------------------------------------------- coincident planes
struct PKey {
    i64 a, b, c, d;
    bool operator==(const PKey& o) const { return a == o.a && b == o.b && c == o.c && d == o.d; }
};
struct PKeyHash {
    size_t operator()(const PKey& k) const {
        size_t h = 1469598103934665603ULL;
        auto mix = [&](i64 v) { h ^= (size_t)v; h *= 1099511628211ULL; };
        mix(k.a); mix(k.b); mix(k.c); mix(k.d);
        return h;
    }
};
static PKey planeKey(int pid) {
    i64 a = planes[pid].a, b = planes[pid].b, c = planes[pid].c, d = planes[pid].d;
    i64 g = igcd64(igcd64(igcd64(a, b), c), d);
    if (g == 0) g = 1;
    a /= g; b /= g; c /= g; d /= g;
    i64 s = a; if (s == 0) s = b; if (s == 0) s = c;
    if (s < 0) { a = -a; b = -b; c = -c; d = -d; }
    return {a, b, c, d};
}

// ---------------------------------------------------------------- Vertices
// A vertex is the intersection of exactly 3 planes ("its triple"). Its
// homogeneous coordinates (X,Y,Z,W), W>0, are computed once via Cramer's
// rule and cached, keyed by the (sorted) plane triple.
struct VData { i128 X, Y, Z, W; int t0, t1, t2; };
static std::vector<VData> verts;
static std::vector<int> triLookup; // size g_npl^3, -1 = uncomputed
static int triLookupNPL = -1;      // NPL the current triLookup buffer was sized for

static inline i128 det3(i128 a1, i128 b1, i128 c1,
                         i128 a2, i128 b2, i128 c2,
                         i128 a3, i128 b3, i128 c3) {
    return a1 * (b2 * c3 - b3 * c2) - b1 * (a2 * c3 - a3 * c2) + c1 * (a2 * b3 - a3 * b2);
}

static int get_vertex(int p0, int p1, int p2) {
    int a = p0, b = p1, c = p2;
    if (a > b) std::swap(a, b);
    if (b > c) std::swap(b, c);
    if (a > b) std::swap(a, b);
    int key = a * g_npl * g_npl + b * g_npl + c;
    int idx = triLookup[key];
    if (idx >= 0) return idx;
    const Plane& P0 = planes[a]; const Plane& P1 = planes[b]; const Plane& P2 = planes[c];
    i128 W = det3(P0.a, P0.b, P0.c, P1.a, P1.b, P1.c, P2.a, P2.b, P2.c);
    i128 X = det3(P0.d, P0.b, P0.c, P1.d, P1.b, P1.c, P2.d, P2.b, P2.c);
    i128 Y = det3(P0.a, P0.d, P0.c, P1.a, P1.d, P1.c, P2.a, P2.d, P2.c);
    i128 Z = det3(P0.a, P0.b, P0.d, P1.a, P1.b, P1.d, P2.a, P2.b, P2.d);
    i128 g = igcd128(igcd128(igcd128(iabs128(X), iabs128(Y)), iabs128(Z)), iabs128(W));
    if (g == 0) throw ConfigError("degenerate vertex: all-zero plane triple (non-generic config)");
    X /= g; Y /= g; Z /= g; W /= g;
    if (W < 0) { X = -X; Y = -Y; Z = -Z; W = -W; }
    if (W == 0) throw ConfigError("degenerate plane triple: no unique intersection (non-generic config)");
    VData vd{X, Y, Z, W, a, b, c};
    idx = (int)verts.size();
    verts.push_back(vd);
    triLookup[key] = idx;
    return idx;
}

static inline int sidesign(int vidx, int pid) {
    const VData& V = verts[vidx]; const Plane& P = planes[pid];
    i128 val = (i128)P.a * V.X + (i128)P.b * V.Y + (i128)P.c * V.Z - (i128)P.d * V.W;
    return (val > 0) - (val < 0);
}

// -------------------------------------------------------------- Cell/Face
// Face.edgePlane[k] is the plane defining the edge (loop[k], loop[(k+1)%m])
// -- i.e. the OTHER plane (besides f.pid) whose intersection with f.pid
// gives that edge's line. This is carried explicitly (not re-derived from
// vertex plane-triples after the fact): the CPP_SPEC's "generic configs
// only" caveat on plane-triple identity bites hard for structured inputs
// like the axial family, where 4+ planes can concur at a single point,
// making triple-intersection an ambiguous (and here, actively wrong) way
// to recover an edge's identity. Carrying the edge plane forward through
// every clip step sidesteps that degeneracy entirely and is exact for
// both generic and structured configs.
struct Face { int pid; std::vector<int> loop; std::vector<int> edgePlane; };
struct Cell { std::vector<Face> faces; u128 mask; };

enum class ClipStatus { ALL_NEG, ALL_POS, SPLIT };
struct ClipOut {
    ClipStatus status;
    bool hasNeg = false, hasPos = false;
    std::vector<Face> neg, pos;
};

// Generation-stamped sign cache: much cheaper than a hash map for the
// "sign of vertex v against the current plane" memoization that clip()
// needs, since vertex ids are small dense integers. Persists (and its
// backing storage keeps growing) across the whole process; `cur` only
// ever increases so stale entries from earlier configs/planes can never
// alias as hits.
struct SignCache {
    std::vector<int64_t> stamp;
    std::vector<int8_t> val;
    int64_t cur = 0;
    void bump() { cur++; }
    int get(int v, int pid) {
        if (v >= (int)stamp.size()) { stamp.resize(v + 256, 0); val.resize(v + 256); }
        if (stamp[v] == cur) return val[v];
        int s = sidesign(v, pid);
        stamp[v] = cur; val[v] = (int8_t)s;
        return s;
    }
};

static SignCache g_signCache;

static ClipOut clip(const std::vector<Face>& faces, int pid, SignCache& signCache) {
    ClipOut res;
    auto sgn = [&](int v) -> int { return signCache.get(v, pid); };
    bool anyPos = false, anyNeg = false;
    for (auto& f : faces) {
        for (int v : f.loop) {
            int s = sgn(v);
            if (s > 0) anyPos = true; else if (s < 0) anyNeg = true;
        }
        if (anyPos && anyNeg) break;
    }
    if (!anyPos) { res.status = ClipStatus::ALL_NEG; return res; }
    if (!anyNeg) { res.status = ClipStatus::ALL_POS; return res; }
    res.status = ClipStatus::SPLIT;

    for (int ki = 0; ki < 2; ki++) {
        int keep = ki == 0 ? -1 : 1;
        std::vector<Face> new_faces;
        // cap_edges: (vertex1, vertex2, sourceFacePid) -- the edge of the
        // new cap polygon contributed by original face sourceFacePid.
        std::vector<std::array<int,3>> cap_edges;
        for (auto& f : faces) {
            std::vector<int> out;      // raw pushed vertices
            std::vector<int> outSrc;   // original edge index that produced each push
            std::vector<char> outOrig; // 1 if pushed via the ORIG (kept-p) path, 0 if CUT
            std::vector<int> zeros;
            int m = (int)f.loop.size();
            for (int i = 0; i < m; i++) {
                int p = f.loop[i], q = f.loop[(i + 1) % m];
                int sp = sgn(p), sq = sgn(q);
                if (sp * keep >= 0) {
                    out.push_back(p); outSrc.push_back(i); outOrig.push_back(1);
                    if (sp == 0) zeros.push_back(p);
                }
                if (sp * sq < 0) {
                    int w = get_vertex(f.pid, f.edgePlane[i], pid);
                    out.push_back(w); outSrc.push_back(i); outOrig.push_back(0);
                    zeros.push_back(w);
                }
            }
            int n = (int)out.size();
            if (n == 0) continue;
            // inEdgePlane[k] = plane of the edge from out[(k-1+n)%n] to out[k]
            std::vector<int> inEdgePlane(n);
            for (int k = 0; k < n; k++) {
                int kp = (k - 1 + n) % n;
                if (outSrc[k] == outSrc[kp]) {
                    inEdgePlane[k] = f.edgePlane[outSrc[kp]];
                } else if (outSrc[k] == (outSrc[kp] + 1) % m && outOrig[k]) {
                    inEdgePlane[k] = f.edgePlane[outSrc[kp]];
                } else {
                    inEdgePlane[k] = pid;
                }
            }
            std::vector<int> ded, dedIn;
            for (int i = 0; i < n; i++) {
                int pr = (i - 1 + n) % n;
                if (out[i] != out[pr]) { ded.push_back(out[i]); dedIn.push_back(inEdgePlane[i]); }
            }
            if ((int)ded.size() >= 3) {
                int dn = (int)ded.size();
                std::vector<int> newEdgePlane(dn);
                for (int k = 0; k < dn; k++) newEdgePlane[k] = dedIn[(k + 1) % dn];
                new_faces.push_back({f.pid, std::move(ded), std::move(newEdgePlane)});
            }
            std::vector<int> zs;
            for (int z : zeros) if (std::find(zs.begin(), zs.end(), z) == zs.end()) zs.push_back(z);
            if (zs.size() == 2) cap_edges.push_back({zs[0], zs[1], f.pid});
        }
        if (!cap_edges.empty()) {
            std::unordered_map<int, std::vector<std::pair<int,int>>> nbr; // v -> [(neighbor, sourceFacePid)]
            for (auto& e : cap_edges) {
                nbr[e[0]].push_back({e[1], e[2]});
                nbr[e[1]].push_back({e[0], e[2]});
            }
            int start = cap_edges[0][0];
            std::vector<int> loop = {start};
            std::vector<int> edgePl;
            int prev = -1, cur = start;
            while (true) {
                std::pair<int,int> nxt{-1,-1};
                bool found = false;
                for (auto& x : nbr[cur]) if (x.first != prev) { nxt = x; found = true; break; }
                if (!found) break;
                edgePl.push_back(nxt.second);
                prev = cur; cur = nxt.first;
                if (cur == start) break;
                loop.push_back(cur);
            }
            if (loop.size() >= 3 && cur == start && edgePl.size() == loop.size())
                new_faces.push_back({-2, std::move(loop), std::move(edgePl)});
        }
        if (keep == -1) { res.hasNeg = !new_faces.empty(); res.neg = std::move(new_faces); }
        else { res.hasPos = !new_faces.empty(); res.pos = std::move(new_faces); }
    }
    return res;
}

// -------------------------------------------------------------- top-level
struct Result {
    long long total;
    std::map<int,int> by_depth;
    std::map<int,int> per_label;
};

static Result exact_count_config(const std::vector<std::array<i64,4>>& quats) {
    int n = (int)quats.size();
    g_n = n;
    g_npl = 6 * n + 6;
    planes.assign(g_npl, Plane{0,0,0,0});
    owner_cube.assign(6 * n, 0);
    owner_axis.assign(6 * n, 0);

    verts.clear();
    if (triLookupNPL != g_npl) {
        triLookup.assign((size_t)g_npl * g_npl * g_npl, -1);
        triLookupNPL = g_npl;
    } else {
        std::fill(triLookup.begin(), triLookup.end(), -1);
    }

    for (int axis = 0; axis < 3; axis++) {
        for (int si = 0; si < 2; si++) {
            int sign = si == 0 ? 1 : -1;
            int pid = boxid(axis, sign);
            planes[pid] = { (i64)(axis == 0), (i64)(axis == 1), (i64)(axis == 2), (i64)sign * 4 };
        }
    }

    for (int k = 0; k < n; k++) {
        i64 w = quats[k][0], x = quats[k][1], y = quats[k][2], z = quats[k][3];
        i64 nn = w*w + x*x + y*y + z*z;
        if (nn == 0) throw ConfigError("zero quaternion");
        i64 M[3][3];
        M[0][0]=w*w+x*x-y*y-z*z; M[0][1]=2*(x*y-w*z); M[0][2]=2*(x*z+w*y);
        M[1][0]=2*(x*y+w*z);     M[1][1]=w*w-x*x+y*y-z*z; M[1][2]=2*(y*z-w*x);
        M[2][0]=2*(x*z-w*y);     M[2][1]=2*(y*z+w*x);     M[2][2]=w*w-x*x-y*y+z*z;
        for (int j = 0; j < 3; j++) {
            i64 a = M[0][j], b = M[1][j], c = M[2][j];
            for (int cs = 0; cs < 2; cs++) {
                int csign = cs == 0 ? 1 : -1;
                int pid = k*6 + j*2 + cs;
                planes[pid] = {a, b, c, (i64)csign * nn};
                owner_cube[pid] = k; owner_axis[pid] = j;
            }
        }
    }

    std::vector<std::vector<std::pair<int,int>>> owners_of(6 * n);
    {
        std::unordered_map<PKey, std::vector<int>, PKeyHash> classes;
        for (int pid = 0; pid < 6 * n; pid++) classes[planeKey(pid)].push_back(pid);
        for (int pid = 0; pid < 6 * n; pid++) {
            auto& cls = classes[planeKey(pid)];
            for (int p2 : cls) owners_of[pid].push_back({owner_cube[p2], owner_axis[p2]});
        }
    }

    Cell c0; c0.mask = 0;
    for (int axis = 0; axis < 3; axis++) {
        int a, b;
        if (axis == 0) { a = 1; b = 2; } else if (axis == 1) { a = 0; b = 2; } else { a = 0; b = 1; }
        for (int fs = 0; fs < 2; fs++) {
            int facesign = fs == 0 ? 1 : -1;
            int facePlane = boxid(axis, facesign);
            int pa_neg = boxid(a, -1), pa_pos = boxid(a, 1);
            int pb_neg = boxid(b, -1), pb_pos = boxid(b, 1);
            int p00 = get_vertex(facePlane, pa_neg, pb_neg);
            int p01 = get_vertex(facePlane, pa_neg, pb_pos);
            int p11 = get_vertex(facePlane, pa_pos, pb_pos);
            int p10 = get_vertex(facePlane, pa_pos, pb_neg);
            // edges: p00->p01 on pa_neg; p01->p11 on pb_pos; p11->p10 on pa_pos; p10->p00 on pb_neg
            c0.faces.push_back({facePlane, {p00, p01, p11, p10}, {pa_neg, pb_pos, pa_pos, pb_neg}});
        }
    }
    std::vector<Cell> cells = {std::move(c0)};

    for (int pid = 0; pid < 6 * n; pid++) {
        g_signCache.bump();
        std::vector<Cell> nxt;
        nxt.reserve(cells.size() * 2);
        for (auto& cell : cells) {
            if (cell.faces.size() == 0) continue;
            ClipOut cr = clip(cell.faces, pid, g_signCache);
            if (cr.status == ClipStatus::ALL_NEG) {
                nxt.push_back({std::move(cell.faces), cell.mask});
                continue;
            }
            if (cr.status == ClipStatus::ALL_POS) {
                nxt.push_back({std::move(cell.faces), cell.mask | ((u128)1 << pid)});
                continue;
            }
            if (cr.hasNeg) {
                for (auto& f : cr.neg) if (f.pid == -2) f.pid = pid;
                nxt.push_back({std::move(cr.neg), cell.mask});
            }
            if (cr.hasPos) {
                for (auto& f : cr.pos) if (f.pid == -2) f.pid = pid;
                nxt.push_back({std::move(cr.pos), cell.mask | ((u128)1 << pid)});
            }
        }
        cells = std::move(nxt);
    }

    int ncell = (int)cells.size();
    auto slabOk = [&](u128 mask, int k, int j) -> bool {
        int posPid = k*6 + j*2 + 0, negPid = k*6 + j*2 + 1;
        bool posBit = (bool)((mask >> posPid) & 1), negBit = (bool)((mask >> negPid) & 1);
        return (!posBit) && negBit;
    };
    auto labelOf = [&](u128 mask) -> int {
        int lab = 0;
        for (int k = 0; k < n; k++)
            if (slabOk(mask,k,0) && slabOk(mask,k,1) && slabOk(mask,k,2)) lab |= 1 << k;
        return lab;
    };
    std::vector<int> labs(ncell);
    for (int i = 0; i < ncell; i++) labs[i] = labelOf(cells[i].mask);

    struct GKey {
        int pid; std::vector<int> verts;
        bool operator==(const GKey& o) const { return pid == o.pid && verts == o.verts; }
    };
    struct GKeyHash {
        size_t operator()(const GKey& k) const {
            size_t h = 1469598103934665603ULL ^ (size_t)k.pid;
            for (int v : k.verts) { h ^= (size_t)v; h *= 1099511628211ULL; }
            return h;
        }
    };
    std::unordered_map<GKey, std::vector<int>, GKeyHash> groups;
    for (int ci = 0; ci < ncell; ci++) {
        for (auto& f : cells[ci].faces) {
            if (f.pid >= 6 * n) continue; // box face: never a real internal facet
            std::vector<int> key = f.loop;
            std::sort(key.begin(), key.end());
            key.erase(std::unique(key.begin(), key.end()), key.end());
            groups[GKey{f.pid, std::move(key)}].push_back(ci);
        }
    }

    std::vector<int> parent(ncell);
    for (int i = 0; i < ncell; i++) parent[i] = i;
    std::function<int(int)> find = [&](int x) -> int {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    };

    for (auto& kv : groups) {
        const auto& cs = kv.second;
        if (cs.size() != 2) throw ConfigError("facet shared by != 2 cells");
        int a = cs[0], b = cs[1];
        int pid = kv.first.pid;
        int flip = 0;
        for (auto& owner : owners_of[pid]) {
            int kk = owner.first, jj = owner.second;
            bool real = true;
            for (int t = 0; t < 3; t++) if (t != jj) real = real && slabOk(cells[a].mask, kk, t);
            if (real) flip |= (1 << kk);
        }
        if (flip) {
            if ((labs[a] ^ labs[b]) != flip) throw ConfigError("real facet flip mismatch");
        } else {
            if (labs[a] != labs[b]) throw ConfigError("phantom facet label mismatch");
            int ra = find(a), rb = find(b);
            if (ra != rb) parent[ra] = rb;
        }
    }

    std::set<std::pair<int,int>> comps;
    for (int i = 0; i < ncell; i++) comps.insert({labs[i], find(i)});
    std::map<int,int> per_label;
    for (auto& p : comps) per_label[p.first]++;
    if (per_label.count(0) == 0 || per_label[0] != 1) throw ConfigError("outside must be a single region");
    std::map<int,int> by_depth;
    long long total = 0;
    for (auto& kv : per_label) {
        int d = __builtin_popcount((unsigned)kv.first);
        by_depth[d] += kv.second;
        total += kv.second;
    }
    total -= 1;
    return {total, by_depth, per_label};
}

// ------------------------------------------------------------ seed chain
// Bit-exact port of mt_sim.py: numpy legacy MT19937 seeding, Marsaglia
// polar Gaussian with has_gauss cache, normalize, scipy-style largest-
// |component|-positive sign convention, round(c*scale), gcd-reduce.
// mt_sim.py's sim_quats(seed, n) already generalizes to n cubes (it just
// draws 4n gaussians instead of 24); this port mirrors that unchanged.
struct MT19937 {
    uint32_t mt[624];
    int idx;
    bool has_gauss;
    double gauss_val;
    explicit MT19937(uint32_t seed) {
        mt[0] = seed;
        for (int i = 1; i < 624; i++)
            mt[i] = (uint32_t)(1812433253u * (mt[i-1] ^ (mt[i-1] >> 30)) + (uint32_t)i);
        idx = 624; has_gauss = false; gauss_val = 0.0;
    }
    uint32_t u32() {
        if (idx >= 624) {
            for (int i = 0; i < 624; i++) {
                uint32_t y = (mt[i] & 0x80000000u) | (mt[(i+1)%624] & 0x7fffffffu);
                mt[i] = mt[(i+397)%624] ^ (y >> 1);
                if (y & 1u) mt[i] ^= 0x9908B0DFu;
            }
            idx = 0;
        }
        uint32_t y = mt[idx++];
        y ^= y >> 11;
        y ^= (y << 7) & 0x9D2C5680u;
        y ^= (y << 15) & 0xEFC60000u;
        y ^= y >> 18;
        return y;
    }
    double dbl() {
        uint32_t a = u32() >> 5, b = u32() >> 6;
        return (a * 67108864.0 + b) / 9007199254740992.0;
    }
    double gauss() {
        if (has_gauss) { has_gauss = false; return gauss_val; }
        double x1, x2, r2;
        do {
            x1 = 2.0 * dbl() - 1.0;
            x2 = 2.0 * dbl() - 1.0;
            r2 = x1*x1 + x2*x2;
        } while (!(r2 < 1.0 && r2 != 0.0));
        double f = std::sqrt(-2.0 * std::log(r2) / r2);
        gauss_val = f * x1; has_gauss = true;
        return f * x2;
    }
};

static inline i64 py_round(double x) { return (i64)std::nearbyint(x); }

static std::vector<std::array<i64,4>> sim_quats(uint32_t seed, int n, int scale = 512) {
    MT19937 mt(seed);
    std::vector<std::array<i64,4>> out;
    out.reserve(n);
    for (int i = 0; i < n; i++) {
        double x = mt.gauss(), y = mt.gauss(), z = mt.gauss(), w = mt.gauss();
        double nrm = std::sqrt(x*x + y*y + z*z + w*w);
        double q[4] = { w/nrm, x/nrm, y/nrm, z/nrm };
        int m = 0; double best = std::fabs(q[0]);
        for (int t = 1; t < 4; t++) if (std::fabs(q[t]) > best) { best = std::fabs(q[t]); m = t; }
        if (q[m] < 0) for (int t = 0; t < 4; t++) q[t] = -q[t];
        i64 ints[4];
        for (int t = 0; t < 4; t++) ints[t] = py_round(q[t] * scale);
        bool allZero = true; for (int t = 0; t < 4; t++) if (ints[t] != 0) allZero = false;
        if (allZero) { ints[0]=1; ints[1]=ints[2]=ints[3]=0; }
        i64 g = igcd64(igcd64(igcd64(ints[0], ints[1]), ints[2]), ints[3]);
        if (g > 1) for (int t = 0; t < 4; t++) ints[t] /= g;
        out.push_back({ints[0], ints[1], ints[2], ints[3]});
    }
    return out;
}

// ------------------------------------------------------------------- I/O
static std::string mapToJson(const std::map<int,int>& m) {
    std::string s = "{"; bool first = true;
    for (auto& kv : m) {
        if (!first) s += ",";
        first = false;
        s += "\"" + std::to_string(kv.first) + "\":" + std::to_string(kv.second);
    }
    s += "}";
    return s;
}
static std::string quatsToJson(const std::vector<std::array<i64,4>>& q) {
    std::string s = "[";
    for (size_t i = 0; i < q.size(); i++) {
        if (i) s += ",";
        s += "[" + std::to_string(q[i][0]) + "," + std::to_string(q[i][1]) + ","
                 + std::to_string(q[i][2]) + "," + std::to_string(q[i][3]) + "]";
    }
    s += "]";
    return s;
}
static void printResult(bool hasSeed, long long seed, const std::vector<std::array<i64,4>>& quats,
                         const Result& r, long long us) {
    std::ostringstream o;
    o << "{\"seed\":" << (hasSeed ? std::to_string(seed) : "null")
      << ",\"n\":" << quats.size()
      << ",\"quats\":" << quatsToJson(quats)
      << ",\"bounded\":" << r.total
      << ",\"by_depth\":" << mapToJson(r.by_depth)
      << ",\"per_label\":" << mapToJson(r.per_label)
      << ",\"us\":" << us << "}";
    std::cout << o.str() << "\n";
}

static std::vector<std::array<i64,4>> parseQuats(const std::string& s, int expectN = -1) {
    std::vector<std::string> groups;
    { std::stringstream ss(s); std::string item; while (std::getline(ss, item, ';')) groups.push_back(item); }
    if (groups.empty()) throw std::runtime_error("need at least 1 ';'-separated quaternion group");
    if (expectN > 0 && (int)groups.size() != expectN)
        throw std::runtime_error("--quats has " + std::to_string(groups.size()) +
                                  " groups but --n " + std::to_string(expectN) + " was given");
    std::vector<std::array<i64,4>> out;
    out.reserve(groups.size());
    for (auto& grp : groups) {
        std::vector<i64> vals;
        std::stringstream ss(grp); std::string item;
        while (std::getline(ss, item, ',')) vals.push_back(std::stoll(item));
        if (vals.size() != 4) throw std::runtime_error("need 4 comma-separated components per quaternion");
        out.push_back({vals[0], vals[1], vals[2], vals[3]});
    }
    return out;
}

// n distinct coprime (p,r) pairs for the "rotation about z by (p,r)" trick:
// q=(p,0,0,r) gives cos t=(p^2-r^2)/(p^2+r^2), sin t=2pr/(p^2+r^2), which
// is automatically rational for ANY integer p,r (no Pythagorean triple
// needed -- that phrase in the original CPP_SPEC referred to the fact that
// the construction sidesteps needing one). Distinct ratios p/r => distinct
// twist angles => a generic axial family for any n <= 12.
static const i64 AXIAL_PR[12][2] = {
    {1,0},{5,1},{4,1},{3,1},{5,2},{2,1},{7,1},{7,2},{7,3},{7,4},{7,5},{7,6}
};

static bool selftest() {
    bool allOk = true;
    // G3a: axial-6, integer quaternions (p,0,0,r) about z; expect total=121,
    // depth histogram {1:24,2:24,3:24,4:24,5:24,6:1} (+ implicit 0:1 outside).
    // This is the n=6 REGRESSION check: exact histogram, not just total.
    {
        std::vector<std::array<i64,4>> quats;
        for (int i = 0; i < 6; i++) quats.push_back({AXIAL_PR[i][0], 0, 0, AXIAL_PR[i][1]});
        try {
            Result r = exact_count_config(quats);
            std::map<int,int> expect = {{0,1},{1,24},{2,24},{3,24},{4,24},{5,24},{6,1}};
            bool ok = (r.total == 121) && (r.by_depth == expect);
            std::cerr << "[selftest] axial-6: total=" << r.total
                      << " by_depth=" << mapToJson(r.by_depth)
                      << (ok ? "  PASS" : "  FAIL (expected total=121, by_depth={\"0\":1,\"1\":24,\"2\":24,\"3\":24,\"4\":24,\"5\":24,\"6\":1})")
                      << "\n";
            allOk = allOk && ok;
        } catch (std::exception& e) {
            std::cerr << "[selftest] axial-6: EXCEPTION " << e.what() << "  FAIL\n";
            allOk = false;
        }
    }
    // G3b: axial-n family for n=2..12, proven law total=(2n-1)^2 (cross-
    // section edge lines all tangent to the common incircle => no triple
    // points, so the total is exact regardless of which twist angles are
    // used -- only the total is checked here, not the depth histogram,
    // since no closed-form per-depth formula is recorded for general n).
    for (int n = 2; n <= 12; n++) {
        std::vector<std::array<i64,4>> quats;
        for (int i = 0; i < n; i++) quats.push_back({AXIAL_PR[i][0], 0, 0, AXIAL_PR[i][1]});
        long long expect = (2LL*n - 1) * (2LL*n - 1);
        try {
            Result r = exact_count_config(quats);
            bool ok = (r.total == expect);
            std::cerr << "[selftest] axial-" << n << ": total=" << r.total
                      << (ok ? "  PASS" : ("  FAIL (expected " + std::to_string(expect) + ")"))
                      << "\n";
            allOk = allOk && ok;
        } catch (std::exception& e) {
            std::cerr << "[selftest] axial-" << n << ": EXCEPTION " << e.what() << "  FAIL\n";
            allOk = false;
        }
    }
    return allOk;
}

int main(int argc, char** argv) {
    std::vector<std::string> args(argv+1, argv+argc);

    // --n K: pull out anywhere in argv, default 6. Applies to --seed/--seeds
    // (drives the seed-chain cube count) and as a consistency check for
    // --quats/--quats-stdin (which otherwise infer n from group count).
    int nArg = -1;
    for (size_t i = 0; i < args.size(); i++) {
        if (args[i] == "--n" && i + 1 < args.size()) {
            nArg = std::stoi(args[i+1]);
            args.erase(args.begin()+i, args.begin()+i+2);
            break;
        }
    }
    int n = nArg > 0 ? nArg : 6;
    if (n < 2 || n > 12) {
        std::cerr << "--n must be in 2..12 (overflow budget untested beyond that)\n";
        return 1;
    }

    if (args.empty() || args[0] == "--help" || args[0] == "-h") {
        std::cerr <<
            "cube_regions -- exact bounded-region counter for N congruent concentric cubes\n"
            "usage:\n"
            "  cube_regions --selftest\n"
            "  cube_regions [--n K] --seed S\n"
            "  cube_regions [--n K] --seeds A B\n"
            "  cube_regions --quats 'w,x,y,z;...;w,x,y,z'   (K ';'-separated groups)\n"
            "  cube_regions --quats-stdin      (one config per line, same format as --quats)\n"
            "--n defaults to 6; range 2..12. For --quats/--quats-stdin, K is inferred\n"
            "from the number of groups (pass --n too and it must agree).\n"
            "note: quaternion components must satisfy |component| <= 512 after gcd\n"
            "reduction for the int128 overflow budget in CPP_SPEC.md to hold (n-independent).\n";
        return args.empty() ? 1 : 0;
    }
    if (args[0] == "--selftest") {
        bool ok = selftest();
        std::cerr << (ok ? "[selftest] ALL PASS\n" : "[selftest] FAILED\n");
        return ok ? 0 : 1;
    }
    if (args[0] == "--seed" && args.size() >= 2) {
        i64 s = std::stoll(args[1]);
        auto quats = sim_quats((uint32_t)s, n);
        auto t0 = std::chrono::high_resolution_clock::now();
        try {
            Result r = exact_count_config(quats);
            auto t1 = std::chrono::high_resolution_clock::now();
            long long us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
            printResult(true, s, quats, r, us);
        } catch (std::exception& e) {
            std::cout << "{\"seed\":" << s << ",\"n\":" << n << ",\"error\":\"" << e.what() << "\"}\n";
        }
        return 0;
    }
    if (args[0] == "--seeds" && args.size() >= 3) {
        i64 A = std::stoll(args[1]), B = std::stoll(args[2]);
        for (i64 s = A; s < B; s++) {
            auto quats = sim_quats((uint32_t)s, n);
            auto t0 = std::chrono::high_resolution_clock::now();
            try {
                Result r = exact_count_config(quats);
                auto t1 = std::chrono::high_resolution_clock::now();
                long long us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
                printResult(true, s, quats, r, us);
            } catch (std::exception& e) {
                std::cout << "{\"seed\":" << s << ",\"n\":" << n << ",\"error\":\"" << e.what() << "\"}\n";
            }
        }
        return 0;
    }
    if (args[0] == "--quats" && args.size() >= 2) {
        auto quats = parseQuats(args[1], nArg);
        auto t0 = std::chrono::high_resolution_clock::now();
        try {
            Result r = exact_count_config(quats);
            auto t1 = std::chrono::high_resolution_clock::now();
            long long us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
            printResult(false, 0, quats, r, us);
        } catch (std::exception& e) {
            std::cout << "{\"seed\":null,\"error\":\"" << e.what() << "\"}\n";
        }
        return 0;
    }
    if (args[0] == "--quats-stdin") {
        std::string line;
        while (std::getline(std::cin, line)) {
            if (line.empty()) continue;
            try {
                auto quats = parseQuats(line, nArg);
                auto t0 = std::chrono::high_resolution_clock::now();
                try {
                    Result r = exact_count_config(quats);
                    auto t1 = std::chrono::high_resolution_clock::now();
                    long long us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
                    printResult(false, 0, quats, r, us);
                } catch (std::exception& e) {
                    std::cout << "{\"seed\":null,\"error\":\"" << e.what() << "\"}\n";
                }
            } catch (std::exception& e) {
                std::cout << "{\"seed\":null,\"error\":\"parse: " << e.what() << "\"}\n";
            }
            std::cout.flush();
        }
        return 0;
    }
    std::cerr << "unrecognized arguments; see --help\n";
    return 1;
}
