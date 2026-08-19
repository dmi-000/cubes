#!/usr/bin/env python3
"""irrational_n45.py -- search n=4 and n=5 for an IRRATIONAL record.

THE LEAD: n=3's record (67) is irrational -- it lives in Q(sqrt2) and
Q(sqrt5) (dimension67.py's RECORDS), not in Q. Every record above n=3
(183 at n=4, 393 at n=5) was found by rational search or by extending a
rational compound, and a subset of a rational compound is always rational,
so 183 provably contains no 67. That means an irrational record at n=4 or
n=5 would be INVISIBLE to every search done so far. Nothing rules one out.

This script searches directly in Z[sqrt d] via cube_regions_q2w --d D
--quats-stdin, for d in {2,3,5,6,7,10,13} (squarefree), n in {4,5}.

Three phases, each time-boxed (wall clock), not config-count-boxed, because
engine speed varies strongly with n, d and component magnitude:
  1. random     -- p+q*sqrt(d) components from small integer ranges, several
                    magnitude caps (menu SHAPE matters more than menu size --
                    ledger note). Cube 0 always fixed to the identity (global
                    rotation is gauge freedom).
  2. seeded     -- start from the two actual n=3 67s (BASE67 below, from
                    dimension67.py's RECORDS) and add 1 (n=4) or 2 (n=5)
                    further cubes drawn widely at random -- NOT extend67.py's
                    narrow perturb-in-place, which only found <=183.
  3. hillclimb  -- single-component +-1 climbing on the best candidates from
                    phases 1-2 to a local max, THEN wide perturbation (several
                    cubes/components at once) and re-climb -- plain greedy
                    climbing stalls, wide perturbation is what found 183
                    (ledger, Postscript 15).

KNOWN-ANSWER GATE runs first and is mandatory: if any of the three seed
counts (67, 67, 183) fails to reproduce exactly, the script stops without
searching -- a wrong number here would poison every later count.

Every engine verdict is one of THREE outcomes, always reported separately:
  - counted  : "bounded" present -- a real region count.
  - refused  : engine returned an "error" (budget overflow OR a degenerate/
               non-generic configuration) -- NOT a low count, must never be
               scored as one.
  - unparseable: stdout line was not valid JSON at all (should not happen;
               reported if it ever does).

Usage: python3 irrational_n45.py [total_minutes]   (default 40)
"""
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "cube_regions_q2w")
LOG_PATH = os.path.join(HERE, "irrational_n45.log")
JSON_PATH = os.path.join(HERE, "irrational_n45.json")

FIELDS = [2, 3, 5, 6, 7, 10, 13]
NS = [4, 5]
RECORD = {4: 183, 5: 393}
IDENTITY = ((1, 0), (0, 0), (0, 0), (0, 0))

# The two n=3 irrational maximisers -- dimension67.py's RECORDS verbatim.
# Component (p, q) means p + q*sqrt(d); cube 0 is the identity in both.
BASE67 = {
    2: [((1, 0), (0, 0), (0, 0), (0, 0)),
        ((1, 0), (1, 0), (0, 1), (0, 0)),
        ((-1, 0), (1, 0), (0, 1), (0, 0))],
    5: [((1, 0), (0, 0), (0, 0), (0, 0)),
        ((2, 0), (1, 1), (-1, 1), (0, 0)),
        ((-2, 0), (1, 1), (-1, 1), (0, 0))],
}

# THE KNOWN-ANSWER GATE (mandatory, run first).
GATES = [
    (2, [IDENTITY, ((1, 0), (1, 0), (0, 1), (0, 0)), ((-1, 0), (1, 0), (0, 1), (0, 0))], 67,
     "octahedral 67"),
    (5, [IDENTITY, ((2, 0), (1, 1), (-1, 1), (0, 0)), ((-2, 0), (1, 1), (-1, 1), (0, 0))], 67,
     "golden 67"),
    (0, [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)], 183,
     "rational n=4 record"),
]

H_LIST = [3, 6, 12]           # random-search magnitude tiers
BATCH_SIZE = 150              # configs per engine subprocess call -- kept
                               # small because time-boxing can only check
                               # the clock BETWEEN batches, so BATCH_SIZE is
                               # the floor of every tier's runtime (n=5
                               # batches cost ~15-20s at this size)


def fmt_component(c):
    return "%d:%d" % c if isinstance(c, tuple) else str(c)


