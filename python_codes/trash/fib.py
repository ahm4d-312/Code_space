
def  fib(n):
    lis=[0,1]
    for i in range(n):
        lis[0],lis[1]=lis[1],lis[0]+lis[1]
    return lis[0]

def main():
    a=-15
    b=10
    print((a^b)^a)
    print((a^b)^b)
if __name__=='__main__':
    main()
        
'''
rax=0111
rbx=1010
rax=1101
rbx=0111
rax=1010
# xor rax,rbx 
# xor rbx, rax 
# xor rax,rbx


'''