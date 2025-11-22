import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("LEARNIFY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_summary(text):
    prompt = f"Summarize this into clean, structured bullet notes:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
