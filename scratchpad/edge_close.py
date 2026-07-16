import numpy as np

M1 = np.array([[0.950747,-0.276202,-0.140689],
               [0.140689,0.788951,-0.598133],
               [0.276202,0.54888,0.788951]])
C = np.array([[0,0,1],[1,0,0],[0,1,0]],float)

print("orthogonality err:", np.abs(M1@M1.T-np.eye(3)).max(), " det:", np.linalg.det(M1))

# identify against slide family: S(t) = R(axis, t*delta) @ Rx(45)
c=np.cos(np.pi/4); s=np.sin(np.pi/4)
Rx45=np.array([[1,0,0],[0,c,-s],[0,s,c]])
R = M1 @ Rx45.T
ang = np.arccos((np.trace(R)-1)/2)
ax = np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]])
ax /= np.linalg.norm(ax)
delta = np.deg2rad(40.3060)
print("rot angle deg:", np.rad2deg(ang), " t =", ang/delta)
print("axis:", ax, " vs slide axis (-0.442177,-0.828653,0.343239)")
