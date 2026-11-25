"""Undo stack for the revision session (feature F6).

A stack is last in, first out: the most recent answer is the first one undone.
push, pop and peek are all O(1) because they only touch the end of a Python list.

Before the scheduler changes a card after an answer, the CLI saves the card's old
revision state with snapshot() and pushes it. Undo pops it and restore() puts the
old values back.
"""

from typing import NamedTuple


class CardState(NamedTuple):
    """The part of a card that a right/wrong answer changes."""
    card_id: int
    due_time: float
    interval: float
    times_correct: int
    times_wrong: int


def snapshot(card):
    """Return the card's current revision state (taken before it is changed)."""
    return CardState(card.card_id, card.due_time, card.interval,
                     card.times_correct, card.times_wrong)


def restore(card, state):
    """Put a card back to a saved state. Raises ValueError if it is a different card."""
    if card.card_id != state.card_id:
        raise ValueError(f"state is for card {state.card_id}, not card {card.card_id}")
    card.due_time = state.due_time
    card.interval = state.interval
    card.times_correct = state.times_correct
    card.times_wrong = state.times_wrong


class UndoStack:
    """A last-in, first-out stack of saved states.

    max_size (optional) keeps memory bounded in a very long session: when full, the
    oldest entry is dropped. Dropping from the bottom is O(n), but only happens once
    max_size answers have been given, so the default (no limit) is plain O(1).
    """

    def __init__(self, max_size=None):
        if max_size is not None and max_size < 1:
            raise ValueError("max_size must be at least 1")
        self._items = []
        self._max_size = max_size

    def push(self, item):
        """Add an item on top. O(1)."""
        self._items.append(item)
        if self._max_size is not None and len(self._items) > self._max_size:
            del self._items[0]

    def pop(self):
        """Remove and return the top item. O(1). Raises IndexError if empty."""
        if not self._items:
            raise IndexError("nothing to undo")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. O(1). Raises IndexError if empty."""
        if not self._items:
            raise IndexError("nothing to undo")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def clear(self):
        self._items.clear()

    def __len__(self):
        return len(self._items)


def undo_last_answer(deck, scheduler, undo_stack):
    """Undo the most recent answer of the session.

    The stack holds (CardState, was_correct) pairs. Restores the card's old values,
    reschedules it, and returns (card, was_correct), or None if there is nothing
    to undo or the card no longer exists.
    """
    if undo_stack.is_empty():
        return None
    state, was_correct = undo_stack.pop()
    card = deck.get_card(state.card_id)
    if card is None:
        return None
    scheduler.restore_state(card, state)
    return card, was_correct
