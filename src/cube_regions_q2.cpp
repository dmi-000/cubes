// cube_regions_q2.cpp -- exact bounded-region counter for compounds of N
// congruent concentric cubes whose ROTATIONS may have coordinates in a
// real quadratic field Q(sqrt d), not just Q. This is cube_regions.cpp
// (DO NOT MODIFY THAT FILE -- it stays the validated pure-integer
// reference) with its scalar type generalised from __int128 to elements
// of Z[sqrt d]. Every algorithmic step -- clip order, cap-face
// construction, phantom-facet union-find merge, the facet-flip real/
// phantom test -- is copied unchanged from cube_regions.cpp; only the
// arithmetic underneath (Plane coefficients, vertex homogeneous coords,
// the side-of-plane sign predicate) is generalised. See CPP_SPEC.md for
// the algorithm's rationale; this header comment covers only what's new.
//
// FIELD ARITHMETIC (Z[sqrt d], d a runtime-fixed nonnegative squarefree
// integer; d=0 is the pure-integer path and must reproduce
// cube_regions.cpp bit-for-bit):
//   element  = p + q*sqrt(d),  p,q in i128
//   add/sub  = componentwise
//   multiply = (p1+q1 rt)(p2+q2 rt) = (p1p2 + d q1q2) + (p1q2+q1p2) rt
//   sign     = see FieldElem::sign() below -- the delicate operation.
//
// OVERFLOW BUDGET (derived, not assumed -- traced through the fixed
// 4-stage multiply chain every plane/vertex/predicate goes through:
// quaternion component -> matrix/plane coefficient (1 field multiply +
// a 4-term sum) -> det3 minor (1 field multiply + a 2-term difference)
// -> det3 result / vertex homogeneous coords (1 field multiply + a
// 3-term sum) -> side-of-plane predicate (1 field multiply + a 4-term
// sum). At each field multiply the p-part grows like P1*P2 + d*Q1*Q2 --
// the "+ d*Q1*Q2" term is the one the plain-integer engine never had to
// budget for.
//
// Let m bound every quaternion component's |p| and |q|. The bound is
// JOINT in (m, d), and it is NOT the flat product m^2*d: worst-case
// bound propagation through the 4 stages above (P,Q per stage; a field
// multiply bounds to (P1*P2+d*Q1*Q2, P1*Q2+Q1*P2); a k-term sum bounds
// to k times the per-term bound) gives, at the true admissible boundary
// (pipeline max stays under 2^112 -- see below), a boundary value of
// m^2*d that is NOT constant: ~9.0e6 at d=1, rising through ~2.54e7 at
// d=29, crossing 2.62e7 (=100*512^2, the OLD rectangle's corner) around
// d=~38, and plateauing at ~2.9-3.0e7 for d gtr 500, then drifting back
// down slightly (~2.88e7 at d=20000). A flat "m^2*d <= 2.62e7" rule is
// therefore UNSAFE (over-permissive by up to ~2%, e.g. it would admit
// m=2289 at d=5 when the true safe limit is m=1855) for d below ~38, and
// needlessly restrictive above ~38. This file therefore does NOT use a
// fixed-exponent guard; validateBudget() computes the true traced bound
// per call (see pipelineBound() below) for the config's actual (m, d).
//
// Two thresholds are enforced, matching the OLD rectangle's margins
// exactly so no safety headroom is lost by widening the admissible
// region:
//   - the i128 CHAIN bound: every intermediate (p,q) anywhere in the
//     matrix/plane/det3/vertex/predicate chain must stay under 2^112 --
//     15 bits of headroom below i128's 2^127 capacity. This reproduces
//     the OLD file's documented number exactly at its own corner
//     (d=100, m=512: traced bound is exactly 112 bits), which is what
//     validates the tracing method used here.
//   - the u256 SIGN bound: FieldElem::sign()'s mixed-sign branch squares
//     its own (largest-in-the-pipeline, i.e. side-of-plane-predicate-
//     stage) operand; p^2 and d*q^2 must stay under 2^231 -- 25 bits of
//     headroom below the 256-bit compare's capacity, matching the OLD
//     file's documented margin.
// Numerically, across the whole admissible (m,d) region (checked from
// d=0 up to the absolute ceiling ~3.03e7, at every d that ceiling's own
// m), the i128 chain bound is ALWAYS the binding constraint -- the u256
// bound has more slack throughout -- but both are still checked, since
// nothing here proves that has to remain true for every input.
//
// At the joint boundary, the smallest possible component (m=1) admits d
// up to 30,319,844; this is the largest d admissible for ANY input,
// since increasing d only ever adds non-negative terms to every stage's
// bound (worst-case propagation is monotonic in d). The task's measured
// small-component/large-d configurations are comfortably inside this
// region with wide margin, e.g. (d=8761, m=36): true ceiling for m=36 is
// d<=23387 (so d=8761 has a lot of room), and for d=8761 the true
// ceiling on m is 58 (so m=36 has room too).
//
// Runtime-enforced (validateBudget(), called before any arithmetic
// runs): 0 <= d (squarefree or 0; a non-squarefree d makes p+q*sqrt(d)
// non-canonical -- e.g. sqrt(4)=2 collapses distinct (p,q) pairs onto
// the same value, silently breaking the vertex/plane-key dedup that
// identity relies on), and the traced joint (m,d) pipeline bound above.
// Exceeding either throws ConfigError before any config is built. Silent
// truncation on overflow is exactly the plausible-wrong-answer failure
// mode CPP_SPEC.md warns about; this is a hard reject, not a clamp.
//
// THE SIGN OPERATION needs MORE than the ~112-bit pipeline budget above,
// because it SQUARES its own operands. sign(p+q*sqrt(d)) is trivial when
// p,q have the same sign (or are zero, matching Q5.sign() in
// cube_compound_exact.py, the reference semantics this ports); when they
// have opposite signs it reduces to comparing p^2 against d*q^2. With
// |p|,|q| up to ~2^112 (the predicate-value bound above) and d up to
// 100 (~2^7), p^2 and d*q^2 are each up to ~2^231 -- nowhere near i128's
// 2^127, but comfortably inside 256 bits (2^231 leaves 25 bits of
// headroom below 2^256). This file implements an exact unsigned 256-bit
// multiply (mulU128, 4x uint64 limbs, built from a 32-bit-limb schoolbook
// multiply so every column's partial-product accumulation is
// unambiguously carry-safe in a uint64 -- no cross-term overflow
// subtlety to get wrong) and an exact 256-bit compare (cmpU256), used
// ONLY inside FieldElem::sign()'s mixed-sign branch. Nothing else in the
// pipeline needs it: every other arithmetic op stays inside the i128
// budget above.
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
using u64 = uint64_t;
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

