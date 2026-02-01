import  random
lis=[]
for i in range(1000):
    lis.append(i+1)
lis=[random.choice(lis) for _ in lis]
lis=[1,2,3]
l=[]
print(lis.extend(l))
print(lis)
def is_sorted(lis): # check if the list is already sorted, avoid worst case scenarios in some algorithms
    # ascending and descending order checking
    ascending=True
    descending=True
    for i in range(len(lis)-1):
        if lis[i]>lis[i+1] :
            ascending=False
        elif lis[i]<lis[i+1]:
            descending=False
    return ascending|descending
print(is_sorted([5,5,4]))