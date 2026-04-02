import time
import random
import statistics
import gc
import numpy as np


def quadratic_search(lis:list, target:int):
    low, top= 0, len(lis)-1
    while top-low > 4:
        mid = low + ((top-low) >> 2)
        quarter_interval = mid - low

        if target < lis[mid]:
            top=mid-1
        elif target < lis[mid+quarter_interval]:
            low=mid
            top=mid+quarter_interval-1
        elif target < lis[mid+quarter_interval*2]:
            low=mid+quarter_interval
            top=mid+quarter_interval*2-1
        else:
            low=mid+quarter_interval*2
    
    for i in range(low,top+1):
        if target==lis[i]:
            return i
    return -1
    

# WRAPPERS (keep overhead equal)
def run_quadratic_search(lis, target):
    return quadratic_search(lis, target)

def bench(search_func, lis, targets):
    # Warm-up phase
    for _ in lis[::-1]:
        search_func(lis, _)

    times = []

    for _ in range(RUNS):
        gc.disable()  # Stop GC from running during the timed loop
        gc.collect()

        start = time.perf_counter()
        for x in targets:
            search_func(lis, x)
        end = time.perf_counter()
        
        gc.enable() # Re-enable after timing is done
        
        total_calls = len(targets)
        times.append((end - start) / total_calls)

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        #"stdev": statistics.stdev(times)
    }

def main():

    global List_Size
    global Test_cases_size
    global RUNS
    global lis
    global random_targets

    List_Size = 10**6
    Test_cases_size = 10**5
    RUNS = 100
    lis = np.arange(List_Size)

    random.seed(777) 
    random_targets = [random.randint(0, List_Size + 1000) for _ in range(Test_cases_size)]

    print("Running fair benchmark...\n")

    final_qs = bench(run_quadratic_search, lis, random_targets)

    print("Average time per call (seconds)")
    print("-" * 45)
    print(f"Average {final_qs['mean']:.9f} ns")
    print(f"Median {final_qs['median']:.9f}")#, stdev {final_bs_4['stdev']:.0f} ns")

if __name__=='__main__':
    main()