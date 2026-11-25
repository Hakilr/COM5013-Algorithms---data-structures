"""Compare sorting algorithms on different kinds of data and different sizes.

Run from the main repo folder:   python -m benchmarks.benchmark_sorts

To add another algorithm, import it and add one line to ALGORITHMS below.
Counting sort needs extra arguments, so it is wrapped (see counting_sort_for_data).
"""

import random
from functools import partial

from benchmarks.common import choose_sizes, format_seconds, measure, report, start_report
from src.sorter import bubble_sort, counting_sort, merge_sort, quick_sort

NAME = "sorts"
SIZES = choose_sizes([100, 1_000, 5_000, 10_000, 100_000])

def counting_sort_for_data(data):
    """Counting sort with its range taken from the data (the min and max scan is timed too)."""
    return counting_sort(data, lambda x: x, min(data), max(data))


# name -> (function, largest size to run). Bubble sort is O(n squared), so it is
# stopped early: at 1,000,000 items it would need about 10^12 steps.
ALGORITHMS = {
    "bubble sort": (bubble_sort, 5_000),
    "merge sort": (merge_sort, 1_000_000),
    "quick sort (median of 3)": (quick_sort, 1_000_000),
    # First-item pivot is O(n squared) on sorted data, so it is stopped early too.
    "quick sort (first pivot)": (partial(quick_sort, pivot="first"), 5_000),
    "counting sort": (counting_sort_for_data, 1_000_000),
    "sorted() (reference)": (sorted, 1_000_000),
}


def random_data(n, rng):
    return [rng.randint(0, 1_000_000) for _ in range(n)]


def already_sorted_data(n, rng):
    return sorted(random_data(n, rng))


def reverse_sorted_data(n, rng):
    return sorted(random_data(n, rng), reverse=True)


def few_distinct_values_data(n, rng):
    return [rng.randint(1, 3) for _ in range(n)]   # like the difficulty field


CASES = {
    "Random data (average case)": random_data,
    "Already sorted (best case)": already_sorted_data,
    "Reverse sorted (worst case)": reverse_sorted_data,
    "Only three distinct values (like difficulty)": few_distinct_values_data,
}


def main():
    start_report(NAME, "Sorting benchmark")
    for heading, make_data in CASES.items():
        rows = []
        for n in SIZES:
            data = make_data(n, random.Random(n))
            row = [f"{n:,}"]
            for function, largest in ALGORITHMS.values():
                if n > largest:
                    row.append("skipped")
                    continue
                repeat = 3 if n <= 5_000 else 1
                row.append(format_seconds(measure(lambda: function(data), repeat=repeat)))
            rows.append(row)
        report(NAME, heading, ["n"] + list(ALGORITHMS), rows)

    report(NAME, "How to read these results", ["Expectation"], [
        ["Multiplying n by 10 should multiply O(n) time by about 10, O(n log n) by slightly more than 10, and O(n squared) by about 100."],
        ["Bubble sort should be fastest on already-sorted data (O(n) with the early exit) and slowest on reverse-sorted data."],
        ["Quick sort with the first item as pivot should slow down sharply on sorted and reverse-sorted data (O(n squared)); the median-of-three version should not."],
        ["Counting sort is O(n + k). On random data k is about 1,000,000, so small lists are slow because the counts list dwarfs the data; with only three distinct values it should beat every comparison sort."],
        ["sorted() is written in C, so it will beat your own sorts by a large factor. Compare your own sorts with each other."],
    ])


if __name__ == "__main__":
    main()
