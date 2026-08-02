#!/usr/bin/env python3
"""Link (I) of the increment chain: Delta_j = |V(G)| - #components(G_j).

INCREMENT_BOUND_SPEC.md derives the one-cube increment from the region
adjacency graph.  Forgetting cube j merges exactly the region pairs joined by
a "bit j" edge -- an adjacency whose two labels differ in bit j -- and merging
is transitive, so

    regions of S_j  =  connected components of G_j,

where G_j is the spanning subgraph of G (INCLUDING the outside region as a
node) keeping only the bit-j edges.  Hence Delta_j = N - #components(G_j) with
N = T + 1, and since a graph on N nodes with c components has at least N - c
edges, Delta_j <= |E(G_j)|.

This checks the identity against the engine: for each j it recounts the
compound with cube j deleted and compares.  The identity is what makes the
whole chain a theorem rather than a heuristic, so it is verified rather than
assumed.

INVARIANT: the two sides are computed by genuinely different routes -- the
left from the adjacency graph of the FULL compound, the right by re-running
the counting engine on the SUBSET.  Deriving both from the same run would make
the test vacuous.
"""
import json
import subprocess

from golden_rotations import rot_from_quat
from region_adjacency import region_adjacency

CONFIGS = {
    'n=2 13-pair': [(1, 0, 0, 0), (0, 1, 1, 1)],
    # a generic rational triple (the first three cubes of the 393 base); the
    # n=3 maximisers are irrational, and this test needs genericity, not a
    # record.  (1,1,0,0) would be a 90-degree turn about x -- a cube
    # self-symmetry -- giving a DUPLICATE solid whose walls change two bits at
    # once and trip region_adjacency's one-bit gate.
    'n=3 generic': [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5)],
    '183 (n=4)': [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
}


def count(cfg):
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    out = subprocess.run(['./cube_regions_n', '--quats', s],
                         capture_output=True, text=True).stdout
    return json.loads(out)['bounded'] if out.startswith('{') else None


def components(nodes, edges):
    parent = {v: v for v in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    return len({find(v) for v in nodes})


def main():
    print('%-12s %2s %6s %6s %8s %8s %8s %7s' %
          ('config', 'j', 'T', 'S_j', 'Delta_j', 'N-comps', '|E(G_j)|', 'ok'))
    allok = True
    for name, cfg in CONFIGS.items():
        res = region_adjacency([rot_from_quat(*q) for q in cfg])
        lab = res['region_label']
        N = len(lab)
        T = res['total']
        assert N == T + 1, (N, T)
        for j in range(len(cfg)):
            bit = 1 << j
            ej = [(u, v) for u, v in res['edges'] if (lab[u] ^ lab[v]) == bit]
            lhs = N - components(list(lab), ej)
            sub = [q for k, q in enumerate(cfg) if k != j]
            Sj = count(sub)
            delta = T - Sj
            ok = (lhs == delta)
            allok &= ok
            print('%-12s %2d %6d %6d %8d %8d %8d %7s'
                  % (name, j, T, Sj, delta, lhs, len(ej),
                     'OK' if ok else 'MISMATCH'), flush=True)
    print('\nidentity (I) holds everywhere: %s' % allok)


if __name__ == '__main__':
    main()
