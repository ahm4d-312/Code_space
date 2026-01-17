import time
import random
import statistics
import gc

# ============================
# CONFIG
# ============================
N = 10**5        # Array size
NUM_TESTS = 10_000
RUNS = 50
INNER = 5
WARMUP = 5

# ============================
# DATA SETUP
# ============================
arr = list(range(N))

# Generate identical random targets for both algorithms
random_targets = [random.randint(0, N + 1000) for _ in range(NUM_TESTS)]

# ============================
# ADD YOUR ALGORITHMS HERE
# ============================
def binary_search(lis, target):
    low, top = 0, len(lis) - 1
    while low <= top:
        mid = (top + low) // 2  # // stores the result as int, same result as floor of normal division.
        if lis[mid] == target:
            return mid
        if lis[mid] >= target:
            top = mid - 1
        else:
            low = mid + 1
    return -1

def binary_search_4(lis, n):
    left,top=0, len(lis)-1
    mid_1=(top+1)//4
    mid_2=mid_1*2
    mid_3=mid_1*3
    if n==lis[0]:
        return 0
    elif n < lis[mid_1]:
        top=mid_1-1
    elif n < lis[mid_2]:
        left,top=mid_1,mid_2-1
    elif n < lis[mid_3]:
        left,top=mid_2,mid_3-1
    elif n<lis[top]:
        left=mid_3
    elif n==lis[top]:
        return top
    while left <= top:
        mid = (top + left) // 2  
        if lis[mid] == n:
            return mid
        if lis[mid] >= n:
            top = mid - 1
        else:
            left = mid + 1
    return -1

def binary_search_3(lis, n):
    left,top=0, len(lis)-1
    mid_1=(top+1)//3
    mid_2=mid_1*2
    if n==lis[0]:
        return 0
    elif n < lis[mid_1]:
        top=mid_1-1
    elif n < lis[mid_2]:
        left,top=mid_1,mid_2-1
    elif n < lis[top]:
        left=mid_2
    elif n==lis[top]:
        return top
    while left <= top:
        mid = (top + left) // 2  
        if lis[mid] == n:
            return mid
        if lis[mid] >= n:
            top = mid - 1
        else:
            left = mid + 1
    return -1

# ============================
# WRAPPERS (keep overhead equal)
# ============================
def run_binary_search_4(data, x):
    return binary_search_4(data, x)

def run_binary_search_3(data, x):
    return binary_search_3(data, x)

def run_binary_search(data, x):
    return binary_search(data, x)




# ============================
# BENCHMARK FUNCTION
# ============================
def bench(search_func, data, targets):
    # Warm-up phase
    for _ in range(WARMUP):
        for x in targets:
            search_func(data, x)

    gc.collect()

    times = []
        

    for _ in range(RUNS):
        start = time.perf_counter()
        for _ in range(INNER):
            for x in targets:
                search_func(data, x)
        end = time.perf_counter()
        times.append((end - start) / INNER)

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times)
    }

# ============================
# RUN BENCHMARKS (ORDER SWAP)
# ============================
print("\nRunning fair benchmark...\n")

# First order
result_bs_1  = bench(run_binary_search, arr, random_targets)
result_bsp_1 = bench(run_binary_search_4, arr, random_targets)
result_bsp_2 = bench(run_binary_search_3, arr, random_targets)
# Second order (swap to avoid bias)
result_bsp_2 = bench(run_binary_search_4, arr, random_targets)
result_bs_2  = bench(run_binary_search, arr, random_targets)
result_bs_3  = bench(run_binary_search_3, arr, random_targets)
# ============================
# AVERAGE BOTH RUNS
# ============================
def avg_results(r1, r2):
    return {
        "mean":   (r1["mean"]   + r2["mean"])   / 2,
        "median": (r1["median"] + r2["median"]) / 2,
        "stdev":  (r1["stdev"]  + r2["stdev"])  / 2
    }

final_bs  = avg_results(result_bs_1,  result_bs_2)
final_bsp = avg_results(result_bsp_1, result_bsp_2)
final_bsp1=avg_results(result_bsp_2,result_bs_3)

# ============================
# PRINT RESULTS
# ============================
print("Average time per call (seconds)")
print("-" * 45)

print(f"binary_search      : {final_bs['mean']:.9f}")
print(f"binary_search_4 : {final_bsp['mean']:.9f}")
print(f"binary_search_3 : {final_bsp1['mean']:.9f}")

print(f"\nbinary_search      : median {final_bs['median']:.9f}, stdev {final_bs['stdev']:.9f}")
print(f"binary_search_4 : median {final_bsp['median']:.9f}, stdev {final_bsp['stdev']:.9f}")
print(f"binary_search_3 : median {final_bsp1['median']:.9f}, stdev {final_bsp1['stdev']:.9f}")
