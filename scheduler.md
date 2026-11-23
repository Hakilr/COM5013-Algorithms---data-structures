# Scheduler benchmark: choosing a data structure

Run on 2026-11-22. Python 3.13.7 on Windows 10 (AMD64).
Mode: standard. Each time is the best of several runs unless marked otherwise.

## 1,000 revision cycles (pop the most urgent card, then reschedule it)

| Cards | own MinHeap | heapq (reference) | sorted list | unsorted list |
|---|---|---|---|---|
| 1,000 | 4.05 ms | 646.9 µs | 847.2 µs | 20.05 ms |
| 10,000 | 2.90 ms | 734.1 µs | 2.95 ms | 184.23 ms |
| 100,000 | 6.33 ms | 1.15 ms | 36.95 ms | 2.21 s |

Do not be surprised if the sorted list is competitive at small sizes: its inserting and shifting run in C, while the heap is written in Python. The point is how each grows as n grows. The heap's cost grows with log n, the sorted list's with n, and the unsorted list pays O(n) on every pop. Say what you actually measured, and why.

## Building a schedule from n cards

| Cards | n pushes (O(n log n)) | MinHeap(values), heapify (O(n)) | sorted(values) (O(n log n)) |
|---|---|---|---|
| 1,000 | 1.09 ms | 702.1 µs | 99.3 µs |
| 10,000 | 6.16 ms | 4.44 ms | 1.30 ms |
| 100,000 | 92.78 ms | 60.29 ms | 20.55 ms |

Bottom-up heapify should be faster than pushing the items one at a time.
