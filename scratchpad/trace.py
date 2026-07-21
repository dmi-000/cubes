import numpy as np
from scipy.optimize import brentq

def resid1(D, P):
    cD,sD,cP,sP = np.cos(D), np.sin(D), np.cos(P), np.sin(P)
    return -cD*cP*sP + cD*sP**2 + cD - cP*sD + cP*sP - sP**2 + 1

def resid2(D, P):
    cD,sD,cP,sP = np.cos(D), np.sin(D), np.cos(P), np.sin(P)
    return cD*cP*sP + cD*sP**2 + cD + cP*sD - cP*sP - sP**2 + 1

import math
oct_psi = math.asin(1/math.sqrt(3))
print('oct psi deg', math.degrees(oct_psi))
print('resid1 at (120,oct)=', resid1(math.radians(120), oct_psi))
print('resid2 at (120,oct)=', resid2(math.radians(120), oct_psi))

# trace resid1=0 branch near Delta=120deg as psi varies
for psi_deg in [20,25,30,35.264,40,45,50,60,70,80,85]:
    P = math.radians(psi_deg)
    try:
        D = brentq(lambda D: resid1(D,P), math.radians(90), math.radians(150))
        print(f'psi={psi_deg:6.2f}  Delta(resid1=0)={math.degrees(D):8.3f}   resid2 there={resid2(D,P):+.6e}')
    except Exception as e:
        print(f'psi={psi_deg}: {e}')
