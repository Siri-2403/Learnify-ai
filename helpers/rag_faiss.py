import os
from dotenv import load_dotenv
import google.generativeai as genai
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

load_dotenv()
genai.configure(api_key=os.getenv("LEARNIFY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

embedder = SentenceTransformer("all-MiniLM-L6-v2")


def split_into_chunks(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def build_faiss_index(text):
    chunks = split_into_chunks(text)
    embeddings = embedder.encode(chunks, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks


def retrieve_relevant_chunks(question, index, chunks, top_k=3):
    q_embedding = embedder.encode([question], convert_to_numpy=True)
    distances, ids = index.search(q_embedding, top_k)
    retrieved = [chunks[i] for i in ids[0]]
    return retrieved


def answer_with_faiss(notes, question):
    index, chunks = build_faiss_index(notes)
    relevant_chunks = retrieve_relevant_chunks(question, index, chunks)

    context = "\n\n".join(relevant_chunks)

    prompt = (
        f"Use the following extracted context from the notes to answer the question:\n\n"
        f"{context}\n\n"
        f"QUESTION: {question}"
    )

    response = model.generate_content(prompt)
    return response.text
