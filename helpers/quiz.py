import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("LEARNIFY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_quiz(text):
    prompt = (
        "Create 5 MCQs and 5 short-answer questions from the following study material:\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    return response.text

