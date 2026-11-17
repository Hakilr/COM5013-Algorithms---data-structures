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