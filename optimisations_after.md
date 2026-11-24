# Optimisation benchmark

Run on 2026-11-24. Python 3.13.7 on Windows 10 (AMD64).
Mode: standard. Each time is the best of several runs unless marked otherwise.

## Adding n cards one at a time: rescan for the largest ID vs a running counter

| Cards added | Rescan every time (O(n) per add) | Running counter (O(1) per add) | Speed-up |
|---|---|---|---|
| 1,000 | 51.58 ms | 1.47 ms | 35x |
| 5,000 | 921.80 ms | 4.91 ms | 188x |
| 20,000 | 16.88 s | 24.10 ms | 700x |

Rescanning makes adding n cards O(n squared) overall. When n grows by 4 times (5,000 to 20,000), the rescan time should grow by about 16 times, while the counter's grows by about 4 times.

## Converting every card to a dictionary: dataclasses.asdict vs Card.to_dict (current code)

| Cards | asdict (original) | Card.to_dict (current) | Speed-up |
|---|---|---|---|
| 1,000 | 6.39 ms | 1.04 ms | 6.1x |
| 10,000 | 67.21 ms | 14.86 ms | 4.5x |
| 100,000 | 572.89 ms | 145.62 ms | 3.9x |

If Card.to_dict still uses asdict, the speed-up will be about 1x. After the change it should be about 3 to 4x.

## Where the time goes when saving

| Cards | Card.to_dict for every card | json.dump (writing the file) | save_deck (total) | Share spent in to_dict |
|---|---|---|---|---|
| 1,000 | 1.04 ms | 23.14 ms | 23.91 ms | 4% |
| 10,000 | 14.86 ms | 226.51 ms | 248.14 ms | 6% |
| 100,000 | 145.62 ms | 2.44 s | 2.64 s | 6% |

Writing the JSON is the larger part of a save, so speeding up to_dict improves the total by less than its own speed-up suggests.
