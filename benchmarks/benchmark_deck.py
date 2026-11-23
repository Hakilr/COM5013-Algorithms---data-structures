"""Measure the Deck (hash map), saving, loading and CSV import at different sizes.

Run from the main repo folder:   python -m benchmarks.benchmark_deck

--large adds 1,000,000 cards. That needs several GB of memory and a few minutes,
and the save file is hundreds of MB, so close other programs first.
"""

import csv
import random
import tempfile
from pathlib import Path

from benchmarks.common import (LARGE, choose_sizes, format_seconds, make_cards, make_deck,
                               measure, report, start_report)
from src.deck import Deck
from src.importer import import_cards_from_csv
from src.storage import load_deck, save_deck

NAME = "deck"
SIZES = choose_sizes([1_000, 10_000, 100_000])
LOOKUPS = 10_000


def write_csv(cards, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["topic", "subtopic", "question", "answer", "difficulty"])
        for card in cards:
            writer.writerow([card.topic, card.subtopic, card.question, card.answer, card.difficulty])


def main():
    start_report(NAME, "Deck, storage and import benchmark")
    if LARGE:
        print("Large mode: this will take several minutes and use a lot of memory.\n")

    rows = []
    with tempfile.TemporaryDirectory() as folder:
        for n in SIZES:
            print(f"Running n = {n:,} ...")
            cards = make_cards(n)
            repeat = 3 if n <= 10_000 else 1

            def build():
                deck = Deck()
                for card in cards:
                    deck.add_card(card)

            build_time = measure(build, repeat=repeat)

            deck = make_deck(cards)
            rng = random.Random(n)
            ids = [rng.randint(1, n) for _ in range(LOOKUPS)]
            lookup_time = measure(lambda: [deck.get_card(i) for i in ids], repeat=3) / LOOKUPS

            save_path = Path(folder) / "deck.json"
            save_time = measure(lambda: save_deck(deck, save_path), repeat=1)
            size_mb = save_path.stat().st_size / 1_048_576
            load_time = measure(lambda: load_deck(save_path), repeat=1)

            csv_path = Path(folder) / "cards.csv"
            write_csv(cards, csv_path)
            added = []
            import_time = measure(lambda: added.append(import_cards_from_csv(Deck(), csv_path).added),
                                  repeat=1)
            rate = added[-1] / import_time

            rows.append([f"{n:,}", format_seconds(build_time), format_seconds(lookup_time),
                         format_seconds(save_time), f"{size_mb:.1f} MB", format_seconds(load_time),
                         format_seconds(import_time), f"{rate:,.0f}/s"])

    report(NAME, "Timings by deck size",
           ["Cards", f"Add all cards", "One lookup (avg)", "Save JSON", "File size", "Load JSON",
            "Import CSV", "Import rate"],
           rows,
           f"A lookup is the average over {LOOKUPS:,} random IDs. The hash map should keep lookup time "
           "about the same however large the deck gets (O(1) on average), while saving, loading and "
           "importing grow in step with n (O(n)). Save and load include validation of every card.")


if __name__ == "__main__":
    main()
