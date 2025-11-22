import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("LEARNIFY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_text_from_image(image_file):
    image = Image.open(image_file)

    prompt = "Extract all handwritten or printed text from this image clearly and accurately."

    response = model.generate_content([prompt, image])
    
    return response.text
