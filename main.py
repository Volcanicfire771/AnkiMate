from Functions.converter import pdf_to_text
from Functions.prompt import prompt

# Converting PDF to text file
pdf_path = "data/Lecture_02 _Climate Change.pdf"
output_txt = "data/lecture.txt"

pdf_to_text(pdf_path, output_txt)

# Converting generated text file to string
with open("data/Lecture.txt", encoding="utf8") as lecture:
    data = lecture.read()

# Prompting Gemini to create flashcards 
cards = prompt(data)


