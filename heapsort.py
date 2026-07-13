"""
heapsort.py
MSCS 532 Assignment 4
Frenie Labrador

Heapsort implementation using a max-heap stored in a plain Python list.
The heap is built in place, then the max is repeatedly swapped to the
end of the array while the heap region shrinks.

Index math for a 0-based array:
    parent(i) = (i - 1) // 2
    left(i)   = 2 * i + 1
    right(i)  = 2 * i + 2
"""


def max_heapify(arr, n, i):
    """Sift the value at index i down until the subtree rooted at i
    satisfies the max-heap property. n is the size of the heap region,
    which can be smaller than len(arr) during the sorting phase.

    Time complexity: O(log n) because in the worst case the value
    travels from the root to a leaf, and the tree height is floor(log2 n).
    """
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest == i:
            return
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def build_max_heap(arr):
    """Turn an arbitrary list into a max-heap in place.

    Starts from the last non-leaf node (index n//2 - 1) and heapifies
    upward toward the root. Even though each heapify call is O(log n),
    the total work sums to O(n) because most nodes sit near the bottom
    of the tree where subtree heights are small.
    """
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)


def heapsort(arr):
    """Sort arr in ascending order, in place.

    Phase 1: build a max-heap, O(n).
    Phase 2: n - 1 times, swap the root (current maximum) with the last
    element of the heap region, shrink the region by one, and heapify
    the new root back down. Each heapify is O(log n), so this phase is
    O(n log n) and dominates.

    Total: O(n log n) in the best, average, and worst case.
    Space: O(1) extra, everything happens inside the input list.
    """
    build_max_heap(arr)
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        max_heapify(arr, end, 0)
    return arr


if __name__ == "__main__":
    import random

    tests = [
        [],
        [1],
        [2, 1],
        [5, 5, 5, 5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        list(range(10)),
        list(range(10, 0, -1)),
        [random.randint(-100, 100) for _ in range(500)],
    ]
    for t in tests:
        expected = sorted(t)
        got = heapsort(list(t))
        assert got == expected, f"FAIL on {t[:10]}..."
    print("All heapsort tests passed.")