// --------------------------------------------------------- 256-bit helper
// Unsigned 256-bit value as 4 little-endian uint64 limbs. Used ONLY by
// FieldElem::sign()'s mixed-sign branch (see the file header). Not a
// general bignum type -- just enough (multiply two u128 exactly, compare
// two U256) to make that one comparison exact.
struct U256 { uint64_t w[4]; };

static inline U256 mulU128(u128 a, u128 b) {
    uint32_t A[4], B[4];
    for (int i = 0; i < 4; i++) { A[i] = (uint32_t)(a >> (32*i)); B[i] = (uint32_t)(b >> (32*i)); }
    uint32_t R[8] = {0,0,0,0,0,0,0,0};
    for (int i = 0; i < 4; i++) {
        uint64_t carry = 0;
        for (int j = 0; j < 4; j++) {
            uint64_t cur = (uint64_t)A[i] * B[j] + R[i+j] + carry;
            R[i+j] = (uint32_t)cur;
            carry = cur >> 32;
        }
        int k = i + 4;
        while (carry) {
            uint64_t cur = (uint64_t)R[k] + carry;
            R[k] = (uint32_t)cur;
            carry = cur >> 32;
            k++;
        }
    }
    U256 r;
    for (int i = 0; i < 4; i++) r.w[i] = ((uint64_t)R[2*i+1] << 32) | R[2*i];
    return r;
}
// U256 * small nonnegative scalar (k fits in uint64; used to multiply a
// squared operand by d, which the runtime budget keeps <= 100).
static inline U256 mulU256Small(U256 x, uint64_t k) {
    U256 r{{0,0,0,0}};
    unsigned __int128 carry = 0;
    for (int i = 0; i < 4; i++) {
        unsigned __int128 cur = (unsigned __int128)x.w[i] * k + carry;
        r.w[i] = (uint64_t)cur;
        carry = cur >> 64;
    }
    // carry beyond 4 limbs would mean overflow past 256 bits -- cannot
    // happen inside the documented budget (checked at input time), but
    // fail loudly rather than silently truncate if it ever did.
    if (carry != 0) throw ConfigError("internal: 256-bit overflow in sign() -- input exceeded the documented budget");
    return r;
}
static inline int cmpU256(const U256& a, const U256& b) {
    for (int i = 3; i >= 0; i--) {
        if (a.w[i] != b.w[i]) return a.w[i] < b.w[i] ? -1 : 1;
    }
    return 0;
}

