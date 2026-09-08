// cube_regions_q2w.cpp -- WIDE_ENGINE_SPEC.md's 256-bit ZZ[sqrt d] engine.
// This is cube_regions_q2.cpp (VALIDATED, DO NOT MODIFY THAT FILE) with its
// scalar generalised from __int128 to a from-scratch signed 256-bit type
// (i256), and the sign predicate's mixed-sign branch generalised from a
// 256-bit compare to a 512-bit compare. Every algorithmic step -- clip
// order, cap-face construction, phantom-facet union-find merge, the
// facet-flip real/phantom test, the field-arithmetic algebra, the gcd
// content-reduction trick, the seed chain, the CLI -- is copied unchanged
// from cube_regions_q2.cpp; only the integer type underneath (Plane
// coefficients, vertex homogeneous coordinates, the side-of-plane sign
// predicate, and the retraced overflow budget) is widened. See
// WIDE_ENGINE_SPEC.md for why this file exists and CPP_SPEC.md /
// cube_regions_q2.cpp's own header for the algorithm's rationale; this
// header covers only what's new here.
//
// WHY: cube_regions_q2 rejects any config whose traced pipeline bound
// exceeds 2^112 (its i128 CHAIN threshold). On the mixed edge-plane /
// corner-quadric strata (mixed_q2_full.py), that rejected 284,634 of
// 508,818 candidate n=6 configurations -- not known to be free of a
// record, just uncounted. Raising the scalar width raises the admissible
// (m, d) region and lets more of them be counted.
//
// THE SCALAR TYPE: i256, a signed 256-bit integer as 4 little-endian
// uint64_t limbs in two's complement (see the "i256" block below), with +,
// -, unary -, * (mod 2^256, i.e. ordinary wraparound multiply truncated to
// the low 256 bits -- exact within the budget below; the budget's job, not
// this operator's, is to guarantee that never actually triggers on an
// accepted config), comparison, equality, isZero, sign, and construction
// from int64_t and __int128. Multiplication is schoolbook over 32-bit
// half-limbs so every partial-product accumulation is carry-safe in a
// uint64_t, exactly as cube_regions_q2.cpp's mulU128 already does for its
// 256-bit path -- just truncated to the low 8 half-limb positions here,
// since this is a MOD-2^256 multiply, not a widening one.
// FieldElem becomes a pair of i256 instead of a pair of i128. Everything
// else in the pipeline (planes, det3 minors, vertices, the side-of-plane
// predicate, the gcd content-reduction trick) keeps its structure
// unchanged; a fresh igcd256/idiv256_exact pair (Euclidean gcd + exact
// unsigned long division, both from scratch -- __int128's built-in / and %
// don't exist at 256 bits) plays the role cube_regions_q2.cpp's igcd128
// played, since the content-reduction step still needs to divide by a
// common gcd and that gcd can now legitimately exceed i128's capacity.
//
// THE BUDGET, RETRACED (WIDE_ENGINE_SPEC.md section 2): pipelineBound()'s
// tracing below is REUSED VERBATIM from cube_regions_q2.cpp -- same 4-stage
// chain (quaternion component -> matrix/plane coefficient -> det3 minor ->
// det3 result/vertex homogeneous coords -> side-of-plane predicate), same
// worst-case propagation, same joint-in-(m,d) non-flat-rectangle shape (see
// cube_regions_q2.cpp's header for the full derivation of why m^2*d is NOT
// the right invariant). Only the two threshold CONSTANTS in validateBudget()
// change, keeping the same style of headroom the spec specifies:
//   - CHAIN: every intermediate (p,q) anywhere in the matrix/plane/det3/
//     vertex/predicate chain must stay under 2^240 -- 16 bits of headroom
//     below i256's 2^256 capacity.
//   - SIGN: FieldElem::sign()'s mixed-sign branch squares its own
//     (largest-in-the-pipeline) operand; p^2 and d*q^2 must stay under
//     2^496 -- 16 bits of headroom below the 512-bit compare's 2^512
//     capacity.
// Numerically (verified independently in Python against this exact
// double-precision formula before writing this file, and cross-checked
// against every number cube_regions_q2.cpp's own header documents for its
// OLD thresholds, which reproduced exactly: max d at m=1 = 30,319,844; max
// m at d=8761 = 58; max d at m=36 = 23,387 -- see WIDE_ENGINE_SPEC.md gate
// report for the full cross-check): at the NEW thresholds, the smallest
// possible component (m=1) admits d up to 130,222,772,695,952,968 (the
// largest SQUAREFREE d admissible at m=1 -- see validateBudget()'s own
// squarefree requirement below -- is 130,222,772,695,952,967); at d=5,13,
// 62,1177,8761 the largest admissible m is 121,598,996 / 85,334,348 /
// 43,675,224 / 10,487,602 / 3,853,837 respectively. As with the OLD
// engine, the i256 chain bound is the binding constraint throughout the
// admissible region checked; the u512 sign bound has more slack, but both
// are still enforced, since nothing proves that has to stay true for
// every input.
//
// D_SANITY_CEILING is retraced too, in the same spirit as
// cube_regions_q2.cpp's own D_SANITY_CEILING (a pre-filter, not the real
// per-config test, whose only job is keeping isSquarefree()'s trial
// division and pipelineBound()'s double arithmetic away from absurd inputs
// before the real joint test runs): the OLD file set its ceiling
// (50,000,000) at ~1.65x its true reachable max-d-at-m=1 (30,319,844).
// Applying the same margin to this file's true reachable ceiling
// (~1.302e17) gives ~2.15e17, so D_SANITY_CEILING here is
// 215,000,000,000,000,000 -- comfortably above the true ceiling (so it
// never wrongly pre-rejects an admissible config, which would silently
// undo the whole point of widening) while still keeping isSquarefree()'s
// O(sqrt d) trial division bounded for any d the real joint test could
// ever admit.
//
// THE SIGN PREDICATE (WIDE_ENGINE_SPEC.md section 3): FieldElem::sign()
// keeps its same-sign/zero fast paths verbatim (see cube_regions_q2.cpp's
// header for why the mixed-sign case needs more than the pipeline's own
// budget -- it SQUARES its own operands). The mixed-sign branch now needs
// an EXACT 512-bit unsigned compare of p^2 against d*q^2 with |p|,|q| up to
// ~2^240. mulU256 (4 limbs x 4 limbs -> 8 limbs, unsigned, exact, no
// truncation) and cmpU512 are implemented in the same carry-safe
// 32-bit-half-limb schoolbook style as cube_regions_q2.cpp's mulU128/
// cmpU256, and used ONLY inside sign()'s mixed-sign branch -- nowhere else
// in the pipeline needs a value wider than i256's own (truncating) multiply
// produces. Per WIDE_ENGINE_SPEC.md's own note: a cheaper sign test (e.g.
// continued-fraction convergents of sqrt d) would NOT widen the admissible
// region, because the CHAIN bound is always the binding constraint, not the
// SIGN bound -- so this file does not attempt one; it just widens both
// thresholds together, matching cube_regions_q2.cpp's own choice to check
// both even though only one currently binds.
//
// A non-squarefree d is rejected outright, same reasoning as
// cube_regions_q2.cpp: it makes p+q*sqrt(d) non-canonical (e.g. sqrt(4)=2
// collapses distinct (p,q) pairs onto the same value), silently breaking
// the vertex/plane-key dedup the whole exact-identity approach relies on.
// validateBudget() throws (ConfigError) before any arithmetic runs on an
// out-of-budget or non-squarefree input -- a hard reject, not a clamp:
// silent truncation on overflow is exactly the plausible-wrong-answer
// failure mode this whole project (and WIDE_ENGINE_SPEC.md explicitly)
// guards against.
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
#include <random>

