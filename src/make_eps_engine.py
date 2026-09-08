#!/usr/bin/env python3
"""Generate cube_regions_eps.cpp from cube_regions_q2.cpp.

WHY A GENERATOR RATHER THAN A HAND-EDITED COPY.  cube_regions.cpp is the
validated pure-integer reference and is marked DO NOT MODIFY; cube_regions_q2.cpp
generalised its scalar from __int128 to Z[sqrt d] while copying every algorithmic
step unchanged.  This does the same thing a second time -- scalar from Z[sqrt d]
to Z[sqrt d][eps]/(eps^9) -- and keeping it as a script means the derivation from
the validated engine is re-runnable and auditable rather than a 1100-line file
someone has to diff by eye.

WHAT THE EPSILON IS FOR.  Every count in this project at a displaced point is
count(base + eps*direction) for some finite eps, and a finite eps is a SAMPLE:
too large and the step leaves the cell being measured (333 of 2196 faces at the
golden 67 disagreed across three fixed step sizes for exactly this reason).
Making eps a positive INFINITESIMAL removes the step size from the question.
Q(sqrt d)(eps), with elements truncated polynomials ordered by the sign of the
lowest-degree nonzero coefficient, is a genuine ordered field -- non-Archimedean,
so 0 < eps < every positive rational -- and every predicate this engine performs
is a sign test, so all of them stay exactly decidable.  The count returned is
then the eps -> 0 limit, by derivation and with no step size anywhere.

WHY DEGREE 8 IS EXACT AND NOT A TRUNCATION.  Trace the pipeline:
    quaternion component          degree <= 1   (base + eps*direction, cleared)
    matrix / plane coefficient    degree <= 2   (product of two quaternion comps)
    det3 2x2 minor                degree <= 4   (product of two plane coeffs)
    det3 result / vertex coord    degree <= 6   (minor * plane coeff)
    side-of-plane predicate       degree <= 8   (plane coeff * vertex coord)
Nothing in the engine multiplies beyond that chain, so at EPSDEG = 8 no product
is ever truncated and "all retained coefficients are zero" means the value is
genuinely zero.  This matters: if truncation could discard a nonzero leading
term, feSign would return 0 for a nonzero quantity and the failure would be a
wrong ANSWER, not a crash.

OVERFLOW BUDGET.  An eps-multiply's degree-k coefficient is a sum of up to
(min(deg_a, deg_b) + 1) coefficient products, so each pipeline stage picks up a
convolution-length factor on top of the term-count factor the base engine already
carries: 2 at the plane stage, then 3 at each of the minor, vertex and predicate
stages.  Those factors compound through the squaring stages to ~2592 = 2^11.3
overall, which costs a factor of ~2592^(1/10) = 2.2 in admissible component
magnitude.  They are inserted into pipelineBound at the exact stages they arise,
so the existing derivation stays valid rather than being replaced by a guess.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'cube_regions_q2.cpp')
DST = os.path.join(HERE, 'cube_regions_eps.cpp')

# ------------------------------------------------------------------ the scalar
OLD_FIELD_START = 'struct FieldElem {\n    i128 p = 0, q = 0;'
NEW_SCALAR = r'''// ---------------------------------------------------- Z[sqrt d][eps] scalar
// EPSDEG is EXACT, not a cutoff: see make_eps_engine.py for the degree trace
// that shows nothing in this engine's multiply chain exceeds degree 8.  If that
// chain ever grows a stage, this must grow with it -- a silently truncated
// leading term makes feSign() answer 0 for a nonzero quantity, which is a wrong
// count rather than a crash.
static const int EPSDEG = 8;

struct Coef {
    i128 p = 0, q = 0;
    Coef() {}
    Coef(i128 p_, i128 q_ = 0) : p(p_), q(q_) {}
};
static inline Coef operator+(const Coef& a, const Coef& b) { return {a.p + b.p, a.q + b.q}; }
static inline Coef operator-(const Coef& a, const Coef& b) { return {a.p - b.p, a.q - b.q}; }
static inline Coef operator-(const Coef& a) { return {-a.p, -a.q}; }
static inline Coef operator*(const Coef& a, const Coef& b) {
    return { a.p * b.p + (i128)g_d * a.q * b.q, a.p * b.q + a.q * b.p };
}
static inline bool coefIsZero(const Coef& a) { return a.p == 0 && a.q == 0; }

// sign(p + q*sqrt(d)) -- unchanged from cube_regions_q2.cpp, including the
// 256-bit squaring for the mixed-sign case.
static inline int coefSign(const Coef& v) {
    i128 p = v.p, q = v.q;
    if (p == 0 && q == 0) return 0;
    if (p >= 0 && q >= 0) return 1;
    if (p <= 0 && q <= 0) return -1;
    u128 ap = (u128)iabs128(p), aq = (u128)iabs128(q);
    U256 p2 = mulU128(ap, ap);
    U256 dq2 = mulU256Small(mulU128(aq, aq), (uint64_t)g_d);
    int c = cmpU256(p2, dq2);
    if (c == 0) return 0;
    int st = c > 0 ? 1 : -1;
    return p > 0 ? st : -st;
}

// An element of Z[sqrt d][eps]/(eps^(EPSDEG+1)).  eps is a POSITIVE
// INFINITESIMAL: smaller than every positive rational, which is what makes the
// ordering below well defined and non-Archimedean.
struct FieldElem {
    Coef c[EPSDEG + 1];
    FieldElem() {}
    FieldElem(i128 p_, i128 q_ = 0) { c[0] = Coef(p_, q_); }
};
static inline FieldElem operator+(const FieldElem& a, const FieldElem& b) {
    FieldElem r; for (int k = 0; k <= EPSDEG; k++) r.c[k] = a.c[k] + b.c[k]; return r;
}
static inline FieldElem operator-(const FieldElem& a, const FieldElem& b) {
    FieldElem r; for (int k = 0; k <= EPSDEG; k++) r.c[k] = a.c[k] - b.c[k]; return r;
}
static inline FieldElem operator-(const FieldElem& a) {
    FieldElem r; for (int k = 0; k <= EPSDEG; k++) r.c[k] = -a.c[k]; return r;
}
static inline FieldElem operator*(const FieldElem& a, const FieldElem& b) {
    FieldElem r;
    for (int i = 0; i <= EPSDEG; i++) {
        if (coefIsZero(a.c[i])) continue;
        for (int j = 0; i + j <= EPSDEG; j++) {
            if (coefIsZero(b.c[j])) continue;
            r.c[i + j] = r.c[i + j] + a.c[i] * b.c[j];
        }
    }
    return r;
}
static inline bool feIsZero(const FieldElem& a) {
    for (int k = 0; k <= EPSDEG; k++) if (!coefIsZero(a.c[k])) return false;
    return true;
}
// THE ORDERING.  eps is a positive infinitesimal, so the lowest-degree nonzero
// coefficient dominates every higher one absolutely -- no magnitude comparison
// between degrees is ever needed, which is why this stays exact.
static inline int feSign(const FieldElem& v) {
    for (int k = 0; k <= EPSDEG; k++) {
        int s = coefSign(v.c[k]);
        if (s != 0) return s;
    }
    return 0;
}
'''

# --------------------------------------------------------------- replacements
REPL = []

# 1. plane key: canonicalise over ALL eps coefficients
REPL.append((
    '''static PKey planeKey(int pid) {
    FieldElem a = planes[pid].a, b = planes[pid].b, c = planes[pid].c, d = planes[pid].d;
    i128 g = gcdOfList({a.p, a.q, b.p, b.q, c.p, c.q, d.p, d.q});
    if (g == 0) g = 1;
    a = FieldElem(a.p/g, a.q/g); b = FieldElem(b.p/g, b.q/g);
    c = FieldElem(c.p/g, c.q/g); d = FieldElem(d.p/g, d.q/g);
    int s = feSign(a); if (s == 0) s = feSign(b); if (s == 0) s = feSign(c);
    if (s < 0) { a = -a; b = -b; c = -c; d = -d; }
    return {a.p,a.q, b.p,b.q, c.p,c.q, d.p,d.q};
}''',
    '''static inline i128 gcdOfElems(const FieldElem* es, int n) {
    i128 g = 0;
    for (int e = 0; e < n; e++)
        for (int k = 0; k <= EPSDEG; k++) {
            g = igcd128(g, es[e].c[k].p);
            g = igcd128(g, es[e].c[k].q);
        }
    return g;
}
static inline void divElem(FieldElem& x, i128 g) {
    for (int k = 0; k <= EPSDEG; k++) { x.c[k].p /= g; x.c[k].q /= g; }
}
static PKey planeKey(int pid) {
    FieldElem e[4] = {planes[pid].a, planes[pid].b, planes[pid].c, planes[pid].d};
    // The content is divided out over every eps coefficient at once: scaling a
    // plane by a positive integer leaves the plane unchanged in any ring, and
    // doing it per-coefficient would NOT -- that would rescale eps degrees
    // relative to each other and change which plane is represented.
    i128 g = gcdOfElems(e, 4);
    if (g == 0) g = 1;
    for (int t = 0; t < 4; t++) divElem(e[t], g);
    int s = feSign(e[0]); if (s == 0) s = feSign(e[1]); if (s == 0) s = feSign(e[2]);
    if (s < 0) for (int t = 0; t < 4; t++) e[t] = -e[t];
    PKey k;
    int i = 0;
    for (int t = 0; t < 4; t++)
        for (int m = 0; m <= EPSDEG; m++) { k.v[i++] = e[t].c[m].p; k.v[i++] = e[t].c[m].q; }
    return k;
}'''))

# 2. PKey itself becomes a flat array over all coefficients
REPL.append((
    '''struct PKey {
    i128 ap, aq, bp, bq, cp, cq, dp, dq;
    bool operator==(const PKey& o) const {
        return ap==o.ap && aq==o.aq && bp==o.bp && bq==o.bq &&
               cp==o.cp && cq==o.cq && dp==o.dp && dq==o.dq;
    }
};''',
    '''struct PKey {
    i128 v[8 * (EPSDEG + 1)];
    PKey() { for (int i = 0; i < 8 * (EPSDEG + 1); i++) v[i] = 0; }
    bool operator==(const PKey& o) const {
        for (int i = 0; i < 8 * (EPSDEG + 1); i++) if (v[i] != o.v[i]) return false;
        return true;
    }
};'''))

REPL.append((
    '''        mix(k.ap); mix(k.aq); mix(k.bp); mix(k.bq);
        mix(k.cp); mix(k.cq); mix(k.dp); mix(k.dq);''',
    '''        for (int i = 0; i < 8 * (EPSDEG + 1); i++) mix(k.v[i]);'''))

# 3. vertex homogeneous coordinate reduction
REPL.append((
    '''    i128 g = gcdOfList({X.p,X.q, Y.p,Y.q, Z.p,Z.q, W.p,W.q});''',
    '''    FieldElem xyzw[4] = {X, Y, Z, W};
    i128 g = gcdOfElems(xyzw, 4);'''))
REPL.append((
    '''    X = FieldElem(X.p/g, X.q/g); Y = FieldElem(Y.p/g, Y.q/g);
    Z = FieldElem(Z.p/g, Z.q/g); W = FieldElem(W.p/g, W.q/g);''',
    '''    divElem(X, g); divElem(Y, g); divElem(Z, g); divElem(W, g);'''))

# 4. budget: measure over every coefficient
REPL.append((
    '''            if (iabs128(c.p) > m128) m128 = iabs128(c.p);
            if (iabs128(c.q) > m128) m128 = iabs128(c.q);
            if (d == 0 && c.q != 0)
                throw ConfigError("internal: nonzero sqrt(d) part with d=0");''',
    '''            for (int k = 0; k <= EPSDEG; k++) {
                if (iabs128(c.c[k].p) > m128) m128 = iabs128(c.c[k].p);
                if (iabs128(c.c[k].q) > m128) m128 = iabs128(c.c[k].q);
                if (d == 0 && c.c[k].q != 0)
                    throw ConfigError("internal: nonzero sqrt(d) part with d=0");
            }
            // Degree above 1 in the INPUT would break the degree trace that
            // makes EPSDEG = 8 exact, so it is refused rather than truncated.
            for (int k = 2; k <= EPSDEG; k++)
                if (!coefIsZero(c.c[k]))
                    throw ConfigError("quaternion components must be degree <= 1 in eps "
                                      "(base + eps*direction); higher input degrees would "
                                      "overflow the degree-8 pipeline trace");'''))

# 5. pipeline bound: convolution-length factors at the stages they arise
REPL.append((
    '''    double P1, Q1; mulBound(P0, Q0, P0, Q0, d, P1, Q1); P1 *= 4; Q1 *= 4;          // matrix/plane coeff (4-term sum)
    double Pmn, Qmn; mulBound(P1, Q1, P1, Q1, d, Pmn, Qmn); Pmn *= 2; Qmn *= 2;    // det3 2x2 minor (2-term diff)
    double P2v, Q2v; mulBound(P1, Q1, Pmn, Qmn, d, P2v, Q2v); P2v *= 3; Q2v *= 3;  // det3 result / vertex coord (3-term sum)
    double P3, Q3; mulBound(P1, Q1, P2v, Q2v, d, P3, Q3); P3 *= 4; Q3 *= 4;        // side-of-plane predicate (4-term sum)''',
    '''    // The extra factor at each stage is the EPS CONVOLUTION LENGTH -- the number
    // of coefficient products summed into one output coefficient -- on top of the
    // base engine's term-count factor.  Inputs are degree <= 1, so: plane = 2,
    // and every later stage <= 3.  See make_eps_engine.py for the compounding.
    double P1, Q1; mulBound(P0, Q0, P0, Q0, d, P1, Q1); P1 *= 4*2; Q1 *= 4*2;      // matrix/plane coeff
    double Pmn, Qmn; mulBound(P1, Q1, P1, Q1, d, Pmn, Qmn); Pmn *= 2*3; Qmn *= 2*3;// det3 2x2 minor
    double P2v, Q2v; mulBound(P1, Q1, Pmn, Qmn, d, P2v, Q2v); P2v *= 3*3; Q2v *= 3*3;// det3 result / vertex coord
    double P3, Q3; mulBound(P1, Q1, P2v, Q2v, d, P3, Q3); P3 *= 4*3; Q3 *= 4*3;    // side-of-plane predicate'''))

# 6. printing
REPL.append((
    '''static std::string feToStr(const FieldElem& v) {
    if (v.q == 0) return std::to_string((long long)v.p);
    std::string s = std::to_string((long long)v.p) + "+" + std::to_string((long long)v.q) + "r" + std::to_string(g_d);
    return s;
}''',
    '''static std::string coefToStr(const Coef& v) {
    if (v.q == 0) return std::to_string((long long)v.p);
    return std::to_string((long long)v.p) + "+" + std::to_string((long long)v.q) + "r" + std::to_string(g_d);
}
static std::string feToStr(const FieldElem& v) {
    std::string s;
    int hi = 0;
    for (int k = 0; k <= EPSDEG; k++) if (!coefIsZero(v.c[k])) hi = k;
    for (int k = 0; k <= hi; k++) {
        if (k) s += "|";
        s += coefToStr(v.c[k]);
    }
    return s.empty() ? "0" : s;
}'''))

# 7. parsing: "p:q|p:q" = coefficient of eps^0, eps^1, ...
REPL.append((
    '''static FieldElem parseComponent(const std::string& tok) {
    auto colon = tok.find(':');
    if (colon == std::string::npos) return FieldElem(std::stoll(tok));
    i128 p = std::stoll(tok.substr(0, colon));
    i128 q = std::stoll(tok.substr(colon + 1));
    return FieldElem(p, q);
}''',
    '''// component syntax: eps powers separated by '|', each "p:q" in Z[sqrt d]
// (a bare integer means q = 0).  "3:1|0:-2" is (3 + sqrt d) + eps*(-2 sqrt d).
static FieldElem parseComponent(const std::string& tok) {
    FieldElem out;
    std::vector<std::string> parts;
    { std::stringstream ss(tok); std::string it; while (std::getline(ss, it, '|')) parts.push_back(it); }
    if ((int)parts.size() > EPSDEG + 1)
        throw std::runtime_error("component has more than EPSDEG+1 eps coefficients");
    for (size_t k = 0; k < parts.size(); k++) {
        const std::string& t = parts[k];
        auto colon = t.find(':');
        if (colon == std::string::npos) out.c[k] = Coef((i128)std::stoll(t));
        else out.c[k] = Coef((i128)std::stoll(t.substr(0, colon)),
                             (i128)std::stoll(t.substr(colon + 1)));
    }
    return out;
}'''))

# 8. always use the field parser: eps is available at d = 0 too
REPL.append((
    '''    return g_d == 0 ? parseQuatsInt(s, expectN) : parseQuatsField(s, expectN);''',
    '''    // Unlike cube_regions_q2, the field parser is used at d = 0 as well: eps is
    // orthogonal to sqrt(d), and the whole point of this engine is to displace a
    // RATIONAL configuration infinitesimally too.  It accepts the plain integer
    // syntax unchanged, so d = 0 inputs written for the base engine still parse.
    (void)parseQuatsInt;
    return parseQuatsField(s, expectN);'''))

REPL.append(('cube_regions_q2 --', 'cube_regions_eps --'))
REPL.append(('cube_regions_q2 [--d D]', 'cube_regions_eps [--d D]'))


def main():
    src = open(SRC).read()
    banner = '// ' + __doc__.replace('\n', '\n// ') + '\n\n'
    i = src.index(OLD_FIELD_START)
    j = src.index('static inline i128 gcdOfList')
    out = src[:i] + NEW_SCALAR + '\n' + src[j:]
    applied, missing = 0, []
    for old, new in REPL:
        if old not in out:
            missing.append(old.splitlines()[0][:70])
            continue
        out = out.replace(old, new)
        applied += 1
    out = banner + out
    if missing:
        print('MISSING %d anchors -- generation ABORTED, nothing written:' % len(missing))
        for m in missing:
            print('   ', m)
        return 1
    open(DST, 'w').write(out)
    print('wrote %s (%d replacements applied)' % (DST, applied))
    return 0


if __name__ == '__main__':
    sys.exit(main())
