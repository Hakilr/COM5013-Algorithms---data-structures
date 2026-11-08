from src.card import Card
from src.deck import Deck


def next_card_id(deck):
    """Return an unused ID: one more than the largest existing ID."""
    ids = [card.card_id for card in deck.all_cards()]
    return max(ids, default=0) + 1


def add_card_prompt(deck):
    """Ask the user for card details, then add the card to the deck."""
    print("\n--- Add a new card ---")
    topic = input("Topic (e.g. Cells and control): ")
    subtopic = input("Subtopic (optional, press Enter to skip): ")
    question = input("Question: ")
    answer = input("Answer: ")
    difficulty_text = input("Difficulty (1 = easy, 2 = medium, 3 = hard) [1]: ")

    try:
        difficulty = int(difficulty_text) if difficulty_text.strip() else 1
        card = Card(
            card_id=next_card_id(deck),
            topic=topic,
            subtopic=subtopic,
            question=question,
            answer=answer,
            difficulty=difficulty,
        )
        deck.add_card(card)
        print(f"Card {card.card_id} added.")
    except ValueError as error:
        print(f"Could not add card: {error}")


def list_cards(deck):
    """Print every card in the deck."""
    cards = deck.all_cards()
    if not cards:
        print("\nThe deck is empty.")
        return
    print()
    for card in cards:
        print(f"[{card.card_id}] {card.topic} | Q: {card.question} | A: {card.answer}")


def main():
    deck = Deck()
    while True:
        print("\n=== Biology Revision ===")
        print("1. Add a card")
        print("2. List cards")
        print("3. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_card_prompt(deck)
        elif choice == "2":
            list_cards(deck)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()