using i64 = int64_t;
using u64 = uint64_t;
using i128 = __int128;
using u128 = unsigned __int128;

// ------------------------------------------------------------- i128 utils
// (unchanged from cube_regions_q2.cpp: still used by the seed chain / CLI
// parsing, which never sees values outside i128 range -- only FieldElem's
// OWN arithmetic is widened.)
static inline i128 iabs128(i128 x) { return x < 0 ? -x : x; }
static inline i64 igcd64(i64 a, i64 b) {
    a = a < 0 ? -a : a; b = b < 0 ? -b : b;
    while (b) { i64 t = a % b; a = b; b = t; }
    return a;
}

struct ConfigError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

// ------------------------------------------------------------------ i256
// Signed 256-bit integer, two's complement, 4 little-endian uint64_t limbs.
// See file header for the operations this supports and why.
struct i256 {
    uint64_t w[4];
    i256() : w{0,0,0,0} {}
    i256(int64_t v) {
        uint64_t sx = (v < 0) ? ~0ULL : 0ULL;
        w[0] = (uint64_t)v; w[1] = sx; w[2] = sx; w[3] = sx;
    }
    i256(__int128 v) {
        unsigned __int128 uv = (unsigned __int128)v;
        w[0] = (uint64_t)uv;
        w[1] = (uint64_t)(uv >> 64);
        uint64_t sx = (v < 0) ? ~0ULL : 0ULL;
        w[2] = sx; w[3] = sx;
    }
};

