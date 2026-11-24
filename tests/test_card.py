import pytest

from src.card import Card, parse_difficulty
from dataclasses import asdict

def test_to_dict_matches_asdict():
    card = Card(7, "Genetics", "Q?", "A", "DNA", 2,
                due_time=12.5, interval=120.0, times_correct=3, times_wrong=1)
    assert card.to_dict() == asdict(card)

def test_to_dict_returns_a_new_dictionary():
    card = Card(1, "Genetics", "Q?", "A", "DNA", 1)
    data = card.to_dict()
    data["topic"] = "Changed"
    assert card.topic == "Genetics"

def test_create_card():
    card = Card(1, "Cells and control", "What is mitosis?", "Cell division", "Mitosis", 2)
    assert card.card_id == 1
    assert card.subtopic == "Mitosis"
    assert card.difficulty == 2
    assert card.times_wrong == 0


def test_blank_question_rejected():
    with pytest.raises(ValueError):
        Card(1, "Cells and control", "   ", "Answer", "Mitosis", 1)


def test_blank_subtopic_rejected():
    with pytest.raises(ValueError):
        Card(1, "Genetics", "Q?", "A", "   ", 1)


@pytest.mark.parametrize("bad_difficulty", [0, 4, 5])
def test_invalid_difficulty_rejected(bad_difficulty):
    with pytest.raises(ValueError):
        Card(1, "Genetics", "Q?", "A", "DNA", bad_difficulty)


def test_id_over_64_bits_survives_round_trip():
    big_id = 2 ** 70
    card = Card(big_id, "Genetics", "Q?", "A", "DNA", 1)
    assert Card.from_dict(card.to_dict()).card_id == big_id


def test_parse_difficulty_accepts_numbers_with_spaces():
    assert parse_difficulty(" 2 ") == 2


@pytest.mark.parametrize("text", ["", "hard", "2.5"])
def test_parse_difficulty_rejects_non_integers(text):
    with pytest.raises(ValueError):
        parse_difficulty(text)