// ------------------------------------------------------------ FieldElem
// An element of Z[sqrt d]: p + q*sqrt(d), d fixed for the whole process
// (set once from --d before any config is built). d=0 makes q always 0
// and every operation below degenerate exactly to plain i128 arithmetic
// -- this is what makes the --d 0 path bit-identical to cube_regions.cpp.
static i64 g_d = 0;

struct FieldElem {
    i128 p = 0, q = 0;
    FieldElem() {}
    FieldElem(i128 p_, i128 q_ = 0) : p(p_), q(q_) {}
};
static inline FieldElem operator+(const FieldElem& a, const FieldElem& b) { return {a.p + b.p, a.q + b.q}; }
static inline FieldElem operator-(const FieldElem& a, const FieldElem& b) { return {a.p - b.p, a.q - b.q}; }
static inline FieldElem operator-(const FieldElem& a) { return {-a.p, -a.q}; }
static inline FieldElem operator*(const FieldElem& a, const FieldElem& b) {
    return { a.p * b.p + (i128)g_d * a.q * b.q, a.p * b.q + a.q * b.p };
}
static inline bool feIsZero(const FieldElem& a) { return a.p == 0 && a.q == 0; }

// sign(p + q*sqrt(d)): mirrors Q5.sign()/Q2.sign() in the Python field
// classes (cube_compound_exact.py, slide3_q2.py, q6_count.py) exactly.
// Same-sign (or zero) cases are immediate. Mixed sign needs
// sign(p^2 - d*q^2) -- see the file header for why that needs 256 bits.
static inline int feSign(const FieldElem& v) {
    i128 p = v.p, q = v.q;
    if (p == 0 && q == 0) return 0;
    if (p >= 0 && q >= 0) return 1;
    if (p <= 0 && q <= 0) return -1;
    // mixed sign, both nonzero: compare p^2 vs d*q^2 exactly in 256 bits.
    u128 ap = (u128)iabs128(p), aq = (u128)iabs128(q);
    U256 p2 = mulU128(ap, ap);
    U256 dq2 = mulU256Small(mulU128(aq, aq), (uint64_t)g_d);
    int c = cmpU256(p2, dq2);   // c = sign(p^2 - d q^2)
    if (c == 0) return 0;       // p^2 == d q^2: exact tie (only possible for d a perfect square, i.e. d=0 or d=1)
    int st = c > 0 ? 1 : -1;
    return p > 0 ? st : -st;
}

// generalized "gcd content" reduction: divide a group of FieldElem's raw
// (p,q) integers by their common integer gcd. This is NOT a field gcd
// (Z[sqrt d] need not be Euclidean) -- it's the same trick as the base
// engine's igcd128 canonicalization of homogeneous coords, just applied
// to all the p's and q's together as one flat list of integers. Dividing
// every component by a common positive integer factor never changes the
// point/plane being represented, in any ring.
static inline i128 gcdOfList(const std::initializer_list<i128>& vals) {
    i128 g = 0;
    for (i128 v : vals) g = igcd128(g, v);
    return g;
}

struct ConfigErrorFwd; // (placeholder to keep diff shape close to base file; unused)

// ------------------------------------------------------------------ Plane
// a*x + b*y + c*z = d.  Planes 0..6n-1 = n cubes x 3 axes x 2 signs
// (pid = k*6 + j*2 + (c==+1?0:1)).  Planes 6n..6n+5 = the 6 fixed box
// planes of [-4,4]^3 (pid = 6n + axis*2 + (sign==+1?0:1)).
struct Plane { FieldElem a, b, c, d; };
static int g_n = 6;         // number of cubes (runtime; default 6)
static int g_npl = 42;      // total plane count = 6*g_n + 6
static std::vector<Plane> planes;
static std::vector<int> owner_cube, owner_axis;   // sized 6*g_n

static inline int boxid(int axis, int sign) { return 6 * g_n + axis * 2 + (sign > 0 ? 0 : 1); }