static inline bool i256IsNeg(const i256& a) { return (a.w[3] >> 63) & 1u; }
static inline bool i256IsZero(const i256& a) {
    return a.w[0]==0 && a.w[1]==0 && a.w[2]==0 && a.w[3]==0;
}
static inline int i256Sign(const i256& a) {
    if (i256IsZero(a)) return 0;
    return i256IsNeg(a) ? -1 : 1;
}

static inline i256 operator+(const i256& a, const i256& b) {
    i256 r; unsigned __int128 carry = 0;
    for (int i = 0; i < 4; i++) {
        unsigned __int128 s = (unsigned __int128)a.w[i] + b.w[i] + carry;
        r.w[i] = (uint64_t)s;
        carry = s >> 64;
    }
    return r;
}
static inline i256 operator-(const i256& a) {
    i256 r; unsigned __int128 carry = 1;
    for (int i = 0; i < 4; i++) {
        unsigned __int128 s = (unsigned __int128)(uint64_t)(~a.w[i]) + carry;
        r.w[i] = (uint64_t)s;
        carry = s >> 64;
    }
    return r;
}
static inline i256 operator-(const i256& a, const i256& b) { return a + (-b); }

// i256's OWN multiply: mod 2^256 (truncating), schoolbook over 32-bit
// half-limbs so every partial-product column accumulates in a carry-safe
// uint64_t -- see file header. This is the multiply used throughout the
// whole geometry pipeline (FieldElem::operator*). It is deliberately NOT
// the same routine as mulU256 below (which produces the full untruncated
// 512-bit product and is used only inside FieldElem::sign()'s mixed-sign
// branch, per WIDE_ENGINE_SPEC.md section 3).
static inline i256 operator*(const i256& a, const i256& b) {
    uint32_t A[8], B[8];
    for (int i = 0; i < 4; i++) {
        A[2*i]   = (uint32_t)a.w[i];       A[2*i+1] = (uint32_t)(a.w[i] >> 32);
        B[2*i]   = (uint32_t)b.w[i];       B[2*i+1] = (uint32_t)(b.w[i] >> 32);
    }
    uint32_t R[8] = {0,0,0,0,0,0,0,0};
    for (int i = 0; i < 8; i++) {
        if (A[i] == 0) continue;
        uint64_t carry = 0;
        for (int j = 0; j + i < 8; j++) {
            uint64_t cur = (uint64_t)A[i] * B[j] + R[i+j] + carry;
            R[i+j] = (uint32_t)cur;
            carry = cur >> 32;
        }
        // any carry beyond half-limb position 7 is >= 2^256 -- discarded,
        // per "mod 2^256" (file header). Within the enforced budget this
        // never actually happens on an accepted config; validateBudget()
        // is the hard reject, not this operator.
    }
    i256 r;
    for (int i = 0; i < 4; i++) r.w[i] = ((uint64_t)R[2*i+1] << 32) | R[2*i];
    return r;
}

static inline bool operator==(const i256& a, const i256& b) {
    return a.w[0]==b.w[0] && a.w[1]==b.w[1] && a.w[2]==b.w[2] && a.w[3]==b.w[3];
}
static inline bool operator!=(const i256& a, const i256& b) { return !(a == b); }
static inline int i256Cmp(const i256& a, const i256& b) {
    bool an = i256IsNeg(a), bn = i256IsNeg(b);
    if (an != bn) return an ? -1 : 1;
    for (int i = 3; i >= 0; i--)
        if (a.w[i] != b.w[i]) return a.w[i] < b.w[i] ? -1 : 1;
    return 0;
}
static inline bool operator<(const i256& a, const i256& b)  { return i256Cmp(a,b) < 0; }
static inline bool operator<=(const i256& a, const i256& b) { return i256Cmp(a,b) <= 0; }
static inline bool operator>(const i256& a, const i256& b)  { return i256Cmp(a,b) > 0; }
static inline bool operator>=(const i256& a, const i256& b) { return i256Cmp(a,b) >= 0; }

