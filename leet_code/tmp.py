s=set()
while True:
    try:
        n=list(map(int,input().split()))
        sum_nums=sum(n)
    except Exception as e:
            break
    if sum_nums not in s:
        s.add(sum_nums)
    else:
        print("exists\n")