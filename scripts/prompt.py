from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')


client = genai.Client(api_key=API_KEY)


def prompt(data):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents= f"""Convert the following text into structured flashcards. Each flashcard should include:
                Q: A clear and concise question
                A: A precise and informative answer
                Use the following structured format for easy parsing:
                Flashcard 1:
                Q: [Question]
                A: [Answer]

                $$$
                Flashcard 2:
                Q: [Question]
                A: [Answer]

                $$$
                ...
                
                text: \n{data}
               """,
    )
    return response.text