static inline i256 iabs256(const i256& a) { return i256IsNeg(a) ? -a : a; }

// i256 -> __int128, valid ONLY when the true value fits in 128 bits (the
// caller's responsibility). Used only by the G4 arithmetic selftest, where
// operands are kept below 2^60 specifically so every result fits.
static inline i128 i256ToI128(const i256& x) {
    return ((i128)(int64_t)x.w[1] << 64) | (u128)x.w[0];
}

// ------------------------------------------------ i256 division and gcd
// __int128 has built-in / and % for cube_regions_q2.cpp's igcd128; i256
// does not, so the content-reduction trick (divide a group of FieldElem's
// raw (p,q) integers by their common integer gcd -- see gcdOfList below)
// needs a from-scratch unsigned long division. Schoolbook bit-at-a-time
// long division, 256 iterations, restoring: exact and simple to verify by
// inspection, which matters more here than speed (this runs once per
// unique plane/vertex, not per clip test). Both operands must be
// nonnegative magnitudes under 2^255 (the sign bit clear) -- guaranteed
// here because everything flowing through it is already inside the
// enforced budget (< 2^240), far below that.
static void udivmod256(const i256& a, const i256& b, i256& qOut, i256& rOut) {
    i256 quotient, remainder; // both zero-initialised
    for (int bit = 255; bit >= 0; bit--) {
        uint64_t carry = 0;
        for (int i = 0; i < 4; i++) {
            uint64_t nc = remainder.w[i] >> 63;
            remainder.w[i] = (remainder.w[i] << 1) | carry;
            carry = nc;
        }
        int limb = bit / 64, off = bit % 64;
        remainder.w[0] |= (a.w[limb] >> off) & 1ULL;
        if (!(remainder < b)) {
            remainder = remainder - b;
            quotient.w[bit/64] |= (1ULL << (bit%64));
        }
    }
    qOut = quotient; rOut = remainder;
}
static inline i256 imod256(const i256& a, const i256& b) {
    i256 q, r; udivmod256(iabs256(a), iabs256(b), q, r); return r;
}
// exact division (b divides a exactly -- true of every call site below,
// which only ever divides by a gcd of the very values being divided).
static inline i256 idiv256_exact(const i256& a, const i256& b) {
    bool neg = (i256IsNeg(a) != i256IsNeg(b));
    i256 q, r; udivmod256(iabs256(a), iabs256(b), q, r);
    return neg ? -q : q;
}
static inline i256 igcd256(i256 a, i256 b) {
    a = iabs256(a); b = iabs256(b);
    while (!i256IsZero(b)) {
        i256 t = imod256(a, b);
        a = b; b = t;
    }
    return a;
}

// i256 -> double, for pipelineBound()'s double-precision tracing (see file
// header for why double precision is exact enough there). Correct for any
// magnitude i256 can hold; in practice only ever called on the small
// (CLI-input-range) component-magnitude bound m.
static inline double i256ToDouble(const i256& x) {
    bool neg = i256IsNeg(x);
    i256 ax = neg ? -x : x;
    double v = 0.0;
    for (int i = 3; i >= 0; i--) v = v * 18446744073709551616.0 /* 2^64 */ + (double)ax.w[i];
    return neg ? -v : v;
}

// i256 -> decimal string, exact (repeated division by 10^18 using
// udivmod256 above). Used only for printing input-echo quaternion
// components and budget-violation messages -- never a hot path, and never
// lossy, unlike a naive truncating cast would be.
static std::string i256ToStr(const i256& v) {
    if (i256IsZero(v)) return "0";
    bool neg = i256IsNeg(v);
    i256 x = neg ? -v : v;
    i256 base = i256((i128)1000000000000000000LL); // 10^18
    std::string digits;
    while (!i256IsZero(x)) {
        i256 q, r;
        udivmod256(x, base, q, r);
        uint64_t chunk = r.w[0]; // r < 10^18 < 2^64
        x = q;
        if (i256IsZero(x)) digits = std::to_string(chunk) + digits;
        else {
            std::string s = std::to_string(chunk);
            digits = std::string(18 - s.size(), '0') + s + digits;
        }
    }
    return (neg ? "-" : "") + digits;
}

