from dataclasses import dataclass, fields


def parse_difficulty(text):
    """Convert typed or imported text to a difficulty number (1, 2 or 3)."""
    try:
        return int(str(text).strip())
    except ValueError:
        raise ValueError("Difficulty must be a whole number (1, 2 or 3)") from None


@dataclass
class Card:
    """A single revision flashcard. Topic, subtopic and difficulty are mandatory."""

    card_id: int
    topic: str
    question: str
    answer: str
    subtopic: str
    difficulty: int
    due_time: float = 0.0
    interval: float = 60.0
    times_correct: int = 0
    times_wrong: int = 0

    def __post_init__(self):
        if not self.topic.strip():
            raise ValueError("Topic cannot be blank")
        if not self.subtopic.strip():
            raise ValueError("Subtopic cannot be blank")
        if not self.question.strip():
            raise ValueError("Question cannot be blank")
        if not self.answer.strip():
            raise ValueError("Answer cannot be blank")
        if self.difficulty not in (1, 2, 3):
            raise ValueError("Difficulty must be 1, 2 or 3")

    def to_dict(self):
        """Return the card's fields as a dictionary, ready to save as JSON.

        Builds the dictionary directly from the field names. This replaces
        dataclasses.asdict, which recursively copies every value and was about
        3 to 4 times slower here. All the fields hold simple values (numbers
        and text), so no deep copy is needed.
        """
        return {name: getattr(self, name) for name in _FIELD_NAMES}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


# Worked out once, after the class exists, so to_dict does not look up the
# fields on every call. It stays in step automatically if a field is added.
_FIELD_NAMES = tuple(f.name for f in fields(Card))
