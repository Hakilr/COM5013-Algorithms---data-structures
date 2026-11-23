"""Compare trie search with a linear scan, and measure the trie's cost.

Run from the main repo folder:   python -m benchmarks.benchmark_search
"""

import tracemalloc

from benchmarks.common import (choose_sizes, format_seconds, make_cards, make_deck,
                               measure, report, start_report)
from src.trie_index import TrieIndex, tokenize

NAME = "search"
SIZES = choose_sizes([1_000, 10_000, 100_000])
MEMORY_LIMIT = 100_000   # tracemalloc slows code down a lot, so skip it above this size
PREFIXES = ["mito", "resp", "enz", "chlor", "photo", "pathog"]


def card_text(card):
    return f"{card.topic} {card.subtopic} {card.question} {card.answer}"


def linear_scan(cards, prefix):
    """The simple alternative: look at every card's words on every search. O(n)."""
    return [card.card_id for card in cards
            if any(word.startswith(prefix) for word in tokenize(card_text(card)))]


def main():
    start_report(NAME, "Search benchmark: trie vs linear scan")
    rows = []
    for n in SIZES:
        cards = make_cards(n)
        deck = make_deck(cards)

        repeat = 3 if n <= 10_000 else 1
        build_time = measure(lambda: TrieIndex.from_deck(deck), repeat=repeat)
        index = TrieIndex.from_deck(deck)

        if n <= MEMORY_LIMIT:
            tracemalloc.start()
            before = tracemalloc.get_traced_memory()[0]
            kept = TrieIndex.from_deck(deck)   # keep a reference, or Python frees it before we measure
            after = tracemalloc.get_traced_memory()[0]
            tracemalloc.stop()
            del kept
            memory = f"{(after - before) / 1_048_576:.1f} MB"
        else:
            memory = "not measured"

        trie_time = measure(lambda: [index.search(p) for p in PREFIXES], repeat=3) / len(PREFIXES)
        scan_time = measure(lambda: [linear_scan(cards, p) for p in PREFIXES], repeat=repeat) / len(PREFIXES)

        if n <= 100_000:   # sanity check: both methods must give the same answers
            for prefix in PREFIXES:
                assert index.search(prefix) == linear_scan(cards, prefix), prefix

        rows.append([f"{n:,}", format_seconds(build_time), f"{index.node_count():,}", memory,
                     format_seconds(trie_time), format_seconds(scan_time),
                     f"{scan_time / trie_time:,.0f}x"])

    report(NAME, "Prefix search, average time per query",
           ["Cards", "Build trie", "Trie nodes", "Trie memory", "Trie query", "Linear scan", "Speed-up"],
           rows,
           f"Queries used: {', '.join(PREFIXES)}. The trie finds the same cards as the linear scan "
           "(checked automatically). Memory is the extra memory used by the index, measured with tracemalloc. "
           "A query costs O(p + s + k): p is the length of the prefix, s the trie nodes below it and k the number "
           "of matching cards. These queries match a fixed share of the deck, so k grows with n and the query "
           "time grows too. The trie's advantage over a linear scan is therefore a roughly constant factor here, "
           "and it would be larger for queries that match few cards. Memory is dominated by storing each card's "
           "ID once per word it contains, plus a word set per card, so it grows with n times words per card. The "
           "node count stays small because the cards share about 75 distinct words.")


if __name__ == "__main__":
    main()
