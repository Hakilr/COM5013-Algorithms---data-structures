import time

from src.heap import MinHeap

INITIAL_INTERVAL = 60.0                # seconds until a wrong card is shown again
MAX_INTERVAL = 30 * 24 * 60 * 60.0     # cap the doubling at 30 days


class Scheduler:
    """Decides which card to revise next, using a min-heap ordered by due time.

    Rule: a correct answer doubles the card's interval (up to MAX_INTERVAL);
    a wrong answer resets it to INITIAL_INTERVAL. The card is then due again at
    now + interval.

    The heap holds (due_time, card_id) entries. When a card is rescheduled or
    removed, its old entry stays in the heap ("lazy deletion") and is skipped
    when it reaches the top. A dictionary records each card's current due time
    so stale entries can be recognised in O(1).
    """

    def __init__(self):
        self._heap = MinHeap()
        self._due = {}    # card ID -> current due time

    @classmethod
    def from_deck(cls, deck):
        """Schedule every card in a deck, using each card's saved due_time."""
        scheduler = cls()
        for card in deck.all_cards():
            scheduler.add_card(card)
        return scheduler

    def add_card(self, card):
        """Start scheduling a card at its due_time. O(log n)."""
        if card.card_id in self._due:
            raise ValueError(f"Card {card.card_id} is already scheduled")
        self._push(card.card_id, card.due_time)

    def remove_card(self, card_id):
        """Stop scheduling a card. O(1); its heap entry is discarded later."""
        if card_id not in self._due:
            raise KeyError(f"Card {card_id} is not scheduled")
        del self._due[card_id]

    def peek(self):
        """Return (card_id, due_time) of the most urgent card, or None if empty."""
        self._discard_stale()
        if not len(self._heap):
            return None
        due_time, card_id = self._heap.peek()
        return card_id, due_time

    def next_due(self, now=None):
        """Return the ID of the most urgent card that is due now, or None."""
        entry = self.peek()
        if entry is None:
            return None
        card_id, due_time = entry
        now = time.time() if now is None else now
        return card_id if due_time <= now else None

    def record_answer(self, card, correct, now=None):
        """Update a card after an answer and reschedule it. O(log n).

        This changes the card's interval, due_time and answer counters.
        """
        if card.card_id not in self._due:
            raise KeyError(f"Card {card.card_id} is not scheduled")
        now = time.time() if now is None else now

        if correct:
            card.times_correct += 1
            card.interval = min(card.interval * 2, MAX_INTERVAL)
        else:
            card.times_wrong += 1
            card.interval = INITIAL_INTERVAL
        card.due_time = now + card.interval
        self._push(card.card_id, card.due_time)

    def heap_size(self):
        """Entries in the heap, including stale ones (useful for benchmarks)."""
        return len(self._heap)

    def __len__(self):
        return len(self._due)

    def _push(self, card_id, due_time):
        self._due[card_id] = due_time
        self._heap.push((due_time, card_id))
        # Too many stale entries? Rebuild the heap from the dictionary. O(n),
        # but it happens rarely, so the cost per operation stays small.
        if len(self._heap) > 2 * len(self._due) + 16:
            self._heap = MinHeap((due, cid) for cid, due in self._due.items())

    def _discard_stale(self):
        """Pop entries from the top until the top entry is current."""
        while len(self._heap):
            due_time, card_id = self._heap.peek()
            if self._due.get(card_id) == due_time:
                return
            self._heap.pop()