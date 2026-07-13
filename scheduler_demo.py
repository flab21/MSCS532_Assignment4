"""
scheduler_demo.py
MSCS 532 Assignment 4
Frenie Labrador

Small priority scheduler simulation built on MaxPriorityQueue.

Model: tasks arrive at different times with a priority and a service
time. At each tick, any newly arrived tasks are inserted, then the CPU
runs the highest priority task that is waiting. This is non-preemptive:
once a task starts it runs to completion. One mid-run priority boost is
included to show increase_key doing real work.
"""

from priority_queue import Task, MaxPriorityQueue


def run_simulation():
    # (task_id, priority, arrival_time, service_time)
    incoming = [
        (1, 3, 0, 4),
        (2, 5, 1, 3),
        (3, 1, 2, 2),
        (4, 8, 3, 1),
        (5, 2, 4, 3),
        (6, 6, 6, 2),
    ]
    service = {tid: s for tid, _, _, s in incoming}

    pq = MaxPriorityQueue()
    clock = 0
    pending = sorted(incoming, key=lambda t: t[2])
    completed = []
    boosted = False

    print(f"{'time':>4}  {'event'}")
    while pending or not pq.is_empty():
        # admit everything that has arrived by now
        while pending and pending[0][2] <= clock:
            tid, pri, arr, _ = pending.pop(0)
            pq.insert(Task(tid, pri, arrival_time=arr))
            print(f"{clock:>4}  task {tid} arrives (priority {pri})")

        # demonstrate increase_key: at t=4, task 3 gets boosted
        if clock == 4 and not boosted and 3 in pq._index:
            pq.increase_key(3, 10)
            boosted = True
            print(f"{clock:>4}  task 3 priority boosted to 10")

        if pq.is_empty():
            clock = pending[0][2]   # jump to next arrival
            continue

        task = pq.extract_max()
        start = clock
        clock += service[task.task_id]
        wait = start - task.arrival_time
        completed.append((task.task_id, task.priority, start, clock, wait))
        print(f"{start:>4}  task {task.task_id} runs "
              f"(pri {task.priority}), finishes at {clock}, waited {wait}")

    print("\nid  pri  start  finish  wait")
    for tid, pri, s, f, w in completed:
        print(f"{tid:>2}  {pri:>3}  {s:>5}  {f:>6}  {w:>4}")
    avg_wait = sum(c[4] for c in completed) / len(completed)
    print(f"\naverage wait time: {avg_wait:.2f} ticks")


if __name__ == "__main__":
    run_simulation()
