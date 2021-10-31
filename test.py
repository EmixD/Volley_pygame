from math import cos, sin,acos
import math
import numpy as np


fa=0
fb=3.1415*0.5
a=[cos(fa),sin(fa)]
b=[cos(fb),sin(fb)]
print(acos(np.dot(a,b)))
print(math.atan2(b[1],b[0])-math.atan2(a[1],a[0]))
