import pytest
from src.card import Card
from src.deck import Deck


def make_card(card_id=1):
    return Card(card_id, "Genetics", "What is DNA?", "Genetic material", "DNA", 1)


def test_empty_deck():
    deck = Deck()
    assert len(deck) == 0
    assert deck.all_cards() == []


def test_add_and_get():
    deck = Deck()
    deck.add_card(make_card(1))
    assert deck.get_card(1).question == "What is DNA?"
    assert 1 in deck


def test_duplicate_id_rejected():
    deck = Deck()
    deck.add_card(make_card(1))
    with pytest.raises(ValueError):
        deck.add_card(make_card(1))


def test_get_missing_returns_none():
    assert Deck().get_card(99) is None


def test_edit_card():
    deck = Deck()
    deck.add_card(make_card(1))
    deck.edit_card(1, answer="Deoxyribonucleic acid")
    assert deck.get_card(1).answer == "Deoxyribonucleic acid"


def test_edit_with_blank_answer_rejected():
    deck = Deck()
    deck.add_card(make_card(1))
    with pytest.raises(ValueError):
        deck.edit_card(1, answer="  ")


def test_delete_card():
    deck = Deck()
    deck.add_card(make_card(1))
    deck.delete_card(1)
    assert len(deck) == 0


def test_delete_missing_raises():
    with pytest.raises(KeyError):
        Deck().delete_card(5)


def test_id_over_64_bits():
    deck = Deck()
    deck.add_card(make_card(2 ** 70))
    assert deck.get_card(2 ** 70) is not None

def test_new_id_for_empty_deck():
    assert Deck().new_id() == 1


def test_new_id_is_one_more_than_the_largest_id():
    deck = Deck()
    deck.add_card(make_card(1))
    deck.add_card(make_card(5))
    assert deck.new_id() == 6


def test_new_id_does_not_drop_when_adding_a_lower_id():
    deck = Deck()
    deck.add_card(make_card(10))
    deck.add_card(make_card(3))
    assert deck.new_id() == 11


def test_ids_are_not_reused_after_deleting_the_highest_card():
    deck = Deck()
    for card_id in (1, 2, 3):
        deck.add_card(make_card(card_id))
    deck.delete_card(3)
    assert deck.new_id() == 4


def test_new_id_is_never_in_use():
    deck = Deck()
    for _ in range(100):
        new_id = deck.new_id()
        assert new_id not in deck
        deck.add_card(make_card(new_id))


def test_editing_does_not_change_new_id():
    deck = Deck()
    deck.add_card(make_card(1))
    deck.edit_card(1, answer="Changed")
    assert deck.new_id() == 2


def test_new_id_after_id_over_64_bits():
    deck = Deck()
    deck.add_card(make_card(2 ** 70))
    assert deck.new_id() == 2 ** 70 + 1