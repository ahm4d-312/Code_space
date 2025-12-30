import time
import random
import numpy as np

binary_search_time_avg=float(0)
linear_search_time_avg=float(0)
def binary_search(lis, target):
    start = time.perf_counter()
    global binary_search_time_avg
    mid = 0 if target == lis[0] else len(lis) - 1 if lis[-1] == target else -1  # checks if the target value is in the first or the last index in the array.

    if mid != -1:
        binary_search_time_avg+=time.perf_counter() - start
        return mid

    low, top = 0, len(lis) - 1

    while low <= top:
        mid = (top + low) // 2  # // stores the result as int, same result as floor of normal division.

        if lis[mid] == target:
            binary_search_time_avg+=time.perf_counter() - start
            return mid

        if lis[mid] >= target:
            top = mid - 1
        else:
            low = mid + 1

    binary_search_time_avg+=time.perf_counter() - start
    return -1


def linear_search(lis, target):
    start = time.perf_counter()
    global linear_search_time_avg
    for i in range(len(lis)):
        if lis[i] == target:
            linear_search_time_avg+=time.perf_counter() - start
            return i

    linear_search_time_avg+=time.perf_counter() - start
    return -1


def main():
    lis = np.arange(10**7)

    test_cases = [random.choice(lis) for _ in range(90)]
    [test_cases.append(x) for x in range(-1,-11,-1)] # adding some none existing values
    print("The list size that the two algorithms will be tested on is 10 millions items.")
    print("The test will be on 100 items 90 of them exist in the array, the remaining 10 is not")
    print("Doing the binary search test cases...")
    for i in range(len(test_cases)):
        print(f"\rTest number: {i+1}...",end="",flush=True)
        time.sleep(0.004)# The binary seach is too fast i have to slow it down a bit to show the progress, remove this and it will be done instantly.
        binary_search(lis, test_cases[i]) # The time is calculated inside the function it self for each test case, then the avrage is calculated, the result doesn't matter.
        
    print("\nDone.")
    print("Doing the linear search test cases...")

    for i in range(len(test_cases)):
        print(f"\rTest number: {i+1}...",end="",flush=True)
        linear_search(lis, test_cases[i])# The time is calculated inside the function it self for each test case, then the avrage is calculated, the result doesn't matter.
    print("\nDone.\nResults:")
    print(f"Binary search avrage search time: {binary_search_time_avg/len(test_cases):.9f}")
    print(f"Linear search avrage search time: {linear_search_time_avg/len(test_cases):.9f}")


if __name__ == "__main__":
    main()