def fmt_config(cfg, d):
    if d == 0:
        # cfg entries are plain 4-tuples of ints (w,x,y,z)
        return ";".join(",".join(str(c) for c in q) for q in cfg)
    return ";".join(",".join(fmt_component(c) for c in q) for q in cfg)


def rand_component(rng, h):
    return (rng.randint(-h, h), rng.randint(-h, h))


def rand_quat(rng, h):
    while True:
        q = tuple(rand_component(rng, h) for _ in range(4))
        if any(c != (0, 0) for c in q):
            return q


class Engine:
    """Batched caller of cube_regions_q2w, with strict counted/refused/
    unparseable accounting and a running best per (n, d)."""

    def __init__(self):
        self.logf = open(LOG_PATH, "a")
        self.counted = 0
        self.refused = 0
        self.unparseable = 0
        self.refusal_reasons = {}
        self.stats = {}   # (n, d) -> dict
        self.t_start = time.time()

    def log(self, msg):
        line = "[%7.1fs] %s" % (time.time() - self.t_start, msg)
        print(line, flush=True)
        self.logf.write(line + "\n")
        self.logf.flush()

    def stat(self, n, d):
        return self.stats.setdefault((n, d), {"counted": 0, "refused": 0,
                                               "best": 0, "best_cfg": None})

    def raw_batch(self, cfgs, d):
        """cfgs: list of configs (each a list of quats). Returns list of
        (bounded_or_None, error_or_None) aligned with cfgs."""
        inp = "\n".join(fmt_config(c, d) for c in cfgs) + "\n"
        try:
            p = subprocess.run([BIN, "--d", str(d), "--quats-stdin"],
                                input=inp, capture_output=True, text=True,
                                timeout=600)
        except subprocess.TimeoutExpired:
            self.log("ENGINE TIMEOUT on batch of %d (d=%d) -- treating all as unparseable"
                      % (len(cfgs), d))
            return [(None, "TIMEOUT")] * len(cfgs)
        lines = p.stdout.splitlines()
        results = []
        for i in range(len(cfgs)):
            if i >= len(lines):
                results.append((None, "MISSING_OUTPUT_LINE"))
                continue
            line = lines[i]
            try:
                obj = json.loads(line)
            except Exception:
                self.unparseable += 1
                results.append((None, "UNPARSEABLE:" + line[:200]))
                continue
            if "bounded" in obj:
                results.append((obj["bounded"], None))
            else:
                err = obj.get("error", "unknown")
                results.append((None, err))
        return results

    def batch(self, n, d, cfgs, tag):
        """Evaluate + record a batch of configs for a given (n, d). cfgs are
        lists of quats (tuples), cube 0 always identity by construction of
        the callers. Returns list of bounded values (None where refused)."""
        results = self.raw_batch(cfgs, d)
        s = self.stat(n, d)
        out = []
        for cfg, (bounded, err) in zip(cfgs, results):
            out.append(bounded)
            if bounded is not None:
                s["counted"] += 1
                self.counted += 1
                if bounded > s["best"]:
                    s["best"] = bounded
                    # must be hashable: climb() memoizes visited configs in
                    # a set, and callers here often pass plain lists
                    s["best_cfg"] = tuple(cfg)
                if bounded >= RECORD.get(n, 10 ** 9):
                    self.log("*** n=%d d=%d BEATS/TIES RECORD %d: bounded=%d cfg=%s tag=%s"
                              % (n, d, RECORD[n], bounded, cfg, tag))
            else:
                s["refused"] += 1
                self.refused += 1
                key = str(err)[:60]
                self.refusal_reasons[key] = self.refusal_reasons.get(key, 0) + 1
        return out

    def eval_one(self, n, d, cfg):
        """Single-config evaluation (used for independent re-verification and
        for cheap single-point checks). Returns (bounded_or_None, err)."""
        r = self.raw_batch([cfg], d)
        return r[0]


# --------------------------------------------------------------- gate
def run_gate(eng):
    eng.log("=" * 70)
    eng.log("KNOWN-ANSWER GATE (mandatory)")
    ok = True
    for d, cfg, expect, label in GATES:
        bounded, err = eng.eval_one(0, d, cfg)  # n arg unused for gate stat
        if bounded == expect:
            eng.log("  PASS  d=%d %-24s -> %d" % (d, label, bounded))
        else:
            eng.log("  FAIL  d=%d %-24s -> got %r (err=%r), expected %d"
                     % (d, label, bounded, err, expect))
            ok = False
    if not ok:
        eng.log("GATE FAILED -- STOPPING. No search performed.")
    else:
        eng.log("GATE PASSED (67, 67, 183 all reproduced exactly).")
    return ok


