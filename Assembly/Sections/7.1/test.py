#!/usr/bin/python3

import sys
lis=[]
t=True 
for i in sys.argv:
    if t:
        t=False
        continue
    lis.append(i)
print(lis)
