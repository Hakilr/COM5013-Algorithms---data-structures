# Sorting benchmark

Run on 2026-11-23. Python 3.13.7 on Windows 10 (AMD64).
Mode: large. Each time is the best of several runs unless marked otherwise.

## Random data (average case)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 685.0 µs | 252.6 µs | 5.4 µs |
| 1,000 | 190.94 ms | 7.54 ms | 201.4 µs |
| 5,000 | 5.50 s | 29.73 ms | 683.2 µs |
| 10,000 | skipped | 103.78 ms | 2.47 ms |
| 100,000 | skipped | 1.15 s | 25.62 ms |
| 1,000,000 | skipped | 13.84 s | 374.41 ms |

## Already sorted (best case)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 36.6 µs | 376.2 µs | 1.4 µs |
| 1,000 | 203.4 µs | 2.50 ms | 16.6 µs |
| 5,000 | 795.6 µs | 26.32 ms | 37.1 µs |
| 10,000 | skipped | 52.92 ms | 106.7 µs |
| 100,000 | skipped | 707.82 ms | 4.18 ms |
| 1,000,000 | skipped | 9.31 s | 87.71 ms |

## Reverse sorted (worst case)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 1.12 ms | 418.2 µs | 1.4 µs |
| 1,000 | 251.41 ms | 3.61 ms | 7.7 µs |
| 5,000 | 6.70 s | 28.56 ms | 45.9 µs |
| 10,000 | skipped | 82.89 ms | 282.3 µs |
| 100,000 | skipped | 898.46 ms | 4.54 ms |
| 1,000,000 | skipped | 23.66 s | 161.28 ms |

## Only three distinct values (like difficulty)

| n | bubble sort | merge sort | sorted() (reference) |
|---|---|---|---|
| 100 | 3.50 ms | 662.5 µs | 5.1 µs |
| 1,000 | 451.01 ms | 10.07 ms | 126.9 µs |
| 5,000 | 12.09 s | 92.43 ms | 429.6 µs |
| 10,000 | skipped | 171.77 ms | 1.87 ms |
| 100,000 | skipped | 2.66 s | 17.37 ms |
| 1,000,000 | skipped | 32.66 s | 177.40 ms |

## How to read these results

| Expectation |
|---|
| Multiplying n by 10 should multiply O(n) time by about 10, O(n log n) by slightly more than 10, and O(n squared) by about 100. |
| Bubble sort should be fastest on already-sorted data (O(n) with the early exit) and slowest on reverse-sorted data. |