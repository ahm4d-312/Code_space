import inspect
import numpy as np
lis,m=np.arange(10**4),4
left,top=0,len(lis)-1
boundrais=np.arange(m+1)
boundrais[0]=left
boundrais[-1]=top
boundrais[1]=(boundrais[-1]+1)//m

for i in range(2,m):
    boundrais[i]=boundrais[1]*i
print([int(x) for x in boundrais])

numpy_int = np.int64(42)
print(numpy_int)