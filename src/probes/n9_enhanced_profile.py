import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import level_graph
d=json.load(open('/Users/dmi/cube-compounds/data/n9_region_map.json'))['records']
out={}
for k,v in d.items():
    qs=[tuple(q) for q in v['quats']]
    g=level_graph(qs)
    enh=tuple((g[l]['V'],g[l]['E'],g[l]['c']) for l in sorted(g))
    out[k]=enh
    print(k,'levels',len(g))
    print('   ',enh, flush=True)
ks=list(out)
print('ENHANCED PROFILES IDENTICAL:', out[ks[0]]==out[ks[1]])
json.dump({k:[list(x) for x in v] for k,v in out.items()},
          open('/Users/dmi/cube-compounds/data/n9_enhanced_profile.json','w'),indent=1)
