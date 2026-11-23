"""Compare data structures for scheduling: own MinHeap, heapq, sorted list, unsorted list.

Run from the main repo folder:   python -m benchmarks.benchmark_scheduler

Workload: a revision session repeatedly takes the most urgent card out and puts
it back with a new due time, so each cycle is one "pop smallest" and one "push".
"""

import bisect
import heapq
import random

from benchmarks.common import choose_sizes, format_seconds, measure, report, start_report
from src.heap import MinHeap

NAME = "scheduler"
SIZES = choose_sizes([1_000, 10_000, 100_000])
CYCLES = 1_000


class OwnHeap:
    def __init__(self, values):
        self._heap = MinHeap(values)

    def push(self, value):
        self._heap.push(value)

    def pop_min(self):
        return self._heap.pop()


class StdlibHeap:
    def __init__(self, values):
        self._items = list(values)
        heapq.heapify(self._items)

    def push(self, value):
        heapq.heappush(self._items, value)

    def pop_min(self):
        return heapq.heappop(self._items)


class SortedList:
    def __init__(self, values):
        self._items = sorted(values)

    def push(self, value):
        bisect.insort(self._items, value)    # finding the place is O(log n), shifting is O(n)

    def pop_min(self):
        return self._items.pop(0)            # shifts every other item: O(n)


class UnsortedList:
    def __init__(self, values):
        self._items = list(values)

    def push(self, value):
        self._items.append(value)            # O(1)

    def pop_min(self):
        smallest = min(self._items)          # O(n)
        self._items.remove(smallest)         # O(n)
        return smallest


# name -> (class, largest size to run)
STRUCTURES = {
    "own MinHeap": (OwnHeap, 1_000_000),
    "heapq (reference)": (StdlibHeap, 1_000_000),
    "sorted list": (SortedList, 1_000_000),
    "unsorted list": (UnsortedList, 100_000),
}


def main():
    start_report(NAME, "Scheduler benchmark: choosing a data structure")

    cycle_rows = []
    build_rows = []
    for n in SIZES:
        rng = random.Random(n)
        initial = [rng.uniform(0, 1_000_000) for _ in range(n)]
        new_values = [rng.uniform(0, 2_000_000) for _ in range(CYCLES)]

        row = [f"{n:,}"]
        for cls, largest in STRUCTURES.values():
            if n > largest:
                row.append("skipped")
                continue

            def run(structure):
                for value in new_values:
                    structure.pop_min()
                    structure.push(value)

            seconds = measure(run, setup=lambda: cls(initial), repeat=3 if n <= 10_000 else 1)
            row.append(format_seconds(seconds))
        cycle_rows.append(row)

        def push_all():
            heap = MinHeap()
            for value in initial:
                heap.push(value)

        build_rows.append([
            f"{n:,}",
            format_seconds(measure(push_all, repeat=3 if n <= 10_000 else 1)),
            format_seconds(measure(lambda: MinHeap(initial), repeat=3 if n <= 10_000 else 1)),
            format_seconds(measure(lambda: sorted(initial), repeat=3 if n <= 10_000 else 1)),
        ])

    report(NAME, f"{CYCLES:,} revision cycles (pop the most urgent card, then reschedule it)",
           ["Cards"] + list(STRUCTURES), cycle_rows,
           "Do not be surprised if the sorted list is competitive at small sizes: its inserting and shifting "
           "run in C, while the heap is written in Python. The point is how each grows as n grows. The "
           "heap's cost grows with log n, the sorted list's with n, and the unsorted list pays O(n) on every "
           "pop. Say what you actually measured, and why.")
    report(NAME, "Building a schedule from n cards",
           ["Cards", "n pushes (O(n log n))", "MinHeap(values), heapify (O(n))", "sorted(values) (O(n log n))"],
           build_rows,
           "Bottom-up heapify should be faster than pushing the items one at a time.")


if __name__ == "__main__":
    main()
