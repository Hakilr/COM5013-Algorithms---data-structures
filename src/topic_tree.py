class TreeNode:
    """One node in the topic tree: a name, child nodes and card IDs."""

    def __init__(self, name):
        self.name = name
        self.children = {}   # child name -> TreeNode (a hash map)
        self.card_ids = {}   # used as an ordered set: card ID -> None


class TopicTree:
    """Tree of topic -> subtopic -> card IDs.

    It stores card IDs only; the cards themselves stay in the Deck.
    Every card has a topic and a subtopic, so there is no fallback branch.
    """

    def __init__(self):
        self._root = TreeNode("root")
        self._size = 0

    @classmethod
    def from_deck(cls, deck):
        """Build a tree from every card in a deck. O(n)."""
        tree = cls()
        for card in deck.all_cards():
            tree.add_card(card)
        return tree

    @staticmethod
    def _get_or_create(parent, name):
        if name not in parent.children:
            parent.children[name] = TreeNode(name)
        return parent.children[name]

    def add_card(self, card):
        """File a card under its topic and subtopic. Average O(1)."""
        topic_node = self._get_or_create(self._root, card.topic.strip())
        sub_node = self._get_or_create(topic_node, card.subtopic.strip())
        if card.card_id in sub_node.card_ids:
            raise ValueError(f"Card {card.card_id} is already in this subtopic")
        sub_node.card_ids[card.card_id] = None
        self._size += 1

    def remove_card(self, card):
        """Remove a card, and any topic or subtopic left empty. Average O(1)."""
        topic_name = card.topic.strip()
        sub_name = card.subtopic.strip()
        topic_node = self._root.children.get(topic_name)
        sub_node = topic_node.children.get(sub_name) if topic_node else None
        if sub_node is None or card.card_id not in sub_node.card_ids:
            raise KeyError(f"Card {card.card_id} is not in the tree")
        del sub_node.card_ids[card.card_id]
        self._size -= 1
        if not sub_node.card_ids:
            del topic_node.children[sub_name]
        if not topic_node.children:
            del self._root.children[topic_name]

    def topics(self):
        """Return all topic names."""
        return list(self._root.children)

    def subtopics(self, topic):
        """Return the subtopic names under a topic (empty list if unknown)."""
        topic_node = self._root.children.get(topic.strip())
        return list(topic_node.children) if topic_node else []

    def card_ids_in(self, topic, subtopic=None):
        """Return card IDs under a topic, or under one subtopic of it."""
        topic_node = self._root.children.get(topic.strip())
        if topic_node is None:
            return []
        if subtopic is None:
            return self._collect_ids(topic_node)
        sub_node = topic_node.children.get(subtopic.strip())
        return list(sub_node.card_ids) if sub_node else []

    def all_card_ids(self):
        """Return every card ID using depth-first traversal. O(n)."""
        return self._collect_ids(self._root)

    @staticmethod
    def _collect_ids(start):
        """Iterative depth-first traversal using an explicit stack."""
        result = []
        stack = [start]
        while stack:
            node = stack.pop()
            result.extend(node.card_ids)
            stack.extend(reversed(list(node.children.values())))
        return result

    def __len__(self):
        return self._size