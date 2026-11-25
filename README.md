# GCSE Biology Revision Tool

A command-line Python app for revising GCSE Edexcel Biology. You add flashcards
(topic, subtopic, difficulty), search and sort them, import them in bulk from CSV,
and revise using a spaced-repetition scheduler that shows the cards you are due.

## Features
- Add, list and delete flashcards (topic, subtopic and difficulty are required)
- Sort the list by topic, subtopic or difficulty
- Fast prefix search (trie)
- Bulk import from CSV, skipping duplicates
- Revision mode: a correct answer doubles the wait before the card returns,
  and a wrong answer brings it back in 60 seconds
- Cards saved to `deck.json`

## Run the app
```
python main.py
```
To load sample cards, choose the import option and enter `biology_cards.csv`.

## Run the tests
```
python -m pytest
```
Expected: 198 passed. What each test checks and the results are in `TESTING.md`.

## Run the benchmarks
```
python -m benchmarks.benchmark_sorts --quick
python -m benchmarks.benchmark_sorts
python -m benchmarks.benchmark_sorts --large
```
The other files in `benchmarks/` (search, scheduler, deck, optimisations) run the
same way. Results are written to `benchmarks/results/`.

## Algorithms and data structures
| Where | What | Why |
|---|---|---|
| `deck.py` | Hash map (dict) | O(1) average lookup by card ID |
| `topic_tree.py` | Tree + iterative DFS | Topic > subtopic > cards |
| `trie_index.py` | Trie | Prefix search in O(p + s + k) |
| `heap.py`, `scheduler.py` | Min-heap (written from scratch) | Next due card in O(log n) |
| `sorter.py` | Bubble, merge, quick and counting sort | Compared in the benchmarks |
| `importer.py` | Hash set | O(n + m) duplicate check on import |

## Project layout
main.py        launcher
src/           application code
tests/         pytest tests
benchmarks/    timing scripts and results/
DESIGN.md      design document
TESTING.md     test evidence


## Author
Hakil Rashid 80013703
