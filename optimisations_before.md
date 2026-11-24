# Optimisation benchmark

Run on 2026-11-24. Python 3.13.7 on Windows 10 (AMD64).
Mode: standard. Each time is the best of several runs unless marked otherwise.

## Adding n cards one at a time: rescan for the largest ID vs a running counter

| Cards added | Rescan every time (O(n) per add) | Running counter (O(1) per add) | Speed-up |
|---|---|---|---|
| 1,000 | 42.57 ms | 842.2 µs | 51x |
| 5,000 | 1.06 s | 5.03 ms | 212x |
| 20,000 | 16.83 s | 25.88 ms | 650x |

Rescanning makes adding n cards O(n squared) overall. When n grows by 4 times (5,000 to 20,000), the rescan time should grow by about 16 times, while the counter's grows by about 4 times.

## Converting every card to a dictionary: dataclasses.asdict vs Card.to_dict (current code)

| Cards | asdict (original) | Card.to_dict (current) | Speed-up |
|---|---|---|---|
| 1,000 | 3.92 ms | 4.05 ms | 1.0x |
| 10,000 | 50.98 ms | 43.12 ms | 1.2x |
| 100,000 | 651.71 ms | 658.41 ms | 1.0x |

If Card.to_dict still uses asdict, the speed-up will be about 1x. After the change it should be about 3 to 4x.

## Where the time goes when saving

| Cards | Card.to_dict for every card | json.dump (writing the file) | save_deck (total) | Share spent in to_dict |
|---|---|---|---|---|
| 1,000 | 4.05 ms | 19.92 ms | 27.68 ms | 15% |
| 10,000 | 43.12 ms | 223.61 ms | 294.17 ms | 15% |
| 100,000 | 658.41 ms | 2.40 s | 2.97 s | 22% |

Writing the JSON is the larger part of a save, so speeding up to_dict improves the total by less than its own speed-up suggests.
