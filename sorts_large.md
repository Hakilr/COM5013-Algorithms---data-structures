# Sorting benchmark

Run on 2026-11-23. Python 3.13.7 on Windows 10 (AMD64).
Mode: large. Each time is the best of several runs unless marked otherwise.

## Random data (average case)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 777.0 µs | 587.0 µs | 5.8 µs |
| 1,000 | 212.20 ms | 8.84 ms | 179.7 µs |
| 5,000 | 5.88 s | 33.22 ms | 747.2 µs |
| 10,000 | skipped | 103.41 ms | 1.67 ms |
| 100,000 | skipped | 1.26 s | 72.55 ms |
| 1,000,000 | skipped | 41.37 s | 881.76 ms |

## Already sorted (best case)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 24.4 µs | 390.0 µs | 2.7 µs |
| 1,000 | 209.3 µs | 10.06 ms | 14.9 µs |
| 5,000 | 1.50 ms | 46.67 ms | 172.1 µs |
| 10,000 | skipped | 168.36 ms | 554.1 µs |
| 100,000 | skipped | 2.10 s | 11.47 ms |
| 1,000,000 | skipped | 24.91 s | 138.32 ms |

## Reverse sorted (worst case)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 7.20 ms | 1.22 ms | 6.5 µs |
| 1,000 | 615.11 ms | 11.74 ms | 35.4 µs |
| 5,000 | 8.46 s | 60.15 ms | 153.1 µs |
| 10,000 | skipped | 179.63 ms | 504.3 µs |
| 100,000 | skipped | 1.81 s | 11.59 ms |
| 1,000,000 | skipped | 15.89 s | 109.74 ms |

## Only three distinct values (like difficulty)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 2.46 ms | 555.3 µs | 4.7 µs |
| 1,000 | 173.43 ms | 6.42 ms | 59.7 µs |
| 5,000 | 4.65 s | 29.86 ms | 501.2 µs |
| 10,000 | skipped | 85.53 ms | 1.09 ms |
| 100,000 | skipped | 1.17 s | 8.78 ms |
| 1,000,000 | skipped | 23.35 s | 200.49 ms |

## How to read these results

| Expectation |
|---|
| Multiplying n by 10 should multiply O(n) time by about 10, O(n log n) by slightly more than 10, and O(n squared) by about 100. |
| Bubble sort should be fastest on already-sorted data (O(n) with the early exit) and slowest on reverse-sorted data. |
