import random

import pytest

from src.card import Card
from src.sorter import bubble_sort, merge_sort

SORTS = [bubble_sort, merge_sort]


def make_card(card_id, difficulty, topic="Genetics"):
    return Card(card_id, topic, "Question?", "Answer", "DNA", difficulty)


@pytest.mark.parametrize("sort", SORTS)
def test_empty_list(sort):
    assert sort([]) == []


@pytest.mark.parametrize("sort", SORTS)
def test_single_item(sort):
    assert sort([5]) == [5]


@pytest.mark.parametrize("sort", SORTS)
def test_already_sorted(sort):
    assert sort([1, 2, 3, 4]) == [1, 2, 3, 4]


@pytest.mark.parametrize("sort", SORTS)
def test_reverse_sorted(sort):
    assert sort([4, 3, 2, 1]) == [1, 2, 3, 4]


@pytest.mark.parametrize("sort", SORTS)
def test_duplicates(sort):
    assert sort([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]


@pytest.mark.parametrize("sort", SORTS)
def test_all_equal(sort):
    assert sort([7, 7, 7]) == [7, 7, 7]


@pytest.mark.parametrize("sort", SORTS)
def test_negative_and_zero_values(sort):
    assert sort([0, -5, 3, 0, -1]) == [-5, -1, 0, 0, 3]


@pytest.mark.parametrize("sort", SORTS)
def test_values_over_64_bits(sort):
    assert sort([2 ** 70, 1, 2 ** 65]) == [1, 2 ** 65, 2 ** 70]


@pytest.mark.parametrize("sort", SORTS)
def test_original_list_not_changed(sort):
    original = [3, 1, 2]
    sort(original)
    assert original == [3, 1, 2]


@pytest.mark.parametrize("sort", SORTS)
def test_matches_python_sorted_on_random_data(sort):
    rng = random.Random(42)
    data = [rng.randint(-1000, 1000) for _ in range(200)]
    assert sort(data) == sorted(data)


@pytest.mark.parametrize("sort", SORTS)
def test_sort_cards_by_difficulty(sort):
    cards = [make_card(1, 3), make_card(2, 1), make_card(3, 2)]
    result = sort(cards, key=lambda card: card.difficulty)
    assert [card.card_id for card in result] == [2, 3, 1]


@pytest.mark.parametrize("sort", SORTS)
def test_sort_is_stable(sort):
    # Equal difficulties must stay in their original order.
    cards = [make_card(1, 2), make_card(2, 1), make_card(3, 2), make_card(4, 1)]
    result = sort(cards, key=lambda card: card.difficulty)
    assert [card.card_id for card in result] == [2, 4, 1, 3]


def test_merge_sort_large_list():
    rng = random.Random(1)
    data = [rng.randint(0, 1_000_000) for _ in range(100_000)]
    assert merge_sort(data) == sorted(data)