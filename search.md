# Search benchmark: trie vs linear scan

Run on 2026-11-22. Python 3.13.7 on Windows 10 (AMD64).
Mode: standard. Each time is the best of several runs unless marked otherwise.

## Prefix search, average time per query

| Cards | Build trie | Trie nodes | Trie memory | Trie query | Linear scan | Speed-up |
|---|---|---|---|---|---|---|
| 1,000 | 78.56 ms | 585 | 3.7 MB | 23.5 µs | 10.54 ms | 449x |
| 10,000 | 748.78 ms | 585 | 36.9 MB | 193.4 µs | 103.11 ms | 533x |
| 100,000 | 7.58 s | 585 | 325.9 MB | 2.65 ms | 1.08 s | 407x |

Queries used: mito, resp, enz, chlor, photo, pathog. The trie finds the same cards as the linear scan (checked automatically). Memory is the extra memory used by the index, measured with tracemalloc. A query costs O(p + s + k): p is the length of the prefix, s the trie nodes below it and k the number of matching cards. These queries match a fixed share of the deck, so k grows with n and the query time grows too. The trie's advantage over a linear scan is therefore a roughly constant factor here, and it would be larger for queries that match few cards. Memory is dominated by storing each card's ID once per word it contains, plus a word set per card, so it grows with n times words per card. The node count stays small because the cards share about 75 distinct words.
