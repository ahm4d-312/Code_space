import time
import random
import numpy as np

time_avg=float(0)
def search(lis, target):
    start = time.perf_counter()
    global time_avg
    mid = 0 if target == lis[0] else len(lis) - 1 if lis[-1] == target else -1  # checks if the target value is in the first or the last index in the array.

    if mid != -1:
        time_avg+=time.perf_counter() - start
        return mid

    low, top = 0, len(lis) - 1

    while low <= top:
        mid = (top + low) // 2  # // stores the result as int, same result as floor of normal division.

        if lis[mid] == target:
            time_avg+=time.perf_counter() - start
            return mid

        if lis[mid] >= target:
            top = mid - 1
        else:
            low = mid + 1

    time_avg+=time.perf_counter() - start
    return -1



def main():
    lis = np.arange(10**7)

    test_cases = [random.choice(lis) for _ in range(900)]
    [test_cases.append(x) for x in range(-1,-101,-1)] # adding some none existing values
    print("The list size that the two algorithms will be tested on is 10 millions items.")
    print("The test will be on 1000 items %90 of them exist in the array, the remaining %10 is not")
    print("Doing the test cases...")
    for i in range(len(test_cases)):
        print(f"\rTest number: {i+1}...",end="",flush=True)
        time.sleep(0.002)# The binary seach is too fast i have to slow it down to show the progress, remove this and it will be done instantly  .

        search(lis, test_cases[i]) # The time is calculated inside the function it self for each test case, then the avrage is calculated, the result doesn't matter.
        
    print("\nDone.")
    print(f"Avrage search time: {time_avg/len(test_cases):.15f}")


if __name__ == "__main__":
    main()