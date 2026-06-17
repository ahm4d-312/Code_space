def fib_recursion(num, memory=None):
    if memory is None:
        memory=dict()
    if num < 2:
        return num
    if num not in memory:
        memory[num] = fib_recursion(num-1,memory) + fib_recursion(num-2,memory)
    return memory[num]

def fib_loop(num):
    lis=[0,1]
    if num < 2:
        return num
    for _ in range(2,num):
        lis[0]=lis[0]^lis[1]
        lis[1]=lis[0]^lis[1]
        lis[0]=lis[0]^lis[1]
        lis[1]=lis[0]+lis[1]
    return lis[0]+ lis[1]

def main():
    print(f"\033[H\033[2J\033[3J")
    while True:
        print("Enter a number to choose a mode:")
        print("1) Recursion mode")
        print("2) For loop mode")
        print("3) exit")
        option=int(input("~> "))
        try:
            if ( option!=1 and option!=2 ):
                break
            num=int(input("Enter the value: "))
            if option==1:
                fib_num=fib_recursion(num)
                print(f"The fib value of {num} is: {fib_num}")
                print("Note: The recursion mode was used")
            else:
                fib_num=fib_loop(num)
                print(f"The fib value of {num} is: {fib_loop(num)}")
                print("Note: The loop mode was used")
            input()
            print(f"\033[H\033[2J\033[3J")
        except Exception as e:
            print(f"Error occured: {str(e)}")
            continue

if __name__=='__main__':
    main()
 