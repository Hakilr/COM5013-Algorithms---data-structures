from src.card import Card

class Deck:
    """A collection of cards stored in a hash map (Python dict) keyed by card ID."""

    def __init__(self):
        self._cards = {}

    def add_card(self, card):
        """Add a card. Raises ValueError if the ID already exists. Average O(1)."""
        if card.card_id in self._cards:
            raise ValueError(f"Card ID {card.card_id} already exists")
        self._cards[card.card_id] = card

    def get_card(self, card_id):
        """Return the card with this ID, or None if it does not exist. Average O(1)."""
        return self._cards.get(card_id)

    def edit_card(self, card_id, **changes):
        """Update fields on a card. Raises KeyError if the ID does not exist."""
        card = self._cards.get(card_id)
        if card is None:
            raise KeyError(f"No card with ID {card_id}")
        if "card_id" in changes:
            raise ValueError("Card ID cannot be changed")
        updated = card.to_dict()
        updated.update(changes)
        self._cards[card_id] = Card.from_dict(updated)  # re-runs validation

    def delete_card(self, card_id):
        """Remove a card. Raises KeyError if the ID does not exist. Average O(1)."""
        if card_id not in self._cards:
            raise KeyError(f"No card with ID {card_id}")
        del self._cards[card_id]

    def all_cards(self):
        """Return a list of all cards. O(n)."""
        return list(self._cards.values())

    def __len__(self):
        return len(self._cards)

    def __contains__(self, card_id):
        return card_id in self._cards