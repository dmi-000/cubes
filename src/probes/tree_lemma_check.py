"""Exact brute-force check of the tree lemma.

Tree bipartite into REGION nodes (colour 0/1/2, degree>=2) and L nodes (LIVE/DEAD),
>=1 LIVE.  H: every DEAD L node's neighbours share one colour.
Quantity: n_P = #components of (T minus colour-P regions) containing a LIVE L
(n_P = 1 if P absent).  Claim under H: #LIVE - 1 >= sum_P (n_P - 1).

Method: component structure of L nodes (per P) does not depend on the live/dead
marking, so it is computed once per (tree, orientation, colouring); markings are then
enumerated as bitmasks.  Under H, non-monochromatic L nodes are forced LIVE and only
monochromatic L nodes are free, so H-instances are enumerated directly (no filtering
bias); "H-instances" = every (tree, orientation, colouring, marking) satisfying H
with >=1 live.  Duplicates across isomorphic labellings/orientations are possible.

Control (H dropped) is run over all 2^l markings up to CONTROL_N (cost), and
also records the smallest counterexample overall (first found in increasing n).

Colours: 3 by default (a triple has three pairs, [P410]). `--colours 4` runs the same check
with four colours, as needed at level 3 of five cubes, where each 4-subset has four 3-subsets
([P430]); its output goes to a separate file.
"""
import itertools, json, time, sys

class Tree:
    """Minimal graph: nodes 0..n-1, adjacency lists (no networkx available)."""
    def __init__(self, n, edges):
        self.n = n; self.adj = [[] for _ in range(n)]; self._e = [tuple(e) for e in edges]
        for a, b in self._e: self.adj[a].append(b); self.adj[b].append(a)
    def __getitem__(self, v): return self.adj[v]
    def degree(self, v): return len(self.adj[v])
    def number_of_nodes(self): return self.n
    def edges(self): return self._e
    def __iter__(self): return iter(range(self.n))

