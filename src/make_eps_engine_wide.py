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
SRC = os.path.join(HERE, 'cube_regions_q2w.cpp')
DST = os.path.join(HERE, 'cube_regions_epsw.cpp')

# ------------------------------------------------------------------ the scalar
OLD_FIELD_START = 'struct FieldElem {\n    i256 p, q;'
NEW_SCALAR = '// ------------------------------------------- Z[sqrt d][eps] scalar, 256-bit\n// Generated from cube_regions_q2w.cpp. Its VALIDATED 256-bit Z[sqrt d] scalar is\n// reused verbatim as the coefficient type, renamed FieldElem -> Coef (and\n// feSign/feIsZero -> coefSign/coefIsZero); only the eps polynomial layer is new.\n// Retyping the 256-bit arithmetic was the alternative and would have put\n// unvalidated bignum code under a sign predicate.\n//\n// EPSDEG is EXACT, not a cutoff. A silently truncated leading term makes\n// feSign() answer 0 for a nonzero quantity -- a WRONG COUNT, not a crash.\nstatic const int EPSDEG = 8;\n\nstruct Coef {\n    i256 p, q;\n    Coef() {}\n    // scalar-construction path: mirrors cube_regions_q2.cpp\'s\n    // Coef(i128 p_, i128 q_=0) exactly, so every existing call site in\n    // the geometry pipeline below (Coef(axis==0), Coef(2),\n    // Coef((i128)sign*4), Coef(q[0]), ...) keeps working\n    // unchanged -- only ONE user-defined conversion (the argument\'s own\n    // standard conversion to i128, then this ctor) is ever needed, so\n    // overload resolution always prefers this over the i256-pair ctor\n    // below for any fundamental-type argument.\n    Coef(i128 p_, i128 q_ = 0) : p(i256(p_)), q(i256(q_)) {}\n    // internal path: used by operator+/-/* below (which already hold\n    // i256 p,q) and by the gcd-reduction call sites (idiv256_exact\n    // results are i256).\n    Coef(i256 p_, i256 q_ = i256((i128)0)) : p(p_), q(q_) {}\n};\nstatic inline Coef operator+(const Coef& a, const Coef& b) { return {a.p + b.p, a.q + b.q}; }\nstatic inline Coef operator-(const Coef& a, const Coef& b) { return {a.p - b.p, a.q - b.q}; }\nstatic inline Coef operator-(const Coef& a) { return {-a.p, -a.q}; }\nstatic inline Coef operator*(const Coef& a, const Coef& b) {\n    return { a.p * b.p + i256(g_d) * a.q * b.q, a.p * b.q + a.q * b.p };\n}\nstatic inline bool coefIsZero(const Coef& a) { return i256IsZero(a.p) && i256IsZero(a.q); }\n\n// sign(p + q*sqrt(d)): mirrors Q5.sign()/Q2.sign() in the Python field\n// classes exactly, ported unchanged from cube_regions_q2.cpp\'s coefSign.\n// Same-sign (or zero) cases are immediate. Mixed sign needs\n// sign(p^2 - d*q^2) -- see the file header for why that needs 512 bits\n// here (vs. 256 in cube_regions_q2.cpp).\nstatic inline int coefSign(const Coef& v) {\n    int sp = i256Sign(v.p), sq = i256Sign(v.q);\n    if (sp == 0 && sq == 0) return 0;\n    if (sp >= 0 && sq >= 0) return 1;\n    if (sp <= 0 && sq <= 0) return -1;\n    // mixed sign, both nonzero: compare p^2 vs d*q^2 exactly in 512 bits.\n    i256 ap = iabs256(v.p), aq = iabs256(v.q);\n    U512 p2 = mulU256(ap, ap);\n    U512 dq2 = mulU512Small(mulU256(aq, aq), (uint64_t)g_d);\n    int c = cmpU512(p2, dq2);   // c = sign(p^2 - d q^2)\n    if (c == 0) return 0;       // exact tie (only possible for d a perfect square, i.e. d=0 or d=1)\n    int st = c > 0 ? 1 : -1;\n    return sp > 0 ? st : -st;\n}\n\n// generalized "gcd content" reduction: divide a group of Coef\'s raw\n// (p,q) integers by their common integer gcd. Same trick as\n// cube_regions_q2.cpp\'s gcdOfList/igcd128, just at 256 bits via igcd256\n// (see above for why __int128\'s built-in % can\'t be reused here).\n\n// An element of Z[sqrt d][eps]/(eps^(EPSDEG+1)).  eps is a POSITIVE\n// INFINITESIMAL: smaller than every positive rational, which is what makes the\n// ordering below well defined and non-Archimedean.\nstruct FieldElem {\n    Coef c[EPSDEG + 1];\n    FieldElem() {}\n    FieldElem(i128 p_, i128 q_ = 0) { c[0] = Coef(p_, q_); }\n};\nstatic inline FieldElem operator+(const FieldElem& a, const FieldElem& b) {\n    FieldElem r; for (int k = 0; k <= EPSDEG; k++) r.c[k] = a.c[k] + b.c[k]; return r;\n}\nstatic inline FieldElem operator-(const FieldElem& a, const FieldElem& b) {\n    FieldElem r; for (int k = 0; k <= EPSDEG; k++) r.c[k] = a.c[k] - b.c[k]; return r;\n}\nstatic inline FieldElem operator-(const FieldElem& a) {\n    FieldElem r; for (int k = 0; k <= EPSDEG; k++) r.c[k] = -a.c[k]; return r;\n}\nstatic inline FieldElem operator*(const FieldElem& a, const FieldElem& b) {\n    FieldElem r;\n    for (int i = 0; i <= EPSDEG; i++) {\n        if (coefIsZero(a.c[i])) continue;\n        for (int j = 0; i + j <= EPSDEG; j++) {\n            if (coefIsZero(b.c[j])) continue;\n            r.c[i + j] = r.c[i + j] + a.c[i] * b.c[j];\n        }\n    }\n    return r;\n}\nstatic inline bool feIsZero(const FieldElem& a) {\n    for (int k = 0; k <= EPSDEG; k++) if (!coefIsZero(a.c[k])) return false;\n    return true;\n}\n// THE ORDERING.  eps is a positive infinitesimal, so the lowest-degree nonzero\n// coefficient dominates every higher one absolutely -- no magnitude comparison\n// between degrees is ever needed, which is why this stays exact.\nstatic inline int feSign(const FieldElem& v) {\n    for (int k = 0; k <= EPSDEG; k++) {\n        int s = coefSign(v.c[k]);\n        if (s != 0) return s;\n    }\n    return 0;\n}\n'