# --------------------------------------------------------------- phase 1: random
def phase_random(eng, rng, budget_seconds):
    pairs = [(n, d) for n in NS for d in FIELDS]
    per_pair = budget_seconds / len(pairs)
    per_tier = per_pair / len(H_LIST)
    eng.log("=" * 70)
    eng.log("PHASE 1: random search -- %d pairs, %.1fs/pair, %.1fs/tier"
             % (len(pairs), per_pair, per_tier))
    for n, d in pairs:
        pair_deadline = time.time() + per_pair
        for h in H_LIST:
            if time.time() >= pair_deadline:
                break  # a prior tier's mandatory single batch already
                       # overran the pair budget -- skip remaining tiers
                       # rather than compound the overrun
            tier_deadline = time.time() + per_tier
            n_batches = 0
            while time.time() < tier_deadline:
                cfgs = []
                for _ in range(BATCH_SIZE):
                    cfg = [IDENTITY] + [rand_quat(rng, h) for _ in range(n - 1)]
                    cfgs.append(cfg)
                eng.batch(n, d, cfgs, tag="random h=%d" % h)
                n_batches += 1
                if time.time() >= pair_deadline:
                    break
            s = eng.stat(n, d)
            eng.log("  n=%d d=%d h=%d: %d batches, running best=%d counted=%d refused=%d"
                     % (n, d, h, n_batches, s["best"], s["counted"], s["refused"]))
        s = eng.stat(n, d)
        eng.log(" n=%d d=%d DONE random: best=%d cfg=%s" % (n, d, s["best"], s["best_cfg"]))


# --------------------------------------------------------------- phase 2: seeded
def phase_seeded(eng, rng, budget_seconds):
    combos = [(n, d) for d in (2, 5) for n in NS]
    per_combo = budget_seconds / len(combos)
    per_tier = per_combo / len(H_LIST)
    eng.log("=" * 70)
    eng.log("PHASE 2: seeded from the two 67s -- %d combos, %.1fs/combo"
             % (len(combos), per_combo))
    for n, d in combos:
        base = BASE67[d]
        n_add = n - 3
        combo_deadline = time.time() + per_combo
        for h in H_LIST:
            if time.time() >= combo_deadline:
                break
            tier_deadline = time.time() + per_tier
            n_batches = 0
            while time.time() < tier_deadline:
                cfgs = []
                for _ in range(BATCH_SIZE):
                    cfg = list(base) + [rand_quat(rng, h) for _ in range(n_add)]
                    cfgs.append(cfg)
                eng.batch(n, d, cfgs, tag="seeded67 h=%d" % h)
                n_batches += 1
                if time.time() >= combo_deadline:
                    break
            s = eng.stat(n, d)
            eng.log("  seeded n=%d d=%d h=%d: %d batches, running best=%d"
                     % (n, d, h, n_batches, s["best"]))
        s = eng.stat(n, d)
        eng.log(" n=%d d=%d DONE seeded: best=%d cfg=%s" % (n, d, s["best"], s["best_cfg"]))


# --------------------------------------------------------------- phase 3: hillclimb
def component_neighbors(cfg, n):
    """All single +-1 moves on p or q of one component of one non-identity
    cube."""
    out = []
    for i in range(1, n):
        quat = cfg[i]
        for j in range(4):
            p, q = quat[j]
            for dp, dq in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                newc = (p + dp, q + dq)
                newquat = list(quat)
                newquat[j] = newc
                if all(c == (0, 0) for c in newquat):
                    continue
                newcfg = list(cfg)
                newcfg[i] = tuple(newquat)
                out.append(tuple(newcfg))
    return out


def wide_kicks(cfg, n, rng, num_variants, k_range, mag_range):
    out = []
    for _ in range(num_variants):
        newcfg = [list(q) for q in cfg]
        k = min(rng.choice(k_range), n - 1)
        idxs = rng.sample(range(1, n), k)
        for i in idxs:
            quat = list(newcfg[i])
            j = rng.randrange(4)
            m = rng.choice(mag_range)
            p, q = quat[j]
            quat[j] = (p + rng.randint(-m, m), q + rng.randint(-m, m))
            newcfg[i] = tuple(quat)
        if any(all(c == (0, 0) for c in newcfg[i]) for i in range(n)):
            continue
        out.append(tuple(tuple(q) for q in newcfg))
    return out


