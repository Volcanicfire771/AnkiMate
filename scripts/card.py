from dataclasses import dataclass
import json



@dataclass(frozen=True)
class Flashcard:
    question: str
    answer: str


def load_flashcards(data):
    seen_questions = set()
    flashcards = []
    for entry in data.values():
        question = entry["question"]
        if question not in seen_questions:
            seen_questions.add(question)
            flashcards.append(Flashcard(**entry))

    return flashcards