def _canon(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    deg = [len(x) for x in adj]; leaves = [v for v in range(n) if deg[v] <= 1]
    rem = n; removed = [False]*n
    while rem > 2:
        rem -= len(leaves); nxt = []
        for v in leaves:
            removed[v] = True
            for u in adj[v]:
                if not removed[u]:
                    deg[u] -= 1
                    if deg[u] == 1: nxt.append(u)
        leaves = nxt
    centers = [v for v in range(n) if not removed[v]]
    def enc(v, p): return "(" + "".join(sorted(enc(u, v) for u in adj[v] if u != p)) + ")"
    return min(enc(c, -1) for c in centers)

_cache = {1: [()]}
def _edge_lists(n):
    if n in _cache: return _cache[n]
    seen = {}
    for el in _edge_lists(n-1):
        for v in range(n-1):
            e2 = list(el) + [(v, n-1)]
            seen.setdefault(_canon(n, e2), e2)
    _cache[n] = list(seen.values()); return _cache[n]

NCOL = int(sys.argv[sys.argv.index('--colours') + 1]) if '--colours' in sys.argv else 3
OUT = "/Users/dmi/cube-compounds/data/tree_lemma_check%s.json" % ('' if NCOL == 3 else '_c%d' % NCOL)
MAX_N = 14
BUDGET = 480.0          # seconds; stop raising N once next n is not expected to fit
CONTROL_N = 9

def claim(nlive, nps):
    return nlive - 1 >= sum(x - 1 for x in nps)

def nP_list(regions, adj_R, nL, colour):
    """Per P: list of component bitmasks over L nodes (or None if P absent)."""
    res = []
    for P in range(NCOL):
        if P not in colour.values():
            res.append(None); continue
        parent = list(range(nL))
        def f(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for r in regions:
            if colour[r] == P: continue
            ls = adj_R[r]
            for a in ls[1:]:
                parent[f(a)] = f(ls[0])
        comps = {}
        for i in range(nL):
            comps[f(i)] = comps.get(f(i), 0) | (1 << i)
        res.append(list(comps.values()))
    return res

def nps_for(comps, live):
    return [1 if c is None else sum(1 for m in c if m & live) for c in comps]

def run_instance_set(G, Rside, Lside, mode, stats, record):
    """mode 'H' or 'ALL'. Updates stats dict."""
    regions = list(Rside); Ls = list(Lside)
    if any(G.degree(r) < 2 for r in regions): return
    lidx = {v: i for i, v in enumerate(Ls)}
    nL = len(Ls)
    adj_R = {r: [lidx[x] for x in G[r]] for r in regions}
    adj_L = [[v for v in G[l]] for l in Ls]
    full = (1 << nL) - 1
    for cols in itertools.product(range(NCOL), repeat=len(regions)):
        colour = dict(zip(regions, cols))
        comps = nP_list(regions, adj_R, nL, colour)
        mono = 0
        for i in range(nL):
            if len({colour[r] for r in adj_L[i]}) <= 1: mono |= 1 << i
        if mode == 'H':
            forced, free = full & ~mono, mono
        else:
            forced, free = 0, full
        sub = free
        while True:                      # all submasks of free (incl 0)
            live = forced | sub
            if live:
                ok_H = (full & ~live & ~mono) == 0
                stats['inst'] += 1
                if ok_H: stats['hinst'] += 1
                nps = nps_for(comps, live)
                if not claim(bin(live).count('1'), nps):
                    if ok_H:
                        stats['hviol'] += 1
                        if stats['hfirst'] is None:
                            stats['hfirst'] = record(G, Rside, Ls, colour, live)
                    else:
                        stats['cviol'] += 1
                        if stats['cfirst'] is None:
                            stats['cfirst'] = record(G, Rside, Ls, colour, live)
            if sub == 0: break
            sub = (sub - 1) & free

def make_record(G, Rside, Ls, colour, live):
    return {"nodes": G.number_of_nodes(), "edges": sorted(map(list, G.edges())),
            "region_colours": {str(r): colour[r] for r in Rside},
            "L_live": {str(l): bool(live >> i & 1) for i, l in enumerate(Ls)}}

def orientations(T):
    if T.number_of_nodes() == 1:
        return [([], [0])]
    col = {0: 0}; st = [0]
    while st:
        v = st.pop()
        for u in T[v]:
            if u not in col: col[u] = 1 - col[v]; st.append(u)
    a = {v for v in col if col[v] == 0}; b = {v for v in col if col[v] == 1}
    return [(sorted(a), sorted(b)), (sorted(b), sorted(a))]

def trees(n):
    return [Tree(n, el) for el in _edge_lists(n)]

def new_stats():
    return dict(inst=0, hinst=0, hviol=0, cviol=0, hfirst=None, cfirst=None)

def main():
    t0 = time.time()
    # --- second control: explicit path
    G = Tree(5, [(0,1),(1,2),(2,3),(3,4)])   # 0=L live,1=R c0,2=L dead,3=R c1,4=L live
    colour = {1: 0, 3: 1}; Ls = [0, 2, 4]; live = 0b101
    regions = [1, 3]
    lidx = {v: i for i, v in enumerate(Ls)}
    adj_R = {r: [lidx[x] for x in G[r]] for r in regions}
    comps = nP_list(regions, adj_R, 3, colour)
    nps = nps_for(comps, live)
    assert nps == [2, 2] + [1] * (NCOL - 2), nps
    assert not claim(2, nps)            # 2-1=1 < 2
    assert len({colour[r] for r in G[2]}) == 2   # indeed violates H
    path_ctrl = {"n_P": nps, "lhs": 1, "rhs": 2, "claim_fails": True}

    per_n = {}; hviol = 0; hfirst = None
    ctrl_per_n = {}; cfirst = None; cviol_total = 0
    maxN = 0; last = 0.0
    for n in range(1, MAX_N + 1):
        tn = time.time()
        sH = new_stats()
        for T in trees(n):
            for Rs, Ls_ in orientations(T):
                run_instance_set(T, Rs, Ls_, 'H', sH, make_record)
        per_n[n] = {"instances": sH['inst'], "H_instances": sH['hinst'],
                    "H_violations": sH['hviol'], "seconds": round(time.time() - tn, 2)}
        hviol += sH['hviol']
        if hfirst is None and sH['hfirst']: hfirst = sH['hfirst']
        maxN = n
        print(f"n={n}: H-instances={sH['hinst']} violations={sH['hviol']} ({time.time()-tn:.1f}s)", flush=True)
        # control (H dropped), all markings
        if n <= CONTROL_N:
            sC = new_stats()
            for T in trees(n):
                for Rs, Ls_ in orientations(T):
                    run_instance_set(T, Rs, Ls_, 'ALL', sC, make_record)
            ctrl_per_n[n] = {"instances": sC['inst'], "H_instances": sC['hinst'],
                             "violations_total": sC['cviol'] + sC['hviol'],
                             "violations_non_H": sC['cviol']}
            assert sC['hinst'] == sH['hinst'] and sC['hviol'] == sH['hviol'], "H-mode vs ALL-mode mismatch"
            cviol_total += sC['cviol']
            if cfirst is None and sC['cfirst']: cfirst = sC['cfirst']
        dt = time.time() - tn
        if (time.time() - t0) + dt * 6 > BUDGET and n >= 12: break
    assert cfirst is not None, "CONTROL FOUND NO VIOLATION: check is vacuous or buggy"
    out = {"max_N_reached": maxN, "per_N_H_enumeration": per_n,
           "H_violations_total": hviol, "H_first_violation": hfirst,
           "control_H_dropped": {"max_N_run": max(ctrl_per_n), "per_N": ctrl_per_n,
                                 "non_H_violations_total": cviol_total,
                                 "smallest_counterexample": cfirst,
                                 "failed_as_required": cfirst is not None},
           "path_control": path_ctrl,
           "notes": "Instances counted with duplicates over (labelled tree rep, orientation, colouring, marking); live>=1; region degree>=2; n=1 (lone live L) included; n=2 yields none.",
           "runtime_seconds": round(time.time() - t0, 1)}
    json.dump(out, open(OUT, "w"), indent=1)
    print("max N", maxN, "H violations", hviol, "control smallest:", json.dumps(cfirst), "runtime", out["runtime_seconds"])

main()