// --------------------------------------------------------- 512-bit helper
// Unsigned 512-bit value as 8 little-endian uint64 limbs. Used ONLY by
// FieldElem::sign()'s mixed-sign branch (see file header). Not a general
// bignum type -- just enough (multiply two i256 magnitudes exactly, compare
// two U512) to make that one comparison exact.
struct U512 { uint64_t w[8]; };

// Exact, untruncated 256x256 -> 512-bit unsigned multiply. Same carry-safe
// 32-bit-half-limb schoolbook style as cube_regions_q2.cpp's mulU128 (and
// as i256's own truncating operator* above), just not truncated: every
// half-limb column 0..15 is kept. The caller passes already-nonnegative
// i256 magnitudes (abs values); their w[] arrays are read as raw unsigned
// limbs.
static inline U512 mulU256(const i256& a, const i256& b) {
    uint32_t A[8], B[8];
    for (int i = 0; i < 4; i++) {
        A[2*i]   = (uint32_t)a.w[i];       A[2*i+1] = (uint32_t)(a.w[i] >> 32);
        B[2*i]   = (uint32_t)b.w[i];       B[2*i+1] = (uint32_t)(b.w[i] >> 32);
    }
    uint32_t R[16] = {0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0};
    for (int i = 0; i < 8; i++) {
        uint64_t carry = 0;
        for (int j = 0; j < 8; j++) {
            uint64_t cur = (uint64_t)A[i] * B[j] + R[i+j] + carry;
            R[i+j] = (uint32_t)cur;
            carry = cur >> 32;
        }
        int k = i + 8;
        while (carry) {
            uint64_t cur = (uint64_t)R[k] + carry;
            R[k] = (uint32_t)cur;
            carry = cur >> 32;
            k++;
        }
    }
    U512 r;
    for (int i = 0; i < 8; i++) r.w[i] = ((uint64_t)R[2*i+1] << 32) | R[2*i];
    return r;
}
// U512 * small nonnegative scalar (d fits in a uint64 -- the runtime budget
// keeps it far smaller). Mirrors cube_regions_q2.cpp's mulU256Small
// exactly, just at double the width.
static inline U512 mulU512Small(const U512& x, uint64_t k) {
    U512 r{{0,0,0,0,0,0,0,0}};
    unsigned __int128 carry = 0;
    for (int i = 0; i < 8; i++) {
        unsigned __int128 cur = (unsigned __int128)x.w[i] * k + carry;
        r.w[i] = (uint64_t)cur;
        carry = cur >> 64;
    }
    if (carry != 0) throw ConfigError("internal: 512-bit overflow in sign() -- input exceeded the documented budget");
    return r;
}
static inline int cmpU512(const U512& a, const U512& b) {
    for (int i = 7; i >= 0; i--)
        if (a.w[i] != b.w[i]) return a.w[i] < b.w[i] ? -1 : 1;
    return 0;
}

// ------------------------------------------------------------ FieldElem
// An element of Z[sqrt d]: p + q*sqrt(d), d fixed for the whole process
// (set once from --d before any config is built). d=0 makes q always 0 and
// every operation below degenerate exactly to plain-integer arithmetic --
// this is what makes the --d 0 path reproduce cube_regions_q2's --d 0 path
// (and hence cube_regions.cpp) exactly.
static i64 g_d = 0;

struct FieldElem {
    i256 p, q;
    FieldElem() {}
    // scalar-construction path: mirrors cube_regions_q2.cpp's
    // FieldElem(i128 p_, i128 q_=0) exactly, so every existing call site in
    // the geometry pipeline below (FieldElem(axis==0), FieldElem(2),
    // FieldElem((i128)sign*4), FieldElem(q[0]), ...) keeps working
    // unchanged -- only ONE user-defined conversion (the argument's own
    // standard conversion to i128, then this ctor) is ever needed, so
    // overload resolution always prefers this over the i256-pair ctor
    // below for any fundamental-type argument.
    FieldElem(i128 p_, i128 q_ = 0) : p(i256(p_)), q(i256(q_)) {}
    // internal path: used by operator+/-/* below (which already hold
    // i256 p,q) and by the gcd-reduction call sites (idiv256_exact
    // results are i256).
    FieldElem(i256 p_, i256 q_ = i256((i128)0)) : p(p_), q(q_) {}
};
static inline FieldElem operator+(const FieldElem& a, const FieldElem& b) { return {a.p + b.p, a.q + b.q}; }
static inline FieldElem operator-(const FieldElem& a, const FieldElem& b) { return {a.p - b.p, a.q - b.q}; }
static inline FieldElem operator-(const FieldElem& a) { return {-a.p, -a.q}; }
static inline FieldElem operator*(const FieldElem& a, const FieldElem& b) {
    return { a.p * b.p + i256(g_d) * a.q * b.q, a.p * b.q + a.q * b.p };
}
static inline bool feIsZero(const FieldElem& a) { return i256IsZero(a.p) && i256IsZero(a.q); }

