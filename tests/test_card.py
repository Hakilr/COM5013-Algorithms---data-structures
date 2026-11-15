import pytest

from src.card import Card, parse_difficulty

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