# ------------------------------------------------- replacements, WIDE variant
# The narrow generator's REPL is reused where its anchors also occur in
# cube_regions_q2w.cpp; the seven that differ (i128 -> i256 and the i256 helper
# API: i256IsZero, i256ToStr, iabs256, idiv256_exact, igcd256) are replaced here.
# Each OLD below was extracted verbatim from cube_regions_q2w.cpp rather than
# transcribed, so an anchor cannot silently drift from the source.
import json as _json, os as _os
_W = _json.load(open(_os.path.join(HERE, '.wide_repl.json')))
_O, _N = _W['old'], _W['new']
_NARROW_OK = _json.load(open(_os.path.join(HERE, '.narrow_ok.json')))
# Narrow pairs 2, 6, 8, 9 -- PKeyHash, the overflow bound, the component parser
# and the parser switch -- whose anchors are IDENTICAL in q2w. Dropping them the
# first time left PKeyHash referring to the old PKey fields and the compile
# failed loudly, which is the right way for that mistake to surface.
REPL = [(o, n) for o, n in _NARROW_OK] + [
    (_O['planek'],  _N['planek']),
    (_O['pkey'],    _N['pkey']),
    (_O['gcdxyzw'], _N['gcdxyzw']),
    (_O['norm'],    _N['norm']),
    (_O['mag'],     _N['mag']),
    (_O['fetos'],   _N['fetos']),
    (_O['usage'],   _N['usage']),
]

def main():
    src = open(SRC).read()
    banner = '// ' + __doc__.replace('\n', '\n// ') + '\n\n'
    i = src.index(OLD_FIELD_START)
    j = src.index('static inline i256 gcdOfList')
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
