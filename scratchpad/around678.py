import sys
from fractions import Fraction as F
sys.path.insert(0,'/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad')
from around import around
from dirscan import BASE
which=sys.argv[1]
if which=='6': around(BASE+[(7,14,1,-5)],'n=6 727',F(1,64))
if which=='7': around(BASE+[(7,14,1,-5),(4,-3,-4,-4)],'n=7 1217',F(1,64))
if which=='8': around(BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)],'n=8 1895',F(1,64))
