"""
priority_queue.py
MSCS 532 Assignment 4
Frenie Labrador

Max-heap based priority queue for task scheduling. Higher priority
number means the task runs sooner.

Design choices:
- The heap lives in a plain Python list. Index math gives parent and
  child positions directly, so no node objects or pointers are needed,
  and the array layout is cache friendly.
- A dictionary (self._index) maps task_id -> current position in the
  list. Without it, increase_key/decrease_key would need an O(n) scan
  just to find the task before doing the O(log n) fix-up.
"""


class Task:
    """One schedulable unit of work."""

    def __init__(self, task_id, priority, arrival_time=0, deadline=None):
        self.task_id = task_id
        self.priority = priority
        self.arrival_time = arrival_time
        self.deadline = deadline

    def __repr__(self):
        return (f"Task(id={self.task_id}, pri={self.priority}, "
                f"arr={self.arrival_time}, dl={self.deadline})")


class MaxPriorityQueue:
    """Binary max-heap of Task objects, keyed on task.priority."""

    def __init__(self):
        self._heap = []          # list of Task objects
        self._index = {}         # task_id -> position in self._heap

    # ---------- internal helpers ----------

    def _swap(self, i, j):
        h = self._heap
        h[i], h[j] = h[j], h[i]
        self._index[h[i].task_id] = i
        self._index[h[j].task_id] = j

    def _sift_up(self, i):
        """Move the task at i toward the root while it beats its parent.
        O(log n): at most one swap per tree level."""
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i].priority > self._heap[parent].priority:
                self._swap(i, parent)
                i = parent
            else:
                return

    def _sift_down(self, i):
        """Move the task at i toward the leaves while a child beats it.
        O(log n): at most one swap per tree level."""
        n = len(self._heap)
        while True:
            left, right, largest = 2 * i + 1, 2 * i + 2, i
            if left < n and self._heap[left].priority > self._heap[largest].priority:
                largest = left
            if right < n and self._heap[right].priority > self._heap[largest].priority:
                largest = right
            if largest == i:
                return
            self._swap(i, largest)
            i = largest

    # ---------- core operations ----------

    def insert(self, task):
        """Append the task at the end of the list, then sift it up.
        Time: O(log n). The append is amortized O(1) and the sift-up
        walks at most the height of the tree."""
        if task.task_id in self._index:
            raise ValueError(f"task_id {task.task_id} already in queue")
        self._heap.append(task)
        self._index[task.task_id] = len(self._heap) - 1
        self._sift_up(len(self._heap) - 1)

    def peek_max(self):
        """Return the highest priority task without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("priority queue is empty")
        return self._heap[0]

    def extract_max(self):
        """Remove and return the highest priority task.
        Swap root with the last element, pop it, then sift the new root
        down. Time: O(log n), dominated by the sift-down."""
        if self.is_empty():
            raise IndexError("priority queue is empty")
        top = self._heap[0]
        last = self._heap.pop()
        del self._index[top.task_id]
        if self._heap:
            self._heap[0] = last
            self._index[last.task_id] = 0
            self._sift_down(0)
        return top

    def increase_key(self, task_id, new_priority):
        """Raise a task's priority and sift it up. O(log n) total:
        O(1) lookup through the index map, then O(log n) sift-up."""
        i = self._index[task_id]
        if new_priority < self._heap[i].priority:
            raise ValueError("new priority is lower, use decrease_key")
        self._heap[i].priority = new_priority
        self._sift_up(i)

    def decrease_key(self, task_id, new_priority):
        """Lower a task's priority and sift it down. O(log n)."""
        i = self._index[task_id]
        if new_priority > self._heap[i].priority:
            raise ValueError("new priority is higher, use increase_key")
        self._heap[i].priority = new_priority
        self._sift_down(i)

    def is_empty(self):
        """O(1)."""
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)


if __name__ == "__main__":
    # quick self-test
    pq = MaxPriorityQueue()
    assert pq.is_empty()

    for tid, pri in [(1, 5), (2, 9), (3, 1), (4, 7), (5, 3)]:
        pq.insert(Task(tid, pri, arrival_time=tid))

    assert pq.peek_max().task_id == 2

    pq.increase_key(3, 20)          # task 3 jumps to the front
    assert pq.peek_max().task_id == 3

    pq.decrease_key(3, 0)           # and drops back down
    assert pq.peek_max().task_id == 2

    order = [pq.extract_max().task_id for _ in range(len(pq))]
    assert order == [2, 4, 1, 5, 3], order
    assert pq.is_empty()

    # duplicate id should raise
    pq.insert(Task(9, 1))
    try:
        pq.insert(Task(9, 2))
        raise AssertionError("duplicate id not caught")
    except ValueError:
        pass

    print("All priority queue tests passed.")
