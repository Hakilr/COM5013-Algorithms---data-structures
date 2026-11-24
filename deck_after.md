# Deck, storage and import benchmark

Run on 2026-11-24. Python 3.13.7 on Windows 10 (AMD64).
Mode: standard. Each time is the best of several runs unless marked otherwise.

## Timings by deck size

| Cards | Add all cards | One lookup (avg) | Save JSON | File size | Load JSON | Import CSV | Import rate |
|---|---|---|---|---|---|---|---|
| 1,000 | 659.7 µs | 348 ns | 83.85 ms | 0.4 MB | 17.98 ms | 23.69 ms | 42,206/s |
| 10,000 | 5.04 ms | 228 ns | 284.02 ms | 3.9 MB | 78.40 ms | 106.94 ms | 93,507/s |
| 100,000 | 40.33 ms | 313 ns | 2.88 s | 39.2 MB | 958.98 ms | 1.16 s | 86,477/s |

A lookup is the average over 10,000 random IDs. The hash map should keep lookup time about the same however large the deck gets (O(1) on average), while saving, loading and importing grow in step with n (O(n)).
