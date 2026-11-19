from pathlib import Path

from src.card import Card, parse_difficulty
from src.importer import ImportFileError, import_cards_from_csv
from src.sorter import merge_sort
from src.storage import StorageError, load_deck, save_deck
from src.trie_index import TrieIndex

SAVE_FILE = Path(__file__).resolve().parent.parent / "deck.json"


def next_card_id(deck):
    """Return an unused ID: one more than the largest existing ID."""
    ids = [card.card_id for card in deck.all_cards()]
    return max(ids, default=0) + 1


def format_card(card):
    """Return a one-line description of a card."""
    return (
        f"[{card.card_id}] {card.topic} > {card.subtopic} "
        f"(difficulty {card.difficulty}) | Q: {card.question} | A: {card.answer}"
    )


# --- Sort orders ---------------------------------------------------------
# merge_sort is stable, so sorting by a secondary key first and the primary
# key second gives "primary key, then secondary key" without extra code.

def sort_by_id(cards):
    return merge_sort(cards, key=lambda card: card.card_id)


def sort_by_difficulty_easiest_first(cards):
    return merge_sort(cards, key=lambda card: card.difficulty)


def sort_by_difficulty_hardest_first(cards):
    return merge_sort(cards, key=lambda card: -card.difficulty)


def sort_by_topic_then_subtopic(cards):
    by_subtopic = merge_sort(cards, key=lambda card: card.subtopic.lower())
    return merge_sort(by_subtopic, key=lambda card: card.topic.lower())


def sort_by_topic_then_difficulty(cards):
    by_difficulty = merge_sort(cards, key=lambda card: card.difficulty)
    return merge_sort(by_difficulty, key=lambda card: card.topic.lower())


SORT_OPTIONS = {
    "1": ("ID (order added)", sort_by_id),
    "2": ("difficulty, easiest first", sort_by_difficulty_easiest_first),
    "3": ("difficulty, hardest first", sort_by_difficulty_hardest_first),
    "4": ("topic, then subtopic", sort_by_topic_then_subtopic),
    "5": ("topic, then difficulty", sort_by_topic_then_difficulty),
}


# --- Menu actions --------------------------------------------------------

def add_card_prompt(deck, index):
    """Ask the user for card details, add the card, index it, then save the deck."""
    print("\n--- Add a new card ---")
    topic = input("Topic (e.g. Cells and control): ")
    subtopic = input("Subtopic (e.g. Mitosis): ")
    question = input("Question: ")
    answer = input("Answer: ")
    difficulty_text = input("Difficulty (1 = easy, 2 = medium, 3 = hard): ")

    try:
        card = Card(
            card_id=next_card_id(deck),
            topic=topic,
            subtopic=subtopic,
            question=question,
            answer=answer,
            difficulty=parse_difficulty(difficulty_text),
        )
        deck.add_card(card)
    except ValueError as error:
        print(f"Could not add card: {error}")
        return

    index.add_card(card)

    try:
        save_deck(deck, SAVE_FILE)
        print(f"Card {card.card_id} added and saved.")
    except StorageError as error:
        print(f"Card added, but it could not be saved: {error}")


def list_cards(deck):
    """Ask how to order the cards, then print them."""
    cards = deck.all_cards()
    if not cards:
        print("\nThe deck is empty.")
        return

    print("\n--- List cards ---")
    for key, (label, _) in SORT_OPTIONS.items():
        print(f"{key}. {label}")
    choice = input("Sort by [1]: ").strip() or "1"

    if choice not in SORT_OPTIONS:
        print("Please choose one of the numbers shown.")
        return

    label, sorter = SORT_OPTIONS[choice]
    print(f"\n{len(cards)} card(s), sorted by {label}:")
    for card in sorter(cards):
        print(format_card(card))


def search_cards_prompt(deck, index):
    """Ask for a search term and show the matching cards."""
    print("\n--- Search cards ---")
    query = input("Search for a word, or the start of one (e.g. mito): ").strip()
    if not query:
        print("Please type something to search for.")
        return

    ids = index.search(query)
    if not ids:
        print("No cards found.")
        return

    print(f"\n{len(ids)} card(s) found:")
    for card_id in ids:
        print(format_card(deck.get_card(card_id)))


def delete_card_prompt(deck, index):
    """Ask for a card ID, confirm, delete the card, then save the deck."""
    print("\n--- Delete a card ---")
    id_text = input("Enter the ID of the card to delete: ").strip()

    try:
        card_id = int(id_text)
    except ValueError:
        print("Please enter a whole number for the ID.")
        return

    card = deck.get_card(card_id)
    if card is None:
        print(f"No card with ID {card_id}.")
        return

    print(format_card(card))
    confirm = input("Delete this card? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled. The card was not deleted.")
        return

    deck.delete_card(card_id)
    index.remove_card(card_id)

    try:
        save_deck(deck, SAVE_FILE)
        print(f"Card {card_id} deleted and saved.")
    except StorageError as error:
        print(f"Card deleted, but the change could not be saved: {error}")


def import_cards_prompt(deck):
    """Ask for a CSV file, import its cards, report the result, then save.

    Returns the number of cards added, so the caller knows whether to rebuild
    the search index.
    """
    print("\n--- Import cards from CSV ---")
    print("Columns (all required): topic, subtopic, question, answer, difficulty")
    path = input("Path to CSV file: ").strip().strip('"')
    if not path:
        print("No file given.")
        return 0

    try:
        result = import_cards_from_csv(deck, path)
    except ImportFileError as error:
        print(f"Import failed: {error}")
        return 0

    print(
        f"Imported {result.added} card(s). "
        f"Skipped {result.skipped_duplicates} duplicate(s). "
        f"{len(result.errors)} row(s) had errors."
    )
    for line, message in result.errors[:10]:
        print(f"  Line {line}: {message}")
    if len(result.errors) > 10:
        print(f"  ...and {len(result.errors) - 10} more.")

    if result.added:
        try:
            save_deck(deck, SAVE_FILE)
            print("Saved.")
        except StorageError as error:
            print(f"Cards were imported, but could not be saved: {error}")

    return result.added


def main():
    try:
        deck = load_deck(SAVE_FILE)
    except StorageError as error:
        print(f"Could not load your saved cards: {error}")
        print("The app has stopped so your save file is not overwritten.")
        return

    index = TrieIndex.from_deck(deck)
    print(f"Loaded {len(deck)} card(s).")

    while True:
        print("\n=== Biology Revision ===")
        print("1. Add a card")
        print("2. List cards")
        print("3. Search cards")
        print("4. Delete a card")
        print("5. Import cards from CSV")
        print("6. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_card_prompt(deck, index)
        elif choice == "2":
            list_cards(deck)
        elif choice == "3":
            search_cards_prompt(deck, index)
        elif choice == "4":
            delete_card_prompt(deck, index)
        elif choice == "5":
            if import_cards_prompt(deck):
                index = TrieIndex.from_deck(deck)   # rebuild so imported cards are searchable
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, 4, 5 or 6.")


if __name__ == "__main__":
    main()