// sign(p + q*sqrt(d)): mirrors Q5.sign()/Q2.sign() in the Python field
// classes exactly, ported unchanged from cube_regions_q2.cpp's feSign.
// Same-sign (or zero) cases are immediate. Mixed sign needs
// sign(p^2 - d*q^2) -- see the file header for why that needs 512 bits
// here (vs. 256 in cube_regions_q2.cpp).
static inline int feSign(const FieldElem& v) {
    int sp = i256Sign(v.p), sq = i256Sign(v.q);
    if (sp == 0 && sq == 0) return 0;
    if (sp >= 0 && sq >= 0) return 1;
    if (sp <= 0 && sq <= 0) return -1;
    // mixed sign, both nonzero: compare p^2 vs d*q^2 exactly in 512 bits.
    i256 ap = iabs256(v.p), aq = iabs256(v.q);
    U512 p2 = mulU256(ap, ap);
    U512 dq2 = mulU512Small(mulU256(aq, aq), (uint64_t)g_d);
    int c = cmpU512(p2, dq2);   // c = sign(p^2 - d q^2)
    if (c == 0) return 0;       // exact tie (only possible for d a perfect square, i.e. d=0 or d=1)
    int st = c > 0 ? 1 : -1;
    return sp > 0 ? st : -st;
}

