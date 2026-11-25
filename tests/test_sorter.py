"""Tests for src/sorter.py: bubble, merge, quick and counting sort."""
import random
from functools import partial

import pytest

from src.card import Card
from src.sorter import (
    MAX_RANGE, bubble_sort, counting_sort, merge_sort, quick_sort,
)


def counting_sort_auto(items, key=lambda x: x):
    """Counting sort with its range taken from the data, so it fits the generic tests."""
    items = list(items)
    if not items:
        return []
    keys = [key(item) for item in items]
    return counting_sort(items, key, min(keys), max(keys))


# Every sort that must give a correct, sorted result.
SORTS = [
    pytest.param(bubble_sort, id="bubble"),
    pytest.param(merge_sort, id="merge"),
    pytest.param(quick_sort, id="quick-median3"),
    pytest.param(partial(quick_sort, pivot="first"), id="quick-first"),
    pytest.param(counting_sort_auto, id="counting"),
]
# Sorts that must keep equal items in their original order.
STABLE_SORTS = [
    pytest.param(bubble_sort, id="bubble"),
    pytest.param(merge_sort, id="merge"),
    pytest.param(counting_sort_auto, id="counting"),
]


def make_card(card_id, difficulty, topic="Genetics"):
    return Card(card_id=card_id, topic=topic, subtopic="Alleles",
                question=f"Question {card_id}?", answer="Answer", difficulty=difficulty)


@pytest.mark.parametrize("sort", SORTS)
def test_empty_list(sort):
    assert sort([]) == []


@pytest.mark.parametrize("sort", SORTS)
def test_single_item(sort):
    assert sort([7]) == [7]


@pytest.mark.parametrize("sort", SORTS)
def test_already_sorted(sort):
    assert sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_reverse_sorted(sort):
    assert sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_duplicates(sort):
    assert sort([3, 1, 3, 2, 1, 3]) == [1, 1, 2, 3, 3, 3]


@pytest.mark.parametrize("sort", SORTS)
def test_all_equal(sort):
    assert sort([4, 4, 4, 4]) == [4, 4, 4, 4]


@pytest.mark.parametrize("sort", SORTS)
def test_negative_and_zero(sort):
    assert sort([0, -3, 5, -1, 0]) == [-3, -1, 0, 0, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_values_over_64_bits(sort):
    base = 2 ** 70
    data = [base + 2, base, base + 1, base + 2]
    assert sort(data) == [base, base + 1, base + 2, base + 2]


@pytest.mark.parametrize("sort", SORTS)
def test_original_is_not_changed(sort):
    data = [3, 1, 2]
    result = sort(data)
    assert data == [3, 1, 2]
    assert result is not data


@pytest.mark.parametrize("sort", SORTS)
def test_random_matches_sorted(sort):
    rng = random.Random(42)
    data = [rng.randint(-50, 50) for _ in range(200)]
    assert sort(data) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_cards_by_difficulty(sort):
    cards = [make_card(1, 3), make_card(2, 1), make_card(3, 2)]
    result = sort(cards, key=lambda card: card.difficulty)
    assert [card.card_id for card in result] == [2, 3, 1]


@pytest.mark.parametrize("sort", STABLE_SORTS)
def test_stable_keeps_equal_items_in_order(sort):
    cards = [make_card(1, 2), make_card(2, 1), make_card(3, 2), make_card(4, 1)]
    result = sort(cards, key=lambda card: card.difficulty)
    assert [card.card_id for card in result] == [2, 4, 1, 3]


def test_quick_sort_is_not_stable():
    """Documents a known property: quick sort can reorder equal items.

    This exact input (all keys equal) is reordered by the default pivot rule, so
    the test is repeatable. It is why the app uses merge sort for its sorted lists.
    """
    data = [(1, 0), (1, 1), (1, 2)]
    result = quick_sort(data, key=lambda pair: pair[0])
    assert sorted(result) == data                    # same items...
    assert result != data                            # ...but not in the original order


# ---- quick sort specifics ----

def test_quick_sort_rejects_unknown_pivot():
    with pytest.raises(ValueError):
        quick_sort([3, 1, 2], pivot="random")


@pytest.mark.parametrize("pivot", ["median_of_three", "first"])
def test_quick_sort_every_small_list(pivot):
    """Every list of up to 6 items over three values (like difficulty)."""
    import itertools
    for size in range(7):
        for data in itertools.product((1, 2, 3), repeat=size):
            assert quick_sort(data, pivot=pivot) == sorted(data)


def test_quick_sort_worst_case_does_not_hit_recursion_limit():
    """Sorted data with the first-item pivot is the worst case; depth must stay small."""
    data = list(range(3000))
    assert quick_sort(data, pivot="first") == data


def test_quick_sort_large_sorted_and_reverse():
    data = list(range(50_000))
    assert quick_sort(data) == data
    assert quick_sort(data[::-1]) == data


def test_quick_sort_many_equal_keys():
    data = [random.Random(i).randint(1, 3) for i in range(50_000)]
    assert quick_sort(data) == sorted(data)


# ---- counting sort specifics ----

def test_counting_sort_by_difficulty_range():
    cards = [make_card(1, 3), make_card(2, 1), make_card(3, 2), make_card(4, 1)]
    result = counting_sort(cards, lambda card: card.difficulty, 1, 3)
    assert [card.card_id for card in result] == [2, 4, 3, 1]


def test_counting_sort_key_called_once_per_item():
    calls = []

    def key(x):
        calls.append(x)
        return x

    counting_sort([3, 1, 2, 1], key, 1, 3)
    assert len(calls) == 4


def test_counting_sort_huge_values_small_range():
    base = 2 ** 70
    assert counting_sort([base + 2, base, base + 1], lambda x: x, base, base + 2) == [
        base, base + 1, base + 2]


def test_counting_sort_range_wider_than_data():
    assert counting_sort([5, 2], lambda x: x, 0, 10) == [2, 5]


def test_counting_sort_empty_with_valid_range():
    assert counting_sort([], lambda x: x, 1, 3) == []


@pytest.mark.parametrize("bad", [0, 4, -1])
def test_counting_sort_key_outside_range(bad):
    """A key below the range would silently wrap round to the wrong slot if unchecked."""
    with pytest.raises(ValueError):
        counting_sort([2, bad], lambda x: x, 1, 3)


def test_counting_sort_rejects_non_integer_key():
    with pytest.raises(TypeError):
        counting_sort([1.5], lambda x: x, 1, 3)


def test_counting_sort_rejects_backwards_range():
    with pytest.raises(ValueError):
        counting_sort([1], lambda x: x, 3, 1)


def test_counting_sort_rejects_huge_range():
    with pytest.raises(ValueError):
        counting_sort([1], lambda x: x, 0, MAX_RANGE)


# ---- larger inputs ----

def test_merge_sort_large_list():
    rng = random.Random(7)
    data = [rng.randint(0, 10 ** 6) for _ in range(100_000)]
    assert merge_sort(data) == sorted(data)
