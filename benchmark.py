"""
benchmark.py
MSCS 532 Assignment 4
Frenie Labrador

Empirical comparison of Heapsort against Merge Sort and randomized
Quicksort on random, sorted, and reverse-sorted inputs.

Randomized quicksort is used instead of last-element-pivot quicksort
because the deterministic version degrades to O(n^2) and blows the
recursion limit on sorted input (already observed in Assignments 2
and 3). Each measurement is the average of 3 runs on fresh copies.

Output: benchmark_results.csv
"""

import csv
import random
import time

from heapsort import heapsort


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def quicksort(arr):
    """Randomized quicksort, iterative on the larger side to keep the
    recursion shallow."""
    def sort(lo, hi):
        while lo < hi:
            p = random.randint(lo, hi)
            arr[p], arr[hi] = arr[hi], arr[p]
            pivot = arr[hi]
            i = lo - 1
            for j in range(lo, hi):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
            p = i + 1
            if p - lo < hi - p:
                sort(lo, p - 1)
                lo = p + 1
            else:
                sort(p + 1, hi)
                hi = p - 1
    sort(0, len(arr) - 1)
    return arr


def make_input(n, dist):
    if dist == "random":
        return [random.randint(0, 10 * n) for _ in range(n)]
    if dist == "sorted":
        return list(range(n))
    if dist == "reverse":
        return list(range(n, 0, -1))
    raise ValueError(dist)


def time_sort(fn, data, runs=3):
    total = 0.0
    for _ in range(runs):
        copy = list(data)
        t0 = time.perf_counter()
        fn(copy)
        total += time.perf_counter() - t0
    return total / runs


def main():
    random.seed(42)
    sizes = [1000, 5000, 10000, 50000, 100000]
    dists = ["random", "sorted", "reverse"]
    algos = [("heapsort", heapsort),
             ("mergesort", merge_sort),
             ("quicksort", quicksort)]

    rows = []
    for dist in dists:
        for n in sizes:
            data = make_input(n, dist)
            for name, fn in algos:
                t = time_sort(fn, data)
                rows.append({"algorithm": name, "distribution": dist,
                             "n": n, "avg_seconds": round(t, 6)})
                print(f"{name:>9} | {dist:>7} | n={n:>6} | {t:.6f}s")

    with open("benchmark_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["algorithm", "distribution",
                                          "n", "avg_seconds"])
        w.writeheader()
        w.writerows(rows)
    print("\nSaved benchmark_results.csv")


if __name__ == "__main__":
    main()
