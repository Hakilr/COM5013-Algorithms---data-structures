from pathlib import Path

from src.card import Card, parse_difficulty
from src.importer import ImportFileError, import_cards_from_csv
from src.storage import StorageError, load_deck, save_deck

SAVE_FILE = Path(__file__).resolve().parent.parent / "deck.json"


def next_card_id(deck):
    """Return an unused ID: one more than the largest existing ID."""
    ids = [card.card_id for card in deck.all_cards()]
    return max(ids, default=0) + 1


def add_card_prompt(deck):
    """Ask the user for card details, add the card, then save the deck."""
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

    try:
        save_deck(deck, SAVE_FILE)
        print(f"Card {card.card_id} added and saved.")
    except StorageError as error:
        print(f"Card added, but it could not be saved: {error}")


def list_cards(deck):
    """Print every card in the deck."""
    cards = deck.all_cards()
    if not cards:
        print("\nThe deck is empty.")
        return
    print()
    for card in cards:
        print(
            f"[{card.card_id}] {card.topic} > {card.subtopic} "
            f"(difficulty {card.difficulty}) | Q: {card.question} | A: {card.answer}"
        )


def delete_card_prompt(deck):
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

    print(
        f"[{card.card_id}] {card.topic} > {card.subtopic} "
        f"(difficulty {card.difficulty}) | Q: {card.question} | A: {card.answer}"
    )
    confirm = input("Delete this card? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled. The card was not deleted.")
        return

    deck.delete_card(card_id)

    try:
        save_deck(deck, SAVE_FILE)
        print(f"Card {card_id} deleted and saved.")
    except StorageError as error:
        print(f"Card deleted, but the change could not be saved: {error}")


def import_cards_prompt(deck):
    """Ask for a CSV file, import its cards, report the result, then save."""
    print("\n--- Import cards from CSV ---")
    print("Columns (all required): topic, subtopic, question, answer, difficulty")
    path = input("Path to CSV file: ").strip().strip('"')
    if not path:
        print("No file given.")
        return

    try:
        result = import_cards_from_csv(deck, path)
    except ImportFileError as error:
        print(f"Import failed: {error}")
        return

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


def main():
    try:
        deck = load_deck(SAVE_FILE)
    except StorageError as error:
        print(f"Could not load your saved cards: {error}")
        print("The app has stopped so your save file is not overwritten.")
        return

    print(f"Loaded {len(deck)} card(s).")

    while True:
        print("\n=== Biology Revision ===")
        print("1. Add a card")
        print("2. List cards")
        print("3. Delete a card")
        print("4. Import cards from CSV")
        print("5. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_card_prompt(deck)
        elif choice == "2":
            list_cards(deck)
        elif choice == "3":
            delete_card_prompt(deck)
        elif choice == "4":
            import_cards_prompt(deck)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, 4 or 5.")


if __name__ == "__main__":
    main()