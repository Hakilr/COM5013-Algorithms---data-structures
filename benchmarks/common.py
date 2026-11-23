"""Shared helpers for the benchmark scripts.

Run any benchmark from the main repo folder, for example:

    python -m benchmarks.benchmark_sorts
    python -m benchmarks.benchmark_sorts --quick     (small sizes, to check it works)
    python -m benchmarks.benchmark_sorts --large     (adds 1,000,000 items: slow, uses a lot of memory)

Each script prints its tables and saves them to benchmarks/results/<name>.md.
"""

import platform
import random
import sys
import time
from datetime import date
from pathlib import Path

from src.card import Card
from src.deck import Deck

QUICK = "--quick" in sys.argv
LARGE = "--large" in sys.argv

RESULTS_DIR = Path(__file__).resolve().parent / "results"

TOPICS = [
    "Key concepts in biology",
    "Cells and control",
    "Genetics",
    "Natural selection and genetic modification",
    "Health, disease and the development of medicines",
    "Plant structures and their functions",
    "Animal coordination, control and homeostasis",
    "Exchange and transport in animals",
    "Ecosystems and material cycles",
]

# A limited vocabulary, like a real deck: many cards share the same words.
WORDS = (
    "mitochondria mitosis meiosis nucleus ribosome membrane chloroplast photosynthesis "
    "respiration enzyme amylase protease substrate diffusion osmosis active transport "
    "pathogen bacteria virus antibody vaccine immune neurone synapse reflex hormone insulin "
    "glucagon pancreas kidney nephron heart artery vein capillary alveoli oxygen carbon "
    "dioxide glucose starch protein lipid chromosome allele genotype phenotype dominant "
    "recessive mutation evolution selection species ecosystem producer consumer decomposer "
    "biomass nitrogen cycle habitat population competition adaptation stem cell tissue organ"
).split()


def choose_sizes(normal, quick=(100, 1_000), extra_large=(1_000_000,)):
    """Pick the list of sizes to run, based on the --quick and --large flags."""
    if QUICK:
        return list(quick)
    return list(normal) + (list(extra_large) if LARGE else [])


def make_cards(n, seed=1):
    """Build n valid cards with repeatable pseudo-random text."""
    rng = random.Random(seed)
    cards = []
    for card_id in range(1, n + 1):
        cards.append(Card(
            card_id,
            rng.choice(TOPICS),
            " ".join(rng.choices(WORDS, k=6)) + "?",
            " ".join(rng.choices(WORDS, k=8)),
            f"Subtopic {rng.randint(1, 5)}",
            rng.randint(1, 3),
        ))
    return cards


def make_deck(cards):
    deck = Deck()
    for card in cards:
        deck.add_card(card)
    return deck


def measure(run, setup=None, repeat=3):
    """Return the best time in seconds over `repeat` runs.

    Taking the best (smallest) time is standard practice, because slowdowns come
    from other programs using the computer, never from the code running faster
    than it should. If `setup` is given, it is called before each run and its
    result is passed to `run`; only `run` is timed.
    """
    best = float("inf")
    for _ in range(repeat):
        if setup is None:
            start = time.perf_counter()
            run()
        else:
            state = setup()
            start = time.perf_counter()
            run(state)
        best = min(best, time.perf_counter() - start)
    return best


def format_seconds(seconds):
    if seconds < 1e-6:
        return f"{seconds * 1e9:.0f} ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.1f} µs"
    if seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    return f"{seconds:.2f} s"


def format_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def machine_info():
    return (f"Python {platform.python_version()} on {platform.system()} "
            f"{platform.release()} ({platform.machine()})")


def start_report(name, title):
    """Start a fresh results file with the date and machine details."""
    RESULTS_DIR.mkdir(exist_ok=True)
    header = (f"# {title}\n\nRun on {date.today().isoformat()}. {machine_info()}.\n"
              f"Mode: {'quick' if QUICK else 'large' if LARGE else 'standard'}. "
              f"Each time is the best of several runs unless marked otherwise.\n")
    (RESULTS_DIR / f"{name}.md").write_text(header, encoding="utf-8")
    print(header)


def report(name, heading, headers, rows, notes=""):
    """Print a table and append it to the results file."""
    text = f"\n## {heading}\n\n{format_table(headers, rows)}\n"
    if notes:
        text += f"\n{notes}\n"
    print(text)
    with open(RESULTS_DIR / f"{name}.md", "a", encoding="utf-8") as file:
        file.write(text)
