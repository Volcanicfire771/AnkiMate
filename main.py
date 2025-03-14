from scripts.converter import pdf_to_text
from scripts.prompt import prompt
from scripts.anki import add_flashcard, invoke
from scripts.card import load_flashcards
from tqdm import tqdm


deck_name = input("Please enter the name of your deck: (Deck 1) ") or "Deck 1"

# Converting PDF to text file
pdf_path = "data/Lecture_02 _Climate Change.pdf"
output_txt = "data/lecture.txt"

pdf_to_text(pdf_path, output_txt)

# Converting generated text file to string
with open("data/Lecture.txt", encoding="utf8") as lecture:
    data = lecture.read()

# Prompting Gemini to create flashcards 
flashcard_string = prompt(data)
# print(flashcard_string)

def organize_flashcards(flashcard_string):
    flashcard_dict = {}
    # str = flashcard_string.split("Number of flash cards is ")
    cnt = 0
    flashcards = flashcard_string.split("$$$")
    for card in flashcards:
        card = card.strip()
        question = card.split("Q: ", 1)[-1].split("A: ", 1)[0].strip() if "Q: " in card else None
        answer = card.split("A: ", 1)[-1].strip() if "A: " in card else None

        flashcard_dict[cnt] = {"question": question, "answer": answer}
        cnt+=1
    return flashcard_dict
    


flashcard_dict = organize_flashcards(flashcard_string)
invoke('createDeck', deck=deck_name)
flash_cards = load_flashcards(flashcard_dict)
for card in tqdm(flash_cards,desc="Adding Cards",unit="card"):
    add_flashcard(deck_name, card.question, card.answer)



# for card in flashcard_dict:
#     add_flashcard(deck_name, card["question"], card["answer"])

