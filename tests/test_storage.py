import json

import pytest

from src.card import Card
from src.deck import Deck
from src.storage import StorageError, load_deck, save_deck


def make_card(card_id=1, **changes):
    fields = dict(card_id=card_id, topic="Genetics", question="What is DNA?",
              answer="Genetic material", subtopic="DNA", difficulty=1)
    fields.update(changes)
    return Card(**fields)


def test_round_trip_keeps_cards(tmp_path):
    deck = Deck()
    deck.add_card(make_card(1, times_wrong=3, due_time=123.5))
    deck.add_card(make_card(2, topic="Ecosystems"))
    file_path = tmp_path / "deck.json"

    save_deck(deck, file_path)
    loaded = load_deck(file_path)

    assert len(loaded) == 2
    assert loaded.get_card(1).times_wrong == 3
    assert loaded.get_card(1).due_time == 123.5
    assert loaded.get_card(2).topic == "Ecosystems"


def test_round_trip_empty_deck(tmp_path):
    file_path = tmp_path / "deck.json"
    save_deck(Deck(), file_path)
    assert len(load_deck(file_path)) == 0


def test_missing_file_returns_empty_deck(tmp_path):
    assert len(load_deck(tmp_path / "does_not_exist.json")) == 0


def test_corrupt_json_raises(tmp_path):
    file_path = tmp_path / "deck.json"
    file_path.write_text("{this is not valid json", encoding="utf-8")
    with pytest.raises(StorageError):
        load_deck(file_path)


def test_empty_file_raises(tmp_path):
    file_path = tmp_path / "deck.json"
    file_path.write_text("", encoding="utf-8")
    with pytest.raises(StorageError):
        load_deck(file_path)


@pytest.mark.parametrize("content", ["[1, 2, 3]", '{"cards": "oops"}', '{"version": 1}'])
def test_wrong_structure_raises(tmp_path, content):
    file_path = tmp_path / "deck.json"
    file_path.write_text(content, encoding="utf-8")
    with pytest.raises(StorageError):
        load_deck(file_path)


def test_invalid_card_in_file_raises(tmp_path):
    bad_card = make_card(1).to_dict()
    bad_card["answer"] = "   "
    file_path = tmp_path / "deck.json"
    file_path.write_text(json.dumps({"version": 1, "cards": [bad_card]}), encoding="utf-8")
    with pytest.raises(StorageError):
        load_deck(file_path)


def test_duplicate_ids_in_file_raise(tmp_path):
    card = make_card(1).to_dict()
    file_path = tmp_path / "deck.json"
    file_path.write_text(json.dumps({"version": 1, "cards": [card, card]}), encoding="utf-8")
    with pytest.raises(StorageError):
        load_deck(file_path)


def test_id_over_64_bits_round_trip(tmp_path):
    deck = Deck()
    deck.add_card(make_card(2 ** 70))
    file_path = tmp_path / "deck.json"
    save_deck(deck, file_path)
    assert load_deck(file_path).get_card(2 ** 70) is not None


def test_unicode_text_round_trip(tmp_path):
    deck = Deck()
    deck.add_card(make_card(1, answer="Mitochondria – the 'powerhouse' (µm scale) ✓"))
    file_path = tmp_path / "deck.json"
    save_deck(deck, file_path)
    assert load_deck(file_path).get_card(1).answer == "Mitochondria – the 'powerhouse' (µm scale) ✓"


def test_save_leaves_no_temp_file(tmp_path):
    deck = Deck()
    deck.add_card(make_card(1))
    save_deck(deck, tmp_path / "deck.json")
    assert [p.name for p in tmp_path.iterdir()] == ["deck.json"]


def test_save_to_missing_folder_raises(tmp_path):
    with pytest.raises(StorageError):
        save_deck(Deck(), tmp_path / "no_such_folder" / "deck.json")