// -------------------------------------------------------- coincident planes
struct PKey {
    i128 ap, aq, bp, bq, cp, cq, dp, dq;
    bool operator==(const PKey& o) const {
        return ap==o.ap && aq==o.aq && bp==o.bp && bq==o.bq &&
               cp==o.cp && cq==o.cq && dp==o.dp && dq==o.dq;
    }
};
struct PKeyHash {
    size_t operator()(const PKey& k) const {
        size_t h = 1469598103934665603ULL;
        auto mix = [&](i128 v) {
            uint64_t lo = (uint64_t)v, hi = (uint64_t)(v >> 64);
            h ^= (size_t)lo; h *= 1099511628211ULL;
            h ^= (size_t)hi; h *= 1099511628211ULL;
        };
        mix(k.ap); mix(k.aq); mix(k.bp); mix(k.bq);
        mix(k.cp); mix(k.cq); mix(k.dp); mix(k.dq);
        return h;
    }
};
static PKey planeKey(int pid) {
    FieldElem a = planes[pid].a, b = planes[pid].b, c = planes[pid].c, d = planes[pid].d;
    i128 g = gcdOfList({a.p, a.q, b.p, b.q, c.p, c.q, d.p, d.q});
    if (g == 0) g = 1;
    a = FieldElem(a.p/g, a.q/g); b = FieldElem(b.p/g, b.q/g);
    c = FieldElem(c.p/g, c.q/g); d = FieldElem(d.p/g, d.q/g);
    int s = feSign(a); if (s == 0) s = feSign(b); if (s == 0) s = feSign(c);
    if (s < 0) { a = -a; b = -b; c = -c; d = -d; }
    return {a.p,a.q, b.p,b.q, c.p,c.q, d.p,d.q};
}

// ---------------------------------------------------------------- Vertices
// A vertex is the intersection of exactly 3 planes ("its triple"). Its
// homogeneous coordinates (X,Y,Z,W), W>0, are computed once via Cramer's
// rule and cached, keyed by the (sorted) plane triple.
struct VData { FieldElem X, Y, Z, W; int t0, t1, t2; };
static std::vector<VData> verts;
static std::vector<int> triLookup; // size g_npl^3, -1 = uncomputed
static int triLookupNPL = -1;      // NPL the current triLookup buffer was sized for

static inline FieldElem det3(FieldElem a1, FieldElem b1, FieldElem c1,
                              FieldElem a2, FieldElem b2, FieldElem c2,
                              FieldElem a3, FieldElem b3, FieldElem c3) {
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
    FieldElem W = det3(P0.a, P0.b, P0.c, P1.a, P1.b, P1.c, P2.a, P2.b, P2.c);
    FieldElem X = det3(P0.d, P0.b, P0.c, P1.d, P1.b, P1.c, P2.d, P2.b, P2.c);
    FieldElem Y = det3(P0.a, P0.d, P0.c, P1.a, P1.d, P1.c, P2.a, P2.d, P2.c);
    FieldElem Z = det3(P0.a, P0.b, P0.d, P1.a, P1.b, P1.d, P2.a, P2.b, P2.d);
    i128 g = gcdOfList({X.p,X.q, Y.p,Y.q, Z.p,Z.q, W.p,W.q});
    if (g == 0) throw ConfigError("degenerate vertex: all-zero plane triple (non-generic config)");
    X = FieldElem(X.p/g, X.q/g); Y = FieldElem(Y.p/g, Y.q/g);
    Z = FieldElem(Z.p/g, Z.q/g); W = FieldElem(W.p/g, W.q/g);
    int wsign = feSign(W);
    if (wsign < 0) { X = -X; Y = -Y; Z = -Z; W = -W; wsign = -wsign; }
    if (wsign == 0) throw ConfigError("degenerate plane triple: no unique intersection (non-generic config)");
    VData vd{X, Y, Z, W, a, b, c};
    idx = (int)verts.size();
    verts.push_back(vd);
    triLookup[key] = idx;
    return idx;
}

static inline int sidesign(int vidx, int pid) {
    const VData& V = verts[vidx]; const Plane& P = planes[pid];
    FieldElem val = P.a * V.X + P.b * V.Y + P.c * V.Z - P.d * V.W;
    return feSign(val);
}

// -------------------------------------------------------------- Cell/Face
// (unchanged from cube_regions.cpp: this layer works on vertex indices
// and plane ids, not on the numeric type, so nothing here needs to know
// about FieldElem.)
struct Face { int pid; std::vector<int> loop; std::vector<int> edgePlane; };
struct Cell { std::vector<Face> faces; unsigned __int128 mask; };

