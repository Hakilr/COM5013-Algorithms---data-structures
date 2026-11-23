# Scheduler benchmark: choosing a data structure

Run on 2026-11-23. Python 3.13.7 on Windows 10 (AMD64).
Mode: large. Each time is the best of several runs unless marked otherwise.

## 1,000 revision cycles (pop the most urgent card, then reschedule it)

| Cards | own MinHeap | heapq (reference) | sorted list | unsorted list |
|---|---|---|---|---|
| 1,000 | 9.16 ms | 483.0 µs | 1.01 ms | 24.57 ms |
| 10,000 | 8.82 ms | 816.1 µs | 4.11 ms | 245.78 ms |
| 100,000 | 14.01 ms | 1.33 ms | 65.28 ms | 2.64 s |
| 1,000,000 | 13.77 ms | 2.43 ms | 1.65 s | skipped |

Do not be surprised if the sorted list is competitive at small sizes: its inserting and shifting run in C, while the heap is written in Python. The point is how each grows as n grows. The heap's cost grows with log n, the sorted list's with n, and the unsorted list pays O(n) on every pop. Say what you actually measured, and why.

## Building a schedule from n cards

| Cards | n pushes (O(n log n)) | MinHeap(values), heapify (O(n)) | sorted(values) (O(n log n)) |
|---|---|---|---|
| 1,000 | 514.4 µs | 328.2 µs | 118.4 µs |
| 10,000 | 12.31 ms | 13.46 ms | 2.70 ms |
| 100,000 | 148.01 ms | 80.74 ms | 23.50 ms |
| 1,000,000 | 1.25 s | 786.88 ms | 381.49 ms |

Bottom-up heapify should be faster than pushing the items one at a time.
