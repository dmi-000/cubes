import numpy as np

# Local model at a triple point: three convex polygons P_i in the tangent plane,
# m_i(theta) = support function h_{P_i}(theta). 
# top diagram = argmin_i m_i  (farthest cell),  deg_top = # index switches
# bottom diagram = argmax_i m_i (nearest cell),  deg_bot = # index switches
# Proposed Step-T lemma claims deg_top <= deg_bot at every triple point.

def support(poly, th):
    # poly: list of 2D vertices; support h(th)=max_v <v,u_th>
    u = np.array([np.cos(th), np.sin(th)])
    return max(np.dot(v, u) for v in poly)

def switches(polys, which):
    # count index switches of arg{min,max} around the circle
    N = 200000
    ths = np.linspace(0, 2*np.pi, N, endpoint=False)
    idx = []
    for th in ths:
        vals = [support(p, th) for p in polys]
        idx.append(int(np.argmin(vals) if which=='min' else np.argmax(vals)))
    idx = np.array(idx)
    sw = np.sum(idx != np.roll(idx, 1))
    return sw

# Counterexample:  P1 ~ small triangle (a=3 corner),  P2,P3 thin 2-gon "blades"
seg_x = [np.array([-3.0,0.0]), np.array([3.0,0.0])]     # P2: blade, gradients +/-x
seg_y = [np.array([0.0,-3.0]), np.array([0.0,3.0])]     # P3: blade, gradients +/-y
tri   = [np.array([1.0,0.0]),                            # P1: small corner (a=3)
         np.array([-0.5, 0.866]),
         np.array([-0.5,-0.866])]

polys = [tri, seg_x, seg_y]
dt = switches(polys, 'min')
db = switches(polys, 'max')
print("deg_top (argmin switches) =", dt)
print("deg_bot (argmax switches) =", db)
print("Lemma deg_top <= deg_bot ?", dt <= db)
