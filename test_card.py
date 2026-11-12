import pytest
from src.card import Card


def test_create_card():
    card = Card(1, "Cells and control", "What is mitosis?", "Cell division")
    assert card.card_id == 1
    assert card.times_wrong == 0


def test_blank_question_rejected():
    with pytest.raises(ValueError):
        Card(1, "Cells and control", "   ", "Answer")


def test_invalid_difficulty_rejected():
    with pytest.raises(ValueError):
        Card(1, "Genetics", "Q?", "A", difficulty=5)


def test_id_over_64_bits_survives_round_trip():
    big_id = 2 ** 70
    card = Card(big_id, "Genetics", "Q?", "A")
    assert Card.from_dict(card.to_dict()).card_id == big_id