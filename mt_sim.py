#!/usr/bin/env python3
# Working principles: CPP_SPEC.md (validated seed->config RNG chain). Project index: README.md
"""Validate a from-scratch reimplementation of the seed -> configuration
chain (numpy MT19937 + legacy polar Gaussian + scipy Rotation.random
quaternion order + our common-scale rationalization) against the real
numpy/scipy, so it can be ported verbatim to JavaScript for the general
seed viewer artifact.

Chain being reproduced, for integer seed < 2**32:
  RandomState(seed): MT19937 init_genrand(seed)      [numpy _legacy_seeding]
  rk_double = ((a>>5)*67108864 + (b>>6)) / 2**53     [two uint32 draws]
  rk_gauss: Marsaglia polar, returns f*x2 first, caches f*x1
  Rotation.random(6): normal(size=(6,4)) row-major = (x,y,z,w) per cube
  as_quat-from-matrix sign convention: largest-|component| positive
  rationalize: flip to (w,x,y,z), round(c*512), gcd-reduce
"""
import math

import numpy as np
from scipy.spatial.transform import Rotation

from certify_six import rationalize
from six_cube_search import random_mats


class MT:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30))
                          + i) & 0xFFFFFFFF
        self.idx = 624
        self.has_gauss = False
        self.gauss = 0.0

    def u32(self):
        if self.idx >= 624:
            for i in range(624):
                y = (self.mt[i] & 0x80000000) | (self.mt[(i + 1) % 624] & 0x7FFFFFFF)
                self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
                if y & 1:
                    self.mt[i] ^= 0x9908B0DF
            self.idx = 0
        y = self.mt[self.idx]
        self.idx += 1
        y ^= y >> 11
        y = (y ^ ((y << 7) & 0x9D2C5680)) & 0xFFFFFFFF
        y = (y ^ ((y << 15) & 0xEFC60000)) & 0xFFFFFFFF
        return y ^ (y >> 18)

    def dbl(self):
        a = self.u32() >> 5
        b = self.u32() >> 6
        return (a * 67108864.0 + b) / 9007199254740992.0

    def gauss_(self):
        if self.has_gauss:
            self.has_gauss = False
            return self.gauss
        while True:
            x1 = 2.0 * self.dbl() - 1.0
            x2 = 2.0 * self.dbl() - 1.0
            r2 = x1 * x1 + x2 * x2
            if r2 < 1.0 and r2 != 0.0:
                break
        f = math.sqrt(-2.0 * math.log(r2) / r2)
        self.gauss = f * x1
        self.has_gauss = True
        return f * x2


def sim_quats(seed, n=6, scale=512):
    """Integer quaternions (w,x,y,z) for the rationalized configuration."""
    mt = MT(seed)
    out = []
    for _ in range(n):
        x, y, z, w = (mt.gauss_() for _ in range(4))
        nrm = math.sqrt(x * x + y * y + z * z + w * w)
        q = [w / nrm, x / nrm, y / nrm, z / nrm]
        # scipy as_quat (from_matrix) sign: largest-|component| positive
        m = max(range(4), key=lambda i: abs(q[i]))
        if q[m] < 0:
            q = [-c for c in q]
        ints = [round(c * scale) for c in q]
        g = math.gcd(*ints)
        if g > 1:
            ints = [i // g for i in ints]
        out.append(ints)
    return out


def ref_quats(seed, scale=512):
    out = []
    for M in random_mats(seed):
        q = Rotation.from_matrix(M).as_quat()
        comps = (q[3], q[0], q[1], q[2])
        ints = [round(c * scale) for c in comps]
        g = math.gcd(*ints)
        if g > 1:
            ints = [i // g for i in ints]
        out.append(ints)
    return out


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    bad = 0
    seeds = list(range(60)) + [119, 403, 422, 777, 12345, 999983]
    for s in seeds:
        if sim_quats(s) != ref_quats(s):
            print(f'MISMATCH at seed {s}')
            print('  sim:', sim_quats(s))
            print('  ref:', ref_quats(s))
            bad += 1
    print(f'{len(seeds)} seeds checked, {bad} mismatches'
          + ('  -- PASS' if bad == 0 else '  -- FAIL'))
