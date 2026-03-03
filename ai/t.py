lis=[3,4,2,1]
for i in range(1,len(lis)):
    key=lis[i]
    j=i-1
    while j>-1 and key<lis[j]:
        lis[j+1]=lis[j]
        j-=1
    lis[j+1]=key
    print(lis)
