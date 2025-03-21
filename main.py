from scripts.prompt import prompt
from scripts.anki import add_flashcard, invoke
from scripts.card import load_flashcards
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from scripts.pdf import pdf_to_text
import threading

stop = False

def choose_pdf():
    """Opens a file dialog to choose a PDF file."""
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        filename_label.config(text=filepath)  # Update label with file path
        print(f"Selected PDF: {filepath}")

        # Convert PDF to text
        output_txt = "data/lecture.txt"
        pdf_to_text(filepath, output_txt)

        # Read the generated text file
        try:
            with open(output_txt, encoding="utf8") as lecture:
                data = lecture.read()
                print("PDF converted to text successfully.")
        except FileNotFoundError:
            print("Error: Converted text file not found.")

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

def submit_action():
    """Processes the selected PDF and creates flashcards."""
    selected_pdf = filename_label.cget("text")
    if not selected_pdf or selected_pdf == "No file selected":
        print("No PDF selected!")
        return

    # Convert PDF to text
    output_txt = "data/lecture.txt"
    pdf_to_text(selected_pdf, output_txt)

    try:
        with open(output_txt, encoding="utf8") as lecture:
            data = lecture.read()
    except FileNotFoundError:
        print("Error: Converted text file not found.")
        return

    # Reset Progress bar
    # pb["value"] = 0
    # update_progress_lael(0)b

    # Generate flashcards using Gemini (or AI model)
    flashcard_string = prompt(data)
    flashcard_dict = organize_flashcards(flashcard_string)

    # Get the deck name from input field then create deck
    deck_name = deck_namer.get(1.0, "end-1c")
    invoke('createDeck', deck=deck_name)

    # Load and add flashcards
    flash_cards = load_flashcards(flashcard_dict)
    percent_increase = 100/len(flashcard_dict.keys())
    sum = 0
    for card in tqdm(flash_cards,desc="Adding Cards",unit="card"):
        add_flashcard(deck_name, card.question, card.answer)
        # sum+= percent_increase
        # update_progress_label(sum)
        # if pb["value"] < 100:
            
    messagebox.showinfo(message='Deck Created')
    print("Flashcards added successfully!")

def stop():
    stop = True

def update_progress_label(sum):
    return f"Current Progress: {sum}%"

# Create the main window
root = tk.Tk()
root.title("AnkiMate")
root.minsize(width=500,height=200)

# Create an input field to enter deck name
deckname_label = tk.Label(root, text="Enter deck name", wraplength=400)
deckname_label.pack()
deck_namer = tk.Text(root, height=1, width=20)
deck_namer.pack()
# Create a button to choose the PDF
choose_button = tk.Button(root, text="Choose PDF", command=choose_pdf)
choose_button.pack(pady=10)

# Create a label to display the selected filename
filename_label = tk.Label(root, text="No file selected", wraplength=400)
filename_label.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_action)
submit_button.pack(pady=10)

# Cancel button
cancel_button = tk.Button(root, text= "Cancel", command=stop)
cancel_button.pack()
# Progress bar
# pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=200)
# pb.pack()
# percentage_label = tk.Label(root, text=update_progress_label(0))
# percentage_label.pack()



# Start the Tkinter event loop
root.mainloop()

## TODO: Progress Bar in UI , Window Width and Height , Write deck name as user input in UI , Add stop Button or Cancel, make .exe file