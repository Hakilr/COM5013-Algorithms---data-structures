from dataclasses import dataclass, asdict


@dataclass
class Card:
    """A single revision flashcard."""

    card_id: int
    topic: str
    question: str
    answer: str
    subtopic: str = ""
    difficulty: int = 1
    due_time: float = 0.0
    interval: float = 60.0
    times_correct: int = 0
    times_wrong: int = 0

    def __post_init__(self):
        if not self.topic.strip():
            raise ValueError("Topic cannot be blank")
        if not self.question.strip():
            raise ValueError("Question cannot be blank")
        if not self.answer.strip():
            raise ValueError("Answer cannot be blank")
        if self.difficulty not in (1, 2, 3):
            raise ValueError("Difficulty must be 1, 2 or 3")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)