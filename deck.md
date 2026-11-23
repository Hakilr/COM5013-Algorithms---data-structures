# Deck, storage and import benchmark

Run on 2026-11-23. Python 3.13.7 on Windows 10 (AMD64).
Mode: standard. Each time is the best of several runs unless marked otherwise.

## Timings by deck size

| Cards | Add all cards | One lookup (avg) | Save JSON | File size | Load JSON | Import CSV | Import rate |
|---|---|---|---|---|---|---|---|
| 1,000 | 140.7 µs | 209 ns | 43.02 ms | 0.4 MB | 18.83 ms | 27.05 ms | 36,974/s |
| 10,000 | 2.07 ms | 157 ns | 402.33 ms | 3.9 MB | 101.58 ms | 149.28 ms | 66,989/s |
| 100,000 | 34.70 ms | 430 ns | 4.19 s | 39.2 MB | 985.89 ms | 1.30 s | 76,826/s |

A lookup is the average over 10,000 random IDs. The hash map should keep lookup time about the same however large the deck gets (O(1) on average), while saving, loading and importing grow in step with n (O(n)). Save and load include validation of every card.
