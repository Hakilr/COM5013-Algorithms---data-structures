import pytest

from src.card import Card
from src.deck import Deck
from src.topic_tree import TopicTree


def make_card(card_id, topic="Genetics", subtopic="DNA"):
    return Card(card_id, topic, "Question?", "Answer", subtopic, 1)


def test_empty_tree():
    tree = TopicTree()
    assert len(tree) == 0
    assert tree.topics() == []
    assert tree.all_card_ids() == []


def test_add_and_browse_by_topic_and_subtopic():
    tree = TopicTree()
    tree.add_card(make_card(1, "Genetics", "DNA"))
    tree.add_card(make_card(2, "Genetics", "Inheritance"))
    tree.add_card(make_card(3, "Ecosystems", "Food chains"))
    assert tree.topics() == ["Genetics", "Ecosystems"]
    assert tree.subtopics("Genetics") == ["DNA", "Inheritance"]
    assert tree.card_ids_in("Genetics") == [1, 2]
    assert tree.card_ids_in("Genetics", "DNA") == [1]


def test_subtopic_whitespace_ignored():
    tree = TopicTree()
    tree.add_card(make_card(1, "Genetics", " DNA "))
    assert tree.card_ids_in("Genetics", "DNA") == [1]


def test_duplicate_card_rejected():
    tree = TopicTree()
    tree.add_card(make_card(1))
    with pytest.raises(ValueError):
        tree.add_card(make_card(1))


def test_unknown_topic_and_subtopic_return_empty():
    tree = TopicTree()
    tree.add_card(make_card(1, "Genetics", "DNA"))
    assert tree.card_ids_in("Nope") == []
    assert tree.card_ids_in("Genetics", "Nope") == []
    assert tree.subtopics("Nope") == []


def test_remove_card_prunes_empty_branches():
    tree = TopicTree()
    card = make_card(1, "Genetics", "DNA")
    tree.add_card(card)
    tree.remove_card(card)
    assert len(tree) == 0
    assert tree.topics() == []


def test_remove_keeps_other_cards():
    tree = TopicTree()
    first, second = make_card(1, "Genetics", "DNA"), make_card(2, "Genetics", "DNA")
    tree.add_card(first)
    tree.add_card(second)
    tree.remove_card(first)
    assert tree.card_ids_in("Genetics", "DNA") == [2]


def test_remove_missing_card_raises():
    tree = TopicTree()
    with pytest.raises(KeyError):
        tree.remove_card(make_card(1))


def test_depth_first_order():
    tree = TopicTree()
    tree.add_card(make_card(1, "A", "x"))
    tree.add_card(make_card(2, "A", "y"))
    tree.add_card(make_card(3, "B", "z"))
    tree.add_card(make_card(4, "A", "x"))
    assert tree.all_card_ids() == [1, 4, 2, 3]


def test_build_from_deck():
    deck = Deck()
    deck.add_card(make_card(1, "Genetics", "DNA"))
    deck.add_card(make_card(2, "Ecosystems"))
    tree = TopicTree.from_deck(deck)
    assert len(tree) == 2
    assert sorted(tree.topics()) == ["Ecosystems", "Genetics"]


def test_id_over_64_bits():
    tree = TopicTree()
    tree.add_card(make_card(2 ** 70))
    assert tree.card_ids_in("Genetics") == [2 ** 70]