import pytest

from src.card import Card
from src.deck import Deck
from src.trie_index import TrieIndex


def make_card(card_id, question="x", answer="y", topic="t", subtopic="s"):
    return Card(card_id, topic, question, answer, subtopic, 1)


def index_of(*cards):
    index = TrieIndex()
    for card in cards:
        index.add_card(card)
    return index


def test_empty_index():
    index = TrieIndex()
    assert len(index) == 0
    assert index.node_count() == 0
    assert index.search("anything") == []


def test_prefix_search_finds_matches():
    index = index_of(
        make_card(1, question="What do mitochondria release?"),
        make_card(2, question="Mitosis is cell division"),
        make_card(3, question="What is DNA?"),
    )
    assert index.search("mito") == [1, 2]
    assert index.search("mitoc") == [1]


def test_search_is_case_insensitive():
    index = index_of(make_card(1, question="Mitochondria"))
    assert index.search("MITO") == [1]
    assert index.search("mito") == [1]


def test_prefix_matches_longer_words():
    index = index_of(make_card(1, question="Plant cells have walls"))
    assert index.search("cell") == [1]


def test_does_not_match_middle_of_word():
    index = index_of(make_card(1, question="Mitochondria"))
    assert index.search("chondria") == []


def test_multiple_terms_must_all_match():
    index = index_of(
        make_card(1, question="red blood cell"),
        make_card(2, question="white blood cell"),
        make_card(3, question="red kite"),
    )
    assert index.search("red blood") == [1]
    assert index.search("blood cell") == [1, 2]
    assert index.search("red nothing") == []


def test_topic_subtopic_and_answer_are_searchable():
    index = index_of(make_card(1, topic="Ecosystems", subtopic="Food chains",
                               answer="producer"))
    assert index.search("ecosys") == [1]
    assert index.search("chains") == [1]
    assert index.search("produc") == [1]


@pytest.mark.parametrize("query", ["", "   ", "!!!"])
def test_blank_query_returns_nothing(query):
    index = index_of(make_card(1, question="something"))
    assert index.search(query) == []


def test_no_match_returns_empty_list():
    index = index_of(make_card(1, question="mitosis"))
    assert index.search("zebra") == []


def test_remove_card_removes_it_from_results():
    index = index_of(make_card(1, question="mitosis"), make_card(2, question="mitosis"))
    index.remove_card(1)
    assert index.search("mito") == [2]
    assert len(index) == 1


def test_remove_prunes_empty_nodes():
    index = TrieIndex()
    index.add_card(make_card(1, question="hello"))
    assert index.node_count() > 0
    index.remove_card(1)
    assert index.node_count() == 0


def test_removing_a_word_that_is_a_prefix_of_another_keeps_the_longer_word():
    index = index_of(make_card(1, question="car"), make_card(2, question="card"))
    assert index.search("car") == [1, 2]
    assert index.search("card") == [2]
    index.remove_card(1)
    assert index.search("car") == [2]
    assert index.search("card") == [2]


def test_remove_missing_card_raises():
    with pytest.raises(KeyError):
        TrieIndex().remove_card(99)


def test_duplicate_card_rejected():
    index = index_of(make_card(1))
    with pytest.raises(ValueError):
        index.add_card(make_card(1))


def test_update_card_after_edit():
    index = index_of(make_card(1, question="alpha"))
    index.update_card(make_card(1, question="beta"))
    assert index.search("alpha") == []
    assert index.search("beta") == [1]


def test_build_from_deck():
    deck = Deck()
    deck.add_card(make_card(1, question="mitosis"))
    deck.add_card(make_card(2, question="meiosis"))
    index = TrieIndex.from_deck(deck)
    assert len(index) == 2
    assert index.search("mei") == [2]


def test_unicode_words():
    index = index_of(make_card(1, answer="measured in µm"))
    assert index.search("µm") == [1]


def test_id_over_64_bits():
    index = index_of(make_card(2 ** 70, question="mitosis"))
    assert index.search("mito") == [2 ** 70]


def test_large_index():
    index = TrieIndex()
    for i in range(1, 10_001):
        index.add_card(make_card(i, question=f"term{i}"))
    assert len(index) == 10_000
    # "term99" prefixes term99, term990 to term999 and term9900 to term9999
    assert len(index.search("term99")) == 111