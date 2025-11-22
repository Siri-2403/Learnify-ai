from helpers.pdf_reader import extract_text_from_pdf
from helpers.ocr import extract_text_from_image

def extract_all_text(uploaded_pdf, uploaded_image, typed_text):
    final = ""

    if uploaded_pdf is not None:
        final += extract_text_from_pdf(uploaded_pdf) + "\n"

    if uploaded_image is not None:
        final += extract_text_from_image(uploaded_image) + "\n"

    if typed_text.strip():
        final += typed_text + "\n"

    return final.strip()