def climb(eng, n, d, start_cfg, start_val, deadline, tag):
    best_cfg, best_val = start_cfg, start_val
    memo = {start_cfg}
    while time.time() < deadline:
        neighbors = [c for c in component_neighbors(best_cfg, n) if c not in memo]
        if not neighbors:
            break
        memo.update(neighbors)
        vals = eng.batch(n, d, neighbors, tag=tag)
        improved = False
        for c, v in zip(neighbors, vals):
            if v is not None and v > best_val:
                best_val, best_cfg = v, c
                improved = True
        if not improved:
            break
    return best_cfg, best_val


def phase_hillclimb(eng, rng, budget_seconds):
    eng.log("=" * 70)
    eng.log("PHASE 3: hillclimb -- single-component climb, then wide "
             "perturbation + re-climb")
    # top candidates: best (n,d) pair per n, plus best seeded-origin ones.
    candidates = []
    for (n, d), s in eng.stats.items():
        if s["best_cfg"] is not None and s["best"] > 0:
            candidates.append((n, d, s["best_cfg"], s["best"]))
    candidates.sort(key=lambda t: -t[3])
    # take top few per n, dedup by (n,d)
    picked = []
    seen_pairs = set()
    for n in NS:
        for (cn, cd, cfg, val) in candidates:
            if cn != n:
                continue
            if (cn, cd) in seen_pairs:
                continue
            picked.append((cn, cd, cfg, val))
            seen_pairs.add((cn, cd))
            if len([1 for p in picked if p[0] == n]) >= 3:
                break
    if not picked:
        eng.log("  no positive-count candidates to climb from -- skipping")
        return
    per_cand = budget_seconds / len(picked)
    eng.log("  climbing %d candidates, %.1fs each: %s"
             % (len(picked), per_cand,
                [(n, d, v) for n, d, _, v in picked]))
    for n, d, cfg, val in picked:
        cand_deadline = time.time() + per_cand
        climb_deadline = time.time() + per_cand * 0.55
        eng.log(" -- climbing n=%d d=%d from %d --" % (n, d, val))
        best_cfg, best_val = climb(eng, n, d, cfg, val, climb_deadline,
                                    tag="climb1 n=%d d=%d" % (n, d))
        eng.log("   local max after single-component climb: %d" % best_val)
        # wide perturbation rounds with the remaining time
        round_no = 0
        while time.time() < cand_deadline:
            round_no += 1
            kicks = wide_kicks(best_cfg, n, rng, num_variants=80,
                                k_range=(2, 3, max(2, n - 1)),
                                mag_range=(1, 2, 3))
            if not kicks:
                break
            vals = eng.batch(n, d, kicks, tag="widekick n=%d d=%d round=%d" % (n, d, round_no))
            top = sorted([(v, c) for v, c in zip(vals, kicks) if v is not None],
                         key=lambda t: -t[0])[:2]
            improved_any = False
            for v, c in top:
                if time.time() >= cand_deadline:
                    break
                sub_deadline = min(cand_deadline, time.time() + per_cand * 0.15)
                rc, rv = climb(eng, n, d, c, v, sub_deadline,
                                tag="climb-after-kick n=%d d=%d" % (n, d))
                if rv > best_val:
                    best_val, best_cfg = rv, rc
                    improved_any = True
            eng.log("   round %d: kicks=%d best now %d%s"
                     % (round_no, len(kicks), best_val, " (improved)" if improved_any else ""))
            if not improved_any and round_no >= 3:
                # widen further or stop; keep trying until time runs out but
                # avoid infinite tight loop with no progress log spam
                pass
        s = eng.stat(n, d)
        if best_val > s["best"]:
            s["best"] = best_val
            s["best_cfg"] = best_cfg
        eng.log(" -- done n=%d d=%d: hillclimb best=%d (started from %d)" % (n, d, best_val, val))


