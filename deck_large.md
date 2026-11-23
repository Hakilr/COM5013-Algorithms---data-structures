# Deck, storage and import benchmark

Run on 2026-11-23. Python 3.13.7 on Windows 10 (AMD64).
Mode: large. Each time is the best of several runs unless marked otherwise.

## Timings by deck size

| Cards | Add all cards | One lookup (avg) | Save JSON | File size | Load JSON | Import CSV | Import rate |
|---|---|---|---|---|---|---|---|
| 1,000 | 569.2 µs | 167 ns | 39.26 ms | 0.4 MB | 33.78 ms | 36.69 ms | 27,256/s |
| 10,000 | 5.32 ms | 349 ns | 493.38 ms | 3.9 MB | 112.58 ms | 276.69 ms | 36,142/s |
| 100,000 | 33.26 ms | 641 ns | 4.66 s | 39.2 MB | 1.17 s | 1.70 s | 58,867/s |
| 1,000,000 | 1.03 s | 850 ns | 57.61 s | 392.7 MB | 12.11 s | 41.24 s | 24,250/s |

A lookup is the average over 10,000 random IDs. The hash map should keep lookup time about the same however large the deck gets (O(1) on average), while saving, loading and importing grow in step with n (O(n)). Save and load include validation of every card.
