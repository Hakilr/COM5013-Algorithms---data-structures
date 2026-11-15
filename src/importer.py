import csv
from dataclasses import dataclass, field
from pathlib import Path

from src.card import Card, parse_difficulty

REQUIRED_COLUMNS = {"topic", "subtopic", "question", "answer", "difficulty"}


class ImportFileError(Exception):
    """Raised when a CSV file cannot be read or has the wrong columns."""


@dataclass
class ImportResult:
    added: int = 0
    skipped_duplicates: int = 0
    errors: list = field(default_factory=list)   # (line number, message)


def _duplicate_key(topic, question):
    return (topic.strip().lower(), question.strip().lower())


def import_cards_from_csv(deck, path):
    """Add cards from a CSV file to the deck and return an ImportResult.

    All five columns are required: topic, subtopic, question, answer, difficulty.
    Extra columns are ignored. Bad rows are skipped and reported with their line
    number, and good rows are still imported.

    A hash set of (topic, question) pairs makes the duplicate check O(1) per row,
    so importing m rows into a deck of n cards is O(n + m). Scanning the deck
    for every row would be O(n * m).
    """
    path = Path(path)
    result = ImportResult()

    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ImportFileError(f"{path} is empty")

            columns = {name.strip().lower() for name in reader.fieldnames if name}
            missing = REQUIRED_COLUMNS - columns
            if missing:
                raise ImportFileError(
                    f"Missing column(s): {', '.join(sorted(missing))}"
                )

            existing = {_duplicate_key(c.topic, c.question) for c in deck.all_cards()}
            next_id = max((c.card_id for c in deck.all_cards()), default=0) + 1

            for raw_row in reader:
                row = {
                    key.strip().lower(): (value or "").strip()
                    for key, value in raw_row.items()
                    if key is not None
                }
                line = reader.line_num
                try:
                    card = Card(
                        card_id=next_id,
                        topic=row["topic"],
                        subtopic=row["subtopic"],
                        question=row["question"],
                        answer=row["answer"],
                        difficulty=parse_difficulty(row["difficulty"]),
                    )
                except ValueError as error:
                    result.errors.append((line, str(error)))
                    continue

                key = _duplicate_key(card.topic, card.question)
                if key in existing:
                    result.skipped_duplicates += 1
                    continue

                deck.add_card(card)
                existing.add(key)
                next_id += 1
                result.added += 1

    except (OSError, UnicodeDecodeError, csv.Error) as error:
        raise ImportFileError(f"Could not read {path}: {error}") from error

    return result