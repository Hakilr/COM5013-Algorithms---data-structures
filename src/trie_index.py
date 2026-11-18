import re

_WORD = re.compile(r"\w+")


def tokenize(text):
    """Split text into lower-case words, ignoring punctuation."""
    return _WORD.findall(text.lower())


class TrieNode:
    """One letter in the trie: child letters, and the cards whose word ends here."""

    __slots__ = ("children", "card_ids")   # saves memory when there are many nodes

    def __init__(self):
        self.children = {}      # letter -> TrieNode (a hash map)
        self.card_ids = set()   # IDs of cards containing the word that ends here


class TrieIndex:
    """Prefix search over the words in every card.

    Indexed fields: topic, subtopic, question and answer. Searching is by word
    prefix and is case-insensitive. It stores card IDs only; the cards stay in the Deck.
    """

    def __init__(self):
        self._root = TrieNode()
        self._words_by_card = {}   # card ID -> set of words indexed for that card

    @classmethod
    def from_deck(cls, deck):
        """Build an index from every card in a deck."""
        index = cls()
        for card in deck.all_cards():
            index.add_card(card)
        return index

    @staticmethod
    def _words_for(card):
        text = f"{card.topic} {card.subtopic} {card.question} {card.answer}"
        return set(tokenize(text))

    def add_card(self, card):
        """Index a card's words. O(L), where L is the total letters in its words."""
        if card.card_id in self._words_by_card:
            raise ValueError(f"Card {card.card_id} is already indexed")
        words = self._words_for(card)
        for word in words:
            node = self._root
            for letter in word:
                node = node.children.setdefault(letter, TrieNode())
            node.card_ids.add(card.card_id)
        self._words_by_card[card.card_id] = words

    def remove_card(self, card_id):
        """Remove a card from the index, pruning nodes left empty. O(L)."""
        words = self._words_by_card.pop(card_id, None)
        if words is None:
            raise KeyError(f"Card {card_id} is not indexed")
        for word in words:
            path = [self._root]
            for letter in word:
                path.append(path[-1].children[letter])
            path[-1].card_ids.discard(card_id)
            # Prune from the bottom up, stopping at the first node still in use.
            for depth in range(len(word), 0, -1):
                node = path[depth]
                if node.card_ids or node.children:
                    break
                del path[depth - 1].children[word[depth - 1]]

    def update_card(self, card):
        """Re-index a card after it was edited (adds it if it is new)."""
        if card.card_id in self._words_by_card:
            self.remove_card(card.card_id)
        self.add_card(card)

    def search(self, query):
        """Return sorted IDs of cards matching every term in the query.

        Each term matches any word that starts with it ("mito" finds "mitosis").
        A blank query returns an empty list.
        Cost per term: O(p + s), where p is the term length and s is the number of
        trie nodes below that prefix.
        """
        terms = tokenize(query)
        if not terms:
            return []
        result = None
        for term in terms:
            ids = self._ids_with_prefix(term)
            result = ids if result is None else result & ids
            if not result:
                return []
        return sorted(result)

    def _ids_with_prefix(self, prefix):
        node = self._root
        for letter in prefix:
            node = node.children.get(letter)
            if node is None:
                return set()
        ids = set()
        stack = [node]   # iterative depth-first walk of everything below the prefix
        while stack:
            current = stack.pop()
            ids.update(current.card_ids)
            stack.extend(current.children.values())
        return ids

    def node_count(self):
        """Number of letter nodes in the trie (useful for memory benchmarks)."""
        count = 0
        stack = list(self._root.children.values())
        while stack:
            node = stack.pop()
            count += 1
            stack.extend(node.children.values())
        return count

    def __len__(self):
        return len(self._words_by_card)