# --------------------------------------------------------------- reporting
def write_report(eng, elapsed):
    report = {
        "elapsed_seconds": round(elapsed, 1),
        "totals": {"counted": eng.counted, "refused": eng.refused,
                    "unparseable": eng.unparseable},
        "refusal_reasons": eng.refusal_reasons,
        "records_to_beat": RECORD,
        "per_n_d": {},
        "record_beaten": {},
    }
    beat_any = False
    for (n, d), s in sorted(eng.stats.items()):
        report["per_n_d"]["n=%d,d=%d" % (n, d)] = {
            "counted": s["counted"], "refused": s["refused"],
            "best": s["best"],
            "best_cfg": [list(map(list, q)) if isinstance(q[0], tuple) else list(q)
                         for q in s["best_cfg"]] if s["best_cfg"] else None,
        }
        if s["best"] >= RECORD.get(n, 10 ** 9):
            beat_any = True
    for n in NS:
        best_over_d = max((s["best"] for (nn, dd), s in eng.stats.items() if nn == n), default=0)
        report["record_beaten"]["n=%d" % n] = best_over_d >= RECORD[n]
    json.dump(report, open(JSON_PATH, "w"), indent=1)
    eng.log("=" * 70)
    eng.log("FINAL REPORT written to %s" % JSON_PATH)
    eng.log("TOTALS: counted=%d refused=%d unparseable=%d"
             % (eng.counted, eng.refused, eng.unparseable))
    if eng.refusal_reasons:
        eng.log("refusal reasons: %s" % eng.refusal_reasons)
    for n in NS:
        eng.log("--- n=%d ---" % n)
        for d in FIELDS:
            s = eng.stats.get((n, d))
            if s is None:
                eng.log("  d=%2d: NOT SEARCHED" % d)
                continue
            flag = "  ** RECORD BEATEN/TIED (%d) **" % RECORD[n] if s["best"] >= RECORD[n] else ""
            eng.log("  d=%2d: counted=%5d refused=%4d best=%4d%s"
                     % (d, s["counted"], s["refused"], s["best"], flag))
    eng.log("record_beaten: %s" % report["record_beaten"])
    return report, beat_any


def independent_reverify(eng, n, d, cfg):
    eng.log("=" * 70)
    eng.log("INDEPENDENT RE-VERIFICATION of candidate n=%d d=%d" % (n, d))
    eng.log("quaternions (p:q each component, p + q*sqrt(%d)):" % d)
    for i, q in enumerate(cfg):
        eng.log("  cube %d: %s" % (i, fmt_config([q], d)))
    bounded, err = eng.eval_one(n, d, cfg)
    eng.log("re-run through engine (fresh subprocess call): bounded=%r err=%r" % (bounded, err))
    eng.log("full config string: %s" % fmt_config(cfg, d))
    return bounded


def main():
    total_minutes = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0
    total_seconds = total_minutes * 60.0
    eng = Engine()
    eng.log("irrational_n45.py starting, budget=%.1f min" % total_minutes)

    if not run_gate(eng):
        write_report(eng, time.time() - eng.t_start)
        sys.exit(1)

    rng = random.Random(20260818)

    # Budget split: random 60%, seeded 17%, hillclimb 21%, ~2% slack already
    # implicit in per-phase time-boxing overrun tolerance.
    remaining = total_seconds - (time.time() - eng.t_start)
    random_budget = remaining * 0.60
    seeded_budget = remaining * 0.18
    climb_budget = remaining * 0.22

    # Each phase checkpoints the JSON report immediately after it finishes,
    # so a crash in a later phase (this cost 27 minutes of engine compute
    # once already, to a hillclimb bug that hit only after phases 1-2 had
    # both completed cleanly) does not discard completed phases' results.
    phase_random(eng, rng, random_budget)
    write_report(eng, time.time() - eng.t_start)
    phase_seeded(eng, rng, seeded_budget)
    write_report(eng, time.time() - eng.t_start)
    phase_hillclimb(eng, rng, climb_budget)

    elapsed = time.time() - eng.t_start
    report, beat_any = write_report(eng, elapsed)

    if beat_any:
        eng.log("*** AT LEAST ONE (n,d) PAIR REACHED OR EXCEEDED ITS RECORD -- "
                 "independently re-verifying each ***")
        for (n, d), s in sorted(eng.stats.items()):
            if s["best"] >= RECORD.get(n, 10 ** 9):
                independent_reverify(eng, n, d, s["best_cfg"])
    else:
        eng.log("No (n,d) pair reached its record (183 for n=4, 393 for n=5). "
                 "Best-found values are reported above and in %s." % JSON_PATH)

    eng.log("DONE. Total elapsed %.1fs (%.1f min)." % (elapsed, elapsed / 60))


if __name__ == "__main__":
    main()