// generalized "gcd content" reduction: divide a group of FieldElem's raw
// (p,q) integers by their common integer gcd. Same trick as
// cube_regions_q2.cpp's gcdOfList/igcd128, just at 256 bits via igcd256
// (see above for why __int128's built-in % can't be reused here).
static inline i256 gcdOfList(const std::initializer_list<i256>& vals) {
    i256 g = i256((i128)0);
    for (const i256& v : vals) g = igcd256(g, v);
    return g;
}

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
    i256 ap, aq, bp, bq, cp, cq, dp, dq;
    bool operator==(const PKey& o) const {
        return ap==o.ap && aq==o.aq && bp==o.bp && bq==o.bq &&
               cp==o.cp && cq==o.cq && dp==o.dp && dq==o.dq;
    }
};
struct PKeyHash {
    size_t operator()(const PKey& k) const {
        size_t h = 1469598103934665603ULL;
        auto mix = [&](const i256& v) {
            for (int i = 0; i < 4; i++) { h ^= (size_t)v.w[i]; h *= 1099511628211ULL; }
        };
        mix(k.ap); mix(k.aq); mix(k.bp); mix(k.bq);
        mix(k.cp); mix(k.cq); mix(k.dp); mix(k.dq);
        return h;
    }
};
static PKey planeKey(int pid) {
    FieldElem a = planes[pid].a, b = planes[pid].b, c = planes[pid].c, d = planes[pid].d;
    i256 g = gcdOfList({a.p, a.q, b.p, b.q, c.p, c.q, d.p, d.q});
    if (i256IsZero(g)) g = i256((i128)1);
    a = FieldElem(idiv256_exact(a.p,g), idiv256_exact(a.q,g));
    b = FieldElem(idiv256_exact(b.p,g), idiv256_exact(b.q,g));
    c = FieldElem(idiv256_exact(c.p,g), idiv256_exact(c.q,g));
    d = FieldElem(idiv256_exact(d.p,g), idiv256_exact(d.q,g));
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
    i256 g = gcdOfList({X.p,X.q, Y.p,Y.q, Z.p,Z.q, W.p,W.q});
    if (i256IsZero(g)) throw ConfigError("degenerate vertex: all-zero plane triple (non-generic config)");
    X = FieldElem(idiv256_exact(X.p,g), idiv256_exact(X.q,g));
    Y = FieldElem(idiv256_exact(Y.p,g), idiv256_exact(Y.q,g));
    Z = FieldElem(idiv256_exact(Z.p,g), idiv256_exact(Z.q,g));
    W = FieldElem(idiv256_exact(W.p,g), idiv256_exact(W.q,g));
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
// (unchanged from cube_regions_q2.cpp: this layer works on vertex indices
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
// Bit-exact port of mt_sim.py, unchanged from cube_regions_q2.cpp. Only
// ever used with --d 0 (rational configs); the resulting integer
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

// Documentary/performance-only ceiling on d -- see file header for the
// derivation of this number (~1.65x the true reachable ceiling at m=1,
// same margin cube_regions_q2.cpp used for its own D_SANITY_CEILING).
static const i64 D_SANITY_CEILING = 215000000000000000LL;

static bool isSquarefree(i64 d) {
    if (d <= 1) return true;
    for (i64 p = 2; p * p <= d; p++)
        if (d % (p * p) == 0) return false;
    return true;
}

// Worst-case |p|,|q| bound after each pipeline stage -- REUSED VERBATIM
// from cube_regions_q2.cpp (see file header: only the threshold constants
// in validateBudget() below change, not this tracing).
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

    i256 m256 = i256((i128)0);
    for (auto& quat : quats) {
        for (auto& c : quat) {
            i256 acp = iabs256(c.p), acq = iabs256(c.q);
            if (acp > m256) m256 = acp;
            if (acq > m256) m256 = acq;
            if (d == 0 && !i256IsZero(c.q))
                throw ConfigError("internal: nonzero sqrt(d) part with d=0");
        }
    }
    if (i256IsZero(m256))
        throw ConfigError("all quaternion components are zero");

    double m = i256ToDouble(m256), dd = (double)d;
    PipelineBound b = pipelineBound(m, dd);
    double maxpq = std::max({b.P1, b.Q1, b.P2, b.Q2, b.P3, b.Q3});
    const double chainLimit = std::ldexp(1.0, 240);   // CHAIN: i256 bound (see file header)
    const double signLimit  = std::ldexp(1.0, 496);   // SIGN: u512 sign() bound (see file header)
    double p2  = b.P3 * b.P3;
    double dq2 = dd * b.Q3 * b.Q3;

    if (!(maxpq < chainLimit) || !(p2 < signLimit) || !(dq2 < signLimit)) {
        std::ostringstream msg;
        msg << "quaternion component magnitude " << i256ToStr(m256) << " and d=" << d
            << " exceed the joint overflow budget: the traced arithmetic pipeline needs ~"
            << std::log2(maxpq) << " bits at the i256 chain stage (limit 240) and ~"
            << std::log2(std::max(p2, dq2)) << " bits at sign()'s 512-bit squaring stage "
               "(limit 496) -- see file header for the derivation. This is NOT a fixed "
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
    if (i256IsZero(v.q)) return i256ToStr(v.p);
    return i256ToStr(v.p) + "+" + i256ToStr(v.q) + "r" + std::to_string(g_d);
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
// for byte the same parser as cube_regions_q2.cpp (so --d 0 output is
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
// cube_regions_q2.cpp for the derivation); only used by --selftest, which
// runs at d=0.
static const i64 AXIAL_PR[12][2] = {
    {1,0},{5,1},{4,1},{3,1},{5,2},{2,1},{7,1},{7,2},{7,3},{7,4},{7,5},{7,6}
};

// ---------------------------------------------------- G4 arithmetic selftest
// Randomised comparison of i256 +, -, *, and comparison against __int128
// (both exact for operands below 2^60), and of the 512-bit square-compare
// (mulU256+cmpU512) against a __int128-based computation, also for operands
// below 2^60 (so p^2,q^2 < 2^120, comfortably exact in i128's 2^127
// capacity -- the oracle itself never overflows). This validates the
// widened engine's own arithmetic primitives, independently of the
// geometry pipeline that G1-G3 validate against the narrow engine / the
// integer engine. Any disagreement stops the run (of that phase) and
// reports the offending operands.
static bool arithmeticSelftest(long long trials) {
    std::mt19937_64 rng(0xC0FFEE1256ULL);  // fixed seed: reproducible run to run
    const int64_t LIM = ((int64_t)1 << 60) - 1;
    std::uniform_int_distribution<int64_t> dist(-LIM, LIM);
    std::uniform_int_distribution<int64_t> distNonneg(0, LIM);

    bool ok = true;
    for (long long t = 0; t < trials; t++) {
        int64_t a = dist(rng), b = dist(rng);
        i256 A(a), B(b);
        i128 ra = (i128)a, rb = (i128)b;

        i256 sum = A + B;   i128 rsum  = ra + rb;
        i256 diff = A - B;  i128 rdiff = ra - rb;
        i256 negA = -A;     i128 rnegA = -ra;
        i256 prod = A * B;  i128 rprod = ra * rb;   // |a|,|b|<2^60 -> |prod|<2^120, exact in i128

        if (i256ToI128(sum) != rsum) {
            std::cerr << "[selftest] i256 SUM mismatch a=" << a << " b=" << b << "  FAIL\n";
            ok = false; break;
        }
        if (i256ToI128(diff) != rdiff) {
            std::cerr << "[selftest] i256 DIFF mismatch a=" << a << " b=" << b << "  FAIL\n";
            ok = false; break;
        }
        if (i256ToI128(negA) != rnegA) {
            std::cerr << "[selftest] i256 NEG mismatch a=" << a << "  FAIL\n";
            ok = false; break;
        }
        if (i256ToI128(prod) != rprod) {
            std::cerr << "[selftest] i256 PROD mismatch a=" << a << " b=" << b << "  FAIL\n";
            ok = false; break;
        }
        bool cmpLt = (A < B), refLt = (ra < rb);
        bool cmpEq = (A == B), refEq = (ra == rb);
        if (cmpLt != refLt || cmpEq != refEq) {
            std::cerr << "[selftest] i256 COMPARE mismatch a=" << a << " b=" << b << "  FAIL\n";
            ok = false; break;
        }
    }
    if (ok)
        std::cerr << "[selftest] i256 +,-,*,compare: " << trials << " trials vs __int128  PASS\n";

    bool ok2 = true;
    for (long long t = 0; t < trials; t++) {
        int64_t p = distNonneg(rng), q = distNonneg(rng);
        i256 P(p), Q(q);
        U512 sqP = mulU256(P, P);
        U512 sqQ = mulU256(Q, Q);
        int c = cmpU512(sqP, sqQ);
        i128 rp2 = (i128)p * (i128)p, rq2 = (i128)q * (i128)q;  // exact: p,q<2^60 -> squares<2^120
        int rc = (rp2 < rq2) ? -1 : (rp2 > rq2 ? 1 : 0);
        if (c != rc) {
            std::cerr << "[selftest] 512-bit square-compare mismatch p=" << p << " q=" << q << "  FAIL\n";
            ok2 = false; break;
        }
    }
    if (ok2)
        std::cerr << "[selftest] mulU256+cmpU512 square-compare: " << trials << " trials vs __int128  PASS\n";

    return ok && ok2;
}

static bool selftest() {
    bool allOk = true;
    allOk = arithmeticSelftest(100000) && allOk;

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
            "cube_regions_q2w -- exact bounded-region counter for N congruent concentric\n"
            "cubes, rotations optionally in Z[sqrt d] (d given at runtime). Widened\n"
            "(256-bit scalar) sibling of cube_regions_q2 -- see WIDE_ENGINE_SPEC.md.\n"
            "usage:\n"
            "  cube_regions_q2w --selftest\n"
            "  cube_regions_q2w [--n K] --seed S                 (d=0 only)\n"
            "  cube_regions_q2w [--n K] --seeds A B               (d=0 only)\n"
            "  cube_regions_q2w [--d D] --quats '...'   (K ';'-separated groups)\n"
            "  cube_regions_q2w [--d D] --quats-stdin   (one config per line)\n"
            "--d defaults to 0 (pure integer path); 0 or squarefree only.\n"
            "  --d 0:  --quats 'w,x,y,z;...;w,x,y,z'                (unchanged syntax)\n"
            "  --d D>0: --quats 'p:q,p:q,p:q,p:q;...'  (component = p+q*sqrt(D);\n"
            "           a bare integer with no ':' means q=0)\n"
            "--n defaults to 6; range 2..12. For --quats/--quats-stdin, K is inferred\n"
            "from the number of groups (pass --n too and it must agree).\n"
            "overflow budget (see file header for the derivation): JOINT in the\n"
            "  quaternion component magnitude m (=max |p|,|q|) and d, not a fixed\n"
            "  rectangle -- checked per config in validateBudget(). Inputs exceeding it\n"
            "  are rejected, not silently truncated.\n";
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