enum class ClipStatus { ALL_NEG, ALL_POS, SPLIT };
struct ClipOut {
    ClipStatus status;
    bool hasNeg = false, hasPos = false;
    std::vector<Face> neg, pos;
};

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
        std::vector<std::array<int,3>> cap_edges;
        for (auto& f : faces) {
            std::vector<int> out;
            std::vector<int> outSrc;
            std::vector<char> outOrig;
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
            std::unordered_map<int, std::vector<std::pair<int,int>>> nbr;
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

using Quat = std::array<FieldElem,4>;

static Result exact_count_config(const std::vector<Quat>& quats) {
    int n = (int)quats.size();
    g_n = n;
    g_npl = 6 * n + 6;
    planes.assign(g_npl, Plane{FieldElem(0),FieldElem(0),FieldElem(0),FieldElem(0)});
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
            planes[pid] = { FieldElem(axis == 0), FieldElem(axis == 1), FieldElem(axis == 2), FieldElem((i128)sign * 4) };
        }
    }

    for (int k = 0; k < n; k++) {
        FieldElem w = quats[k][0], x = quats[k][1], y = quats[k][2], z = quats[k][3];
        FieldElem nn = w*w + x*x + y*y + z*z;
        if (feIsZero(nn)) throw ConfigError("zero quaternion");
        FieldElem M[3][3];
        FieldElem two(2);
        M[0][0]=w*w+x*x-y*y-z*z; M[0][1]=two*(x*y-w*z); M[0][2]=two*(x*z+w*y);
        M[1][0]=two*(x*y+w*z);   M[1][1]=w*w-x*x+y*y-z*z; M[1][2]=two*(y*z-w*x);
        M[2][0]=two*(x*z-w*y);   M[2][1]=two*(y*z+w*x);   M[2][2]=w*w-x*x-y*y+z*z;
        for (int j = 0; j < 3; j++) {
            FieldElem a = M[0][j], b = M[1][j], c = M[2][j];
            for (int cs = 0; cs < 2; cs++) {
                int csign = cs == 0 ? 1 : -1;
                int pid = k*6 + j*2 + cs;
                planes[pid] = {a, b, c, csign > 0 ? nn : -nn};
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
                nxt.push_back({std::move(cell.faces), cell.mask | ((unsigned __int128)1 << pid)});
                continue;
            }
            if (cr.hasNeg) {
                for (auto& f : cr.neg) if (f.pid == -2) f.pid = pid;
                nxt.push_back({std::move(cr.neg), cell.mask});
            }
            if (cr.hasPos) {
                for (auto& f : cr.pos) if (f.pid == -2) f.pid = pid;
                nxt.push_back({std::move(cr.pos), cell.mask | ((unsigned __int128)1 << pid)});
            }
        }
        cells = std::move(nxt);
    }

    int ncell = (int)cells.size();
    auto slabOk = [&](unsigned __int128 mask, int k, int j) -> bool {
        int posPid = k*6 + j*2 + 0, negPid = k*6 + j*2 + 1;
        bool posBit = (bool)((mask >> posPid) & 1), negBit = (bool)((mask >> negPid) & 1);
        return (!posBit) && negBit;
    };
    auto labelOf = [&](unsigned __int128 mask) -> int {
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
            if (f.pid >= 6 * n) continue;
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
// Bit-exact port of mt_sim.py (see cube_regions.cpp for full rationale).
// Only ever used with --d 0 (rational configs); the resulting integer
// quaternions are embedded as FieldElem(v,0), which is exact for any d.
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

static std::vector<std::array<i64,4>> sim_quats_int(uint32_t seed, int n, int scale = 512) {
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
static std::vector<Quat> sim_quats(uint32_t seed, int n) {
    auto ints = sim_quats_int(seed, n);
    std::vector<Quat> out;
    out.reserve(ints.size());
    for (auto& q : ints) out.push_back({FieldElem(q[0]), FieldElem(q[1]), FieldElem(q[2]), FieldElem(q[3])});
    return out;
}

// ------------------------------------------------------------ budget check
// Runtime-enforced overflow budget -- see the file header derivation.

// Documentary/performance-only ceiling on d: the joint test below never
// admits d beyond ~30,319,844 for ANY component magnitude (m=1 is the
// most permissive case), so nothing past this is ever reachable -- this
// just keeps isSquarefree()'s trial division (and the double-precision
// arithmetic in pipelineBound()) away from absurd inputs before the real
// per-config joint test runs.
static const i64 D_SANITY_CEILING = 50000000;

static bool isSquarefree(i64 d) {
    if (d <= 1) return true;
    for (i64 p = 2; p * p <= d; p++)
        if (d % (p * p) == 0) return false;
    return true;
}

// Worst-case |p|,|q| bound after each pipeline stage (see file header),
// given a bound m on every quaternion component's |p| and |q|, and d.
// Mirrors operator*/operator+ exactly: a field multiply (P1,Q1)x(P2,Q2)
// bounds to (P1*P2+d*Q1*Q2, P1*Q2+Q1*P2); a k-term signed sum bounds to
// k times the per-term bound (worst case: no cancellation). Computed in
// double precision -- see file header for why that is exact enough:
// the margins being enforced (>=15 bits at the i128 stage, >=25 bits at
// the u256 stage) dwarf a double's ~2^-52 relative rounding error, and
// on inputs far outside the budget the doubles overflow to +inf, which
// still correctly fails every "< limit" check in validateBudget() --
// there is no path by which floating-point rounding could admit an
// input that actually overflows the exact i128/u256 arithmetic.
struct PipelineBound { double P1,Q1, P2,Q2, P3,Q3; };
static inline void mulBound(double P1, double Q1, double P2, double Q2, double d,
                             double& Po, double& Qo) {
    Po = P1 * P2 + d * Q1 * Q2;
    Qo = P1 * Q2 + Q1 * P2;
}
static PipelineBound pipelineBound(double m, double d) {
    double P0 = m, Q0 = m;
    double P1, Q1; mulBound(P0, Q0, P0, Q0, d, P1, Q1); P1 *= 4; Q1 *= 4;          // matrix/plane coeff (4-term sum)
    double Pmn, Qmn; mulBound(P1, Q1, P1, Q1, d, Pmn, Qmn); Pmn *= 2; Qmn *= 2;    // det3 2x2 minor (2-term diff)
    double P2v, Q2v; mulBound(P1, Q1, Pmn, Qmn, d, P2v, Q2v); P2v *= 3; Q2v *= 3;  // det3 result / vertex coord (3-term sum)
    double P3, Q3; mulBound(P1, Q1, P2v, Q2v, d, P3, Q3); P3 *= 4; Q3 *= 4;        // side-of-plane predicate (4-term sum)
    return {P1, Q1, P2v, Q2v, P3, Q3};
}

static void validateBudget(const std::vector<Quat>& quats, i64 d) {
    if (d < 0)
        throw ConfigError("--d " + std::to_string(d) + " must be nonnegative");
    if (d > D_SANITY_CEILING)
        throw ConfigError("--d " + std::to_string(d) + " exceeds the sanity ceiling "
                           + std::to_string(D_SANITY_CEILING) + " (no component magnitude "
                           "makes d this large admissible; see file header)");
    if (d != 0 && !isSquarefree(d))
        throw ConfigError("--d " + std::to_string(d) + " is not squarefree (or 0): "
                           "Z[sqrt d] would be non-canonical (e.g. sqrt(4)=2 collapses distinct (p,q) pairs)");

    i128 m128 = 0;
    for (auto& quat : quats) {
        for (auto& c : quat) {
            if (iabs128(c.p) > m128) m128 = iabs128(c.p);
            if (iabs128(c.q) > m128) m128 = iabs128(c.q);
            if (d == 0 && c.q != 0)
                throw ConfigError("internal: nonzero sqrt(d) part with d=0");
        }
    }
    if (m128 == 0)
        throw ConfigError("all quaternion components are zero");

    double m = (double)m128, dd = (double)d;
    PipelineBound b = pipelineBound(m, dd);
    double maxpq = std::max({b.P1, b.Q1, b.P2, b.Q2, b.P3, b.Q3});
    const double i128Limit = std::ldexp(1.0, 112);   // see file header: i128 chain bound
    const double u256Limit = std::ldexp(1.0, 231);   // see file header: u256 sign() bound
    double p2  = b.P3 * b.P3;
    double dq2 = dd * b.Q3 * b.Q3;

    if (!(maxpq < i128Limit) || !(p2 < u256Limit) || !(dq2 < u256Limit)) {
        std::ostringstream msg;
        msg << "quaternion component magnitude " << (long long)m128 << " and d=" << d
            << " exceed the joint overflow budget: the traced arithmetic pipeline needs ~"
            << std::log2(maxpq) << " bits at the i128 chain stage (limit 112) and ~"
            << std::log2(std::max(p2, dq2)) << " bits at sign()'s 256-bit squaring stage "
               "(limit 231) -- see file header for the derivation. This is NOT a fixed "
               "m^2*d rule; reduce the component magnitude or d.";
        throw ConfigError(msg.str());
    }
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
static std::string feToStr(const FieldElem& v) {
    if (v.q == 0) return std::to_string((long long)v.p);
    std::string s = std::to_string((long long)v.p) + "+" + std::to_string((long long)v.q) + "r" + std::to_string(g_d);
    return s;
}
static std::string quatsToJson(const std::vector<Quat>& q) {
    std::string s = "[";
    for (size_t i = 0; i < q.size(); i++) {
        if (i) s += ",";
        s += "[\"" + feToStr(q[i][0]) + "\",\"" + feToStr(q[i][1]) + "\",\""
                   + feToStr(q[i][2]) + "\",\"" + feToStr(q[i][3]) + "\"]";
    }
    s += "]";
    return s;
}
static void printResult(bool hasSeed, long long seed, const std::vector<Quat>& quats,
                         const Result& r, long long us) {
    std::ostringstream o;
    o << "{\"seed\":" << (hasSeed ? std::to_string(seed) : "null")
      << ",\"n\":" << quats.size()
      << ",\"d\":" << g_d
      << ",\"quats\":" << quatsToJson(quats)
      << ",\"bounded\":" << r.total
      << ",\"by_depth\":" << mapToJson(r.by_depth)
      << ",\"per_label\":" << mapToJson(r.per_label)
      << ",\"us\":" << us << "}";
    std::cout << o.str() << "\n";
}

// old integer syntax: 'w,x,y,z;...;w,x,y,z' -- used only for --d 0, byte
// for byte the same parser as cube_regions.cpp (so --d 0 output is
// identical for identical input).
static std::vector<Quat> parseQuatsInt(const std::string& s, int expectN = -1) {
    std::vector<std::string> groups;
    { std::stringstream ss(s); std::string item; while (std::getline(ss, item, ';')) groups.push_back(item); }
    if (groups.empty()) throw std::runtime_error("need at least 1 ';'-separated quaternion group");
    if (expectN > 0 && (int)groups.size() != expectN)
        throw std::runtime_error("--quats has " + std::to_string(groups.size()) +
                                  " groups but --n " + std::to_string(expectN) + " was given");
    std::vector<Quat> out;
    out.reserve(groups.size());
    for (auto& grp : groups) {
        std::vector<i64> vals;
        std::stringstream ss(grp); std::string item;
        while (std::getline(ss, item, ',')) vals.push_back(std::stoll(item));
        if (vals.size() != 4) throw std::runtime_error("need 4 comma-separated components per quaternion");
        out.push_back({FieldElem(vals[0]), FieldElem(vals[1]), FieldElem(vals[2]), FieldElem(vals[3])});
    }
    return out;
}

// field syntax (--d D, D != 0): 'p:q,p:q,p:q,p:q;...;p:q,p:q,p:q,p:q'
// each component is p+q*sqrt(D); a bare integer (no ':') is shorthand
// for q=0.
static FieldElem parseComponent(const std::string& tok) {
    auto colon = tok.find(':');
    if (colon == std::string::npos) return FieldElem(std::stoll(tok));
    i128 p = std::stoll(tok.substr(0, colon));
    i128 q = std::stoll(tok.substr(colon + 1));
    return FieldElem(p, q);
}
static std::vector<Quat> parseQuatsField(const std::string& s, int expectN = -1) {
    std::vector<std::string> groups;
    { std::stringstream ss(s); std::string item; while (std::getline(ss, item, ';')) groups.push_back(item); }
    if (groups.empty()) throw std::runtime_error("need at least 1 ';'-separated quaternion group");
    if (expectN > 0 && (int)groups.size() != expectN)
        throw std::runtime_error("--quats has " + std::to_string(groups.size()) +
                                  " groups but --n " + std::to_string(expectN) + " was given");
    std::vector<Quat> out;
    out.reserve(groups.size());
    for (auto& grp : groups) {
        std::vector<std::string> toks;
        std::stringstream ss(grp); std::string item;
        while (std::getline(ss, item, ',')) toks.push_back(item);
        if (toks.size() != 4) throw std::runtime_error("need 4 comma-separated p:q components per quaternion");
        out.push_back({parseComponent(toks[0]), parseComponent(toks[1]), parseComponent(toks[2]), parseComponent(toks[3])});
    }
    return out;
}
static std::vector<Quat> parseQuatsAuto(const std::string& s, int expectN) {
    return g_d == 0 ? parseQuatsInt(s, expectN) : parseQuatsField(s, expectN);
}

// n distinct coprime (p,r) pairs for the axial family (see
// cube_regions.cpp for the derivation); only used by --selftest, which
// runs at d=0.
static const i64 AXIAL_PR[12][2] = {
    {1,0},{5,1},{4,1},{3,1},{5,2},{2,1},{7,1},{7,2},{7,3},{7,4},{7,5},{7,6}
};

static bool selftest() {
    bool allOk = true;
    g_d = 0;
    {
        std::vector<Quat> quats;
        for (int i = 0; i < 6; i++)
            quats.push_back({FieldElem(AXIAL_PR[i][0]), FieldElem(0), FieldElem(0), FieldElem(AXIAL_PR[i][1])});
        try {
            validateBudget(quats, 0);
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
    for (int n = 2; n <= 12; n++) {
        std::vector<Quat> quats;
        for (int i = 0; i < n; i++)
            quats.push_back({FieldElem(AXIAL_PR[i][0]), FieldElem(0), FieldElem(0), FieldElem(AXIAL_PR[i][1])});
        long long expect = (2LL*n - 1) * (2LL*n - 1);
        try {
            validateBudget(quats, 0);
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

    // --d D: pull out anywhere in argv, default 0 (pure integer path).
    i64 dArg = 0;
    for (size_t i = 0; i < args.size(); i++) {
        if (args[i] == "--d" && i + 1 < args.size()) {
            dArg = std::stoll(args[i+1]);
            args.erase(args.begin()+i, args.begin()+i+2);
            break;
        }
    }
    g_d = dArg;
    if (g_d < 0 || g_d > D_SANITY_CEILING) {
        std::cerr << "--d must be in [0," << D_SANITY_CEILING << "]\n";
        return 1;
    }
    if (g_d != 0 && !isSquarefree(g_d)) {
        std::cerr << "--d " << g_d << " is not squarefree; Z[sqrt d] would be non-canonical\n";
        return 1;
    }
    // NOTE: this is only the cheap sign/squarefree/sanity-ceiling check --
    // the real joint (component-magnitude, d) budget test runs later, in
    // validateBudget(), once the quaternions are known (see file header).

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
            "cube_regions_q2 -- exact bounded-region counter for N congruent concentric\n"
            "cubes, rotations optionally in Z[sqrt d] (d given at runtime).\n"
            "usage:\n"
            "  cube_regions_q2 --selftest\n"
            "  cube_regions_q2 [--n K] --seed S                 (d=0 only)\n"
            "  cube_regions_q2 [--n K] --seeds A B               (d=0 only)\n"
            "  cube_regions_q2 [--d D] --quats '...'   (K ';'-separated groups)\n"
            "  cube_regions_q2 [--d D] --quats-stdin   (one config per line)\n"
            "--d defaults to 0 (pure integer, __int128 -- reproduces cube_regions.cpp\n"
            "exactly); 0 or squarefree only.\n"
            "  --d 0:  --quats 'w,x,y,z;...;w,x,y,z'                (unchanged syntax)\n"
            "  --d D>0: --quats 'p:q,p:q,p:q,p:q;...'  (component = p+q*sqrt(D);\n"
            "           a bare integer with no ':' means q=0)\n"
            "--n defaults to 6; range 2..12. For --quats/--quats-stdin, K is inferred\n"
            "from the number of groups (pass --n too and it must agree).\n"
            "overflow budget (see file header comment for the derivation): JOINT in the\n"
            "  quaternion component magnitude m (=max |p|,|q|) and d, not a fixed\n"
            "  rectangle -- e.g. (d=100,m=512), (d=8761,m=36), (d=1,m=3002) are all\n"
            "  admissible, (d=100,m=534) is not. Checked per config in validateBudget().\n"
            "  Inputs exceeding it are rejected, not silently truncated.\n";
        return args.empty() ? 1 : 0;
    }
    if (args[0] == "--selftest") {
        bool ok = selftest();
        std::cerr << (ok ? "[selftest] ALL PASS\n" : "[selftest] FAILED\n");
        return ok ? 0 : 1;
    }
    if (args[0] == "--seed" && args.size() >= 2) {
        if (g_d != 0) { std::cerr << "--seed is only supported for --d 0\n"; return 1; }
        i64 s = std::stoll(args[1]);
        auto quats = sim_quats((uint32_t)s, n);
        auto t0 = std::chrono::high_resolution_clock::now();
        try {
            validateBudget(quats, g_d);
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
        if (g_d != 0) { std::cerr << "--seeds is only supported for --d 0\n"; return 1; }
        i64 A = std::stoll(args[1]), B = std::stoll(args[2]);
        for (i64 s = A; s < B; s++) {
            auto quats = sim_quats((uint32_t)s, n);
            auto t0 = std::chrono::high_resolution_clock::now();
            try {
                validateBudget(quats, g_d);
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
        auto quats = parseQuatsAuto(args[1], nArg);
        auto t0 = std::chrono::high_resolution_clock::now();
        try {
            validateBudget(quats, g_d);
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
                auto quats = parseQuatsAuto(line, nArg);
                auto t0 = std::chrono::high_resolution_clock::now();
                try {
                    validateBudget(quats, g_d);
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
