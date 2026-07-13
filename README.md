# MSCS 532 Assignment 4: Heap Data Structures

Frenie Labrador, University of the Cumberlands

Heapsort implementation and analysis, plus a max-heap priority queue applied to a small task scheduler simulation.

## Files

- `heapsort.py` - max_heapify, build_max_heap, and heapsort with a built-in self test
- `priority_queue.py` - Task class and MaxPriorityQueue (insert, extract_max, increase_key, decrease_key, is_empty) with a built-in self test
- `scheduler_demo.py` - non-preemptive priority scheduler simulation using the queue
- `benchmark.py` - compares heapsort, merge sort, and randomized quicksort on random, sorted, and reverse-sorted inputs (n up to 100,000), writes `benchmark_results.csv`
- `make_plots.py` - builds the three charts in `plots/` from the CSV
- `Assignment4_Report.docx` - full report with design choices, complexity analysis, and results discussion

## How to run

Python 3.10+ is enough. Matplotlib is only needed for the plots.

```
python3 heapsort.py          # runs heapsort self tests
python3 priority_queue.py    # runs priority queue self tests
python3 scheduler_demo.py    # prints the scheduling trace
python3 benchmark.py         # takes about a minute, writes the CSV
python3 make_plots.py        # writes plots/*.png
```

## Summary of findings

- Heapsort ran in O(n log n) on every distribution, confirming the theory. At n = 100,000 it took about 0.44s on random input and about 0.35s on sorted and reverse input.
- Merge sort was the fastest on sorted and reverse-sorted inputs, and randomized quicksort was the fastest on random input. Heapsort was consistently the slowest of the three by a constant factor, which matches its known weakness: the sift-down jumps around the array and gets little help from CPU caches.
- The trade-off is space and predictability. Heapsort sorts in place with O(1) extra memory and never degrades, merge sort needs O(n) extra memory, and quicksort only avoids its O(n^2) worst case here because pivots are randomized.
- All priority queue operations except is_empty and peek are O(log n). A task_id to index dictionary makes increase_key and decrease_key O(log n) instead of O(n).
