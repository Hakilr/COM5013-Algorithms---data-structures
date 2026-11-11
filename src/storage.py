import json
import os
from pathlib import Path

from src.card import Card
from src.deck import Deck

FORMAT_VERSION = 1


class StorageError(Exception):
    """Raised when a deck file cannot be saved, read or understood."""


def save_deck(deck, path):
    """Save every card in the deck to a JSON file. O(n) in the number of cards.

    Writes to a temporary file first, then swaps it in, so a crash part-way
    through cannot leave a half-written save file.
    """
    path = Path(path)
    data = {
        "version": FORMAT_VERSION,
        "cards": [card.to_dict() for card in deck.all_cards()],
    }
    temp_path = path.with_name(path.name + ".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        os.replace(temp_path, path)
    except OSError as error:
        raise StorageError(f"Could not save deck to {path}: {error}") from error


def load_deck(path):
    """Load a deck from a JSON file. O(n) in the number of cards.

    A missing file gives an empty deck (first run). A damaged or invalid
    file raises StorageError instead of crashing or loading bad data.
    """
    path = Path(path)
    deck = Deck()

    if not path.exists():
        return deck

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise StorageError(f"{path} is not valid JSON: {error}") from error
    except OSError as error:
        raise StorageError(f"Could not read {path}: {error}") from error

    if not isinstance(data, dict) or not isinstance(data.get("cards"), list):
        raise StorageError(f"{path} does not have the expected format")

    for item in data["cards"]:
        try:
            deck.add_card(Card.from_dict(item))
        except (TypeError, ValueError) as error:
            raise StorageError(f"Invalid card in {path}: {error}") from error

    return deck